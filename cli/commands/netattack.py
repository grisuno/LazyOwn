"""Windows network-attack surface command set: plan, attest, show.

``lazy_netattack`` grades the observed surface from the world model and
attested SMB-signing evidence, prints the exact operator-executed commands
and records operator attestations. It never launches poisoning, WPAD MITM
or NTLM relay: those run on the operator's listening interface and stay
operator-gated. The loop's ``ad_surface`` trigger consumes the same pure
decision from :mod:`modules.lazy_netattack` and turns viable grades into
hint nodes.
"""

from __future__ import annotations

import json
import shlex
from pathlib import Path

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import print_error, print_msg, print_warn


def _signing_evidence_path() -> Path:
    """Return the canonical sessions path for attested signing evidence."""
    return Path("sessions") / "smb_signing.json"


def _world_evidence() -> tuple[dict[str, dict[str, dict]], dict[str, str]]:
    """Read service and OS evidence from the live world model."""
    host_services: dict[str, dict[str, dict]] = {}
    os_hints: dict[str, str] = {}
    try:
        from modules.world_model import get_world_model

        world = get_world_model().snapshot()
        for ip, host in (world.get("hosts", {}) or {}).items():
            if not isinstance(host, dict):
                continue
            os_hints[str(ip)] = str(host.get("os_hint", "") or "")
            for port, svc in (host.get("services", {}) or {}).items():
                svc = svc if isinstance(svc, dict) else {"name": str(svc)}
                host_services.setdefault(str(ip), {})[str(port)] = {
                    "name": str(svc.get("name", "")),
                    "version": str(svc.get("version", "") or ""),
                }
    except Exception as exc:
        print_warn(f"world model unavailable ({exc}); plan degrades to an empty surface")
    return host_services, os_hints


class NetAttackCommandSet(LazyOwnCommandSet):
    """Windows net-attack surface: evidence-shaped plan, operator consent."""

    phase = "enum"
    category = "exploitation"

    @cmd2.with_category("exploitation")
    def do_lazy_netattack(self, line: str) -> None:
        """Windows net-attack surface: grade + exact commands; never executes.

        Usage:
            lazy_netattack plan [target]
            lazy_netattack attest <host> <ok|off> [note]
            lazy_netattack show
        """
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error("Usage: lazy_netattack plan [target] | attest <host> <ok|off> | show")
            return
        action = args[0].lower()
        if action == "attest" and len(args) >= 3:
            self._attest(args)
            return
        if action == "show":
            self._show_attestations()
            return
        if action != "plan":
            print_error("Usage: lazy_netattack plan [target] | attest <host> <ok|off> | show")
            return
        self._plan(args[1] if len(args) > 1 else "")

    def _attest(self, args: list[str]) -> None:
        """Record operator-attested signing status for one host."""
        host = args[1]
        state = args[2].lower()
        if state not in ("ok", "off"):
            print_error("state must be 'ok' (signing required) or 'off' (signing not required)")
            return
        note = " ".join(args[3:])[:200]
        path = _signing_evidence_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        payload: dict = {}
        if path.is_file():
            try:
                payload = dict(json.loads(path.read_text(encoding="utf-8", errors="replace") or "{}"))
            except Exception:
                payload = {}
        payload[host] = f"operator attestation: signing {state} {note}".strip()
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print_msg(f"[+] signing attested for {host}: {state} -> {path}")

    def _show_attestations(self) -> None:
        """Print current operator attestations."""
        path = _signing_evidence_path()
        if not path.is_file():
            print_msg("no signing attestations; run: lazy_netattack plan / gym surface probe first")
            return
        try:
            print_msg(str(json.dumps(json.loads(path.read_text(encoding="utf-8")), indent=2)))
        except Exception as exc:
            print_error(f"signing evidence unreadable: {exc}")

    def _plan(self, target: str) -> None:
        """Render the family verdicts and operator commands."""
        host_services, os_hints = _world_evidence()
        if target and target not in host_services:
            host_services.setdefault(target, {})
            os_hints.setdefault(target, "")
            for ip in list(host_services):
                if ip != target and ip.split(".")[:2] == target.split(".")[:2] and not host_services[target]:
                    host_services[target] = host_services[ip]
                    os_hints[target] = os_hints.get(ip, "")
                    break
        from modules import lazy_netattack
        from modules.loop_triggers import read_signing_evidence

        evidence = lazy_netattack.SurfaceEvidence(
            services=host_services,
            os_hints=os_hints,
            signing=read_signing_evidence(),
            lm_compat={},
        )
        decisions = lazy_netattack.surface_decision(evidence)
        actionable = [row for row in decisions.values() if row.verdict != "blocked"]
        if not actionable:
            print_warn("no Windows attack surface observed in the world model; scan the target first")
            return
        print_msg("[netattack] plan (kinetic steps NEVER auto-run; operator executes):")
        for row in actionable:
            print_msg(f"  {row.family} [{row.verdict}] targets={','.join(row.targets[:4]) or 'n/a'}")
            for reason in row.reasons[:2]:
                print_msg(f"    reason: {reason[:140]}")
            for missing in row.missing:
                print_warn(f"    missing: {missing[:180]}")
            for command in row.commands[:4]:
                rendered = (
                    command.replace("{target}", target or "{target}")
                    .replace("{smb_port}", "445")
                    .replace("{ldap_port}", "389")
                )
                print_msg(f"    cmd: {rendered[:240]}")
