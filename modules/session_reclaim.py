"""Audited cleanup planner for the top-level ``sessions`` directory.

The legacy ``clean`` command deleted everything in ``sessions`` that was not
in a short hardcoded allow list. That list predated most of the durable state
the framework now keeps there, so the command silently destroyed secrets
(``api_keys.json``, ``.secret_key``, ``team_ca.*``, ``rbac.db``), the canonical
operator persona (``soul.md``), captured loot and the encrypted world model.

This module replaces the flat allow list with an auditable three-tier plan:

``protected``
    Never removed. Scaffolding seeded into ``sessions`` (payload builders,
    wordlists), long-lived secrets and operator identity, and the canonical
    persona file. Losing any of these breaks the framework or the engagement.

``sensitive``
    Engagement loot, evidence, findings, reports, operator notes and the
    campaign memory. Deletable, but only when the operator explicitly opts in,
    so a routine reset never discards proof of work.

``reclaim``
    Per-engagement noise that a reset is meant to clear: scans, transcripts,
    atomic runs, loop state, implant builds, logs, caches and the C2 traffic
    archive.

``build_plan`` is pure and side-effect free so it can drive a dry-run preview.
``remove_entries`` performs the deletion in-process (no shell), escaping
control characters when a crafted filename is displayed.
"""

from __future__ import annotations

import os
import re
import shutil
import unicodedata
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from fnmatch import fnmatch

SESSIONS_DIRNAME = "sessions"

TIER_PROTECTED = "protected"
TIER_SENSITIVE = "sensitive"
TIER_RECLAIM = "reclaim"

_BYTE_UNITS = ("B", "K", "M", "G", "T", "P")
_BYTE_STEP = 1024
_RECLAIM_FALLBACK_LABEL = "Other campaign artifacts"
_TARGET_DIR_RE = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
_CONTROL_CATEGORY_PREFIX = "C"

PROTECTED_NAMES = frozenset(
    {
        "c",
        "implant",
        "lin",
        "win",
        "php",
        "download_resources.sh",
        "routes_to_templates.json",
        "sslscan-singleip.sh",
        "tor.sh",
        "www.py",
        "nmap-bootstrap.xsl",
        "payloads.txt",
        "users.txt",
        "ip2asn-v4.tsv.gz",
        "phishing",
        "uploads",
        "temp_uploads",
        "operators",
        "api_keys.json",
        "permissions.json",
        "rbac.db",
        "team_ca.key",
        "team_ca.pem",
        "key.aes",
        ".secret_key",
        ".auto_crypto_salt",
        "soul.md",
    }
)

EMPTY_ONLY_DIRS = frozenset({"logs"})

SUBSET_PATTERNS = {
    "nmap": ("scan*",),
    "test": ("test*", "ltest*", "*testimpl*"),
    "log": ("logs", "*.log"),
}


def _glob_matcher(*patterns: str) -> Callable[[str], bool]:
    """Return a predicate that is true when a name matches any glob pattern."""

    def _match(name: str) -> bool:
        return any(fnmatch(name, pattern) for pattern in patterns)

    return _match


def _target_dir_matcher(name: str) -> bool:
    """Return true when a name looks like a per-target working directory."""
    return bool(_TARGET_DIR_RE.match(name))


@dataclass(frozen=True)
class _Rule:
    """A display label bound to a name predicate."""

    label: str
    matches: Callable[[str], bool]


SENSITIVE_RULES: tuple[_Rule, ...] = (
    _Rule(
        "Captured credentials and hashes",
        _glob_matcher("credentials*", "*cred*", "hash*", "lazycreds*"),
    ),
    _Rule(
        "Evidence, findings and loot",
        _glob_matcher(
            "evidence",
            "findings",
            "loot",
            "captured_images",
            "ctf",
            "intel_*",
            "lazy_intel_*",
        ),
    ),
    _Rule(
        "Campaign memory",
        _glob_matcher("world_model.json", "world_model.json.*", "campaign_lessons*"),
    ),
    _Rule(
        "Engagement records",
        _glob_matcher("engagements", "operations", "default_engagement", "engagement_*"),
    ),
    _Rule("Operator notes", _glob_matcher("notes.txt", "plan.txt")),
)

