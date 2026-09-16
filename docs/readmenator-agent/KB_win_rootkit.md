# Subsystem: win_rootkit

## modules/win_rootkit/backup.c
- Layer: utility
- Doc: include <stdio.h> include <stdlib.h> include <string.h> include <unistd.h> include <winsock2.h> include <windows.h> incl
- Language: c
- Symbols:
  - `elp` (function, line 63) `void elp()`
  - `ensure_pid_file_exists` (function, line 85) `void ensure_pid_file_exists()`
  - `ensure_key_file_exists` (function, line 122) `void ensure_key_file_exists()`
  - `ensure_hide_file_exists` (function, line 149) `void ensure_hide_file_exists()`
  - `infect_command` (function, line 178) `void infect_command()`
  - `handle_client` (function, line 203) `DWORD WINAPI handle_client(LPVOID client_socket)`
  - `monitor_shell` (function, line 428) `DWORD WINAPI monitor_shell(LPVOID data)`
  - `main` (function, line 540) `int main()`
  - `PORT` (macro, line 16)
  - `BUFFER_SIZE` (macro, line 18)
  - `MAX_COMMANDS` (macro, line 19)
  - `PID_FILE` (macro, line 20)
  - `HIDE_FILE` (macro, line 21)
  - `KEY_FILE` (macro, line 22)
  - `PASSWORD` (macro, line 24)

## modules/win_rootkit/mrhyde.c
- Layer: utility
- Doc: include <windows.h> include <stdio.h> include <stdlib.h> include <string.h> include <tlhelp32.h>  define MAX_HIDE_PIDS 1
- Language: c
- Symbols:
  - `RunExperiment` (function, line 19) `void __cdecl RunExperiment()`
  - `load_hidden_pids` (function, line 23) `void load_hidden_pids()`
  - `load_hidden_files` (function, line 46) `void load_hidden_files()`
  - `FindProcessId` (function, line 89) `DWORD FindProcessId(const char* processName)`
  - `HideProcessByPID` (function, line 114) `void HideProcessByPID(DWORD pid)`
  - `search_pid` (function, line 136) `BOOL search_pid()`
  - `should_hide_pid` (function, line 147) `BOOL should_hide_pid(DWORD pid)`
  - `should_hide_file` (function, line 159) `BOOL should_hide_file(const char* filename)`
  - `HookedFindFirstFile` (function, line 171) `HANDLE WINAPI HookedFindFirstFile(LPCSTR lpFileName, LPWIN32_FIND_DATA lpFindFileData)`
  - `HookedFindNextFile` (function, line 180) `BOOL WINAPI HookedFindNextFile(HANDLE hFindFile, LPWIN32_FIND_DATA lpFindFileData)`
  - `HookedCreateToolhelp32Snapshot` (function, line 189) `HANDLE WINAPI HookedCreateToolhelp32Snapshot(DWORD dwFlags, DWORD th32ProcessID)`
  - `HookedProcess32First` (function, line 198) `BOOL WINAPI HookedProcess32First(HANDLE hSnapshot, LPPROCESSENTRY32 lppe)`
  - `HookedProcess32Next` (function, line 210) `BOOL WINAPI HookedProcess32Next(HANDLE hSnapshot, LPPROCESSENTRY32 lppe)`
  - `HookFunctions` (function, line 222) `void HookFunctions()`
  - `DllMain` (function, line 271) `BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)`
  - `MAX_HIDE_PIDS` (macro, line 6)
  - `PID_FILE_PATH` (macro, line 8)
  - `FILE_HIDE_PATH` (macro, line 9)

## modules/win_rootkit/win_rin3_rootkit.cs
- Layer: utility
- Language: cs
- Symbols:
  - `WinRing3Rootkit` (class, line 30)
  - `WIN32_FIND_DATA` (class, line 47)
  - `SECURITY_ATTRIBUTES` (class, line 64)
  - `TOKEN_USER` (class, line 123)
  - `SID_AND_ATTRIBUTES` (class, line 129)
  - `SID` (class, line 136)
  - `GetUsernameFromPid` (method, line 143)
  - `ShouldHidePid` (method, line 201)
  - `HookFindFirstFile` (method, line 212)
  - `HookCreateFile` (method, line 224)

## modules/win_rootkit/win_ring3_rootkit.c
- Layer: utility
- Doc: include <stdio.h> include <stdlib.h> include <string.h> include <unistd.h> include <winsock2.h> include <windows.h> incl
- Language: c
- Symbols:
  - `DownloadDLL` (function, line 78) `BOOL DownloadDLL(const char* url, PBYTE* buffer, DWORD* size)`
  - `ReflectiveLoadDLL` (function, line 98) `BOOL ReflectiveLoadDLL(PBYTE dllBuffer, DWORD dllSize)`
  - `initPIDArray` (function, line 146) `void initPIDArray(PIDArray *array)`
  - `addPID` (function, line 153) `void addPID(PIDArray *array, DWORD pid)`
  - `freePIDArray` (function, line 162) `void freePIDArray(PIDArray *array)`
  - `getPIDsFromTasklist` (function, line 165) `void getPIDsFromTasklist(PIDArray *pidArray)`
  - `AddDllToAppInitDLLs` (function, line 190) `BOOL AddDllToAppInitDLLs(const char* dllPath)`
  - `GetProcessIdByName` (function, line 238) `DWORD GetProcessIdByName(const char* processName)`
  - `Gifted` (function, line 268) `BOOL Gifted(DWORD processId, const char* dllPath)`
  - `elp` (function, line 361) `void elp()`
  - `ensure_pid_file_exists` (function, line 381) `void ensure_pid_file_exists()`
  - `ensure_key_file_exists` (function, line 418) `void ensure_key_file_exists()`
  - `ensure_hide_file_exists` (function, line 445) `void ensure_hide_file_exists()`
  - `giveGift` (function, line 474) `BOOL giveGift()`
  - `handle_client` (function, line 524) `DWORD WINAPI handle_client(LPVOID client_socket)`
  - `monitor_shell` (function, line 753) `DWORD WINAPI monitor_shell(LPVOID data)`
  - `main` (function, line 865) `int main()`
  - `PORT` (macro, line 17)
  - `BUFFER_SIZE` (macro, line 19)
  - `MAX_COMMANDS` (macro, line 20)
  - `PID_FILE` (macro, line 21)
  - `HIDE_FILE` (macro, line 22)
  - `KEY_FILE` (macro, line 23)
  - `PASSWORD` (macro, line 25)

## modules/win_rootkit/win_ring3_rootkit.cpp
- Layer: utility
- Language: cpp
- Symbols:
  - `get_username_from_pid` (function, line 41) `char* get_username_from_pid(DWORD pid)`
  - `should_hide_pid` (function, line 64) `int should_hide_pid(const char* pid)`
  - `hook_FindFirstFile` (function, line 75) `HANDLE WINAPI hook_FindFirstFile(CONST char* path, WIN32_FIND_DATA* find_data)`
  - `hook_CreateFile` (function, line 85) `HANDLE WINAPI hook_CreateFile(CONST char* path, DWORD access, DWORD share, LPSECURITY_ATTRIBUTES ...`
  - `DllMain` (function, line 93) `BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)`
  - `HIDDEN_DIR` (macro, line 31)
  - `HIDDEN_FILE` (macro, line 33)
  - `HIDE_USER` (macro, line 34)
  - `MAX_HIDE_PIDS` (macro, line 35)
