"""Plugin tiers and operator ratings for the marketplace.

Tiers separate what the core team maintains from community contributions
and unvetted experiments:

- ``official``: shipped in-repo and maintained by the core team.
- ``community``: default for everything else, including community clones.
- ``experimental``: explicitly marked as unvetted; may break or change
  without notice.

Resolution order for a plugin name: explicit entry in
``plugins/tiers.yaml`` first, then a ``tier:`` field inside the plugin's
own YAML metadata, then ``community``.

Ratings are operator-local (stored in ``sessions/plugin_ratings.json`` by
default, never committed) and aggregate as a plain average with a count.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

TIER_OFFICIAL = "official"
TIER_COMMUNITY = "community"
TIER_EXPERIMENTAL = "experimental"

KNOWN_TIERS = frozenset({TIER_OFFICIAL, TIER_COMMUNITY, TIER_EXPERIMENTAL})

DEFAULT_RATINGS_FILE = "plugin_ratings.json"


def load_tier_manifest(manifest: str | Path) -> dict[str, str]:
    """Load explicit tier overrides from a ``tiers.yaml`` manifest.

    Args:
        manifest: Path to a YAML mapping of plugin name to tier.

    Returns:
        Mapping of plugin name to tier. Unknown tiers and malformed
        entries are ignored so a bad manifest can never break listing.
    """
    path = Path(manifest)
    if not path.is_file():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (yaml.YAMLError, OSError, UnicodeDecodeError):
        return {}
    if not isinstance(data, dict):
        return {}
    tiers: dict[str, str] = {}
    for name, tier in data.items():
        if isinstance(name, str) and isinstance(tier, str) and tier in KNOWN_TIERS:
            tiers[name] = tier
    return tiers


def tier_of(name: str, manifest_tiers: dict[str, str] | None = None, metadata_tier: str = "") -> str:
    """Resolve the tier for a plugin name.

    Args:
        name: Plugin/addon/tool stem.
        manifest_tiers: Explicit overrides from :func:`load_tier_manifest`.
        metadata_tier: Value of the plugin YAML ``tier:`` field, if any.

    Returns:
        The manifest tier, the metadata tier when valid, else ``community``.
    """
    if manifest_tiers and name in manifest_tiers:
        return manifest_tiers[name]
    if isinstance(metadata_tier, str) and metadata_tier in KNOWN_TIERS:
        return metadata_tier
    return TIER_COMMUNITY


def _load_ratings(store: str | Path) -> dict[str, list[int]]:
    path = Path(store)
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeDecodeError):
        return {}
    if not isinstance(data, dict):
        return {}
    ratings: dict[str, list[int]] = {}
    for name, votes in data.items():
        if isinstance(name, str) and isinstance(votes, list):
            clean = [v for v in votes if isinstance(v, int) and 1 <= v <= 5]
            if clean:
                ratings[name] = clean
    return ratings


def rate_plugin(name: str, stars: int, store: str | Path) -> tuple[float, int]:
    """Record an operator rating and return the new ``(average, count)``.

    Args:
        name: Plugin/addon/tool stem. Must be non-empty.
        stars: Integer rating from 1 to 5.
        store: JSON file holding the ratings map.

    Raises:
        ValueError: When the name is empty or stars are outside 1-5.
    """
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Plugin name must be a non-empty string.")
    if not isinstance(stars, int) or isinstance(stars, bool) or not 1 <= stars <= 5:
        raise ValueError(f"Rating must be an integer from 1 to 5 (got {stars!r}).")
    path = Path(store)
    ratings = _load_ratings(path)
    ratings.setdefault(name, []).append(stars)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ratings, indent=2, sort_keys=True), encoding="utf-8")
    return rating_summary(name, store)


def rating_summary(name: str, store: str | Path) -> tuple[float, int]:
    """Return the ``(average, count)`` rating for a plugin name.

    Args:
        name: Plugin/addon/tool stem.
        store: JSON file holding the ratings map.

    Returns:
        ``(0.0, 0)`` when nobody rated the plugin yet.
    """
    votes = _load_ratings(store).get(name, [])
    if not votes:
        return (0.0, 0)
    return (round(sum(votes) / len(votes), 2), len(votes))


def format_rating(average: float, count: int) -> str:
    """Render a compact rating label for list and info views."""
    if count == 0:
        return "unrated"
    return f"{average:.1f}/5 ({count} vote{'s' if count != 1 else ''})"


def default_store(base_dir: str | Path) -> Path:
    """Return the default ratings file under ``<base_dir>/sessions``."""
    return Path(base_dir) / "sessions" / DEFAULT_RATINGS_FILE


def read_metadata_tier(path: str | Path) -> str:
    """Read the optional ``tier:`` field from a plugin YAML file."""
    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError, UnicodeDecodeError):
        return ""
    if isinstance(data, dict) and isinstance(data.get("tier"), str):
        return data["tier"]
    return ""
