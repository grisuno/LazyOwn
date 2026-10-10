"""Rich per-step engagement summaries from evidence and sessions artefacts.

Builds the operator-facing detail LAZY shows in its plan tab: what each
step found (OS, ports, populated fields, facts, candidates, payload),
what was skipped and why, and what to run next via the unified
recommendation engine (``cli/recommendation.py`` — the single source of
truth for suggestions). Full step outputs come from the evidence vault,
never from truncated tails. Reports persist under
``sessions/engagements/`` for later queries by operators or agents.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]")
OPEN_PORT_RE = re.compile(r"(\d+)\s*/\s*([A-Za-z0-9_?.-]+)")
TTL_RE = re.compile(r"TTL\s*[:=]\s*(\d+)", re.IGNORECASE)
CHANGED_RE = re.compile(r"^\s*\+\s*(\S+)", re.MULTILINE)
SERVICES_RE = re.compile(r"Services\s*:\s*(.+)", re.IGNORECASE)
EDB_RE = re.compile(r"(Exploit-DB|EDB-ID|CVE-\d{4}-\d+)[^\n]{0,100}", re.IGNORECASE)
PAYLOAD_RE = re.compile(r"(windows|linux)/[a-z0-9_/]+|[\w\-./]+\.(exe|elf|dll|ps1|sh)\b",
                        re.IGNORECASE)
SAVED_RE = re.compile(r"(Saved|Written|staged|output)\s+(to|at|:)?\s*([^\n]{1,120})",
                      re.IGNORECASE)

MAX_MARKER_LINES = 12
MAX_PORTS_SHOWN = 15
MAX_NEXT = 5


def marker_lines(text: str, limit: int = MAX_MARKER_LINES) -> list[str]:
    """Extract real log lines (``[+] ... [+]``) dropping panels and bars."""
    cleaned = ANSI_RE.sub("", str(text or ""))
    found: list[str] = []
    for raw in cleaned.splitlines():
        line = raw.strip()
        if "[+]" not in line:
            continue
        line = line.replace("[+]", "").strip(" |")
        if line and line not in found:
            found.append(line)
        if len(found) >= limit:
            break
    return found


def full_output(step: dict, sessions_dir: str | Path) -> str:
    """Return the full step output from evidence, falling back to the tail."""
    evidence = str(step.get("evidence", "") or "")
    if evidence:
        try:
            from modules.evidence import EvidenceStore as _Vault
            return _Vault(Path(str(sessions_dir)) / "evidence").get(evidence).decode(
                "utf-8", "replace")
        except Exception:
            pass
    return str(step.get("output_tail", "") or "")


def held_scan_ports(target: str, sessions_dir: str | Path) -> tuple[list[str], list[str]]:
    """Parse held scan XMLs for open ports.

    Returns (ports, source_names). Ports look like ``4000/remoteanything``.
    """
    try:
        from modules.enrich import scan_files_for as _scan_files
    except ImportError:
        return [], []
    ports: list[str] = []
    sources: list[str] = []
    try:
        import xml.etree.ElementTree as _ET
    except ImportError:
        return [], []
    for path in _scan_files(sessions_dir, target):
        if path.suffix != ".xml":
            continue
        try:
            root = _ET.parse(str(path)).getroot()
        except Exception:
            continue
        sources.append(path.name)
        for port_el in root.iter("port"):
            state = port_el.find("state")
            if state is None or state.get("state") != "open":
                continue
            svc = port_el.find("service")
            name = svc.get("name", "") if svc is not None else ""
            ports.append(f"{port_el.get('portid', '?')}/{name or '?'}")
    seen = [p for p in dict.fromkeys(ports)]
    return seen, sources


def detail_for(tool: str, text: str, target: str = "",
               sessions_dir: str | Path = "sessions") -> list[str]:
    """Extract the key facts from one step output for the summary."""
    lines = marker_lines(text)
    blob = "\n".join(lines)
    normalized = str(tool or "").lower()
    if normalized == "ping":
        out = [line for line in lines
               if "TTL" in line or "alive" in line or "os_id" in line]
        return out or lines[:3]
    if normalized in ("lazynmap", "nmap", "rustscan", "masscan"):
        found = OPEN_PORT_RE.findall(blob)
        if found:
            shown = [f"{port}/{svc}" for port, svc in found[:MAX_PORTS_SHOWN]]
            return [f"open ports: {', '.join(shown)}"]
        return lines[:4] or ["scan produced no parseable output"]
    if normalized == "auto_populate":
        out = []
        services = SERVICES_RE.search(blob)
        if services:
            out.append(f"services: {services.group(1).strip()[:200]}")
        out.extend(f"populated {m}" for m in CHANGED_RE.findall(blob)[:8])
        intel = [line for line in lines if "ntelligence" in line or "ngested" in line]
        out.extend(intel[:2])
        plain = [line for line in lines if "No changes" in line]
        out.extend(plain[:1])
        return out or lines[:4]
    if normalized == "facts_show":
        return lines[:8] or ["no facts"]
    if normalized == "searchsploit":
        hits = EDB_RE.findall(blob)
        if hits:
            return [f"candidate: {h.strip()[:100]}" for h in hits[:8]]
        if "Not Found" in blob or "Not Found" in str(text or ""):
            return ["no candidates (Not Found)"]
        return lines[:6] or ["no candidates"]
    if normalized in ("lazymsfvenom", "generate_reverse_shell"):
        out = []
        payloads = PAYLOAD_RE.findall(blob)
        if payloads:
            first = payloads[0]
            name = first[0] if isinstance(first, tuple) else first
            out.append(f"payload: {name}")
        saved = SAVED_RE.search(blob)
        if saved:
            out.append(f"staged: {saved.group(3).strip()[:120]}")
        if "Not Found" in blob and not out:
            return ["no payload staged (Not Found)"]
        return out or lines[:6]
    return lines[:6]


def next_actions(target: str, sessions_dir: str | Path = "sessions",
                 limit: int = MAX_NEXT) -> list[dict]:
    """Rank next actions via the unified recommendation engine.

    Degrades to [] when the engine is unavailable — callers always work.
    """
    try:
        payload_path = Path(str(sessions_dir)).parent / "payload.json"
        if payload_path.name != "payload.json":
            payload_path = Path("payload.json")
        payload = json.loads(Path("payload.json").read_text(encoding="utf-8"))
    except Exception:
        payload = {}
    try:
        from cli.recommendation_signals import build_context, build_default_engine
        engine = build_default_engine(payload=dict(payload))
        ctx = build_context(dict(payload), sessions_dir=str(sessions_dir),
                            target=target, limit=limit)
        return [{"action": r.action, "command": r.command_preview or "",
                 "reasons": list(r.reasons or [])[:2]}
                for r in engine.recommend(ctx)[:limit]]
    except Exception:
        return []


def render_text(engagement_id: str, target: str, shell: bool,
                steps: list[dict], sessions_dir: str | Path = "sessions") -> str:
    """Render the console summary with per-step detail lines."""
    lines = [f"daemon engaged {target}: {engagement_id}"]
    for idx, step in enumerate(steps, 1):
        phase = step.get("phase", "?")
        label = step.get("label", "")
        command = step.get("command", "")
        skipped = step.get("skipped_reason", "")
        title = f"{label}:" if label else ""
        if skipped:
            detail = ""
            if skipped == "scan_already_held":
                ports, sources = held_scan_ports(target, sessions_dir)
                if ports:
                    detail = f" held ports: {', '.join(ports[:MAX_PORTS_SHOWN])}"
                    if sources:
                        detail += f" ({sources[0]})"
            lines.append(f"  {idx}. [SKIP] {phase} {title} {command} "
                         f"({skipped}{detail})".rstrip())
            continue
        mark = "ok" if step.get("success") else "FAIL"
        lines.append(f"  {idx}. [{mark}] {phase} {title} {command}".rstrip())
        text = full_output(step, sessions_dir)
        for fact in detail_for((command or "").split()[0] if command else "",
                               text, target, sessions_dir):
            lines.append(f"       - {fact[:220]}")
        if mark == "FAIL":
            tail = str(step.get("output_tail", "") or "")[-120:].strip()
            if tail:
                lines.append(f"       ! {tail[:120]}")
    lines.append(f"  shell={'YES' if shell else 'no'} steps={len(steps)}")
    return "\n".join(lines)


def render_markdown(engagement_id: str, target: str, shell: bool,
                    steps: list[dict], next_list: list[dict],
                    sessions_dir: str | Path = "sessions") -> str:
    """Render the persisted per-engagement report."""
    out = [f"# Engagement {engagement_id}", "", f"Target: {target}",
           f"Shell: {'YES' if shell else 'no'}", f"Steps: {len(steps)}", "",
           "## Steps", ""]
    for idx, step in enumerate(steps, 1):
        status = ("SKIP " + step.get("skipped_reason", "")
                  if step.get("skipped_reason")
                  else ("ok" if step.get("success") else "FAIL"))
        out.append(f"### {idx}. [{status}] {step.get('phase', '?')} — "
                   f"{step.get('label', step.get('command', ''))}")
        out.append(f"Command: `{step.get('command', '')}`")
        if step.get("switched_from"):
            out.append(f"Switched from: `{step['switched_from']}`")
        if step.get("evidence"):
            out.append(f"Evidence: `{str(step['evidence'])[:12]}`")
        if not step.get("skipped_reason"):
            text = full_output(step, sessions_dir)
            for fact in detail_for((step.get("command", "") or "").split()[0],
                                   text, target, sessions_dir):
                out.append(f"- {fact[:220]}")
        out.append("")
    out.append("## Next actions")
    out.append("")
    if next_list:
        for item in next_list:
            cmd = f" — `{item['command']}`" if item.get("command") else ""
            out.append(f"- {item.get('action', '?')}{cmd}")
    else:
        out.append("No recommendations available.")
    out.append("")
    out.append(f"Ledger: `sessions/intents.jsonl` (engagement_id={engagement_id})")
    return "\n".join(out) + "\n"


def write_report(engagement_id: str, target: str, shell: bool,
                 steps: list[dict],
                 sessions_dir: str | Path = "sessions") -> str:
    """Persist the engagement report; return its relative path."""
    base = Path(str(sessions_dir))
    directory = base / "engagements"
    directory.mkdir(parents=True, exist_ok=True)
    upcoming = next_actions(target, sessions_dir)
    text = render_markdown(engagement_id, target, shell, steps, upcoming,
                           sessions_dir)
    path = directory / f"engage_{engagement_id}.md"
    path.write_text(text, encoding="utf-8")
    return str(path)


__all__ = [
    "marker_lines", "full_output", "held_scan_ports", "detail_for",
    "next_actions", "render_text", "render_markdown", "write_report",
]
