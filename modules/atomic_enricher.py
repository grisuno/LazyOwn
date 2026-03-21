"""
atomic_enricher.py — Enrich techniques.parquet with structured derived columns.

Reads  parquets/techniques.parquet  (1690 Atomic Red Team tests, already present)
Writes parquets/techniques_enriched.parquet  (same rows + 6 new columns)

New columns
-----------
platform_list : List[str]   normalised platform list  ['linux','windows','macos',...]
scope         : str          'local' | 'remote' | 'elevated' | 'any'
has_prereqs   : bool         prereq_command is non-empty
complexity    : str          'low' | 'medium' | 'high'  (from command line count)
tactic_prefix : str          'T1003' extracted from mitre_id 'T1003.007'
keyword_tags  : List[str]    top meaningful tokens from name (stop-words removed)

Public API
----------
enrich()        -> pd.DataFrame   build enriched dataframe + save
load_enriched() -> pd.DataFrame   load existing enriched parquet (build if missing)
"""

from __future__ import annotations

import re
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

log = logging.getLogger(__name__)

try:
    import pandas as pd
    import numpy as np
    _PANDAS_OK = True
except ImportError:
    _PANDAS_OK = False

PARQUETS_DIR = Path(__file__).parent.parent / "parquets"
SRC_PARQUET  = PARQUETS_DIR / "techniques.parquet"
DST_PARQUET  = PARQUETS_DIR / "techniques_enriched.parquet"

# Words to strip when building keyword_tags
_STOP = {
    "a","an","the","and","or","for","with","from","on","in","to","of","by",
    "using","via","via","as","at","is","are","be","use","uses","run","runs",
    "create","creates","set","sets","local","remote","elevated","windows",
    "linux","macos","freebsd","cloud","aws","azure","gcp","test","atomic",
    "technique","techniques","method","methods","powershell","cmd","bash","sh",
    "python","python3","script","scripts","command","commands","file","files",
    "registry","process","service","system","user","admin","domain",
}

# Scope markers in the technique name
_SCOPE_RE = re.compile(r'\b(elevated|remote|local)\b', re.IGNORECASE)

# Complexity thresholds (number of non-empty lines in command)
_COMPLEXITY_HIGH = 10
_COMPLEXITY_MED  = 4


# ── helpers ───────────────────────────────────────────────────────────────────

def _parse_platforms(raw: Any) -> List[str]:
    """Convert numpy array / list / string platform field → sorted list."""
    if raw is None:
        return []
    if hasattr(raw, "tolist"):
        raw = raw.tolist()
    if isinstance(raw, list):
        return sorted({str(p).strip().lower() for p in raw if p})
    # string like "[linux]" or "linux, windows"
    text = str(raw).strip("[]").lower()
    return sorted({p.strip() for p in re.split(r"[,\s]+", text) if p.strip()})


def _parse_scope(name: str) -> str:
    m = _SCOPE_RE.search(str(name))
    if m:
        return m.group(1).lower()
    return "any"


def _parse_complexity(command: str) -> str:
    lines = [l for l in str(command).splitlines() if l.strip()]
    n = len(lines)
    if n >= _COMPLEXITY_HIGH:
        return "high"
    if n >= _COMPLEXITY_MED:
        return "medium"
    return "low"


def _parse_keyword_tags(name: str, description: str = "") -> List[str]:
    text = f"{name} {description[:200]}"
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}", text)
    seen: dict = {}
    for t in tokens:
        tl = t.lower()
        if tl not in _STOP:
            seen[tl] = seen.get(tl, 0) + 1
    ranked = sorted(seen.items(), key=lambda x: x[1], reverse=True)
    return [k for k, _ in ranked[:8]]


def _tactic_prefix(mitre_id: str) -> str:
    if not mitre_id:
        return ""
    return str(mitre_id).split(".")[0].strip()


# ── main enrichment ───────────────────────────────────────────────────────────

