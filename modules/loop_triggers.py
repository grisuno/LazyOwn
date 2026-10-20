"""TriggerStore: persistent loop triggers extracted from the loop core.

Responsibility-only extraction (no behavior change): the trigger
catalogue used to live inside the loop core module. It now owns its own
file so the loop core shrinks and trigger semantics stay editable in
one place. Path resolution and JSON helpers are resolved through the
loop core at call time, so store redirections monkeypatched by tests
keep applying to every user of this module.
"""

from __future__ import annotations

TRIGGER_KINDS = ("interval", "finding", "goal", "timeout", "toolcall", "hint", "service", "task_create")


def _core():
    """Import the loop core lazily to keep this module cycle-free."""
    import modules.lazy_loop as core

    return core


class TriggerStore:
    """Persistent event/interval triggers like server/scheduler (P3)."""

    def __init__(self, task_id: str = "") -> None:
        """Bind trigger table (global when task_id empty)."""
        core = _core()
        name = f"triggers_{task_id}.json" if task_id else "triggers.json"
        self._path = core._store_path(name)

    def _load(self) -> dict:
        """Load trigger payload."""
        return _core()._load_json(self._path, {"seq": 0, "items": []})

    def add(self, kind: str, arg: str = "", every_sec: float = 0.0) -> dict:
        """Register a trigger; interval needs every_sec, events fire on new rows."""
        from modules.trigger_policy import TRIGGER_POLICY

        core = _core()
        if kind not in core.TRIGGER_KINDS:
            raise ValueError(f"kind must be one of {core.TRIGGER_KINDS}")
        payload = self._load()
        payload["seq"] = int(payload.get("seq", 0)) + 1
        item = {
            "id": payload["seq"],
            "kind": kind,
            "arg": (arg or "")[: TRIGGER_POLICY.arg_max_chars],
            "every_sec": float(every_sec or 0.0),
            "last_fire": 0.0,
            "watermark": 0,
            "enabled": True,
        }
        payload.setdefault("items", []).append(item)
        core._save_json(self._path, payload)
        return item

    def upsert_defaults(self, seeds: list[dict]) -> list[dict]:
        """Merge declarative seeds without duplicating or re-enabling.

        Args:
            seeds: Seed entries shaped like ``{kind, arg, every_sec, enabled}``.

        Returns:
            The trigger items added by this call.
        """
        core = _core()
        payload = self._load()
        items = list(payload.get("items", []))
        existing = {(str(i.get("kind", "")), str(i.get("arg", "")), str(i.get("task_id", ""))) for i in items}
        added: list[dict] = []
        for seed in seeds:
            kind = str(seed.get("kind", "")).strip()
            if kind not in core.TRIGGER_KINDS:
                continue
            arg = str(seed.get("arg", "") or "")[:300]
            signature = (kind, arg, str(seed.get("task_id", "") or ""))
            if signature in existing:
                continue
            payload["seq"] = int(payload.get("seq", 0)) + 1
            item = {
                "id": payload["seq"],
                "kind": kind,
                "arg": arg,
                "every_sec": float(seed.get("every_sec", 0.0) or 0.0),
                "last_fire": 0.0,
                "watermark": 0,
                "enabled": bool(seed.get("enabled", True)),
            }
            if signature[2]:
                item["task_id"] = signature[2]
            items.append(item)
            existing.add(signature)
            added.append(item)
        if added:
            payload["items"] = items
            core._save_json(self._path, payload)
        return added

    def remove(self, trigger_id: int) -> bool:
        """Delete a trigger."""
        core = _core()
        payload = self._load()
        before = len(payload.get("items", []))
        payload["items"] = [i for i in payload["items"] if int(i.get("id", 0)) != int(trigger_id)]
        if len(payload["items"]) != before:
            core._save_json(self._path, payload)
            return True
        return False

    def set_enabled(self, trigger_id: int, enabled: bool) -> bool:
        """Flip one trigger's enabled flag in place."""
        core = _core()
        payload = self._load()
        touched = False
        for item in payload.get("items", []):
            if int(item.get("id", 0)) == int(trigger_id):
                if bool(item.get("enabled")) != bool(enabled):
                    item["enabled"] = bool(enabled)
                    touched = True
        if touched:
            core._save_json(self._path, payload)
        return touched

    def list(self) -> list[dict]:
        """Return all triggers."""
        return list(self._load().get("items", []))

    def ensure_service_trigger(self) -> bool:
        """Register the catalog trigger once so services fire the loop.

        The trigger is what turns ``lazyaddons`` / ``tools`` service
        metadata into an orchestrator event: whenever a new service
        asset lands, the next round fires with the matching addon and
        tool names attached.
        """
        if any(item.get("kind") == "service" for item in self.list()):
            return False
        self.add("service")
        return True

    def due(self, task_id: str, graph, activity, assets=None, store=None) -> list[dict]:
        """Evaluate triggers like the scheduler tick; fires at most once each.

        The ``service`` and ``task_create`` kinds need the asset graph /
        task store: pass them to enable those events, the rest stay
        graph/activity driven.
        """
        core = _core()
        payload = self._load()
        fired: list[dict] = []
        now = core._now()
        for item in payload.get("items", []):
            if not item.get("enabled"):
                continue
            kind = item.get("kind")
            if kind == "interval":
                if now - float(item.get("last_fire", 0.0)) >= max(5.0, float(item.get("every_sec", 60.0))):
                    item["last_fire"] = now
                    fired.append({"kind": "interval", "id": item["id"]})
            elif kind == "finding":
                current = [n.node_id for n in graph.list("finding")]
                new = [i for i in current if i > int(item.get("watermark", 0))]
                if new:
                    item["watermark"] = max(new)
                    fired.append({"kind": "finding", "ids": new, "id": item["id"]})
            elif kind == "goal":
                met = [n.node_id for n in graph.list("goal", "done")]
                seen = set(item.get("fired_goals", []))
                new = [i for i in met if i not in seen]
                if new:
                    item["fired_goals"] = sorted(seen | set(new))
                    fired.append({"kind": "goal", "ids": new, "id": item["id"]})
            elif kind == "hint":
                pending = [n.node_id for n in graph.list("hint", "pending")]
                new = [i for i in pending if i > int(item.get("watermark", 0))]
                if new:
                    item["watermark"] = max(new)
                    fired.append({"kind": "hint", "ids": new, "id": item["id"]})
            elif kind == "toolcall":
                total = len(activity.read(2000))
                if total > int(item.get("watermark", 0)):
                    item["watermark"] = total
                    fired.append({"kind": "toolcall", "total": total, "id": item["id"]})
            elif kind == "service":
                if assets is None:
                    continue
                fresh = [a for a in assets.list("service") if a.asset_id > int(item.get("watermark", 0))]
                if fresh:
                    item["watermark"] = max(a.asset_id for a in fresh)
                    hits: list[str] = []
                    try:
                        from modules.auto_registry import addon_hits_for

                        for asset in fresh[:8]:
                            for name, source in addon_hits_for(asset.value, limit=3):
                                label = f"{name}:{source}"
                                if label not in hits:
                                    hits.append(label)
                    except Exception:
                        hits = []
                    fired.append(
                        {
                            "kind": "service",
                            "ids": [a.asset_id for a in fresh],
                            "services": [a.value for a in fresh[:8]],
                            "addons": hits[:8],
                            "id": item["id"],
                        }
                    )
            elif kind == "task_create":
                if store is None:
                    continue
                current = [str(task.get("task_id", "")) for task in store.list()]
                seen = set(item.get("fired_tasks", []))
                fresh = [task_id_value for task_id_value in current if task_id_value not in seen]
                if fresh:
                    item["fired_tasks"] = sorted(seen | set(fresh))
                    fired.append({"kind": "task_create", "ids": fresh, "id": item["id"]})
            elif kind == "timeout":
                fired.append({"kind": "timeout", "id": item["id"]})
        if fired:
            core._save_json(self._path, payload)
        return fired


__all__ = ["TRIGGER_KINDS", "TriggerStore"]
