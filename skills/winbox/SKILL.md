---
name: winbox
description: "WinBox — isolated Windows vulnerability-research lab inside LazyOwn. VM lifecycle, SYSTEM guest execution, defense posture, hypervisor debugging, scored gym matrix and the Windows APT chain via CLI, MCP and autonomous loop."
version: 1.0.0
author: grisun0
license: AGPL-3.0-only
platforms: [linux]
metadata:
  hermes:
    tags: [redteam, pentest, windows, lab, mcp, winbox, vulnerability-research]
    homepage: https://github.com/grisuno/LazyOwn
    related_skills: [lazyown, lazyaddon-creator]
---

# WinBox Lab Skill

You are operating the WinBox lab: a headless Windows VM (Server Core 2022/2025,
Windows 11 or Windows 10) controlled from the operator host through the
[totekuh/winbox](https://github.com/totekuh/winbox) CLI, integrated into
LazyOwn as a first-class Red Team Gym scenario (`scenario: winbox`).

- **Shell command**: `winbox <action>` (module: `modules/winbox_gym.py`, CommandSet: `cli/commands/winbox_gym.py`)
- **Gym catalogue**: `playbooks/gym_winbox.yaml` + `exploits/winbox_*.yaml` + `chains/gym_winbox_*.yaml`
- **Gym definitions**: `gyms/winbox_*.yaml`
- **Lazyaddon**: `lazyaddons/winbox.yaml` (upstream repo under `external/.exploit/winbox`)
- **MCP**: 9 `lazyown_winbox_*` tools in `skills/lazyown_mcp.py`, plus the upstream `winbox mcp` server (97 tools)

## Hard rules

1. The lab VM is for vulnerability research in isolation. Never point WinBox
   at production infrastructure. The gym runs are confined to the libvirt
   domain the winbox CLI manages.
2. Destructive posture changes (Defender/AppLocker disable, net unplug,
   destroy, eventlogs clear) require an explicit confirm token (`-y`/`--yes`)
   in the shell command.
3. Snapshots are the rollback plan: `winbox snapshot pre-attack` before
   flipping defenses or running unknown binaries; `winbox restore <name>`
   to return to clean state.
4. All evidence lands in `sessions/winbox/` (CLI transcripts) and
   `sessions/ctf/<vector_id>/` (scored captures).

## One-time setup (automatic)

`winbox up` and `gym start winbox_*` do ALL of this idempotently in one
command: clone the upstream repo into `external/.exploit/winbox`,
`pip install -e .`, install missing host packages through
`sudo -n apt-get install -y ...` (guidance when sudo needs a password),
download the guest ISO (~4.7 GB, resumable), build and provision the VM
(~20 min), boot the guest and bind `rhost` to the VM IP. Re-running it
skips every satisfied stage.

The lazyaddon `install_command` mirrors the host-package install so a
manual addon install covers prerequisites too:

```bash
sudo apt-get install -y qemu-system-x86 qemu-utils libvirt-daemon-system virtinst \
    libguestfs-tools virtiofsd p7zip-full genisoimage sshpass wget libwin-hivex-perl
winbox tools add Rubeus.exe SharpHound.exe
```

## Session flow (agent)

1. **Bootstrap and bind**: `winbox up` (or `gym start winbox_windows_apt`)
   brings the whole lab to attackable state — installs repo + host deps,
   downloads ISO and builds the VM only when missing, boots the guest and
   mirrors the VM IP into `payload.json` rhost. Check with `winbox status`
   or `lazyown_winbox_status` (MCP): if not ready, report the printed
   setup steps and stop — never install unprompted beyond `winbox up`.
2. **Recon**: `lazynmap` reuses `sessions/scan_<ip>.nmap.xml` when present.
   SMB and RDP vectors fingerprint the guest (`winbox_smb_enum`,
   `winbox_rdp_probe`).
3. **Execution**: `winbox exec --timeout 120 whoami` runs as SYSTEM.
   Background jobs: `winbox exec --bg --log <tool>` then `winbox jobs list`.
4. **Posture**: `winbox av status` / `winbox applocker status` are
   bidirectional — flip on to test bypass tools, flip off for fast triage.
5. **Evidence**: `winbox eventlogs --since 1h --max 50` shows what the
   guest logged about the run (OPSEC hygiene), stored in `sessions/winbox/`.
6. **Containment**: `winbox net isolate` (block internet, keep host channels)
   or `winbox net unplug -y` (full air-gap); `winbox snapshot pre-attack`
   before detonation work.

## Scored gym matrix

```bash
winbox gym list              # catalogue summary + validation
winbox gym plan              # ordered plan from rhost
winbox gym run               # one chain per vector, captures into sessions/ctf
winbox gym report            # capture summary
winbox gym verify winbox_system_exec
```

Vectors: `winbox_smb_enum` (T1135), `winbox_rdp_probe` (T1021.001),
`winbox_system_exec` (T1059.003), `winbox_defender_posture` (T1562.001),
`winbox_eventlogs_evidence` (T1070.002).

Start a scored run through the standard gym pipeline:
`gym start winbox_first_shell` or `gym start winbox_windows_apt`.

## Autonomous loop and APT chain

The lab is attackable by the same engines as Metasploitable 2:

```bash
assign rhost <vm-ip>
auto_loop --rounds 5 "attack the isolated WinBox Windows lab: map services, prove guest-agent execution, review defenses and collect evidence"
apt_chain apt_winbox_windows <vm-ip>
```

`apt_winbox_windows` runs the Windows golden path: bind, VM up, resolve,
scan, SMB/RDP mapping, exploit sweep, SYSTEM execution, posture review,
LockBit playbook emulation, event-log evidence, sync, snapshot. Deep
research (kernel debugging, protected memory, named pipes, IOCTLs) goes
through the upstream `winbox mcp` 97-tool server instead of shell verbs.

## MCP tool reference (LazyOwn)

| Tool | Purpose |
|------|---------|
| `lazyown_winbox_status` | Readiness + VM state + loop attackability |
| `lazyown_winbox_vm` | bootstrap / up / down / suspend / status |
| `lazyown_winbox_exec` | SYSTEM or per-user guest command |
| `lazyown_winbox_tools` | list / add / remove guest tools |
| `lazyown_winbox_eventlogs` | Query Security/Sysmon/Defender logs |
| `lazyown_winbox_snapshot` | list / create / restore rollback points |
| `lazyown_winbox_gym_list` | Catalogue summary + matrix validation |
| `lazyown_winbox_gym_plan` | Ordered attack plan |
| `lazyown_winbox_gym_run` | Scored matrix run with captures |

## Troubleshooting

- **winbox binary missing** → run `winbox up` (auto-clones to
  `external/.exploit/winbox` and pip-installs); for the MCP surface use
  `lazyown_winbox_vm` with `action=bootstrap`.
- **sudo password required for apt** → the bootstrap prints the exact
  manual command: `sudo apt-get install -y <packages>`. Run it once and
  re-run `winbox up`.
- **VM IP unknown** → `winbox up` then `winbox resolve`; the status regex
  reads the `IP:` line of `winbox status`.
- **Chain steps skipped with unresolved token** → pass `--target` or set
  rhost before running the matrix.
- **Guest wedged** → `winbox down --force` then `winbox restore pre-attack`.
