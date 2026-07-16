"""Phase-scoped CommandSet modules.

Each submodule defines one or more ``cmd2.CommandSet`` subclasses grouping
commands that share a kill-chain phase (recon, enum, exploit, postexp,
persist, privesc, cred, lateral, c2, report). ``cli.registry`` discovers and
registers them onto ``LazyOwnShell`` at startup.

Migration status (Tier 3 in progress)
--------------------------------------

The following phases have been migrated from ``lazyown.py`` into
per-phase CommandSets:

- ``cli.commands.recon`` — 12 commands (nmap, DNS, web fingerprinting, ...)
- ``cli.commands.enum``  — 10 commands (SMB, RPC, LDAP quick checks, ...)
- ``cli.commands.exploit`` — 10 commands (sqlmap, lazypwn, rev, commix,
  download_exploit, img2cookie, wrapper, kusa, ticketer, www)
  *Pending — switch to LazyOwnCommandSet after deleting originals from
  lazyown.py.*
- ``cli.commands.postexp`` — 8 commands (lazywebshell, disableav, mimikatzpy,
  scavenger, follina, shellcode, ofuscatorps1, atomic_lazyown) *Pending.*
- ``cli.commands.persist`` — 7 commands (createwebshell, createrevshell,
  createwinrevshell, conptyshell, pwncatcs, ssh, revwin) *Pending.*
- ``cli.commands.cred`` — 9 commands (hashcat, john2hash, hydra, medusa,
  crunch, cewl, sshkey, creds_py, spraykatz) *Pending.*
- ``cli.commands.lateral`` — 8 commands (socat, chisel, set_proxychains,
  ngrok, ligolo, nc, wmiexec, ssh) *Pending.*
- ``cli.commands.report`` — 8 commands (gpt, eyewitness, gowitness,
  createtargets, banners, vulns, create_session_json, malwarebazar) *Pending.*

Previously migrated (active): ``cli.commands.privilege_escalation`` (9
commands) and ``cli.commands.exfiltration`` (19 commands) are already active
as ``PendingCommandSet`` subclasses.

Empty scaffold (active, ``LazyOwnCommandSet``):
``cli.commands.command_and_control`` — ready for one-at-a-time migration.
"""
