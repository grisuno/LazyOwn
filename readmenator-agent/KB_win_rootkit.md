# Subsystem: win_rootkit

## modules/win_rootkit/backup.c
- Layer: utility
- Language: c
- Symbols:
  - `Command` (struct, line 27)
  - `VirtualFile` (struct, line 33)
  - `elp` (function, line 66) `void elp()`
  - `ensure_pid_file_exists` (function, line 86) `void ensure_pid_file_exists()`
  - `ensure_key_file_exists` (function, line 123) `void ensure_key_file_exists()`
  - `ensure_hide_file_exists` (function, line 150) `void ensure_hide_file_exists()`
  - `infect_command` (function, line 179) `void infect_command()`
  - `handle_client` (function, line 204) `DWORD WINAPI handle_client(LPVOID client_socket)`
  - `monitor_shell` (function, line 430) `DWORD WINAPI monitor_shell(LPVOID data)`
  - `main` (function, line 540) `int main()`
  - `PORT` (macro, line 17) `#define PORT`
  - `BUFFER_SIZE` (macro, line 18) `#define BUFFER_SIZE`
  - `MAX_COMMANDS` (macro, line 19) `#define MAX_COMMANDS`
  - `PID_FILE` (macro, line 20) `#define PID_FILE`
  - `HIDE_FILE` (macro, line 21) `#define HIDE_FILE`
  - `KEY_FILE` (macro, line 22) `#define KEY_FILE`
  - `PASSWORD` (macro, line 24) `#define PASSWORD`

## modules/win_rootkit/mrhyde.c
- Layer: utility
- Language: c
- Symbols:
  - `RunExperiment` (function, line 19) `void __cdecl RunExperiment()`
  - `load_hidden_pids` (function, line 24) `void load_hidden_pids()`
  - `load_hidden_files` (function, line 47) `void load_hidden_files()`
  - `FindProcessId` (function, line 89) `DWORD FindProcessId(const char* processName)`
  - `HideProcessByPID` (function, line 115) `void HideProcessByPID(DWORD pid)`
  - `search_pid` (function, line 137) `BOOL search_pid()`
  - `should_hide_pid` (function, line 147) `BOOL should_hide_pid(DWORD pid)`
  - `should_hide_file` (function, line 161) `BOOL should_hide_file(const char* filename)`
  - `HookedFindFirstFile` (function, line 171) `HANDLE WINAPI HookedFindFirstFile(LPCSTR lpFileName, LPWIN32_FIND_DATA lpFindFileData)`
  - `HookedFindNextFile` (function, line 180) `BOOL WINAPI HookedFindNextFile(HANDLE hFindFile, LPWIN32_FIND_DATA lpFindFileData)`
  - `HookedCreateToolhelp32Snapshot` (function, line 189) `HANDLE WINAPI HookedCreateToolhelp32Snapshot(DWORD dwFlags, DWORD th32ProcessID)`
  - `HookedProcess32First` (function, line 198) `BOOL WINAPI HookedProcess32First(HANDLE hSnapshot, LPPROCESSENTRY32 lppe)`
  - `HookedProcess32Next` (function, line 210) `BOOL WINAPI HookedProcess32Next(HANDLE hSnapshot, LPPROCESSENTRY32 lppe)`
  - `HookFunctions` (function, line 222) `void HookFunctions()`
  - `DllMain` (function, line 272) `BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)`
  - `MAX_HIDE_PIDS` (macro, line 7) `#define MAX_HIDE_PIDS`
  - `PID_FILE_PATH` (macro, line 8) `#define PID_FILE_PATH`
  - `FILE_HIDE_PATH` (macro, line 9) `#define FILE_HIDE_PATH`

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
- Language: c
- Symbols:
  - `Command` (struct, line 28)
  - `VirtualFile` (struct, line 34)
  - `PIDArray` (struct, line 40)
  - `DownloadDLL` (function, line 79) `BOOL DownloadDLL(const char* url, PBYTE* buffer, DWORD* size)`
  - `ReflectiveLoadDLL` (function, line 99) `BOOL ReflectiveLoadDLL(PBYTE dllBuffer, DWORD dllSize)`
  - `initPIDArray` (function, line 146) `void initPIDArray(PIDArray *array)`
  - `addPID` (function, line 153) `void addPID(PIDArray *array, DWORD pid)`
  - `freePIDArray` (function, line 162) `void freePIDArray(PIDArray *array)`
  - `getPIDsFromTasklist` (function, line 166) `void getPIDsFromTasklist(PIDArray *pidArray)`
  - `AddDllToAppInitDLLs` (function, line 191) `BOOL AddDllToAppInitDLLs(const char* dllPath)`
  - `GetProcessIdByName` (function, line 240) `DWORD GetProcessIdByName(const char* processName)`
  - `Gifted` (function, line 270) `BOOL Gifted(DWORD processId, const char* dllPath)`
  - `elp` (function, line 362) `void elp()`
  - `ensure_pid_file_exists` (function, line 382) `void ensure_pid_file_exists()`
  - `ensure_key_file_exists` (function, line 419) `void ensure_key_file_exists()`
  - `ensure_hide_file_exists` (function, line 446) `void ensure_hide_file_exists()`
  - `giveGift` (function, line 475) `BOOL giveGift()`
  - `handle_client` (function, line 526) `DWORD WINAPI handle_client(LPVOID client_socket)`
  - `monitor_shell` (function, line 755) `DWORD WINAPI monitor_shell(LPVOID data)`
  - `main` (function, line 865) `int main()`
  - `PORT` (macro, line 18) `#define PORT`
  - `BUFFER_SIZE` (macro, line 19) `#define BUFFER_SIZE`
  - `MAX_COMMANDS` (macro, line 20) `#define MAX_COMMANDS`
  - `PID_FILE` (macro, line 21) `#define PID_FILE`
  - `HIDE_FILE` (macro, line 22) `#define HIDE_FILE`
  - `KEY_FILE` (macro, line 23) `#define KEY_FILE`
  - `PASSWORD` (macro, line 25) `#define PASSWORD`

## modules/win_rootkit/win_ring3_rootkit.cpp
- Layer: utility
- Language: cpp
- Symbols:
  - `get_username_from_pid` (function, line 42) `char* get_username_from_pid(DWORD pid)`
  - `should_hide_pid` (function, line 65) `int should_hide_pid(const char* pid)`
  - `hook_FindFirstFile` (function, line 75) `HANDLE WINAPI hook_FindFirstFile(CONST char* path, WIN32_FIND_DATA* find_data)`
  - `hook_CreateFile` (function, line 85) `HANDLE WINAPI hook_CreateFile(CONST char* path, DWORD access, DWORD share, LPSECURITY_ATTRIBUTES ...`
  - `DllMain` (function, line 94) `BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)`
  - `HIDDEN_DIR` (macro, line 32) `#define HIDDEN_DIR`
  - `HIDDEN_FILE` (macro, line 33) `#define HIDDEN_FILE`
  - `HIDE_USER` (macro, line 34) `#define HIDE_USER`
  - `MAX_HIDE_PIDS` (macro, line 35) `#define MAX_HIDE_PIDS`
