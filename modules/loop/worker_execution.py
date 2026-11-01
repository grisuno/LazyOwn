from __future__ import annotations

import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.lazy_loop import ExplorationNode


class WorkerExecutionMixin:
    """Command execution, background jobs and persistent-shell lifecycle for a loop worker.

    Groups the mechanics of actually running a step: dispatch through the
    injected executor or the LazyOwn registry, tracked background jobs, a
    persistent bash session, alias resolution and the small admissibility
    helpers (deny constraints, auto-approval, missing binaries). Every
    method binds to the host ``Worker`` through ``self`` and relies on the
    collaborators set in ``__init__`` (``activity``, ``store``, ``shell``,
    ``_jobs``, ``_shell_session``, ``_shell_queue``).
    """

    def _start_background_job(self, command: str, intent: ExplorationNode, transcripts: list) -> str:
        """Launch one guarded command as a tracked background job.

        Returns the model-facing acknowledgment with the job id. The
        output stays queryable through the job_status/job_output tools
        and is folded into the intent transcript once finished.
        """
        from modules.auto_registry import execute_streaming
        from modules.lazy_loop import _now

        job_id = f"job_{len(self._jobs) + 1}"
        entry: dict = {"id": job_id, "command": command, "output": [], "done": False, "result": "", "ts": _now()}

        def _work() -> None:
            try:
                entry["result"] = execute_streaming(command, on_output=entry["output"].append)
            except Exception as exc:
                entry["result"] = f"execution failed: {exc}"
            finally:
                entry["done"] = True

        thread = threading.Thread(target=_work, daemon=True, name=job_id)
        entry["thread"] = thread
        self._jobs[job_id] = entry
        thread.start()
        self.activity.emit(
            self.name, "job", f"{job_id} started in background: {command[:160]}", intent_id=intent.node_id
        )
        transcripts.append((command, f"[background {job_id}] started"))
        return (
            f"[SYSTEM] background job {job_id} started. Poll it with job_status('{job_id}') and job_output('{job_id}')."
        )

    def _open_shell_session(self, intent: ExplorationNode) -> str:
        """Start a persistent bash session for the agentic loop."""
        import os
        import queue as _queue
        import subprocess

        process = self._shell_session
        if process is not None and process.poll() is None:
            return "shell session already open"
        environment = {**os.environ, "PS1": "", "TERM": "dumb", "LAZYOWN_AUTONOMOUS": "1"}
        self._shell_session = subprocess.Popen(  # noqa: S603 - fixed argv
            ["bash"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            start_new_session=True,
            env=environment,
        )
        self._shell_queue = _queue.Queue()

        def _reader() -> None:
            session = self._shell_session
            try:
                if session is not None and session.stdout is not None:
                    for line in session.stdout:
                        self._shell_queue.put(line)
            except Exception:
                return

        threading.Thread(target=_reader, daemon=True, name="shell-reader").start()
        self.activity.emit(self.name, "shell", "persistent shell session opened (bash)", intent_id=intent.node_id)
        return "shell session open; run commands with shell_send(command)"

    def _send_shell(self, command: str, intent: ExplorationNode, timeout_sec: float = 30.0) -> str:
        """Run one guarded command inside the persistent shell session."""
        import os
        import queue as _queue
        import time as _time

        process = self._shell_session
        queue_obj = self._shell_queue
        if process is None or process.stdin is None or queue_obj is None:
            return "no shell session; call shell_open first"
        refusal = self._agent_preflight(intent, command)
        if refusal:
            return refusal
        marker = f"__LAZY_DONE_{os.getpid()}_{_time.time_ns()}__"
        try:
            process.stdin.write(f"{command}\nprintf '%s\\n' {marker}\n")
            process.stdin.flush()
        except OSError as exc:
            return f"shell write failed: {exc}"
        deadline = _time.monotonic() + max(1.0, float(timeout_sec or 30.0))
        lines: list[str] = []
        while _time.monotonic() < deadline:
            remaining = max(0.05, min(0.5, deadline - _time.monotonic()))
            try:
                line = queue_obj.get(timeout=remaining)
            except _queue.Empty:
                continue
            if marker in line:
                output = "".join(lines)[-4000:]
                self.activity.emit(
                    self.name, "shell", f"$ {command[:160]} -> {len(output)} chars", intent_id=intent.node_id
                )
                return output or "(no output)"
            lines.append(line)
        return "timeout waiting for shell output; partial:\n" + "".join(lines)[-2000:]

    def _close_shell_session(self) -> None:
        """Terminate the persistent shell session, if any."""
        import os
        import signal

        process = self._shell_session
        self._shell_session = None
        self._shell_queue = None
        if process is None:
            return
        try:
            if process.stdin is not None:
                process.stdin.close()
        except Exception:
            pass
        try:
            process.wait(timeout=2)
        except Exception:
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            except Exception:
                try:
                    process.kill()
                except Exception:
                    pass
        self.activity.emit(self.name, "shell", "persistent shell session closed", intent_id=0)

    def _denied(self, command: str) -> str:
        """Return matching worker-scope deny constraint text or empty string."""
        lowered = (command or "").lower()
        record = self.store.get(self.task_id) or {}
        for item in record.get("constraints", []) or []:
            if str((item or {}).get("scope", "both") or "both") not in ("worker", "both"):
                continue
            if (item or {}).get("type") == "deny" and str(item.get("text", "")).lower() in lowered:
                return str(item.get("text"))
        return ""

    def _auto_approve(self, command: str) -> bool:
        """Auto-approve read-only probes, hold the rest for approval."""
        lowered = (command or "").lower()
        read_only = ("nmap", "curl", "dig", "host ", "whatweb", "nikto", "enum")
        if lowered.startswith(read_only):
            return True
        try:
            from modules.auto_registry import is_shell_verb as _is_auto_verb
        except Exception:
            return False
        return _is_auto_verb(lowered)

    def _missing_tool(self, command: str) -> str:
        """Return the binary a probe needs but the host lacks, else ''.

        Automation verbs run through the shell and their tooling was
        already gated by the registry, so only raw bash probes are
        preflighted here.
        """
        try:
            from modules.auto_registry import is_routable_command, missing_binary

            if is_routable_command(command):
                return ""
            return missing_binary(command)
        except Exception:
            return ""

    def _run(self, command: str, executor) -> str:
        """Execute command through injected executor or LazyOwn runner."""
        if (command or "").startswith("custom tool "):
            if executor is not None:
                try:
                    return str(executor(command) or "")
                except Exception as exc:
                    return f"execution failed: {exc}"
            try:
                from modules.custom_tools import run_tool

                parts = (command or "").split(maxsplit=4)
                name = parts[2] if len(parts) > 2 else ""
                arg = " ".join(parts[3:]).strip() if len(parts) > 3 else ""
                return str(run_tool(name, arg) or "")
            except Exception as exc:
                return f"execution failed: {exc}"
        try:
            from modules.auto_registry import is_routable_command as _routable

            routable = _routable(command)
        except Exception:
            routable = False
        if routable:
            if executor is not None:
                try:
                    return str(executor(command) or "")
                except Exception as exc:
                    return f"execution failed: {exc}"
            if getattr(self, "shell", None) is not None:
                try:
                    from modules.auto_registry import execute_shell_verb as _shell_verb

                    return _shell_verb(self.shell, command)
                except Exception as exc:
                    return f"execution failed: {exc}"
            return (
                "execution failed: automation verb needs a shell context "
                f"(run via auto_loop or lazy_loop from the shell): {command[:120]}"
            )
        try:
            if executor is not None:
                result = executor(command)
                return str(result or "")
            from modules.auto_registry import execute_streaming as _stream

            return _stream(command)
        except Exception as exc:
            return f"execution failed: {exc}"

    def _resolved_command(self, command: str) -> str:
        """Expand the first-token shell alias so checks see through it."""
        text = str(command or "").strip()
        if not text:
            return text
        token = text.split()[0]
        aliases = getattr(self.shell, "aliases", None)
        if isinstance(aliases, dict):
            macro = aliases.get(token)
            if macro:
                rest = " ".join(text.split()[1:])
                return f"{macro} {rest}".strip()
        return text
