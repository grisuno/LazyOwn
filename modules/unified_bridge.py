"""
UnifiedBridge — single API over all LazyOwn bridges and routing engines.

Merges three previously isolated bridges into one cohesive interface:
- lazyown_bridge  : command catalog + phase/service-aware selection
- toposwarm_bridge: neural/keyword routing from natural language
- mcp_agent_bridge: AI agent delegation (Groq/Ollama)

Plus integration with EventBus (all routing decisions published) and
StateManager (context from current campaign state).

Design (SOLID)
--------------
- Single Responsibility : route prompts to tools; delegate to agents.
- Open/Closed           : add backends via register_route_backend().
- Liskov                : all backends return RouteResult with same shape.
- Interface Segregation : route() and delegate() are the only two operations.
- Dependency Inversion  : depends on RouteBackend abstraction, not concrete bridges.
"""

from __future__ import annotations

import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

log = logging.getLogger("unified_bridge")

_LAZYOWN_DIR = Path(__file__).resolve().parent.parent
_SESSIONS_DIR = _LAZYOWN_DIR / "sessions"


@dataclass
class RouteResult:
    prompt: str
    tool: str = ""
    args: dict[str, Any] = field(default_factory=dict)
    command: str = ""
    confidence: float = 0.0
    backend: str = "unknown"
    phase: str = ""
    explanation: str = ""
    error: str = ""


@dataclass
class DelegateResult:
    goal: str
    agent_id: str = ""
    status: str = "pending"
    result: str = ""
    error: str = ""


class RouteBackend(ABC):
    @abstractmethod
    def available(self) -> bool: ...

    @abstractmethod
    def route(self, prompt: str, context: dict[str, Any]) -> RouteResult: ...


class KeywordBackend(RouteBackend):
    """Regex/keyword-based routing (~80% accuracy on common pentesting phrases)."""

    _KEYWORD_MAP: dict[str, tuple[str, str]] = {
        "scan": ("lazyown_run_command", "lazynmap"),
        "nmap": ("lazyown_run_command", "lazynmap"),
        "enum": ("lazyown_run_command", "enum4linux"),
        "smb": ("lazyown_run_command", "smbmap"),
        "exploit": ("lazyown_run_command", "searchsploit"),
        "creds": ("lazyown_run_command", "lazycredsspray"),
        "crack": ("lazyown_run_command", "john"),
        "hash": ("lazyown_run_command", "hashcat"),
        "privesc": ("lazyown_run_command", "lazyprivesc"),
        "persist": ("lazyown_run_command", "lazypersist"),
        "c2": ("lazyown_run_command", "lazyc2"),
        "vuln": ("lazyown_recommend_next", ""),
        "report": ("lazyown_run_command", "lazystartreport"),
        "facts": ("lazyown_facts_show", ""),
        "beacon": ("lazyown_get_beacons", ""),
        "web": ("lazyown_run_command", "lazywebscan"),
        "http": ("lazyown_run_command", "lazywebscan"),
        "kerbero": ("lazyown_run_command", "GetUserSPNs"),
        "bloodhound": ("lazyown_run_command", "bloodhound"),
        "pivot": ("lazyown_run_command", "lazypivot"),
        "exfil": ("lazyown_run_command", "lazyexfil"),
    }

    def available(self) -> bool:
        return True

    def route(self, prompt: str, context: dict[str, Any]) -> RouteResult:
        prompt_lower = prompt.lower()
        best_match = ("lazyown_recommend_next", "")
        best_len = 0
        for keyword, (tool, args_str) in self._KEYWORD_MAP.items():
            if keyword in prompt_lower and len(keyword) > best_len:
                best_match = (tool, args_str)
                best_len = len(keyword)
        return RouteResult(
            prompt=prompt,
            tool=best_match[0],
            command=best_match[1],
            confidence=0.8,
            backend="keyword",
            explanation=f"Keyword '{best_match}' matched",
        )


class LazyownBridgeBackend(RouteBackend):
    """Phase-aware command selection using the lazyown_bridge catalog."""

    def available(self) -> bool:
        try:
            from modules.lazyown_bridge import BridgeDispatcher
            return True
        except ImportError:
            return False

    def route(self, prompt: str, context: dict[str, Any]) -> RouteResult:
        try:
            from modules.lazyown_bridge import BridgeDispatcher
            dispatcher = BridgeDispatcher()
            phase = context.get("phase", "recon")
            services = context.get("services", [])
            command = dispatcher.select_for_phase(phase, services)
            if command:
                return RouteResult(
                    prompt=prompt,
                    tool="lazyown_run_command",
                    command=command.command,
                    confidence=0.9,
                    backend="lazyown_bridge",
                    phase=command.phase,
                    explanation=command.description,
                )
        except Exception:
            log.debug("lazyown_bridge routing failed", exc_info=True)
        return RouteResult(
            prompt=prompt, backend="lazyown_bridge",
            error="No matching command found",
        )


class TopoSwarmBackend(RouteBackend):
    """Neural routing via the TopoSwarm 2M-parameter model."""

    def available(self) -> bool:
        try:
            from modules.toposwarm_bridge import TopoSwarmBridge
            bridge = TopoSwarmBridge()
            return bridge.available
        except ImportError:
            return False

    def route(self, prompt: str, context: dict[str, Any]) -> RouteResult:
        try:
            from modules.toposwarm_bridge import TopoSwarmBridge
            bridge = TopoSwarmBridge()
            topo_result = bridge.route(prompt)
            return RouteResult(
                prompt=prompt,
                tool=topo_result.tool_name,
                args=topo_result.args if hasattr(topo_result, 'args') else {},
                confidence=topo_result.confidence,
                backend=f"toposwarm_{topo_result.backend}",
                explanation=getattr(topo_result, 'explanation', ''),
            )
        except Exception:
            return RouteResult(
                prompt=prompt, backend="toposwarm",
                error="TopoSwarm routing failed",
            )


