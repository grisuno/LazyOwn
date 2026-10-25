# Subsystem: backdoor

## modules/backdoor/backdoor.c
- Layer: utility
- Language: c
- Symbols:
  - `bootRun` (function, line 22) `int bootRun()`
  - `str_cut` (function, line 53) `char *
str_cut(char str[], int slice_from, int slice_to)`
  - `Shell` (function, line 88) `void Shell()`
  - `WinMain` (function, line 129) `int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrev, LPSTR lpCmdLine, int nCmdShow)`
  - `bzero` (macro, line 14) `#define bzero(p, size)`
  - `RUNKEY_NAME` (macro, line 17) `#define RUNKEY_NAME`
- Depends on: `modules/backdoor/keylogger.h`

## modules/backdoor/keylogger.h
- Layer: utility
- Language: h
- Symbols:
  - `logg` (function, line 1) `DWORD WINAPI logg(LPVOID lpParam)`
- Imported by: `modules/backdoor/backdoor.c`

## modules/backdoor/server.c
- Layer: utility
- Language: c
- Symbols:
  - `main` (function, line 10) `int main()`
- Imported by: `cli/commands/dns_exfil.py`, `cli/commands/phishing_wizard.py`, `contrib/legacy/lazygalazy.py`, `contrib/legacy/lazyhttpreverseshell.py`, `lazyc2.py`, `modules/lazy_proxy.py`, `modules/lazyown_bprfuzzer.py`, `skills/hermes-lazyown/mcp_server.py`, `skills/lazyown_mcp.py`, `skills/lazyown_mcp_opencode.py`, `tests/test_lazy_proxy.py`, `utils.py`
