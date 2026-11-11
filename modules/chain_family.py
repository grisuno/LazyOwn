"""Isomorphism transfer: reuse a winning chain across structurally-similar targets.

sapper-v2 reuses a proven playbook across challenges that are structurally
identical ("isomorphism transfer"). LazyOwn's equivalent: derive a stable
*family signature* from a target's structural facts (its service set, OS hint
and whether credentials are known), remember which chain proved a target of
that family, and surface that winning chain the next time a same-family target
is synthesised, so the loop does not re-derive a plan it already has.

The signature function is pure. The registry persists to
``sessions/chain_families.json`` through the same atomic JSON helpers the rest
of the loop uses, and records both associations (synthesised chains) and wins
(chains whose run proved the goal), ranking proven chains first.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from pathlib import Path
from typing import Any

_SIGNATURE_LEN = 16
_SERVICE_ALIASES = {
    "www": "http",
    "http-alt": "http",
    "https-alt": "https",
    "microsoft-ds": "smb",
    "netbios-ssn": "smb",
    "ms-wbt-server": "rdp",
}


def _normalize_service(name: str) -> str:
    """Return a canonical service token, collapsing common aliases."""
    token = str(name or "").strip().lower()
    token = token.split("?")[0].split("/")[0].strip()
    return _SERVICE_ALIASES.get(token, token)


def family_signature(facts: Mapping[str, Any]) -> str:
    """Return a stable structural signature for a target from its facts.

    Two targets that expose the same set of services, the same OS hint and the
    same credential posture share a signature, even when their addresses
    differ. Service order and duplicates do not affect the result.

    Args:
        facts: A mapping with ``services`` (iterable of names), ``os_hint``
            (string) and ``has_creds`` (bool).

    Returns:
        A short hex signature string; ``"empty"`` when no service is known.
    """
    services = facts.get("services", []) or []
    if isinstance(services, (str, bytes)):
        services = [services]
    normalized = sorted({_normalize_service(name) for name in services if str(name).strip()})
    normalized = [name for name in normalized if name]
    if not normalized:
        return "empty"
    os_hint = str(facts.get("os_hint", "") or "").strip().lower()
    creds = "c1" if bool(facts.get("has_creds")) else "c0"
    basis = "|".join(normalized) + f"|{os_hint}|{creds}"
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:_SIGNATURE_LEN]


class FamilyRegistry:
    """Persisted map from a family signature to the chains seen for it.

    Each signature holds per-chain counters (associations and wins). ``best``
    ranks chains with recorded wins first, then by total sightings, so a chain
    that actually proved a target is preferred over one merely synthesised.
    """

    def __init__(self, path: str | Path) -> None:
        """Bind the registry to a JSON file.

        Args:
            path: The ``chain_families.json`` path (created on first write).
        """
        self.path = Path(path)

    def _load(self) -> dict[str, Any]:
        """Return the persisted mapping, or an empty structure."""
        from modules.lazy_loop import _load_json

        return _load_json(self.path, {"families": {}})

    def _save(self, data: Mapping[str, Any]) -> None:
        """Atomically persist the mapping."""
        from modules.lazy_loop import _save_json

        _save_json(self.path, dict(data))

    def _touch(self, signature: str, chain: str, *, win: bool, target: str) -> dict[str, Any]:
        """Increment counters for one (family, chain) pair and persist."""
        data = self._load()
        families = data.setdefault("families", {})
        family = families.setdefault(signature, {"chains": {}})
        chains = family.setdefault("chains", {})
        entry = chains.setdefault(chain, {"seen": 0, "wins": 0, "targets": []})
        entry["seen"] = int(entry.get("seen", 0)) + 1
        if win:
            entry["wins"] = int(entry.get("wins", 0)) + 1
        if target and target not in entry["targets"]:
            entry["targets"] = (entry.get("targets", []) + [target])[-10:]
        self._save(data)
        return entry

    def record_association(self, signature: str, chain: str, target: str = "") -> None:
        """Record that ``chain`` was synthesised for a target of this family."""
        if not signature or not chain or signature == "empty":
            return
        self._touch(signature, chain, win=False, target=target)

    def record_win(self, signature: str, chain: str, target: str = "") -> None:
        """Record that ``chain`` proved a target of this family."""
        if not signature or not chain or signature == "empty":
            return
        self._touch(signature, chain, win=True, target=target)

    def best(self, signature: str) -> dict[str, Any] | None:
        """Return the strongest chain recorded for a family, or None.

        Chains with wins rank first, then by total sightings; ties break by
        chain name for determinism.

        Args:
            signature: The family signature.

        Returns:
            A dict ``{chain, wins, seen, targets}`` or None when unseen.
        """
        if not signature or signature == "empty":
            return None
        family = self._load().get("families", {}).get(signature)
        if not family:
            return None
        chains: dict[str, Any] = family.get("chains", {})
        if not chains:
            return None
        best_name = max(
            chains,
            key=lambda name: (
                int(chains[name].get("wins", 0)),
                int(chains[name].get("seen", 0)),
                name,
            ),
        )
        entry = chains[best_name]
        return {
            "chain": best_name,
            "wins": int(entry.get("wins", 0)),
            "seen": int(entry.get("seen", 0)),
            "targets": list(entry.get("targets", [])),
        }

    def transfer_note(self, facts: Mapping[str, Any]) -> str:
        """Return an operator note when this family has a known winning chain.

        Args:
            facts: Target facts (see :func:`family_signature`).

        Returns:
            A human-readable note, or an empty string when nothing transfers.
        """
        best = self.best(family_signature(facts))
        if not best:
            return ""
        verb = "proven" if best["wins"] > 0 else "seen"
        return (
            f"isomorphism transfer: same-family target(s) {verb} with chain "
            f"'{best['chain']}' (wins={best['wins']}, seen={best['seen']})"
        )


def _default_registry_path() -> Path:
    """Return the shared registry path under the loop store directory."""
    from modules.lazy_loop import _store_path

    return _store_path("chain_families.json")


def default_registry() -> FamilyRegistry:
    """Return a registry bound to the shared ``chain_families.json``."""
    return FamilyRegistry(_default_registry_path())


__all__ = ["FamilyRegistry", "default_registry", "family_signature"]
