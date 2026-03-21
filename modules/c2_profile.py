#!/usr/bin/env python3
"""
modules/c2_profile.py
======================
Malleable C2 profile system for LazyOwn.

Controls beacon HTTP behavior: headers, URIs, sleep timing, jitter,
user-agent, and staging configuration.

Architecture follows SOLID principles:
  - Single Responsibility: each class handles one concern
  - Open/Closed: new profiles registered without modifying existing code
  - Liskov: dataclasses are safely substitutable
  - Interface Segregation: ProfileApplier separates Flask/requests concerns
  - Dependency Inversion: loaders/validators depend on abstractions (dicts/paths)

Usage:
    from modules.c2_profile import get_profile, list_profiles, get_registry

    profile = get_profile("stealth")
    delay   = profile.jitter_delay()
    headers = profile.build_headers("GET")
    uri     = profile.get_uri("POST")

CLI:
    python3 modules/c2_profile.py --list
    python3 modules/c2_profile.py --show stealth
"""
from __future__ import annotations

import logging
import math
import os
import random
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

log = logging.getLogger("c2_profile")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_BASE_DIR       = Path(__file__).parent.parent
_PROFILES_DIR   = _BASE_DIR / "sessions" / "c2_profiles"

# ---------------------------------------------------------------------------
# Dataclasses (Single Responsibility: pure data containers)
# ---------------------------------------------------------------------------


@dataclass
class SleepConfig:
    """Sleep and jitter configuration for a beacon."""

    interval_ms: int       # sleep interval in milliseconds (must be > 0)
    jitter_pct: int        # jitter percentage 0-50


@dataclass
class HttpConfig:
    """HTTP request configuration for one direction (GET or POST)."""

    method: str
    uri_paths: List[str]
    headers: Dict[str, str]
    user_agent: str


@dataclass
class StagerConfig:
    """Staging payload configuration."""

    enabled: bool
    stage_uri: str
    max_size_kb: int


@dataclass
class C2Profile:
    """
    Complete malleable C2 profile.

    Encapsulates all behavioral parameters that govern how a beacon
    communicates over HTTP.
    """

    name: str
    description: str
    sleep: SleepConfig
    http_get: HttpConfig
    http_post: HttpConfig
    stager: StagerConfig
    metadata: Dict[str, str] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Behavioral helpers
    # ------------------------------------------------------------------

    def jitter_delay(self) -> float:
        """
        Return the next sleep delay as a float in seconds.

        The delay is interval_ms/1000 scaled by a random multiplier in
        [1 - jitter_pct/100 , 1 + jitter_pct/100].
        """
        base = self.sleep.interval_ms / 1000.0
        if self.sleep.jitter_pct == 0:
            return base
        factor = random.uniform(
            1.0 - self.sleep.jitter_pct / 100.0,
            1.0 + self.sleep.jitter_pct / 100.0,
        )
        return base * factor

    def get_uri(self, method: str = "GET") -> str:
        """
        Pick a random URI path from the appropriate HttpConfig.

        Parameters
        ----------
        method : "GET" or "POST" (case-insensitive)
        """
        cfg = self._config_for(method)
        return random.choice(cfg.uri_paths)

    def build_headers(self, method: str = "GET") -> Dict[str, str]:
        """
        Return the headers dict for the given HTTP method.

        The returned dict is a shallow copy; callers may mutate it freely.
        """
        cfg = self._config_for(method)
        result = dict(cfg.headers)
        if "User-Agent" not in result and cfg.user_agent:
            result["User-Agent"] = cfg.user_agent
        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _config_for(self, method: str) -> HttpConfig:
        if method.upper() == "POST":
            return self.http_post
        return self.http_get


# ---------------------------------------------------------------------------
# ProfileValidator (Single Responsibility: validation only)
# ---------------------------------------------------------------------------


class ProfileValidator:
    """
    Validates a C2Profile instance.

    Returns a list of error strings; an empty list means the profile is valid.
    """

    def validate(self, profile: C2Profile) -> List[str]:
        errors: List[str] = []

        # SleepConfig checks
        if profile.sleep.interval_ms <= 0:
            errors.append("sleep.interval_ms must be greater than 0")
        if not (0 <= profile.sleep.jitter_pct <= 50):
            errors.append("sleep.jitter_pct must be between 0 and 50 inclusive")

        # HttpConfig checks
        for direction, cfg in (("http_get", profile.http_get), ("http_post", profile.http_post)):
            if not cfg.uri_paths:
                errors.append(f"{direction}.uri_paths must contain at least one URI")
            for k, v in cfg.headers.items():
                if not isinstance(v, str):
                    errors.append(
                        f"{direction}.headers['{k}'] value must be a string, got {type(v).__name__}"
                    )

        return errors


