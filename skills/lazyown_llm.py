#!/usr/bin/env python3
"""
LazyOwn LLM Bridge — MCP Edition
=================================
Unified satellite-model interface for lazyown_mcp.py.

Backends:
  groq    — Groq API (llama-3.3-70b / llama-3.1-8b).
            Native tool calling via OpenAI-compatible API.
  ollama  — Local Ollama.  deepseek-r1:1.5b has NO native tool calling.
            Bridge implements ReAct (Reason + Act) via prompt engineering:
            the model emits Thought/Action/Action Input/Observation turns
            that are parsed and executed here, then fed back.

Design:
  - Zero Flask dependency — pure stdlib + optional groq SDK + requests
  - Single LLMBridge class owns the tool registry
  - Both backends share the same tool registry (name → callable)
  - Groq path: native tool_calls JSON from API → execute → assistant turn
  - Ollama path: ReAct text loop → regex parse → execute → inject Observation
  - deepseek-r1 wraps reasoning in <think>…</think>; those are stripped before
    parsing so the Action line is always visible to the parser
  - All tool outputs are truncated to MAX_TOOL_OUTPUT chars (context safety)

MCP usage:
  lazyown_llm_ask(goal="…", backend="groq", max_iterations=6)
  lazyown_llm_ask(goal="…", backend="ollama")

CLI usage:
  python3 skills/lazyown_llm.py ask "Enumerate SMB on 127.0.0.1" --backend groq
  python3 skills/lazyown_llm.py ask "What ports are open on 127.0.0.1?" --backend ollama
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# ─── Constants ────────────────────────────────────────────────────────────────

GROQ_API_URL         = "https://api.groq.com/openai/v1/chat/completions"
GROQ_DEFAULT_MODEL   = "llama-3.3-70b-versatile"
GROQ_FAST_MODEL      = "llama-3.1-8b-instant"

OLLAMA_HOST          = os.environ.get("OLLAMA_HOST", "127.0.0.1")
OLLAMA_PORT          = int(os.environ.get("OLLAMA_PORT", "11434"))
OLLAMA_DEFAULT_MODEL = os.environ.get("OLLAMA_DEFAULT_MODEL", "deepseek-r1:1.5b")

MAX_TOOL_OUTPUT   = int(os.environ.get("LLM_MAX_TOOL_OUTPUT", "3000"))
MAX_ITERATIONS    = int(os.environ.get("LLM_MAX_ITERATIONS", "8"))
HTTP_TIMEOUT      = int(os.environ.get("LLM_HTTP_TIMEOUT", "90"))

BASE_DIR     = Path(__file__).parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"

log = logging.getLogger("lazyown_llm")

# ─── Tool definition ──────────────────────────────────────────────────────────


@dataclass
class LLMTool:
    """A callable tool available to the satellite model."""

    name: str
    description: str
    parameters: Dict[str, Any]
    func: Callable

    def openai_schema(self) -> Dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": self.parameters,
                    "required": list(self.parameters.keys()),
                },
            },
        }


# ─── LLMBridge ───────────────────────────────────────────────────────────────


class LLMBridge:
    """
    Unified bridge to Groq (native tool calling) and local Ollama (ReAct).

    Register tools once, then call ask().  Both backends execute the same tools.
    """

    def __init__(
        self,
        backend: str = "groq",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        self._backend = backend.lower()
        self._api_key = api_key or os.environ.get("GROQ_API_KEY", "")
        if self._backend == "groq":
            self._model = model or GROQ_DEFAULT_MODEL
        else:
            self._model = model or OLLAMA_DEFAULT_MODEL
        self._tools: Dict[str, LLMTool] = {}

    def register_tool(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        func: Callable,
    ) -> None:
        self._tools[name] = LLMTool(name=name, description=description,
                                    parameters=parameters, func=func)

    def ask(
        self,
        goal: str,
        context: str = "",
        max_iterations: int = MAX_ITERATIONS,
        system_prompt: str = "",
    ) -> str:
        if self._backend == "groq":
            return self._ask_groq(goal, context, max_iterations, system_prompt)
        return self._ask_ollama_react(goal, context, max_iterations, system_prompt)

    # ── Groq path (native tool calling) ──────────────────────────────────────

    def _ask_groq(
        self,
        goal: str,
        context: str,
        max_iterations: int,
        system_prompt: str,
    ) -> str:
        if not self._api_key:
            return "[groq] No API key — set GROQ_API_KEY or api_key in payload.json"

        sys_content = system_prompt or _default_system_prompt(list(self._tools.keys()))
        messages: List[Dict] = [
            {"role": "system", "content": sys_content},
        ]
        if context:
            messages.append({"role": "user", "content": f"Context:\n{context}"})
        messages.append({"role": "user", "content": goal})

        tools = [t.openai_schema() for t in self._tools.values()] or None

        for iteration in range(max_iterations):
            response = self._groq_request(messages, tools)
            if "error" in response:
                return f"[groq error] {response['error']}"

            choice = response.get("choices", [{}])[0]
            msg    = choice.get("message", {})
            finish = choice.get("finish_reason", "")

            messages.append({"role": "assistant", **{k: v for k, v in msg.items()
                                                      if k != "role"}})

            tool_calls = msg.get("tool_calls") or []
            if not tool_calls:
                return msg.get("content") or "(no response)"

            for tc in tool_calls:
                fn   = tc.get("function", {})
                name = fn.get("name", "")
                try:
                    args = json.loads(fn.get("arguments", "{}"))
                except json.JSONDecodeError:
                    args = {}
                result = self._call_tool(name, args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.get("id", ""),
                    "name": name,
                    "content": result,
                })

            if finish == "stop":
                break

        final_msg = next(
            (m.get("content") for m in reversed(messages)
             if m.get("role") == "assistant" and m.get("content")),
            "(max iterations reached without final answer)"
        )
        return final_msg

    def _groq_request(self, messages: List[Dict], tools: Optional[List]) -> Dict:
        body: Dict[str, Any] = {
            "model": self._model,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 4096,
        }
        if tools:
            body["tools"] = tools
            body["tool_choice"] = "auto"
        data = json.dumps(body).encode()
        req = urllib.request.Request(
            GROQ_API_URL,
            data=data,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            body_bytes = exc.read()
            return {"error": f"HTTP {exc.code}: {body_bytes.decode(errors='replace')[:300]}"}
        except Exception as exc:
            return {"error": str(exc)}

    # ── Ollama ReAct path ─────────────────────────────────────────────────────

    _THINK_RE   = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
    _ACTION_RE  = re.compile(
        r"Action\s*:\s*(?P<tool>\w+)\s*\n\s*Action\s*Input\s*:\s*(?P<args>\{.*?\})",
        re.DOTALL | re.IGNORECASE,
    )
    _FINAL_RE   = re.compile(r"Final\s*Answer\s*:\s*(?P<answer>.+)", re.DOTALL | re.IGNORECASE)

    def _ask_ollama_react(
        self,
        goal: str,
        context: str,
        max_iterations: int,
        system_prompt: str,
    ) -> str:
        tool_descriptions = "\n".join(
            f"  {t.name}: {t.description}\n"
            f"    Parameters: {json.dumps(t.parameters)}"
            for t in self._tools.values()
        )
        sys_block = system_prompt or (
            "You are LazyOwn, an expert penetration testing AI assistant.\n"
            "Answer concisely and always support conclusions with executed tool results."
        )
        react_instructions = f"""
{sys_block}

