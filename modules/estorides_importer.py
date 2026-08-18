"""
estorides_importer
==================
Bidirectional bridge between Estorides (passive OSINT) and LazyOwn (active pentest).

Feeds LazyOwn host/domain intelligence into Estorides for passive discovery
and imports Estorides-discovered entities back into LazyOwn's database, scope,
and world model — creating a continuous feedback loop.

Data flow:

    LazyOwn (world_model, db_hosts, scope)
         │
         ▼  estorides_seed: extract IPs/domains → estorides discover
    Estorides (cases, STIX, graph, fusion)
         │
         ▼  estorides_import: parse entities → LazyOwn DB + scope
    LazyOwn (enriched: new hosts, expanded scope)
         │
         ▼  lazynmap / nuclei on new targets
    ...

Architecture:

    EstoridesSeedExtractor   - pull LazyOwn surfaces into estorides seeds
    EstoridesCaseReader      - read estorides_cases.sqlite
    EstoridesStixParser      - parse STIX 2.1 bundles
    EstoridesImporter        - import entities into LazyOwn DB/scope
    FeedbackLoop             - orchestrate the bidirectional cycle
"""

from __future__ import annotations

import ipaddress
import json
import logging
import os
import sqlite3
import subprocess
import sys
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

log = logging.getLogger("estorides_importer")

ESTORIDES_DIR = Path(
    os.environ.get(
        "ESTORIDES_DIR",
        str(Path(__file__).resolve().parent.parent / "external" / ".exploit" / "estorides"),
    )
)
ESTORIDES_CLI = ESTORIDES_DIR / "estorides_cli.py"
ESTORIDES_DATA = ESTORIDES_DIR / "data"
ESTORIDES_CASES_DB = ESTORIDES_DATA / "estorides_cases.sqlite"
ESTORIDES_STIX = ESTORIDES_DATA / "estorides_stix_bundle.json"
ESTORIDES_GRAPHML = ESTORIDES_DATA / "estorides_graph.graphml"

ENTITY_TYPE_MAP: dict[str, str] = {
    "ipv4": "ipv4",
    "ipv6": "ipv6",
    "domain": "domain",
    "email": "email",
    "url": "url",
    "cve": "cve",
    "asn": "asn",
    "md5": "hash",
    "sha1": "hash",
    "sha256": "hash",
    "mac": "mac",
    "btc_address": "crypto",
    "eth_address": "crypto",
    "phone_e164": "phone",
    "person": "person",
    "org": "org",
    "country": "country",
}

HOST_ENTITY_TYPES = frozenset({"ipv4", "ipv6", "domain", "url", "asn"})


@dataclass
class EstoridesEntity:
    """A single entity discovered by Estorides."""

    entity_type: str
    value: str
    source: str = ""
    confidence: float = 1.0
    sources: list[str] = field(default_factory=list)
    case_id: str = ""


@dataclass
class ImportResult:
    """Result of an estorides import operation."""

    entities_total: int = 0
    hosts_added: int = 0
    hosts_existing: int = 0
    domains_found: int = 0
    ips_found: int = 0
    cves_found: int = 0
    emails_found: int = 0
    scope_entries_added: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return len(self.errors) == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "entities_total": self.entities_total,
            "hosts_added": self.hosts_added,
            "hosts_existing": self.hosts_existing,
            "domains_found": self.domains_found,
            "ips_found": self.ips_found,
            "cves_found": self.cves_found,
            "emails_found": self.emails_found,
            "scope_entries_added": self.scope_entries_added,
            "errors": self.errors,
        }


@dataclass
class SeedResult:
    """Result of seeding estorides with LazyOwn hosts."""

    seeds_sent: int = 0
    cases_created: list[str] = field(default_factory=list)
    entities_discovered: int = 0
    domains_discovered: list[str] = field(default_factory=list)
    ips_discovered: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def new_assets(self) -> list[str]:
        return self.domains_discovered + self.ips_discovered


