"""
LazyOwn Timeline Narrator
==========================
Reads events.jsonl, groups them into time windows, and asks Groq to
generate a concise red-team prose narrative. Writes sessions/timeline.md.

The narrative reads like a penetration test report timeline:
  "10:32 — Initial reconnaissance revealed an open HTTP port on 10.10.11.78.
   10:35 — SMB enumeration was initiated after detecting port 445 ..."

Public API:
  narrate(api_key: str | None, force: bool) -> str
      Builds and returns the narrative text, writes timeline.md.
      Set force=True to regenerate even if file is fresh (< 5 min old).

  load_timeline() -> str
      Return the last written timeline.md, or empty string.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR       = Path(__file__).parent.parent
SESSIONS       = BASE_DIR / "sessions"
EVENTS_FILE    = SESSIONS / "events.jsonl"
TIMELINE_FILE  = SESSIONS / "timeline.md"
PAYLOAD_FILE   = BASE_DIR / "payload.json"

_GROQ_MODEL    = "llama-3.3-70b-versatile"
_MAX_TOKENS    = 1200
_REFRESH_SECS  = 300   # don't regenerate if file is younger than 5 min
_MAX_EVENTS    = 60    # cap events sent to Groq to control token cost


# ── System prompt ─────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = """\
You are a senior penetration tester writing the timeline section of an
engagement report. Given a list of security events (from a red-team tool),
produce a concise chronological narrative in plain English.

Style rules:
- Start each paragraph with a timestamp range (e.g. "10:32–10:40 —").
- Group related events into a single paragraph.
- Use active voice: "The operator enumerated...", "A credential was captured..."
- Keep the full narrative under 400 words.
- Do NOT include markdown headers or bullet points — prose only.
- If there are no meaningful events, write: "No significant activity recorded."
"""


# ── Event loader ──────────────────────────────────────────────────────────────

def _load_events(n: int = _MAX_EVENTS) -> list[dict]:
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


# ── Event formatter ───────────────────────────────────────────────────────────

def _format_events_for_prompt(events: list[dict]) -> str:
    lines = []
    for ev in events:
        ts      = ev.get("timestamp", "")[:16].replace("T", " ")
        etype   = ev.get("type", "UNKNOWN")
        sev     = ev.get("severity", "info").upper()
        cmd     = ev["source"].get("command", "?") if "source" in ev else "?"
        target  = ev["source"].get("target", "") if "source" in ev else ""
        suggest = ev.get("suggest", "")
        lines.append(
            f"[{ts}] [{sev}] {etype} — command={cmd}"
            + (f" target={target}" if target else "")
            + (f" | {suggest[:80]}" if suggest else "")
        )
    return "\n".join(lines) if lines else "(no events)"


# ── AI call with fallback ─────────────────────────────────────────────────────

def _call_ai(api_key: str, events_text: str, target: str) -> tuple[str, str]:
    """Returns (narrative_text, backend_used)."""
    from ai_fallback import call as _ai_call

    user_msg = (
        f"Target: {target or 'unknown'}\n\n"
        f"Events:\n{events_text}\n\n"
        "Write the timeline narrative now."
    )
    result = _ai_call(
        prompt      = user_msg,
        system      = _SYSTEM_PROMPT,
        api_key     = api_key,
        max_tokens  = _MAX_TOKENS,
        temperature = 0.5,
    )
    return result.text, result.backend


# ── Timeline writer ───────────────────────────────────────────────────────────

def _write_timeline(narrative: str, event_count: int, target: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = (
        f"# LazyOwn — Red Team Timeline\n\n"
        f"**Generated:** {now}  |  **Target:** {target or 'N/A'}  |  "
        f"**Events processed:** {event_count}\n\n"
        f"---\n\n"
        f"{narrative}\n"
    )
    TIMELINE_FILE.write_text(content)


# ── Public API ────────────────────────────────────────────────────────────────

def narrate(api_key: str | None = None, force: bool = False) -> str:
    """Generate and return the timeline narrative. Writes timeline.md."""
    # Skip if file is fresh and force=False
    if not force and TIMELINE_FILE.exists():
        age = (datetime.now() - datetime.fromtimestamp(TIMELINE_FILE.stat().st_mtime)).total_seconds()
        if age < _REFRESH_SECS:
            return TIMELINE_FILE.read_text()

    # Resolve API key
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        try:
            cfg = json.loads(PAYLOAD_FILE.read_text())
            api_key = cfg.get("api_key", "")
        except Exception:
            pass
    if not api_key:
        return "[narrator] No GROQ_API_KEY found. Set api_key in payload.json."

    # Load target
    target = ""
    try:
        cfg    = json.loads(PAYLOAD_FILE.read_text())
        target = cfg.get("rhost", "") or cfg.get("domain", "")
    except Exception:
        pass

    events       = _load_events()
    events_text  = _format_events_for_prompt(events)
    narrative, backend = _call_ai(api_key, events_text, target)
    _write_timeline(narrative, len(events), target)
    return TIMELINE_FILE.read_text()


def load_timeline() -> str:
    """Return the last written timeline.md or empty string."""
    if TIMELINE_FILE.exists():
        try:
            return TIMELINE_FILE.read_text()
        except Exception:
            pass
    return ""


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    result = narrate(force=True)
    print(result)
    print(f"\nWritten to: {TIMELINE_FILE}")
