from __future__ import annotations

import json
import os
import time
from typing import Any

from modules.selection.command_selector import CommandDecision, ICommandSelector

__all__ = [
    "ReactiveSelector",
    "LLMSelector",
    "SWANSelector",
    "FallbackSelector",
    "MetricsAwareSelector",
    "UnifiedBrainSelector",
]


def _daemon():
    """Return the live autonomous_daemon module object.

    ``skills`` is not a package, so the daemon can be imported both as
    ``autonomous_daemon`` (skills dir on sys.path) and as
    ``skills.autonomous_daemon``. The selectors read daemon-level helpers and
    monkeypatchable module state (``SESSIONS_DIR``, ``EVENTS_FILE``) through this
    resolver so they always bind to the same module object the caller uses,
    preferring an already-imported one.
    """
    import sys

    return (
        sys.modules.get("skills.autonomous_daemon")
        or sys.modules.get("autonomous_daemon")
        or __import__("skills.autonomous_daemon", fromlist=["__name__"])
    )


class ReactiveSelector(ICommandSelector):
    """
    Returns a pending reactive engine decision if one is available.
    Single Responsibility: reactive engine integration only.
    """

    def __init__(self, reactive_engine: Any) -> None:
        self._engine = reactive_engine
        self._pending: CommandDecision | None = None

    def register_output(
        self,
        output: str,
        command: str,
        platform: str = "linux",
    ) -> None:
        """Feed reactive engine with last command output to generate new decisions."""
        _d = _daemon()
        log = _d.log
        if self._engine is None:
            return
        try:
            decisions = self._engine.analyse(
                output=output,
                command=command,
                platform=platform,
            )
            if decisions:
                top = decisions[0]
                if top.priority <= 2:
                    self._pending = CommandDecision(
                        command=top.command,
                        source="reactive",
                        reason=top.reason,
                        priority=top.priority,
                    )
        except Exception as exc:
            log.debug("reactive engine error: %s", exc)

    def select(self, target: str, phase: str, context: dict) -> CommandDecision | None:
        """Pop and return the pending reactive decision if present."""
        if self._pending:
            dec = self._pending
            self._pending = None
            return dec
        return None