RECLAIM_RULES: tuple[_Rule, ...] = (
    _Rule(
        "Generated reports, plans and digests",
        _glob_matcher(
            "reports",
            "report_*",
            "recon_plan_*",
            "digest_*",
            "killchain_*.html",
            "pentest_*",
            "*.md",
            "*.html",
        ),
    ),
    _Rule("C2 traffic archive", _glob_matcher("traffic")),
    _Rule(
        "Knowledge caches and vector DB",
        _glob_matcher(
            "chromadb",
            "cve_feed",
            "cve_cache",
            "detection_cache",
            "osint_cache.json",
            "rag_state.json",
            "keyword_fallback_index.json",
        ),
    ),
    _Rule(
        "Scans and recon",
        _glob_matcher(
            "scan*",
            "recon*",
            "hosts*",
            "k8s_scan*",
            "docker_enum*",
            "surface*",
            "attack_*",
            "graph.*",
        ),
    ),
    _Rule(
        "Transcripts and TTP traces",
        _glob_matcher(
            "transcript*",
            "ttpscope*",
            "ttp_*",
            "worker_traces*",
            "timeline*",
        ),
    ),
    _Rule(
        "Atomic and emulation runs",
        _glob_matcher("atomic*", "emulate*", "purple*"),
    ),
    _Rule(
        "Autonomous loop state",
        _glob_matcher(
            "loop*",
            "loops",
            "retry",
            "continuations",
            "chain*",
            "intents.jsonl",
            "decisions.jsonl",
            "outcomes.jsonl",
            "objectives.jsonl",
            "tasks.json",
            "autonomous_*",
            "policy_*",
            "rl_*",
            "expert_*",
            "metrics.jsonl",
        ),
    ),
    _Rule(
        "Implant and beacon builds",
        _glob_matcher(
            "implant_config_*",
            "l_*",
            "*.exe",
            "*.go",
            "*.so",
            "*.so.*",
            "*.dll",
            "*.o",
            "*.syso",
            "*.bat",
            "*.hta",
            "stub*",
            "beacon*",
            "loader_*",
            "main.go",
            "linux*",
            "ms2implant*",
            "no_priv*",
            "monrev*",
            "ld-linux*",
            "libc*",
            "whoami*",
            "theone",
            "server",
            "b.c",
            "mr*.c",
            "rootkit_*",
        ),
    ),
    _Rule(
        "Session and bridge state",
        _glob_matcher(
            "session_*.json",
            "sessionLazyOwn.json",
            "session_state.json",
            "cli_session.json",
            "lazy_bridge_*",
            "lazy_*",
            "listener*",
            "redirectors.json",
            "c2_*",
            "cmd_*",
            "banners.json",
            "notifications*",
            "conditional_hooks.json",
            "permissions_audit.jsonl",
            "config_changes*",
            "decisions*",
            "detection_feedback*",
            "evasion_profiles*",
            "events.jsonl",
            "finding_lifecycle.json",
            "exploit_recommendations.json",
            "cves.json",
        ),
    ),
    _Rule("Logs", _glob_matcher("logs", "*.log", "access.log", "out.txt")),
    _Rule("Target working directories", _target_dir_matcher),
)


@dataclass(frozen=True)
class CleanupEntry:
    """A single top-level item under ``sessions`` with its cleanup verdict."""

    name: str
    path: str
    size_bytes: int
    is_dir: bool
    tier: str
    label: str
    empty_only: bool = False

    @property
    def display_name(self) -> str:
        """Return the entry name with control characters escaped for the terminal."""
        return safe_label(self.name) + ("/" if self.is_dir else "")


