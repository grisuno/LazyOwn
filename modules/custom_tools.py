"""Operator-defined custom tools exposed to the autonomous loop.

Kinds:
    command -- shell line with ``{arg}`` substituted and executed through
        the streaming runner (guard/scope/constraints still apply).
    script  -- ``.sh`` runs with bash, anything else with python3.
    http    -- URL/body templates with ``{arg}`` posting through the
        notification URL allowlist.

The planner proposes matches as ``custom tool <name> <target>`` intents
and the worker routes them to :func:`run_tool` in-process, so custom
tools get the same trigger+command contract as the rest of the loop.
"""

from __future__ import annotations

import json
import re
import shlex
import urllib.parse
import urllib.request
from pathlib import Path

KINDS = ("command", "script", "http")
MAX_HTTP_BODY = 200_000
DEFAULT_TIMEOUT_SEC = 60.0
STORE_NAME = "custom_tools.json"


def _store_file() -> Path:
    """Resolve the tool registry path through the lazy store layer."""
    from modules.lazy_loop import _store_path

    return _store_path(STORE_NAME)


def _load() -> dict:
    """Load the registry payload."""
    try:
        return json.loads(_store_file().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"tools": []}


def _save(payload: dict) -> None:
    """Persist the registry payload."""
    path = _store_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def add_tool(name: str, kind: str, target: str, description: str = "",
             method: str = "GET", body: str = "",
             timeout: float = DEFAULT_TIMEOUT_SEC, trigger: str = "") -> dict:
    """Register or replace one custom tool.

    Args:
        name: Tool name used in intents.
        kind: ``command``, ``script`` or ``http``.
        target: Command line, script path or URL template.
        description: Short text used for keyword matching.
        method: HTTP method for ``http`` tools.
        body: Request body template for ``http`` tools.
        timeout: Execution timeout in seconds.
        trigger: Comma/space separated service tokens (``http,https,smb``)
            that make the loop propose this tool when the matching
            service is discovered, exactly like ``tools/*.tool`` files.

    Returns:
        Stored tool entry.

    Raises:
        ValueError: Unknown kind or empty name/target.
    """
    kind = (kind or "").strip().lower()
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}")
    clean_name = (name or "").strip()[:120]
    clean_target = (target or "").strip()
    if not clean_name or not clean_target:
        raise ValueError("name and target are required")
    payload = _load()
    tools = [tool for tool in payload.get("tools", []) if tool.get("name") != clean_name]
    entry = {"name": clean_name, "kind": kind, "target": clean_target[:2000],
             "description": (description or "")[:300],
             "trigger": _trigger_tokens(trigger),
             "method": (method or "GET").upper()[:8] if kind == "http" else "",
             "body": (body or "")[:4000] if kind == "http" else "",
             "timeout": max(5.0, min(3600.0, float(timeout or DEFAULT_TIMEOUT_SEC)))}
    tools.append(entry)
    tools.sort(key=lambda tool: tool.get("name", ""))
    payload["tools"] = tools
    _save(payload)
    return dict(entry)


def remove_tool(name: str) -> bool:
    """Delete a tool by name."""
    payload = _load()
    tools = payload.get("tools", [])
    kept = [tool for tool in tools if tool.get("name") != name]
    if len(kept) == len(tools):
        return False
    payload["tools"] = kept
    _save(payload)
    return True


def list_tools() -> list[dict]:
    """Return every registered tool."""
    return list(_load().get("tools", []))


def get_tool(name: str) -> dict | None:
    """Find one tool by name."""
    for tool in list_tools():
        if tool.get("name") == name:
            return tool
    return None


def _trigger_tokens(raw: str) -> list[str]:
    """Normalize a comma/space separated trigger string into tokens."""
    return [token.strip().lower()
            for token in re.split(r"[,\s]+", raw or "") if token.strip()]


def match_tools(text: str, limit: int = 3) -> list[dict]:
    """Rank tools whose name/description/trigger keywords appear in the text."""
    lowered = (text or "").lower()
    if not lowered.strip():
        return []
    scored: list[tuple[int, dict]] = []
    for tool in list_tools():
        tokens = {token.lower() for token in
                  re.findall(r"[A-Za-z][A-Za-z0-9_-]+",
                             f"{tool.get('name', '')} {tool.get('description', '')}")
                  if len(token) >= 4}
        score = sum(1 for token in tokens if token in lowered)
        for trigger in tool.get("trigger", []) or []:
            if str(trigger).strip() and str(trigger).lower() in lowered:
                score += 3
        if tool.get("name", "").lower() in lowered:
            score += 2
        if score > 0:
            scored.append((score, tool))
    scored.sort(key=lambda pair: (-pair[0], pair[1].get("name", "")))
    return [tool for _score, tool in scored[: max(1, int(limit))]]


def run_tool(name: str, arg: str = "", on_output=None) -> str:
    """Execute one custom tool and return its transcript.

    Args:
        name: Tool name.
        arg: Argument substituted into ``{arg}`` placeholders.
        on_output: Optional live line observer.

    Returns:
        Captured output or an ``execution failed:`` transcript line.
    """
    tool = get_tool(name)
    if tool is None:
        return f"execution failed: unknown custom tool: {name}"
    kind = tool.get("kind", "")
    target = str(tool.get("target", ""))
    timeout = float(tool.get("timeout", DEFAULT_TIMEOUT_SEC) or DEFAULT_TIMEOUT_SEC)
    if kind == "http":
        return _run_http(tool, arg, on_output)
    line = target.replace("{arg}", shlex.quote(arg))
    if kind == "script":
        runner = "bash" if target.endswith(".sh") else "python3"
        line = f"{runner} {shlex.quote(target)} {shlex.quote(arg)}".strip()
    from modules.auto_registry import execute_streaming

    return execute_streaming(line, on_output=on_output, timeout_sec=timeout)


def _run_http(tool: dict, arg: str, on_output=None) -> str:
    """Execute an http custom tool through the URL allowlist."""
    quoted = urllib.parse.quote(arg, safe="")
    url = str(tool.get("target", "")).replace("{arg}", quoted)
    if not url.lower().startswith(("http://", "https://")):
        return "execution failed: http tool target must be a URL"
    try:
        from modules.notify import url_allowed

        allowed, reason = url_allowed(url)
        if not allowed:
            return f"execution failed: url blocked ({reason})"
    except Exception:
        pass
    method = str(tool.get("method") or "GET").upper()
    body = str(tool.get("body", "")).replace("{arg}", arg)
    data = body.encode() if body else None
    request = urllib.request.Request(url, data=data, method=method)
    if data:
        request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=float(tool.get("timeout", 30))) as response:
            payload = response.read(MAX_HTTP_BODY).decode("utf-8", "replace")
    except Exception as exc:
        return f"execution failed: {exc}"
    if on_output is not None:
        try:
            for line in payload.splitlines()[:200]:
                on_output(line)
        except Exception:
            pass
    return f"HTTP {method} {url} :: {payload[:4000]}"


__all__ = ["DEFAULT_TIMEOUT_SEC", "KINDS", "add_tool", "get_tool", "list_tools",
           "match_tools", "remove_tool", "run_tool"]