class UnifiedBridge:
    """Single entry point for all LazyOwn routing and delegation.

    Usage::

        bridge = UnifiedBridge.get()
        result = bridge.route("scan open ports on 10.0.0.1")
        if result.command:
            executor.run(f"{result.command} {result.args}")
        elif result.tool:
            # call MCP tool
            pass

        # Delegate to internal AI agents
        delegate = bridge.delegate("Analyze CVE-2023-1234", backend="groq")
    """

    _instance: Optional["UnifiedBridge"] = None

    def __init__(self) -> None:
        self._backends: list[RouteBackend] = []
        self._publish_callback: Optional[Callable[[str, str, dict], None]] = None
        self._init_backends()

    def _init_backends(self) -> None:
        self._backends.append(TopoSwarmBackend())
        self._backends.append(LazyownBridgeBackend())
        self._backends.append(KeywordBackend())

    @classmethod
    def get(cls) -> "UnifiedBridge":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def set_publish_callback(self, cb: Callable[[str, str, dict], None]) -> None:
        self._publish_callback = cb

    def _publish(self, category: str, event_type: str, payload: dict[str, Any]) -> None:
        if self._publish_callback:
            try:
                self._publish_callback(category, event_type, payload)
            except Exception:
                pass
        try:
            from modules.event_bus import EventCategory, LazyEvent, get_event_bus
            get_event_bus().publish(LazyEvent(
                category=EventCategory(category),
                event_type=event_type,
                source="unified_bridge",
                payload=payload,
            ))
        except Exception:
            pass

    def route(
        self,
        prompt: str,
        context: Optional[dict[str, Any]] = None,
    ) -> RouteResult:
        """Route a natural-language prompt to the best LazyOwn tool.

        Tries backends in priority order: TopoSwarm → lazyown_bridge → keyword.
        Returns the first successful (non-empty) route result.

        Args:
            prompt: Natural-language description of the desired action.
            context: Optional dict with phase, services, target, etc.

        Returns:
            RouteResult with tool name, command, args, confidence, and backend.
        """
        ctx = context or {}
        if "phase" not in ctx:
            ctx["phase"] = self._detect_phase()
        if "target" not in ctx:
            ctx["target"] = self._get_active_target()

        for backend in self._backends:
            if not backend.available():
                continue
            result = backend.route(prompt, ctx)
            if result.tool or result.command or result.error:
                self._publish("command", "route_complete", {
                    "prompt": prompt,
                    "tool": result.tool,
                    "command": result.command,
                    "backend": result.backend,
                    "confidence": result.confidence,
                })
                return result

        return RouteResult(
            prompt=prompt,
            backend="none",
            error="No routing backend available",
        )

    def delegate(
        self,
        goal: str,
        backend: str = "groq",
        timeout: int = 120,
    ) -> DelegateResult:
        """Delegate a complex task to an internal AI agent.

        Args:
            goal: Task description for the agent.
            backend: AI backend ("groq" or "ollama").
            timeout: Maximum seconds to wait.

        Returns:
            DelegateResult with agent_id, status, and result.
        """
        result = DelegateResult(goal=goal)
        try:
            from modules.mcp_agent_bridge import AgentBridgeWorker
            agent_id = f"bridge_{int(time.time())}"
            worker = AgentBridgeWorker(
                agent_id=agent_id,
                goal=goal,
                backend=backend,
            )
            worker.start()
            worker.join(timeout=timeout)
            result.agent_id = agent_id

            agent_file = _SESSIONS_DIR / "agents" / f"{agent_id}.jsonl"
            if agent_file.exists():
                try:
                    lines = agent_file.read_text(encoding="utf-8").strip().split("\n")
                    last = json.loads(lines[-1]) if lines else {}
                    result.status = last.get("status", "completed")
                    result.result = last.get("output", last.get("result", ""))
                except Exception:
                    pass
            else:
                result.status = "timeout"

            self._publish("command", "agent_delegated", {
                "goal": goal, "agent_id": agent_id,
                "backend": backend, "status": result.status,
            })
        except ImportError:
            result.error = "mcp_agent_bridge not available"
        except Exception as exc:
            result.error = str(exc)

        return result

    def list_backends(self) -> list[dict[str, Any]]:
        return [
            {"name": b.__class__.__name__, "available": b.available()}
            for b in self._backends
        ]

    def _detect_phase(self) -> str:
        try:
            from modules.state_manager import get_state_manager
            snap = get_state_manager().session_snapshot()
            return snap.phase
        except Exception:
            return "recon"

    def _get_active_target(self) -> str:
        try:
            from modules.state_manager import get_state_manager
            snap = get_state_manager().session_snapshot()
            return snap.active_target
        except Exception:
            return ""


def route_prompt(prompt: str, context: Optional[dict[str, Any]] = None) -> RouteResult:
    """Convenience: route a prompt without instantiating UnifiedBridge."""
    return UnifiedBridge.get().route(prompt, context)


def delegate_task(goal: str, backend: str = "groq") -> DelegateResult:
    """Convenience: delegate a task to an AI agent."""
    return UnifiedBridge.get().delegate(goal, backend)