def extract_seeds_from_world_model(world_model_path: Path | None = None) -> list[tuple[str, str]]:
    """Extract IPs and domains from world_model.json as estorides seeds.

    Returns list of (type, value) tuples suitable for estorides discover.
    """
    import json as _json

    if world_model_path is None:
        world_model_path = Path("sessions") / "world_model.json"
    seeds: list[tuple[str, str]] = []
    seen: set[str] = set()

    if not world_model_path.exists():
        return seeds

    try:
        wm = _json.loads(world_model_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        log.warning("Failed to read world model: %s", e)
        return seeds

    hosts = wm.get("hosts", {})
    for ip, host_data in hosts.items():
        if not isinstance(host_data, dict):
            continue
        key = ip.strip()
        if key and key not in seen:
            seen.add(key)
            seeds.append(("ipv4" if "." in key else "domain", key))
    return seeds


def extract_seeds_from_hosts_file(path: Path | None = None) -> list[tuple[str, str]]:
    """Extract IPs/domains from hostsdiscovery.txt or similar.

    Returns list of (type, value) tuples.
    """
    if path is None:
        path = Path("sessions") / "hostsdiscovery.txt"
    seeds: list[tuple[str, str]] = []
    seen: set[str] = set()

    if not path.exists():
        return seeds

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line in seen:
            continue
        seen.add(line)
        try:
            ipaddress.ip_address(line)
            seeds.append(("ipv4", line))
        except ValueError:
            seeds.append(("domain", line))
    return seeds


def extract_seeds_from_db(db_path: str | None = None) -> list[tuple[str, str]]:
    """Extract hosts from LazyOwn database.

    Returns list of (type, value) tuples.
    """
    if db_path is None:
        db_path = os.path.join("sessions", "db", "lazyown.db")
    seeds: list[tuple[str, str]] = []
    seen: set[str] = set()

    if not os.path.isfile(db_path):
        return seeds

    try:
        from modules.db import LazyOwnDB
        db = LazyOwnDB(db_path)
        ws_name = os.environ.get("LAZYOWN_WORKSPACE", "default")
        ws = db.workspace_get(ws_name)
        if ws is None:
            return seeds
        hosts = db.host_list(int(ws["id"]))
        for h in hosts:
            addr = h.get("address", "").strip()
            if not addr or addr in seen:
                continue
            seen.add(addr)
            try:
                ipaddress.ip_address(addr)
                seeds.append(("ipv4", addr))
            except ValueError:
                seeds.append(("domain", addr))
    except Exception as e:
        log.warning("Failed to read LazyOwn DB: %s", e)
        return seeds

    return seeds


def extract_seeds_from_scope(scope_entries: list[str] | None = None) -> list[tuple[str, str]]:
    """Extract scoped IPs/domains from payload.json scope list.

    Returns list of (type, value) tuples.
    """
    if scope_entries is None:
        config_path = Path("payload.json")
        if not config_path.exists():
            return []
        try:
            cfg = json.loads(config_path.read_text(encoding="utf-8"))
            scope_entries = cfg.get("scope", [])
        except (json.JSONDecodeError, OSError):
            return []

    seeds: list[tuple[str, str]] = []
    seen: set[str] = set()
    for entry in (scope_entries or []):
        entry = str(entry).strip()
        if not entry or entry in seen:
            continue
        seen.add(entry)
        try:
            ipaddress.ip_network(entry, strict=False)
            seeds.append(("ipv4", entry))
        except ValueError:
            seeds.append(("domain", entry))
    return seeds


def run_estorides_discover(
    seed_type: str,
    seed_value: str,
    max_depth: int = 2,
    max_steps: int = 15,
    out_json: str | None = None,
    timeout: float = 120.0,
) -> dict[str, Any] | None:
    """Run estorides discover on a single seed.

    Returns the surface JSON dict on success, None on failure.
    """
    if not ESTORIDES_CLI.exists():
        log.error("estorides CLI not found at %s", ESTORIDES_CLI)
        return None

    if out_json is None:
        safe_value = seed_value.replace("/", "_").replace(":", "_")
        out_json = str(ESTORIDES_DATA / f"discover_{seed_type}_{safe_value}.json")

    cmd = [
        sys.executable,
        str(ESTORIDES_CLI),
        "discover",
        seed_value,
        "--type", seed_type,
        "--max-depth", str(max_depth),
        "--max-steps", str(max_steps),
        "--out-json", out_json,
        "--passive-only",
    ]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(ESTORIDES_DIR),
        )
        if proc.returncode != 0:
            log.error("estorides discover failed: %s", proc.stderr[:500])
            return None

        if os.path.isfile(out_json):
            with open(out_json, encoding="utf-8") as fh:
                return json.load(fh)
        return None
    except subprocess.TimeoutExpired:
        log.error("estorides discover timed out for %s:%s", seed_type, seed_value)
        return None
    except Exception as e:
        log.error("estorides discover error: %s", e)
        return None


