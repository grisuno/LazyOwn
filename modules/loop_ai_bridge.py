"""Single edge between the autonomous loop and the LazyOwn AI stack.

The loop does not reimplement AI plumbing: this bridge is the one place
where it publishes events to the unified event bus, feeds the episodic
Hive Mind memory, consults the detection oracle, uses the MoE router
and RL trainer for expert selection and outcome learning, and can ask
SWAN for an ensemble plan. Every call is guarded and gated by an
orchestrator stage toggle, so disabling a stage (or an unavailable
dependency) degrades to a no-op instead of breaking the loop.
"""

from __future__ import annotations

import threading

STREAM_KINDS = frozenset({"tool", "result", "llm", "agent-turn", "agent-tool", "hb"})
HIVE_KINDS = frozenset({"finding", "verdict", "round", "finish", "task", "sync", "settle", "block"})

_CATEGORY = {
    "finding": "finding",
    "verdict": "finding",
    "cred": "credential",
    "credential": "credential",
    "loot": "loot",
    "exploit": "exploit",
    "enriched": "recon",
    "enrich": "recon",
    "block": "error",
    "deny": "error",
    "agent-error": "error",
    "round": "system",
    "task": "system",
    "wake": "system",
    "heartbeat": "system",
    "sync": "system",
    "intel": "system",
}

_SEVERITY = {
    "block": "warning",
    "deny": "warning",
    "agent-error": "warning",
    "finding": "high",
}

_SINGLETON_LOCK = threading.Lock()
_SINGLETONS: dict = {}


def _singleton(key: str, factory):
    """Return a process-wide instance built lazily, or None on failure."""
    with _SINGLETON_LOCK:
        if key in _SINGLETONS:
            return _SINGLETONS[key]
    try:
        instance = factory()
    except Exception:
        instance = None
    with _SINGLETON_LOCK:
        _SINGLETONS.setdefault(key, instance)
        return _SINGLETONS[key]


def _stage(name: str, default: bool = True) -> bool:
    """Return the orchestrator stage flag, tolerant of config failures."""
    try:
        from modules.orchestrator_config import stage_enabled

        return bool(stage_enabled(name))
    except Exception:
        return default


def publish_loop_event(task_id: str, worker: str, kind: str, text: str, severity: str = "info") -> None:
    """Publish one loop activity to the unified bus and Hive memory.

    Raw stream kinds (tool output, LLM chatter) are skipped so the event
    ledger stays meaningful; everything else gets a category, severity
    and the task id in its payload.
    """
    if str(kind) in STREAM_KINDS or not _stage("ai_bus"):
        return
    category = _CATEGORY.get(str(kind), "discovery")
    sev = _SEVERITY.get(str(kind), severity)
    try:
        from modules.event_bus import publish_event

        publish_event(
            category,
            f"loop:{kind}",
            source=f"loop/{worker}",
            payload={"task_id": task_id, "worker": worker, "text": str(text)[:1500]},
            severity=sev,
        )
    except Exception:
        pass
    if str(kind) in HIVE_KINDS:
        _hive_store(task_id, worker, kind, text)


def _hive_store(task_id: str, worker: str, kind: str, text: str) -> None:
    """Persist one meaningful activity into Hive Mind episodic memory."""

    def _open():
        from skills.hive_mind import EpisodicStore

        return EpisodicStore()

    store = _singleton("hive", _open)
    if store is None:
        return
    try:
        store.store(
            f"{kind}: {text}"[:2000],
            agent_id="lazy_loop",
            role=str(worker)[:40],
            event_type="loop_activity",
            meta={"task_id": task_id, "kind": str(kind)},
            session_tag=str(task_id),
        )
    except Exception:
        pass


def annotate_detection(command: str, action_category: str = "execution") -> dict | None:
    """Return oracle details for one command, or None when unavailable."""
    if not _stage("detection_oracle"):
        return None

    def _open():
        from modules.detection_oracle import get_oracle

        return get_oracle()

    oracle = _singleton("oracle", _open)
    if oracle is None:
        return None
    try:
        assessment = oracle.assess("bash", str(command), action_category)
    except Exception:
        return None
    return {
        "probability": float(assessment.probability),
        "sigma_names": list(assessment.sigma_names or [])[:4],
        "recommendation": str(assessment.recommendation or "")[:200],
    }


def moe_route(task_type: str, goal: str = ""):
    """Return the MoE router's preferred expert for a task type, or None."""

    def _open():
        from modules.moe_router import get_router

        return get_router()

    router = _singleton("moe_router", _open)
    if router is None:
        return None
    try:
        return router.route(str(task_type), goal, deterministic=True)
    except Exception:
        return None


def moe_record_outcome(expert_id: str, task_type: str, reward: float, detection_prob: float = 0.0) -> None:
    """Feed one execution outcome back to the MoE performance store."""
    if not _stage("rl_feedback"):
        return

    def _open():
        from modules.moe_router import get_router

        return get_router()

    router = _singleton("moe_router", _open)
    if router is None:
        return
    try:
        router.record_outcome(str(expert_id), str(task_type), float(reward), float(detection_prob))
    except Exception:
        pass