class LLMSelector(ICommandSelector):
    """
    Queries Groq/Ollama for a command suggestion.
    Only active when AUTO_USE_LLM=1.
    Single Responsibility: LLM command recommendation only.
    """

    def select(self, target: str, phase: str, context: dict) -> CommandDecision | None:
        """Return an LLM-suggested command with catalog context, or None if disabled."""
        if os.environ.get("AUTO_USE_LLM", "0") != "1":
            return None
        return self._llm_candidate(target, phase, context)

    def _llm_candidate(self, target: str, phase: str, context: dict) -> CommandDecision | None:
        _d = _daemon()
        SESSIONS_DIR, _emit, _get_phase_command_catalog, _load_payload, _read_recent_csv_commands, log = (
            _d.SESSIONS_DIR,
            _d._emit,
            _d._get_phase_command_catalog,
            _d._load_payload,
            _d._read_recent_csv_commands,
            _d.log,
        )
        try:
            from lazyown_llm import LLMBridge

            payload = _load_payload()
            api_key = payload.get("api_key", "") or os.environ.get("GROQ_API_KEY", "")
            if not api_key:
                return None
            catalog = _get_phase_command_catalog(phase)
            services = context.get("services", [])
            os_hint = context.get("os_hint", "unknown")
            has_creds = bool(payload.get("start_pass") or payload.get("start_user"))

            # Recent session history for context
            recent_cmds = _read_recent_csv_commands(limit=3)
            recent_line = f"Recently executed: {', '.join(recent_cmds)}\n" if recent_cmds else ""

            # World model context
            wm_line = ""
            wm_file = SESSIONS_DIR / "world_model.json"
            if wm_file.exists():
                try:
                    from modules.world_model import read_state_dict

                    wm = read_state_dict(wm_file)
                    wm_hosts = list(wm.get("hosts", {}).keys())[:3]
                    wm_creds = len(wm.get("credentials", []))
                    wm_vulns = len(wm.get("vulnerabilities", []))
                    wm_line = f"World model: known_hosts={wm_hosts} creds={wm_creds} vulns={wm_vulns}\n"
                except Exception:
                    pass

            catalog_line = f"Available LazyOwn commands for phase '{phase}': {catalog}\n" if catalog else ""
            goal = (
                f"{catalog_line}"
                f"CRITICAL: These are HIGH-LEVEL ABSTRACTIONS. payload.json auto-injects rhost/domain/creds/wordlist. "
                f"Never write raw tool flags — just the command name.\n"
                f"Target: {target} | OS: {os_hint} | Services: {services[:5]} | Has-creds: {has_creds}\n"
                f"{recent_line}"
                f"{wm_line}"
                f"Suggest the BEST SINGLE command for phase='{phase}' that has NOT been recently executed. "
                f"Reply with ONLY the command name (one word). No explanation."
            )
            answer = None
            _pool_exhausted_cls: type | None = None
            try:
                from modules.llm_pool import PoolExhausted as _PoolExhausted

                _pool_exhausted_cls = _PoolExhausted
            except Exception:
                pass
            try:
                from modules.llm_pool import LLMPool as _LLMPool
                from modules.llm_pool import PoolMember as _PoolMember
                from modules.llm_pool import shared_registry as _shared_registry

                def _ask_via(_backend: str, _goal: str = goal, _key: str = api_key) -> str:
                    return LLMBridge(backend=_backend, api_key=_key).ask(goal=_goal, max_iterations=1)

                _pool = _LLMPool(
                    [
                        _PoolMember("groq", "groq", "groq", rank=10, complete=lambda p: _ask_via("groq")),
                        _PoolMember("ollama", "ollama", "ollama", rank=1, complete=lambda p: _ask_via("ollama")),
                    ],
                    health=_shared_registry(),
                )
                answer = _pool.complete(goal)
            except Exception as _pool_exc:
                if _pool_exhausted_cls is not None and isinstance(_pool_exc, _pool_exhausted_cls):
                    _emit(
                        "LLM_POOL_EXHAUSTED",
                        {"target": target, "phase": phase, "detail": str(_pool_exc)[:200]},
                        severity="warning",
                    )
                answer = LLMBridge(backend="groq", api_key=api_key).ask(goal=goal, max_iterations=1)
            cmd = answer.strip().split()[0] if answer and answer.strip() else None
            if cmd and len(cmd) < 50:
                return CommandDecision(
                    command=cmd,
                    source="llm",
                    reason=f"LLM recommendation (catalog={bool(catalog)})",
                    priority=4,
                )
        except Exception as exc:
            log.debug("LLM candidate error: %s", exc)
        return None


