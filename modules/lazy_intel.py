"""Intel feed from the Lazy autonomous loop.

Every routing decision the loop makes (which shell verb, for which intent,
with what outcome) is recorded as JSONL under ``sessions/lazy/`` and fused
into the :class:`WorldModel` on sync. The intel graph
(``modules.intel_fusion.build_intel_graph``) and the attack graph
(``modules.attack_surface3d.build_attack_graph``) are derived views over
``sessions/`` artefacts, so feeding the world model feeds both graphs and
everything the orchestrator reads.

The same records back the TopoSwarm orchestrator dataset, see
:mod:`modules.lazy_orchestrator_dataset`.

Stdlib only. Never raises; all entry points degrade to no-ops on error.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STORE_DIR = REPO_ROOT / "sessions" / "lazy"
ROUTING_LOG = "routing_decisions.jsonl"

OUTCOME_TERMINAL = ("done", "blocked", "exhausted", "stopped")


def _now() -> float:
    """Return current epoch seconds."""
    return time.time()


def _log_path() -> Path:
    """Return routing log path, ensuring the directory exists."""
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    return STORE_DIR / ROUTING_LOG


def _mask(text: str) -> str:
    """Mask secrets in stored text, mirroring console redaction.

    Beyond pattern redaction, configured credential values from the live
    payload are replaced outright (the PentAGI secret-patterns idea), so
    routing records and training rows never persist live passwords or keys.
    """
    try:
        from utils import redact_secrets as _redact

        masked = _redact(text)
    except Exception:
        masked = str(text or "")
    try:
        from core.config import load_payload

        payload = load_payload() or {}
        secrets = [
            str(payload.get(key, "") or "")
            for key in (
                "start_pass",
                "password",
                "backdoor_password",
                "api_key",
                "c2_pass",
                "hash",
                "rat_key",
                "email_password",
            )
        ]
        for secret in sorted(set(secrets), key=len, reverse=True):
            if len(secret) >= 6 and secret in masked:
                masked = masked.replace(secret, "***")
    except Exception:
        pass
    return masked


def _append(record: dict) -> None:
    """Append one record to the routing log. Never raises."""
    try:
        with _log_path().open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass


def infer_source(command: str, intent_text: str = "") -> str:
    """Classify where a resolved step likely came from.

    Args:
        command: Resolved shell command line.
        intent_text: Original intent summary.

    Returns:
        One of auto, cli, heuristic.
    """
    lowered = (intent_text or "").strip().lower()
    if lowered.startswith(("auto ", "lazy addon ", "custom tool ")):
        return "auto"
    head = (command or "").strip().split()[0] if (command or "").strip() else ""
    if head and lowered.split()[:1] == [head.lower()]:
        return "cli"
    try:
        from modules.lazy_cli_bridge import is_cli_verb

        if head and is_cli_verb(head):
            return "cli"
    except Exception:
        pass
    return "heuristic"


def describe_command(command: str) -> dict:
    """Describe a command with phase and risk. Never raises."""
    head = (command or "").strip().split()[0] if (command or "").strip() else ""
    phase = "other"
    risk = "safe"
    try:
        from modules.lazy_cli_bridge import phase_for, risk_for

        phase = phase_for(head)
        risk = risk_for(head)
    except Exception:
        pass
    return {"verb": head, "phase": phase, "risk": risk}


def record_routing_decision(
    task_id: str,
    intent_id: int,
    command: str,
    intent_text: str = "",
    target: str = "",
    stack: str = "",
) -> dict:
    """Record which verb the loop chose for one intent.

    Args:
        task_id: Loop task identifier.
        intent_id: Exploration node the command serves.
        command: Resolved shell command line.
        intent_text: Original intent summary for source inference.
        target: Bound target, if any.
        stack: Target stack fingerprint for cross-task priors.

    Returns:
        The stored record.
    """
    info = describe_command(command)
    record = {
        "ts": _now(),
        "kind": "decision",
        "task": str(task_id or ""),
        "intent": int(intent_id or 0),
        "command": _mask(str(command or "")[:500]),
        "verb": info["verb"],
        "source": infer_source(command, intent_text),
        "phase": info["phase"],
        "risk": info["risk"],
        "target": str(target or "")[:200],
        "stack": str(stack or "")[:200],
        "intent_text": _mask(str(intent_text or "")[:300]),
    }
    _append(record)
    return record


def record_routing_outcome(
    task_id: str,
    intent_id: int,
    command: str,
    state: str = "",
    facts: int = 0,
    findings: int = 0,
    stack: str = "",
) -> dict:
    """Record the terminal outcome of one executed command.

    Args:
        task_id: Loop task identifier.
        intent_id: Exploration node the command served.
        command: Executed shell command line.
        state: Terminal intent state (done, blocked, exhausted, stopped).
        facts: Facts persisted by the intent.
        findings: Findings reported by the intent.
        stack: Target stack fingerprint for cross-task priors.

    Returns:
        The stored record.
    """
    info = describe_command(command)
    record = {
        "ts": _now(),
        "kind": "outcome",
        "task": str(task_id or ""),
        "intent": int(intent_id or 0),
        "command": _mask(str(command or "")[:500]),
        "verb": info["verb"],
        "phase": info["phase"],
        "risk": info["risk"],
        "state": str(state or ""),
        "facts": int(facts or 0),
        "findings": int(findings or 0),
        "stack": str(stack or "")[:200],
    }
    _append(record)
    return record


def read_decisions(task_id: str = "", limit: int = 2000) -> list[dict]:
    """Read routing records, optionally filtered by task.

    Args:
        task_id: Only return records for this task when set.
        limit: Max records from the tail.

    Returns:
        Parsed record list, oldest first.
    """
    try:
        lines = _log_path().read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    out = []
    for line in lines[-max(1, int(limit or 2000)) :]:
        try:
            record = json.loads(line)
        except ValueError:
            continue
        if task_id and str(record.get("task", "")) != str(task_id):
            continue
        out.append(record)
    return out


def mask_configured(text: str) -> str:
    """Mask only operator-configured credential values in live text.

    Unlike :func:`_mask` (defense in depth for stored records), this keeps
    discovered loot (hashes, target creds) visible to the model — the loop
    needs them for cracking and reuse reasoning — while configured secrets
    never reach cloud backends. Mirrors the secret-patterns approach of
    only masking known-configured values in transit.
    """
    masked = str(text or "")
    try:
        from core.config import load_payload

        payload = load_payload() or {}
        secrets = [
            str(payload.get(key, "") or "")
            for key in (
                "start_pass",
                "password",
                "backdoor_password",
                "api_key",
                "c2_pass",
                "hash",
                "rat_key",
                "email_password",
            )
        ]
        for secret in sorted(set(secrets), key=len, reverse=True):
            if len(secret) >= 6 and secret in masked:
                masked = masked.replace(secret, "***")
    except Exception:
        pass
    return masked


def stack_signature(assets=None) -> str:
    """Fingerprint the target stack from service assets.

    Sorted service values joined short, so equal stacks share priors
    across engagements (the cross-task learning query) while unseen
    stacks fall back to global priors.

    Args:
        assets: Object exposing ``list("service")`` with ``.value``.

    Returns:
        Stack fingerprint, empty when unknowable. Never raises.
    """
    try:
        values = sorted({str(getattr(node, "value", "")) for node in assets.list("service")})
        return ",".join(v for v in values if v)[:200]
    except Exception:
        return ""


def _is_ip_literal(value: str) -> bool:
    """Return True when value parses as an IP literal."""
    try:
        import ipaddress

        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def fuse_routing_decisions(task_id: str = "") -> dict:
    """Fuse routing records into the world model as host notes.

    Only decisions bound to IP-literal targets write notes, so the world
    model gains per-host evidence of what the loop already tried. The
    intel and attack graphs rebuild from the world model, hence from
    these notes as well.

    Args:
        task_id: Fuse only this task when set, else everything recent.

    Returns:
        Summary with fused count. Never raises.
    """
    summary = {"fused": 0}
    try:
        records = [r for r in read_decisions(task_id) if r.get("kind") == "decision"]
        if not records:
            return summary
        from modules.world_model import get_world_model

        world = get_world_model()
        seen: set[tuple[str, str]] = set()
        for record in records[-500:]:
            target = str(record.get("target", "") or "")
            verb = str(record.get("verb", "") or "")
            if not target or not verb or not _is_ip_literal(target):
                continue
            key = (target, verb)
            if key in seen:
                continue
            seen.add(key)
            world.add_note(target, f"lazy loop routed {verb} [{record.get('phase', '')}/{record.get('source', '')}]")
            summary["fused"] += 1
    except Exception:
        pass
    return summary


def export_spans(task_id: str, out: str | Path | None = None) -> dict:
    """Export activity records as trace spans for observability.

    Maps the existing trace fields onto span semantics: ``task`` is the
    trace id, ``tool_use_id`` (or a synthetic ``kind:index`` id) is the
    span id, ``intent_id`` is the parent, and ``tool``/``result`` pairs
    sharing a ``tool_use_id`` join into one span with duration. Point
    records without a pair become single-event spans.

    Args:
        task_id: Loop task identifier.
        out: Destination path. Defaults to ``spans_<task>.jsonl``.

    Returns:
        Summary with spans written and destination. Never raises.
    """
    from modules.mediation import MediationDomains, resolve

    dest = Path(out) if out else STORE_DIR / f"spans_{task_id}.jsonl"
    summary = {"spans": 0, "dest": str(dest)}
    try:
        records = resolve(MediationDomains.INTEL).activity_records(str(task_id), 5000)
    except Exception:
        return summary
    starts: dict[str, dict] = {}
    spans = []
    for index, record in enumerate(records):
        tool_use_id = str(record.get("tool_use_id", "") or "")
        kind = str(record.get("kind", "") or "")
        if kind == "tool" and tool_use_id:
            starts[tool_use_id] = record
            continue
        if kind == "result" and tool_use_id and tool_use_id in starts:
            start = starts.pop(tool_use_id)
            spans.append(
                {
                    "trace_id": str(task_id),
                    "span_id": tool_use_id,
                    "parent_id": f"intent-{record.get('intent_id', 0)}",
                    "name": f"{record.get('worker', '')}:{str(start.get('text', ''))[:80]}",
                    "start": float(start.get("ts", 0.0) or 0.0),
                    "end": float(record.get("ts", 0.0) or 0.0),
                    "status": "error" if str(record.get("text", "")).startswith("execution failed:") else "ok",
                    "attributes": {
                        "worker": str(record.get("worker", "")),
                        "intent": int(record.get("intent_id", 0) or 0),
                    },
                }
            )
            continue
        spans.append(
            {
                "trace_id": str(task_id),
                "span_id": tool_use_id or f"{kind}:{index}",
                "parent_id": f"intent-{record.get('intent_id', 0)}",
                "name": f"{record.get('worker', '')}:{kind}",
                "start": float(record.get("ts", 0.0) or 0.0),
                "end": float(record.get("ts", 0.0) or 0.0),
                "status": "ok",
                "attributes": {
                    "worker": str(record.get("worker", "")),
                    "intent": int(record.get("intent_id", 0) or 0),
                    "text": _mask(str(record.get("text", ""))[:300]),
                },
            }
        )
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("w", encoding="utf-8") as handle:
            for span in spans:
                handle.write(json.dumps(span, ensure_ascii=False) + "\n")
        summary["spans"] = len(spans)
    except OSError:
        pass
    return summary


__all__ = [
    "describe_command",
    "export_spans",
    "fuse_routing_decisions",
    "infer_source",
    "mask_configured",
    "read_decisions",
    "record_routing_decision",
    "record_routing_outcome",
    "stack_signature",
]
