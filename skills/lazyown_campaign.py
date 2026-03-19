#!/usr/bin/env python3
"""
LazyOwn CampaignStore
=====================
Groups multiple targets under a single named penetration-test engagement.

A *campaign* tracks:
  - A human-readable engagement name  (e.g. "HTB-Mirage", "Client-ACME-2026")
  - Scope: CIDR ranges / individual IPs that are authorised for testing
  - Per-host attack phase  (recon → scan → exploit → post-exploit → complete)
  - Milestones achieved during the engagement  (initial_foothold, priv_esc, …)
  - Start / end timestamps  and freeform notes

Persistence: sessions/campaign.json  (one active campaign at a time)

Usage
-----
  python3 skills/lazyown_campaign.py new "HTB-Mirage" --scope 10.10.11.0/24
  python3 skills/lazyown_campaign.py status
  python3 skills/lazyown_campaign.py phase 10.10.11.78 exploit
  python3 skills/lazyown_campaign.py milestone 10.10.11.78 initial_foothold --notes "via evil-winrm"
  python3 skills/lazyown_campaign.py complete
  python3 skills/lazyown_campaign.py add-scope 10.10.10.5
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import logging
import os
import secrets
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

# ─── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("lazyown.campaign")

# ─── Paths ────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
CAMPAIGN_FILE = SESSIONS_DIR / "campaign.json"


# ─── Helper ───────────────────────────────────────────────────────────────────


def _now_iso() -> str:
    """Return current UTC time as an ISO-8601 string (no microseconds)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def is_ip_in_scope(ip: str, scope: List[str]) -> bool:
    """Return True if *ip* belongs to any entry in *scope*.

    Each scope entry is tried as an ipaddress network first; if that fails
    the function falls back to a simple string-prefix comparison so that
    hostnames stored as plain strings (e.g. "api.acme.com") also match.

    Parameters
    ----------
    ip:
        The IP address (or hostname) to test.
    scope:
        A list of CIDR strings (``10.10.11.0/24``) or individual addresses /
        hostnames (``10.10.10.5``, ``api.acme.com``).
    """
    for entry in scope:
        try:
            network = ipaddress.ip_network(entry, strict=False)
            try:
                addr = ipaddress.ip_address(ip)
                if addr in network:
                    return True
                continue
            except ValueError:
                # ip is not a numeric address — fall through to prefix match
                pass
        except ValueError:
            # entry is not a valid network — try prefix / exact match below
            pass

        # Fallback: simple prefix or exact match (covers hostnames)
        if ip == entry or ip.startswith(entry.rstrip(".*")):
            return True

    return False


# ─── Data model ───────────────────────────────────────────────────────────────


