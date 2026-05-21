"""Unified orchestrator facade collapsing daemon, hive and SWAN into one surface.

The framework historically exposes three independent autonomous heads:

* :class:`skills.autonomous_daemon.EngageOrchestrator` — single-target
  kill-chain executor.
* :class:`skills.hive_mind.QueenBrain` — drone swarm coordinator.
* :class:`skills.swan_agent.SwanOrchestrator` — MoE+RL expert ensemble.

Each ships its own input shape, result shape, event format and lifecycle.
That overlap forces the operator (and the LLM) to know which head to use
before they can ask a question. This module re-frames them as
interchangeable :class:`IOrchestratorBackend` implementations behind a
single :class:`UnifiedOrchestrator` entry point that:

1. Normalises the input into an :class:`OrchestratorGoal`.
2. Picks a backend via :class:`RouterPolicy`.
3. Executes through the backend's lazily-imported real engine.
4. Normalises the output into :class:`OrchestratorResult`.
5. Emits a structured record onto the shared event bus.

The originals are untouched — this is a façade in the Gang-of-Four sense,
not a rewrite. New code calls this module; the legacy entry points keep
working until they are deprecated.
"""

from __future__ import annotations

import errno
import json
import os
import tempfile
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Any, Callable, Mapping, Optional, Protocol, Sequence


_BACKEND_DAEMON = "daemon"
_BACKEND_HIVE = "hive"
_BACKEND_SWAN = "swan"
_MODE_AUTO = "auto"

_STATUS_OK = "ok"
_STATUS_ERROR = "error"
_STATUS_UNAVAILABLE = "unavailable"
_STATUS_INVALID = "invalid"


@dataclass(frozen=True)
class OrchestratorConfig:
    """Configuration container for :class:`UnifiedOrchestrator`.

    Every tunable lives here so the orchestrator can be reconfigured from
    ``payload.json`` without code edits.
    """

    sessions_dir: str = "sessions"
    events_filename: str = "autonomous_events.jsonl"
    default_mode: str = _MODE_AUTO
    default_phase: str = "exploitation"
    default_task_type: str = "exploit_generation"
    default_drones: int = 4
    daemon_default_max_switches: int = 3
    swan_default_timeout: float = 300.0
    hive_default_max_iterations: int = 10
    max_goal_chars: int = 4096
    max_event_bytes: int = 65536
    file_mode: int = 0o600
    bus_filename_encoding: str = "utf-8"
    enabled_modes: tuple[str, ...] = (
        _MODE_AUTO,
        _BACKEND_DAEMON,
        _BACKEND_HIVE,
        _BACKEND_SWAN,
    )
    hive_role_keywords: tuple[str, ...] = (
        "swarm",
        "parallel",
        "many",
        "multiple",
        "drones",
        "team",
        "concurrent",
    )
    swan_task_keywords: tuple[str, ...] = (
        "exploit",
        "shell",
        "rce",
        "payload",
        "lateral",
        "escalat",
    )
    swan_phase_keywords: tuple[str, ...] = (
        "exploit",
        "postexp",
        "lateral",
    )
    daemon_target_keys: tuple[str, ...] = ("target", "rhost", "host")
    autonomous_event_kind: str = "orchestrator"
    daemon_target_score: int = 7
    hive_drones_bonus: int = 10
    hive_drones_threshold: int = 1
    swan_phase_bonus: int = 5
    swan_keyword_weight: int = 3
    invalid_modes_message: str = "mode must be one of: auto, daemon, hive, swan"
    empty_goal_message: str = "goal must be a non-empty string"
    backend_missing_message: str = "no backend available for the requested mode"

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any] | None) -> "OrchestratorConfig":
        """Return a config with ``payload.json`` overrides applied.

        Args:
            payload: Loaded payload mapping. ``None`` returns the defaults.

        Returns:
            A new :class:`OrchestratorConfig` instance.
        """
        if not payload:
            return cls()
        base = cls()
        updates: dict[str, Any] = {}
        sessions = payload.get("sessions_dir")
        if isinstance(sessions, str) and sessions.strip():
            updates["sessions_dir"] = sessions.strip()
        events_name = payload.get("orchestrator_events_filename")
        if isinstance(events_name, str) and events_name.strip():
            updates["events_filename"] = events_name.strip()
        mode = payload.get("orchestrator_default_mode")
        if isinstance(mode, str) and mode.strip() in base.enabled_modes:
            updates["default_mode"] = mode.strip()
        drones = payload.get("orchestrator_default_drones")
        if isinstance(drones, int) and drones > 0:
            updates["default_drones"] = drones
        timeout = payload.get("orchestrator_swan_timeout")
        if isinstance(timeout, (int, float)) and timeout > 0:
            updates["swan_default_timeout"] = float(timeout)
        return replace(base, **updates) if updates else base


