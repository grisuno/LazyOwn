"""Phase-scoped CommandSet modules.

Each submodule defines one or more ``cmd2.CommandSet`` subclasses grouping
commands that share a kill-chain phase (recon, enum, exploit, postexp,
persist, privesc, cred, lateral, c2, report). ``cli.registry`` discovers and
registers them onto ``LazyOwnShell`` at startup.

This package is intentionally small at Tier 2: it provides the structure
without migrating the ~280 ``do_*`` methods from ``lazyown.py``. Migration of
individual phases happens in subsequent tiers, one file at a time, with each
move covered by tests in ``tests/test_tier2_cli.py``.
"""