@dataclass
class Campaign:
    """Represents a single penetration-test engagement.

    Attributes
    ----------
    campaign_id:
        8-character lowercase hex identifier generated at creation time.
    name:
        Human-readable engagement label (e.g. ``"HTB-Mirage"``).
    scope:
        List of CIDR ranges or individual IPs / hostnames in scope.
    started_at:
        ISO-8601 timestamp (UTC) of when the campaign was created.
    ended_at:
        ISO-8601 timestamp when the campaign was completed, or ``""`` if
        still active.
    phase_per_host:
        Mapping of ``ip → phase``.  Known phases (not enforced):
        ``recon``, ``scan``, ``exploit``, ``post-exploit``, ``complete``.
    milestones:
        Ordered list of milestone dicts::

            {
                "host":      "10.10.11.78",
                "type":      "initial_foothold",
                "timestamp": "2026-03-19T14:00:00Z",
                "notes":     "via evil-winrm"
            }
    notes:
        Freeform engagement notes (operator journal).
    """

    campaign_id: str
    name: str
    scope: List[str]
    started_at: str
    ended_at: str
    phase_per_host: Dict[str, str]
    milestones: List[Dict]
    notes: str

    # ── convenience ──────────────────────────────────────────────────────────

    def is_active(self) -> bool:
        """Return True when the campaign has not been completed yet."""
        return self.ended_at == ""

    def to_dict(self) -> dict:
        """Serialise to a plain dict suitable for JSON persistence."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Campaign":
        """Deserialise from a dict loaded out of JSON."""
        return cls(
            campaign_id=data["campaign_id"],
            name=data["name"],
            scope=data.get("scope", []),
            started_at=data.get("started_at", ""),
            ended_at=data.get("ended_at", ""),
            phase_per_host=data.get("phase_per_host", {}),
            milestones=data.get("milestones", []),
            notes=data.get("notes", ""),
        )


# ─── Store ────────────────────────────────────────────────────────────────────


class CampaignStore:
    """Thin persistence layer around :class:`Campaign`.

    All mutating methods immediately flush changes to
    ``sessions/campaign.json``.
    """

    def __init__(self, campaign_file: Path = CAMPAIGN_FILE) -> None:
        self._file = campaign_file
        self._file.parent.mkdir(parents=True, exist_ok=True)

    # ── I/O ──────────────────────────────────────────────────────────────────

    def _save(self, campaign: Campaign) -> None:
        """Persist *campaign* to disk (atomic write via temp-then-rename)."""
        tmp = self._file.with_suffix(".tmp")
        tmp.write_text(json.dumps(campaign.to_dict(), indent=2), encoding="utf-8")
        tmp.replace(self._file)
        log.debug("Campaign saved → %s", self._file)

    def load(self) -> Optional[Campaign]:
        """Load the current campaign from disk.

        Returns
        -------
        Campaign | None
            The campaign if the file exists and is valid JSON, else ``None``.
        """
        if not self._file.exists():
            return None
        try:
            data = json.loads(self._file.read_text(encoding="utf-8"))
            return Campaign.from_dict(data)
        except (json.JSONDecodeError, KeyError) as exc:
            log.warning("Could not load campaign file: %s", exc)
            return None

    # ── Lifecycle ────────────────────────────────────────────────────────────

    def create(self, name: str, scope: List[str], notes: str = "") -> Campaign:
        """Create and persist a brand-new campaign.

        Parameters
        ----------
        name:
            Human-readable engagement label.
        scope:
            Initial list of CIDR ranges / IPs / hostnames.
        notes:
            Optional freeform notes to attach at creation time.

        Returns
        -------
        Campaign
            The newly created (and saved) campaign.
        """
        campaign = Campaign(
            campaign_id=secrets.token_hex(4),  # 8-char hex
            name=name,
            scope=list(scope),
            started_at=_now_iso(),
            ended_at="",
            phase_per_host={},
            milestones=[],
            notes=notes,
        )
        self._save(campaign)
        log.info("Campaign '%s' created  [id=%s]", name, campaign.campaign_id)
        return campaign

    def complete(self, notes: str = "") -> None:
        """Mark the active campaign as completed.

        Parameters
        ----------
        notes:
            Optional closing notes to append to the campaign's notes field.

        Raises
        ------
        FileNotFoundError
            If no campaign file exists.
        ValueError
            If the campaign was already completed.
        """
        campaign = self._require()
        if not campaign.is_active():
            raise ValueError(f"Campaign '{campaign.name}' is already completed.")
        campaign.ended_at = _now_iso()
        if notes:
            sep = "\n" if campaign.notes else ""
            campaign.notes += sep + notes
        self._save(campaign)
        log.info("Campaign '%s' completed at %s", campaign.name, campaign.ended_at)

    # ── Mutations ────────────────────────────────────────────────────────────

    def update_phase(self, host: str, phase: str) -> None:
        """Set (or update) the attack phase for *host*.

        Parameters
        ----------
        host:
            Target IP address or hostname.
        phase:
            Phase label (e.g. ``"recon"``, ``"exploit"``).
        """
        campaign = self._require()
        old = campaign.phase_per_host.get(host, "<none>")
        campaign.phase_per_host[host] = phase
        self._save(campaign)
        log.info("Phase for %s: %s → %s", host, old, phase)

    def add_milestone(
        self, host: str, milestone_type: str, notes: str = ""
    ) -> None:
        """Record a milestone achievement for *host*.

        Parameters
        ----------
        host:
            Target IP / hostname this milestone applies to.
        milestone_type:
            Short label such as ``"initial_foothold"``, ``"priv_esc"``,
            ``"data_exfil"``, ``"lateral_movement"``.
        notes:
            Optional freeform description of how the milestone was reached.
        """
        campaign = self._require()
        milestone: Dict = {
            "host": host,
            "type": milestone_type,
            "timestamp": _now_iso(),
            "notes": notes,
        }
        campaign.milestones.append(milestone)
        self._save(campaign)
        log.info("Milestone '%s' added for %s", milestone_type, host)

    def add_to_scope(self, ip_or_cidr: str) -> None:
        """Append *ip_or_cidr* to the campaign scope (idempotent).

        Parameters
        ----------
        ip_or_cidr:
            A CIDR range (``10.10.10.0/24``) or individual address /
            hostname to add.
        """
        campaign = self._require()
        if ip_or_cidr in campaign.scope:
            log.info("%s is already in scope — skipped", ip_or_cidr)
            return
        campaign.scope.append(ip_or_cidr)
        self._save(campaign)
        log.info("Added to scope: %s", ip_or_cidr)

    # ── Queries ──────────────────────────────────────────────────────────────

    def in_scope(self, ip: str) -> bool:
        """Return True if *ip* falls within the campaign scope."""
        campaign = self.load()
        if campaign is None:
            return False
        return is_ip_in_scope(ip, campaign.scope)

    def summary(self) -> str:
        """Return a human-readable multi-line summary of the campaign."""
        campaign = self.load()
        if campaign is None:
            return "No active campaign found.  Run: lazyown_campaign.py new <name>"

        status = "ACTIVE" if campaign.is_active() else f"COMPLETED at {campaign.ended_at}"
        lines = [
            "=" * 60,
            f"  Campaign : {campaign.name}  [{campaign.campaign_id}]",
            f"  Status   : {status}",
            f"  Started  : {campaign.started_at}",
            f"  Scope    : {', '.join(campaign.scope) or '(none)'}",
            "-" * 60,
        ]

        if campaign.phase_per_host:
            lines.append("  Host phases:")
            for host, phase in sorted(campaign.phase_per_host.items()):
                lines.append(f"    {host:<20} {phase}")
        else:
            lines.append("  Host phases: (none recorded)")

        lines.append("-" * 60)

        if campaign.milestones:
            lines.append(f"  Milestones ({len(campaign.milestones)}):")
            for ms in campaign.milestones:
                note_suffix = f"  # {ms['notes']}" if ms.get("notes") else ""
                lines.append(
                    f"    [{ms['timestamp']}] {ms['host']} → {ms['type']}{note_suffix}"
                )
        else:
            lines.append("  Milestones: (none recorded)")

        if campaign.notes:
            lines.append("-" * 60)
            lines.append("  Notes:")
            for note_line in campaign.notes.splitlines():
                lines.append(f"    {note_line}")

        lines.append("=" * 60)
        return "\n".join(lines)

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _require(self) -> Campaign:
        """Load the campaign or raise FileNotFoundError."""
        campaign = self.load()
        if campaign is None:
            raise FileNotFoundError(
                "No campaign file found at %s.  "
                "Create one with: lazyown_campaign.py new <name>" % self._file
            )
        return campaign


# ─── CLI ──────────────────────────────────────────────────────────────────────


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lazyown_campaign.py",
        description="Manage LazyOwn penetration-test campaigns.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # new
    p_new = sub.add_parser("new", help="Create a new campaign.")
    p_new.add_argument("name", help='Engagement name, e.g. "HTB-Mirage".')
    p_new.add_argument(
        "--scope",
        action="append",
        default=[],
        metavar="CIDR",
        help="Add a CIDR range / IP to scope (repeatable).",
    )
    p_new.add_argument("--notes", default="", help="Initial campaign notes.")

    # status
    sub.add_parser("status", help="Print campaign summary.")

    # phase
    p_phase = sub.add_parser("phase", help="Set the attack phase for a host.")
    p_phase.add_argument("host", help="Target IP / hostname.")
    p_phase.add_argument("phase", help="Phase label (recon, scan, exploit, …).")

    # milestone
    p_ms = sub.add_parser("milestone", help="Record a milestone for a host.")
    p_ms.add_argument("host", help="Target IP / hostname.")
    p_ms.add_argument("type", help="Milestone type (initial_foothold, priv_esc, …).")
    p_ms.add_argument("--notes", default="", help="How the milestone was reached.")

    # complete
    p_done = sub.add_parser("complete", help="Mark the campaign as completed.")
    p_done.add_argument("--notes", default="", help="Closing notes.")

    # add-scope
    p_scope = sub.add_parser("add-scope", help="Add an IP / CIDR to campaign scope.")
    p_scope.add_argument("ip_or_cidr", help="IP address or CIDR range to add.")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    store = CampaignStore()

    try:
        if args.command == "new":
            c = store.create(name=args.name, scope=args.scope, notes=args.notes)
            print(f"Campaign '{c.name}' created  [id={c.campaign_id}]")
            print(f"Saved to: {CAMPAIGN_FILE}")

        elif args.command == "status":
            print(store.summary())

        elif args.command == "phase":
            store.update_phase(args.host, args.phase)
            print(f"Phase updated: {args.host} → {args.phase}")

        elif args.command == "milestone":
            store.add_milestone(args.host, args.type, notes=args.notes)
            print(f"Milestone '{args.type}' recorded for {args.host}")

        elif args.command == "complete":
            store.complete(notes=args.notes)
            print("Campaign marked as completed.")

        elif args.command == "add-scope":
            store.add_to_scope(args.ip_or_cidr)
            print(f"Scope updated — added: {args.ip_or_cidr}")

    except (FileNotFoundError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
