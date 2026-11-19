"""Code-mode (lazymode) first attempt for the loop worker.

Code mode (Cloudflare's name; "programmatic tool calling" in Anthropic's)
is already implemented in this repo as the ``lazy`` SDK facade plus the
``sdk.lazymode.run`` runner (the ``lazyown_lazymode_exec`` MCP tool wraps
it). Instead of the model driving an intent through many separate tool
round-trips, the model writes ONE Python script against ``lazy``; the
script runs in a bounded subprocess and only its structured result returns
to the context, so one model call replaces the whole round-trip loop and
the intermediate output never costs tokens.

This mixin wires that existing capability into the worker as the FIRST
option: for each intent the worker asks the model for one lazymode script
and executes it through ``sdk.lazymode.run``. The model path (the classic
multi-tool agent) remains the second option and ``auto_pwn`` the third, so
a weak or empty script never strands an intent: an exploitation intent that
the script does not shell falls through unchanged to the agent and then to
the deterministic ``auto_pwn`` fallback.

The mixin never imports ``modules.lazy_loop`` at load time (cycle-free);
runtime names are bound lazily inside methods, following the house
decomposition pattern.
"""

from __future__ import annotations

import json
import re
import time
from typing import Any

LAZYMODE_FIRST_KEY = "loop_lazymode_first"
LAZYMODE_MAX_TOKENS_KEY = "loop_lazymode_max_tokens"
LAZYMODE_TIMEOUT_KEY = "loop_lazymode_timeout"
_DEFAULT_MAX_TOKENS = 1200
_DEFAULT_TIMEOUT_SEC = 180.0
_CONTEXT_FACT_LIMIT = 4
_FACT_CHAR_LIMIT = 200
_PROOF_CHAR_LIMIT = 8000
_TRANSCRIPT_CHAR_LIMIT = 4000
_MIN_CONTENT_CHARS = 24
_CODE_FENCE_RE = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.DOTALL)


