"""
LazyOwn MCP Agent Bridge
========================
Allows Claude (via MCP) to delegate tasks to internal AI agents
(Groq / Ollama) running inside LazyOwn, without blocking the MCP server.

Architecture:
  Claude → lazyown_run_agent(goal, model)
              → spawns AgentBridgeWorker in a thread
              → writes live log to sessions/agents/<id>.jsonl
  Claude → lazyown_agent_status(id)   → progress + last action
  Claude → lazyown_agent_result(id)   → final answer

Supported backends:
  - "groq"   : GroqModel via Groq SDK  (requires GROQ_API_KEY)
  - "ollama" : OllamaModel via OpenAI-compatible SDK → localhost:11434/v1
"""

import json
import logging
import os
import sys
import threading
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

BASE_DIR    = Path(__file__).parent.parent
SESSIONS    = BASE_DIR / "sessions"
AGENTS_DIR  = SESSIONS / "agents"
AGENTS_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("mcp_agent_bridge")


# ── OpenAI-compatible client factory ─────────────────────────────────────────

def _make_client(backend: str):
    """
    Return (client, model_name) for the given backend.
    Groq: returns Groq SDK client.
    Ollama: returns None (OllamaReActWorker uses requests directly).
    """
    if backend == "groq":
        from groq import Groq
        api_key = os.environ.get("GROQ_API_KEY", "")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")
        return Groq(api_key=api_key), "llama-3.3-70b-versatile"

    elif backend == "ollama":
        import requests as _req
        # Pure-reasoning models that only emit <think> tokens and no content
        THINKING_ONLY_MODELS = {"qwen3", "qwen3.5", "deepseek-r1"}

        try:
            resp  = _req.get("http://localhost:11434/api/tags", timeout=3)
            all_models = [m["name"] for m in resp.json().get("models", [])]
        except Exception:
            all_models = []

        # Prefer instruction-tuned chat models over reasoning-only ones
        preferred_order = ["llama3", "mistral", "gemma", "phi3", "neural-chat",
                           "deepseek-coder", "codellama", "qwen2"]
        model = next(
            (m for pref in preferred_order for m in all_models if pref in m.lower()),
            all_models[0] if all_models else "llama3.2:3b"
        )

        # Warn if we're stuck with a thinking-only model
        is_thinking = any(t in model.lower() for t in THINKING_ONLY_MODELS)
        if is_thinking:
            raise ValueError(
                f"Model '{model}' is a reasoning-only model and cannot produce ReAct output. "
                f"Install a chat model: `ollama pull llama3.2:3b` or `ollama pull mistral`"
            )

        return None, model   # client=None, use requests in OllamaReActWorker

    else:
        raise ValueError(f"Unknown backend '{backend}'. Use 'groq' or 'ollama'.")


def _ollama_chat(model: str, messages: list, max_tokens: int = 2000, timeout: int = 120) -> str:
    """
    Call Ollama /api/chat and return the assistant text.
    Handles reasoning models (qwen3, deepseek-r1) that put output in
    message.content or the top-level 'thinking' field.
    Uses non-streaming for simplicity with generous timeout.
    """
    import requests as _req, re as _re
    payload = {
        "model":    model,
        "messages": messages,
        "stream":   False,
        "options":  {"num_predict": max_tokens, "temperature": 0.2},
    }
    try:
        r = _req.post("http://localhost:11434/api/chat",
                      json=payload, timeout=timeout)
        obj = r.json()
    except Exception as e:
        return f"[ollama error: {e}]"

    # Standard chat response
    msg     = obj.get("message", {})
    content = (msg.get("content") or "").strip()
    if content:
        # Strip inline <think> blocks (deepseek-r1 style)
        content = _re.sub(r"<think>[\s\S]*?</think>", "", content).strip()
        if content:
            return content

    # Reasoning-only models (qwen3.5 in thinking mode) put output in 'thinking'
    thinking = (obj.get("thinking") or msg.get("thinking") or "").strip()
    if thinking:
        # Extract the actual answer from the thinking block (last paragraph or after "Answer:")
        answer_match = _re.search(r"(?:Answer|Result|Output|Final)[:\s]+(.+?)(?:\n\n|\Z)", thinking, _re.DOTALL)
        if answer_match:
            return answer_match.group(1).strip()
        # Last non-empty paragraph as fallback
        paragraphs = [p.strip() for p in thinking.split("\n\n") if p.strip()]
        return paragraphs[-1] if paragraphs else thinking[:300]

    return "[no response from model]"


