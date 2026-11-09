"""MCP tool ``lazyown_credentials``: aggregate captured credentials."""

from __future__ import annotations

import glob
import json
from pathlib import Path
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_KEY_PREVIEW_CHARS = 40

TOOL = types.Tool(
    name="lazyown_credentials",
    description=(
        "Aggregate ALL captured credentials from every source in the session: "
        "(1) sessions/credentials*.txt — raw cred files; "
        "(2) sessions/sessionLazyOwn.json credentials + hashes arrays; "
        "(3) sessions/world_model.json credentials list; "
        "(4) sessions/facts_store.json (if present). "
        "Returns a deduped, formatted table: user, password/hash, host, source, confirmed. "
        "Also returns id_rsa keys found in sessionLazyOwn.json. "
        "Call this before any lateral movement or privilege escalation attempt."
    ),
    inputSchema={"type": "object", "properties": {}},
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Collect, dedupe and format credentials from all session sources."""
    rows: list[dict] = []
    seen: set[str] = set()

    def _add(user: str, secret: str, host: str, source: str, confirmed: bool = False) -> None:
        key = f"{user}:{secret}:{host}"
        if key not in seen:
            seen.add(key)
            rows.append({"user": user, "secret": secret, "host": host, "source": source, "confirmed": confirmed})

    for cred_file in glob.glob(str(ctx.sessions_dir / "credentials*.txt")):
        try:
            for line in Path(cred_file).read_text().splitlines():
                line = line.strip()
                if ":" in line:
                    user, _, secret = line.partition(":")
                    _add(user.strip(), secret.strip(), "?", Path(cred_file).name, True)
        except Exception:
            pass

    session_file = ctx.sessions_dir / "sessionLazyOwn.json"
    if session_file.exists():
        try:
            session = json.loads(session_file.read_text())
            for cred in session.get("credentials", []):
                _add(cred.get("username", "?"), cred.get("contraseña", "?"), "?", "session_json", True)
            for hashed in session.get("hashes", []):
                _add("?", str(hashed), "?", "session_json_hash", False)
            for key in session.get("id_rsa", []):
                _add("id_rsa", str(key)[:_KEY_PREVIEW_CHARS], "?", "session_json_key", True)
        except Exception:
            pass

    wm_file = ctx.sessions_dir / "world_model.json"
    if wm_file.exists():
        try:
            wm = json.loads(wm_file.read_text())
            for cred in wm.get("credentials", []):
                val = cred.get("value", "?")
                if ":" in val:
                    user, _, secret = val.partition(":")
                    _add(user, secret, cred.get("host", "?"), "world_model", cred.get("confirmed", False))
                else:
                    _add("?", val, cred.get("host", "?"), "world_model_hash", False)
        except Exception:
            pass

    if not rows:
        return ctx.text(tool_name, "No credentials found in session files.")
    lines = [f"Captured credentials ({len(rows)} unique):", ""]
    for row in rows:
        confirmed = "[✓]" if row["confirmed"] else "[?]"
        lines.append(f"{confirmed} {row['user']}:{row['secret']}  host={row['host']}  src={row['source']}")
    return ctx.text(tool_name, "\n".join(lines))