class WorkerLazymodeMixin:
    """Run one model-authored code-mode script before the agent.

    Expected on the composing worker: ``task_id``, ``store``, ``graph``,
    ``activity``, ``name``, ``_target_for``, ``_scope_allows_target`` and
    ``_publish_shell_proof``.
    """

    def _lazymode_enabled(self) -> bool:
        """Return whether the code-mode first attempt is active.

        Reads ``payload.json:loop_lazymode_first`` (default True).

        Returns:
            True when the worker should try a code-mode script first.
        """
        value = self._lazymode_payload().get(LAZYMODE_FIRST_KEY, True)
        if isinstance(value, str):
            return value.strip().lower() not in ("0", "false", "no", "off", "")
        return bool(value)

    @staticmethod
    def _lazymode_payload() -> dict[str, Any]:
        """Return the loaded payload, or an empty mapping on failure."""
        try:
            from core.config import load_payload

            return load_payload() or {}
        except Exception:
            return {}

    def _codemode_max_tokens(self) -> int:
        """Return the output-token cap for the script-authoring call."""
        try:
            value = int(self._lazymode_payload().get(LAZYMODE_MAX_TOKENS_KEY, _DEFAULT_MAX_TOKENS))
        except Exception:
            return _DEFAULT_MAX_TOKENS
        return value if value > 0 else _DEFAULT_MAX_TOKENS

    def _codemode_timeout(self) -> float:
        """Return the wall-clock timeout for the code-mode subprocess."""
        try:
            value = float(self._lazymode_payload().get(LAZYMODE_TIMEOUT_KEY, _DEFAULT_TIMEOUT_SEC))
        except Exception:
            return _DEFAULT_TIMEOUT_SEC
        return value if value > 0 else _DEFAULT_TIMEOUT_SEC

    @staticmethod
    def _sdk_surface() -> str:
        """Return a compact description of the ``lazy`` SDK surface.

        Introspected live from the facade so a new namespace or method
        appears without editing this prompt.

        Returns:
            One ``path signature - summary`` line per callable, or a terse
            fallback when the index cannot be built.
        """
        try:
            from sdk.lazymode import build_index

            lines = [
                f"{entry['path']}{entry['signature']} - {entry['summary']}".rstrip(" -")
                for entry in build_index()
            ]
            return "\n".join(lines)
        except Exception:
            return (
                "lazy.sh(command) - run a shell command, returns output\n"
                "lazy.recon.scan(target) / lazy.recon.ports(target) - nmap + parse\n"
                "lazy.search_exploits(query) - searchsploit\n"
                "lazy.config.get(key) / lazy.sessions.read(path)"
            )

    def _recent_facts(self) -> str:
        """Return a short transcript of this task's recent facts.

        Returns:
            Up to :data:`_CONTEXT_FACT_LIMIT` recent fact texts, bounded,
            or an empty string when none exist.
        """
        try:
            nodes = list(self.graph.list("fact"))
        except Exception:
            return ""
        lines = [str(node.text or "")[:_FACT_CHAR_LIMIT] for node in nodes[-_CONTEXT_FACT_LIMIT:]]
        return "\n".join(line for line in lines if line)

    def _codemode_prompt(self, intent, target: str) -> str:
        """Build the single-shot prompt that asks for one lazymode script.

        Args:
            intent: Intent the script must satisfy.
            target: Resolved target host, possibly empty.

        Returns:
            The prompt string handed to the model.
        """
        facts = self._recent_facts()
        return (
            "You are the LazyOwn code-mode worker. Instead of many tool calls, "
            "write ONE Python script that drives the framework through the `lazy` "
            "SDK object (already in scope) and does all the work for this intent "
            "in a single pass.\n\n"
            f"INTENT: {intent.text}\n"
            f"TARGET: {target or '(none; read from lazy.config)'}\n"
            f"{('RECENT FACTS:' + chr(10) + facts + chr(10)) if facts else ''}"
            "\nSDK surface (call paths):\n"
            f"{self._sdk_surface()}\n\n"
            "Rules:\n"
            "- `lazy` is ALREADY a defined global. Do NOT write `import lazy` or "
            "`from lazy import ...`; just use `lazy` directly.\n"
            "- You may use the Python stdlib (socket, subprocess, re, json).\n"
            "- Do the full job here: recon/enum/exploit as the intent needs.\n"
            "- Assign a dict to `result` summarizing findings. If you obtain a shell, "
            "put the proof (command output showing uid/root/prompt) under result['proof'] "
            "and set result['shell']=True.\n"
            "- No questions, no prose. Output ONLY a single ```python code block.\n\n"
            "Example:\n"
            "```python\n"
            "ports = lazy.recon.scan(target)\n"
            "banner = lazy.sh('curl -sI http://' + target)\n"
            "result = {'ports': ports, 'banner': banner}\n"
            "```"
        )

    @staticmethod
    def _extract_script(reply: str) -> str:
        """Return the Python source from a model reply.

        Args:
            reply: Raw model text.

        Returns:
            The fenced code block, the whole reply when it is plainly a
            script, or an empty string.
        """
        if not reply:
            return ""
        match = _CODE_FENCE_RE.search(reply)
        if match:
            return match.group(1).strip()
        if "result" in reply and ("lazy." in reply or "import " in reply):
            return reply.strip()
        return ""

    @staticmethod
    def _result_text(result) -> str:
        """Return the combined, bounded proof text from a run result."""
        parts: list[str] = []
        stdout = getattr(result, "stdout", "") or ""
        if stdout:
            parts.append(str(stdout))
        value = getattr(result, "result", None)
        if value is not None:
            try:
                parts.append(json.dumps(value, default=str))
            except Exception:
                parts.append(str(value))
        return "\n".join(parts)[:_PROOF_CHAR_LIMIT]

    def _lazymode_try(
        self,
        intent,
        outcome: dict,
        transcripts: list,
        executor,
        budget,
        deadline: float = 0.0,
    ) -> bool:
        """Drive the intent with one model-authored code-mode script.

        The model writes a single ``lazy`` SDK script; it runs through the
        existing ``sdk.lazymode.run`` in a bounded subprocess. The attempt
        owns the intent only when it produces real progress: an
        exploitation intent needs canonical shell evidence (via
        :meth:`_publish_shell_proof`); any other intent needs a non-trivial
        script result. Every other outcome returns False so the agent and
        then ``auto_pwn`` still run unchanged. Never raises.

        Args:
            intent: Intent being driven.
            outcome: Execution outcome dict to mutate on a win.
            transcripts: Executed ``(command, output)`` pairs to append to.
            executor: Worker command executor (unused; the script self-drives).
            budget: Task budget gate.
            deadline: Absolute intent wall-clock epoch; 0 disables the gate.

        Returns:
            True when the code-mode script owned the outcome.
        """
        if not self._lazymode_enabled():
            return False
        if deadline and time.time() >= deadline:
            return False
        try:
            if self.store.expired(self.task_id) or not budget.check(self.task_id)["ok"]:
                return False
        except Exception:
            pass
        target = (self._target_for(intent) or "").strip()
        if target:
            try:
                if not self._scope_allows_target(target):
                    return False
            except Exception:
                return False
        try:
            from modules.lazy_loop import LlmPool, _initial_access_intent, task_llm_chain
        except Exception:
            return False
        try:
            pool = LlmPool()
            chain = task_llm_chain(self.store, self.task_id)
        except Exception:
            return False
        if not pool.members() and not chain:
            return False
        self.activity.emit(
            self.name,
            "lazymode",
            f"code mode: asking the model for one SDK script (intent #{intent.node_id}; "
            "one call replaces the tool round-trips)",
            intent_id=intent.node_id,
        )
        try:
            reply = pool.complete(
                self._codemode_prompt(intent, target),
                max_tokens=self._codemode_max_tokens(),
                members=chain or None,
                task_id=self.task_id,
            ) or ""
        except Exception as exc:
            self.activity.emit(
                self.name, "lazymode", f"code mode: model error: {str(exc)[:160]}", intent_id=intent.node_id
            )
            return False
        script = self._extract_script(reply)
        if not script:
            self.activity.emit(
                self.name,
                "lazymode",
                "code mode: model returned no script; handing off to the agent",
                intent_id=intent.node_id,
            )
            return False
        try:
            from sdk.lazymode import run as lazymode_run

            result = lazymode_run(script, lang="python", timeout=self._codemode_timeout())
        except Exception as exc:
            self.activity.emit(
                self.name, "lazymode", f"code mode: run error: {str(exc)[:160]}", intent_id=intent.node_id
            )
            return False
        proof = self._result_text(result)
        command = f"lazymode:script#{intent.node_id}"
        transcripts.append((command, proof[:_TRANSCRIPT_CHAR_LIMIT]))
        self.activity.emit(
            self.name,
            "lazymode",
            f"code mode: script ok={result.ok} duration={result.duration_s:.1f}s "
            f"(no model tokens spent on execution)",
            intent_id=intent.node_id,
        )
        if not result.ok:
            error = str(getattr(result, "error", "") or "").strip().splitlines()[-1:] or [""]
            self.activity.emit(
                self.name,
                "lazymode",
                f"code mode: script failed ({error[0][:160]}); handing off to the agent then auto_pwn",
                intent_id=intent.node_id,
            )
            return False
        exploitation = bool(target) and _initial_access_intent((intent.text or "").lower())
        if target and self._publish_shell_proof(intent, target, command, proof):
            outcome["findings"] += 1
            outcome["state"] = "done"
            self.activity.emit(
                self.name,
                "lazymode",
                f"code mode: foothold on {target} via one SDK script; agent and auto_pwn skipped",
                intent_id=intent.node_id,
            )
            return True
        if exploitation:
            self.activity.emit(
                self.name,
                "lazymode",
                "code mode: script opened no proven shell; falling back to the agent then auto_pwn",
                intent_id=intent.node_id,
            )
            return False
        if self._codemode_has_content(result):
            outcome["facts"] += 1
            outcome["state"] = "done"
            self.activity.emit(
                self.name,
                "lazymode",
                f"code mode: intent #{intent.node_id} resolved in one call; agent skipped",
                intent_id=intent.node_id,
            )
            return True
        return False

    @staticmethod
    def _codemode_has_content(result) -> bool:
        """Return whether a non-exploitation script produced usable output.

        Args:
            result: The lazymode run result.

        Returns:
            True when the script result or stdout carries real content.
        """
        value = getattr(result, "result", None)
        if isinstance(value, dict) and value:
            return True
        if isinstance(value, (list, tuple)) and value:
            return True
        if isinstance(value, str) and len(value.strip()) >= _MIN_CONTENT_CHARS:
            return True
        stdout = str(getattr(result, "stdout", "") or "").strip()
        return len(stdout) >= _MIN_CONTENT_CHARS