def enrich(force: bool = False) -> "pd.DataFrame":
    """
    Build enriched parquet.  Skips if DST_PARQUET already exists (use force=True to rebuild).
    Returns the enriched DataFrame.
    """
    if not _PANDAS_OK:
        raise ImportError("pandas + pyarrow required: pip install pandas pyarrow")

    if DST_PARQUET.exists() and not force:
        log.info("atomic_enricher: %s exists, loading (use force=True to rebuild)", DST_PARQUET)
        return pd.read_parquet(DST_PARQUET)

    if not SRC_PARQUET.exists():
        raise FileNotFoundError(f"Source parquet not found: {SRC_PARQUET}")

    df = pd.read_parquet(SRC_PARQUET)
    log.info("atomic_enricher: enriching %d rows", len(df))

    df["platform_list"] = df["platforms"].apply(_parse_platforms)
    df["scope"]         = df["name"].apply(_parse_scope)
    df["has_prereqs"]   = df["prereq_command"].apply(
        lambda x: bool(x and str(x).strip())
    )
    df["complexity"]    = df["command"].apply(_parse_complexity)
    df["tactic_prefix"] = df["mitre_id"].apply(_tactic_prefix)
    df["keyword_tags"]  = df.apply(
        lambda r: _parse_keyword_tags(r["name"], r.get("description", "")), axis=1
    )

    PARQUETS_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(DST_PARQUET, index=False)
    log.info("atomic_enricher: saved %s  (%d rows, %d columns)", DST_PARQUET, len(df), len(df.columns))
    return df


def _to_pylist(val: Any) -> List[str]:
    """Normalise numpy array / list / None → plain Python list of strings."""
    if val is None:
        return []
    if hasattr(val, "tolist"):
        return [str(x) for x in val.tolist()]
    if isinstance(val, list):
        return [str(x) for x in val]
    return []


def load_enriched() -> "pd.DataFrame":
    """Load enriched parquet, building it first if it doesn't exist.
    Normalises list columns to plain Python lists after loading."""
    if not DST_PARQUET.exists():
        return enrich()
    if not _PANDAS_OK:
        raise ImportError("pandas + pyarrow required: pip install pandas pyarrow")
    df = pd.read_parquet(DST_PARQUET)
    for col in ("platform_list", "keyword_tags"):
        if col in df.columns:
            df[col] = df[col].apply(_to_pylist)
    return df


# ── quick query helper used by parquet_db ─────────────────────────────────────