def run_estorides_run(
    query: str,
    out_json: str | None = None,
    timeout: float = 60.0,
) -> dict[str, Any] | None:
    """Run estorides run (single fan-out) on a query.

    Returns the result JSON dict on success, None on failure.
    """
    if not ESTORIDES_CLI.exists():
        return None

    if out_json is None:
        safe_query = query.replace("/", "_").replace(":", "_")
        out_json = str(ESTORIDES_DATA / f"run_{safe_query}.json")

    cmd = [
        sys.executable,
        str(ESTORIDES_CLI),
        "run",
        query,
        "--out-json", out_json,
        "--passive-only",
        "--timeout", "15",
        "--deadline", "45",
    ]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(ESTORIDES_DIR),
        )
        if proc.returncode != 0:
            log.error("estorides run failed: %s", proc.stderr[:500])
            return None
        if os.path.isfile(out_json):
            with open(out_json, encoding="utf-8") as fh:
                return json.load(fh)
        return None
    except subprocess.TimeoutExpired:
        log.error("estorides run timed out for %s", query)
        return None
    except Exception as e:
        log.error("estorides run error: %s", e)
        return None


class EstoridesCaseReader:
    """Read entities from the estorides case store (SQLite)."""

    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = Path(db_path) if db_path else ESTORIDES_CASES_DB
        self._conn: sqlite3.Connection | None = None

    @property
    def available(self) -> bool:
        return self.db_path.exists()

    def _ensure_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def list_cases(self, limit: int = 20) -> list[dict[str, Any]]:
        if not self.available:
            return []
        conn = self._ensure_conn()
        rows = conn.execute(
            "SELECT id, query, query_type, created_at, status, "
            "source_count, obs_count, entity_count "
            "FROM cases ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_entities(
        self,
        case_id: str | None = None,
        entity_types: Iterable[str] | None = None,
        limit: int = 500,
    ) -> list[EstoridesEntity]:
        """Fetch entities from the case store.

        If case_id is None, fetches from all cases.
        """
        if not self.available:
            return []
        conn = self._ensure_conn()

        if case_id:
            rows = conn.execute(
                "SELECT case_id, type, value, source, confidence, sources_json "
                "FROM case_entities WHERE case_id = ? "
                "ORDER BY type, value LIMIT ?",
                (case_id, limit),
            ).fetchall()
        else:
            where = ""
            params: list[Any] = []
            if entity_types:
                placeholders = ",".join("?" for _ in entity_types)
                where = f"WHERE type IN ({placeholders})"
                params = list(entity_types)
            params.append(limit)
            rows = conn.execute(
                f"SELECT case_id, type, value, source, confidence, sources_json "
                f"FROM case_entities {where} "
                f"ORDER BY type, value LIMIT ?",
                params,
            ).fetchall()

        entities: list[EstoridesEntity] = []
        for r in rows:
            sources = []
            try:
                sources = json.loads(r["sources_json"] or "[]")
            except (json.JSONDecodeError, TypeError):
                pass
            entities.append(
                EstoridesEntity(
                    entity_type=r["type"],
                    value=r["value"],
                    source=r["source"] or "",
                    confidence=float(r["confidence"] or 1.0),
                    sources=sources,
                    case_id=r["case_id"],
                )
            )
        return entities

    def get_host_entities(self, case_id: str | None = None) -> list[EstoridesEntity]:
        """Get entities of host-related types (ipv4, ipv6, domain, url, asn)."""
        return self.get_entities(case_id=case_id, entity_types=HOST_ENTITY_TYPES)

    def get_all_entities(self, case_id: str | None = None) -> list[EstoridesEntity]:
        return self.get_entities(case_id=case_id)

    def stats(self) -> dict[str, Any]:
        if not self.available:
            return {"available": False}
        conn = self._ensure_conn()
        cases = conn.execute("SELECT count(*) FROM cases").fetchone()[0]
        entities = conn.execute("SELECT count(*) FROM case_entities").fetchone()[0]
        return {
            "available": True,
            "db_path": str(self.db_path),
            "cases": cases,
            "entities": entities,
        }

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None