@dataclass
class CleanupPlan:
    """The audited partition of ``sessions`` into protected, sensitive and reclaim."""

    sessions_dir: str
    subset: str | None = None
    entries: list[CleanupEntry] = field(default_factory=list)

    def by_tier(self, tier: str) -> list[CleanupEntry]:
        """Return the entries assigned to a given tier, largest first."""
        selected = [entry for entry in self.entries if entry.tier == tier]
        return sorted(selected, key=lambda item: item.size_bytes, reverse=True)

    def grouped(self, tier: str) -> dict[str, list[CleanupEntry]]:
        """Return the tier entries grouped by display label, largest group first."""
        groups: dict[str, list[CleanupEntry]] = {}
        for entry in self.by_tier(tier):
            groups.setdefault(entry.label, []).append(entry)
        ordered = sorted(groups.items(), key=lambda kv: _group_size(kv[1]), reverse=True)
        return dict(ordered)

    def tier_bytes(self, tier: str) -> int:
        """Return the total size in bytes of the entries in a tier."""
        return sum(entry.size_bytes for entry in self.entries if entry.tier == tier)

    def removable(self, include_sensitive: bool) -> list[CleanupEntry]:
        """Return the entries that execution would remove for the chosen scope."""
        tiers = {TIER_RECLAIM}
        if include_sensitive:
            tiers.add(TIER_SENSITIVE)
        return [entry for entry in self.entries if entry.tier in tiers]


@dataclass
class CleanupResult:
    """The outcome of executing a cleanup plan."""

    removed: list[CleanupEntry] = field(default_factory=list)
    errors: list[tuple[CleanupEntry, str]] = field(default_factory=list)
    reclaimed_bytes: int = 0


def human_size(num_bytes: int) -> str:
    """Return a compact human-readable representation of a byte count."""
    value = float(max(num_bytes, 0))
    for unit in _BYTE_UNITS:
        if value < _BYTE_STEP or unit == _BYTE_UNITS[-1]:
            if unit == "B":
                return f"{int(value)}{unit}"
            return f"{value:.1f}{unit}"
        value /= _BYTE_STEP
    return f"{value:.1f}{_BYTE_UNITS[-1]}"


def safe_label(name: str) -> str:
    """Return a name with control and direction-override characters neutralised.

    Crafted filenames in ``sessions`` can carry bidirectional override or other
    control characters that spoof the terminal. Rendering them verbatim in an
    audit report is itself a risk, so every control character is replaced with
    its escaped code point before display.
    """
    rendered = []
    for char in name:
        if unicodedata.category(char).startswith(_CONTROL_CATEGORY_PREFIX):
            rendered.append(f"\\u{ord(char):04x}")
        else:
            rendered.append(char)
    return "".join(rendered)


def entry_size(path: str) -> int:
    """Return the size in bytes of a file or the recursive size of a directory."""
    try:
        if os.path.islink(path):
            return os.lstat(path).st_size
        if os.path.isfile(path):
            return os.path.getsize(path)
    except OSError:
        return 0
    total = 0
    for root, _dirs, files in os.walk(path):
        for name in files:
            candidate = os.path.join(root, name)
            try:
                if not os.path.islink(candidate):
                    total += os.path.getsize(candidate)
            except OSError:
                continue
    return total


def classify(name: str) -> tuple[str, str]:
    """Return the ``(tier, label)`` verdict for a top-level entry name."""
    if name in PROTECTED_NAMES:
        return TIER_PROTECTED, "Protected scaffolding, secrets and persona"
    for rule in SENSITIVE_RULES:
        if rule.matches(name):
            return TIER_SENSITIVE, rule.label
    for rule in RECLAIM_RULES:
        if rule.matches(name):
            return TIER_RECLAIM, rule.label
    return TIER_RECLAIM, _RECLAIM_FALLBACK_LABEL


