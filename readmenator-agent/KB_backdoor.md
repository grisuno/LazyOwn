# Subsystem: backdoor

## modules/backdoor/backdoor.c
- Layer: utility
- Language: c
- Symbols:
  - `bootRun` (function, line 18) `int bootRun()`
  - `str_cut` (function, line 49) `char *
str_cut(char str[], int slice_from, int slice_to)`
  - `Shell` (function, line 84) `void Shell()`
  - `WinMain` (function, line 125) `int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrev, LPSTR lpCmdLine, int nCmdShow)`
  - `bzero` (macro, line 14) `#define bzero(p, size)`
- Depends on: `modules/backdoor/keylogger.h`

## modules/backdoor/keylogger.h
- Layer: infrastructure
- Language: h
- Symbols:
  - `logg` (function, line 1) `DWORD WINAPI logg(LPVOID lpParam)`
- Imported by: `modules/backdoor/backdoor.c`

## modules/backdoor/server.c
- Layer: utility
- Language: c
- Symbols:
  - `main` (function, line 10) `int main()`
- Imported by: `cli/commands/dns_exfil.py`, `cli/commands/phishing_wizard.py`, `lazyc2.py`, `modules/lazyown_bprfuzzer.py`, `modules/legacy/lazygalazy.py`, `modules/legacy/lazyhttpreverseshell.py`, `skills/hermes-lazyown/mcp_server.py`, `skills/lazyown_mcp.py`, `skills/lazyown_mcp_opencode.py`, `utils.py`
