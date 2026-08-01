# payloads/

Directory stores generated payload files (reverse shells, exploits, binaries).

## Naming convention

`<target>_<type>_<port>.<ext>`

- `target`: Target host IP or hostname (dots replaced with underscores)
- `type`: Payload type (e.g. `revshell`, `bind`, `dll`, `exe`, `ps1`)
- `port`: Listener port

## Examples

```
10.10.11.5_revshell_4444.py
dc01_bind_5985.ps1
fileserver_dll_8080.dll
```

## Security warning

These are offensive security tools. All files in this directory implement
exploit delivery, remote access, or privilege escalation capabilities.
Handle responsibly:

- Never expose generated payloads to untrusted environments
- Delete payloads from this directory after each engagement
- Never commit payloads to version control

## Git

Files in this directory are gitignored by the top-level `.gitignore`.
