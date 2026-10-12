# `cli.commands`

> Source: [cli/commands/__init__.py:1](../../cli/commands/__init__.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Phase-scoped CommandSet modules.

Each submodule defines one or more ``cmd2.CommandSet`` subclasses grouping
commands that share a kill-chain phase or attack domain. `[`cli.registry`](cli.registry.py.md)`
discovers and registers them onto `[`LazyOwnShell`](lazyown.py.md#lazyownshell)` at startup.

Active CommandSets (27)
-----------------------

- `[`cli.commands.recon`](cli.commands.recon.py.md)` — 12 commands (nmap, DNS, web fingerprinting)
- `[`cli.commands.enum`](cli.commands.enum.py.md)`  — 10 commands (SMB, RPC, LDAP quick checks)
- `[`cli.commands.scan`](cli.commands.scan.py.md)` — Network scanning commands
- `[`cli.commands.exploit`](cli.commands.exploit.py.md)` — 10 commands (sqlmap, lazypwn, rev, commix,
  download_exploit, img2cookie, wrapper, kusa, ticketer, www)
- `[`cli.commands.postexp`](cli.commands.postexp.py.md)` — 8 commands (lazywebshell, disableav, mimikatzpy,
  scavenger, follina, shellcode, ofuscatorps1, atomic_lazyown)
- `[`cli.commands.persist`](cli.commands.persist.py.md)` — 7 commands (createwebshell, createrevshell,
  createwinrevshell, conptyshell, pwncatcs, revwin)
- `[`cli.commands.cred`](cli.commands.cred.py.md)` — 9 commands (hashcat, john2hash, hydra, medusa,
  crunch, cewl, sshkey, creds_py, spraykatz)
- `[`cli.commands.lateral`](cli.commands.lateral.py.md)` — 8 commands (socat, chisel, set_proxychains,
  ngrok, ligolo, nc, wmiexec, ssh)
- ``cli.commands.report`` — 8 commands (gpt, eyewitness, gowitness,
  createtargets, banners, vulns, create_session_json, malwarebazar)
- `[`cli.commands.privilege_escalation`](cli.commands.privilege_escalation.py.md)` — 9 commands (linpeas, winpeas, pspy)
- `[`cli.commands.exfiltration`](cli.commands.exfiltration.py.md)` — 19 commands (data exfiltration tools)
- `[`cli.commands.command_and_control`](cli.commands.command_and_control.py.md)` — 6 commands (c2_status, c2_beacons,
  c2_keygen, c2_quickstart, c2_beacon_cmd, c2_implant)
- `[`cli.commands.cloud`](cli.commands.cloud.py.md)` — 4 commands (cloud_metadata, cloud_buckets,
  cloud_scan, cloud_iam)
- `[`cli.commands.containers`](cli.commands.containers.py.md)` — 5 commands (docker_enum, k8s_enum,
  container_escape, k8s_pods, k8s_secrets)
- `[`cli.commands.database`](cli.commands.database.py.md)` — DB management commands
- `[`cli.commands.caldera`](cli.commands.caldera.py.md)` — CALDERA integration
- `[`cli.commands.ai`](cli.commands.ai.py.md)` — AI/LLM commands
- `[`cli.commands.audit`](cli.commands.audit.py.md)` — Audit commands
- `[`cli.commands.orchestration`](cli.commands.orchestration.py.md)` — Orchestration commands
- `[`cli.commands.module_manager`](cli.commands.module_manager.py.md)` — Module management
- `[`cli.commands.resource_scripting`](cli.commands.resource_scripting.py.md)` — Resource script commands
- `[`cli.commands.payload_generation`](cli.commands.payload_generation.py.md)` — Payload generation
- `[`cli.commands.diagnostics`](cli.commands.diagnostics.py.md)` — Diagnostics commands
- `[`cli.commands.lab`](cli.commands.lab.py.md)` — CTF lab management (lab list|start|stop|status)
- `[`cli.commands.marketplace`](cli.commands.marketplace.py.md)` — Plugin discovery & install (marketplace list|search|install|update|info)
- `[`cli.commands.campaign`](cli.commands.campaign.py.md)` — Campaign export/import as portable archives (campaign export|import|list)
- `[`cli.commands.collaboration`](cli.commands.collaboration.py.md)` — Multi-operator team commands (lock_target, unlock_target, team_status, team_chat, share_finding)
- ``cli.commands.report_enhanced`` — Professional multi-format reports with MITRE ATT&CK matrix (report generate|mitre|findings|timeline)
- `[`cli.commands.purple_team`](cli.commands.purple_team.py.md)` — Purple team closed-loop: exec+measure, score, report, dashboard (purple_exec, purple_test, purple_score, purple_report, purple_dashboard)
