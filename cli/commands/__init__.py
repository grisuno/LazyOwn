"""Phase-scoped CommandSet modules.

Each submodule defines one or more ``cmd2.CommandSet`` subclasses grouping
commands that share a kill-chain phase or attack domain. ``cli.registry``
discovers and registers them onto ``LazyOwnShell`` at startup.

Active CommandSets (27)
-----------------------

- ``cli.commands.recon`` — 12 commands (nmap, DNS, web fingerprinting)
- ``cli.commands.enum``  — 10 commands (SMB, RPC, LDAP quick checks)
- ``cli.commands.scan`` — Network scanning commands
- ``cli.commands.exploit`` — 10 commands (sqlmap, lazypwn, rev, commix,
  download_exploit, img2cookie, wrapper, kusa, ticketer, www)
- ``cli.commands.postexp`` — 8 commands (lazywebshell, disableav, mimikatzpy,
  scavenger, follina, shellcode, ofuscatorps1, atomic_lazyown)
- ``cli.commands.persist`` — 7 commands (createwebshell, createrevshell,
  createwinrevshell, conptyshell, pwncatcs, revwin)
- ``cli.commands.cred`` — 9 commands (hashcat, john2hash, hydra, medusa,
  crunch, cewl, sshkey, creds_py, spraykatz)
- ``cli.commands.lateral`` — 8 commands (socat, chisel, set_proxychains,
  ngrok, ligolo, nc, wmiexec, ssh)
- ``cli.commands.report`` — 8 commands (gpt, eyewitness, gowitness,
  createtargets, banners, vulns, create_session_json, malwarebazar)
- ``cli.commands.privilege_escalation`` — 9 commands (linpeas, winpeas, pspy)
- ``cli.commands.exfiltration`` — 19 commands (data exfiltration tools)
- ``cli.commands.command_and_control`` — 6 commands (c2_status, c2_beacons,
  c2_keygen, c2_quickstart, c2_beacon_cmd, c2_implant)
- ``cli.commands.cloud`` — 4 commands (cloud_metadata, cloud_buckets,
  cloud_scan, cloud_iam)
- ``cli.commands.containers`` — 5 commands (docker_enum, k8s_enum,
  container_escape, k8s_pods, k8s_secrets)
- ``cli.commands.database`` — DB management commands
- ``cli.commands.caldera`` — CALDERA integration
- ``cli.commands.ai`` — AI/LLM commands
- ``cli.commands.audit`` — Audit commands
- ``cli.commands.orchestration`` — Orchestration commands
- ``cli.commands.module_manager`` — Module management
- ``cli.commands.resource_scripting`` — Resource script commands
- ``cli.commands.payload_generation`` — Payload generation
- ``cli.commands.diagnostics`` — Diagnostics commands
- ``cli.commands.lab`` — CTF lab management (lab list|start|stop|status)
- ``cli.commands.marketplace`` — Plugin discovery & install (marketplace list|search|install|update|info)
- ``cli.commands.campaign`` — Campaign export/import as portable archives (campaign export|import|list)
- ``cli.commands.collaboration`` — Multi-operator team commands (lock_target, unlock_target, team_status, team_chat, share_finding)
- ``cli.commands.report_enhanced`` — Professional multi-format reports with MITRE ATT&CK matrix (report generate|mitre|findings|timeline)
- ``cli.commands.purple_team`` — Purple team closed-loop: exec+measure, score, report, dashboard (purple_exec, purple_test, purple_score, purple_report, purple_dashboard)
"""