def _subset_filter(subset: str | None) -> Callable[[str], bool] | None:
    """Return a predicate restricting the plan to a named subset, or ``None``."""
    if subset is None:
        return None
    patterns = SUBSET_PATTERNS.get(subset)
    if not patterns:
        raise ValueError(f"Unknown clean subset: {subset}")
    return _glob_matcher(*patterns)


def build_plan(sessions_dir: str = SESSIONS_DIRNAME, subset: str | None = None) -> CleanupPlan:
    """Partition ``sessions_dir`` into a protected, sensitive and reclaim plan.

    Args:
        sessions_dir: Path to the sessions directory to audit.
        subset: Optional keyword (``nmap``, ``log``, ``test``) restricting the
            plan to a matching family of artefacts.

    Returns:
        A :class:`CleanupPlan`. When a subset is given, protected entries are
        omitted and only the matching reclaim/sensitive entries are listed.
    """
    plan = CleanupPlan(sessions_dir=sessions_dir, subset=subset)
    try:
        names = sorted(os.listdir(sessions_dir))
    except OSError:
        return plan
    keep = _subset_filter(subset)
    for name in names:
        if keep is not None and not keep(name):
            continue
        tier, label = classify(name)
        if subset is not None and tier == TIER_PROTECTED:
            continue
        path = os.path.join(sessions_dir, name)
        is_dir = os.path.isdir(path) and not os.path.islink(path)
        plan.entries.append(
            CleanupEntry(
                name=name,
                path=path,
                size_bytes=entry_size(path),
                is_dir=is_dir,
                tier=tier,
                label=label,
                empty_only=is_dir and name in EMPTY_ONLY_DIRS,
            )
        )
    return plan


def _default_remove(entry: CleanupEntry) -> None:
    """Remove one entry from disk, emptying ``empty_only`` directories in place."""
    if entry.empty_only and entry.is_dir:
        for child in os.listdir(entry.path):
            child_path = os.path.join(entry.path, child)
            if os.path.isdir(child_path) and not os.path.islink(child_path):
                shutil.rmtree(child_path, onerror=_force_remove)
            else:
                _unlink(child_path)
        return
    if entry.is_dir:
        shutil.rmtree(entry.path, onerror=_force_remove)
    else:
        _unlink(entry.path)


def _unlink(path: str) -> None:
    """Remove a single file, retrying once after relaxing its mode."""
    try:
        os.remove(path)
    except PermissionError:
        os.chmod(path, 0o600)
        os.remove(path)


def _force_remove(func, path, _exc_info) -> None:
    """``shutil.rmtree`` error handler that relaxes mode then retries once."""
    os.chmod(path, 0o700)
    func(path)


def remove_entries(
    entries: Iterable[CleanupEntry],
    remover: Callable[[CleanupEntry], None] = _default_remove,
) -> CleanupResult:
    """Delete the given entries, collecting reclaimed bytes and per-entry errors.

    Args:
        entries: The entries to remove.
        remover: Injectable removal function, defaulting to in-process deletion.

    Returns:
        A :class:`CleanupResult` summarising what was removed and what failed.
    """
    result = CleanupResult()
    for entry in entries:
        try:
            remover(entry)
        except OSError as exc:
            result.errors.append((entry, str(exc)))
            continue
        result.removed.append(entry)
        result.reclaimed_bytes += entry.size_bytes
    return result


def _group_size(entries: list[CleanupEntry]) -> int:
    """Return the combined size in bytes of a group of entries."""
    return sum(entry.size_bytes for entry in entries)


__all__ = [
    "TIER_PROTECTED",
    "TIER_SENSITIVE",
    "TIER_RECLAIM",
    "CleanupEntry",
    "CleanupPlan",
    "CleanupResult",
    "build_plan",
    "classify",
    "remove_entries",
    "human_size",
    "safe_label",
    "entry_size",
]
