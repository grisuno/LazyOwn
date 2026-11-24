from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.lazy_loop import ActivityLog, ExplorationGraph, ExplorationNode


class EngineVerdictMixin:
    """Extracted LazyLoopEngine methods (verbatim lift + lazy imports).

    Each method injects its ``modules.lazy_loop`` module-level dependencies as a
    lazy import to avoid a circular import at load time. See
    modules/loop/README.md for the decomposition contract.
    """

    def goal_met(self, task_id: str, reason: str = "") -> bool:
        """Declare the whole task complete like goal_met (weighted, audited)."""
        from modules.lazy_loop import ActivityLog, ExplorationGraph

        graph = ExplorationGraph(task_id)
        for node in graph.list("goal"):
            graph.set_state(node.node_id, "done")
        self.store.set_status(task_id, "done")
        self.runtime.abort(task_id, "goal_met", reason[:300] or "operator declared complete")
        ActivityLog(task_id).emit("planner", "goal", f"goal_met: {reason[:200]}")
        return True

    def record_fact(self, task_id: str, text: str, evidence: str = "", intent_id: int = 0) -> ExplorationNode:
        """Operator-visible fact write like recordFact."""
        from modules.lazy_loop import ActivityLog, ExplorationGraph

        graph = ExplorationGraph(task_id)
        node = graph.record_fact(text, evidence=evidence, intent_id=int(intent_id))
        ActivityLog(task_id).emit("human", "fact", text[:300], intent_id=int(intent_id))
        return node

    def record_verdict(self, task_id: str, finding_id: int, verdict: str, note: str = "") -> dict:
        """Record an operator retest verdict on one finding.

        Args:
            task_id: Task owning the finding.
            finding_id: Finding node id.
            verdict: One of ``reproduced``, ``fixed``, ``inconclusive``.
            note: Optional evidence note.

        Returns:
            Dict with finding_id and the stored verdict.

        Raises:
            KeyError: Unknown finding id.
            ValueError: Unsupported verdict.
        """
        from modules.lazy_loop import RETEST_VERDICTS, ActivityLog, ExplorationGraph

        if verdict not in RETEST_VERDICTS:
            raise ValueError(f"verdict must be one of {RETEST_VERDICTS}")
        graph = ExplorationGraph(task_id)
        finding = graph.get(int(finding_id))
        if finding is None or finding.kind != "finding":
            raise KeyError(f"unknown finding: {finding_id}")
        finding.meta["retest"] = {
            "verdict": verdict,
            "attempts": 0,
            "evidence": note[:1000],
            "note": note[:300],
            "source": "operator",
        }
        if verdict == "fixed":
            finding.state = "done"
            finding.meta["status"] = "fixed"
            finding.meta["vstate"] = "discarded"
        elif verdict == "reproduced":
            finding.state = "done"
            finding.meta["vstate"] = "confirmed"
            finding.meta["level"] = "critical" if str(finding.meta.get("severity", "")) == "critical" else "confirmed"
        else:
            finding.state = "done"
            finding.meta["status"] = "inconclusive"
            finding.meta["vstate"] = "partial"
            finding.meta["retest_terminal"] = True
        graph.persist()
        ActivityLog(task_id).emit("human", "verdict", f"finding #{finding_id}: {verdict} {note[:120]}")
        try:
            from modules.outcome_bus import record_event

            record_event(
                kind="finding",
                task_id=task_id,
                title=f"operator verdict #{finding_id}: {verdict}",
                severity=str(finding.meta.get("severity", "")),
                mitre_id=str(finding.meta.get("technique_id", "")),
                confidence=1.0,
                success=verdict == "reproduced",
                source="operator",
                command=str(finding.meta.get("poc", ""))[:500],
                output=note[:1500],
                artifacts=list(finding.meta.get("traffic_refs", []) or []),
                metadata={
                    "finding_id": finding_id,
                    "finding_ref": str(finding_id),
                    "verdict": verdict,
                    "technique_id": str(finding.meta.get("technique_id", "")),
                    "state": str(finding.meta.get("vstate", "")),
                    "level": str(finding.meta.get("level", "")),
                    "refresh_report": False,
                },
            )
        except Exception:
            pass
        return {"finding_id": int(finding_id), "verdict": verdict}

    def _evaluate_goal(self, task_id: str) -> dict:
        """Judge the task against its original goal, independent of step claims.

        Ports the evaluator idea: every subtask may report success while the
        user objective stands unmet. The verdict derives from graph evidence
        (findings, coverage, facts), never from worker self-reports; an LLM
        turn only upgrades the wording when a pool exists. The report lands
        at ``sessions/lazy/report_<task>.md`` for the operator and the dataset.

        Returns:
            Verdict dict with goal, verdict, coverage, counts and path.
        """
        from modules.lazy_loop import (
            ActivityLog,
            ExplorationGraph,
            LlmPool,
            _ledger_confirmed_count,
            _ledger_side_hits,
            _store_path,
            task_llm_chain,
        )

        verdict: dict = {"task_id": task_id, "verdict": "failed", "path": ""}
        try:
            record = self.store.get(task_id) or {}
            goal = str(record.get("goal", "") or "")
            status = str(record.get("status", "") or "")
            graph = ExplorationGraph(task_id)
            activity = ActivityLog(task_id)
            scope = record.get("scope", []) or []
            coverage = self.assets.coverage_for(graph, scope)
            facts = [n for n in graph.list("fact") if not n.meta.get("cold_digest")]
            findings = graph.list("finding")
            confirmed = [
                n for n in findings if str(n.state) in ("confirmed",) or "reproduced" in str(n.meta.get("verdict", ""))
            ]
            ledger_confirmed = _ledger_confirmed_count(task_id)
            confirmed_count = max(len(confirmed), ledger_confirmed)
            lowered_goal = goal.lower()
            wants_creds = any(k in lowered_goal for k in ("cred", "password", "hash", "login"))
            wants_access = any(
                k in lowered_goal for k in ("access", "shell", "session", "own", "exploit", "compromis", "foothold")
            )
            wants_lateral = any(k in lowered_goal for k in ("lateral", "pivot", "propagate", "spread", "move to"))
            lateral_hit = False
            if wants_lateral:
                scope_values = [str((item or {}).get("value", "") or "") for item in scope if (item or {}).get("value")]
                primary = scope_values[0] if scope_values else ""
                scoped_ips = {
                    str((item or {}).get("value", "") or "") for item in scope if (item or {}).get("kind") == "ip"
                }
                lateral_hit = any(ip and ip in (n.text or "") for n in findings for ip in scoped_ips if ip != primary)
                if not lateral_hit:
                    not_before = float((record.get("runtime") or {}).get("started", 0) or 0)
                    lateral_hit = bool(_ledger_side_hits(task_id, sorted(scoped_ips), primary, not_before))
            cred_hit = any(
                k in (n.text or "").lower() for n in findings for k in ("password", "hash", "login:", "credential")
            )
            if status == "done":
                verdict["verdict"] = "achieved"
            elif wants_lateral and not lateral_hit:
                verdict["verdict"] = "partial"
                verdict["completion_reason"] = (
                    "goal asks for lateral movement but no scoped side host carries finding evidence yet"
                )
            elif wants_creds and cred_hit:
                verdict["verdict"] = "achieved"
            elif wants_access and confirmed_count:
                verdict["verdict"] = "achieved"
            elif facts or (coverage.get("tested", 0) or 0) > 0:
                verdict["verdict"] = "partial"
            try:
                from modules import lazy_finalizer

                decision = lazy_finalizer.decide(
                    status=status,
                    candidate_verdict=verdict["verdict"],
                    facts=len(facts),
                    findings=len(findings),
                    confirmed=confirmed_count,
                    tested=int(coverage.get("tested", 0) or 0),
                )
                if decision.verdict != verdict["verdict"]:
                    activity.emit(
                        "planner",
                        "finalizer",
                        f"verdict {verdict['verdict']} -> {decision.verdict} ({decision.completion_reason})",
                    )
                verdict["verdict"] = decision.verdict
                verdict["evidence_verified"] = decision.evidence_verified
                verdict["completion_reason"] = decision.completion_reason
                if decision.missing_checks:
                    verdict["missing_checks"] = decision.missing_checks
            except Exception:
                pass
            if verdict["verdict"] == "achieved":
                self._mark_goals_achieved(task_id, graph, activity)
            verdict.update(
                {
                    "goal": goal[:300],
                    "status": status,
                    "coverage_pct": coverage.get("pct", 0.0),
                    "tested": coverage.get("tested", 0),
                    "total": coverage.get("total", 0),
                    "facts": len(facts),
                    "findings": len(findings),
                    "confirmed": confirmed_count,
                }
            )
            note = ""
            try:
                pool = LlmPool()
                chain = task_llm_chain(self.store, task_id)
                if pool.members() or chain:
                    from modules.lazy_roles import role_prompt as _role_prompt

                    prompt = (
                        _role_prompt(
                            "mirror",
                            goal,
                            f"coverage={coverage.get('pct', 0)}% facts={len(facts)} findings={len(findings)} confirmed={confirmed_count}",
                        )
                        + " Reply with one verdict line: achieved, partial or failed, plus why."
                    )
                    note = (
                        pool.complete(prompt, max_tokens=120, members=chain or None, task_id=task_id) or ""
                    ).strip()[:400]
            except Exception:
                note = ""
            if note:
                verdict["review"] = note
            lines = [
                f"# Lazy verdict {task_id}",
                "",
                f"- goal: {goal[:300]}",
                f"- verdict: {verdict['verdict']} (engine status: {status})",
                f"- coverage: {coverage.get('pct', 0)}% tested={coverage.get('tested', 0)}/{coverage.get('total', 0)}",
                f"- facts={len(facts)} findings={len(findings)} confirmed={confirmed_count}",
            ]
            if note:
                lines += ["", f"> {note}"]
            if findings:
                lines.append("")
                for node in findings[-20:]:
                    lines.append(f"- finding #{node.node_id}[{node.state}] {node.text[:140]}")
            path = _store_path(f"report_{task_id}.md")
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            verdict["path"] = str(path)
            activity.emit(
                "planner",
                "verdict",
                f"{verdict['verdict']}: coverage={coverage.get('pct', 0)}% facts={len(facts)} findings={len(findings)}",
            )
        except Exception:
            pass
        return verdict

    def prove_goal(self, task_id: str, goal_id: int, evidence_id: int, reason: str) -> bool:
        """Mark goal met with finding/fact evidence like the planner prove_goal.

        Refuses quantitative goals (coverage %, N flags) unless the
        overview actually satisfies them — never stamp early.
        """
        from modules.lazy_loop import ActivityLog, ExplorationGraph

        graph = ExplorationGraph(task_id)
        goal = graph.get(goal_id)
        evidence = graph.get(evidence_id)
        if goal is None or evidence is None or goal.kind != "goal":
            return False
        if evidence.kind not in ("finding", "fact"):
            return False
        lowered = goal.text.lower()
        if any(mark in lowered for mark in ("100%", "coverage", "all ports", "every")):
            record = self.store.get(task_id) or {}
            coverage = self.assets.coverage_for(graph, record.get("scope", []))
            if float(coverage.get("pct", 0.0)) < 100.0:
                ActivityLog(task_id).emit(
                    "planner", "skip", f"goal #{goal_id} quantitative bar unmet ({coverage.get('pct', 0)}%)"
                )
                return False
        if not (reason or "").strip():
            return False
        graph.add_edge(evidence_id, goal_id, "proves")
        graph.set_state(goal_id, "done")
        ActivityLog(task_id).emit("planner", "goal", f"goal #{goal_id} proven by #{evidence_id}: {reason[:200]}")
        if self._goals_met(task_id):
            self.store.set_status(task_id, "done")
        else:
            self.store.resume(task_id)
        return True

    def _foothold_evidence_id(self, graph: ExplorationGraph) -> int | None:
        """Return a graph finding node that evidences a foothold, if any.

        Prefers a confirmed/reproduced finding; falls back to any finding
        whose text or captured output carries interactive-shell evidence.

        Args:
            graph: Task exploration graph.

        Returns:
            A finding ``node_id`` usable as ``prove_goal`` evidence, or None.
        """
        from modules.lazy_loop import _FOOTHOLD_FINDING_MARKS

        try:
            from modules.atomic_exploit_bridge import shell_output_evidence
        except Exception:
            shell_output_evidence = None
        fallback: int | None = None
        for node in graph.list("finding"):
            lowered = (node.text or "").lower()
            is_foothold = any(mark in lowered for mark in _FOOTHOLD_FINDING_MARKS)
            if not is_foothold and shell_output_evidence is not None:
                blob = str((node.meta or {}).get("evidence", "") or (node.meta or {}).get("output", "") or "")
                is_foothold = bool(blob and shell_output_evidence(blob[:5000]))
            if not is_foothold:
                continue
            confirmed = str(node.state) == "confirmed" or "reproduced" in str(node.meta.get("verdict", ""))
            if confirmed:
                return node.node_id
            if fallback is None:
                fallback = node.node_id
        return fallback

    def _mark_goals_achieved(self, task_id: str, graph: ExplorationGraph, activity: ActivityLog) -> None:
        """Credit pending goal nodes once the wrap-up verdict is achieved.

        The round-time goal checker keeps a lone initial-access goal pending
        on purpose (the planner stops once every goal is done), so goal nodes
        legitimately lag behind an achieved campaign and the operator footer
        reads ``goals 0/2`` under ``achieved``. At wrap-up the achieved
        verdict is authoritative: every surviving pending goal is credited
        against the strongest confirmed finding. Conservative: without a
        confirmed finding node the footer stays behind rather than lying.

        Args:
            task_id: Engagement identifier.
            graph: Task exploration graph.
            activity: Activity log for the proven-by trace.
        """
        pending = graph.list("goal", "pending")
        if not pending:
            return
        evidence = None
        for candidate in graph.list("finding"):
            if str(candidate.state) in ("confirmed",) or "reproduced" in str(candidate.meta.get("verdict", "")):
                evidence = candidate
                break
        if evidence is None:
            return
        for goal in pending:
            graph.add_edge(evidence.node_id, goal.node_id, "proves")
            graph.set_state(goal.node_id, "done")
            activity.emit(
                "planner",
                "goal",
                f"goal #{goal.node_id} proven by #{evidence.node_id}: wrap-up verdict achieved",
            )

    def _check_goals(self, task_id: str, graph: ExplorationGraph, activity: ActivityLog) -> None:
        """Prove goals from evidence.

        Two rules: a goal whose text appears verbatim in a finding is
        proven by that finding; an initial-access goal is proven once this
        engagement confirms a foothold, because foothold findings describe
        the outcome ("shell obtained") and never echo the goal wording
        ("gain initial access"), so the literal rule alone can never credit
        it and the loop would re-attempt the foothold forever.

        The foothold rule is gated on a surviving downstream objective. A
        foothold never credits the initial-access goal when that goal is
        the whole engagement (no non-initial-access goal stays pending),
        because crediting the sole goal marks every goal done, and the
        planner stops planning once all goals are done
        (:meth:`Planner.plan` returns nothing when every goal is done), so
        :meth:`_goals_met` fires and the campaign ends at the foothold
        instead of advancing to privesc, lateral and exfil. The kill chain
        already advances on evidence, not goal state
        (:meth:`Planner._initial_access_candidate` is gated by
        :func:`_target_foothold_proven`), so leaving the lone initial-access
        goal pending keeps the planner driving the rest of the kill chain
        until rounds or budget run out. With a downstream goal present the
        foothold credits initial access and a never-proven downstream goal
        keeps the loop alive, so the kill chain progresses either way.
        """
        from modules.lazy_loop import (
            _initial_access_intent,
            _target_foothold_proven,
            resolve_target,
        )

        pending_goals = graph.list("goal", "pending")
        if not pending_goals:
            return
        record = self.store.get(task_id) or {}
        target = (resolve_target(task_id, self.store, graph) or str(record.get("target", "") or "")).strip()
        foothold = bool(target) and _target_foothold_proven(target, task_id)
        foothold_evidence = self._foothold_evidence_id(graph) if foothold else None
        downstream_pending = any(not _initial_access_intent(goal.text.lower()) for goal in pending_goals)
        for goal in pending_goals:
            matched = False
            for finding in graph.list("finding"):
                if goal.text[:40].lower() in finding.text.lower():
                    self.prove_goal(task_id, goal.node_id, finding.node_id, "finding text entails goal")
                    matched = True
                    break
            if matched:
                continue
            if (
                foothold
                and foothold_evidence is not None
                and downstream_pending
                and _initial_access_intent(goal.text.lower())
            ):
                self.prove_goal(task_id, goal.node_id, foothold_evidence, "confirmed foothold proves initial access")

    def _goals_met(self, task_id: str) -> bool:
        """Report whether every goal node is done."""
        from modules.lazy_loop import ExplorationGraph

        graph = ExplorationGraph(task_id)
        goals = graph.list("goal")
        return bool(goals) and all(g.state == "done" for g in goals)

    def _foothold_proven(self, target: str, task_id: str = "") -> bool:
        """Report whether this engagement already reached an initial foothold.

        Delegates to the module-level :func:`_target_foothold_proven`, the one
        foothold gate shared with the planner's deterministic access path. The
        gate reads per-engagement evidence only, so a host exploited by a prior
        campaign never suppresses ``auto_pwn`` in a fresh run.

        Args:
            target: Target host address.
            task_id: Engagement identifier whose own evidence decides the gate.

        Returns:
            True when this engagement already recorded a confirmed foothold.
        """
        from modules.lazy_loop import _target_foothold_proven

        return _target_foothold_proven(target, task_id)

    def _terminal_autopwn_fallback(self, task_id: str, executor, activity: ActivityLog) -> bool:
        """Run ``auto_pwn`` as the guaranteed terminal fallback.

        The ultimate purpose of the loop is to win a foothold; the operator
        goal text is secondary. When the round loop exhausts without a proven
        shell, this runs the deterministic ``auto_pwn <target>`` engine once,
        independent of the goal wording, and publishes a shell proof when the
        output carries interactive-shell evidence. Never raises.

        Args:
            task_id: Engagement identifier.
            executor: Command executor ``(command) -> output``; required.
            activity: Activity log for operator-visible breadcrumbs.

        Returns:
            True when the fallback obtained an interactive shell.
        """
        from modules.lazy_loop import ExplorationGraph, _auto_pwn_cover_all, resolve_target

        if executor is None:
            return False
        target = (resolve_target(task_id, self.store, ExplorationGraph(task_id)) or "").strip()
        if not target or self._foothold_proven(target, task_id):
            return False
        reuse = None
        try:
            from modules.atomic_exploit_bridge import probe_live_shell

            reuse = probe_live_shell(target)
        except Exception:
            reuse = None
        if reuse is not None:
            owner = str(reuse.get("owner", ""))
            activity.emit(
                "engine",
                "fallback",
                f"live shell already on {target}; reusing session {owner} instead of re-running auto_pwn",
            )
            return self._publish_fallback_shell(
                task_id,
                target,
                f"id -u via live shell {owner}",
                str(reuse.get("output", "")),
                activity,
                reused=True,
            )
        try:
            from modules.auto_registry import verb_enabled, verb_gap

            if verb_gap("auto_pwn") or not verb_enabled("auto_pwn"):
                return False
        except Exception:
            pass
        vector = "auto_pwn"
        claim_effect = release_effect = None
        try:
            from modules.atomic_exploit_bridge import claim_effect, release_effect
        except Exception:
            claim_effect = release_effect = None
        if claim_effect is not None and not claim_effect(target, vector):
            activity.emit(
                "engine",
                "fallback",
                f"auto_pwn already in flight for {target}; skipping duplicate terminal fallback",
            )
            return False
        cover = " --all" if _auto_pwn_cover_all() else ""
        command = f"auto_pwn {target}{cover}".strip()
        activity.emit(
            "engine",
            "fallback",
            f"loop exhausted without a shell; terminal auto_pwn fallback: {command}",
        )
        try:
            output = str(executor(command) or "")
        except Exception as exc:
            activity.emit("engine", "fallback", f"terminal auto_pwn fallback error: {str(exc)[:160]}")
            return False
        finally:
            if release_effect is not None:
                try:
                    release_effect(target, vector)
                except Exception:
                    pass
        try:
            from modules.atomic_exploit_bridge import shell_output_evidence

            shelled = bool(shell_output_evidence((output or "")[:5000]))
        except Exception:
            shelled = False
        if not shelled:
            activity.emit("engine", "fallback", "terminal auto_pwn fallback produced no shell evidence")
            return False
        return self._publish_fallback_shell(task_id, target, command, output, activity, reused=False)

    def _publish_fallback_shell(
        self,
        task_id: str,
        target: str,
        command: str,
        output: str,
        activity: ActivityLog,
        reused: bool = False,
    ) -> bool:
        """Publish a terminal-fallback shell proof to the outcome bus.

        Shared by the fresh ``auto_pwn`` fallback and the reuse-of-live-session
        path so both emit one consistent critical exploit event and operator
        breadcrumb. Never raises.

        Args:
            task_id: Engagement identifier.
            target: Host the shell runs on.
            command: Command or reuse marker that evidenced the shell.
            output: Captured shell evidence.
            activity: Activity log for operator-visible breadcrumbs.
            reused: Whether the shell came from reusing a cached session
                rather than a fresh exploitation.

        Returns:
            True always, mirroring a successful foothold.
        """
        title = "shell via reused live session" if reused else "shell via terminal auto_pwn fallback"
        source = "lazy_loop_fallback_reuse" if reused else "lazy_loop_fallback"
        try:
            from modules.outcome_bus import record_event

            record_event(
                kind="exploit",
                target=target,
                host=target,
                task_id=task_id,
                title=title,
                description=f"{title} carries interactive-shell evidence ({command})",
                severity="critical",
                success=True,
                shell=True,
                source=source,
                command=command[:400],
                output=(output or "")[:1500],
                metadata={"fallback": True, "reused": reused},
            )
        except Exception:
            pass
        done = f"reused live shell on {target}" if reused else "terminal auto_pwn fallback obtained a shell"
        activity.emit("engine", "fallback", done)
        return True

    def _engagement_decision(self, task_id: str, round_index: int, summary: dict) -> str:
        """Decide structural stops after one round: handoff or pentest stop.

        The qualitative progress rule counts consecutive rounds without
        objective evidence (facts/findings/reproduced verdicts/goals);
        hypotheses alone never reset the counter. In ``pentest`` mode the
        first reproduced-or-confirmed finding settles the engagement
        instead of deep exploitation.

        Args:
            task_id: Engagement identifier.
            round_index: Just-finished round number.
            summary: Round summary from ``run_round``.

        Returns:
            ``""`` to continue, ``"handoff"`` after the strike cap, or
            ``"pentest_proven"`` in pentest mode with confirmed evidence.
        """
        from modules.lazy_loop import STORE_DIR, ActivityLog, ExplorationGraph, _ledger_side_hits

        mode = str(getattr(self, "engagement_mode", "") or "").strip().lower()
        graph = ExplorationGraph(task_id)
        goals_done = sum(1 for goal in graph.list("goal") if goal.state == "done")
        explained = [1 for finding in graph.list("finding") if str(finding.meta.get("vstate", "")) in ("confirmed",)]
        brief = {
            "facts": int((summary.get("overview") or {}).get("facts", 0) or 0),
            "findings": int((summary.get("overview") or {}).get("findings", 0) or 0),
            "goals_done": goals_done,
            "reproduced": len(explained),
            "new_intents": int(summary.get("new_intents", 0) or 0),
        }
        try:
            from modules import orchestrator_config
            from modules.progress_ledger import ProgressLedger, StrikePolicy

            try:
                progress = orchestrator_config.progress_config()
                policy = StrikePolicy(
                    max_strikes=int(progress.get("max_strikes", 3) or 3),
                    handoff_on_strikes=bool(progress.get("handoff_on_strikes", True)),
                )
            except Exception as config_exc:
                ActivityLog(task_id).emit(
                    "engine",
                    "progress",
                    f"progress config unavailable, using defaults: {str(config_exc)[:100]}",
                )
                policy = StrikePolicy()
            ledger = ProgressLedger(task_id, STORE_DIR, policy).load()
            signals = ledger.signals_from_brief(brief)
            result = ledger.observe(signals, note=f"round {round_index}")
            ActivityLog(task_id).emit(
                "engine",
                "progress",
                f"round {round_index}: {result['decision']} "
                f"strikes={result['strikes']}/{result['max_strikes']} ({result['reason']})",
            )
        except Exception as exc:
            ActivityLog(task_id).emit("engine", "progress", f"progress ledger unavailable: {str(exc)[:120]}")
            result = {"decision": ""}
        if mode == "pentest" and explained:
            record = self.store.get(task_id) or {}
            goal = str(record.get("goal", "") or "").lower()
            wants_lateral = any(k in goal for k in ("lateral", "pivot", "propagate", "spread", "move to"))
            if wants_lateral:
                scope_items = [
                    str((item or {}).get("value", "") or "")
                    for item in (record.get("scope", []) or [])
                    if (item or {}).get("kind") == "ip" and (item or {}).get("value")
                ]
                primary = scope_items[0] if scope_items else ""
                not_before = float((record.get("runtime") or {}).get("started", 0) or 0)
                side_hits = [
                    1
                    for finding in graph.list("finding")
                    for ip in scope_items
                    if ip and ip != primary and ip in (finding.text or "")
                ]
                if not side_hits and _ledger_side_hits(task_id, scope_items, primary, not_before):
                    side_hits = [1]
                if not side_hits:
                    ActivityLog(task_id).emit(
                        "engine",
                        "pentest-stop",
                        "foothold proven but goal asks for lateral movement; continuing "
                        "(no side-host finding evidence yet)",
                    )
                    return ""
                ActivityLog(task_id).emit(
                    "engine",
                    "pentest-decision",
                    f"lateral goal satisfied: side evidence found ({len(scope_items)} scoped, primary {primary})",
                )
            return "pentest_proven"
        if str(result.get("decision", "")) == "handoff":
            self._archive_discards(task_id, last_results=summary.get("results", []) or [])
            return "handoff"
        return ""