# ── Agent state file helpers ──────────────────────────────────────────────────

def _agent_file(agent_id: str) -> Path:
    return AGENTS_DIR / f"{agent_id}.jsonl"


def _write_log(agent_id: str, entry: dict):
    with open(_agent_file(agent_id), "a") as f:
        f.write(json.dumps(entry) + "\n")


def _read_log(agent_id: str) -> list[dict]:
    f = _agent_file(agent_id)
    if not f.exists():
        return []
    entries = []
    for line in f.read_text().splitlines():
        try:
            entries.append(json.loads(line))
        except Exception:
            pass
    return entries


def get_agent_status(agent_id: str) -> dict:
    """Public: returns current status dict for an agent."""
    entries = _read_log(agent_id)
    if not entries:
        return {"error": f"Agent {agent_id} not found."}

    meta    = next((e for e in entries if e.get("type") == "meta"), {})
    actions = [e for e in entries if e.get("type") == "action"]
    result  = next((e for e in entries if e.get("type") == "result"), None)
    error   = next((e for e in entries if e.get("type") == "error"), None)

    return {
        "agent_id":    agent_id,
        "goal":        meta.get("goal", ""),
        "backend":     meta.get("backend", ""),
        "model":       meta.get("model", ""),
        "status":      result["status"] if result else (error["status"] if error else "running"),
        "iterations":  len(actions),
        "last_action": actions[-1].get("tool") if actions else None,
        "started_at":  meta.get("started_at", ""),
        "finished_at": result.get("finished_at") if result else None,
        "answer":      result.get("answer") if result else None,
    }


def get_agent_result(agent_id: str) -> dict:
    """Public: returns final result + full action log."""
    entries = _read_log(agent_id)
    if not entries:
        return {"error": f"Agent {agent_id} not found."}

    status = get_agent_status(agent_id)
    actions = [e for e in entries if e.get("type") == "action"]

    return {
        **status,
        "action_log": [
            {
                "step":   a.get("step"),
                "tool":   a.get("tool"),
                "args":   a.get("args"),
                "output": (a.get("output") or "")[:500],  # truncate for readability
            }
            for a in actions
        ],
    }


def list_agents(limit: int = 10) -> list[dict]:
    """List recent agents sorted by start time."""
    results = []
    for f in sorted(AGENTS_DIR.glob("*.jsonl"), key=lambda x: x.stat().st_mtime, reverse=True)[:limit]:
        agent_id = f.stem
        results.append(get_agent_status(agent_id))
    return results


# ── Core agent worker ─────────────────────────────────────────────────────────

# ── Groq: native tool-calling loop ───────────────────────────────────────────

GROQ_SYSTEM = """You are LazyOwn, an autonomous pentesting AI agent.
Achieve the given GOAL using the run_lazyown_command tool.
Rules:
1. Think before each action. Use minimum steps.
2. Never repeat the same exact command.
3. After 3-5 actions summarize findings and stop (don't call any tool).
4. Adapt if a command fails — don't retry identically.
"""

