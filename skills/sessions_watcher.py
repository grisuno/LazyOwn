#!/usr/bin/env python3
"""
LazyOwn Sessions Watcher
========================
Watchdog daemon over sessions/.

When new or modified files appear, it:

  scan_*.nmap (nmap text output)
    → calls VulnBot (or local Ollama fallback) to generate sessions/plan.txt
    → injects a PLAN_READY objective into objectives.jsonl
    → emits PLAN_READY event to events.jsonl

  scan_*.nmap.xml (nmap XML)
    → calls FactStore.ingest_xml()
    → emits SCAN_XML_READY event

  sessions/<ip>/<port>/<tool>/*.txt  (pwntomate tool output)
    → calls FactStore.ingest_text()
    → emits TOOL_OUTPUT_READY event
    → injects a factual objective: "Review <tool> output for <ip>:<port>"

  sessions/plan.txt  (VulnBot or manual plan)
    → emits PLAN_UPDATED event with first 500 chars as preview

This closes the OpenClaw-style loop:
  lazynmap → watcher → plan.txt → objective injected →
  Claude Code polls → reasons → acts → new output → watcher fires again

Usage (background daemon):
    python3 skills/sessions_watcher.py &

    or via MCP:  lazyown_run_command("python3 skills/sessions_watcher.py &")

Stop:  kill $(pgrep -f sessions_watcher.py)
"""

from __future__ import annotations

import json
import logging
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

# Optional watchdog import (install with: pip install watchdog)
try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
    _WATCHDOG_AVAILABLE = True
except ImportError:
    _WATCHDOG_AVAILABLE = False

BASE_DIR     = Path(__file__).parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
SKILLS_DIR   = Path(__file__).parent

# ── Shared imports from skills/ ───────────────────────────────────────────────

if str(SKILLS_DIR) not in sys.path:
    sys.path.insert(0, str(SKILLS_DIR))

try:
    from lazyown_objective import ObjectiveStore, PLAN_FILE
    _OBJECTIVES_AVAILABLE = True
except ImportError:
    _OBJECTIVES_AVAILABLE = False

try:
    from lazyown_facts import FactStore
    _facts = FactStore()
    _FACTS_AVAILABLE = True
except ImportError:
    _FACTS_AVAILABLE = False
    _facts = None  # type: ignore[assignment]

# event_engine is in modules/
if str(BASE_DIR / "modules") not in sys.path:
    sys.path.insert(0, str(BASE_DIR / "modules"))

try:
    from event_engine import _append_event
    _ENGINE_AVAILABLE = True
except ImportError:
    _ENGINE_AVAILABLE = False
    def _append_event(ev: dict) -> None:  # type: ignore[misc]
        pass

# ── Constants ─────────────────────────────────────────────────────────────────

OLLAMA_HOST  = os.environ.get("OLLAMA_HOST", "127.0.0.1")
OLLAMA_PORT  = int(os.environ.get("OLLAMA_PORT", "11434"))
OLLAMA_MODEL = os.environ.get("OLLAMA_SMALL_MODEL", "qwen3.5:0.8b")

POLL_INTERVAL_S   = float(os.environ.get("WATCHER_POLL_INTERVAL", "3"))
MAX_PLAN_CHARS    = int(os.environ.get("WATCHER_MAX_PLAN_CHARS", "6000"))