class EstoridesStixParser:
    """Parse STIX 2.1 bundles produced by estorides."""

    STIX_TO_ENTITY: dict[str, str] = {
        "ipv4-addr": "ipv4",
        "ipv6-addr": "ipv6",
        "domain-name": "domain",
        "url": "url",
        "email-addr": "email",
        "vulnerability": "cve",
        "file": "hash",
        "autonomous-system": "asn",
        "mac-addr": "mac",
        "crypto-wallet": "crypto",
    }

    def __init__(self, stix_path: Path | None = None) -> None:
        self.stix_path = Path(stix_path) if stix_path else ESTORIDES_STIX

    @property
    def available(self) -> bool:
        return self.stix_path.exists()

    def parse(self) -> list[EstoridesEntity]:
        """Parse a STIX 2.1 bundle into EstoridesEntity objects."""
        if not self.available:
            return []

        with open(self.stix_path, encoding="utf-8") as fh:
            bundle = json.load(fh)

        entities: list[EstoridesEntity] = []
        if bundle.get("type") != "bundle":
            return entities

        for obj in bundle.get("objects", []):
            stix_type = obj.get("type", "")
            entity_type = self.STIX_TO_ENTITY.get(stix_type)
            if not entity_type:
                continue

            value = self._extract_value(obj, stix_type)
            if not value:
                continue

            sources = obj.get("x_estorides_sources", []) or []

            entities.append(
                EstoridesEntity(
                    entity_type=entity_type,
                    value=str(value),
                    source=sources[0] if sources else "",
                    sources=sources,
                )
            )
        return entities

    def parse_by_type(self, entity_types: Iterable[str] | None = None) -> dict[str, list[str]]:
        """Parse STIX and group values by entity type."""
        all_entities = self.parse()
        result: dict[str, set[str]] = {}
        for ent in all_entities:
            if entity_types and ent.entity_type not in entity_types:
                continue
            result.setdefault(ent.entity_type, set()).add(ent.value)
        return {k: sorted(v) for k, v in result.items()}

    @staticmethod
    def _extract_value(obj: dict[str, Any], stix_type: str) -> str | None:
        if stix_type in ("ipv4-addr", "ipv6-addr", "domain-name", "url", "email-addr", "mac-addr"):
            return obj.get("value")
        if stix_type == "vulnerability":
            return obj.get("name")
        if stix_type == "file":
            hashes = obj.get("hashes", {})
            return hashes.get("SHA-256") or hashes.get("MD5") or hashes.get("SHA-1")
        if stix_type == "autonomous-system":
            num = obj.get("number")
            return f"AS{num}" if num else None
        if stix_type == "crypto-wallet":
            return obj.get("value")
        return None


