"""Target and lab preflight checks for autonomous loops and auto_pwn.

An autonomous loop that reports success against a target nobody can
reach is worse than a crash: the operator trusts a finished badge while
the gym was down all along. This module answers one question before any
round is spent — is the target actually up?

Two liveness sources, cheapest first:

1. Lab membership: when the target IP belongs to a known lab scenario
   (``modules.lab_runtime.LAB_SCENARIOS``), the authoritative state is
   the container state itself. A stopped or never-created lab container
   fails the run before a single command fires, with the exact recovery
   command in the reason.
2. TCP reachability: for non-lab targets a bounded parallel probe of
   common service ports answers whether anything at all listens there.

Never raises; every path returns a mapping. All docker and socket I/O
is injected so tests run without docker or a network.
"""

from __future__ import annotations

import socket
import time
from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor

PREFLIGHT_PROBE_PORTS: tuple[int, ...] = (
    21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445,
    1433, 3000, 3306, 3389, 5432, 8000, 8080, 8443, 9090,
)
PREFLIGHT_CONNECT_TIMEOUT_SEC = 1.5
PREFLIGHT_MAX_WORKERS = 24
NO_PREFLIGHT_HINT = "--no-preflight"


def lab_state_for(
    target: str,
    scenarios: Iterable[str] | None = None,
    running: list[str] | None = None,
    existing: list[str] | None = None,
    ip_lookup: Callable[[str], str] | None = None,
) -> dict:
    """Map a target IP to its lab scenario and container state.

    Args:
        target: Candidate IP address.
        scenarios: Scenario names to consider; defaults to every
            ``LAB_SCENARIOS`` key.
        running: Running container names override (tests).
        existing: All container names override (tests).
        ip_lookup: Container-name-to-IP resolver override (tests).

    Returns:
        ``{"scenario": name, "container": name, "ip": ip, "running": bool}``
        when the target matches a known lab container IP, else ``{}``.
    """
    from modules import lab_runtime

    names = list(scenarios or lab_runtime.LAB_SCENARIOS)
    lookup = ip_lookup or lab_runtime.container_ip
    running = running if running is not None else lab_runtime.running_containers()
    existing = existing if existing is not None else lab_runtime.existing_containers()
    for scenario in names:
        container = lab_runtime.container_name(scenario)
        if container not in existing:
            continue
        try:
            ip = str(lookup(container) or "")
        except Exception:
            continue
        if ip == str(target or "").strip():
            return {
                "scenario": scenario,
                "container": container,
                "ip": ip,
                "running": container in running,
            }
    return {}


def probe_tcp_detailed(
    target: str,
    ports: Iterable[int] | None = None,
    timeout: float | None = None,
) -> tuple[list[int], int]:
    """Probe TCP ports in parallel and classify the answers.

    A refused connection is evidence the host is alive (something
    answered with RST); a timeout means the port is filtered or the
    host is unreachable.

    Args:
        target: Host or IP to probe.
        ports: Port list override; defaults to ``PREFLIGHT_PROBE_PORTS``.
        timeout: Per-connect timeout override.

    Returns:
        Tuple (open ports sorted, refused count).
    """
    candidates = sorted({int(p) for p in (ports or PREFLIGHT_PROBE_PORTS) if int(p) > 0})
    window = max(1.0, float(timeout or PREFLIGHT_CONNECT_TIMEOUT_SEC))
    open_ports: list[int] = []
    refused = 0

    def _probe(port: int) -> tuple[int | None, bool]:
        try:
            with socket.create_connection((target, port), timeout=window):
                return port, False
        except ConnectionRefusedError:
            return None, True
        except OSError:
            return None, False

    with ThreadPoolExecutor(max_workers=min(PREFLIGHT_MAX_WORKERS, len(candidates))) as pool:
        for result, was_refused in pool.map(_probe, candidates):
            if result is not None:
                open_ports.append(result)
            elif was_refused:
                refused += 1
    return sorted(open_ports), refused


