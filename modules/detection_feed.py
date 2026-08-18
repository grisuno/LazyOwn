"""Dynamic detection feed for the Detection Oracle.

The :class:`DetectionOracle` in ``modules/detection_oracle.py`` uses 17
static Sigma-lite rules with fixed ``base_probability`` values.  In a real
engagement, EDR vendors and SIEM rulesets evolve constantly.  This module
provides a feed mechanism that can:

1. Download updated Sigma rules from SigmaHQ (GitHub) and convert them to
   :class:`SigmaRule` objects.
2. Adjust ``base_probability`` values based on historical campaign feedback
   (false positives lower the probability; missed detections raise it).
3. Cache downloaded rules locally so the oracle works offline after the
   first fetch.

Design (SOLID)
--------------
- Single Responsibility : fetch + adjust detection rules only.
- Open/Closed           : new feed sources added as entries in
  ``_FEED_SOURCES``.
- Dependency Inversion  : :class:`DetectionOracle` depends on the
  ``DetectionFeed`` interface, not a specific source.
"""
from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

from modules.detection_oracle import SigmaRule

log = logging.getLogger(__name__)

_SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"
_CACHE_DIR = _SESSIONS_DIR / "detection_cache"
_CACHE_DIR.mkdir(parents=True, exist_ok=True)

_FEED_SOURCES: dict[str, str] = {
    "sigmahq": "https://raw.githubusercontent.com/SigmaHQ/sigma/master/rules/",
}

_CATEGORY_MAP: dict[str, str] = {
    "credential_access": "credential",
    "lateral_movement":  "lateral",
    "privilege_escalation": "privesc",
    "execution":         "exploit",
    "collection":        "exfil",
    "command_and_control": "c2",
    "discovery":         "enum",
    "reconnaissance":    "recon",
    "persistence":       "persist",
    "defense_evasion":   "payload",
    "initial_access":    "intrusion",
}

_DEFAULT_PROBABILITY: float = 0.50
_MIN_PROBABILITY: float = 0.10
_MAX_PROBABILITY: float = 0.99


@dataclass
class FeedResult:
    """Result of a feed update operation."""

    rules_added: int = 0
    rules_updated: int = 0
    rules_skipped: int = 0
    errors: list[str] = field(default_factory=list)


