
"""Unified kill-chain — single source of truth consumed by all surfaces.

This module is the canonical authority for kill-chain phases, progress
derivation, phase mapping, and atomic updates. Every kill-chain display
(CLI, Flask dashboard, GUI2, Textual TUI, tips engine, recommendation
signals, MCP) imports from here. There is exactly one phase definition,
one mapping table, and one update path.

Contracts:
    - ``KillChainConfig`` holds all definitions (phases, colors, labels, maps).
    - ``KillChain`` reads from the `WorldModel` singleton as the primary
      source and falls back to raw ``world_model.json`` keys for operator
      overrides.
    - ``KillChain.advance_phase()`` is the only function that writes
      ``current_phase`` / ``completed_phases`` / ``phase`` into the raw
      JSON. Every other module that needs to change the kill-chain phase
      must call this function.
"""

from __future__ import annotations

import datetime
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

from modules.world_model import read_state_dict, write_state_dict

_log = logging.getLogger(__name__)

_LAZYOWN_DIR = Path(os.environ.get("LAZYOWN_DIR", str(Path(__file__).resolve().parent.parent)))
_SESSIONS_DIR = _LAZYOWN_DIR / "sessions"
_WORLD_MODEL_PATH = _SESSIONS_DIR / "world_model.json"


@dataclass(frozen=True, slots=True)
class KillChainConfig:
    """Centralised constants for the unified kill-chain.

    Every colour, label, and mapping lives here. No magic values anywhere.
    """

    phases: tuple[str, ...] = field(default=(
        "recon", "scan", "enum", "exploit", "privesc", "lateral", "exfil", "report"
    ))
    phase_labels: dict[str, str] = field(default_factory=lambda: {
        "recon": "Reconnaissance",
        "scan": "Scanning",
        "enum": "Enumeration",
        "exploit": "Exploitation",
        "privesc": "Privilege Escalation",
        "lateral": "Lateral Movement",
        "exfil": "Exfiltration",
        "report": "Reporting",
    })
    phase_colors: dict[str, str] = field(default_factory=lambda: {
        "recon": "#a371f7",
        "scan": "#58a6ff",
        "enum": "#56d364",
        "exploit": "#f85149",
        "privesc": "#d2991d",
        "lateral": "#db61a2",
        "exfil": "#7c3aed",
        "report": "#3fb950",
    })
    phase_rich_colors: dict[str, str] = field(default_factory=lambda: {
        "recon": "cyan",
        "scan": "blue",
        "enum": "magenta",
        "exploit": "bold red",
        "privesc": "bold yellow",
        "lateral": "orange3",
        "exfil": "dark_orange",
        "report": "green",
    })
    engagement_to_cli: dict[str, str] = field(default_factory=lambda: {
        "recon": "recon",
        "scanning": "scan",
        "enumeration": "enum",
        "exploitation": "exploit",
        "post_exploitation": "privesc",
        "complete": "report",
    })
    cli_to_host_state: dict[str, str] = field(default_factory=lambda: {
        "recon": "",
        "scan": "scanned",
        "enum": "enumerated",
        "exploit": "exploited",
        "privesc": "owned",
        "lateral": "owned",
        "exfil": "owned",
        "report": "owned",
        "cred": "owned",
        "postexp": "owned",
        "persist": "owned",
        "c2": "owned",
    })
    compact_phases: tuple[str, ...] = field(default=("recon", "enum", "exploit", "privesc", "lateral"))
    compact_labels: dict[str, str] = field(default_factory=lambda: {
        "recon": "R", "enum": "E", "exploit": "X", "privesc": "P", "lateral": "L"
    })
    sessions_dir: Path = field(default=_SESSIONS_DIR)
    world_model_filename: str = field(default="world_model.json")

    def world_model_path(self) -> Path:
        """Return the resolved path to world_model.json."""
        return self.sessions_dir / self.world_model_filename

    def phase_index(self, phase: str) -> int:
        """Return the positional index of a canonical phase in the kill chain."""
        try:
            return self.phases.index(phase)
        except ValueError:
            return -1

    def is_valid_phase(self, phase: str) -> bool:
        """Return True when ``phase`` is a recognised canonical phase."""
        return phase in self.phases


_DEFAULT_CONFIG = KillChainConfig()


@dataclass(frozen=True, slots=True)
class PhaseStatus:
    """Progress for a single kill-chain phase."""

    key: str
    label: str
    color: str
    status: str  # "done" | "active" | "pending"


