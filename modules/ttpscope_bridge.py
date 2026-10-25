"""Secure bridge for the TTPScope MITRE ATT&CK research client.

Wraps the ``ttpscope`` C binary (built from
https://github.com/bl4ckr0ss3/ttpscope) so CLI operators, MCP agents,
and the autonomous loop share one validated, non-interactive path.

Security invariants:
    1. No shell execution — argv list-form via safe_run_argv only.
    2. Technique/object IDs validated before reaching the binary.
    3. Free-text queries length-capped and passed as single argv element.
    4. Output truncated (200 KB) and always staged under sessions/.
    5. ``chain`` action joins ttpscope + atomic_resolver + parquet
       without executing anything on a target.

Fallback independence (no hard dependency on ttpscope):
    When the binary is missing or unusable, every read action degrades
    to an embedded backend: the cached STIX bundle
    (``~/.cache/ttpscope/enterprise-attack.json``, synced via stdlib
    urllib) is queried directly, and ``parquets/techniques*.parquet``
    covers Atomic technique lookups. Agents keep working with a
    ``backend: fallback-*`` marker in the result.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

log = logging.getLogger("ttpscope_bridge")

_BASE_DIR = Path(__file__).resolve().parent.parent
for _bootstrap_path in (str(_BASE_DIR), str(_BASE_DIR / "modules")):
    if _bootstrap_path not in sys.path:
        sys.path.insert(0, _bootstrap_path)
_INSTALL_DIR = _BASE_DIR / "external" / ".exploit" / "ttpscope"
_BUILT_BIN = _INSTALL_DIR / "build" / "ttpscope"
_SESSIONS_DIR = _BASE_DIR / "sessions"
_REPO_URL = "https://github.com/bl4ckr0ss3/ttpscope.git"

_MAX_QUERY_LEN = 200
_MAX_NOTE_LEN = 2000
_MAX_OUTPUT_BYTES = 200_000
_TIMEOUT_S = 60

_OBJECT_RE = re.compile(r"^(T\d{4}(\.\d{3})?|G\d{4}|S\d{4}|M\d{4}|C\d{4}|DS\d{4}|TA\d{4})$", re.IGNORECASE)
_PLATFORM_ALLOWLIST = frozenset({"windows", "linux", "macos"})
_ACTION_ALLOWLIST = frozenset({"sync", "search", "show", "matrix", "note", "notes", "version", "chain"})

_FALLBACK_DATA_URL = (
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/"
    "enterprise-attack/enterprise-attack.json"
)
_FALLBACK_MAX_DOWNLOAD_BYTES = 100_000_000
_FALLBACK_MAX_SEARCH_ROWS = 50

_TACTIC_ORDER = (
    "reconnaissance",
    "resource-development",
    "initial-access",
    "execution",
    "persistence",
    "privilege-escalation",
    "defense-evasion",
    "credential-access",
    "discovery",
    "lateral-movement",
    "collection",
    "exfiltration",
    "command-and-control",
    "impact",
)


def locate_binary() -> Path | None:
    """Return the ttpscope binary path, preferring the vendored build."""
    if _BUILT_BIN.exists() and os.access(_BUILT_BIN, os.X_OK):
        return _BUILT_BIN
    which = shutil.which("ttpscope")
    if which:
        return Path(which)
    return None


def validate_object_id(raw: str) -> str:
    """Validate an ATT&CK object ID (T1059.001, G0016, S0002, ...)."""
    candidate = (raw or "").strip().upper()
    if not _OBJECT_RE.match(candidate):
        raise ValueError(f"Invalid ATT&CK object ID: {raw!r}")
    return candidate


def validate_query(raw: str) -> str:
    """Validate a free-text search query."""
    text = (raw or "").strip()
    if not text:
        raise ValueError("Search query must not be empty")
    if len(text) > _MAX_QUERY_LEN:
        raise ValueError(f"Query exceeds {_MAX_QUERY_LEN} chars")
    if "\x00" in text:
        raise ValueError("Query contains null bytes")
    return text


def validate_platform(raw: str) -> str:
    """Validate a matrix platform filter (empty means all)."""
    if not raw:
        return ""
    candidate = raw.strip()
    lowered = candidate.lower()
    if lowered not in _PLATFORM_ALLOWLIST:
        raise ValueError(f"Unknown platform: {raw!r}")
    return {"windows": "Windows", "linux": "Linux", "macos": "macOS"}[lowered]


def _slug(text: str) -> str:
    """Make a filesystem-safe slug (alphanumeric, dash, underscore)."""
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", text.strip())[:60]
    return cleaned.strip("_") or "query"


def _run_ttpscope(args: list[str]) -> tuple[int, str, str]:
    """Run the binary with argv list-form and capped output."""
    binary = locate_binary()
    if binary is None:
        raise FileNotFoundError(
            "ttpscope binary not found. Build it: "
            "cmake -S external/.exploit/ttpscope -B external/.exploit/ttpscope/build "
            "&& cmake --build external/.exploit/ttpscope/build"
        )
    from core.safe_exec import safe_run_argv

    completed = safe_run_argv([str(binary)] + args, timeout=_TIMEOUT_S)
    stdout = (completed.stdout or "")[:_MAX_OUTPUT_BYTES]
    stderr = (completed.stderr or "")[:_MAX_OUTPUT_BYTES]
    return completed.returncode, stdout, stderr


def _cache_dataset_path() -> Path:
    """Return the shared STIX bundle path (same layout as ttpscope)."""
    xdg = os.environ.get("XDG_CACHE_HOME", "").strip()
    base = Path(xdg) if xdg else Path.home() / ".cache"
    return base / "ttpscope" / "enterprise-attack.json"


def _fallback_sync() -> dict[str, Any]:
    """Download the Enterprise STIX bundle without the ttpscope binary.

    Uses stdlib urllib only. The bundle lands at the same cache path
    the binary uses, so a later ttpscope install works offline at once.
    """
    import urllib.request

    dest = _cache_dataset_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        _FALLBACK_DATA_URL, headers={"User-Agent": "LazyOwn-ttpscope-bridge/1.0"}
    )
    total = 0
    tmp = dest.with_suffix(".tmp")
    try:
        with urllib.request.urlopen(request, timeout=_TIMEOUT_S) as response, open(tmp, "wb") as fh:
            while True:
                chunk = response.read(65536)
                if not chunk:
                    break
                total += len(chunk)
                if total > _FALLBACK_MAX_DOWNLOAD_BYTES:
                    raise ValueError("STIX bundle exceeds size cap")
                fh.write(chunk)
        if total < 1024:
            raise ValueError("Downloaded dataset is invalid")
        os.replace(tmp, dest)
    except Exception:
        try:
            if tmp.exists():
                tmp.unlink()
        except OSError:
            pass
        raise
    summary = f"Dataset synced ({total} bytes) -> {dest} [fallback backend]"
    path = _stage("sync", "bundle", summary)
    return {"returncode": 0, "staged": str(path), "output": summary, "backend": "fallback"}


def _load_stix_bundle() -> dict[str, Any] | None:
    """Load the cached STIX bundle, or None when absent/corrupt."""
    import json as _json

    dest = _cache_dataset_path()
    try:
        if not dest.exists() or dest.stat().st_size > _FALLBACK_MAX_DOWNLOAD_BYTES:
            return None
        with dest.open("r", encoding="utf-8") as fh:
            data = _json.load(fh)
        if not isinstance(data, dict) or "objects" not in data:
            return None
        return data
    except Exception as exc:
        log.warning("fallback STIX load failed: %s", exc)
        return None


def _stix_external_id(obj: dict[str, Any]) -> str:
    """Extract the MITRE external ID from a STIX object."""
    for ref in obj.get("external_references", []) or []:
        if isinstance(ref, dict) and ref.get("source_name") == "mitre-attack":
            return str(ref.get("external_id", ""))
    return ""


def _stix_index(bundle: dict[str, Any]) -> tuple[dict[str, dict], dict[str, dict]]:
    """Build (by_external_id, by_stix_id) indexes for live objects."""
    by_ext: dict[str, dict] = {}
    by_id: dict[str, dict] = {}
    for obj in bundle.get("objects", []) or []:
        if not isinstance(obj, dict):
            continue
        if obj.get("revoked") or obj.get("x_mitre_deprecated"):
            continue
        by_id[str(obj.get("id", ""))] = obj
        ext = _stix_external_id(obj)
        if ext:
            by_ext[ext.upper()] = obj
    return by_ext, by_id


def _fallback_search_bundle(query: str, limit: int = 20) -> dict[str, Any]:
    """Search the cached STIX bundle (all object types, no binary)."""
    bundle = _load_stix_bundle()
    if bundle is None:
        return _fallback_search_parquet(query, limit)
    needle = query.lower()
    hits: list[str] = []
    for obj in bundle.get("objects", []) or []:
        if not isinstance(obj, dict) or obj.get("revoked") or obj.get("x_mitre_deprecated"):
            continue
        if obj.get("type") == "relationship":
            continue
        aliases = " ".join(str(a) for a in (obj.get("aliases") or obj.get("x_mitre_aliases") or []) if a)
        haystack = f"{_stix_external_id(obj)} {obj.get('name', '')} {aliases} {obj.get('description', '')[:500]}".lower()
        if needle in haystack:
            ext = _stix_external_id(obj) or "-"
            hits.append(f"{ext:13s} {str(obj.get('type', '')):14s} {obj.get('name', '')}")
        if len(hits) >= _FALLBACK_MAX_SEARCH_ROWS:
            break
    text = "\n".join(hits[:limit]) or f"No matches for '{query}' in cached bundle."
    path = _stage("search", _slug(query), text)
    return {"returncode": 0 if hits else 3, "query": query, "staged": str(path), "output": text, "backend": "fallback-stix"}


def _load_parquet(name: str) -> Any | None:
    """Load a parquet knowledge base, or None when unavailable."""
    try:
        import pandas as pd  # type: ignore

        target = _BASE_DIR / "parquets" / f"{name}.parquet"
        if not target.exists():
            return None
        return pd.read_parquet(target)
    except Exception as exc:
        log.warning("fallback parquet load failed (%s): %s", name, exc)
        return None


def _load_atomic_parquet() -> Any | None:
    """Return the first non-empty Atomic catalogue parquet, or None."""
    for name in ("techniques_enriched", "techniques"):
        df = _load_parquet(name)
        if df is not None and not df.empty:
            return df
    return None


def _fallback_search_parquet(query: str, limit: int = 20) -> dict[str, Any]:
    """Search the Atomic catalogue when neither binary nor bundle exists."""
    df = _load_atomic_parquet()
    if df is None or df.empty:
        raise FileNotFoundError(
            "No backend available: install ttpscope, run "
            "'ttpscope action=sync', or ensure parquets/techniques*.parquet exist."
        )
    needle = query.lower()
    lines: list[str] = []
    for _, row in df.iterrows():
        haystack = f"{row.get('mitre_id', '')} {row.get('name', '')} {str(row.get('description', ''))[:400]}".lower()
        if needle in haystack:
            lines.append(f"{row.get('mitre_id', '-'):13s} technique    {row.get('name', '')}")
        if len(lines) >= limit:
            break
    text = "\n".join(lines) or f"No matches for '{query}' in parquet catalogue."
    path = _stage("search", _slug(query), text)
    return {"returncode": 0 if lines else 3, "query": query, "staged": str(path), "output": text, "backend": "fallback-parquet"}


def _fallback_show_bundle(object_id: str) -> dict[str, Any] | None:
    """Show one object from the cached STIX bundle (None when absent)."""
    bundle = _load_stix_bundle()
    if bundle is None:
        return None
    by_ext, by_id = _stix_index(bundle)
    obj = by_ext.get(object_id.upper())
    if obj is None:
        text = (
            f"Object {object_id} not in cached bundle.\n"
            f"See https://attack.mitre.org/search?query={object_id}"
        )
        path = _stage("show", object_id.replace(".", "_"), text)
        return {"returncode": 3, "object_id": object_id, "staged": str(path), "output": text, "backend": "fallback-stix"}
    lines = [
        f"{object_id}  {obj.get('name', '')}  ({obj.get('type', '')})",
        "",
        str(obj.get("description", ""))[:4000],
        "",
    ]
    tactics = sorted({p.get("phase_name", "") for p in obj.get("kill_chain_phases", []) or [] if isinstance(p, dict)})
    if tactics:
        lines.append(f"Tactics: {', '.join(tactics)}")
    platforms = ", ".join(str(p) for p in (obj.get("x_mitre_platforms", []) or []))
    if platforms:
        lines.append(f"Platforms: {platforms}")
    stix_id = str(obj.get("id", ""))
    rels = [
        o for o in bundle.get("objects", []) or []
        if isinstance(o, dict) and o.get("type") == "relationship"
        and stix_id in (str(o.get("source_ref", "")), str(o.get("target_ref", "")))
    ][:30]
    if rels:
        lines.append("")
        lines.append(f"Relationships ({len(rels)} shown, {object_id} <-> other):")
        for rel in rels:
            other_id = str(rel.get("target_ref", "")) if str(rel.get("source_ref", "")) == stix_id else str(rel.get("source_ref", ""))
            other = by_id.get(other_id, {})
            other_ext = _stix_external_id(other) or other_id[:30]
            lines.append(f"  - {rel.get('relationship_type', '')}: {other_ext} {other.get('name', '')}")
    lines.append("")
    lines.append(f"Ref: https://attack.mitre.org/search?query={object_id}")
    text = "\n".join(lines)[:12000]
    path = _stage("show", object_id.replace(".", "_"), text)
    return {"returncode": 0, "object_id": object_id, "staged": str(path), "output": text, "backend": "fallback-stix"}


def _fallback_show_parquet(object_id: str) -> dict[str, Any]:
    """Show Atomic tests for a technique from parquets (T* IDs only)."""
    upper = object_id.upper()
    if not upper.startswith("T"):
        text = (
            f"Offline fallback covers techniques (T*) only; {object_id} needs "
            f"the STIX bundle (run 'ttpscope action=sync') or the binary.\n"
            f"See https://attack.mitre.org/search?query={object_id}"
        )
        path = _stage("show", object_id.replace(".", "_"), text)
        return {"returncode": 3, "object_id": object_id, "staged": str(path), "output": text, "backend": "fallback-parquet"}
    df = _load_atomic_parquet()
    if df is None or df.empty:
        raise FileNotFoundError("No backend available: run 'ttpscope action=sync' first.")
    matches = df[df["mitre_id"].str.upper() == upper]
    if matches.empty:
        prefix = upper.split(".")[0]
        matches = df[df["mitre_id"].str.upper().str.startswith(prefix)]
    lines = [f"{upper} — {len(matches)} Atomic test(s) [parquet fallback]", ""]
    for _, row in matches.head(10).iterrows():
        plats = row.get("platform_list", row.get("platforms", []))
        try:
            plats = ", ".join(list(plats))
        except TypeError:
            plats = str(plats)
        lines.append(f"[{row.get('mitre_id', '')}] {row.get('name', '')} ({plats})")
        lines.append(f"  {str(row.get('description', ''))[:300]}")
    lines.append("")
    lines.append(f"Ref: https://attack.mitre.org/techniques/{upper.replace('.', '/')}")
    text = "\n".join(lines)[:12000]
    path = _stage("show", object_id.replace(".", "_"), text)
    return {"returncode": 0, "object_id": object_id, "staged": str(path), "output": text, "backend": "fallback-parquet"}


def _fallback_matrix_bundle(platform: str) -> dict[str, Any] | None:
    """Render a tactic-grouped matrix from the cached STIX bundle."""
    bundle = _load_stix_bundle()
    if bundle is None:
        return None
    wanted = platform.lower()
    grid: dict[str, list[str]] = {t: [] for t in _TACTIC_ORDER}
    for obj in bundle.get("objects", []) or []:
        if not isinstance(obj, dict) or obj.get("type") != "attack-pattern":
            continue
        if obj.get("revoked") or obj.get("x_mitre_deprecated"):
            continue
        if wanted:
            plats = [str(p).lower() for p in (obj.get("x_mitre_platforms", []) or [])]
            if wanted not in plats and not any(wanted in p for p in plats):
                continue
        tactics = [p.get("phase_name", "") for p in obj.get("kill_chain_phases", []) or [] if isinstance(p, dict)]
        ext = _stix_external_id(obj)
        for tactic in tactics:
            if tactic in grid:
                grid[tactic].append(f"{ext} {obj.get('name', '')}")
    lines = [f"Enterprise matrix (platform: {platform or 'all'}) [STIX fallback]", ""]
    for tactic in _TACTIC_ORDER:
        rows = sorted(set(grid[tactic]))
        lines.append(f"== {tactic} ({len(rows)}) ==")
        lines.extend(f"  {row}" for row in rows[:40])
    text = "\n".join(lines)[:12000]
    path = _stage("matrix", (platform or "all").lower(), text)
    return {"returncode": 0, "platform": platform or "all", "staged": str(path), "output": text, "backend": "fallback-stix"}


def _notes_dir() -> Path:
    """Return the notes directory (same layout as ttpscope)."""
    xdg = os.environ.get("XDG_DATA_HOME", "").strip()
    base = Path(xdg) if xdg else Path.home() / ".local" / "share"
    return base / "ttpscope" / "notes"


def _fallback_note(object_id: str, text: str) -> dict[str, Any]:
    """Append a timestamped Markdown note without the binary."""
    body = (text or "").strip()
    if not body:
        raise ValueError("Note text must not be empty")
    if len(body) > _MAX_NOTE_LEN:
        raise ValueError(f"Note exceeds {_MAX_NOTE_LEN} chars")
    if "\x00" in body:
        raise ValueError("Note contains null bytes")
    notes_dir = _notes_dir()
    notes_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    target = notes_dir / f"{object_id}.md"
    with target.open("a", encoding="utf-8") as fh:
        fh.write(f"\n## {stamp}\n\n{body}\n")
    summary = f"Note added to {object_id} ({target}) [fallback backend]"
    path = _stage("note", object_id.replace(".", "_"), summary)
    return {"returncode": 0, "object_id": object_id, "staged": str(path), "output": summary, "backend": "fallback-notes"}


def _fallback_notes(object_id: str) -> dict[str, Any]:
    """Read Markdown notes without the binary."""
    target = _notes_dir() / f"{object_id}.md"
    if target.exists():
        text = target.read_text(encoding="utf-8", errors="replace")[:8000]
    else:
        text = f"No notes for {object_id}."
    path = _stage("notes", object_id.replace(".", "_"), text)
    return {"returncode": 0, "object_id": object_id, "staged": str(path), "output": text, "backend": "fallback-notes"}


def _fallback_matrix_parquet(platform: str) -> dict[str, Any]:
    """Render a technique-prefix matrix from parquets (degraded, no tactics)."""
    df = _load_atomic_parquet()
    if df is None or df.empty:
        raise FileNotFoundError("No backend available: run 'ttpscope action=sync' first.")
    wanted = platform.lower()
    if wanted and "platform_list" in df.columns:
        def _as_list(value: object) -> list[str]:
            if value is None:
                return []
            if hasattr(value, "tolist"):
                return [str(x).lower() for x in value.tolist()]  # type: ignore
            if isinstance(value, list):
                return [str(x).lower() for x in value]
            return []

        df = df[df["platform_list"].apply(lambda lst: wanted in _as_list(lst))]
    groups: dict[str, int] = {}
    for _, row in df.iterrows():
        prefix = str(row.get("mitre_id", "")).split(".")[0]
        groups[prefix] = groups.get(prefix, 0) + 1
    lines = [
        f"Technique matrix (platform: {platform or 'all'}) [parquet fallback, grouped by prefix]",
        "",
    ]
    for prefix in sorted(groups):
        lines.append(f"  {prefix}: {groups[prefix]} test(s)")
    text = "\n".join(lines)[:12000]
    path = _stage("matrix", (platform or "all").lower(), text)
    return {"returncode": 0, "platform": platform or "all", "staged": str(path), "output": text, "backend": "fallback-parquet"}


def _stage(action: str, slug: str, stdout: str, extra: dict[str, Any] | None = None) -> Path:
    """Stage text output under sessions/ and return the path."""
    _SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    path = _SESSIONS_DIR / f"ttpscope_{action}_{slug}_{stamp}.txt"
    path.write_text(stdout, encoding="utf-8", errors="replace")
    if extra:
        json_path = path.with_suffix(".json")
        json_path.write_text(json.dumps(extra, indent=2, ensure_ascii=False)[:_MAX_OUTPUT_BYTES], encoding="utf-8")
    return path


def do_sync() -> dict[str, Any]:
    """Download the Enterprise ATT&CK bundle via ttpscope sync."""
    try:
        code, stdout, stderr = _run_ttpscope(["sync"])
    except FileNotFoundError:
        log.info("ttpscope binary missing — syncing STIX bundle via fallback downloader")
        return _fallback_sync()
    path = _stage("sync", "bundle", stdout + ("\n" + stderr if stderr else ""))
    return {"returncode": code, "staged": str(path), "output": stdout[:4000], "backend": "ttpscope"}


def do_search(query: str) -> dict[str, Any]:
    """Search IDs, names, aliases and descriptions."""
    clean = validate_query(query)
    try:
        code, stdout, stderr = _run_ttpscope(["search", clean])
    except FileNotFoundError:
        log.info("ttpscope binary missing — searching cached STIX/parquet instead")
        return _fallback_search_bundle(clean)
    path = _stage("search", _slug(clean), stdout or stderr)
    return {"returncode": code, "query": clean, "staged": str(path), "output": (stdout or stderr)[:8000], "backend": "ttpscope"}


def do_show(object_id: str) -> dict[str, Any]:
    """Show one ATT&CK object and its relationships."""
    clean = validate_object_id(object_id)
    try:
        code, stdout, stderr = _run_ttpscope(["show", clean])
    except FileNotFoundError:
        log.info("ttpscope binary missing — reading cached STIX/parquet instead")
        bundled = _fallback_show_bundle(clean)
        if bundled is not None:
            return bundled
        return _fallback_show_parquet(clean)
    path = _stage("show", clean.replace(".", "_"), stdout or stderr)
    return {"returncode": code, "object_id": clean, "staged": str(path), "output": (stdout or stderr)[:12000], "backend": "ttpscope"}


def do_matrix(platform: str = "") -> dict[str, Any]:
    """Render the Enterprise matrix, optionally filtered by platform."""
    clean_platform = validate_platform(platform)
    args = ["matrix"] if not clean_platform else ["matrix", "--platform", clean_platform]
    try:
        code, stdout, stderr = _run_ttpscope(args)
    except FileNotFoundError:
        log.info("ttpscope binary missing — rendering matrix from cache instead")
        bundled = _fallback_matrix_bundle(clean_platform)
        if bundled is not None:
            return bundled
        return _fallback_matrix_parquet(clean_platform)
    path = _stage("matrix", clean_platform.lower() or "all", stdout or stderr)
    return {"returncode": code, "platform": clean_platform or "all", "staged": str(path), "output": (stdout or stderr)[:12000], "backend": "ttpscope"}


def do_note(object_id: str, text: str) -> dict[str, Any]:
    """Append a timestamped research note."""
    clean = validate_object_id(object_id)
    body = (text or "").strip()
    if not body:
        raise ValueError("Note text must not be empty")
    if len(body) > _MAX_NOTE_LEN:
        raise ValueError(f"Note exceeds {_MAX_NOTE_LEN} chars")
    if "\x00" in body:
        raise ValueError("Note contains null bytes")
    try:
        code, stdout, stderr = _run_ttpscope(["note", clean, body])
    except FileNotFoundError:
        log.info("ttpscope binary missing — appending Markdown note directly")
        return _fallback_note(clean, body)
    path = _stage("note", clean.replace(".", "_"), stdout or stderr)
    return {"returncode": code, "object_id": clean, "staged": str(path), "output": (stdout or stderr)[:2000], "backend": "ttpscope"}


def do_notes(object_id: str) -> dict[str, Any]:
    """Read research notes for an object."""
    clean = validate_object_id(object_id)
    try:
        code, stdout, stderr = _run_ttpscope(["notes", clean])
    except FileNotFoundError:
        log.info("ttpscope binary missing — reading Markdown notes directly")
        return _fallback_notes(clean)
    path = _stage("notes", clean.replace(".", "_"), stdout or stderr)
    return {"returncode": code, "object_id": clean, "staged": str(path), "output": (stdout or stderr)[:8000], "backend": "ttpscope"}


def do_chain(object_id: str, platform: str = "linux", limit: int = 5) -> dict[str, Any]:
    """Join ttpscope context with Atomic tests and parquet techniques.

    Does not execute anything on a target. Returns a JSON-ready dict
    for MCP agents and the autonomous loop to emulate the technique.
    """
    clean = validate_object_id(object_id)
    platform_norm = (platform or "linux").strip().lower()
    if platform_norm not in {"windows", "linux", "macos"}:
        raise ValueError(f"Unknown chain platform: {platform!r}")
    capped = max(1, min(int(limit), 10))

    ttp: dict[str, Any] = {"error": "ttpscope binary unavailable"}
    try:
        ttp = do_show(clean)
    except FileNotFoundError as exc:
        ttp = {"error": str(exc)}

    atomic_tests: list[dict[str, Any]] = []
    if clean.startswith("T"):
        try:
            sys.path.insert(0, str(_BASE_DIR / "modules"))
            from atomic_resolver import get_resolver

            resolver = get_resolver()
            atomic_tests = [t.to_dict() for t in resolver.list_for_technique(clean, platform=platform_norm)[:capped]]
        except ValueError:
            atomic_tests = []
        except Exception as exc:
            log.warning("chain atomic lookup failed: %s", exc)

    parquet_hits: list[dict[str, Any]] = []
    try:
        sys.path.insert(0, str(_BASE_DIR / "skills"))
        from lazyown_parquet_db import get_pdb

        pdb = get_pdb(_BASE_DIR)
        if pdb is not None:
            parquet_hits = pdb.query_atomic(
                mitre_id=clean, platform=platform_norm, limit=capped
            )
    except Exception as exc:
        log.warning("chain parquet lookup failed: %s", exc)

    payload = {
        "object_id": clean,
        "platform": platform_norm,
        "ttpscope": {"staged": ttp.get("staged", ""), "output": str(ttp.get("output", ""))[:6000]},
        "atomic_tests": [
            {
                "guid": t.get("guid", ""),
                "name": t.get("name", ""),
                "mitre_id": t.get("mitre_id", ""),
                "platforms": t.get("platforms", []),
                "command_preview": str(t.get("command", ""))[:300],
                "mitre_url": t.get("mitre_url", ""),
            }
            for t in atomic_tests
        ],
        "parquet": parquet_hits[:capped],
        "next": (
            f"Emulate with: atomic_tests {clean} / atomic_gen <guid> "
            f"or lazyown_atomic_search(mitre_id='{clean}', platform='{platform_norm}')"
        ),
    }
    path = _stage("chain", clean.replace(".", "_"), json.dumps(payload, indent=2, ensure_ascii=False), extra=payload)
    payload["staged"] = str(path)
    return payload


def run_action(action: str, **kwargs: Any) -> dict[str, Any]:
    """Dispatch a validated action (used by CLI addons and MCP)."""
    normalized = (action or "").strip().lower()
    if normalized not in _ACTION_ALLOWLIST:
        raise ValueError(f"Unknown ttpscope action: {action!r}")
    if normalized == "sync":
        return do_sync()
    if normalized == "search":
        return do_search(str(kwargs.get("query", "")))
    if normalized == "show":
        return do_show(str(kwargs.get("object_id", kwargs.get("technique_id", ""))))
    if normalized == "matrix":
        return do_matrix(str(kwargs.get("platform", "")))
    if normalized == "note":
        return do_note(str(kwargs.get("object_id", "")), str(kwargs.get("text", kwargs.get("note_text", ""))))
    if normalized == "notes":
        return do_notes(str(kwargs.get("object_id", "")))
    if normalized == "version":
        code, stdout, stderr = _run_ttpscope(["version"])
        return {"returncode": code, "output": (stdout or stderr)[:500]}
    return do_chain(
        str(kwargs.get("object_id", kwargs.get("technique_id", ""))),
        platform=str(kwargs.get("platform", "linux")),
        limit=int(kwargs.get("limit", 5)),
    )


def main() -> None:
    """CLI entry point for the lazyaddon execute_command."""
    parser = argparse.ArgumentParser(description="LazyOwn TTPScope bridge (agent-safe)")
    parser.add_argument("action", choices=sorted(_ACTION_ALLOWLIST))
    parser.add_argument("--query", default="")
    parser.add_argument("--id", default="", dest="object_id")
    parser.add_argument("--platform", default="")
    parser.add_argument("--text", default="")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--json", action="store_true", help="Print JSON result to stdout")
    args = parser.parse_args()
    try:
        result = run_action(
            args.action,
            query=args.query,
            object_id=args.object_id,
            platform=args.platform,
            text=args.text,
            limit=args.limit,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(f"ttpscope error: {exc}")
        raise SystemExit(2)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    else:
        print(result.get("output", ""))
        if result.get("staged"):
            print(f"Staged: {result['staged']}")
        if result.get("next"):
            print(result["next"])


if __name__ == "__main__":
    main()