class SWANSelector(ICommandSelector):
    """
    SWAN (Scalable Weighted Adaptive Network) command selector.

    Routes the command-recommendation query to the best MoE expert via
    Q-learning-guided routing.  Only active when AUTO_USE_SWAN=1.

    Single Responsibility : MoE/RL expert routing only — no direct execution.
    Open/Closed           : Extend SwanOrchestrator subclasses; this selector
                            never changes to support new experts.
    Dependency Inversion  : depends on ICommandSelector interface; imports
                            swan_agent lazily so the daemon starts even without
                            GROQ_API_KEY present.
    """

    # Mapping from LazyOwn daemon phase names → SWAN task_type strings
    _PHASE_TO_TASK: dict[str, str] = {
        "recon": "recon",
        "enum": "recon",
        "exploit": "exploit",
        "postexp": "privesc",
        "post_exploit": "privesc",
        "cred": "cred",
        "lateral": "lateral",
        "privesc": "privesc",
        "persist": "lateral",
        "exfil": "cred",
        "c2": "analyze",
        "report": "analyze",
    }

    def select(self, target: str, phase: str, context: dict) -> CommandDecision | None:
        """Ask the best MoE expert for a command recommendation. Returns None if disabled."""
        if os.environ.get("AUTO_USE_SWAN", "0") != "1":
            return None
        return self._swan_candidate(target, phase, context)

    def _swan_candidate(self, target: str, phase: str, context: dict) -> CommandDecision | None:
        _d = _daemon()
        _get_phase_command_catalog, log = _d._get_phase_command_catalog, _d.log
        try:
            from swan_agent import mcp_swan_run as _swan_run  # lazy import

            services = context.get("services", [])
            os_hint = context.get("os_hint", "unknown")
            task_type = self._PHASE_TO_TASK.get(phase, "analyze")
            catalog = _get_phase_command_catalog(phase)
            catalog_line = f"Available LazyOwn commands for phase '{phase}': {catalog}\n" if catalog else ""
            goal = (
                f"{catalog_line}"
                f"IMPORTANT: These are HIGH-LEVEL ABSTRACTIONS — payload.json auto-injects all parameters. "
                f"Reply with ONLY the command name.\n"
                f"Suggest the best command for phase='{phase}' target='{target}' "
                f"os={os_hint} services={services[:5]}."
            )
            raw = _swan_run(task_type, goal, phase=phase)
            data = json.loads(raw)
            output = data.get("output", "").strip()
            # Extract first word (command name) from the expert output
            cmd = output.split()[0] if output.split() else None
            if cmd and len(cmd) < 50 and "\n" not in cmd:
                return CommandDecision(
                    command=cmd,
                    source="swan",
                    reason=(f"SWAN expert={data.get('expert_id', '?')} detect={data.get('detection_pct', 0):.0f}%"),
                    priority=3,
                )
        except Exception as exc:
            log.debug("SWANSelector error: %s", exc)
        return None


class FallbackSelector(ICommandSelector):
    """
    Static map fallback — always returns a CommandDecision, never None.
    Selects OS-appropriate commands when the OS is known.
    Single Responsibility: static fallback map only.
    """

    def select(self, target: str, phase: str, context: dict) -> CommandDecision | None:
        """Return the static fallback command for this phase. Never returns None."""
        _d = _daemon()
        _FALLBACK_MAP, _FALLBACK_MAP_LINUX, _FALLBACK_MAP_WINDOWS, _PHASE_CATEGORIES = (
            _d._FALLBACK_MAP,
            _d._FALLBACK_MAP_LINUX,
            _d._FALLBACK_MAP_WINDOWS,
            _d._PHASE_CATEGORIES,
        )
        categories = _PHASE_CATEGORIES.get(phase, ["other"])
        category = categories[0]
        os_hint = context.get("os_hint", "unknown")

        os_map = _FALLBACK_MAP_WINDOWS if os_hint == "windows" else _FALLBACK_MAP_LINUX if os_hint == "linux" else {}
        cmd = os_map.get(category) or _FALLBACK_MAP.get(category, "list")

        return CommandDecision(
            command=cmd,
            source="fallback",
            reason=f"static map for {category} (os={os_hint})",
        )