logging.basicConfig(
    level=logging.INFO,
    format="[watcher] %(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("sessions_watcher")

# ── Event helper ──────────────────────────────────────────────────────────────

import uuid as _uuid
import datetime as _datetime


def _emit(event_type: str, severity: str, suggest: str, source: dict) -> None:
    ev = {
        "id":        _uuid.uuid4().hex[:8],
        "timestamp": _datetime.datetime.now(_datetime.timezone.utc).isoformat(),
        "type":      event_type,
        "severity":  severity,
        "rule_id":   f"watcher_{event_type.lower()}",
        "source":    source,
        "suggest":   suggest,
        "status":    "pending",
    }
    _append_event(ev)
    log.info(f"event emitted: {event_type}  {suggest[:60]}")


# ── Plan generation ───────────────────────────────────────────────────────────


def _call_ollama(prompt: str) -> Optional[str]:
    url = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"
    body = json.dumps({"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read())
            return data.get("response", "").strip()
    except Exception as exc:
        log.warning(f"Ollama call failed: {exc}")
        return None


def _generate_plan_from_nmap(nmap_path: Path) -> str:
    try:
        content = nmap_path.read_text(errors="replace")[:MAX_PLAN_CHARS]
    except OSError:
        return ""

    prompt = f"""You are an expert penetration tester. Analyze this nmap output and produce a
concise, prioritized attack plan. List specific commands with target IP and port.
Format: numbered steps, each starting with the tool name.

NMAP OUTPUT:
{content}

ATTACK PLAN:"""

    plan = _call_ollama(prompt)
    if not plan:
        plan = _minimal_plan_from_nmap(content)
    return plan


def _minimal_plan_from_nmap(content: str) -> str:
    import re
    open_ports = re.findall(r"(\d+)/open\s+tcp\s+(\S+)", content)
    if not open_ports:
        return "(no open ports detected in nmap output)"
    lines = ["Auto-generated plan from nmap output:", ""]
    priority_tools = {
        "http": "gobuster / nikto / ffuf",
        "https": "gobuster / nikto / sslscan",
        "microsoft-ds": "crackmapexec / enum4linux / smbmap",
        "netbios-ssn": "enum4linux / smbclient",
        "ldap": "ldapsearch / ldapdomaindump",
        "ssh": "ssh-audit / hydra",
        "ftp": "ftp anonymous login / hydra",
        "rdp": "crackmapexec / hydra rdp",
        "ms-wbt-server": "crackmapexec / hydra rdp",
        "kerberos-sec": "kerbrute / impacket GetNPUsers",
        "msrpc": "rpcclient enumdomusers",
    }
    for port, svc in sorted(open_ports, key=lambda x: int(x[0])):
        tool = priority_tools.get(svc.lower(), f"manual analysis of {svc}")
        lines.append(f"  {len(lines)-1}. Port {port}/{svc} → {tool}")
    return "\n".join(lines)


# ── File handlers ─────────────────────────────────────────────────────────────


def _handle_nmap_txt(path: Path) -> None:
    log.info(f"nmap output detected: {path.name}")
    plan = _generate_plan_from_nmap(path)
    if not plan:
        return
    PLAN_FILE.write_text(f"# Attack Plan — {path.name}\n\n{plan}\n")
    log.info(f"plan.txt updated ({len(plan)} chars)")

    target = _extract_target_from_filename(path.name)
    if _OBJECTIVES_AVAILABLE:
        store = ObjectiveStore()
        store.inject(
            text=f"Execute attack plan derived from {path.name} — read sessions/plan.txt for steps",
            priority="high",
            source="watcher",
            context={"nmap_file": str(path), "target": target},
        )
    _emit(
        event_type="PLAN_READY",
        severity="high",
        suggest="Read sessions/plan.txt — inject_objective or auto_loop to act on it.",
        source={"file": str(path), "target": target},
    )


def _handle_nmap_xml(path: Path) -> None:
    log.info(f"nmap XML detected: {path.name}")
    if _FACTS_AVAILABLE and _facts is not None:
        n = _facts.ingest_xml(path)
        _facts.save()
        log.info(f"FactStore: ingested {n} service facts from {path.name}")
    target = _extract_target_from_filename(path.name)
    _emit(
        event_type="SCAN_XML_READY",
        severity="info",
        suggest=f"FactStore updated from {path.name}. Run facts_show(target='{target}').",
        source={"file": str(path), "target": target},
    )


def _handle_tool_output(path: Path) -> None:
    parts = path.parts
    try:
        sessions_idx = next(i for i, p in enumerate(parts) if p == "sessions")
        ip   = parts[sessions_idx + 1]
        port = parts[sessions_idx + 2]
        tool = parts[sessions_idx + 3]
    except (StopIteration, IndexError):
        ip = port = tool = "unknown"

    log.info(f"tool output: {ip}:{port}/{tool}")

    if _FACTS_AVAILABLE and _facts is not None:
        try:
            n = _facts.ingest_text(path, host_hint=ip)
            if n:
                _facts.save()
                log.info(f"FactStore: {n} facts from {path.name}")
        except Exception as exc:
            log.warning(f"FactStore ingest failed: {exc}")

    if _OBJECTIVES_AVAILABLE:
        store = ObjectiveStore()
        store.inject(
            text=f"Review {tool} output for {ip}:{port} — check sessions/{ip}/{port}/{tool}/",
            priority="medium",
            source="watcher",
            context={"ip": ip, "port": port, "tool": tool, "file": str(path)},
        )

    _emit(
        event_type="TOOL_OUTPUT_READY",
        severity="info",
        suggest=f"New output from {tool} on {ip}:{port}. Run facts_show(refresh=True).",
        source={"ip": ip, "port": port, "tool": tool, "file": str(path)},
    )


def _handle_plan_updated(path: Path) -> None:
    try:
        preview = path.read_text(errors="replace")[:500]
    except OSError:
        preview = ""
    _emit(
        event_type="PLAN_UPDATED",
        severity="high",
        suggest="sessions/plan.txt updated. Use next_objective to get the current goal.",
        source={"preview": preview},
    )


def _extract_target_from_filename(name: str) -> str:
    import re
    m = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", name)
    return m.group(1) if m else "unknown"


# ── Watchdog handler ─────────────────────────────────────────────────────────

_SEEN: set = set()  # debounce — avoid double-firing on same path


def _dispatch(path: Path) -> None:
    key = (str(path), path.stat().st_size if path.exists() else 0)
    if key in _SEEN:
        return
    _SEEN.add(key)
    if len(_SEEN) > 2000:
        # prune oldest half to avoid unbounded growth
        pruned = list(_SEEN)[1000:]
        _SEEN.clear()
        _SEEN.update(pruned)

    name = path.name
    strpath = str(path)

    if name.endswith(".nmap") and "scan_" in name and not name.endswith(".xml"):
        _handle_nmap_txt(path)
    elif name.endswith(".nmap.xml") and "scan_" in name:
        _handle_nmap_xml(path)
    elif "/sessions/" in strpath and name.endswith(".txt"):
        parts = Path(strpath).parts
        if "sessions" in parts:
            idx = list(parts).index("sessions")
            depth = len(parts) - idx
            if depth >= 5:
                _handle_tool_output(path)
    elif name == "plan.txt" and str(path.parent) == str(SESSIONS_DIR):
        _handle_plan_updated(path)


if _WATCHDOG_AVAILABLE:
    class _Handler(FileSystemEventHandler):
        def on_created(self, event):
            if not event.is_directory:
                _dispatch(Path(event.src_path))

        def on_modified(self, event):
            if not event.is_directory:
                _dispatch(Path(event.src_path))


# ── Main loop ─────────────────────────────────────────────────────────────────


def _run_watchdog() -> None:
    handler = _Handler()
    observer = Observer()
    observer.schedule(handler, str(SESSIONS_DIR), recursive=True)
    observer.start()
    log.info(f"watchdog active on {SESSIONS_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def _run_poll_loop() -> None:
    log.info(f"poll loop active (interval={POLL_INTERVAL_S}s) on {SESSIONS_DIR}")
    snapshot: dict[str, float] = {}

    def _scan() -> dict[str, float]:
        result: dict[str, float] = {}
        try:
            for root, _dirs, files in os.walk(SESSIONS_DIR):
                for fname in files:
                    fp = Path(root) / fname
                    try:
                        result[str(fp)] = fp.stat().st_mtime
                    except OSError:
                        pass
        except Exception:
            pass
        return result

    snapshot = _scan()
    while True:
        time.sleep(POLL_INTERVAL_S)
        current = _scan()
        for path_str, mtime in current.items():
            if path_str not in snapshot or snapshot[path_str] != mtime:
                _dispatch(Path(path_str))
        snapshot = current


def main() -> None:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    if _WATCHDOG_AVAILABLE:
        _run_watchdog()
    else:
        log.warning("watchdog not installed — using poll loop. pip install watchdog for inotify.")
        _run_poll_loop()


if __name__ == "__main__":
    main()
