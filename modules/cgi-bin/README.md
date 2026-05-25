# CGI-Bin Web Shells

Minimal web shells for quick deployment on compromised web servers.

## Contents

| File | Language | Notes |
|------|----------|-------|
| `lazywebshell.asp` | ASP (IIS) | Classic ASP reverse shell. |
| `lazywebshell.cgi` | Perl CGI | Platform-agnostic CGI shell. |
| `lazywebshell.py` | Python WSGI | Python-based web shell with minimal dependencies. |
| `lazywebshell.sh` | Bash CGI | POSIX shell CGI for *nix hosts. |

## Usage

Upload the appropriate file to a web-accessible directory (e.g., `cgi-bin/`) and interact via HTTP requests. The CLI command `do_createwebshell` automates payload selection and upload based on the detected server stack.

## Warning

These files contain raw shell commands. Do not leave them on disk longer than necessary; use `do_cleanlogs` and `do_removewebshell` to erase traces after the operation.
