from __future__ import annotations

from modules.loop_guardrails import FactVectorStore


class WorkerMemoryMixin:
    """Durable and in-session memory behaviour for a loop worker.

    Groups the worker's failure counters, task-scoped vector memory and
    reactive absorption so the executing worker stays a thin coordinator.
    Every method binds to the host ``Worker`` through ``self`` and relies
    on the collaborators the worker sets in ``__init__`` (``activity``,
    ``store``, ``task_id``) plus ``_target_for`` for target resolution.
    """

    _ABSORB_OUTPUT_LIMIT = 4000

    def _failure_memory(self):
        """Return the durable failure memory, or None when unusable.

        The memory keeps per-target failure counters across loop
        restarts so an exhausted command never burns another round. A
        missing store directory is created by the memory itself and any
        import failure degrades to no memory at all.

        Returns:
            ``modules.auto_loop_memory.FailureMemory`` instance bound to
            the lazy store, or None.
        """
        try:
            from modules.auto_loop_memory import FailureMemory
            from modules.lazy_loop import _store_path

            return FailureMemory(_store_path("failure_memory.json"))
        except Exception:
            return None

    def _fact_memory_store(self) -> FactVectorStore:
        """Task-scoped vector memory, created on first use."""
        if self._fact_store is None:
            from modules.lazy_loop import _store_path

            self._fact_store = FactVectorStore(_store_path(f"vector_facts_{self.task_id}.json"))
        return self._fact_store

    def _remember_fact(self, intent, command: str, output: str) -> None:
        """Embed one successful step into the task's vector memory."""
        try:
            target = self._target_for(intent)
            digest = f"{command} :: target {target} :: {output[:600]}"
            self._fact_memory_store().add(digest, meta={"intent": intent.node_id, "target": target})
        except Exception:
            pass

    def _recall_facts(self, query: str, k: int = 4) -> str:
        """Retrieve the facts most relevant to the current step, prompt-ready."""
        try:
            return self._fact_memory_store().search_block(query, k=k)
        except Exception:
            return ""

    def _absorb_reaction(self, intent, command: str, output: str) -> None:
        """Park reactive decisions and reuse captured credentials in-session."""
        if not output or len(output) < 20:
            return
        self._remember_fact(intent, command, output)
        target = self._target_for(intent)
        try:
            from modules.mediation.contracts import MediationDomains
            from modules.mediation.hub import get_hub
            from modules.reaction_bridge import find_credentials

            creds = find_credentials(output[: self._ABSORB_OUTPUT_LIMIT])
            if creds:
                engines = get_hub().mediator_for(MediationDomains.ENGINES)
                queued = engines.retry_with_credentials(target, credentials=creds) if engines else 0
                self.activity.emit(
                    self.name,
                    "cred-reuse",
                    f"{queued} credential pair(s) from step output fed to retry engine ({target})",
                    intent_id=intent.node_id,
                )
        except Exception:
            pass
        try:
            from modules.mediation.contracts import MediationDomains
            from modules.mediation.hub import get_hub
            from modules.reaction_bridge import ReactionPick
            from modules.reaction_bridge import save_decisions as _save_reactions

            platform = "unknown"
            try:
                from modules.world_model import WorldModel

                platform = str(WorldModel().snapshot().get("hosts", {}).get(target, {}).get("platform", "unknown"))
            except Exception:
                platform = "unknown"
            engines = get_hub().mediator_for(MediationDomains.ENGINES)
            decisions = (
                engines.analyse(output[: self._ABSORB_OUTPUT_LIMIT], command, platform)
                if engines is not None
                else []
            )
            picks = [
                ReactionPick(command=str(d.command), reason=str(d.reason), priority=int(d.priority), mitre=str(d.mitre_tactic))
                for d in decisions
                if str(getattr(d, "command", "") or "").strip()
            ]
            if picks:
                _save_reactions(self.task_id, picks[:3])
                self.activity.emit(
                    self.name,
                    "reactive",
                    f"parked {len(picks[:3])} reactive decision(s) for next planner round",
                    intent_id=intent.node_id,
                )
        except Exception:
            pass