Available tools:
{tool_descriptions if tool_descriptions else "(no tools registered)"}

To use a tool, write EXACTLY:
  Thought: <one line of reasoning>
  Action: <tool_name>
  Action Input: {{"param": "value"}}

When you have enough information, write:
  Final Answer: <your complete answer>

Rules:
- Never invent tool results — always execute the tool and use the real output.
- Never repeat the same Action+Input twice.
- Maximum {max_iterations} tool calls before giving Final Answer.
"""
        history = f"Context:\n{context}\n\n" if context else ""
        history += f"Question: {goal}\n\n"

        for iteration in range(max_iterations):
            prompt = react_instructions + "\n---\n" + history + "Thought:"
            raw = self._ollama_generate(prompt)
            if raw.startswith("[ollama error]"):
                return raw

            clean = self._THINK_RE.sub("", raw).strip()
            full_turn = "Thought:" + clean

            final_m = self._FINAL_RE.search(full_turn)
            if final_m:
                return final_m.group("answer").strip()

            action_m = self._ACTION_RE.search(full_turn)
            if not action_m:
                if iteration == max_iterations - 1:
                    return full_turn.strip()
                history += full_turn + "\n"
                continue

            tool_name = action_m.group("tool").strip()
            try:
                args = json.loads(action_m.group("args"))
            except json.JSONDecodeError:
                args = {}

            observation = self._call_tool(tool_name, args)
            history += full_turn[:action_m.end()] + f"\nObservation: {observation}\n\n"

        return "(max iterations reached — no final answer produced)"

    def _ollama_generate(self, prompt: str) -> str:
        url = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"
        body = json.dumps({"model": self._model, "prompt": prompt, "stream": False}).encode()
        req = urllib.request.Request(url, data=body,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                data = json.loads(resp.read())
                return data.get("response", "").strip()
        except Exception as exc:
            return f"[ollama error] {exc}"

    # ── Tool executor ─────────────────────────────────────────────────────────

    def _call_tool(self, name: str, args: Dict) -> str:
        if name not in self._tools:
            return f"[tool error] unknown tool '{name}'. Available: {list(self._tools.keys())}"
        try:
            result = str(self._tools[name].func(**args))
        except Exception as exc:
            result = f"[tool error] {exc}"
        if len(result) > MAX_TOOL_OUTPUT:
            cut = len(result) - MAX_TOOL_OUTPUT
            result = result[:MAX_TOOL_OUTPUT] + f"\n[...{cut} chars truncated...]"
        return result


# ─── Default tools (LazyOwn-aware) ───────────────────────────────────────────


def _make_default_tools(bridge: LLMBridge) -> None:
    """
    Register a standard set of LazyOwn-aware tools on the bridge.

    These tools are safe to call autonomously:
      run_command     — executes a LazyOwn shell command
      read_nmap       — reads the latest nmap scan for a target
      read_plan       — reads sessions/plan.txt
      read_facts      — shows FactStore summary for a target
      read_objectives — lists pending objectives
    """

    def run_command(command: str) -> str:
        """Execute a LazyOwn shell command and return its output."""
        from lazyown_mcp import _run_lazyown_command  # local import to avoid circular
        return _run_lazyown_command(command, timeout=60)

    def read_nmap(target: str = "127.0.0.1") -> str:
        """Read the nmap scan file for the given target IP."""
        patterns = [
            SESSIONS_DIR / f"scan_{target}.nmap",
            SESSIONS_DIR / f"scan_{target}_*.nmap",
        ]
        import glob as _glob
        for pat in patterns:
            matches = _glob.glob(str(pat))
            if matches:
                try:
                    return Path(matches[0]).read_text(errors="replace")[:MAX_TOOL_OUTPUT]
                except OSError as exc:
                    return f"[read_nmap error] {exc}"
        return f"No nmap file found for {target} in sessions/"

    def read_plan() -> str:
        """Read the current attack plan from sessions/plan.txt."""
        plan_file = SESSIONS_DIR / "plan.txt"
        if not plan_file.exists():
            return "(no plan yet)"
        return plan_file.read_text(errors="replace")[:MAX_TOOL_OUTPUT]

    def read_facts(target: str = "") -> str:
        """Return FactStore structured facts for a target (or all targets)."""
        try:
            skills_path = str(Path(__file__).parent)
            if skills_path not in sys.path:
                sys.path.insert(0, skills_path)
            from lazyown_facts import FactStore
            store = FactStore()
            return store.summary(target or None)
        except Exception as exc:
            return f"[read_facts error] {exc}"

    def read_objectives(limit: int = 5) -> str:
        """List the next N pending attack objectives."""
        try:
            from lazyown_objective import ObjectiveStore
            store = ObjectiveStore()
            objs = store.list_pending(limit=limit)
            if not objs:
                return "No pending objectives."
            return "\n".join(
                f"[{o.priority}] [{o.id}] {o.text}" for o in objs
            )
        except Exception as exc:
            return f"[read_objectives error] {exc}"

    bridge.register_tool(
        "run_command",
        "Execute any LazyOwn shell command (e.g. 'lazynmap', 'set rhost 10.10.11.78', 'linpeas'). "
        "Returns the command output.",
        {"command": {"type": "string", "description": "LazyOwn command with arguments"}},
        run_command,
    )
    bridge.register_tool(
        "read_nmap",
        "Read the nmap scan results file for a target IP. "
        "Returns the raw nmap output text.",
        {"target": {"type": "string", "description": "Target IP address"}},
        read_nmap,
    )
    bridge.register_tool(
        "read_plan",
        "Read the current attack plan (sessions/plan.txt) generated by VulnBot.",
        {},
        read_plan,
    )
    bridge.register_tool(
        "read_facts",
        "Return structured facts for a target: open ports, services, credentials, access level.",
        {"target": {"type": "string", "description": "Target IP or empty string for all"}},
        read_facts,
    )
    bridge.register_tool(
        "read_objectives",
        "List the highest-priority pending attack objectives.",
        {"limit": {"type": "integer", "description": "Max number of objectives to return"}},
        read_objectives,
    )


# ─── Public factory ───────────────────────────────────────────────────────────


def build_bridge(
    backend: str = "groq",
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    with_default_tools: bool = True,
) -> LLMBridge:
    """
    Create a ready-to-use LLMBridge with optional default LazyOwn tools.

    Called by lazyown_mcp.py for the lazyown_llm_ask handler.
    """
    bridge = LLMBridge(backend=backend, model=model, api_key=api_key)
    if with_default_tools:
        _make_default_tools(bridge)
    return bridge


def _default_system_prompt(tool_names: List[str]) -> str:
    return (
        "You are LazyOwn, an expert autonomous penetration testing AI.\n"
        "You have access to tools to execute commands and read session data.\n"
        f"Available tools: {', '.join(tool_names) or 'none'}.\n"
        "Be concise. Support every conclusion with real tool output.\n"
        "Never invent scan results or credentials."
    )


# ─── MCP integration helper ───────────────────────────────────────────────────


def llm_ask(
    goal: str,
    context: str = "",
    backend: str = "groq",
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    max_iterations: int = MAX_ITERATIONS,
    system_prompt: str = "",
    extra_tools: Optional[Dict[str, Callable]] = None,
) -> str:
    """
    Single-call entry point for lazyown_mcp.py.

    extra_tools: {name: (description, parameters_dict, callable)}
    """
    bridge = build_bridge(backend=backend, model=model, api_key=api_key)
    if extra_tools:
        for name, (desc, params, func) in extra_tools.items():
            bridge.register_tool(name, desc, params, func)
    return bridge.ask(goal, context=context, max_iterations=max_iterations,
                      system_prompt=system_prompt)


# ─── CLI ─────────────────────────────────────────────────────────────────────


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="LazyOwn LLM Bridge — satellite model interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd")

    p_ask = sub.add_parser("ask", help="Ask the satellite model a question/goal")
    p_ask.add_argument("goal", help="Goal or question")
    p_ask.add_argument("--backend", default="groq", choices=["groq", "ollama"])
    p_ask.add_argument("--model", default=None)
    p_ask.add_argument("--context", default="", help="Additional context text")
    p_ask.add_argument("--max-iterations", type=int, default=MAX_ITERATIONS)
    p_ask.add_argument("--no-tools", action="store_true",
                       help="Disable default tools (pure reasoning only)")

    p_info = sub.add_parser("info", help="Show configured backends and models")

    args = parser.parse_args()

    logging.basicConfig(level=logging.WARNING)

    if args.cmd == "ask":
        bridge = LLMBridge(backend=args.backend, model=args.model)
        if not args.no_tools:
            _make_default_tools(bridge)
        result = bridge.ask(args.goal, context=args.context,
                            max_iterations=args.max_iterations)
        print(result)
    elif args.cmd == "info":
        print(f"Groq   model: {GROQ_DEFAULT_MODEL}  (fast: {GROQ_FAST_MODEL})")
        print(f"Ollama model: {OLLAMA_DEFAULT_MODEL}  @ {OLLAMA_HOST}:{OLLAMA_PORT}")
        print(f"Tool output cap: {MAX_TOOL_OUTPUT} chars  |  HTTP timeout: {HTTP_TIMEOUT}s")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
