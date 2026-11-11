from __future__ import annotations

import json
import re
from collections.abc import Mapping
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.lazy_loop import Budget, ExplorationNode, InterceptQueue

_MAX_COMMAND_CHARS = 300
_LINE_LEAD = re.compile(r"^[\d\-\*\.\)\s]+")


def _planner_temperature() -> float:
    """Return the deterministic planner temperature, defaulting to greedy.

    Delegates to :func:`modules.lazy_loop.planner_temperature` so the pinned
    value lives in one place; any import or config failure falls back to a
    fully greedy ``0.0`` rather than reintroducing sampling noise.
    """
    try:
        from modules.lazy_loop import planner_temperature

        return planner_temperature()
    except Exception:
        return 0.0


def _verb_of(command: str) -> str:
    """Return the leading verb of a command for attribution demotion."""
    try:
        from modules.outcome_attribution import verb_of

        return verb_of(command)
    except Exception:
        return ""


def _loop_deterministic() -> bool:
    """Return whether the loop runs in fully reproducible mode.

    In deterministic mode the worker prefers its heuristic, evidence-based
    steps and only consults the LLM when the deterministic layer produced
    nothing, so an identical engagement state replays the same primary
    action without any model variance. The flag is read from
    ``payload.json:loop_deterministic`` (default off) and never raises.
    """
    try:
        from core.config import load_payload

        return bool((load_payload() or {}).get("loop_deterministic", False))
    except Exception:
        return False


def _is_placeholder_steps(steps: list[str]) -> bool:
    """Return True when steps carry no real probe, only a no-target notice.

    The heuristic planner emits a single ``echo no-target`` line when scope is
    missing; that is not a reproducible action worth preferring over the LLM
    fallback, so deterministic mode still defers to the model in that case.
    """
    if not steps:
        return True
    if len(steps) == 1 and steps[0].startswith("echo no-target"):
        return True
    return False


def _strip_command(raw: str) -> str:
    """Normalise one proposed command line into a bare shell string."""
    return _LINE_LEAD.sub("", str(raw or "").strip()).strip("`").strip()


def _extract_llm_commands(reply: str) -> list[str]:
    """Parse planner output into an ordered, de-duplicated command list.

    The planner is asked for a JSON array of ``{"command", "reason", "mitre"}``
    objects; this honours that contract first so a well-formed reply is parsed
    exactly. A model that ignores the contract and emits bare lines still
    degrades gracefully through the legacy line parser, so no backend regresses
    to zero suggestions. Order is preserved and duplicates collapse, which is
    what makes the downstream ledger candidate list stable.

    Args:
        reply: The raw model reply.

    Returns:
        Up to a bounded set of candidate command strings, in first-seen order.
    """
    text = str(reply or "").strip()
    if not text:
        return []
    commands: list[str] = []
    seen: set[str] = set()

    def _push(value: str) -> None:
        command = _strip_command(value)
        if not command or len(command) > _MAX_COMMAND_CHARS:
            return
        if command in seen:
            return
        seen.add(command)
        commands.append(command)

    parsed = _try_json_commands(text)
    if parsed is not None:
        for item in parsed:
            _push(item)
        return commands
    for line in text.splitlines():
        _push(line)
    return commands


def _try_json_commands(text: str) -> list[str] | None:
    """Return command strings from a JSON array reply, or None when not JSON.

    Args:
        text: The trimmed model reply.

    Returns:
        The extracted ``command`` fields when the reply is a JSON array of
        objects (or strings), otherwise ``None`` so the caller can fall back to
        line parsing. A fenced ```json block is unwrapped first.
    """
    candidate = text
    if candidate.startswith("```"):
        candidate = re.sub(r"^```[a-zA-Z0-9]*\n?", "", candidate)
        candidate = re.sub(r"\n?```$", "", candidate).strip()
    start = candidate.find("[")
    end = candidate.rfind("]")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        data = json.loads(candidate[start : end + 1])
    except ValueError:
        return None
    if not isinstance(data, list):
        return None
    out: list[str] = []
    for item in data:
        if isinstance(item, Mapping):
            value = item.get("command") or item.get("cmd") or ""
            if value:
                out.append(str(value))
        elif isinstance(item, str):
            out.append(item)
    return out