def query_atomic(
    keyword: str = "",
    mitre_id: str = "",
    platform: str = "",
    scope: str = "",
    has_prereqs: Optional[bool] = None,
    complexity: str = "",
    limit: int = 10,
    include_command: bool = False,
) -> List[Dict[str, Any]]:
    """
    Structured query over the enriched Atomic Red Team technique catalogue.

    Parameters
    ----------
    keyword      : free-text search over name + description + keyword_tags
    mitre_id     : exact match OR prefix (e.g. "T1059" matches T1059, T1059.001, …)
    platform     : 'linux' | 'windows' | 'macos' | 'freebsd' | 'cloud'
    scope        : 'local' | 'remote' | 'elevated' | 'any'
    has_prereqs  : True → only tests with prerequisites; False → no prereqs needed
    complexity   : 'low' | 'medium' | 'high'
    limit        : max results (default 10)
    include_command : include the raw command text in results

    Returns
    -------
    List of dicts with keys:
        id, name, mitre_id, tactic_prefix, platform_list, scope,
        complexity, has_prereqs, keyword_tags,
        description_preview (first 200 chars),
        command_preview     (first 300 chars, only if include_command=True)
    """
    df = load_enriched()

    # ── filters ──────────────────────────────────────────────────────────────
    mask = pd.Series([True] * len(df), index=df.index)

    if keyword:
        kl = keyword.lower()
        mask &= (
            df["name"].str.lower().str.contains(kl, regex=False, na=False)
            | df["description"].str.lower().str.contains(kl, regex=False, na=False)
            | df["keyword_tags"].apply(
                lambda tags: any(kl in t for t in (tags or []))
            )
        )

    if mitre_id:
        ml = mitre_id.upper().strip()
        mask &= (
            df["mitre_id"].str.upper().str.startswith(ml)
            | (df["tactic_prefix"].str.upper() == ml)
        )

    if platform:
        pl = platform.lower()
        mask &= df["platform_list"].apply(lambda lst: pl in (lst or []))

    if scope and scope != "any":
        mask &= df["scope"] == scope.lower()

    if has_prereqs is not None:
        mask &= df["has_prereqs"] == has_prereqs

    if complexity:
        mask &= df["complexity"] == complexity.lower()

    filtered = df[mask].head(limit)

    # ── serialise ─────────────────────────────────────────────────────────────
    results: List[Dict[str, Any]] = []
    for _, row in filtered.iterrows():
        entry: Dict[str, Any] = {
            "id":                  row["id"],
            "name":                row["name"],
            "mitre_id":            row["mitre_id"],
            "tactic_prefix":       row["tactic_prefix"],
            "platform_list":       _to_pylist(row["platform_list"]),
            "scope":               row["scope"],
            "complexity":          row["complexity"],
            "has_prereqs":         bool(row["has_prereqs"]),
            "keyword_tags":        _to_pylist(row["keyword_tags"]),
            "description_preview": str(row.get("description", ""))[:200],
        }
        if include_command:
            entry["command_preview"] = str(row.get("command", ""))[:300]
        results.append(entry)

    return results


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse, json, sys
    sys.path.insert(0, str(Path(__file__).parent))

    parser = argparse.ArgumentParser(description="Atomic Red Team technique enricher")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("enrich",  help="Build techniques_enriched.parquet")
    sub.add_parser("rebuild", help="Force-rebuild even if parquet exists")

    p_q = sub.add_parser("query",  help="Query enriched techniques")
    p_q.add_argument("--keyword",     default="")
    p_q.add_argument("--mitre",       default="", dest="mitre_id")
    p_q.add_argument("--platform",    default="")
    p_q.add_argument("--scope",       default="", choices=["","local","remote","elevated","any"])
    p_q.add_argument("--complexity",  default="", choices=["","low","medium","high"])
    p_q.add_argument("--has-prereqs", action="store_true", default=None, dest="has_prereqs")
    p_q.add_argument("--no-prereqs",  action="store_false",             dest="has_prereqs")
    p_q.add_argument("--limit",       type=int, default=10)
    p_q.add_argument("--command",     action="store_true", dest="include_command")

    sub.add_parser("stats", help="Show enrichment stats")

    args = parser.parse_args()

    if args.cmd in ("enrich", None):
        df = enrich()
        print(f"Enriched: {len(df)} rows, {len(df.columns)} columns → {DST_PARQUET}")
    elif args.cmd == "rebuild":
        df = enrich(force=True)
        print(f"Rebuilt: {len(df)} rows, {len(df.columns)} columns → {DST_PARQUET}")
    elif args.cmd == "query":
        rows = query_atomic(
            keyword=args.keyword,
            mitre_id=args.mitre_id,
            platform=args.platform,
            scope=args.scope,
            has_prereqs=args.has_prereqs,
            complexity=args.complexity,
            limit=args.limit,
            include_command=args.include_command,
        )
        print(f"{len(rows)} results")
        for r in rows:
            print(f"\n  {r['mitre_id']:12s} [{r['complexity']:6s}] [{r['scope']:8s}]  {r['name']}")
            print(f"  platforms: {', '.join(r['platform_list'])}")
            print(f"  tags:      {', '.join(r['keyword_tags'][:5])}")
            print(f"  prereqs:   {r['has_prereqs']}")
            if args.include_command:
                print(f"  command:   {r['command_preview'][:120]}")
    elif args.cmd == "stats":
        df = load_enriched()
        print(f"Rows: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        print(f"\nComplexity distribution:")
        print(df["complexity"].value_counts().to_string())
        print(f"\nScope distribution:")
        print(df["scope"].value_counts().to_string())
        print(f"\nTop platforms:")
        from collections import Counter
        plat_ctr: Counter = Counter()
        for lst in df["platform_list"]:
            for p in _to_pylist(lst):
                plat_ctr[p] += 1
        for p, n in plat_ctr.most_common():
            print(f"  {p}: {n}")
        print(f"\nUnique MITRE tactic prefixes: {df['tactic_prefix'].nunique()}")
        print(f"Has prereqs: {df['has_prereqs'].sum()} / {len(df)}")