class GroqAgentWorker:
    def __init__(self, agent_id, goal, client, model, run_cmd, max_iter):
        self.agent_id = agent_id
        self.goal     = goal
        self.client   = client
        self.model    = model
        self.run_cmd  = run_cmd
        self.max_iter = max_iter
        self.executed = set()
        self.history  = [
            {"role": "system", "content": GROQ_SYSTEM},
            {"role": "user",   "content": f"GOAL: {goal}"},
        ]

    def _tools(self):
        return [{"type": "function", "function": {
            "name": "run_lazyown_command",
            "description": "Execute a LazyOwn shell command and return its output.",
            "parameters": {"type": "object",
                           "properties": {"command": {"type": "string"}},
                           "required": ["command"]},
        }}]

    def run(self):
        for step in range(1, self.max_iter + 1):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model, messages=self.history,
                    tools=self._tools(), tool_choice="auto",
                    temperature=0.1, max_tokens=1024,
                )
            except Exception as e:
                _write_log(self.agent_id, {"type":"error","status":"failed","error":str(e),"finished_at":datetime.now().isoformat()})
                return

            msg        = resp.choices[0].message
            tool_calls = getattr(msg, "tool_calls", None) or []

            if not tool_calls:
                _write_log(self.agent_id, {"type":"result","status":"completed",
                    "answer": msg.content or "Done.", "finished_at": datetime.now().isoformat()})
                return

            self.history.append({"role":"assistant","content":msg.content,
                "tool_calls":[{"id":tc.id,"type":"function",
                    "function":{"name":tc.function.name,"arguments":tc.function.arguments}}
                    for tc in tool_calls]})

            for tc in tool_calls:
                args = json.loads(tc.function.arguments) if tc.function.arguments else {}
                cmd  = args.get("command", "")
                out  = "⚠️ Duplicate." if cmd in self.executed else self.run_cmd(cmd)
                if cmd: self.executed.add(cmd)
                if len(out) > 2000: out = out[:2000] + "\n...[truncated]"
                _write_log(self.agent_id, {"type":"action","step":step,
                    "tool":tc.function.name,"args":args,"output":out,"ts":datetime.now().isoformat()})
                self.history.append({"role":"tool","tool_call_id":tc.id,
                    "name":tc.function.name,"content":out})

        # Forced summary
        self.history.append({"role":"user","content":"Summarize your findings concisely."})
        try:
            r = self.client.chat.completions.create(model=self.model,messages=self.history,max_tokens=512)
            answer = r.choices[0].message.content or "No summary."
        except Exception as e:
            answer = f"Summary error: {e}"
        _write_log(self.agent_id, {"type":"result","status":"completed",
            "answer":answer,"finished_at":datetime.now().isoformat()})


# ── Ollama: ReAct text-based loop (no tool-calling) ──────────────────────────

REACT_SYSTEM = """You are LazyOwn, an autonomous pentesting AI.
Achieve the GOAL using LazyOwn shell commands.

At each step you MUST respond in exactly this format:
Thought: <your reasoning>
Action: <lazyown_command_here>

When you have enough information, respond with:
Thought: <reasoning>
Answer: <final summary of findings>

Rules:
- One Action per response. No extra text.
- Never repeat the same Action twice.
- Use real LazyOwn commands (lazynmap, enum4linux_ng, ad_ldap_enum, etc.)
- After 3-5 steps write Answer: and stop.
"""