@dataclass(frozen=True)
class OrchestratorGoal:
    """Validated request shape consumed by every backend."""

    goal: str
    mode: str
    phase: str
    task_type: str
    target: str = ""
    drones: int = 0
    timeout: float = 0.0
    api_key: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def with_defaults(self, config: OrchestratorConfig) -> "OrchestratorGoal":
        """Return a copy with empty fields populated from ``config``.

        Only fields whose absence is unambiguous are populated here.
        ``task_type`` is intentionally left blank when the caller did
        not specify one so the router scores routing purely on the goal
        text; SWAN's backend defaults the task type internally. The
        numeric fields ``drones`` and ``timeout`` are likewise left at
        zero so backends can apply their own defaults.
        """
        return replace(
            self,
            mode=self.mode or config.default_mode,
            phase=self.phase or config.default_phase,
        )


@dataclass(frozen=True)
class OrchestratorResult:
    """Canonical result shape returned by :class:`UnifiedOrchestrator`.

    Attributes:
        request_id: Stable id for correlating events with this run.
        backend: Identifier of the backend that handled the request.
        status: One of ``ok``, ``error``, ``unavailable``, ``invalid``.
        summary: Short single-line human-readable description.
        artefacts: Mapping of optional output paths or identifiers.
        events: Structured event entries emitted during the run.
        duration: Wall-clock seconds spent in :meth:`IOrchestratorBackend.run`.
        raw: Backend-native payload (kept opaque to callers).
    """

    request_id: str
    backend: str
    status: str
    summary: str
    artefacts: Mapping[str, Any] = field(default_factory=dict)
    events: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    duration: float = 0.0
    raw: Any = None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable dictionary of the result."""
        return {
            "request_id": self.request_id,
            "backend": self.backend,
            "status": self.status,
            "summary": self.summary,
            "artefacts": dict(self.artefacts),
            "events": [dict(e) for e in self.events],
            "duration": self.duration,
        }


class IOrchestratorBackend(Protocol):
    """Backend contract. Implementations must be side-effect-free on import."""

    name: str

    def available(self) -> bool:
        """Return ``True`` when this backend can satisfy a request."""
        ...

    def run(self, goal: OrchestratorGoal) -> OrchestratorResult:
        """Execute ``goal`` and return a normalised :class:`OrchestratorResult`."""
        ...


class EventBus:
    """Atomic append-only writer for orchestrator events.

    The bus appends one JSON line per event to
    ``sessions/<events_filename>``. Writes are serialised with a process-
    level lock and use ``O_APPEND`` to avoid interleaving when multiple
    orchestrators share the same file.
    """

    def __init__(self, config: OrchestratorConfig, root: Path | None = None) -> None:
        """Bind the bus to the active config.

        Args:
            config: Active orchestrator configuration.
            root: Optional explicit sessions directory. Resolved against
                the current working directory.

        Raises:
            ValueError: When ``config.max_event_bytes`` is non-positive.
        """
        if config.max_event_bytes <= 0:
            raise ValueError("max_event_bytes must be positive")
        self._config = config
        base = Path(root) if root is not None else Path(config.sessions_dir)
        self._root = base.resolve()
        self._lock = threading.Lock()

    @property
    def path(self) -> Path:
        """Return the resolved event file path."""
        return self._root / self._config.events_filename

    def emit(self, event: Mapping[str, Any]) -> bool:
        """Append a single sanitised event to the bus.

        Args:
            event: Event mapping. Must serialise to a JSON object whose
                encoded form fits within ``config.max_event_bytes``.

        Returns:
            ``True`` when the event was persisted, ``False`` when the
            event was rejected (oversize, unserialisable) or the write
            failed.
        """
        try:
            encoded = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
        except (TypeError, ValueError):
            return False
        if len(encoded.encode(self._config.bus_filename_encoding)) > self._config.max_event_bytes:
            return False
        try:
            self._root.mkdir(parents=True, exist_ok=True)
        except OSError:
            return False
        with self._lock:
            try:
                fd = os.open(
                    str(self.path),
                    os.O_WRONLY | os.O_CREAT | os.O_APPEND,
                    self._config.file_mode,
                )
            except OSError:
                return False
            try:
                payload = (encoded + "\n").encode(self._config.bus_filename_encoding)
                os.write(fd, payload)
            except OSError:
                return False
            finally:
                try:
                    os.close(fd)
                except OSError:
                    pass
        return True


class BackendRegistry:
    """Ordered registry of :class:`IOrchestratorBackend` implementations."""

    def __init__(self, backends: Sequence[IOrchestratorBackend]) -> None:
        """Bind the registry to a fixed-order tuple of backends.

        Args:
            backends: Sequence of backends. Order is preserved so the
                router can iterate by priority.

        Raises:
            ValueError: When two backends share a name.
        """
        names: list[str] = []
        unique: dict[str, IOrchestratorBackend] = {}
        for backend in backends:
            name = getattr(backend, "name", "")
            if not isinstance(name, str) or not name.strip():
                raise ValueError("backend name must be a non-empty string")
            if name in unique:
                raise ValueError(f"duplicate backend name: {name}")
            unique[name] = backend
            names.append(name)
        self._order: tuple[str, ...] = tuple(names)
        self._by_name: dict[str, IOrchestratorBackend] = unique

    @property
    def names(self) -> tuple[str, ...]:
        """Return the registered backend names in declaration order."""
        return self._order

    def get(self, name: str) -> Optional[IOrchestratorBackend]:
        """Return the backend registered as ``name`` or ``None``."""
        return self._by_name.get(name)

    def available(self) -> list[IOrchestratorBackend]:
        """Return every backend that currently reports availability."""
        return [self._by_name[n] for n in self._order if self._by_name[n].available()]


class RouterPolicy:
    """Pick the best backend for a given :class:`OrchestratorGoal`.

    The policy is deliberately small and explicit so the operator can
    predict routing decisions without reading the source.
    """

    def __init__(self, config: OrchestratorConfig, registry: BackendRegistry) -> None:
        """Bind the policy to config and backend registry."""
        self._config = config
        self._registry = registry

    def choose(self, goal: OrchestratorGoal) -> Optional[IOrchestratorBackend]:
        """Return the backend that should execute ``goal``."""
        if goal.mode != _MODE_AUTO:
            backend = self._registry.get(goal.mode)
            if backend is not None and backend.available():
                return backend
            return None
        scored: list[tuple[int, IOrchestratorBackend]] = []
        for backend in self._registry.available():
            scored.append((self._score(goal, backend), backend))
        if not scored:
            return None
        scored.sort(key=lambda item: item[0], reverse=True)
        return scored[0][1]

    def _score(self, goal: OrchestratorGoal, backend: IOrchestratorBackend) -> int:
        name = backend.name
        text_parts: list[str] = [goal.goal]
        if goal.task_type:
            text_parts.append(goal.task_type)
        text = " ".join(text_parts).lower()
        if name == _BACKEND_HIVE:
            keyword = self._keyword_score(text, self._config.hive_role_keywords)
            drones_bonus = (
                self._config.hive_drones_bonus
                if goal.drones and goal.drones > self._config.hive_drones_threshold
                else 0
            )
            return keyword + drones_bonus
        if name == _BACKEND_SWAN:
            keyword = self._keyword_score(text, self._config.swan_task_keywords)
            phase_lower = goal.phase.lower() if goal.phase else ""
            phase_bonus = (
                self._config.swan_phase_bonus
                if phase_lower and any(kw in phase_lower for kw in self._config.swan_phase_keywords)
                else 0
            )
            return keyword * self._config.swan_keyword_weight + phase_bonus
        if name == _BACKEND_DAEMON:
            target = goal.target
            resolver = getattr(backend, "effective_target", None)
            if not target and callable(resolver):
                try:
                    target = resolver(goal)
                except Exception:
                    target = ""
            if not target:
                return 0
            return self._config.daemon_target_score
        return 0

    @staticmethod
    def _keyword_score(text: str, keywords: Sequence[str]) -> int:
        return sum(1 for kw in keywords if kw in text)


class DaemonBackend:
    """Adapter onto :class:`skills.autonomous_daemon.EngageOrchestrator`."""

    name = _BACKEND_DAEMON

    def __init__(
        self,
        config: OrchestratorConfig,
        factory: Optional[Callable[[OrchestratorGoal], Any]] = None,
        payload: Mapping[str, Any] | None = None,
    ) -> None:
        """Bind to config, optional engine factory and payload mapping.

        Args:
            config: Active configuration.
            factory: Optional callable that returns an object exposing
                ``run() -> dict``. Injected for tests; in production the
                adapter constructs the real ``EngageOrchestrator``
                lazily.
            payload: Optional ``payload.json`` mapping used to derive a
                fallback target (``active_target`` / ``rhost`` / ``host``)
                when the goal does not carry one explicitly.
        """
        self._config = config
        self._factory = factory
        self._payload = payload or {}

    def available(self) -> bool:
        """Return ``True`` when the underlying engine can be imported."""
        if self._factory is not None:
            return True
        try:
            self._import_class()
            return True
        except Exception:
            return False

    def run(self, goal: OrchestratorGoal) -> OrchestratorResult:
        """Execute a single-target kill-chain engagement.

        Args:
            goal: The validated request shape.

        Returns:
            A normalised :class:`OrchestratorResult`. ``status`` reflects
            backend-side failures without raising.
        """
        target = self.effective_target(goal)
        if not target:
            return _make_result(
                request_id=goal.metadata.get("request_id", _new_request_id()),
                backend=self.name,
                status=_STATUS_INVALID,
                summary="daemon backend requires a non-empty target",
            )
        request_id = goal.metadata.get("request_id", _new_request_id())
        start = time.monotonic()
        try:
            engine = self._build(goal, target)
            raw = engine.run()
        except Exception as exc:
            return _make_result(
                request_id=request_id,
                backend=self.name,
                status=_STATUS_ERROR,
                summary=f"daemon failed: {exc}",
                duration=time.monotonic() - start,
            )
        duration = time.monotonic() - start
        summary = self._summarise(raw, target)
        artefacts = self._artefacts(raw)
        return _make_result(
            request_id=request_id,
            backend=self.name,
            status=_STATUS_OK,
            summary=summary,
            artefacts=artefacts,
            duration=duration,
            raw=raw,
        )

    def effective_target(self, goal: OrchestratorGoal) -> str:
        """Return the daemon target this backend would use for ``goal``.

        Resolution order:
            1. ``goal.target`` when set.
            2. ``goal.metadata[<daemon_target_keys>]``.
            3. ``payload[<daemon_target_keys>]``.
        Returns an empty string when no candidate is available.
        """
        if goal.target:
            return goal.target
        return self._target_from_metadata(goal)

    def _target_from_metadata(self, goal: OrchestratorGoal) -> str:
        for key in self._config.daemon_target_keys:
            value = goal.metadata.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        for key in self._config.daemon_target_keys:
            value = self._payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return ""

    def _build(self, goal: OrchestratorGoal, target: str) -> Any:
        if self._factory is not None:
            return self._factory(replace(goal, target=target))
        EngageOrchestrator = self._import_class()
        return EngageOrchestrator(
            target=target,
            max_switches_per_step=self._config.daemon_default_max_switches,
        )

    @staticmethod
    def _import_class() -> Any:
        from skills.autonomous_daemon import EngageOrchestrator  # noqa: PLC0415
        return EngageOrchestrator

    @staticmethod
    def _summarise(raw: Any, target: str) -> str:
        if isinstance(raw, dict):
            flag = raw.get("flag") or raw.get("status") or raw.get("engagement_id")
            if flag:
                return f"daemon engaged {target}: {flag}"
        return f"daemon engaged {target}"

    @staticmethod
    def _artefacts(raw: Any) -> dict[str, Any]:
        if isinstance(raw, dict):
            return {k: v for k, v in raw.items() if isinstance(k, str)}
        return {}


class HiveBackend:
    """Adapter onto :class:`skills.hive_mind.QueenBrain`."""

    name = _BACKEND_HIVE

    def __init__(
        self,
        config: OrchestratorConfig,
        factory: Optional[Callable[[], Any]] = None,
    ) -> None:
        """Bind to config and an optional queen factory."""
        self._config = config
        self._factory = factory

    def available(self) -> bool:
        """Return ``True`` when the hive engine is importable."""
        if self._factory is not None:
            return True
        try:
            self._import_factory()
            return True
        except Exception:
            return False

    def run(self, goal: OrchestratorGoal) -> OrchestratorResult:
        """Plan, dispatch, collect and synthesise via the hive."""
        request_id = goal.metadata.get("request_id", _new_request_id())
        start = time.monotonic()
        try:
            queen = self._build()
        except Exception as exc:
            return _make_result(
                request_id=request_id,
                backend=self.name,
                status=_STATUS_UNAVAILABLE,
                summary=f"hive unavailable: {exc}",
                duration=time.monotonic() - start,
            )
        try:
            effective_drones = goal.drones if goal.drones > 0 else self._config.default_drones
            tasks = queen.plan(goal.goal, n_drones=max(1, effective_drones))
            drone_ids = queen.dispatch(
                tasks,
                api_key=goal.api_key or None,
                max_iterations=self._config.hive_default_max_iterations,
            )
            results = queen.collect(drone_ids)
            synthesis = queen.synthesize(results) if hasattr(queen, "synthesize") else results
        except Exception as exc:
            return _make_result(
                request_id=request_id,
                backend=self.name,
                status=_STATUS_ERROR,
                summary=f"hive run failed: {exc}",
                duration=time.monotonic() - start,
            )
        duration = time.monotonic() - start
        summary = self._summarise(tasks, synthesis)
        artefacts = {
            "drone_ids": list(drone_ids) if drone_ids else [],
            "task_count": len(tasks),
        }
        return _make_result(
            request_id=request_id,
            backend=self.name,
            status=_STATUS_OK,
            summary=summary,
            artefacts=artefacts,
            duration=duration,
            raw=synthesis,
        )

    def _build(self) -> Any:
        if self._factory is not None:
            return self._factory()
        build_default_hive_memory, HiveBus, DronePool, QueenBrain = self._import_factory()
        memory = build_default_hive_memory()
        bus = HiveBus()
        pool = DronePool(memory=memory, bus=bus)
        return QueenBrain(memory=memory, bus=bus, pool=pool)

    @staticmethod
    def _import_factory() -> tuple[Any, Any, Any, Any]:
        from skills.hive_mind import (  # noqa: PLC0415
            DronePool,
            HiveBus,
            QueenBrain,
            build_default_hive_memory,
        )
        return build_default_hive_memory, HiveBus, DronePool, QueenBrain

    @staticmethod
    def _summarise(tasks: Sequence[Any], synthesis: Any) -> str:
        count = len(tasks) if tasks is not None else 0
        if isinstance(synthesis, str) and synthesis.strip():
            head = synthesis.strip().splitlines()[0][:120]
            return f"hive dispatched {count} drones: {head}"
        return f"hive dispatched {count} drones"


class SwanBackend:
    """Adapter onto :class:`skills.swan_agent.SwanOrchestrator`."""

    name = _BACKEND_SWAN

    def __init__(
        self,
        config: OrchestratorConfig,
        factory: Optional[Callable[[str], Any]] = None,
    ) -> None:
        """Bind to config and an optional orchestrator factory."""
        self._config = config
        self._factory = factory

    def available(self) -> bool:
        """Return ``True`` when the SWAN engine is importable."""
        if self._factory is not None:
            return True
        try:
            self._import_factory()
            return True
        except Exception:
            return False

    def run(self, goal: OrchestratorGoal) -> OrchestratorResult:
        """Execute a single SWAN task and normalise the result."""
        request_id = goal.metadata.get("request_id", _new_request_id())
        start = time.monotonic()
        try:
            orchestrator = self._build(goal.api_key)
        except Exception as exc:
            return _make_result(
                request_id=request_id,
                backend=self.name,
                status=_STATUS_UNAVAILABLE,
                summary=f"swan unavailable: {exc}",
                duration=time.monotonic() - start,
            )
        effective_timeout = goal.timeout if goal.timeout > 0 else self._config.swan_default_timeout
        effective_task_type = goal.task_type or self._config.default_task_type
        try:
            swan_result = orchestrator.run(
                task_type=effective_task_type,
                goal=goal.goal,
                engagement_phase=goal.phase,
                timeout=effective_timeout,
            )
        except Exception as exc:
            return _make_result(
                request_id=request_id,
                backend=self.name,
                status=_STATUS_ERROR,
                summary=f"swan run failed: {exc}",
                duration=time.monotonic() - start,
            )
        duration = time.monotonic() - start
        return _make_result(
            request_id=request_id,
            backend=self.name,
            status=_STATUS_OK,
            summary=self._summarise(swan_result),
            artefacts=self._artefacts(swan_result),
            duration=duration,
            raw=swan_result,
        )

    def _build(self, api_key: str) -> Any:
        if self._factory is not None:
            return self._factory(api_key)
        get_swan, _ = self._import_factory()
        return get_swan(api_key=api_key or "")

    @staticmethod
    def _import_factory() -> tuple[Any, Any]:
        from skills.swan_agent import SwanOrchestrator, get_swan  # noqa: PLC0415
        return get_swan, SwanOrchestrator

    @staticmethod
    def _summarise(swan_result: Any) -> str:
        if swan_result is None:
            return "swan returned no result"
        text = getattr(swan_result, "text", None) or getattr(swan_result, "summary", None)
        if isinstance(text, str) and text.strip():
            head = text.strip().splitlines()[0][:120]
            return f"swan: {head}"
        return "swan run completed"

    @staticmethod
    def _artefacts(swan_result: Any) -> dict[str, Any]:
        if swan_result is None:
            return {}
        out: dict[str, Any] = {}
        for attribute in ("expert_id", "reward", "detection_probability", "elapsed"):
            value = getattr(swan_result, attribute, None)
            if value is not None:
                out[attribute] = value
        return out


class GoalValidator:
    """Boundary validator: raw input → :class:`OrchestratorGoal`.

    The validator is the single place where user-controlled strings are
    bounded and the mode whitelist is enforced. Everything downstream
    works with already-validated values.
    """

    def __init__(self, config: OrchestratorConfig) -> None:
        """Bind the validator to the active configuration."""
        self._config = config

    def validate(
        self,
        goal: str,
        mode: str = "",
        phase: str = "",
        task_type: str = "",
        target: str = "",
        drones: int = 0,
        timeout: float = 0.0,
        api_key: str = "",
        metadata: Mapping[str, Any] | None = None,
    ) -> OrchestratorGoal:
        """Return a normalised goal or raise :class:`ValueError`.

        Args:
            goal: Free-form objective string.
            mode: Routing mode (``auto`` / ``daemon`` / ``hive`` / ``swan``).
            phase: Kill-chain phase identifier.
            task_type: SWAN task type identifier.
            target: Single-target identifier for the daemon backend.
            drones: Hive drone count.
            timeout: SWAN timeout in seconds.
            api_key: Optional API key forwarded to the backend.
            metadata: Optional metadata mapping carried alongside the
                goal (used by tests to inject a stable ``request_id``).

        Returns:
            A validated :class:`OrchestratorGoal`.

        Raises:
            ValueError: When ``goal`` is empty or ``mode`` is unknown.
        """
        if not isinstance(goal, str) or not goal.strip():
            raise ValueError(self._config.empty_goal_message)
        bounded_goal = goal.strip()[: self._config.max_goal_chars]
        chosen_mode = (mode or self._config.default_mode).strip()
        if chosen_mode not in self._config.enabled_modes:
            raise ValueError(self._config.invalid_modes_message)
        meta = dict(metadata) if metadata else {}
        meta.setdefault("request_id", _new_request_id())
        return OrchestratorGoal(
            goal=bounded_goal,
            mode=chosen_mode,
            phase=phase.strip() if isinstance(phase, str) else "",
            task_type=task_type.strip() if isinstance(task_type, str) else "",
            target=target.strip() if isinstance(target, str) else "",
            drones=max(0, int(drones)) if isinstance(drones, (int, float)) else 0,
            timeout=max(0.0, float(timeout)) if isinstance(timeout, (int, float)) else 0.0,
            api_key=api_key.strip() if isinstance(api_key, str) else "",
            metadata=meta,
        ).with_defaults(self._config)


class UnifiedOrchestrator:
    """Single entry point that routes a goal through one of the backends."""

    def __init__(
        self,
        config: OrchestratorConfig,
        registry: BackendRegistry,
        router: RouterPolicy,
        validator: GoalValidator,
        bus: EventBus,
    ) -> None:
        """Bind the orchestrator to its collaborators."""
        self._config = config
        self._registry = registry
        self._router = router
        self._validator = validator
        self._bus = bus

    @property
    def backends(self) -> tuple[str, ...]:
        """Return the registered backend names in declaration order."""
        return self._registry.names

    def execute(
        self,
        goal: str,
        mode: str = "",
        phase: str = "",
        task_type: str = "",
        target: str = "",
        drones: int = 0,
        timeout: float = 0.0,
        api_key: str = "",
        metadata: Mapping[str, Any] | None = None,
    ) -> OrchestratorResult:
        """Validate, route, execute and emit one goal end-to-end.

        Returns:
            The normalised :class:`OrchestratorResult`. Validation errors
            and missing backends are returned as results with the
            corresponding status — this method never raises.
        """
        try:
            validated = self._validator.validate(
                goal=goal,
                mode=mode,
                phase=phase,
                task_type=task_type,
                target=target,
                drones=drones,
                timeout=timeout,
                api_key=api_key,
                metadata=metadata,
            )
        except ValueError as exc:
            result = _make_result(
                request_id=_new_request_id(),
                backend="",
                status=_STATUS_INVALID,
                summary=str(exc),
            )
            self._emit(result, mode=mode, goal=goal)
            return result
        backend = self._router.choose(validated)
        if backend is None:
            result = _make_result(
                request_id=validated.metadata.get("request_id", _new_request_id()),
                backend=validated.mode,
                status=_STATUS_UNAVAILABLE,
                summary=self._config.backend_missing_message,
            )
            self._emit(result, mode=validated.mode, goal=validated.goal)
            return result
        result = backend.run(validated)
        self._emit(result, mode=validated.mode, goal=validated.goal)
        return result

    def _emit(self, result: OrchestratorResult, mode: str, goal: str) -> None:
        event = {
            "kind": self._config.autonomous_event_kind,
            "request_id": result.request_id,
            "mode": mode,
            "backend": result.backend,
            "status": result.status,
            "goal": goal[: self._config.max_goal_chars],
            "summary": result.summary,
            "duration": result.duration,
            "ts": time.time(),
        }
        self._bus.emit(event)


def _new_request_id() -> str:
    """Return a short opaque identifier used to correlate events."""
    return uuid.uuid4().hex[:12]


def _make_result(
    request_id: str,
    backend: str,
    status: str,
    summary: str,
    artefacts: Mapping[str, Any] | None = None,
    events: Sequence[Mapping[str, Any]] | None = None,
    duration: float = 0.0,
    raw: Any = None,
) -> OrchestratorResult:
    """Construct an :class:`OrchestratorResult` with sane defaults.

    The helper avoids repeating the verbose dataclass-instantiation
    keyword list at every error path.
    """
    return OrchestratorResult(
        request_id=request_id,
        backend=backend,
        status=status,
        summary=summary,
        artefacts=dict(artefacts or {}),
        events=tuple(events or ()),
        duration=duration,
        raw=raw,
    )


def build_default_orchestrator(
    payload: Mapping[str, Any] | None,
    sessions_dir: str | None = None,
) -> UnifiedOrchestrator:
    """Wire the canonical three-backend orchestrator.

    Args:
        payload: ``payload.json`` mapping. Used to derive the config and
            forwarded to per-backend defaults.
        sessions_dir: Optional override for the sessions directory.

    Returns:
        A ready-to-use :class:`UnifiedOrchestrator`.
    """
    config = OrchestratorConfig.from_payload(payload)
    if sessions_dir is not None and sessions_dir.strip():
        config = replace(config, sessions_dir=sessions_dir.strip())
    backends: list[IOrchestratorBackend] = [
        DaemonBackend(config, payload=payload),
        HiveBackend(config),
        SwanBackend(config),
    ]
    registry = BackendRegistry(backends)
    router = RouterPolicy(config, registry)
    validator = GoalValidator(config)
    bus = EventBus(config)
    return UnifiedOrchestrator(config, registry, router, validator, bus)


__all__ = [
    "OrchestratorConfig",
    "OrchestratorGoal",
    "OrchestratorResult",
    "IOrchestratorBackend",
    "EventBus",
    "BackendRegistry",
    "RouterPolicy",
    "DaemonBackend",
    "HiveBackend",
    "SwanBackend",
    "GoalValidator",
    "UnifiedOrchestrator",
    "build_default_orchestrator",
]
