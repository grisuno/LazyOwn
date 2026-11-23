"""MITRE ATT&CK mapper — LazyOwn commands to the Enterprise matrix.

Maps the LazyOwn bridge command catalog (each command carries a
MITRE technique id) to the ATT&CK tactic matrix, then intersects the
catalog with the commands actually executed during the campaign
(loop audit trails) to produce an adversary-coverage report: which
tactics and techniques the framework can execute and which were really
exercised.

>>> from modules.mitre_mapper import coverage_report
>>> report = coverage_report()
>>> report["tactics"] and isinstance(report["tactics"], dict)
True
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from modules.report_engagement import collect_audit_rows, collect_loop_runs

TECH_ID_RE = re.compile(r"^T\d{4}(?:\.\d{3})?$")

UNKNOWN = "unknown"

TACTIC_BY_PREFIX: dict[str, str] = {
    "T1595": "reconnaissance",
    "T1592": "reconnaissance",
    "T1589": "reconnaissance",
    "T1590": "reconnaissance",
    "T1591": "reconnaissance",
    "T1593": "reconnaissance",
    "T1596": "reconnaissance",
    "T1598": "reconnaissance",
    "T1587": "resource-development",
    "T1588": "resource-development",
    "T1190": "initial-access",
    "T1566": "initial-access",
    "T1187": "initial-access",
    "T1203": "initial-access",
    "T1210": "initial-access",
    "T1078": "initial-access",
    "T1059": "execution",
    "T1053": "execution",
    "T1205": "execution",
    "T1569": "execution",
    "T1574": "execution",
    "T1098": "persistence",
    "T1136": "persistence",
    "T1505": "persistence",
    "T1543": "persistence",
    "T1548": "privilege-escalation",
    "T1068": "privilege-escalation",
    "T1055": "privilege-escalation",
    "T1027": "defense-evasion",
    "T1562": "defense-evasion",
    "T1218": "defense-evasion",
    "T1518": "defense-evasion",
    "T1649": "defense-evasion",
    "T1003": "credential-access",
    "T1110": "credential-access",
    "T1552": "credential-access",
    "T1555": "credential-access",
    "T1539": "credential-access",
    "T1558": "credential-access",
    "T1046": "discovery",
    "T1087": "discovery",
    "T1083": "discovery",
    "T1049": "discovery",
    "T1135": "discovery",
    "T1012": "discovery",
    "T1018": "discovery",
    "T1047": "discovery",
    "T1021": "lateral-movement",
    "T1022": "lateral-movement",
    "T1056": "collection",
    "T1125": "collection",
    "T1113": "collection",
    "T1114": "collection",
    "T1005": "collection",
    "T1071": "command-and-control",
    "T1090": "command-and-control",
    "T1095": "command-and-control",
    "T1105": "command-and-control",
    "T1573": "command-and-control",
    "T1572": "command-and-control",
    "T1041": "exfiltration",
    "T1048": "exfiltration",
    "T1486": "impact",
    "T1485": "impact",
    "T1185": "execution",
    "T0000": "execution",
    "T1488": "impact",
    "T1213": "collection",
    "T1602": "collection",
    "T1537": "resource-development",
}

TACTIC_ORDER = (
    "reconnaissance",
    "resource-development",
    "initial-access",
    "execution",
    "persistence",
    "privilege-escalation",
    "defense-evasion",
    "credential-access",
    "discovery",
    "lateral-movement",
    "collection",
    "command-and-control",
    "exfiltration",
    "impact",
    UNKNOWN,
)


def tactic_for_technique(technique_id: str) -> str:
    """Resolve the ATT&CK tactic for a technique id.

    Args:
        technique_id: MITRE technique id (``T1003`` or ``T1003.001``).

    Returns:
        Tactic slug; ``unknown`` when the id or prefix is unmapped.
    """
    if not technique_id:
        return UNKNOWN
    prefix = technique_id.split(".")[0]
    if prefix in TACTIC_BY_PREFIX:
        return TACTIC_BY_PREFIX[prefix]
    for known, tactic in TACTIC_BY_PREFIX.items():
        if known == prefix:
            return tactic
    return UNKNOWN


def _catalog_entries() -> list[Any]:
    """Load the bridge command catalog.

    Returns:
        List of CatalogEntry objects; empty when the bridge is unavailable.
    """
    try:
        from modules.lazyown_bridge import CommandCatalog

        return list(CommandCatalog()._entries)
    except Exception:
        return []


def executed_commands() -> set[str]:
    """Collect the command names really executed across loop audits.

    Matching is alias-aware: the audit trail stores raw tool invocations
    (``nmap -sV ...``, ``curl ...``) while the catalog names them
    (``lazynmap``), so every catalog name is searched as a whole word in
    the executed line.

    Returns:
        Set of executed catalog command names.
    """
    executed: set[str] = set()
    catalog_names = [str(entry.command or "") for entry in _catalog_entries()]
    catalog_names = [name for name in catalog_names if name]
    patterns = {name: re.compile(rf"(?<![\w-]){re.escape(name)}(?![\w-])") for name in catalog_names}
    for run in collect_loop_runs():
        for row in collect_audit_rows(run.task_id, kind="command"):
            line = str(row.get("command", "")).strip()
            if not line:
                continue
            for name, pattern in patterns.items():
                if pattern.search(line):
                    executed.add(name)
    return executed


def coverage_report(include_executed: bool = True) -> dict[str, Any]:
    """Build the adversary coverage report.

    Args:
        include_executed: Also intersect with actually executed commands.

    Returns:
        Mapping with ``tactics`` (slug -> counters), ``techniques`` rows
        and ``totals``.
    """
    executed = executed_commands() if include_executed else set()
    techniques: dict[str, dict[str, Any]] = {}
    for entry in _catalog_entries():
        technique_id = str(entry.mitre_tactic or "").strip()
        if not technique_id or not TECH_ID_RE.match(technique_id):
            continue
        name = str(entry.command or "")
        phase = str(entry.phase or "")
        row = techniques.setdefault(
            technique_id,
            {
                "technique_id": technique_id,
                "tactic": tactic_for_technique(technique_id),
                "commands": [],
                "executed": [],
            },
        )
        row["commands"].append(name)
        if name in executed:
            row["executed"].append(name)
    tactics: dict[str, dict[str, Any]] = {}
    for row in techniques.values():
        tactic = row["tactic"]
        bucket = tactics.setdefault(
            tactic,
            {"tactic": tactic, "techniques": 0, "commands": 0, "executed_techniques": 0, "executed_commands": 0},
        )
        bucket["techniques"] += 1
        bucket["commands"] += len(row["commands"])
        bucket["executed_techniques"] += 1 if row["executed"] else 0
        bucket["executed_commands"] += len(row["executed"])
    ordered_tactics = {slug: tactics[slug] for slug in TACTIC_ORDER if slug in tactics}
    for slug in sorted(tactics):
        if slug not in ordered_tactics:
            ordered_tactics[slug] = tactics[slug]
    totals = {
        "techniques": len(techniques),
        "commands": sum(len(row["commands"]) for row in techniques.values()),
        "executed_techniques": sum(1 for row in techniques.values() if row["executed"]),
        "executed_commands": sum(len(row["executed"]) for row in techniques.values()),
    }
    return {
        "tactics": ordered_tactics,
        "techniques": sorted(techniques.values(), key=lambda r: r["technique_id"]),
        "totals": totals,
    }


def render_markdown(report: dict[str, Any]) -> str:
    """Render the coverage report as Markdown.

    Args:
        report: Mapping from :func:`coverage_report`.

    Returns:
        Markdown document.
    """
    lines = [
        "# LazyOwn MITRE ATT&CK Adversary Coverage",
        "",
        f"Techniques mapped: {report['totals']['techniques']} | Commands: {report['totals']['commands']} | "
        f"Executed techniques: {report['totals']['executed_techniques']} | Executed commands: {report['totals']['executed_commands']}",
        "",
        "| Tactic | Techniques | Commands | Executed tech | Executed cmds |",
        "|---|---|---|---|---|",
    ]
    for bucket in report["tactics"].values():
        lines.append(
            f"| {bucket['tactic']} | {bucket['techniques']} | {bucket['commands']} | "
            f"{bucket['executed_techniques']} | {bucket['executed_commands']} |"
        )
    lines.extend(["", "## Techniques", "", "| Technique | Tactic | Commands | Executed |", "|---|---|---|---|"])
    for row in report["techniques"]:
        executed = ", ".join(row["executed"][:3]) + (" ..." if len(row["executed"]) > 3 else "")
        lines.append(
            f"| {row['technique_id']} | {row['tactic']} | {', '.join(row['commands'][:4])} | {executed or '-'} |"
        )
    return "\n".join(lines) + "\n"


def render_html(report: dict[str, Any]) -> str:
    """Render the coverage report as a standalone HTML document.

    Args:
        report: Mapping from :func:`coverage_report`.

    Returns:
        HTML string with the tactic table and technique breakdown.
    """
    tactic_rows = "".join(
        "<tr><td>"
        + bucket["tactic"]
        + "</td><td>"
        + str(bucket["techniques"])
        + "</td><td>"
        + str(bucket["commands"])
        + "</td><td>"
        + str(bucket["executed_techniques"])
        + "</td><td>"
        + str(bucket["executed_commands"])
        + "</td></tr>"
        for bucket in report["tactics"].values()
    )
    technique_rows = "".join(
        "<tr>"
        f"<td>{row['technique_id']}</td><td>{row['tactic']}</td>"
        f"<td>{', '.join(row['commands'][:4])}</td><td>{', '.join(row['executed'][:3]) or '-'}</td></tr>"
        for row in report["techniques"]
    )
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>LazyOwn ATT&CK coverage</title>
<style>
body {{ font-family: system-ui, sans-serif; background: #0d1117; color: #c9d1d9; margin: 24px; }}
table {{ border-collapse: collapse; margin: 12px 0; width: 100%; }}
th, td {{ border: 1px solid #30363d; padding: 6px 10px; text-align: left; }}
th {{ background: #161b22; color: #58a6ff; }}
h1 {{ color: #58a6ff; }}
</style></head><body>
<h1>LazyOwn MITRE ATT&CK Adversary Coverage</h1>
<p>Techniques: {report["totals"]["techniques"]} &middot; Commands: {report["totals"]["commands"]} &middot;
Executed techniques: {report["totals"]["executed_techniques"]} &middot; Executed commands: {report["totals"]["executed_commands"]}</p>
<h2>Tactics</h2>
<table><tr><th>Tactic</th><th>Techniques</th><th>Commands</th><th>Executed tech</th><th>Executed cmds</th></tr>
{tactic_rows}</table>
<h2>Techniques</h2>
<table><tr><th>Technique</th><th>Tactic</th><th>Commands</th><th>Executed</th></tr>
{technique_rows}</table>
</body></html>
"""


def write_coverage(out_dir: Path | None = None) -> dict[str, str]:
    """Write the coverage artefacts (md + html).

    Args:
        out_dir: Output directory override; defaults to ``sessions/reports``.

    Returns:
        Mapping with the written file paths.
    """
    out_path = out_dir or (Path("sessions") / "reports")
    out_path.mkdir(parents=True, exist_ok=True)
    report = coverage_report()
    md_path = out_path / "mitre_coverage.md"
    html_path = out_path / "mitre_coverage.html"
    md_path.write_text(render_markdown(report), encoding="utf-8")
    html_path.write_text(render_html(report), encoding="utf-8")
    return {"markdown": str(md_path), "html": str(html_path)}