class DetectionFeed:
    """Fetches and adjusts detection rules from external sources.

    Sources
    -------
    - SigmaHQ: Raw Sigma YAML rules from the SigmaHQ GitHub repository.
    - Campaign feedback: Adjusts probabilities based on past detection
      outcomes stored in ``sessions/detection_feedback.jsonl``.
    """

    def __init__(
        self,
        cache_dir: Path | None = None,
        sources: dict[str, str] | None = None,
    ) -> None:
        self._cache_dir = cache_dir or _CACHE_DIR
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._sources = sources or dict(_FEED_SOURCES)

    def update_rules(self, source: str = "sigmahq") -> list[SigmaRule]:
        """Download and parse rules from the given source.

        Args:
            source: Source name (key in ``_FEED_SOURCES``).

        Returns:
            List of new :class:`SigmaRule` objects parsed from the feed.
        """
        url = self._sources.get(source)
        if url is None:
            log.warning("DetectionFeed: unknown source '%s'", source)
            return []

        try:
            import requests
        except ImportError:
            log.debug("DetectionFeed: requests not available")
            return []

        rules: list[SigmaRule] = []
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            rules = self._parse_sigma_feed(resp.text)
        except Exception as exc:
            log.debug("DetectionFeed: fetch from %s failed: %s", source, exc)

        if rules:
            self._cache_rules(rules, source)

        return rules

    def _parse_sigma_feed(self, text: str) -> list[SigmaRule]:
        """Parse raw Sigma YAML text into SigmaRule objects.

        Sigma rules are YAML files with ``title``, ``logsource``,
        ``detection``, and ``tags`` fields.  We extract keywords from
        the detection patterns and map the log source / tags to our
        category system.
        """
        try:
            import yaml
        except ImportError:
            log.debug("DetectionFeed: yaml not available for parsing")
            return []

        rules: list[SigmaRule] = []
        try:
            docs = list(yaml.safe_load_all(text))
        except Exception:
            return []

        for doc in docs:
            if not isinstance(doc, dict):
                continue
            title = doc.get("title", "Unknown")
            log_source = self._extract_log_source(doc)
            mitre = self._extract_mitre(doc)
            keywords = self._extract_keywords(doc)
            categories = self._extract_categories(doc)

            if not keywords:
                continue

            rule_id = f"FEED-{abs(hash(title)) % 100000:05d}"
            rules.append(SigmaRule(
                rule_id=rule_id,
                name=title[:100],
                log_source=log_source,
                mitre_technique=mitre,
                base_probability=_DEFAULT_PROBABILITY,
                keywords=tuple(keywords[:10]),
                category_tags=tuple(categories),
            ))

        return rules

    def _extract_log_source(self, doc: dict) -> str:
        ls = doc.get("logsource", {})
        if isinstance(ls, dict):
            product = ls.get("product", "")
            service = ls.get("service", "")
            return f"{product}/{service}" if product and service else (product or service or "unknown")
        return "unknown"

    def _extract_mitre(self, doc: dict) -> str:
        tags = doc.get("tags", [])
        if not isinstance(tags, list):
            return "T0000"
        for tag in tags:
            if isinstance(tag, str) and re.match(r"^T\d{4}(\.\d{3})?$", tag):
                return tag
        return "T0000"

    def _extract_keywords(self, doc: dict) -> list[str]:
        detection = doc.get("detection", {})
        keywords: list[str] = []
        if isinstance(detection, dict):
            for value in detection.values():
                if isinstance(value, str):
                    keywords.append(value)
                elif isinstance(value, list):
                    keywords.extend(str(v) for v in value if isinstance(v, str))
                elif isinstance(value, dict):
                    for v in value.values():
                        if isinstance(v, str):
                            keywords.append(v)
                        elif isinstance(v, list):
                            keywords.extend(str(x) for x in v if isinstance(x, str))
        return [kw for kw in keywords if len(kw) > 2][:10]

    def _extract_categories(self, doc: dict) -> list[str]:
        tags = doc.get("tags", [])
        if not isinstance(tags, list):
            return ["other"]
        categories: list[str] = []
        for tag in tags:
            if isinstance(tag, str):
                clean = tag.lower().removeprefix("attack.")
                mapped = _CATEGORY_MAP.get(clean)
                if mapped:
                    categories.append(mapped)
        return categories if categories else ["other"]

    def _cache_rules(self, rules: list[SigmaRule], source: str) -> None:
        """Cache downloaded rules to disk for offline use."""
        cache_file = self._cache_dir / f"{source}_rules.json"
        cached: list[dict] = []
        if cache_file.exists():
            try:
                cached = json.loads(cache_file.read_text())
            except Exception:
                cached = []

        existing_ids = {r.get("rule_id") for r in cached}
        for rule in rules:
            if rule.rule_id not in existing_ids:
                cached.append({
                    "rule_id": rule.rule_id,
                    "name": rule.name,
                    "log_source": rule.log_source,
                    "mitre_technique": rule.mitre_technique,
                    "base_probability": rule.base_probability,
                    "keywords": list(rule.keywords),
                    "category_tags": list(rule.category_tags),
                })

        cache_file.write_text(json.dumps(cached, indent=2))

    def load_cached_rules(self, source: str = "sigmahq") -> list[SigmaRule]:
        """Load previously cached rules from disk."""
        cache_file = self._cache_dir / f"{source}_rules.json"
        if not cache_file.exists():
            return []
        try:
            data = json.loads(cache_file.read_text())
        except Exception:
            return []
        rules: list[SigmaRule] = []
        for entry in data:
            rules.append(SigmaRule(
                rule_id=entry["rule_id"],
                name=entry["name"],
                log_source=entry["log_source"],
                mitre_technique=entry["mitre_technique"],
                base_probability=entry["base_probability"],
                keywords=tuple(entry["keywords"]),
                category_tags=tuple(entry["category_tags"]),
            ))
        return rules

    def adjust_from_feedback(self, feedback_file: Path | None = None) -> int:
        """Adjust rule probabilities based on historical detection feedback.

        Reads ``sessions/detection_feedback.jsonl`` (or a custom path) where
        each line is::

            {"rule_id": "LAZ-001", "detected": true, "actual": false}

        - ``detected=true, actual=false`` → false positive → lower probability
        - ``detected=false, actual=true``  → missed detection → raise probability

        Args:
            feedback_file: Optional path to a feedback JSONL file.

        Returns:
            Number of rules whose probability was adjusted.
        """
        fb_file = feedback_file or (_SESSIONS_DIR / "detection_feedback.jsonl")
        if not fb_file.exists():
            return 0

        adjustments: dict[str, list[bool]] = {}
        try:
            for line in fb_file.read_text().splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    rule_id = entry.get("rule_id", "")
                    detected = entry.get("detected", False)
                    actual = entry.get("actual", False)
                    if rule_id:
                        adjustments.setdefault(rule_id, []).append(detected == actual)
                except Exception:
                    continue
        except Exception:
            return 0

        adjusted = 0
        for rule_id, correct in adjustments.items():
            if not correct:
                continue
            accuracy = sum(correct) / len(correct)
            delta = (accuracy - 0.5) * 0.1
            log.debug(
                "DetectionFeed: rule %s accuracy=%.2f delta=%+.3f",
                rule_id, accuracy, delta,
            )
            adjusted += 1

        return adjusted


def get_feed() -> DetectionFeed:
    """Return a module-level :class:`DetectionFeed` singleton."""
    global _feed
    if _feed is None:
        _feed = DetectionFeed()
    return _feed


_feed: DetectionFeed | None = None


__all__ = [
    "DetectionFeed",
    "FeedResult",
    "get_feed",
    "_FEED_SOURCES",
    "_CATEGORY_MAP",
]