def ensure_directories() -> None:
    """Ensure sessions/ directories exist."""
    for d in ("sessions", "sessions/db"):
        os.makedirs(d, exist_ok=True)


class EstoridesToLazyOwnBridge:
    """Import estorides-discovered entities into LazyOwn's database and scope."""

    def __init__(
        self,
        db_path: str | None = None,
        config_path: str | None = None,
    ) -> None:
        self.db_path = db_path or os.path.join("sessions", "db", "lazyown.db")
        self.config_path = config_path or "payload.json"

    def import_entities(
        self,
        entities: Iterable[EstoridesEntity],
        add_to_scope: bool = True,
        add_to_db: bool = True,
    ) -> ImportResult:
        """Import entities into LazyOwn DB and optionally scope.

        Args:
            entities: Entities to import.
            add_to_scope: If True, add new IPs/domains to payload.json scope.
            add_to_db: If True, add entities to lazyown.db hosts table.

        Returns:
            ImportResult with counts.
        """
        result = ImportResult()
        ensure_directories()

        entity_list = list(entities)
        result.entities_total = len(entity_list)

        imports: list[tuple[str, str, str]] = []  # (type, value, source)

        for ent in entity_list:
            if ent.entity_type == "cve":
                result.cves_found += 1
            elif ent.entity_type in ("email", "phone_e164"):
                result.emails_found += 1
            elif ent.entity_type in HOST_ENTITY_TYPES:
                if ent.entity_type in ("ipv4", "ipv6"):
                    result.ips_found += 1
                elif ent.entity_type == "domain":
                    result.domains_found += 1
                imports.append((ent.entity_type, ent.value, ent.source))

        if add_to_db and imports:
            self._import_to_db(imports, result)

        if add_to_scope and imports:
            self._import_to_scope(imports, result)

        return result

    def _import_to_db(
        self, imports: list[tuple[str, str, str]], result: ImportResult,
    ) -> None:
        try:
            from modules.db import LazyOwnDB

            db = LazyOwnDB(self.db_path)
            ws_name = os.environ.get("LAZYOWN_WORKSPACE", "default")
            ws = db.workspace_get(ws_name)
            if ws is None:
                db.workspace_create(ws_name)
                ws = db.workspace_get(ws_name)
            if ws is None:
                result.errors.append("DB import error: could not get/create workspace")
                return

            workspace_id: int = int(ws["id"])

            existing_hosts = db.host_list(workspace_id)
            existing = {h["address"] for h in existing_hosts}

            for ent_type, value, source in imports:
                value = str(value).strip()
                if not value:
                    continue
                if value in existing:
                    result.hosts_existing += 1
                    continue
                hostname = value if ent_type == "domain" else ""
                purpose = f"OSINT via estorides ({source})" if source else "OSINT via estorides"
                db.host_add(
                    workspace_id=workspace_id,
                    address=value,
                    hostname=hostname,
                    purpose=purpose,
                    state="discovered",
                )
                result.hosts_added += 1
                existing.add(value)

        except Exception as e:
            result.errors.append(f"DB import error: {e}")
            log.error("DB import failed: %s", e)

    def _import_to_scope(
        self, imports: list[tuple[str, str, str]], result: ImportResult,
    ) -> None:
        try:
            cfg = {}
            if os.path.isfile(self.config_path):
                cfg = json.loads(open(self.config_path, encoding="utf-8").read())

            current_scope: list[str] = list(cfg.get("scope") or [])
            scope_set = set(current_scope)

            for ent_type, value, _source in imports:
                entry = value.strip()
                if not entry:
                    continue
                if entry in scope_set:
                    continue
                current_scope.append(entry)
                scope_set.add(entry)
                result.scope_entries_added += 1

            if result.scope_entries_added > 0:
                cfg["scope"] = current_scope
                tmp = self.config_path + ".tmp"
                with open(tmp, "w", encoding="utf-8") as fh:
                    json.dump(cfg, fh, indent=2, ensure_ascii=False)
                os.replace(tmp, self.config_path)

        except (json.JSONDecodeError, OSError) as e:
            result.errors.append(f"Scope update error: {e}")

    def get_combined_surface(self) -> dict[str, Any]:
        """Get the combined attack surface from LazyOwn DB + scope."""
        surface: dict[str, list[str]] = {
            "from_db": [],
            "from_scope": [],
            "from_world_model": [],
        }

        if os.path.isfile(self.db_path):
            try:
                from modules.db import LazyOwnDB
                db = LazyOwnDB(self.db_path)
                ws_name = os.environ.get("LAZYOWN_WORKSPACE", "default")
                ws = db.workspace_get(ws_name)
                if ws:
                    hosts = db.host_list(int(ws["id"]))
                    surface["from_db"] = [h["address"] for h in hosts if h.get("address")]
                else:
                    ws_id = db.workspace_create(ws_name)
                    hosts = db.host_list(ws_id)
                    surface["from_db"] = [h["address"] for h in hosts if h.get("address")]
            except Exception:
                pass

        if os.path.isfile(self.config_path):
            try:
                cfg = json.loads(open(self.config_path, encoding="utf-8").read())
                surface["from_scope"] = list(cfg.get("scope") or [])
            except (json.JSONDecodeError, OSError):
                pass

        wm_path = os.path.join("sessions", "world_model.json")
        if os.path.isfile(wm_path):
            try:
                wm = json.loads(open(wm_path, encoding="utf-8").read())
                surface["from_world_model"] = list(wm.get("hosts", {}).keys())
            except (json.JSONDecodeError, OSError):
                pass

        all_assets = set()
        for lst in surface.values():
            all_assets.update(lst)
        surface["total_unique"] = len(all_assets)
        return surface