def probe_tcp(
    target: str,
    ports: Iterable[int] | None = None,
    timeout: float | None = None,
) -> list[int]:
    """Probe TCP ports in parallel and return the open ones.

    Args:
        target: Host or IP to probe.
        ports: Port list override; defaults to ``PREFLIGHT_PROBE_PORTS``.
        timeout: Per-connect timeout override.

    Returns:
        Sorted open port numbers; empty when nothing answers or the
        target cannot be resolved.
    """
    open_ports, _refused = probe_tcp_detailed(target, ports=ports, timeout=timeout)
    return open_ports


def check_target(
    target: str,
    ports: Iterable[int] | None = None,
    connect_timeout: float | None = None,
    lab: dict | None = None,
) -> dict:
    """Decide whether a loop may be spent against this target.

    Args:
        target: Target IP or hostname.
        ports: TCP probe ports override (non-lab targets).
        connect_timeout: TCP probe timeout override.
        lab: Precomputed lab state override (tests); when omitted the
            state is resolved live.

    Returns:
        ``{"ok": bool, "reason": str, "target": str, "lab": dict,
        "open_ports": list[int], "hint": str}``. ``ok`` is True only
        when a lab scenario for the target is running or at least one
        probed TCP port answers. ``hint`` carries the recovery command
        for lab scenarios that are down.
    """
    target_text = str(target or "").strip()
    base = {"target": target_text, "lab": {}, "open_ports": [], "ok": False, "reason": "", "hint": ""}
    if not target_text:
        base["reason"] = "no target configured"
        return base
    state = lab if lab is not None else lab_state_for(target_text)
    base["lab"] = state
    if state:
        scenario = str(state.get("scenario", ""))
        if state.get("running"):
            base["ok"] = True
            base["reason"] = f"lab scenario '{scenario}' is running ({state.get('container', '')})"
            return base
        base["reason"] = (
            f"lab scenario '{scenario}' is DOWN (container {state.get('container', '')} "
            "exists but is stopped) — the loop would burn every round against a dead target"
        )
        base["hint"] = f"lab start {scenario}"
        return base
    started = time.monotonic()
    open_ports, refused = probe_tcp_detailed(target_text, ports=ports, timeout=connect_timeout)
    elapsed = time.monotonic() - started
    probed_count = len(PREFLIGHT_PROBE_PORTS if ports is None else list(ports))
    base["open_ports"] = open_ports
    if open_ports:
        base["ok"] = True
        base["reason"] = f"{len(open_ports)} TCP service(s) answered in {elapsed:.1f}s"
        return base
    if refused:
        base["ok"] = True
        base["reason"] = (
            f"host alive: {refused}/{probed_count} probed ports answered refused in {elapsed:.1f}s "
            "(no service on the probed set, but the target answers)"
        )
        return base
    base["reason"] = (
        f"no TCP service answered on {target_text} (probed "
        f"{probed_count} ports in {elapsed:.1f}s) "
        "— target is down or fully filtered; the loop would finish without touching it"
    )
    base["hint"] = NO_PREFLIGHT_HINT
    return base


def recovery_hint(outcome: dict) -> str:
    """Return the operator-facing recovery line for a failed preflight."""
    hint = str(outcome.get("hint", "") or "")
    if not hint:
        return ""
    if hint == NO_PREFLIGHT_HINT:
        return f"override with {NO_PREFLIGHT_HINT} (explicit operator consent)"
    return f"recover with: {hint}"


__all__ = [
    "NO_PREFLIGHT_HINT",
    "PREFLIGHT_CONNECT_TIMEOUT_SEC",
    "PREFLIGHT_MAX_WORKERS",
    "PREFLIGHT_PROBE_PORTS",
    "check_target",
    "lab_state_for",
    "probe_tcp",
    "recovery_hint",
]
