# Metasploitable 2 Gym

I keep one exploit, one chain and one index entry for every
Metasploitable 2 vector I emulate. The index is
`playbooks/gym_metasploitable.yaml`; the loader is
`modules/metasploitable_gym.py`; the runtime artefacts are the normal
`exploits/*.yaml` and `chains/*.yaml` files.

## Matrix

The shipped index covers 45 vectors:

- FTP: vsftpd 2.3.4 backdoor, ProFTPD anonymous.
- SSH, Telnet, SMTP, DNS, rlogin.
- SMB: Samba username map script.
- Web and OWASP: phpMyAdmin, DVWA SQLi/blind SQLi, reflected/stored/DOM
  XSS, CSRF, LFI, file upload, brute force, command injection,
  Mutillidae XSS/LFI/RFI/command injection/CSRF, PHP-CGI argument
  injection, TWiki XSS, Axis2, WebDAV PUT, Apache TRACE, Shellshock,
  Tomcat Manager.
- Remote services: Java RMI, ingreslock, UnrealIRCd, distcc.
- Data and desktop: NFS exports, MySQL root, PostgreSQL default,
  VNC, X11.

Every entry names its `exploit` id and `chain` name. The validator
refuses a matrix where either file is missing or the chain defaults do
not match.

## Commands

```bash
gym_ms2 list
gym_ms2 chains
gym_ms2 validate
chain list gym
gym_ms2 info ms2_distcc_exec
gym_ms2 chain ms2_distcc_exec
apt_chain gym_metasploitable_ms2_distcc_exec 172.17.0.2
apt_chain gym_metasploitable_ms2_distcc_exec 172.17.0.2 --dry-run
```

The per-vulnerability chain inherits `gym_metasploitable_chain`:

1. bind the target (`assign target`);
2. scan once (`lazynmap`, skipped when the XML exists);
3. run the selected YAML exploit with `--feed`;
4. mirror the loop graphs (`lazy_sync`);
5. refresh the session report (`create_session_json`);
6. open the interactive shell (`atomic_shell --interactive`).

Every exploit outcome goes through `atomic_exploit_bridge.record_outcome`
and the outcome bus, so the world model, kill-chain, intel graph, attack
graph, C2 banners/CVEs/notes, objectives and report stay current.

## Lab

```bash
lab start metasploitable
# prints the container IP and the assign command, and starts Apache
assign rhost <container-ip>
gym start metasploitable_full_chain
apt_chain gym_metasploitable_ms2_tomcat_manager <container-ip>
```

The Docker lab maps the container ports; the classic VM flow lives in
`scripts/lazy_msf_lab.sh`. Both are lab-only and in-scope targets only.

## Gym catalogue and run state

The gamified gym catalogue lives in `gyms/*.yaml` (one file per gym).
`lazy_orchestrator` exposes the same catalogue in its **Gyms** tab:
`space` starts the selected gym (or stops its active runs), `a` creates a
definition, `e` edits the raw YAML with validation, and `d` deletes it
after confirmation. A definition with active runs cannot be deleted.

Active runs are persisted in `sessions/world_model.json` under the
`gyms` section, not in per-operator files. Run identifiers are stable
(`gym0001`, `gym0002`, ...), so status survives sessions and can be
queried directly:

```bash
gym list
gym start first_implant --target 172.20.0.20
gym status
gym status gym0001
gym stop gym0001
gym stop first_implant
gym stop                      # stop every active gym
gym submit gym0001 --techniques implant_deploy,beacon_callback
gym top
```

`gym status` lists every active run with its run id, operator, elapsed
time and target. `gym stop` without arguments stops every active gym;
with a run id, challenge id or display name it stops only the matching
runs. `gym submit` requires a run id when more than one gym is active.

A shell opened with `atomic_shell` is not a gym run. `gym status` shows
live shells and compromised hosts as engagement context, but scoring
starts only with an explicit `gym start`. Hosts outside the current
`rhost` are ignored rather than shown as engagement state. If an old
world model holds stale loopback hosts, remove one explicitly:

```bash
rm_wm_host 127.0.0.1
python3 -m modules.world_model reset-host 10.0.0.5
```

`rm_wm_host` is the shell alias for `python3 -m modules.world_model
remove-host <ip>` (declared in `cli/aliases.yaml`).

## Adding a vector


1. Add the exploit YAML under `exploits/`.
2. Add the chain YAML under `chains/`, extending the gym base.
3. Add the index entry to `playbooks/gym_metasploitable.yaml`.
4. Run `gym_ms2 validate` and `pytest tests/test_metasploitable_gym.py`.

`tools/generate_metasploitable_gym.py` holds the catalogue table used to
regenerate the shipped files when several vectors change at once.

## Tests

`tests/test_metasploitable_gym.py` pins index completeness, exploit and
chain loadability, dry-run resolution without unresolved tokens and clear
errors for a broken matrix. `tests/test_apt_chain_integration.py` pins the
real cmd2 path: raw output visible, no boolean leak, interactive shell on
the calling thread. `tests/test_lab_target_visibility.py` pins the IP and
assign line in `lab start` and `lab status`.