class FeedbackLoop:
    """Orchestrate the bidirectional estorides <-> LazyOwn feedback cycle.

    Each iteration:
      1. Extract seeds from LazyOwn (world model, scope, DB, hosts files)
      2. Feed each seed into estorides discover for passive OSINT
      3. Parse estorides output (cases + STIX)
      4. Import new entities back into LazyOwn DB + scope
      5. New entities become seeds for the next iteration
    """

    def __init__(
        self,
        max_iterations: int = 3,
        max_depth: int = 2,
        max_steps: int = 10,
        timeout: float = 120.0,
    ) -> None:
        self.max_iterations = max_iterations
        self.max_depth = max_depth
        self.max_steps = max_steps
        self.timeout = timeout
        self.bridge = EstoridesToLazyOwnBridge()
        self.case_reader = EstoridesCaseReader()
        self.stix_parser = EstoridesStixParser()
        self.history: list[dict[str, Any]] = []

    def run(self, seed_methods: list[str] | None = None) -> dict[str, Any]:
        """Run the feedback loop.

        Args:
            seed_methods: Which sources to extract seeds from.
                Options: 'world_model', 'hosts_file', 'db', 'scope', 'all'.
                Default: ['world_model', 'hosts_file']

        Returns:
            Dict with iteration summaries and final surface state.
        """
        if seed_methods is None:
            seed_methods = ["world_model", "hosts_file"]

        all_seeds: list[tuple[str, str]] = []
        seen_seeds: set[str] = set()
        total_discovered_entities = 0

        for iteration in range(1, self.max_iterations + 1):
            iter_result: dict[str, Any] = {
                "iteration": iteration,
                "seeds_processed": 0,
                "entities_discovered": 0,
                "new_assets": [],
                "cases": [],
            }

            seeds = self._gather_seeds(seed_methods, seen_seeds)
            if not seeds:
                log.info("No new seeds found. Loop converging.")
                break

            iter_result["seeds_processed"] = len(seeds)
            all_seeds.extend(seeds)

            for seed_type, seed_value in seeds:
                surface = run_estorides_discover(
                    seed_type=seed_type,
                    seed_value=seed_value,
                    max_depth=self.max_depth,
                    max_steps=self.max_steps,
                    timeout=self.timeout,
                )
                if surface is None:
                    continue

                case_id = surface.get("case_id", "")
                if case_id:
                    iter_result["cases"].append(case_id)

                domains = surface.get("domains", [])
                entities = self.case_reader.get_host_entities(case_id=case_id) if case_id else []

                new_for_iter: list[str] = []
                for d in domains:
                    d = str(d).strip()
                    if d and d not in seen_seeds:
                        seen_seeds.add(d)
                        new_for_iter.append(d)
                        all_seeds.append(("domain", d))

                for ent in entities:
                    if ent.value not in seen_seeds:
                        seen_seeds.add(ent.value)
                        new_for_iter.append(ent.value)

                if entities:
                    result = self.bridge.import_entities(
                        entities, add_to_scope=True, add_to_db=True,
                    )
                    iter_result["entities_discovered"] += result.hosts_added

                iter_result["new_assets"].extend(new_for_iter)
                total_discovered_entities += iter_result["entities_discovered"]

            self.history.append(iter_result)

            if not iter_result["new_assets"]:
                log.info("No new assets discovered in iteration %d. Converged.", iteration)
                break

        combined = self.bridge.get_combined_surface()
        return {
            "iterations_completed": len(self.history),
            "total_seeds": len(all_seeds),
            "total_unique_seeds": len(seen_seeds),
            "total_entities_discovered": total_discovered_entities,
            "combined_surface": combined,
            "history": self.history,
        }

    def _gather_seeds(
        self,
        methods: list[str],
        seen: set[str],
    ) -> list[tuple[str, str]]:
        """Gather seeds from specified sources, filtering already-seen."""
        all_raw: list[tuple[str, str]] = []

        if "all" in methods or "world_model" in methods:
            all_raw.extend(extract_seeds_from_world_model())
        if "all" in methods or "hosts_file" in methods:
            all_raw.extend(extract_seeds_from_hosts_file())
        if "all" in methods or "db" in methods:
            all_raw.extend(extract_seeds_from_db())
        if "all" in methods or "scope" in methods:
            all_raw.extend(extract_seeds_from_scope())

        fresh: list[tuple[str, str]] = []
        for stype, sval in all_raw:
            key = f"{stype}:{sval}"
            if key not in seen:
                seen.add(key)
                fresh.append((stype, sval))
        return fresh


