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
  - `bzero` (macro, line 13)

## modules/backdoor/keylogger.h
- Layer: infrastructure
- Language: h
- Symbols:
  - `logg` (function, line 1) `DWORD WINAPI logg(LPVOID lpParam)`

## modules/backdoor/server.c
- Layer: utility
- Doc: include <stdio.h> include <sys/types.h> include <sys/socket.h> include <netinet/in.h> include <stdlib.h> include <string
- Language: c
- Symbols:
  - `main` (function, line 9) `int main()`
- Imported by: `cli/commands/dns_exfil.py`, `cli/commands/phishing_wizard.py`, `lazyc2.py`, `modules/lazyown_bprfuzzer.py`, `modules/legacy/lazygalazy.py`, `modules/legacy/lazyhttpreverseshell.py`, `skills/hermes-lazyown/mcp_server.py`, `skills/lazyown_mcp.py`, `skills/lazyown_mcp_opencode.py`, `utils.py`