def rl_select(task_type: str, phase: str, candidates: list[str], deterministic: bool = False) -> str:
    """Pick an expert with the RL policy; first candidate when unavailable."""
    if not candidates:
        return ""
    if not _stage("rl_feedback"):
        return str(candidates[0])

    def _open():
        from modules.rl_trainer import get_trainer

        return get_trainer()

    trainer = _singleton("rl_trainer", _open)
    if trainer is None:
        return str(candidates[0])
    try:
        state = trainer.encode_state(str(task_type), str(phase))
        return str(trainer.select_action(state, list(candidates), force_exploit=bool(deterministic)))
    except Exception:
        return str(candidates[0])


def rl_update(
    task_type: str, phase: str, action: str, reward: float, candidates: list[str], detection_prob: float = 0.0
) -> None:
    """Apply one Q-learning update for an executed action."""
    if not _stage("rl_feedback") or not candidates:
        return

    def _open():
        from modules.rl_trainer import get_trainer

        return get_trainer()

    trainer = _singleton("rl_trainer", _open)
    if trainer is None:
        return
    try:
        state = trainer.encode_state(str(task_type), str(phase))
        next_state = trainer.encode_state(str(task_type), str(phase), float(reward))
        trainer.update(state, str(action), float(reward), next_state, list(candidates), float(detection_prob))
    except Exception:
        pass


def rl_save() -> None:
    """Persist the RL tables after a run."""
    if not _stage("rl_feedback"):
        return

    def _open():
        from modules.rl_trainer import get_trainer

        return get_trainer()

    trainer = _singleton("rl_trainer", _open)
    if trainer is None:
        return
    try:
        trainer.save()
    except Exception:
        pass


def record_step(task_id: str, worker: str, command: str, output: str, detection_prob: float = 0.0) -> None:
    """Feed one executed command outcome to MoE and the RL trainer.

    Reward is 1.0 for a productive run (output present, no execution
    failure) and 0.0 otherwise; the action is the command's first token
    so the trainer learns which tool classes work for this engagement.
    """
    text = str(output or "")
    reward = 1.0 if text.strip() and not text.startswith("execution failed:") else 0.0
    moe_record_outcome(f"worker:{worker}", "execution", reward, detection_prob)
    action = str(command or "").strip().split(maxsplit=1)
    token = action[0] if action else "unknown"
    rl_update("execution", "exploit", token, reward, [token], detection_prob)


def swan_available() -> bool:
    """Return True when the SWAN orchestrator can be constructed."""
    if not _stage("swan_ensemble", default=False):
        return False

    def _open():
        from skills.swan_agent import get_swan

        return get_swan()

    return _singleton("swan", _open) is not None


def swan_consult(prompt: str, task_type: str = "recon", phase: str = "enumeration", timeout: float = 120.0) -> str:
    """Ask SWAN for an ensemble answer; empty string when unavailable."""
    if not swan_available():
        return ""
    with _SINGLETON_LOCK:
        swan = _SINGLETONS.get("swan")
    if swan is None:
        return ""
    try:
        result = swan.run(task_type, str(prompt)[:4000], phase, timeout)
    except Exception:
        return ""
    output = str(getattr(result, "output", "") or "").strip()
    if not output:
        return ""
    try:
        moe_record_outcome(
            str(getattr(result, "expert_id", "swan")),
            task_type,
            float(getattr(result, "reward", 0.0) or 0.0),
            float(getattr(result, "detection_prob", 0.0) or 0.0),
        )
    except Exception:
        pass
    return output


def stream_enabled() -> bool:
    """Return whether token streaming into the activity log is enabled.

    Returns:
        True when the ``llm_stream`` stage is on; the pool then asks the
        LLM factory for incremental deltas and reports them as activity.
    """
    return _stage("llm_stream")


def ai_snapshot() -> dict:
    """Compact status of the wired AI stack for the operator log."""
    snapshot: dict = {
        "bus": _stage("ai_bus"),
        "oracle": False,
        "rl_epsilon": None,
        "moe": None,
        "swan": False,
        "hive": False,
    }
    try:
        from modules.detection_oracle import get_oracle

        oracle = get_oracle()
        snapshot["oracle"] = getattr(oracle, "rule_count", None) or len(getattr(oracle, "rules", []) or [])
    except Exception:
        snapshot["oracle"] = False
    if _stage("rl_feedback"):
        try:
            from modules.rl_trainer import get_trainer

            snapshot["rl_epsilon"] = round(float(get_trainer().epsilon), 3)
        except Exception:
            snapshot["rl_epsilon"] = None
        try:
            from modules.moe_router import get_router

            report = get_router().status_report()
            snapshot["moe"] = {key: report.get(key) for key in ("experts", "temperature") if key in report} or True
        except Exception:
            snapshot["moe"] = None
    snapshot["swan"] = swan_available()
    snapshot["hive"] = _stage("ai_bus")
    return snapshot


__all__ = [
    "ai_snapshot",
    "annotate_detection",
    "moe_record_outcome",
    "moe_route",
    "publish_loop_event",
    "record_step",
    "rl_save",
    "rl_select",
    "rl_update",
    "swan_available",
    "swan_consult",
]