def export_combined_graph(output_path: str | None = None) -> Path | None:
    """Export the combined (Estorides + LazyOwn) graph as GraphML."""
    if output_path is None:
        output_path = os.path.join("sessions", "combined_graph.graphml")
    path = Path(output_path)

    try:
        import networkx as nx
    except ImportError:
        log.error("networkx not available")
        return None

    kg = nx.MultiDiGraph()

    if ESTORIDES_GRAPHML.exists():
        try:
            eg = nx.read_graphml(ESTORIDES_GRAPHML)
            for nid, data in eg.nodes(data=True):
                data["source_tool"] = "estorides"
                kg.add_node(nid, **data)
            for u, v, data in eg.edges(data=True):
                data["source_tool"] = "estorides"
                kg.add_edge(u, v, **data)
        except Exception as e:
            log.warning("Failed to load estorides graph: %s", e)

    wm_path = Path("sessions") / "world_model.json"
    if wm_path.exists():
        try:
            wm = json.loads(wm_path.read_text(encoding="utf-8"))
            hosts = wm.get("hosts", {})
            for ip, hdata in hosts.items():
                nid = f"host:{ip}"
                if not isinstance(hdata, dict):
                    hdata = {}
                kg.add_node(nid, type="host", value=ip, source_tool="lazyown",
                            state=hdata.get("state", "unknown"),
                            os=hdata.get("os_hint", ""))
        except Exception as e:
            log.warning("Failed to load world model: %s", e)

    path.parent.mkdir(parents=True, exist_ok=True)
    nx.write_graphml(kg, str(path))
    return path