# ---------------------------------------------------------------------------
# ProfileLoader (Single Responsibility: serialisation/deserialisation)
# ---------------------------------------------------------------------------


class ProfileLoader:
    """
    Loads and saves C2Profile objects from/to YAML or dict representations.

    Depends on PyYAML when loading YAML files; falls back with a clear error
    if PyYAML is not installed.
    """

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    @staticmethod
    def from_yaml(path: str | Path) -> C2Profile:
        """Load a C2Profile from a YAML file at *path*."""
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise ImportError(
                "PyYAML is required to load YAML profiles. "
                "Install it with: pip install pyyaml"
            ) from exc

        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Profile YAML not found: {p}")
        with p.open("r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        return ProfileLoader.from_dict(raw)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> C2Profile:
        """Construct a C2Profile from a plain Python dictionary."""
        sleep_raw   = d.get("sleep", {})
        get_raw     = d.get("http_get", {})
        post_raw    = d.get("http_post", {})
        stager_raw  = d.get("stager", {})

        sleep = SleepConfig(
            interval_ms=int(sleep_raw.get("interval_ms", 60_000)),
            jitter_pct=int(sleep_raw.get("jitter_pct", 0)),
        )
        http_get = HttpConfig(
            method="GET",
            uri_paths=list(get_raw.get("uri_paths", ["/"])),
            headers=dict(get_raw.get("headers", {})),
            user_agent=str(get_raw.get("user_agent", "")),
        )
        http_post = HttpConfig(
            method="POST",
            uri_paths=list(post_raw.get("uri_paths", ["/"])),
            headers=dict(post_raw.get("headers", {})),
            user_agent=str(post_raw.get("user_agent", http_get.user_agent)),
        )
        stager = StagerConfig(
            enabled=bool(stager_raw.get("enabled", False)),
            stage_uri=str(stager_raw.get("stage_uri", "/stage")),
            max_size_kb=int(stager_raw.get("max_size_kb", 512)),
        )
        return C2Profile(
            name=str(d.get("name", "unnamed")),
            description=str(d.get("description", "")),
            sleep=sleep,
            http_get=http_get,
            http_post=http_post,
            stager=stager,
            metadata=dict(d.get("metadata", {})),
        )

    @staticmethod
    def to_dict(profile: C2Profile) -> Dict[str, Any]:
        """Convert a C2Profile to a plain Python dictionary."""
        return {
            "name": profile.name,
            "description": profile.description,
            "sleep": {
                "interval_ms": profile.sleep.interval_ms,
                "jitter_pct": profile.sleep.jitter_pct,
            },
            "http_get": {
                "uri_paths": profile.http_get.uri_paths,
                "headers": profile.http_get.headers,
                "user_agent": profile.http_get.user_agent,
            },
            "http_post": {
                "uri_paths": profile.http_post.uri_paths,
                "headers": profile.http_post.headers,
                "user_agent": profile.http_post.user_agent,
            },
            "stager": {
                "enabled": profile.stager.enabled,
                "stage_uri": profile.stager.stage_uri,
                "max_size_kb": profile.stager.max_size_kb,
            },
            "metadata": profile.metadata,
        }

    @staticmethod
    def save(profile: C2Profile, path: str | Path) -> Path:
        """Serialise *profile* to a YAML file and return the written path."""
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise ImportError(
                "PyYAML is required to save YAML profiles. "
                "Install it with: pip install pyyaml"
            ) from exc

        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as fh:
            yaml.safe_dump(ProfileLoader.to_dict(profile), fh, sort_keys=False)
        log.info("Profile '%s' saved to %s", profile.name, out)
        return out


# ---------------------------------------------------------------------------
# Built-in profile definitions
# ---------------------------------------------------------------------------

_BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

_ONEDRIVE_UA = (
    "Microsoft SkyDriveSync 23.076.0402.0003 ship; "
    "Windows NT 10.0 (17763)"
)


def _make_default_profile() -> C2Profile:
    return C2Profile(
        name="default",
        description="Standard browser-mimicking profile with 60s sleep.",
        sleep=SleepConfig(interval_ms=60_000, jitter_pct=20),
        http_get=HttpConfig(
            method="GET",
            uri_paths=["/jquery-3.6.0.min.js", "/assets/jquery.min.js"],
            headers={
                "Accept": "text/javascript, application/javascript, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
            user_agent=_BROWSER_UA,
        ),
        http_post=HttpConfig(
            method="POST",
            uri_paths=["/submit", "/api/data"],
            headers={
                "Accept": "*/*",
                "Content-Type": "application/x-www-form-urlencoded",
                "Connection": "keep-alive",
            },
            user_agent=_BROWSER_UA,
        ),
        stager=StagerConfig(enabled=True, stage_uri="/stage", max_size_kb=512),
        metadata={"author": "LazyOwn", "version": "1.0"},
    )


def _make_stealth_profile() -> C2Profile:
    guid1 = "1c3a5e7b-9f2d-4a6b-8c0e-2d4f6a8b0c2e"
    guid2 = "3e5f7a9b-1c3d-5e7f-9a1b-3c5d7e9f1a3b"
    guid3 = "7f9b1d3e-5a7c-9b1d-3e5a-7c9b1d3e5a7c"
    return C2Profile(
        name="stealth",
        description=(
            "Low-and-slow profile mimicking Microsoft OneDrive sync traffic. "
            "5-minute sleep with 30% jitter and long GUID-based URIs."
        ),
        sleep=SleepConfig(interval_ms=300_000, jitter_pct=30),
        http_get=HttpConfig(
            method="GET",
            uri_paths=[
                f"/personal/{guid1}/Documents/shared/delta",
                f"/drives/{guid2}/root/children",
                f"/_api/v2.0/drives/{guid3}/items/root/delta",
            ],
            headers={
                "Accept": "application/json;odata.metadata=minimal",
                "Accept-Language": "en-US",
                "Authorization": "Bearer PLACEHOLDER",
                "Cache-Control": "no-store",
                "Connection": "keep-alive",
                "X-RequestDigest": "0x" + uuid.uuid4().hex.upper(),
            },
            user_agent=_ONEDRIVE_UA,
        ),
        http_post=HttpConfig(
            method="POST",
            uri_paths=[
                f"/personal/{guid1}/Documents/shared/upload",
                f"/drives/{guid2}/root/createUploadSession",
            ],
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json; charset=utf-8",
                "Connection": "keep-alive",
            },
            user_agent=_ONEDRIVE_UA,
        ),
        stager=StagerConfig(enabled=False, stage_uri="/stage", max_size_kb=256),
        metadata={"author": "LazyOwn", "version": "1.0", "category": "stealth"},
    )


def _make_aggressive_profile() -> C2Profile:
    return C2Profile(
        name="aggressive",
        description="Fast polling profile with 5s sleep and minimal headers.",
        sleep=SleepConfig(interval_ms=5_000, jitter_pct=5),
        http_get=HttpConfig(
            method="GET",
            uri_paths=["/poll", "/check", "/ping"],
            headers={"Connection": "keep-alive"},
            user_agent="Go-http-client/1.1",
        ),
        http_post=HttpConfig(
            method="POST",
            uri_paths=["/data", "/send"],
            headers={
                "Content-Type": "application/octet-stream",
                "Connection": "keep-alive",
            },
            user_agent="Go-http-client/1.1",
        ),
        stager=StagerConfig(enabled=True, stage_uri="/payload", max_size_kb=1024),
        metadata={"author": "LazyOwn", "version": "1.0", "category": "aggressive"},
    )


def _make_debug_profile() -> C2Profile:
    return C2Profile(
        name="debug",
        description=(
            "1-second sleep with no jitter; verbose headers for development "
            "and integration testing."
        ),
        sleep=SleepConfig(interval_ms=1_000, jitter_pct=0),
        http_get=HttpConfig(
            method="GET",
            uri_paths=["/debug/beacon", "/debug/check"],
            headers={
                "Accept": "*/*",
                "X-Debug": "1",
                "X-Profile": "debug",
                "Cache-Control": "no-cache, no-store",
                "Connection": "keep-alive",
            },
            user_agent="LazyOwn-Debug/1.0",
        ),
        http_post=HttpConfig(
            method="POST",
            uri_paths=["/debug/callback", "/debug/upload"],
            headers={
                "Accept": "*/*",
                "Content-Type": "application/json",
                "X-Debug": "1",
                "X-Profile": "debug",
                "Connection": "keep-alive",
            },
            user_agent="LazyOwn-Debug/1.0",
        ),
        stager=StagerConfig(enabled=True, stage_uri="/debug/stage", max_size_kb=64),
        metadata={"author": "LazyOwn", "version": "1.0", "category": "debug"},
    )


# ---------------------------------------------------------------------------
# ProfileRegistry (Open/Closed: new profiles registered without modifying core)
# ---------------------------------------------------------------------------


class ProfileRegistry:
    """
    In-memory registry of named C2Profile objects.

    Register custom profiles at runtime, or load an entire directory of
    YAML files.
    """

    def __init__(self) -> None:
        self._profiles: Dict[str, C2Profile] = {}

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def register(self, name: str, profile: C2Profile) -> None:
        """Register *profile* under *name*, overwriting any previous entry."""
        self._profiles[name] = profile
        log.debug("Registered profile '%s'", name)

    # ------------------------------------------------------------------
    # Access
    # ------------------------------------------------------------------

    def get(self, name: str) -> C2Profile:
        """
        Return the profile registered under *name*.

        Raises KeyError if no such profile exists.
        """
        try:
            return self._profiles[name]
        except KeyError:
            available = ", ".join(self.list_names()) or "(none)"
            raise KeyError(
                f"Profile '{name}' not found. Available profiles: {available}"
            )

    def list_names(self) -> List[str]:
        """Return a sorted list of all registered profile names."""
        return sorted(self._profiles.keys())

    # ------------------------------------------------------------------
    # Bulk loading
    # ------------------------------------------------------------------

    def load_from_directory(self, path: str | Path) -> int:
        """
        Scan *path* for *.yaml files and register each as a profile.

        Returns the count of successfully loaded profiles.
        """
        d = Path(path)
        if not d.is_dir():
            log.warning("Profile directory does not exist: %s", d)
            return 0
        count = 0
        for yaml_file in sorted(d.glob("*.yaml")):
            try:
                profile = ProfileLoader.from_yaml(yaml_file)
                self.register(profile.name, profile)
                count += 1
            except Exception as exc:
                log.warning("Failed to load profile from %s: %s", yaml_file, exc)
        log.info("Loaded %d profile(s) from %s", count, d)
        return count


# ---------------------------------------------------------------------------
# ProfileApplier (Interface Segregation: separate Flask / requests concerns)
# ---------------------------------------------------------------------------


class ProfileApplier:
    """
    Applies a C2Profile to Flask responses or requests.Session objects.

    This class has no state; all methods are pure functions of their
    arguments.
    """

    @staticmethod
    def apply_to_response(profile: C2Profile, response: Any) -> Any:
        """
        Patch the headers of a Flask response object to match the profile.

        Sets appropriate Cache-Control and removes server-identifying headers.
        The response object is mutated in-place and also returned.
        """
        headers = profile.build_headers("GET")
        for key, value in headers.items():
            # Avoid overwriting Content-Type set by Flask
            if key.lower() not in ("content-type", "content-length"):
                response.headers[key] = value

        # Standard cache suppression for C2 traffic masquerading
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        response.headers["Pragma"]        = "no-cache"
        response.headers["Expires"]       = "0"

        # Remove headers that leak server identity
        for leak in ("Server", "X-Powered-By"):
            response.headers.pop(leak, None)

        return response

    @staticmethod
    def apply_to_session(profile: C2Profile, session: Any) -> Any:
        """
        Configure a requests.Session to mimic the profile's HTTP GET behavior.

        Sets headers and User-Agent on *session* and returns it.
        """
        headers = profile.build_headers("GET")
        session.headers.update(headers)
        if profile.http_get.user_agent:
            session.headers["User-Agent"] = profile.http_get.user_agent
        return session

    @staticmethod
    def get_beacon_config(profile: C2Profile) -> Dict[str, Any]:
        """
        Return a JSON-serialisable dict suitable for embedding in a beacon
        handshake response.

        The dict contains only the fields a beacon needs to self-configure;
        it does not expose full header details.
        """
        return {
            "profile":       profile.name,
            "sleep_ms":      profile.sleep.interval_ms,
            "jitter_pct":    profile.sleep.jitter_pct,
            "get_uris":      profile.http_get.uri_paths,
            "post_uris":     profile.http_post.uri_paths,
            "user_agent":    profile.http_get.user_agent,
            "stager_enabled": profile.stager.enabled,
            "stage_uri":     profile.stager.stage_uri if profile.stager.enabled else None,
            "max_stage_kb":  profile.stager.max_size_kb,
        }


# ---------------------------------------------------------------------------
# Module-level singleton and convenience API
# ---------------------------------------------------------------------------

_registry: Optional[ProfileRegistry] = None


def get_registry() -> ProfileRegistry:
    """
    Return the module-level singleton ProfileRegistry.

    On first call, registers the four built-in profiles and then scans the
    default profiles directory for additional YAML files.
    """
    global _registry
    if _registry is None:
        _registry = ProfileRegistry()
        # Register built-in profiles
        for factory in (
            _make_default_profile,
            _make_stealth_profile,
            _make_aggressive_profile,
            _make_debug_profile,
        ):
            p = factory()
            _registry.register(p.name, p)
        # Scan default profiles directory (optional; failures are non-fatal)
        _PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        _registry.load_from_directory(_PROFILES_DIR)
    return _registry


def get_profile(name: str) -> C2Profile:
    """Return the named profile from the module singleton registry."""
    return get_registry().get(name)


def list_profiles() -> List[str]:
    """Return a sorted list of all registered profile names."""
    return get_registry().list_names()


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import json as _json

    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")

    ap = argparse.ArgumentParser(
        description="LazyOwn C2 Profile Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python3 modules/c2_profile.py --list\n"
            "  python3 modules/c2_profile.py --show stealth\n"
            "  python3 modules/c2_profile.py --show debug --json\n"
            "  python3 modules/c2_profile.py --validate stealth\n"
        ),
    )
    ap.add_argument("--list",     action="store_true", help="List all registered profiles")
    ap.add_argument("--show",     metavar="NAME",      help="Print details for a named profile")
    ap.add_argument("--validate", metavar="NAME",      help="Validate a named profile and report errors")
    ap.add_argument("--json",     action="store_true", help="Output --show in JSON format")
    args = ap.parse_args()

    reg = get_registry()

    if args.list:
        names = reg.list_names()
        print(f"Registered profiles ({len(names)}):")
        for n in names:
            p = reg.get(n)
            print(f"  {n:15s}  {p.description[:70]}")

    elif args.show:
        try:
            profile = reg.get(args.show)
        except KeyError as exc:
            print(f"Error: {exc}")
            raise SystemExit(1)

        if args.json:
            print(_json.dumps(ProfileLoader.to_dict(profile), indent=2))
        else:
            print(f"Profile      : {profile.name}")
            print(f"Description  : {profile.description}")
            print(f"Sleep        : {profile.sleep.interval_ms} ms  jitter={profile.sleep.jitter_pct}%")
            print(f"GET URIs     : {profile.http_get.uri_paths}")
            print(f"POST URIs    : {profile.http_post.uri_paths}")
            print(f"User-Agent   : {profile.http_get.user_agent}")
            print(f"Stager       : {'enabled' if profile.stager.enabled else 'disabled'}"
                  f"  uri={profile.stager.stage_uri}  max={profile.stager.max_size_kb} KB")
            print(f"GET headers  : {profile.http_get.headers}")
            print(f"POST headers : {profile.http_post.headers}")
            print(f"Metadata     : {profile.metadata}")
            sample_delay = profile.jitter_delay()
            print(f"Sample delay : {sample_delay:.3f} s")

    elif args.validate:
        try:
            profile = reg.get(args.validate)
        except KeyError as exc:
            print(f"Error: {exc}")
            raise SystemExit(1)
        errors = ProfileValidator().validate(profile)
        if errors:
            print(f"Validation FAILED for '{args.validate}':")
            for err in errors:
                print(f"  - {err}")
            raise SystemExit(2)
        else:
            print(f"Profile '{args.validate}' is valid.")

    else:
        ap.print_help()
