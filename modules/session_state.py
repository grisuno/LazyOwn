"""
LazyOwn Session State
=====================
Aggregates live session data from multiple sources into a single
sessions/session_state.json snapshot consumed by the recommender,
timeline narrator, and MCP tools.

Sources:
  - payload.json          → active target, lhost, config
  - sessions/events.jsonl → rule-matched events (findings)
  - sessions/LazyOwn_session_report.csv → last N commands executed

Public API:
  build_state()  → dict   build and return state (does NOT write to disk)
  refresh()      → dict   build + write sessions/session_state.json
  load()         → dict   read the last written state (or build if missing)
"""

import csv
import json
import re
from datetime import datetime
from pathlib import Path

BASE_DIR     = Path(__file__).parent.parent
SESSIONS     = BASE_DIR / "sessions"
PAYLOAD_FILE = BASE_DIR / "payload.json"
EVENTS_FILE  = SESSIONS / "events.jsonl"
CSV_FILE     = SESSIONS / "LazyOwn_session_report.csv"
STATE_FILE   = SESSIONS / "session_state.json"

# How many recent CSV rows / events to consider
_CSV_TAIL    = 30
_EVENT_TAIL  = 50


# ── Phase detection ───────────────────────────────────────────────────────────

_PHASE_SIGNALS = [
    # (phase_name, event_types_that_indicate_it)
    ("exfil",        {"EXFIL_TRIGGERED"}),
    ("post-exploit", {"PRIVESC_ATTEMPT", "CREDENTIALS_CAPTURED", "C2_COMMAND_ISSUED"}),
    ("exploit",      {"VULN_SCAN_COMPLETE"}),
    ("enumeration",  {"AD_ENUM_STARTED", "SMB_PORT_FOUND", "WEB_PORT_FOUND"}),
    ("scanning",     {"WEB_PORT_FOUND", "SMB_PORT_FOUND"}),
    ("recon",        set()),   # default
]

def _detect_phase(event_types: set[str]) -> str:
    for phase, signals in _PHASE_SIGNALS:
        if signals & event_types:
            return phase
    return "recon"


# ── CSV tail reader ───────────────────────────────────────────────────────────

_CSV_FIELDS = [
    "start", "end", "source_ip", "source_port",
    "destination_ip", "destination_port", "domain",
    "subdomain", "url", "pivot_port", "command", "args",
]

def _read_last_commands(n: int = _CSV_TAIL) -> list[dict]:
    if not CSV_FILE.exists():
        return []
    rows = []
    try:
        with open(CSV_FILE, "r", newline="", errors="replace") as f:
            reader = csv.DictReader(f, fieldnames=_CSV_FIELDS)
            next(reader, None)   # skip header
            for row in reader:
                rows.append(row)
        return rows[-n:]
    except Exception:
        return []


# ── Event reader ──────────────────────────────────────────────────────────────

def _read_events(n: int = _EVENT_TAIL) -> list[dict]:
    if not EVENTS_FILE.exists():
        return []
    events = []
    try:
        for line in EVENTS_FILE.read_text().splitlines():
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except Exception:
                    pass
    except Exception:
        pass
    return events[-n:]


# ── Credential extractor ──────────────────────────────────────────────────────

_CRED_PATTERN = re.compile(
    r"(?:password|passwd|pass|cred|hash|ntlm)[=:\s]+([^\s,;\"']{4,})",
    re.IGNORECASE,
)

def _extract_creds_from_events(events: list[dict]) -> list[str]:
    creds = []
    for ev in events:
        suggest = ev.get("suggest", "")
        m = _CRED_PATTERN.search(suggest)
        if m:
            creds.append(m.group(1))
        if ev.get("type") == "CREDENTIALS_CAPTURED":
            creds.append(f"[captured via {ev['source'].get('command','?')}]")
    return list(dict.fromkeys(creds))   # dedup, preserve order