class OllamaReActWorker:
    def __init__(self, agent_id, goal, client, model, run_cmd, max_iter):
        self.agent_id = agent_id
        self.goal     = goal
        self.client   = client
        self.model    = model
        self.run_cmd  = run_cmd
        self.max_iter = max_iter
        self.executed = set()
        self.history  = [
            {"role": "system", "content": REACT_SYSTEM},
            {"role": "user",   "content": f"GOAL: {goal}"},
        ]

    def _parse(self, text: str):
        """Extract (action, answer) from ReAct-format response."""
        import re
        action = re.search(r"Action:\s*(.+)", text)
        answer = re.search(r"Answer:\s*([\s\S]+)", text)
        return (action.group(1).strip() if action else None,
                answer.group(1).strip() if answer else None)

    def run(self):
        for step in range(1, self.max_iter + 1):
            try:
                text = _ollama_chat(self.model, self.history, max_tokens=800, timeout=90)
            except Exception as e:
                _write_log(self.agent_id, {
                    "type": "error", "status": "failed",
                    "error": f"step={step} {type(e).__name__}: {e}",
                    "finished_at": datetime.now().isoformat()
                })
                return

            _write_log(self.agent_id, {"type": "_debug", "step": step, "raw": text[:200]})
            action, answer = self._parse(text)

            self.history.append({"role": "assistant", "content": text})

            if answer:
                _write_log(self.agent_id, {"type":"result","status":"completed",
                    "answer":answer,"finished_at":datetime.now().isoformat()})
                return

            if not action:
                _write_log(self.agent_id, {"type":"result","status":"completed",
                    "answer": text or "Agent stopped without answer.",
                    "finished_at":datetime.now().isoformat()})
                return

            out = "⚠️ Duplicate." if action in self.executed else self.run_cmd(action)
            if action: self.executed.add(action)
            if len(out) > 1500: out = out[:1500] + "\n...[truncated]"

            _write_log(self.agent_id, {"type":"action","step":step,
                "tool":"run_lazyown_command","args":{"command":action},
                "output":out,"ts":datetime.now().isoformat()})

            self.history.append({"role":"user","content":f"Observation: {out}"})

        _write_log(self.agent_id, {"type":"result","status":"completed",
            "answer":"Iteration limit reached. Check action log for findings.",
            "finished_at":datetime.now().isoformat()})


# ── Unified AgentBridgeWorker ─────────────────────────────────────────────────

class AgentBridgeWorker:
    """Dispatches to GroqAgentWorker or OllamaReActWorker based on backend."""

    def __init__(self, agent_id, goal, backend, run_cmd, max_iterations):
        self.agent_id       = agent_id
        self.goal           = goal
        self.backend        = backend
        self.run_cmd        = run_cmd
        self.max_iterations = max_iterations

    def run(self):
        try:
            client, model = _make_client(self.backend)
        except Exception as e:
            _write_log(self.agent_id, {"type":"error","status":"failed",
                "error":str(e),"finished_at":datetime.now().isoformat()})
            return

        _write_log(self.agent_id, {"type":"meta","goal":self.goal,
            "backend":self.backend,"model":model,
            "started_at":datetime.now().isoformat()})

        if self.backend == "groq":
            GroqAgentWorker(self.agent_id, self.goal, client, model,
                            self.run_cmd, self.max_iterations).run()
        else:
            OllamaReActWorker(self.agent_id, self.goal, client, model,
                              self.run_cmd, self.max_iterations).run()


# ── Public API: start an agent ────────────────────────────────────────────────

def start_agent(goal: str, backend: str, lazyown_runner_fn,
                max_iterations: int = 8) -> str:
    """
    Start an agent in a background thread.
    Returns the agent_id for polling.
    """
    agent_id = str(uuid.uuid4())[:8]
    worker   = AgentBridgeWorker(
        agent_id=agent_id,
        goal=goal,
        backend=backend,
        run_cmd=lazyown_runner_fn,
        max_iterations=max_iterations,
    )
    t = threading.Thread(target=worker.run, daemon=True, name=f"agent-{agent_id}")
    t.start()
    return agent_id


# ── CLI for quick testing ─────────────────────────────────────────────────────

if __name__ == "__main__":
    import time

    def dummy_runner(cmd: str) -> str:
        return f"[dry-run] would execute: {cmd}"

    backend = sys.argv[1] if len(sys.argv) > 1 else "ollama"
    goal    = sys.argv[2] if len(sys.argv) > 2 else "List available recon commands in LazyOwn"

    print(f"[bridge] Starting {backend} agent for: {goal}")
    aid = start_agent(goal, backend, dummy_runner, max_iterations=3)
    print(f"[bridge] Agent ID: {aid}")

    for _ in range(30):
        time.sleep(2)
        s = get_agent_status(aid)
        print(f"[bridge] status={s['status']}  iterations={s['iterations']}  last={s['last_action']}")
        if s["status"] in ("completed", "failed"):
            print("\n[bridge] RESULT:")
            r = get_agent_result(aid)
            print(r.get("answer", r.get("error")))
            break