class MetricsAwareSelector(ICommandSelector):
    """Decorator that demotes commands with a poor recent track record.

    Wraps another :class:`ICommandSelector`. When the wrapped selector
    proposes a command whose recent ``success_rate`` in
    :class:`modules.metrics.MetricsRecorder` is below the configured
    threshold and whose attempt count clears
    :data:`METRICS_BIAS_MIN_ATTEMPTS`, the decision is dropped (returns
    ``None``) so the cascade falls through to the next selector. The
    rejection itself is logged at debug level and broadcast as a
    ``METRICS_BIAS_SKIP`` event so operators can audit why the daemon
    sidestepped an otherwise valid recommendation.

    The fallback selector is intentionally left unwrapped at chain
    composition time: when every other selector has been filtered, the
    cascade must still converge on *something*.
    """

    _SUMMARY_KEY: str = "by_command"
    _SKIP_EVENT_TYPE: str = "METRICS_BIAS_SKIP"

    def __init__(
        self,
        wrapped: ICommandSelector,
        metrics_source: Any = None,
        min_success_rate: float | None = None,
        min_attempts: int | None = None,
        window_seconds: int | None = None,
        cache_ttl_s: float | None = None,
        clock: Any | None = None,
    ) -> None:
        """Initialise the decorator.

        Args:
            wrapped: The selector whose decisions may be filtered.
            metrics_source: Object exposing ``summarize(window_seconds)``.
                Defaults to :func:`modules.metrics.get_recorder` resolved
                lazily on first use so the module remains importable
                without the metrics package present.
            min_success_rate: Inclusive lower bound on ``success_rate``;
                values strictly below this are considered failing.
            min_attempts: Minimum number of recorded attempts before a
                command can be filtered. Avoids over-reacting to a
                single failure.
            window_seconds: Aggregation window forwarded to
                ``summarize``. Set to ``0`` or a negative value to
                aggregate the whole log.
            cache_ttl_s: Time-to-live for the in-memory summary cache.
                Repeated calls within the TTL reuse the cached
                aggregate to avoid re-reading the JSONL log every
                step.
            clock: Callable returning the current monotonic time.
                Injected in tests; defaults to :func:`time.monotonic`.
        """
        _d = _daemon()
        if min_success_rate is None:
            min_success_rate = _d.METRICS_BIAS_MIN_SUCCESS
        if min_attempts is None:
            min_attempts = _d.METRICS_BIAS_MIN_ATTEMPTS
        if window_seconds is None:
            window_seconds = _d.METRICS_BIAS_WINDOW_S
        if cache_ttl_s is None:
            cache_ttl_s = _d.METRICS_BIAS_CACHE_TTL_S

        self._wrapped = wrapped
        self._metrics_source = metrics_source
        self._metrics_source_loaded = metrics_source is not None
        self._min_success_rate = float(min_success_rate)
        self._min_attempts = int(min_attempts)
        self._window_seconds = int(window_seconds) if int(window_seconds) > 0 else None
        self._cache_ttl_s = float(cache_ttl_s)
        self._clock = clock or time.monotonic
        self._cached_summary: dict[str, Any] = {}
        self._cache_stamp: float = -1.0

    @property
    def wrapped(self) -> ICommandSelector:
        """Return the underlying selector for introspection in tests."""

        return self._wrapped

    def _resolve_source(self) -> Any | None:
        """Return the metrics source, resolving the singleton on first use.

        Returns:
            The configured metrics source, or ``None`` when the metrics
            module cannot be imported (the decorator then degrades to a
            transparent pass-through).
        """
        _d = _daemon()
        log = _d.log

        if self._metrics_source_loaded:
            return self._metrics_source
        self._metrics_source_loaded = True
        try:
            from metrics import get_recorder
        except ImportError:
            try:
                from modules.metrics import get_recorder
            except ImportError as exc:
                log.debug("MetricsAwareSelector: metrics unavailable: %s", exc)
                return None
        try:
            self._metrics_source = get_recorder()
        except Exception as exc:
            log.debug("MetricsAwareSelector: get_recorder failed: %s", exc)
            self._metrics_source = None
        return self._metrics_source

    def _current_summary(self) -> dict[str, Any]:
        """Return a fresh or cached summary dictionary.

        Returns:
            The ``by_command`` section of the summary, or an empty dict
            when no metrics source is available.
        """
        _d = _daemon()
        log = _d.log

        now = float(self._clock())
        if self._cached_summary and self._cache_stamp >= 0 and now - self._cache_stamp < self._cache_ttl_s:
            return self._cached_summary
        source = self._resolve_source()
        if source is None:
            self._cached_summary = {}
            self._cache_stamp = now
            return self._cached_summary
        try:
            summary = source.summarize(window_seconds=self._window_seconds)
        except Exception as exc:
            log.debug("MetricsAwareSelector: summarize failed: %s", exc)
            self._cached_summary = {}
            self._cache_stamp = now
            return self._cached_summary
        by_command = summary.get(self._SUMMARY_KEY)
        if not isinstance(by_command, dict):
            by_command = {}
        self._cached_summary = by_command
        self._cache_stamp = now
        return self._cached_summary

    def _should_skip(self, command: str) -> tuple[bool, dict[str, Any] | None]:
        """Decide whether *command* should be filtered out.

        Args:
            command: First token of the proposed command.

        Returns:
            ``(skip, stats)`` — ``skip`` is ``True`` when the command
            should be filtered; ``stats`` carries the underlying
            count and success rate when available, for telemetry.
        """

        by_command = self._current_summary()
        stats = by_command.get(command) if isinstance(by_command, dict) else None
        if not isinstance(stats, dict):
            return False, None
        count = int(stats.get("count", 0) or 0)
        if count < self._min_attempts:
            return False, stats
        success_rate = float(stats.get("success_rate", 0.0) or 0.0)
        if success_rate >= self._min_success_rate:
            return False, stats
        return True, stats

    def select(
        self,
        target: str,
        phase: str,
        context: dict,
    ) -> CommandDecision | None:
        """Honour the :class:`ICommandSelector` contract.

        Delegates to the wrapped selector. When the proposed command
        fails the success-rate gate, returns ``None`` and emits a
        ``METRICS_BIAS_SKIP`` event so the rejection is auditable.
        """
        _d = _daemon()
        _daemon_tool, _emit, log = _d._daemon_tool, _d._emit, _d.log

        decision = self._wrapped.select(target, phase, context)
        if decision is None or not decision.command:
            return decision
        command_token = _daemon_tool(decision.command)
        skip, stats = self._should_skip(command_token)
        if not skip:
            return decision
        try:
            _emit(
                self._SKIP_EVENT_TYPE,
                {
                    "wrapped": self._wrapped.__class__.__name__,
                    "command": decision.command,
                    "phase": phase,
                    "target": target,
                    "reason": decision.reason,
                    "stats": stats or {},
                    "min_success": self._min_success_rate,
                    "min_attempts": self._min_attempts,
                    "window_s": self._window_seconds,
                },
            )
        except Exception as exc:
            log.debug("MetricsAwareSelector emit failed: %s", exc)
        return None


