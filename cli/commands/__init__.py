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

Remaining phases (postexp, persist, privesc, cred, lateral, c2,
report) still live in ``lazyown.py`` and will be lifted in subsequent tiers.
"""