# ── Host/port extractor ───────────────────────────────────────────────────────

def _extract_hosts(rows: list[dict], payload: dict) -> dict[str, dict]:
    """Build {ip: {ports: [...], domain: str}} from CSV rows + payload."""
    hosts: dict[str, dict] = {}

    # Seed with active target
    rhost = payload.get("rhost", "")
    if rhost:
        hosts[rhost] = {
            "domain":  payload.get("domain", ""),
            "ports":   [],
            "is_active": True,
        }

    for row in rows:
        ip = row.get("destination_ip", "").strip()
        if not ip or ip in ("-", "None", ""):
            continue
        if ip not in hosts:
            hosts[ip] = {"domain": row.get("domain", ""), "ports": [], "is_active": False}
        port = row.get("destination_port", "").strip()
        if port and port not in ("-", "None", "0", ""):
            try:
                p = int(port)
                if p not in hosts[ip]["ports"]:
                    hosts[ip]["ports"].append(p)
            except ValueError:
                pass

    # Merge known ports from payload targets list
    for t in payload.get("targets", []):
        tip = t.get("ip", "")
        if tip and tip in hosts:
            for p in t.get("ports", []):
                if p not in hosts[tip]["ports"]:
                    hosts[tip]["ports"].append(p)

    return hosts


# ── Recent commands summary ───────────────────────────────────────────────────

def _summarise_commands(rows: list[dict]) -> list[str]:
    seen = []
    for row in reversed(rows):
        cmd = row.get("command", "").strip()
        if cmd and cmd not in seen:
            seen.append(cmd)
        if len(seen) >= 10:
            break
    return list(reversed(seen))


# ── Core builder ─────────────────────────────────────────────────────────────

def build_state() -> dict:
    """Assemble and return the current session state dict."""
    # Load payload
    payload: dict = {}
    try:
        payload = json.loads(PAYLOAD_FILE.read_text())
    except Exception:
        pass

    events   = _read_events()
    rows     = _read_last_commands()

    event_types = {ev.get("type", "") for ev in events}
    phase       = _detect_phase(event_types)
    hosts       = _extract_hosts(rows, payload)
    creds       = _extract_creds_from_events(events)
    last_cmds   = _summarise_commands(rows)

    # Pending events (not yet acked)
    pending_events = [
        {
            "id":       ev["id"],
            "type":     ev["type"],
            "severity": ev["severity"],
            "suggest":  ev.get("suggest", ""),
            "command":  ev["source"].get("command", ""),
            "target":   ev["source"].get("target", ""),
            "ts":       ev["timestamp"][:19],
        }
        for ev in events if ev.get("status") == "pending"
    ][-10:]   # only last 10 pending

    state = {
        "generated_at":  datetime.now().isoformat(),
        "phase":         phase,
        "active_target": payload.get("rhost", ""),
        "lhost":         payload.get("lhost", ""),
        "domain":        payload.get("domain", ""),
        "os_target":     payload.get("os", "unknown"),
        "hosts":         hosts,
        "credentials":   creds,
        "last_commands": last_cmds,
        "pending_events": pending_events,
        "total_events":  len(events),
        "open_event_count": len(pending_events),
        "targets_list":  payload.get("targets", []),
    }
    return state


def refresh() -> dict:
    """Build state and persist to sessions/session_state.json."""
    SESSIONS.mkdir(exist_ok=True)
    state = build_state()
    STATE_FILE.write_text(json.dumps(state, indent=2))
    return state


def load() -> dict:
    """Return the last written state, or build it fresh if stale/missing."""
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            # Refresh if older than 60 seconds
            ts = datetime.fromisoformat(data.get("generated_at", "2000-01-01"))
            age = (datetime.now() - ts).total_seconds()
            if age < 60:
                return data
        except Exception:
            pass
    return refresh()


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    s = refresh()
    print(json.dumps(s, indent=2))
