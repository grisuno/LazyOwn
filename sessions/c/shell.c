#include <stdio.h>
#include <string.h>
unsigned char shellcode[] = "{shellcode}";
int main() {
    void (*ret)() = (void(*)())shellcode;
    ret();
    return 0;
}
