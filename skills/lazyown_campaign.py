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
from typing import Any, Dict, List, Optional

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


# ─── Episode reflection ───────────────────────────────────────────────────────


@dataclass
class LessonLearned:
    """A single distilled lesson extracted from a completed campaign.

    Stored in hive memory (ChromaDB) so future campaigns can retrieve
    relevant lessons via semantic search.
    """

    campaign_id:   str
    campaign_name: str
    topic:         str   # e.g. "privesc", "lateral_movement", "detection_evasion"
    lesson:        str   # the actionable insight
    context:       str   # brief context that produced this lesson
    derived_at:    str   = field(default_factory=_now_iso)

    def to_dict(self) -> dict:
        return asdict(self)


class EpisodeReflectionEngine:
    """
    Post-campaign reflection engine.

    After a campaign completes, analyses milestones and notes to produce
    a set of LessonLearned records and persists them to:
      1. sessions/campaign_lessons.jsonl  — local flat file for offline review
      2. hive_memory (ChromaDB / SQLite)  — for semantic retrieval in future campaigns

    Design
    ------
    - Single Responsibility : reflection + lesson extraction only
    - Open/Closed           : lesson extractors added as _EXTRACTORS entries
    - Dependency Inversion  : hive memory injected (or None for offline mode)

    The lesson extraction is intentionally heuristic and conservative — it
    only produces lessons from concrete observed milestones, not from
    speculative reasoning.
    """

    _LESSONS_FILE = BASE_DIR / "sessions" / "campaign_lessons.jsonl"

    # Maps milestone type to a lesson topic and template function
    _MILESTONE_LESSONS: Dict[str, tuple] = {
        "initial_foothold": (
            "intrusion",
            lambda m: (
                f"Initial foothold on {m['host']} achieved at {m['timestamp']}. "
                f"Method: {m.get('notes', 'not recorded')}. "
                "Capture the exact service version and auth mechanism for future reference."
            ),
        ),
        "priv_esc": (
            "privesc",
            lambda m: (
                f"Privilege escalation on {m['host']}: {m.get('notes', 'method not recorded')}. "
                "Verify whether the same path exists on other hosts in the same subnet."
            ),
        ),
        "lateral_movement": (
            "lateral_movement",
            lambda m: (
                f"Lateral movement to {m['host']}: {m.get('notes', 'not recorded')}. "
                "Record which credential enabled this move for future pass-the-hash attempts."
            ),
        ),
        "data_exfil": (
            "exfiltration",
            lambda m: (
                f"Data exfiltration from {m['host']}: {m.get('notes', 'not recorded')}. "
                "Note the channel used and whether it triggered any IDS alert."
            ),
        ),
        "credential_dump": (
            "credential_access",
            lambda m: (
                f"Credential dump on {m['host']}: {m.get('notes', 'not recorded')}. "
                "Store hashes in sessions/ for offline cracking; "
                "attempt pass-the-hash before cracking."
            ),
        ),
    }

    def __init__(self, hive_memory: Optional[Any] = None) -> None:
        """
        Parameters
        ----------
        hive_memory:
            Optional HiveMemory instance for semantic storage.
            When None, lessons are only written to the flat JSONL file.
        """
        self._hive_memory = hive_memory
        self._lessons_file = self._LESSONS_FILE
        self._lessons_file.parent.mkdir(parents=True, exist_ok=True)

    def reflect(self, campaign: "Campaign") -> List[LessonLearned]:
        """
        Extract lessons from *campaign* and persist them.

        Returns the list of LessonLearned records produced.
        """
        lessons: List[LessonLearned] = []

        # Lesson per concrete milestone
        for milestone in campaign.milestones:
            mtype = milestone.get("type", "")
            if mtype in self._MILESTONE_LESSONS:
                topic, template_fn = self._MILESTONE_LESSONS[mtype]
                try:
                    lesson_text = template_fn(milestone)
                except Exception:
                    lesson_text = f"Milestone '{mtype}' achieved on {milestone.get('host', '?')}."
                lessons.append(LessonLearned(
                    campaign_id=campaign.campaign_id,
                    campaign_name=campaign.name,
                    topic=topic,
                    lesson=lesson_text,
                    context=f"milestone:{mtype} host:{milestone.get('host', '?')}",
                ))

        # Aggregate lesson: scope coverage
        completed_hosts = [
            h for h, phase in campaign.phase_per_host.items()
            if phase == "complete"
        ]
        if completed_hosts:
            lessons.append(LessonLearned(
                campaign_id=campaign.campaign_id,
                campaign_name=campaign.name,
                topic="scope_coverage",
                lesson=(
                    f"Campaign '{campaign.name}' fully pwned "
                    f"{len(completed_hosts)}/{len(campaign.scope)} scoped targets: "
                    f"{', '.join(completed_hosts)}. "
                    "Review which hosts were never exploited and why."
                ),
                context="aggregate:scope_coverage",
            ))

        # Duration lesson
        if campaign.started_at and campaign.ended_at:
            lessons.append(LessonLearned(
                campaign_id=campaign.campaign_id,
                campaign_name=campaign.name,
                topic="campaign_duration",
                lesson=(
                    f"Campaign ran from {campaign.started_at} to {campaign.ended_at}. "
                    f"Total milestones: {len(campaign.milestones)}. "
                    "Review timeline gaps to identify enumeration bottlenecks."
                ),
                context="aggregate:duration",
            ))

        self._persist_lessons(lessons)
        return lessons

    def _persist_lessons(self, lessons: List[LessonLearned]) -> None:
        """Write lessons to the flat JSONL file and to hive memory."""
        with self._lessons_file.open("a", encoding="utf-8") as fh:
            for lesson in lessons:
                fh.write(json.dumps(lesson.to_dict()) + "\n")
        log.info("EpisodeReflectionEngine: %d lessons written to %s",
                 len(lessons), self._lessons_file)

        if self._hive_memory is not None:
            for lesson in lessons:
                try:
                    self._hive_memory.store(
                        content=(
                            f"[LESSON] campaign={lesson.campaign_name} "
                            f"topic={lesson.topic}\n{lesson.lesson}"
                        ),
                        agent_id="reflection_engine",
                        role="architect",
                        event_type="lesson_learned",
                        meta={
                            "campaign_id":   lesson.campaign_id,
                            "campaign_name": lesson.campaign_name,
                            "topic":         lesson.topic,
                        },
                    )
                except Exception as exc:
                    log.debug("EpisodeReflectionEngine: hive store error: %s", exc)


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

    def complete(
        self,
        notes: str = "",
        run_reflection: bool = True,
        hive_memory: Optional[Any] = None,
    ) -> List[LessonLearned]:
        """Mark the active campaign as completed and optionally run reflection.

        Parameters
        ----------
        notes:
            Optional closing notes to append to the campaign's notes field.
        run_reflection:
            When True (default), run EpisodeReflectionEngine after marking
            completion to extract and persist lessons learned.
        hive_memory:
            Optional HiveMemory instance for semantic lesson storage.
            Only used when run_reflection=True.

        Returns
        -------
        List[LessonLearned]
            The lessons extracted (empty list when run_reflection=False).

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

        if run_reflection:
            engine = EpisodeReflectionEngine(hive_memory=hive_memory)
            lessons = engine.reflect(campaign)
            log.info(
                "Episode reflection: %d lessons extracted for campaign '%s'",
                len(lessons),
                campaign.name,
            )
            return lessons

        return []

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
            lessons = store.complete(notes=args.notes, run_reflection=True)
            print("Campaign marked as completed.")
            if lessons:
                print(f"\nEpisode reflection: {len(lessons)} lesson(s) extracted.")
                for ls in lessons:
                    print(f"  [{ls.topic}] {ls.lesson[:120]}")
                print(f"\nFull lessons saved to: {EpisodeReflectionEngine._LESSONS_FILE}")

        elif args.command == "add-scope":
            store.add_to_scope(args.ip_or_cidr)
            print(f"Scope updated — added: {args.ip_or_cidr}")

    except (FileNotFoundError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