class UnifiedBrainSelector(ICommandSelector):
    """Daemon adapter over the one shared selector cascade.

    Routes the daemon through ``modules.selection.registry.propose_next`` so it
    consults the exact same action brain as the LazyLoopEngine planner: chains,
    credential reuse, APT playbooks, adversary profiles and MITRE/atomic
    techniques, all orchestrator-administered. Replaces the daemon's separate
    chain, credential-spray and bridge selectors (now subsumed). Per-run dedupe
    is carried as the shared exclude set so a command is proposed at most once,
    and the daemon's burned-verb counts are passed as the shared burned set so
    history- and catalogue-driven selectors skip verbs that keep failing.
    """

    name = "unified_brain"

    def __init__(self, fail_counts: dict[str, int] | None = None) -> None:
        self._proposed: set[str] = set()
        self._fail_counts = fail_counts if fail_counts is not None else {}

    def select(self, target: str, phase: str, context: dict) -> CommandDecision | None:
        """Build a SelectionContext and return the cascade's first decision."""
        _d = _daemon()
        MAX_FAILS_PER_CMD, _load_payload = _d.MAX_FAILS_PER_CMD, _d._load_payload
        if not target:
            return None
        try:
            from modules.selection.base import SelectionContext
            from modules.selection.registry import propose_next
        except Exception:
            return None
        payload = _load_payload()
        has_creds = bool(
            str(payload.get("start_user", "") or "").strip()
            and str(payload.get("start_pass", "") or payload.get("hash", "") or "").strip()
        )
        burned = frozenset(verb for verb, count in self._fail_counts.items() if count >= MAX_FAILS_PER_CMD)
        ctx = SelectionContext(
            target=target,
            phase=phase,
            os_hint=str(context.get("os_hint", "") or ""),
            services=tuple(context.get("services", []) or ()),
            has_creds=has_creds,
            exclude=frozenset(self._proposed),
            burned=burned,
            extra={"goal": str(context.get("goal", "") or "")},
        )
        decision = propose_next(ctx)
        if decision is None or not decision.command.strip():
            return None
        self._proposed.add(decision.command)
        return CommandDecision(
            command=decision.command,
            source=decision.source,
            reason=decision.reason,
            priority=decision.priority,
        )
