"""
LazyOwn Smart Command Recommender
===================================
Reads the current session state and asks Groq to rank the best
3-5 next LazyOwn commands, with confidence scores and reasoning.

Output written to: sessions/recommendations/next_actions.json

Public API:
  recommend(state: dict | None, api_key: str) -> list[dict]
      Returns ranked recommendations:
      [{"command": "smbmap", "confidence": 0.95, "reason": "...", "args": "-H {rhost}"}]

  recommend_and_save(api_key: str) -> list[dict]
      Builds state, calls Groq, writes JSON, returns list.
"""

import json
import os
from datetime import datetime
from pathlib import Path

BASE_DIR         = Path(__file__).parent.parent
SESSIONS         = BASE_DIR / "sessions"
RECO_DIR         = SESSIONS / "recommendations"
NEXT_ACTIONS_FILE = RECO_DIR / "next_actions.json"
PAYLOAD_FILE     = BASE_DIR / "payload.json"

_GROQ_MODEL = "llama-3.3-70b-versatile"
_MAX_TOKENS = 1024


# ── Prompt builder ────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = """\
You are an expert red-team operator assisting with a penetration test using the
LazyOwn framework. Your job is to recommend the best next shell commands to run
given the current session state.

Rules:
- Only suggest real LazyOwn commands (the operator knows them; do not invent).
- Rank by expected value: likelihood of progressing the engagement × stealth impact.
- For each command include: command name, optional args with {placeholder} syntax,
  confidence (0.0-1.0), and a one-line reason.
- Return ONLY valid JSON — no markdown, no explanation outside the JSON.

Output format (array, max 5 items):
[
  {"command": "<name>", "args": "<optional args>", "confidence": 0.87, "reason": "<why now>"},
  ...
]
"""

def _build_user_prompt(state: dict) -> str:
    phase         = state.get("phase", "recon")
    active_target = state.get("active_target", "?")
    os_target     = state.get("os_target", "unknown")
    domain        = state.get("domain", "")
    last_cmds     = state.get("last_commands", [])
    hosts         = state.get("hosts", {})
    creds         = state.get("credentials", [])
    pending       = state.get("pending_events", [])

    # Summarise hosts compactly
    hosts_summary = []
    for ip, info in list(hosts.items())[:5]:
        ports = info.get("ports", [])
        dom   = info.get("domain", "")
        hosts_summary.append(
            f"  {ip}" + (f" ({dom})" if dom else "") +
            (f"  ports: {ports}" if ports else "")
        )

    # Summarise pending events
    events_summary = [
        f"  [{ev['severity'].upper()}] {ev['type']} — {ev['suggest'][:80]}"
        for ev in pending[:5]
    ]

    prompt = f"""Current session state:
Phase: {phase}
Active target: {active_target}  OS: {os_target}  Domain: {domain or 'unknown'}

Known hosts:
{chr(10).join(hosts_summary) or '  (none discovered yet)'}

Credentials found: {creds if creds else 'none'}

Last 8 commands run: {', '.join(last_cmds[-8:]) if last_cmds else 'none'}

Pending events (unactioned):
{chr(10).join(events_summary) or '  (none)'}

Given this state, what are the best 3-5 LazyOwn commands to run next?
Return ONLY the JSON array."""
    return prompt


# ── AI call with fallback ─────────────────────────────────────────────────────

def _call_ai(api_key: str, user_prompt: str) -> list[dict]:
    from ai_fallback import call as _ai_call

    result = _ai_call(
        prompt      = user_prompt,
        system      = _SYSTEM_PROMPT,
        api_key     = api_key,
        max_tokens  = _MAX_TOKENS,
        temperature = 0.3,
    )

    if result.backend == "error":
        return [{"command": "_unavailable", "args": "", "confidence": 0.0,
                 "reason": result.text}]

    raw = result.text
    # Strip accidental markdown fences
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    # Strip fallback warning prefix (e.g. "[Groq quota exceeded — using local model ...]")
    if raw.startswith("[") and "]\n\n" in raw:
        raw = raw.split("]\n\n", 1)[1]

    try:
        parsed = json.loads(raw)
        if result.backend == "ollama":
            # Tag recommendations to show they came from local model
            for r in parsed:
                r["_via"] = result.model
        return parsed
    except json.JSONDecodeError as e:
        return [{"command": "_error", "args": "", "confidence": 0.0,
                 "reason": f"JSON parse error ({result.backend}/{result.model}): {e}\nRaw: {raw[:200]}"}]


# ── Public API ────────────────────────────────────────────────────────────────

def recommend(state: dict, api_key: str) -> list[dict]:
    """Return ranked recommendations without writing to disk."""
    prompt = _build_user_prompt(state)
    recs   = _call_ai(api_key, prompt)
    # Normalise: ensure required keys
    cleaned = []
    for r in recs:
        if not isinstance(r, dict):
            continue
        cleaned.append({
            "command":    str(r.get("command", "")).strip(),
            "args":       str(r.get("args", "")).strip(),
            "confidence": float(r.get("confidence", 0.5)),
            "reason":     str(r.get("reason", "")).strip(),
        })
    return sorted(cleaned, key=lambda x: x["confidence"], reverse=True)


def recommend_and_save(api_key: str | None = None) -> list[dict]:
    """Build state → call Groq → write JSON → return recommendations."""
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
        return [{"command": "_error", "args": "", "confidence": 0.0,
                 "reason": "No GROQ_API_KEY found. Set api_key in payload.json or GROQ_API_KEY env var."}]

    from session_state import load as _load_state
    state = _load_state()
    recs  = recommend(state, api_key)

    RECO_DIR.mkdir(parents=True, exist_ok=True)
    output = {
        "generated_at": datetime.now().isoformat(),
        "phase":        state.get("phase", "unknown"),
        "target":       state.get("active_target", ""),
        "recommendations": recs,
    }
    NEXT_ACTIONS_FILE.write_text(json.dumps(output, indent=2))
    return recs


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    recs = recommend_and_save()
    print(f"\nRecommended next actions (phase: see next_actions.json):\n")
    for i, r in enumerate(recs, 1):
        bar = "█" * int(r["confidence"] * 10)
        print(f"  {i}. [{bar:<10}] {r['confidence']:.0%}  {r['command']} {r['args']}")
        print(f"       {r['reason']}")
    print(f"\nSaved to: {NEXT_ACTIONS_FILE}")
