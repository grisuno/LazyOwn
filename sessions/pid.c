#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main(void) {
    printf("PID: %d\n", getpid()); //PID to be injected

    while (1) {
        continue;
    }

    return 0;
}