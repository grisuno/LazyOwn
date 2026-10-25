#!/usr/bin/env python3
from pathlib import Path

files = list(Path("cli/commands").glob("*migrated.py"))

CLASS_MAP = {
    "ReconCommandSet": "ReconMigratedCommandSet",
    "ExploitCommandSet": "ExploitMigratedCommandSet",
    "ScanCommandSet": "ScanMigratedCommandSet",
    "PostexpCommandSet": "PostexpMigratedCommandSet",
    "PersistCommandSet": "PersistMigratedCommandSet",
    "CredCommandSet": "CredMigratedCommandSet",
    "LateralCommandSet": "LateralMigratedCommandSet",
    "ReportCommandSet": "ReportMigratedCommandSet",
    "MiscCommandSet": "MiscMigratedCommandSet",
    "CommandAndControlCommandSet": "CommandAndControlMigratedCommandSet",
    "Command_And_ControlCommandSet": "CommandAndControlMigratedCommandSet",
}

for f in files:
    content = f.read_text()

    # Add PendingCommandSet import if missing
    if "PendingCommandSet" not in content:
        content = content.replace(
            "from cli.commands._base import LazyOwnCommandSet",
            "from cli.commands._base import LazyOwnCommandSet\nfrom cli.commands._dormancy import PendingCommandSet",
        )

    # Change base class
    content = content.replace("(LazyOwnCommandSet)", "(PendingCommandSet)")

    # Rename classes
    for old, new in CLASS_MAP.items():
        content = content.replace(old, new)

    f.write_text(content)
    print(f"Updated {f.name}")
