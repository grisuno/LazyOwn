"""World-diff sink: snapshot hosts and record what changed per outcome."""

from __future__ import annotations

from pathlib import Path

from modules.lazy_world_diff import campaign_snapshots, record_changes
from modules.outcome_bus import SESSIONS_DIR, OutcomeEvent
from modules.world_model import read_state_dict

_DIFF_KINDS = frozenset({"discovery", "finding", "exploit", "shell", "chain", "emulation", "report"})


def apply(event: OutcomeEvent) -> bool:
    """Diff one host's world snapshot and record the changes.

    Args:
        event: Outcome that may have moved the world.

    Returns:
        True when a snapshot was created or refreshed (changes recorded
        or not); False when there was nothing to diff.
    """
    if event.kind not in _DIFF_KINDS:
        return False
    host = event.host_value
    if not host:
        return False
    root = Path(str(event.metadata.get("sessions_dir") or SESSIONS_DIR))
    try:
        before = _stored_host(root, host)
        after = _current_host(root, host)
    except Exception:
        return False
    if not after and not before:
        return False
    if before == after:
        return False
    try:
        from modules.lazy_world_diff import SurfaceChange, diff_snapshots

        if before is None:
            record_changes([SurfaceChange("host_new", host, 0, None, {"state": str(after.get("state", ""))})], root)
        else:
            record_changes(diff_snapshots(before, after), root)
        _store_host(root, host, after)
    except Exception:
        return False
    return True


def _stored_host(root: Path, host: str) -> dict | None:
    from modules.lazy_world_diff import load_host_snapshots

    return load_host_snapshots(root).get(host)


def _current_host(root: Path, host: str) -> dict:
    from modules.lazy_world_diff import host_snapshot

    world = read_state_dict(root / "world_model.json")
    return host_snapshot(world if isinstance(world, dict) else {}, host)


def _store_host(root: Path, host: str, snapshot: dict) -> None:
    from modules.lazy_world_diff import load_host_snapshots, save_host_snapshots

    stored = load_host_snapshots(root)
    stored[host] = snapshot
    save_host_snapshots(stored, root)


__all__ = ["apply", "campaign_snapshots"]
