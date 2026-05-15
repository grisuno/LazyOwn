# tools

Pwntomate service-triggered job files. Each `.tool` file defines a command
that runs automatically when nmap discovers a specific port or service on a
target. The pwntomate engine reads these files at scan time and dispatches the
right tool for each open port.

## How it works

1. `do_lazynmap` finishes and writes `sessions/scan_<rhost>.nmap.xml`.
2. The pwntomate engine reads the XML and walks each open port.
3. For each port, it looks up matching `.tool` files by service name and port
   number.
4. Matched jobs are queued and executed sequentially. Output lands in
   `sessions/<ip>/<port>/<tool>/*.txt`.

## File format

Each `.tool` file is a plain text file containing a shell command template.
Placeholder tokens are substituted at run time:

| Token | Value |
|-------|-------|
| `{rhost}` | Target IP |
| `{rport}` | Target port |
| `{lhost}` | Attacker IP |
| `{lport}` | Reverse-shell listener port |
| `{domain}` | Target domain |
| `{wordlist}` | Directory brute-force wordlist path |

Example (`dirb.tool`):
```
dirb http://{rhost}:{rport}/ {wordlist} -o sessions/{rhost}/{rport}/dirb/output.txt
```

## Current tools (69 files)

Categories of coverage:

- Web content discovery: `dirb.tool`, `dirb_domain.tool`
- DNS enumeration: `dig.tool`, `dig-reverse.tool`, `dnsenum.tool`
- SMB: `crackmapexec-smb.tool`, `crackmapexec-ldap.tool`
- Kerberos / AD: `asrep_roast.tool`, `bloodhound-python.tool`
- General: `bigbang.tool` (runs a curated set of tools for the service in one pass)

## Adding a tool

1. Create `tools/<service_or_port>.tool` with the command template.
2. Use only the substitution tokens listed above.
3. Write output to `sessions/{rhost}/{rport}/<toolname>/` so the bridge
   selector and evidence grep can find it.
4. Do not add infinite-loop or destructive commands — tools run unattended.

## Output location

All pwntomate output lands under `sessions/<target_ip>/<port>/<tool>/`.
The `bridge_suggest` and `threat_model` MCP tools read from this tree.