class WorkerAgenticMixin:
    """Tool-calling agent loop and LLM step planning for a loop worker.

    Groups the agentic path: the guard-enforced tool catalogue handed to
    the model, the invariant system prompt, the multi-attempt agent
    session, operator steer drainage, stop-reason checkpoints and the
    deterministic LLM step suggestions used when tool-calling is off.
    Every method binds to the host ``Worker`` through ``self``.
    """

    def _agent_checkpoint(self, intent: ExplorationNode) -> str:
        """Return the stop reason for the agent loop, or empty to continue."""
        from modules.lazy_loop import Budget

        if (self.store.get(self.task_id) or {}).get("status") == "paused":
            return "paused"
        if self.store.killed(self.task_id, intent.node_id):
            return "killed"
        if self.store.expired(self.task_id):
            return "expired"
        try:
            if not Budget(self.store).check(self.task_id)["ok"]:
                return "budget"
        except Exception:
            pass
        return ""

    def _drain_steer(self, intent: ExplorationNode) -> str:
        """Return and clear a pending operator steer as a model message."""
        steer = self.store.steer_for(self.task_id, intent.node_id)
        if not steer:
            return ""
        self.store.clear_steer(self.task_id, intent.node_id)
        self.activity.emit(
            self.name, "steer", f"delivered to agent as operator message: {steer}", intent_id=intent.node_id
        )
        return steer

    def _agent_preflight(self, intent: ExplorationNode, command: str) -> str:
        """Guard preflight for agent side channels; empty when allowed.

        Background jobs and persistent-shell commands must pass the same
        scope, deny-constraint, binary and guard checks as foreground
        steps; returns the refusal text or an empty string.
        """
        target = self._target_for(intent)
        if target and not self._scope_allows_target(target):
            return "[SYSTEM] blocked by scope policy: target outside authorized scope."
        denied = self._denied(command)
        if denied:
            return f"[SYSTEM] blocked by deny constraint '{denied}'."
        sudo_ok, _sudo_reason = self._sudo_guard(intent, command)
        if not sudo_ok:
            return "[SYSTEM] skipped: sudo requires a terminal and this loop is unattended."
        gap = self._missing_tool(command)
        if gap:
            return f"[SYSTEM] skipped: binary '{gap}' is not installed."
        decision = self.guard.check("Bash", command, source="worker-side-channel", intent_id=intent.node_id)
        self.activity.emit(
            self.name,
            "tool",
            f"[{decision['action']}] (side-channel) {command[:200]}",
            intent_id=intent.node_id,
            tool_use_id=str(decision.get("tool_use_id", "")),
        )
        if decision["action"] == "deny":
            return f"[SYSTEM] blocked by guard: {decision.get('reason', 'denied')}."
        if decision["action"] == "ask" and not self._auto_approve(command):
            return "[SYSTEM] held for approval; run it as a foreground command instead so the operator can decide."
        return ""

    def _agent_tools(
        self,
        intent: ExplorationNode,
        executor,
        transcripts: list,
        budget: Budget,
        intercept: InterceptQueue,
        retry_state: dict,
    ) -> list[dict]:
        """Tool specs handed to the agentic worker (guard-enforced)."""
        from modules.lazy_loop import FindingService

        def run_command(command: str = "", background: bool = False) -> str:
            """Run one shell probe/verb through scope, guard and audit.

            With ``background`` the command is launched as a tracked job
            (job_status/job_output) instead of blocking the model turn.
            """
            reason = self._agent_checkpoint(intent)
            if reason:
                return f"[SYSTEM] stop requested: {reason}. Reply with your final summary now."
            if background:
                refusal = self._agent_preflight(intent, command)
                if refusal:
                    return refusal
                return self._start_background_job(command, intent, transcripts)
            output, status, detail = self._guard_step(intent, command, executor, budget, intercept, retry_state)
            if status == "blocked":
                return f"[SYSTEM] blocked by policy: {detail}. Do not retry that exact command."
            if status == "skipped":
                return f"[SYSTEM] skipped: binary '{detail}' is not installed. Use another approach."
            transcripts.append((command, output))
            self._absorb_reaction(intent, command, output)
            steer = self._drain_steer(intent)
            if steer:
                output = f"[OPERATOR MESSAGE] {steer}\nAdjust course accordingly before continuing.\n{output}"
            return output or "(no output)"

        def record_fact(text: str = "") -> str:
            """Persist one observed or inferred fact on the exploration graph."""
            node = self.graph.add_node(
                "fact", str(text)[:600], state="done", meta={"agent": True, "intent": intent.node_id}
            )
            self.graph.add_edge(intent.node_id, node.node_id, "yields")
            self.activity.emit(self.name, "agent-fact", str(text)[:300], intent_id=intent.node_id)
            return f"fact recorded as #{node.node_id}"

        def report_finding(name: str = "", evidence: str = "", severity: str = "medium") -> str:
            """Record a verified vulnerability with its evidence."""
            finding = FindingService(self.task_id, self.graph, self.activity, self.store).report(
                name=name or "agent finding",
                summary=evidence[:400],
                poc=evidence,
                severity=severity,
                intent_id=intent.node_id,
            )
            return f"finding #{finding.node_id} [{finding.meta.get('severity')}] recorded"

        def traffic_search(query: str = "") -> str:
            """Search captured command/traffic records by keyword."""
            hits = self.traffic.search(str(query), limit=5)
            compact = [
                {
                    "command": str(row.get("command", ""))[:160],
                    "preview": str(row.get("preview", ""))[:200],
                    "digest": str(row.get("digest", ""))[:12],
                }
                for row in hits
            ]
            return json.dumps(compact, ensure_ascii=False)[:1500] or "no hits"

        def graph_state() -> str:
            """Compact exploration overview: intents, facts, findings."""
            overview = self.graph.overview()
            compact = {
                "facts_total": overview.get("facts", 0),
                "findings": overview.get("findings", 0),
                "recent_facts": [str(f.get("text", ""))[:160] for f in overview.get("fact_list", [])[-6:]],
                "open_intents": [
                    str(i.get("text", ""))[:120]
                    for i in overview.get("intents", [])
                    if i.get("state") in ("open", "running", "pending")
                ][:6],
            }
            return json.dumps(compact, ensure_ascii=False)[:1500]

        def shell_open() -> str:
            """Open a persistent bash session for multi-step shell work."""
            return self._open_shell_session(intent)

        def shell_send(command: str = "") -> str:
            """Run one guarded command in the persistent shell session."""
            return self._send_shell(command, intent)

        def job_status(job_id: str = "") -> str:
            """Report whether one background job is still running."""
            entry = self._jobs.get(str(job_id))
            if entry is None:
                return f"unknown job: {job_id}"
            state = "done" if entry.get("done") else "running"
            return f"{job_id}: {state} ({len(entry.get('output', []))} output lines)"

        def job_output(job_id: str = "") -> str:
            """Return the tail of one background job's output."""
            entry = self._jobs.get(str(job_id))
            if entry is None:
                return f"unknown job: {job_id}"
            state = "done" if entry.get("done") else "running"
            tail = "".join(entry.get("output", [])[-80:])
            return f"{job_id} [{state}]\n{tail[-3000:] or '(no output yet)'}"

        return [
            {
                "name": "run_command",
                "func": run_command,
                "description": "Execute one shell command or LazyOwn verb; returns its output. "
                "All calls pass scope, guard and audit.",
                "parameters": {"command": {"type": "string", "description": "Command line to execute"}},
                "required": ["command"],
            },
            {
                "name": "record_fact",
                "func": record_fact,
                "description": "Persist one factual observation (positive or negative).",
                "parameters": {"text": {"type": "string", "description": "Fact text with evidence"}},
                "required": ["text"],
            },
            {
                "name": "report_finding",
                "func": report_finding,
                "description": "Record a verified vulnerability; evidence is required.",
                "parameters": {
                    "name": {"type": "string", "description": "Finding title"},
                    "evidence": {"type": "string", "description": "Proof and output"},
                    "severity": {"type": "string", "description": "critical|high|medium|low"},
                },
                "required": ["name", "evidence"],
            },
            {
                "name": "traffic_search",
                "func": traffic_search,
                "description": "Search previously captured tool traffic by keyword.",
                "parameters": {"query": {"type": "string", "description": "Keyword"}},
                "required": ["query"],
            },
            {
                "name": "graph_state",
                "func": graph_state,
                "description": "Read the compact exploration overview.",
                "parameters": {},
                "required": [],
            },
            {
                "name": "shell_open",
                "func": shell_open,
                "description": "Open a persistent bash session for multi-step work "
                "(state survives between shell_send calls).",
                "parameters": {},
                "required": [],
            },
            {
                "name": "shell_send",
                "func": shell_send,
                "description": "Run one guarded command inside the persistent shell session.",
                "parameters": {"command": {"type": "string", "description": "Command line"}},
                "required": ["command"],
            },
            {
                "name": "job_status",
                "func": job_status,
                "description": "Report the state of one background job.",
                "parameters": {"job_id": {"type": "string", "description": "Job id"}},
                "required": ["job_id"],
            },
            {
                "name": "job_output",
                "func": job_output,
                "description": "Return the tail output of one background job.",
                "parameters": {"job_id": {"type": "string", "description": "Job id"}},
                "required": ["job_id"],
            },
        ]

    def _agent_system_prompt(self, intent: ExplorationNode) -> str:
        """Invariant agent contract: goal, intent, scope, constraints, rules."""
        from modules.lazy_loop import constraint_block

        record = self.store.get(self.task_id) or {}
        constraints = constraint_block(record.get("constraints", []), scope="worker")[:400]
        scope = [f"{s.get('kind')}:{s.get('value')}" for s in (record.get("scope", []) or [])][:8]
        skills_block = ""
        try:
            from modules.lazy_skills import skills_context

            skills_block = skills_context(
                f"{record.get('goal', '')} {intent.text[:120]}",
                explicit=list(record.get("skills", []) or []),
                auto=bool(record.get("skills_auto", True)),
                budget=600,
            )
        except Exception:
            skills_block = ""
        return (
            "You are the LazyOwn worker agent of an authorized penetration test.\n"
            f"Task goal: {str(record.get('goal', ''))[:300]}\n"
            f"Intent #{intent.node_id}: {intent.text[:300]}\n"
            f"Authorized scope: {', '.join(scope) or 'see constraints'}\n"
            f"Constraints: {constraints or 'none'}\n"
            f"{skills_block + chr(10) if skills_block else ''}"
            "Rules: use run_command for every probe (it enforces scope/guard/audit). "
            "Prefer lazynmap <target> over raw nmap so scans persist in sessions/. "
            "Read each result before the next call, never repeat an identical command. "
            "Persist positive and negative observations with record_fact; report only "
            "actually-triggered vulnerabilities with report_finding (evidence required). "
            "Finish with a concise factual summary."
        )

    def _agentic_try(
        self,
        intent: ExplorationNode,
        outcome: dict,
        transcripts: list,
        executor,
        budget: Budget,
        intercept: InterceptQueue,
        retry_state: dict,
    ) -> bool:
        """Run the intent through a real tool-calling agent when configured.

        Returns True when the agentic path executed (successfully or
        not); False falls back to the deterministic step loop.
        """
        from modules.lazy_loop import LlmPool

        try:
            from modules import lazy_agent
        except Exception:
            return False
        if not lazy_agent.tool_calling_enabled():
            return False
        tools = self._agent_tools(intent, executor, transcripts, budget, intercept, retry_state)
        self.activity.emit(
            self.name, "agent", f"tool-calling agent start: intent #{intent.node_id}", intent_id=intent.node_id
        )
        launch_prompt = (
            "Execute the intent now with the available tools. "
            "Inspect results between calls. When done, reply with "
            "a concise factual summary."
        )
        steer = self._drain_steer(intent)
        if steer:
            launch_prompt = f"[OPERATOR MESSAGE] {steer}\n\n{launch_prompt}"
        result = None
        tried: set[str] = set()
        for _attempt in range(3):
            try:
                model = lazy_agent.resolve_agentic_model(exclude=tried)
            except Exception:
                model = None
            if model is None:
                break
            model_name = str(getattr(model, "model", "model"))
            tried.add(model_name)
            try:
                result = lazy_agent.run_worker_session(
                    model=model,
                    task_id=self.task_id,
                    intent_id=intent.node_id,
                    system_prompt=self._agent_system_prompt(intent),
                    launch_prompt=launch_prompt,
                    tools=tools,
                    on_event=lambda kind, name, text: self.activity.emit(
                        self.name, f"agent-{kind}", f"{name}: {text[:400]}", intent_id=intent.node_id
                    ),
                )
                break
            except Exception as exc:
                member_name = str(getattr(model, "_lazy_member_name", model_name))
                self.activity.emit(
                    self.name,
                    "agent-error",
                    f"{model_name}: {str(exc)[:240]}; trying next member",
                    intent_id=intent.node_id,
                )
                try:
                    pool = LlmPool()
                    if pool._health is not None:
                        pool._health.report_failure(member_name, str(exc)[:200])
                except Exception:
                    pass
                continue
        if result is None:
            return False
        reply = str(result.get("reply", "")).strip()
        if reply and not transcripts:
            node = self.graph.add_node(
                "fact",
                f"agent summary intent #{intent.node_id}: {reply[:500]}",
                state="done",
                meta={"agent": True, "intent": intent.node_id},
            )
            self.graph.add_edge(intent.node_id, node.node_id, "yields")
            outcome["facts"] += 1
        stop_reason = self._agent_checkpoint(intent)
        if stop_reason == "paused":
            self.graph.set_state(intent.node_id, "pending")
            outcome["state"] = "stopped"
        elif stop_reason in ("killed", "expired"):
            outcome["state"] = "stopped"
        elif stop_reason == "budget":
            self.graph.set_state(intent.node_id, "pending")
            outcome["state"] = "blocked"
        self.activity.emit(
            self.name, "agent", f"tool-calling agent done: {result.get('tool_calls', {})}", intent_id=intent.node_id
        )
        return True

    def _with_llm_steps(self, intent: ExplorationNode, steps: list[str], prior_text: str = "") -> list[str]:
        """Merge pool-suggested commands with the deterministic steps.

        Default mode prefixes the LLM suggestions, keeping the heuristic steps
        as fallback. Deterministic mode inverts the contract: when the
        heuristic layer produced real probes it wins outright and the model is
        not consulted, so the primary action replays identically. The model is
        still the fallback when scope is missing and the heuristic emitted only
        a placeholder.

        Args:
            intent: The intent being expanded into steps.
            steps: The deterministic steps from :meth:`_steps_for`.
            prior_text: Prior transcript for the intent, passed to the planner.

        Returns:
            The ordered, de-duplicated step list, capped at the worker budget.
        """
        from modules.lazy_loop import MAX_WORKER_STEPS

        if _loop_deterministic() and not _is_placeholder_steps(steps):
            self.activity.emit(
                self.name, "deterministic", "deterministic mode: heuristic steps win, model not consulted",
                intent_id=intent.node_id,
            )
            return steps[:MAX_WORKER_STEPS]
        suggested = []
        try:
            from modules.harness import gate as _harness_gate

            if _harness_gate("worker_llm_steps"):
                suggested = self._llm_steps(intent, prior_text)
        except Exception:
            suggested = []
        if not suggested:
            return steps
        order = [*steps, *suggested] if _loop_deterministic() else [*suggested, *steps]
        merged: list[str] = []
        for command in order:
            if command not in merged:
                merged.append(command)
        return merged[:MAX_WORKER_STEPS]

    def _llm_steps(self, intent: ExplorationNode, prior_text: str = "") -> list[str]:
        """Ask the pool for up to three concrete next commands for this intent.

        Suggestions are filtered before execution: denied by config,
        missing binaries and out-of-scope hosts never reach the loop.
        """
        from modules.lazy_loop import (
            LlmPool,
            build_prompt_context,
            constraint_block,
            plausible_command,
            task_llm_chain,
        )

        try:
            pool = LlmPool()
            chain = task_llm_chain(self.store, self.task_id)
            if not pool.members() and not chain:
                return []
            target = self._target_for(intent)
            record = self.store.get(self.task_id) or {}
            context = build_prompt_context(
                self.task_id, self.graph, self.assets, self.store, budget=pool.context_budget(), top=6
            )
            constraints = constraint_block(record.get("constraints", []), scope="worker")[:400]
            prior_block = (
                f"Previous transcript for this intent (continue from here, do not repeat):\n{prior_text[:1200]}\n"
                if prior_text
                else ""
            )
            memory_block = self._recall_facts(f"{str(record.get('goal', ''))[:200]} {intent.text[:200]} {target}")
            memory_section = (
                f"Known facts similar to the current step (vector memory):\n{memory_block}\n"
                if memory_block
                else ""
            )
            prompt = (
                f"Task goal: {str(record.get('goal', ''))[:300]}\n"
                f"Intent: {intent.text[:300]}\n"
                f"Target: {target or 'unknown'}\n"
                f"{context}\n"
                f"{prior_block}"
                f"{memory_section}"
                f"Constraints: {constraints}\n"
                "Propose up to 3 shell commands to advance this intent. Reply with a "
                'JSON array of objects, each {"command": "<shell>", "reason": "<why>", '
                '"mitre": "<Txxxx or empty>"}, and nothing else. Use only tools '
                "installed on this host. Never leave the authorized target. Never use "
                "sudo: this runs unattended without a tty, so sudo commands always "
                "fail. Prefer lazynmap <target> over raw nmap: it persists XML, "
                "post-scan artefacts and intel in sessions/ automatically."
            )
            temperature = _planner_temperature()
            reply = (
                pool.complete(
                    prompt,
                    max_tokens=400,
                    members=chain or None,
                    task_id=self.task_id,
                    on_delta=self._delta_sink(intent.node_id),
                    temperature=temperature,
                )
                or ""
            )
        except Exception:
            return []
        candidates = _extract_llm_commands(reply)
        blocked_verbs = self._blocked_verbs()
        guard = self._guard_rules()
        out: list[str] = []
        seen: set[str] = set()
        filtered: list[tuple[str, str]] = []
        sudo_skipped = 0
        for command in candidates:
            if len(command) < 4 or len(command) > 300 or command.startswith("#"):
                filtered.append((command, "shape"))
                continue
            if command.split(maxsplit=1)[0] == "sudo":
                sudo_skipped += 1
                filtered.append((command, "sudo-no-tty"))
                continue
            if guard is not None and guard.blocks_command(command):
                filtered.append((command, "guard-rule"))
                continue
            if blocked_verbs and _verb_of(command) in blocked_verbs:
                filtered.append((command, "attrib-blocked"))
                continue
            if command.strip() in ("bash", "sh", "zsh"):
                filtered.append((command, "bare-shell"))
                continue
            if not plausible_command(command):
                filtered.append((command, "implausible"))
                continue
            if self._missing_tool(command) or self._denied(command):
                filtered.append((command, "missing-or-denied"))
                continue
            command = self._sanitize_step(intent, command)
            if not command or command in seen:
                filtered.append((command, "empty-or-duplicate"))
                continue
            if self._missing_tool(command) or self._denied(command):
                filtered.append((command, "missing-or-denied"))
                continue
            if not self._command_in_scope(command):
                filtered.append((command, "out-of-scope"))
                continue
            seen.add(command)
            out.append(command)
            if len(out) >= 3:
                break
        self._record_llm_decision(intent, prompt, reply, candidates, out, filtered)
        if sudo_skipped:
            self.activity.emit(
                self.name,
                "capability",
                f"skip {sudo_skipped} sudo step(s): unattended loop has no tty",
                intent_id=intent.node_id,
            )
        if out:
            self.activity.emit(
                self.name, "llm", f"pool proposed {len(out)} step(s): {' | '.join(out)[:400]}", intent_id=intent.node_id
            )
        return out

    def _blocked_verbs(self) -> set[str]:
        """Return verbs the target has repeatedly blocked for this task.

        The planner demotes these so a verb the target keeps refusing with a
        WAF or rate limiter is not re-proposed round after round, which is the
        strategy-change the failure attribution exists to drive. Any failure
        returns an empty set so attribution never widens into a hard gate.

        Returns:
            The set of blocked verbs, empty when none or on error.
        """
        try:
            from modules.outcome_attribution import AttributionLedger

            return AttributionLedger(self.task_id).blocked_verbs()
        except Exception:
            return set()

    def _guard_rules(self):
        """Return the seeded guard ruleset for this task, or None on failure.

        Guard rules arm the planner filter from the first round with a baseline
        of commands an unattended loop must never emit, before any attribution
        data has accrued. Any failure returns None so the guard can only ever
        add safety, never gate the loop into silence.

        Returns:
            A :class:`~modules.guard_rules.GuardRules` instance, or None.
        """
        try:
            from modules.guard_rules import GuardRules

            return GuardRules(self.task_id)
        except Exception:
            return None

    def _record_llm_decision(
        self,
        intent: ExplorationNode,
        prompt: str,
        reply: str,
        candidates: list[str],
        chosen: list[str],
        filtered: list[tuple[str, str]],
    ) -> None:
        """Append the planner's choice to the reproducible decision ledger.

        The record proves which command the LLM planner committed to, which
        candidates it rejected and why, and fingerprints the prompt and reply
        so an identical engagement state can be recognised on replay. Ledger
        failures never interrupt the loop.

        Args:
            intent: The intent the planner advanced.
            prompt: The exact model prompt issued.
            reply: The raw model reply.
            candidates: Every command parsed from the reply before filtering.
            chosen: The commands that survived every gate.
            filtered: Rejected candidates paired with their reason.
        """
        try:
            from modules.loop import decision_log

            payload: dict = {}
            try:
                from core.config import load_payload

                payload = load_payload() or {}
            except Exception:
                payload = {}
            rec = decision_log.DecisionRecord(
                run_id=f"task:{self.task_id}",
                step=int(getattr(intent, "node_id", 0) or 0),
                source="llm",
                model_fallback=True,
                chosen=(chosen[0] if chosen else ""),
                reason=(f"{len(chosen)} of {len(candidates)} candidate(s) accepted"),
                ctx_digest=decision_log.digest(f"{intent.text}|{self.task_id}"),
                config_digest=decision_log.config_digest(payload),
                prompt_digest=decision_log.digest(prompt),
                reply_digest=decision_log.digest(reply),
                candidates=tuple(candidates),
                filtered=decision_log.filtered_rows(filtered),
            )
            decision_log.record(rec)
        except Exception:
            return
