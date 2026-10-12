"""Agentic tool-calling bridge for the loop and the main agent.

The loop's planner/worker use one-shot completions by default. This
module upgrades them to real tool calling through the existing
OpenAI-compatible backends (groq/openai/deepseek): :class:`AgentRunner`
already speaks the function-calling protocol, so here we add

- tool registration for loop operations (the worker builds the guarded
  executors; this module only wires schemas and the agent loop),
- per-intent and per-session conversation persistence, so a resumed
  intent continues the same model conversation instead of replaying,
- an external ``opencode run`` backend for the main agent (full MCP
  tooling through that CLI) with best-effort session capture.

Native mode keeps guard/scope/audit parity because every tool call is
executed by the worker's guarded runner.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import threading
import time
from collections.abc import Callable, Iterable

from modules import lazy_loop as _lazy_loop
from modules.agent_runner import AgentRunner, AgentTool
from modules.lazy_loop import _load_json, _now, _save_json

CLIENT_BACKENDS = ("groq", "openai", "deepseek")
MAX_SEEDED_TURNS = 12
MAX_STORED_MESSAGES = 40
DEFAULT_MAX_ITERATIONS = 6
EXTERNAL_TIMEOUT_SEC = 900.0
MODEL_KEEPALIVE_SEC = 15.0


def tool_calling_enabled() -> bool:
    """Return whether agentic tool calling is enabled by configuration.

    ``payload.json`` key ``agent_tool_calling`` disables it explicitly;
    absent means enabled whenever a compatible backend resolves.
    """
    try:
        from core.config import load_payload

        payload = load_payload() or {}
    except Exception:
        return True
    return bool(payload.get("agent_tool_calling", True))


def max_iterations() -> int:
    """Return the bounded agent step budget from configuration."""
    try:
        from core.config import load_payload

        value = int((load_payload() or {}).get("agent_max_iterations", DEFAULT_MAX_ITERATIONS))
    except Exception:
        value = DEFAULT_MAX_ITERATIONS
    return max(2, min(16, value))


def resolve_agentic_model(exclude: set[str] | None = None):
    """Return a raw tool-calling backend for the best pool member, or None.

    Members are tried by priority; only the openai-compatible legs can
    speak function calling here. Ollama/Anthropic/toposwarm members are
    skipped so the loop degrades to the deterministic path instead of
    erroring mid-intent. ``exclude`` holds model names already tried
    this intent so a failing member cannot pin the whole attempt.
    """
    try:
        from modules.lazy_loop import LlmPool
        from modules.llm_factory import get_llm_backend_raw

        members = LlmPool().members()
    except Exception:
        return None
    skipped = {str(name) for name in (exclude or set())}
    ordered = sorted(members, key=lambda member: -int(member.get("priority", 0)))
    for member in ordered:
        spec = str(member.get("model", "") or "")
        backend, _, name = spec.partition(":")
        if backend not in CLIENT_BACKENDS or not name:
            continue
        if name in skipped or spec in skipped:
            continue
        try:
            raw = get_llm_backend_raw(backend=backend)
        except Exception:
            continue
        if not getattr(raw, "client", None):
            continue
        try:
            raw.model = name
            raw._lazy_member_name = str(member.get("name", name))
        except Exception:
            pass
        return raw
    return None


def _enable_streaming(runner, on_event) -> None:
    """Turn on token-level streaming for a runner when the stage is on.

    Args:
        runner: ObservableAgentRunner about to run.
        on_event: Optional (kind, name, text) observer to receive
            ``delta`` and ``think`` events.
    """
    if on_event is None:
        runner.stream_enabled = False
        return
    try:
        from modules.loop_ai_bridge import stream_enabled

        enabled = bool(stream_enabled())
    except Exception:
        enabled = False
    runner.stream_enabled = enabled
    if enabled:
        runner.delta_sink = lambda kind, text: on_event(kind, "stream", text)


class ObservableAgentRunner(AgentRunner):
    """AgentRunner that reports every tool call and result to a sink."""

    def __init__(
        self,
        model,
        system_prompt: str = "",
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
        on_event: Callable[[str, str, str], None] | None = None,
    ) -> None:
        """Bind the model and the optional event sink (kind, name, text)."""
        super().__init__(model, system_prompt, max_iterations)
        self._on_event = on_event or (lambda kind, name, text: None)

    def _process_tool_call(self, tool_call) -> None:
        """Run the tool through the base runner, then report the result."""
        name = str(getattr(tool_call.function, "name", "tool"))
        try:
            super()._process_tool_call(tool_call)
        finally:
            entry = self.conversation_history[-1] if self.conversation_history else {}
            self._on_event("tool", name, str(entry.get("content", ""))[:1500])

    def run(self, user_input: str) -> str:
        """Base loop plus final-turn persistence for true resume."""
        reply = super().run(user_input)
        self.conversation_history.append({"role": "assistant", "content": str(reply or "")})
        return reply

    def _call_model(self):
        """Wrap one model turn with start/end and keep-alive wait events.

        A slow or hung backend must never be invisible: while the call
        blocks, the runner reports every ``MODEL_KEEPALIVE_SEC`` that the
        model is still being awaited.
        """
        model_name = str(getattr(self.model, "model", "model"))
        self._on_event("turn", model_name, "waiting for model response")
        started = time.monotonic()
        stop = threading.Event()

        def _tick() -> None:
            waited = 0
            while not stop.wait(MODEL_KEEPALIVE_SEC):
                waited += int(MODEL_KEEPALIVE_SEC)
                self._on_event("turn", model_name, f"still waiting for model response ({waited}s)")

        ticker = threading.Thread(target=_tick, daemon=True)
        ticker.start()
        try:
            response = super()._call_model()
        finally:
            stop.set()
        self._on_event("turn", model_name, f"model replied in {time.monotonic() - started:.1f}s")
        return response


def _json_default(value):
    """JSON fallback for tool-call objects from any model SDK."""
    for attr in ("model_dump", "dict"):
        method = getattr(value, attr, None)
        if callable(method):
            try:
                return method()
            except Exception:
                pass
    if hasattr(value, "__dict__"):
        return {key: item for key, item in vars(value).items() if not key.startswith("_")}
    return str(value)


def _json_safe(messages: Iterable[dict]) -> list[dict]:
    """Round-trip messages through JSON so SDK objects persist cleanly."""
    try:
        return json.loads(json.dumps(list(messages), default=_json_default))
    except (TypeError, ValueError):
        return [dict(item) for item in messages]


class ConversationStore:
    """Per-task persistence of agent conversations (intents and sessions)."""

    def __init__(self, task_id: str = "") -> None:
        """Bind the conversation store for one task (``main`` when empty)."""
        name = f"convo_{task_id}.json" if task_id else "agent_sessions.json"
        self._path = _lazy_loop._store_path(name)

    def _load(self) -> dict:
        """Load the conversation payload."""
        return _load_json(self._path, {"intents": {}, "sessions": {}})

    def intent_messages(self, intent_id: int) -> list[dict]:
        """Return the stored messages for one intent (resume seed)."""
        entry = self._load().get("intents", {}).get(str(int(intent_id))) or {}
        return [dict(item) for item in entry.get("messages", []) if isinstance(item, dict)]

    def save_intent(self, intent_id: int, messages: Iterable[dict]) -> None:
        """Persist the tail of one intent conversation."""
        payload = self._load()
        payload.setdefault("intents", {})[str(int(intent_id))] = {
            "messages": _json_safe(list(messages)[-MAX_STORED_MESSAGES:]),
            "updated": _now(),
        }
        _save_json(self._path, payload)

    def session(self, session_id: str) -> dict:
        """Return one main-agent session payload (empty when unknown)."""
        return dict(self._load().get("sessions", {}).get(session_id) or {})

    def sessions(self) -> list[dict]:
        """List main-agent sessions with title, message count and age."""
        out = []
        for sid, entry in (self._load().get("sessions", {}) or {}).items():
            out.append(
                {
                    "session_id": sid,
                    "title": str(entry.get("title", ""))[:120],
                    "messages": len(entry.get("messages", []) or []),
                    "updated": float(entry.get("updated", 0.0) or 0.0),
                }
            )
        return sorted(out, key=lambda row: row["updated"], reverse=True)

    def save_session(self, session_id: str, messages: Iterable[dict], title: str = "") -> None:
        """Persist one main-agent session conversation tail."""
        payload = self._load()
        entry = payload.setdefault("sessions", {}).setdefault(session_id, {})
        entry["messages"] = _json_safe(list(messages)[-MAX_STORED_MESSAGES:])
        entry["updated"] = _now()
        if title:
            entry["title"] = title[:120]
        _save_json(self._path, payload)

    def reset_intents(self) -> None:
        """Drop every stored intent conversation (fresh agent start)."""
        payload = self._load()
        payload["intents"] = {}
        _save_json(self._path, payload)


def register_tools(runner: ObservableAgentRunner, specs: Iterable[dict]) -> None:
    """Register tool specs (name, description, func, parameters, required)."""
    for spec in specs:
        tool = AgentTool(
            name=str(spec["name"]),
            description=str(spec.get("description", "")),
            func=spec["func"],
            parameters=dict(spec.get("parameters", {})),
            required=list(spec.get("required", [])) or None,
        )
        runner.register_tool(tool)


def run_worker_session(
    model,
    task_id: str,
    intent_id: int,
    system_prompt: str,
    launch_prompt: str,
    tools: Iterable[dict],
    on_event: Callable[[str, str, str], None] | None = None,
) -> dict:
    """Run one agentic intent attempt with resume seeding.

    Args:
        model: Raw tool-calling backend.
        task_id: Task whose conversation store persists the session.
        intent_id: Intent the conversation belongs to.
        system_prompt: Invariant contract (goal, intent, scope, rules).
        launch_prompt: The user turn for this attempt.
        tools: Tool specs registered on the runner.
        on_event: Optional (kind, name, text) observer.

    Returns:
        Dict with reply, tool usage and persisted message count.
    """
    runner = ObservableAgentRunner(model, system_prompt, max_iterations=max_iterations(), on_event=on_event)
    _enable_streaming(runner, on_event)
    register_tools(runner, tools)
    store = ConversationStore(task_id)
    seed = store.intent_messages(intent_id)
    if seed:
        runner.conversation_history = [{"role": "system", "content": system_prompt}] + seed[-MAX_SEEDED_TURNS:]
    reply = runner.run(launch_prompt)
    store.save_intent(intent_id, runner.conversation_history)
    return {
        "reply": str(reply or ""),
        "tool_calls": dict(runner.tool_usage_count),
        "messages": len(runner.conversation_history),
    }


def run_main_session(
    model,
    session_id: str,
    system_prompt: str,
    prompt: str,
    tools: Iterable[dict],
    on_event: Callable[[str, str, str], None] | None = None,
) -> dict:
    """Run one main-agent turn, resuming the stored session conversation."""
    runner = ObservableAgentRunner(model, system_prompt, max_iterations=max_iterations() + 4, on_event=on_event)
    _enable_streaming(runner, on_event)
    register_tools(runner, tools)
    store = ConversationStore("")
    entry = store.session(session_id)
    seed = [dict(item) for item in entry.get("messages", []) or []]
    if seed:
        runner.conversation_history = [{"role": "system", "content": system_prompt}] + seed[-MAX_SEEDED_TURNS:]
    reply = runner.run(prompt)
    store.save_session(session_id, runner.conversation_history, title=str(entry.get("title") or prompt)[:120])
    return {"reply": str(reply or ""), "tool_calls": dict(runner.tool_usage_count), "session_id": session_id}


def run_external_opencode(
    prompt: str, session_id: str = "", agent: str = "", cwd: str = "", timeout_sec: float = EXTERNAL_TIMEOUT_SEC
) -> dict:
    """Run one headless ``opencode run`` task with MCP tooling.

    Best-effort session capture: when the JSON stream carries a session
    id it is returned so the next call can resume with ``--session``.

    Args:
        prompt: Task text handed to the external agent.
        session_id: Existing session to continue, when known.
        agent: Optional opencode agent name (``--agent``).
        cwd: Working directory for the agent.
        timeout_sec: Hard timeout for the child process.

    Returns:
        Dict with reply, captured session id and return code; never raises.
    """
    executable = shutil.which("opencode")
    if not executable:
        return {"reply": "", "session_id": session_id, "error": "opencode not installed"}
    command = [executable, "run", "--format", "json"]
    if session_id:
        command += ["--session", session_id]
    if agent:
        command += ["--agent", agent]
    if cwd:
        command += ["--dir", cwd]
    command += [prompt]
    chunks: list[str] = []
    captured = session_id
    process = None
    try:
        process = subprocess.Popen(  # noqa: S603 - fixed argv, no shell
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            text=True,
            errors="replace",
            start_new_session=True,
            cwd=cwd or None,
        )
        watchdog = _process_watchdog(timeout_sec, process)
        try:
            from modules.auto_registry import track_process

            track_process(process)
        except Exception:
            pass
        try:
            if process.stdout is not None:
                for line in iter(process.stdout.readline, ""):
                    chunks.append(line)
                    captured = captured or _session_from_line(line)
        finally:
            watchdog.cancel()
            try:
                process.wait(timeout=30)
            except Exception:
                pass
            try:
                from modules.auto_registry import untrack_process

                untrack_process(process)
            except Exception:
                pass
    except Exception as exc:
        return {"reply": "".join(chunks)[-2000:], "session_id": captured, "error": str(exc)}
    return {
        "reply": "".join(chunks)[-8000:],
        "session_id": captured,
        "returncode": process.returncode if process else -1,
    }


def _session_from_line(line: str) -> str:
    """Extract a session id from one opencode JSON event line, if present."""
    text = (line or "").strip()
    if not text.startswith("{"):
        return ""
    try:
        payload = json.loads(text)
    except ValueError:
        return ""
    for key in ("sessionID", "session_id", "sessionId"):
        value = str(payload.get(key, "") or "")
        if value:
            return value
    props = payload.get("properties")
    if isinstance(props, dict):
        for key in ("sessionID", "session_id", "sessionId"):
            value = str(props.get(key, "") or "")
            if value:
                return value
    return ""


def _process_watchdog(timeout_sec: float, process) -> threading.Timer:
    """Kill a child process group after the timeout; returns the timer."""
    import os
    import signal

    def _kill() -> None:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        except Exception:
            try:
                process.kill()
            except Exception:
                pass

    watchdog = threading.Timer(max(5.0, float(timeout_sec or EXTERNAL_TIMEOUT_SEC)), _kill)
    watchdog.daemon = True
    watchdog.start()
    return watchdog


__all__ = [
    "CLIENT_BACKENDS",
    "ConversationStore",
    "ObservableAgentRunner",
    "register_tools",
    "resolve_agentic_model",
    "run_external_opencode",
    "run_main_session",
    "run_worker_session",
    "tool_calling_enabled",
]