class KillChain:
    """Unified kill-chain operations consumed by every display surface.

    All methods are static or classmethods so no instantiation is needed.
    The `WorldModel` singleton is read as the primary source; raw JSON
    keys in ``world_model.json`` provide operator overrides.
    """

    @staticmethod
    def config() -> KillChainConfig:
        """Return the centralised configuration."""
        return _DEFAULT_CONFIG

    @staticmethod
    def phases() -> tuple[str, ...]:
        """Return the canonical 8-phase tuple."""
        return _DEFAULT_CONFIG.phases

    @staticmethod
    def phase_labels() -> dict[str, str]:
        """Return the canonical phase label mapping."""
        return _DEFAULT_CONFIG.phase_labels

    @staticmethod
    def phase_colors() -> dict[str, str]:
        """Return the canonical phase hex-color mapping."""
        return _DEFAULT_CONFIG.phase_colors

    @staticmethod
    def phase_rich_colors() -> dict[str, str]:
        """Return the canonical phase rich-terminal color mapping."""
        return _DEFAULT_CONFIG.phase_rich_colors

    @staticmethod
    def engagement_phase_to_cli(engagement_value: str) -> str:
        """Map a ``WorldModel.EngagementPhase`` value to the CLI phase key.

        Args:
            engagement_value: An ``EngagementPhase`` value string.

        Returns:
            The corresponding CLI phase or ``"recon"`` as the safe default.
        """
        return _DEFAULT_CONFIG.engagement_to_cli.get(engagement_value, "recon")

    @staticmethod
    def cli_phase_to_host_state(phase: str) -> str:
        """Map a CLI phase to a ``WorldModel.HostState`` value.

        Args:
            phase: A canonical CLI phase key.

        Returns:
            The corresponding ``HostState.value``, or empty string when no
            state advancement is warranted.
        """
        return _DEFAULT_CONFIG.cli_to_host_state.get(phase, "")

    @staticmethod
    def current_phase(
        world_model_path: Path | None = None,
    ) -> str:
        """Derive the current kill-chain phase.

        Resolution order:
        1. ``WorldModel.get_phase()`` (derived from host states).
        2. Raw ``world_model.json`` ``current_phase`` key (operator override).
        3. Raw ``world_model.json`` ``phase`` key (legacy).
        4. ``"recon"`` as the safe fallback.

        Args:
            world_model_path: Optional override path for the world model file.

        Returns:
            A canonical CLI phase key.
        """
        wm_path = world_model_path or _DEFAULT_CONFIG.world_model_path()
        cli_phase = "recon"
        try:
            from modules.world_model import get_world_model, read_state_dict
            wm_path = world_model_path or _DEFAULT_CONFIG.world_model_path()
            wm = get_world_model(path=wm_path)
            wm_phase = wm.get_phase().value
            cli_phase = KillChain.engagement_phase_to_cli(wm_phase)
        except Exception as exc:
            _log.debug("WorldModel phase read failed: %s", exc)

        try:
            raw = read_state_dict(wm_path)
            explicit = (raw.get("current_phase") or "").strip().lower()
            if explicit and _DEFAULT_CONFIG.is_valid_phase(explicit):
                explicit_rank = _DEFAULT_CONFIG.phase_index(explicit)
                derived_rank = _DEFAULT_CONFIG.phase_index(cli_phase)
                if explicit_rank > derived_rank:
                    return explicit
                return cli_phase if derived_rank >= 0 else explicit
            legacy = (raw.get("phase") or "").strip().lower()
            if legacy and _DEFAULT_CONFIG.is_valid_phase(legacy):
                return legacy
        except Exception as exc:
            _log.debug("Raw world_model.json read failed: %s", exc)

        return cli_phase

    @staticmethod
    def advance_phase(
        new_phase: str,
        world_model_path: Path | None = None,
    ) -> bool:
        """Advance the kill-chain phase for all connected surfaces.

        Persists ``current_phase``, ``phase``, and ``completed_phases``
        in the raw ``world_model.json`` AND advances every host in the
        ``WorldModel`` to the corresponding ``HostState``.

        Args:
            new_phase: A valid canonical phase key.
            world_model_path: Optional override path for the world model file.

        Returns:
            True when the write succeeded, False otherwise.
        """
        if not _DEFAULT_CONFIG.is_valid_phase(new_phase):
            _log.warning("Invalid phase %r passed to advance_phase", new_phase)
            return False

        wm_path = world_model_path or _DEFAULT_CONFIG.world_model_path()
        try:
            raw = read_state_dict(wm_path)
        except Exception:
            raw = {}

        old_phase = (raw.get("phase") or raw.get("current_phase") or "").strip().lower()

        raw["phase"] = new_phase
        raw["current_phase"] = new_phase

        completed: list[str] = list(raw.get("completed_phases", []) or [])
        if old_phase and _DEFAULT_CONFIG.is_valid_phase(old_phase):
            old_idx = _DEFAULT_CONFIG.phase_index(old_phase)
            new_idx = _DEFAULT_CONFIG.phase_index(new_phase)
            if new_idx > old_idx:
                for p in _DEFAULT_CONFIG.phases[old_idx:new_idx]:
                    if p not in completed:
                        completed.append(p)
        raw["completed_phases"] = completed

        try:
            write_state_dict(wm_path, raw)
            _log.info("KillChain advanced to %s (completed: %s)", new_phase, completed)
        except Exception as exc:
            _log.error("Failed to write world_model.json: %s", exc)
            return False

        target_state = KillChain.cli_phase_to_host_state(new_phase)
        if target_state:
            try:
                from modules.world_model import HostState, get_world_model
                wm = get_world_model(path=wm_path)
                wm.reload()
                for ip in wm.get_hosts_summary():
                    wm.advance_host(ip, HostState(target_state))
            except Exception as exc:
                _log.warning("WorldModel host advance failed: %s", exc)

        return True

    @staticmethod
    def get_progress(
        world_model_path: Path | None = None,
    ) -> list[PhaseStatus]:
        """Return the current kill-chain progress as a list of status objects.

        Each phase is tagged as ``"done"``, ``"active"``, or ``"pending"``.
        Suitable for rendering in any UI (CLI, web, GUI, TUI).

        Args:
            world_model_path: Optional override path for the world model file.

        Returns:
            A list of ``PhaseStatus`` named tuples in kill-chain order.
        """
        wm_path = world_model_path or _DEFAULT_CONFIG.world_model_path()
        current = KillChain.current_phase(world_model_path=wm_path)
        completed: set[str] = set()
        try:
            raw = read_state_dict(wm_path)
            raw_completed = raw.get("completed_phases", [])
            if isinstance(raw_completed, list):
                completed = {str(p).strip().lower() for p in raw_completed if _DEFAULT_CONFIG.is_valid_phase(str(p).strip().lower())}
        except Exception:
            pass

        current_idx = _DEFAULT_CONFIG.phase_index(current)
        result: list[PhaseStatus] = []
        for idx, phase_key in enumerate(_DEFAULT_CONFIG.phases):
            if phase_key == current:
                status = "active"
            elif phase_key in completed or (current_idx >= 0 and idx < current_idx):
                status = "done"
            else:
                status = "pending"
            result.append(PhaseStatus(
                key=phase_key,
                label=_DEFAULT_CONFIG.phase_labels.get(phase_key, phase_key),
                color=_DEFAULT_CONFIG.phase_colors.get(phase_key, "#484f58"),
                status=status,
            ))
        return result

    @staticmethod
    def compact_progress(current_phase: str, phases_entered: list[str] | None = None) -> str:
        """Return a compact single-line progress indicator ``[R>E>X>P>L]``.

        Args:
            current_phase: The active phase key.
            phases_entered: Optional list of phases the operator has entered.

        Returns:
            A string suitable for inline display (e.g., below the prompt).
        """
        entered_set = set(phases_entered or [])
        parts: list[str] = []
        for i, p in enumerate(_DEFAULT_CONFIG.compact_phases):
            label = _DEFAULT_CONFIG.compact_labels.get(p, p[0].upper())
            parts.append(label)
            if i < len(_DEFAULT_CONFIG.compact_phases) - 1:
                parts.append(">")
        return "[" + "".join(parts) + "]"

    @staticmethod
    def phases_for_display() -> tuple[tuple[str, str, str], ...]:
        """Return an ordered ``(key, label, hex_color)`` triple for every phase.

        Convenience for UI builders that need to render every phase.
        """
        return tuple(
            (p, _DEFAULT_CONFIG.phase_labels.get(p, p), _DEFAULT_CONFIG.phase_colors.get(p, "#484f58"))
            for p in _DEFAULT_CONFIG.phases
        )

    @staticmethod
    def phase_index(phase: str) -> int:
        """Return the zero-based index of a canonical phase."""
        return _DEFAULT_CONFIG.phase_index(phase)

    @staticmethod
    def snapshot(world_model_path: Path | None = None) -> dict:
        """Return a single, render-agnostic snapshot of the whole kill-chain.

        This is the one payload every surface (CLI, Flask dashboard, GUI2,
        Textual TUI, tips engine, REST API) consumes. It centralises the
        current phase, the completed set, per-phase progress, host states and
        a compact progress glyph so surfaces cannot diverge.

        Args:
            world_model_path: Optional override path for the world model file.

        Returns:
            A JSON-serialisable dict with keys: ``current_phase``,
            ``completed_phases``, ``progress``, ``host_states``,
            ``compact`` and ``updated_at``.
        """
        wm_path = world_model_path or _DEFAULT_CONFIG.world_model_path()
        progress = KillChain.get_progress(world_model_path=wm_path)
        current = KillChain.current_phase(world_model_path=wm_path)
        raw = read_state_dict(wm_path)
        completed: list[str] = []
        for p in (raw.get("completed_phases") or []):
            key = str(p).strip().lower()
            if _DEFAULT_CONFIG.is_valid_phase(key) and key not in completed:
                completed.append(key)
        phases_entered = (raw.get("phases_entered") or []) or completed
        host_states: dict[str, str] = {}
        for ip, host in (raw.get("hosts") or {}).items():
            if isinstance(host, dict):
                host_states[str(ip)] = str(host.get("state") or "unscanned")
        return {
            "current_phase": current,
            "completed_phases": completed,
            "progress": [
                {"key": p.key, "label": p.label, "color": p.color, "status": p.status}
                for p in progress
            ],
            "host_states": host_states,
            "compact": KillChain.compact_progress(current, phases_entered=phases_entered),
            "updated_at": datetime.datetime.now(datetime.UTC).isoformat(),
        }


def get_killchain() -> type[KillChain]:
    """Return the ``KillChain`` class as a module-level entry point."""
    return KillChain


__all__ = [
    "KillChain",
    "KillChainConfig",
    "PhaseStatus",
    "get_killchain",
]
