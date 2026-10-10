"""MCP verb bridge — one command language for operators and agents.

The MCP server (``skills/lazyown_mcp.py``) exposes workflow verbs that the
operator documentation (ESSENTIALS.md, CHEATSHEET.md) teaches, but those
verbs historically only existed on the agent side, so a human following the
golden path hit ``unknown command``. This CommandSet registers the same
verbs in the interactive shell, delegating to the same underlying modules
the MCP handlers use, so the documented path works end to end:

    ping -> lazynmap -> auto_populate -> facts_show -> recommend_next

Provides:
    auto_populate   Parse the latest nmap XML and fill payload context.
    facts_show      Show structured facts extracted from scans/tool output.
    rag_query       Semantic search over session artefacts.
    parquet_query   Query the parquet knowledge bases (GTFOBins/LOLBas/ATT&CK).
    threat_model    Build or inspect the derived threat model.
    playbook_run    Execute a generated YAML playbook through the shell.
    auto_loop       Run a goal through the daemon orchestrator backend.
    session_state   Alias of ``sitrep`` (MCP name parity).
    campaign_sitrep Alias of ``sitrep`` (MCP name parity).
    timeline        Alias of ``timeline_browser`` (MCP name parity).
"""

from __future__ import annotations

import argparse
import json
import shlex
from pathlib import Path

import defusedxml.ElementTree as ET
from cmd2 import Cmd2ArgumentParser, with_argparser, with_category

from cli.commands._base import LazyOwnCommandSet
from core.config import save_payload
from utils import ai_category, print_error, print_msg, print_warn

SESSIONS_DIR = "sessions"
SCAN_XML_TEMPLATE = "scan_{target}.nmap.xml"
CREDENTIALS_FILE = "credentials.txt"
PLAYBOOK_GLOB = "playbook_*.yaml"
OS_ID_WINDOWS = "2"
OS_ID_GENERIC = "1"
MAX_SERVICES_SHOWN = 20
MAX_RAG_TEXT = 300
MAX_KEYWORD_ROWS = 5


def _build_auto_populate_parser() -> Cmd2ArgumentParser:
    """Return the argparse parser used by ``auto_populate``."""
    parser = Cmd2ArgumentParser(prog="auto_populate")
    parser.add_argument(
        "target",
        nargs="?",
        default="",
        help="target IP or hostname (default: rhost from payload.json)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite payload fields even if already set",
    )
    return parser


def _build_facts_show_parser() -> Cmd2ArgumentParser:
    """Return the argparse parser used by ``facts_show``."""
    parser = Cmd2ArgumentParser(prog="facts_show")
    parser.add_argument(
        "target",
        nargs="?",
        default="",
        help="filter to a specific target IP (default: rhost, empty for all)",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="re-parse sessions/ artefacts before displaying",
    )
    return parser


def _build_rag_query_parser() -> Cmd2ArgumentParser:
    """Return the argparse parser used by ``rag_query``."""
    parser = Cmd2ArgumentParser(prog="rag_query")
    parser.add_argument("query", nargs="+", help="free-text query over session artefacts")
    parser.add_argument("-n", type=int, default=5, help="max hits (default 5)")
    return parser


def _build_parquet_query_parser() -> Cmd2ArgumentParser:
    """Return the argparse parser used by ``parquet_query``."""
    parser = Cmd2ArgumentParser(prog="parquet_query")
    parser.add_argument(
        "--mode",
        choices=("session", "keyword", "context", "stats", "list"),
        default="context",
        help="query mode (default: context)",
    )
    parser.add_argument("--phase", default="recon", help="kill-chain phase filter")
    parser.add_argument("--target", default="", help="target IP filter (default: rhost)")
    parser.add_argument("--keyword", default="", help="keyword for keyword mode")
    parser.add_argument("--parquet", default="", help="restrict keyword search to one parquet")
    parser.add_argument("--success-only", action="store_true", help="session mode: only successful rows")
    parser.add_argument("--limit", type=int, default=15, help="max rows per result set")
    parser.add_argument("--sync", action="store_true", help="re-ingest CSV before querying")
    return parser


def _build_threat_model_parser() -> Cmd2ArgumentParser:
    """Return the argparse parser used by ``threat_model``."""
    parser = Cmd2ArgumentParser(prog="threat_model")
    parser.add_argument(
        "action",
        nargs="?",
        choices=("build", "load", "ttps"),
        default="build",
        help="build regenerates, load shows the cached model, ttps lists techniques",
    )
    return parser


def _build_playbook_run_parser() -> Cmd2ArgumentParser:
    """Return the argparse parser used by ``playbook_run``."""
    parser = Cmd2ArgumentParser(prog="playbook_run")
    parser.add_argument(
        "path",
        nargs="?",
        default="",
        help="playbook YAML path (default: newest sessions/playbook_*.yaml)",
    )
    parser.add_argument("--target", default="", help="override the playbook target")
    parser.add_argument("--dry-run", action="store_true", help="print steps without executing")
    return parser


class McpBridgeCommandSet(LazyOwnCommandSet):
    """CLI shims exposing the documented MCP verbs to human operators."""

    phase = "ai"
    category = ai_category

    @with_category(ai_category)
    @with_argparser(_build_auto_populate_parser())
    def do_auto_populate(self, args: argparse.Namespace) -> None:
        """Parse the latest nmap XML scan and auto-populate payload context.

        Fills domain, os_id, open services and start_user/start_pass from
        ``sessions/scan_<target>.nmap.xml`` and ``sessions/credentials.txt``.
        Run this right after ``lazynmap`` so subsequent commands inherit the
        discovered target context. Mirrors the ``lazyown_auto_populate`` MCP
        tool.
        """
        params = self.params
        target = (args.target or "").strip() or str(params.get("rhost", "") or "")
        if not target:
            print_error("No target specified and rhost not set. Example: assign rhost 10.10.10.10")
            return
        force = bool(args.force)
        changed: list[str] = []
        services_found: list[str] = []

        xml_path = Path(SESSIONS_DIR) / SCAN_XML_TEMPLATE.format(target=target)
        if xml_path.exists():
            try:
                root = ET.parse(str(xml_path)).getroot()
                for hostname in root.iter("hostname"):
                    name = hostname.get("name", "")
                    if name and "." in name:
                        if force or not params.get("domain"):
                            params["domain"] = name
                            changed.append(f"domain={name}")
                        break
                for port_el in root.iter("port"):
                    state_el = port_el.find("state")
                    if state_el is not None and state_el.get("state") == "open":
                        svc_el = port_el.find("service")
                        svc_name = svc_el.get("name", "") if svc_el is not None else ""
                        if svc_name:
                            services_found.append(f"{port_el.get('portid', '')}/{svc_name}")
                for osmatch in root.iter("osmatch"):
                    os_name = osmatch.get("name", "").lower()
                    if os_name:
                        os_id = OS_ID_WINDOWS if "windows" in os_name else OS_ID_GENERIC
                        if force or not params.get("os_id"):
                            params["os_id"] = os_id
                            changed.append(f"os_id={os_id} ({os_name[:40]})")
                        break
                for addr_el in root.iter("address"):
                    if addr_el.get("addrtype") == "ipv4":
                        extra_ip = addr_el.get("addr", "")
                        if extra_ip and extra_ip != target:
                            changed.append(f"discovered_host={extra_ip}")
            except Exception as exc:
                print_warn(f"XML parse error: {exc}")
        else:
            print_warn(f"No XML at {xml_path} — run lazynmap first")

        cred_file = Path(SESSIONS_DIR) / CREDENTIALS_FILE
        if cred_file.exists():
            for raw_line in cred_file.read_text(errors="replace").splitlines():
                entry = raw_line.split("#")[0].strip()
                if ":" in entry:
                    user, _, secret = entry.partition(":")
                    if user and secret:
                        if force or not params.get("start_user"):
                            params["start_user"] = user.strip()
                            params["start_pass"] = secret.strip()
                            changed.append(f"start_user={user.strip()}")
                        break

        if changed:
            try:
                save_payload(dict(params))
            except Exception as exc:
                print_error(f"Error writing payload.json: {exc}")
                return
            self._refresh_aliases()

        print_msg(f"AUTO-POPULATE for target={target}")
        if services_found:
            print_msg("Services: " + ", ".join(services_found[:MAX_SERVICES_SHOWN]))
        if changed:
            print_msg("payload.json updated:")
            for entry in changed:
                print_msg(f"  + {entry}")
        else:
            print_msg("No changes — payload already populated.")

        try:
            from modules.intelligence_engine import get_intelligence_engine

            engine = get_intelligence_engine()
            result = engine.run_full_cycle(target)
            ingested = result.get("facts_ingested", 0)
            if ingested:
                print_msg(f"Intelligence: {ingested} facts ingested, {result.get('assessments_count', 0)} assessments")
        except Exception:
            pass

        try:
            from modules.world_model import get_world_model

            ingested = get_world_model().consume_policy_facts()
            if ingested:
                print_msg(f"World model: ingested {ingested} facts from policy_facts.json")
        except Exception:
            pass

    @with_category(ai_category)
    @with_argparser(_build_facts_show_parser())
    def do_facts_show(self, args: argparse.Namespace) -> None:
        """Show structured facts extracted from nmap scans and tool output.

        Facts include open ports, detected services, discovered credentials,
        accessible shares and achieved access level per target. Mirrors the
        ``lazyown_facts_show`` MCP tool.
        """
        try:
            from skills.lazyown_facts import FactStore
        except Exception as exc:
            print_error(f"FactStore unavailable: {exc}")
            return
        target = (args.target or "").strip() or str(self.params.get("rhost", "") or "") or None
        try:
            store = FactStore()
            if args.refresh:
                store.parse_all(target=target)
            summary = store.summary(target)
        except Exception as exc:
            print_error(f"facts_show failed: {exc}")
            return
        print_msg(summary or "No facts found. Run: facts_show --refresh")

    @with_category(ai_category)
    @with_argparser(_build_rag_query_parser())
    def do_rag_query(self, args: argparse.Namespace) -> None:
        """Semantic search over session artefacts (scans, logs, notes).

        Mirrors the ``lazyown_rag_query`` MCP tool.
        """
        query = " ".join(args.query).strip()
        if not query:
            print_error("Usage: rag_query <query> [-n 5]")
            return
        try:
            from modules.session_rag import get_rag

            rag = get_rag()
            rag.index_new()
            hits = rag.query(query, args.n)
        except Exception as exc:
            print_error(f"rag_query failed: {exc}")
            return
        if not hits:
            print_msg("No results found.")
            return
        print_msg(f"RAG query: '{query}'  ({len(hits)} hits)")
        for index, hit in enumerate(hits, 1):
            score = hit.get("score")
            score_str = f"  score={score:.3f}" if score is not None else ""
            print_msg(f"{index}. [{hit.get('source', '?')}]{score_str}")
            print_msg(str(hit.get("text", "")).strip()[:MAX_RAG_TEXT])

    @with_category(ai_category)
    @with_argparser(_build_parquet_query_parser())
    def do_parquet_query(self, args: argparse.Namespace) -> None:
        """Query the parquet knowledge bases (GTFOBins, LOLBas, ATT&CK, sessions).

        Modes: ``session`` (past command outcomes by phase/target),
        ``keyword`` (search all parquets), ``context`` (phase briefing),
        ``stats`` and ``list``. Mirrors the ``lazyown_parquet_query`` MCP tool.
        """
        try:
            from skills.lazyown_parquet_db import get_pdb

            pdb = get_pdb()
        except Exception as exc:
            print_error(f"ParquetDB unavailable: {exc}. Run: pip install pandas pyarrow")
            return
        if pdb is None:
            print_error("ParquetDB unavailable. Run: pip install pandas pyarrow")
            return
        target = (args.target or "").strip() or str(self.params.get("rhost", "") or "") or None
        try:
            if args.sync:
                pdb.sync()
            if args.mode == "stats":
                result = pdb.stats()
            elif args.mode == "list":
                names = "\n".join(f"  - {name}" for name in pdb.list_parquets())
                result = f"Available parquets:\n{names}"
            elif args.mode == "keyword":
                if not args.keyword:
                    print_error("keyword mode requires --keyword")
                    return
                rows_by_parquet = pdb.query_knowledge(args.keyword, args.parquet or None, limit=args.limit)
                if not rows_by_parquet:
                    result = f"No results for keyword '{args.keyword}'."
                else:
                    parts: list[str] = []
                    for stem, rows in rows_by_parquet.items():
                        parts.append(f"-- {stem} ({len(rows)} matches) --")
                        for row in rows[:MAX_KEYWORD_ROWS]:
                            parts.append(json.dumps({k: str(v)[:100] for k, v in row.items()}, ensure_ascii=False))
                    result = "\n".join(parts)
            elif args.mode == "session":
                rows = pdb.query_session(
                    phase=args.phase,
                    target=target,
                    success_only=args.success_only,
                    limit=args.limit,
                )
                result = (
                    json.dumps(rows, indent=2, default=str)
                    if rows
                    else f"No session rows for phase='{args.phase}' target='{target}'."
                )
            else:
                ctx = pdb.context_for_phase(args.phase, target, limit=args.limit)
                result = json.dumps(ctx, indent=2, default=str)
        except Exception as exc:
            print_error(f"parquet_query failed: {exc}")
            return
        print_msg(result)

    @with_category(ai_category)
    @with_argparser(_build_threat_model_parser())
    def do_threat_model(self, args: argparse.Namespace) -> None:
        """Build or inspect the threat model derived from session events.

        Actions: ``build`` (default) regenerates the model, ``load`` shows the
        cached one, ``ttps`` lists observed ATT&CK techniques. Mirrors the
        ``lazyown_threat_model`` MCP tool.
        """
        try:
            from modules.threat_model import get_builder

            builder = get_builder()
            if args.action == "load":
                model = builder.load()
                if model is None:
                    print_error("No threat model found — run: threat_model build")
                    return
            else:
                model = builder.build()
        except Exception as exc:
            print_error(f"threat_model failed: {exc}")
            return

        if args.action == "ttps":
            ttps = model.get("ttps", [])
            print_msg(f"TTPs ({len(ttps)}):")
            for ttp in ttps:
                print_msg(
                    f"  {ttp['technique_id']:12s} [{ttp['severity']:8s}]  "
                    f"{ttp['technique_name']}  (x{ttp['occurrences']})"
                )
            return

        summary = model.get("summary", {})
        print_msg(f"Threat Model  generated_at={model.get('generated_at', '')}")
        print_msg(
            f"  Assets:          {len(model.get('assets', []))}  (highest risk: {summary.get('highest_risk_asset', '')})"
        )
        print_msg(
            f"  TTPs:            {len(model.get('ttps', []))}  (dominant tactic: {summary.get('dominant_tactic', '')})"
        )
        print_msg(f"  IOCs:            {len(model.get('ioc_registry', []))}")
        print_msg(f"  Detection rules: {len(model.get('detection_rules', []))}")
        print_msg(f"  Total events:    {summary.get('total_events', 0)}")
        print_msg("Top 5 TTPs:")
        for ttp in model.get("ttps", [])[:5]:
            print_msg(
                f"  {ttp['technique_id']:12s} [{ttp['severity']:8s}] {ttp['tactic']:28s} "
                f"{ttp['technique_name']}  (x{ttp['occurrences']})"
            )
        print_msg("Full model: sessions/reports/threat_model.json")

    @with_category(ai_category)
    @with_argparser(_build_playbook_run_parser())
    def do_playbook_run(self, args: argparse.Namespace) -> None:
        """Execute a generated YAML playbook step by step through the shell.

        Each step command runs via the interactive shell so aliases and hooks
        apply. Defaults to the newest ``sessions/playbook_*.yaml``. Mirrors
        the ``lazyown_playbook_run`` MCP tool.
        """
        try:
            from modules.playbook_engine import PlaybookEngine
        except Exception as exc:
            print_error(f"PlaybookEngine unavailable: {exc}")
            return

        pb_path = (args.path or "").strip()
        PLAYS_DIR = Path("playbooks")
        if pb_path:
            pb_file = Path(pb_path)
            if not pb_file.exists() and PLAYS_DIR.is_dir():
                alt = PLAYS_DIR / pb_file.name
                if alt.exists():
                    pb_file = alt
        else:
            candidates = sorted(
                list(Path(SESSIONS_DIR).glob(PLAYBOOK_GLOB)) + list(PLAYS_DIR.glob("apt_*.yaml")),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            if not candidates:
                print_error("No playbook found. Generate one first (playbook_generate).")
                return
            pb_file = candidates[0]

        try:
            engine = PlaybookEngine()
            playbook = engine.load(pb_file)
        except Exception as exc:
            print_error(f"Could not load playbook {pb_file}: {exc}")
            return

        target = (
            (args.target or "").strip() or getattr(playbook, "target", "") or str(self.params.get("rhost", "") or "")
        )
        shell = self._resolve_shell()

        def _executor(command: str, host: str = "") -> str:
            effective = host or target
            cmd = command.replace("{target}", effective) if effective else command
            if shell is not None:
                shell.cmd(cmd)
            return ""

        try:
            result = engine.execute(playbook, executor=_executor, dry_run=bool(args.dry_run))
            print_msg(engine.result_summary(result))
        except Exception as exc:
            print_error(f"playbook_run failed: {exc}")

    @with_category(ai_category)
    def do_auto_loop(self, line: str) -> None:
        """Run a goal through the single lazy orchestrator (auto-invokes all lazy_* steps).

        Usage: auto_loop [--target T] [--max-steps N] [--rounds N] [--workers N] [--timeout S] <goal>
        Same engine as ``lazy_loop``: single orchestrate() entry, one chain.
        """
        raw = (line or "").strip()
        if not raw:
            print_error("Usage: auto_loop [--target T] [--max-steps N] <goal>  (e.g. auto_loop --max-steps 5 'gain initial access')")
            return
        try:
            parts = shlex.split(raw)
        except ValueError as exc:
            print_error(f"auto_loop parse error: {exc}")
            return
        target = ""
        max_steps = 0
        workers = 2
        timeout = 0.0
        goal_parts: list[str] = []
        idx = 0
        while idx < len(parts):
            tok = parts[idx]
            if tok == "--target" and idx + 1 < len(parts):
                target = parts[idx + 1]
                idx += 2
                continue
            if tok in ("--max-steps", "--rounds") and idx + 1 < len(parts):
                try:
                    max_steps = max(0, int(parts[idx + 1]))
                except ValueError:
                    max_steps = 0
                idx += 2
                continue
            if tok == "--workers" and idx + 1 < len(parts):
                try:
                    workers = max(1, min(5, int(parts[idx + 1])))
                except ValueError:
                    pass
                idx += 2
                continue
            if tok == "--timeout" and idx + 1 < len(parts):
                try:
                    timeout = max(0.0, float(parts[idx + 1]))
                except ValueError:
                    pass
                idx += 2
                continue
            if tok in ("--no-bootstrap", "--step-delay"):
                if tok == "--step-delay":
                    idx += 2
                else:
                    idx += 1
                continue
            goal_parts.append(tok)
            idx += 1
        goal = " ".join(goal_parts).strip()
        shell = self._resolve_shell()
        if not target and shell is not None:
            try:
                target = str((getattr(shell, "params", {}) or {}).get("rhost", "") or "")
            except Exception:
                target = ""
        if not goal and target:
            goal = f"gain initial access on {target}"
        if not goal:
            print_error("Usage: auto_loop [--target T] [--max-steps N] <goal>")
            return
        try:
            from modules.lazy_engine import LazyEngine
        except Exception as exc:
            print_error(f"auto_loop: lazy engine unavailable ({exc})")
            return
        engine = LazyEngine()
        rounds = max_steps if max_steps > 0 else 6
        print_msg(f"[*] orchestrator chain: {'/'.join(engine.ORCHESTRATOR_CHAIN)}")
        try:
            from modules.auto_registry import DEFAULT_SHELL_TIMEOUT_SEC as _AUTO_TIMEOUT
            from modules.auto_registry import execute_shell_verb as _shell_verb
            from modules.auto_registry import is_shell_verb as _is_auto
        except Exception:
            _shell_verb = None
            _is_auto = None
            _AUTO_TIMEOUT = 600.0

        def _loop_executor(cmd: str) -> str:
            """Route automation verbs through the shell, bash stays on bash."""
            if shell is not None and _is_auto is not None and _shell_verb is not None:
                try:
                    if _is_auto(cmd or ""):
                        return _shell_verb(shell, cmd, timeout_sec=timeout or _AUTO_TIMEOUT)
                except Exception as exc:
                    return f"execution failed: {exc}"
            from core.process import run_command as _bash
            try:
                return str(_bash(cmd) or "")
            except Exception as exc:
                return f"execution failed: {exc}"

        try:
            from modules.lazy_loop import ActivityLog, ExplorationGraph
            from modules.loop_progress import (
                LoopProgress,
                snapshot_from_overview,
            )
        except Exception:
            LoopProgress = None  # type: ignore[assignment]

        try:
            created = engine.create_task(goal)
            task_id = str(created.get("task_id", ""))
        except Exception:
            task_id = ""
        if LoopProgress is None or not task_id:
            try:
                result = engine.orchestrate(
                    goal=goal, target=target, max_rounds=rounds,
                    workers=workers, timeout_sec=timeout,
                    executor=_loop_executor)
            except Exception as exc:
                print_error(f"auto_loop failed: {exc}")
                return
            task_id = result["task_id"]
            print_msg(f"[+] {task_id} [{result['status']}] rounds={result['rounds']} "
                      f"intents={len(result['overview'].get('intents', []))} "
                      f"facts={result['overview'].get('facts', 0)} "
                      f"findings={result['overview'].get('findings', 0)}")
            if result["overview"].get("findings"):
                print_warn("Findings present — inspect with: lazy_finding list / lazy_trace list")
            return

        progress = LoopProgress(goal=goal, target=target)
        progress.start()

        import contextlib
        import io as _io
        import queue as _queue
        import threading as _threading

        transcript: _queue.Queue = _queue.Queue()

        class _QueueWriter(_io.TextIOBase):
            def write(self, data):  # noqa: ANN001, ANN202
                transcript.put(str(data))
                return len(str(data))

        outcome: dict = {}

        def _run_orchestrator() -> None:
            try:
                with contextlib.redirect_stdout(_QueueWriter()):
                    outcome["result"] = engine.orchestrate(
                        goal=goal, task_id=task_id, target=target,
                        max_rounds=rounds, workers=workers,
                        timeout_sec=timeout, executor=_loop_executor)
            except Exception as exc:  # noqa: BLE001 - reported like today
                outcome["error"] = exc

        worker = _threading.Thread(target=_run_orchestrator, daemon=True)
        worker.start()
        import time as _time
        graph = ExplorationGraph(task_id)
        activity = ActivityLog(task_id)
        started = _time.monotonic()
        pending_line = ""
        try:
            while worker.is_alive():
                while True:
                    try:
                        chunk = transcript.get_nowait()
                    except _queue.Empty:
                        break
                    pending_line += chunk
                    while "\n" in pending_line:
                        line, pending_line = pending_line.split("\n", 1)
                        progress.emit(line)
                try:
                    graph.reload()
                    overview = graph.overview()
                except Exception:
                    overview = graph.overview()
                try:
                    record = engine.store.get(task_id) or {}
                except Exception:
                    record = {}
                entries = []
                try:
                    entries = activity.read(limit=60) or []
                except Exception:
                    entries = []
                tools = sum(1 for e in entries if e.get("kind") == "tool")
                results = sum(1 for e in entries if e.get("kind") == "result")
                last = str(entries[-1].get("text", "") if entries else "")
                snap = snapshot_from_overview(
                    overview, record, activity_tail=last,
                    elapsed_sec=_time.monotonic() - started)
                snap.tool_calls = tools
                snap.results = results
                progress.refresh(snap)
                worker.join(timeout=0.5)
        except KeyboardInterrupt:
            progress.emit("interrupted by operator; settling partial results...")
            try:
                engine.runtime.abort(task_id, "interrupted", "operator Ctrl+C")
            except Exception:
                pass
        if pending_line.strip():
            progress.emit(pending_line)
        try:
            overview = graph.overview()
            record = engine.store.get(task_id) or {}
            snap = snapshot_from_overview(
                overview, record, elapsed_sec=_time.monotonic() - started)
            progress.refresh(snap)
        except Exception:
            pass
        progress.stop()
        if "error" in outcome:
            print_error(f"auto_loop failed: {outcome['error']}")
            return
        if "result" not in outcome:
            print_error("auto_loop failed: orchestrator produced no result")
            return
        result = outcome["result"]
        print_msg(f"[+] {task_id} [{result['status']}] rounds={result['rounds']} "
                  f"intents={len(result['overview'].get('intents', []))} "
                  f"facts={result['overview'].get('facts', 0)} "
                  f"findings={result['overview'].get('findings', 0)}")
        if result["overview"].get("findings"):
            print_warn("Findings present — inspect with: lazy_finding list / lazy_trace list")

    @with_category(ai_category)
    def do_session_state(self, line: str) -> None:
        """Alias of ``sitrep`` kept for MCP verb parity (lazyown_session_state)."""
        self._delegate("sitrep", line)

    @with_category(ai_category)
    def do_campaign_sitrep(self, line: str) -> None:
        """Alias of ``sitrep`` kept for MCP verb parity (lazyown_campaign_sitrep)."""
        self._delegate("sitrep", line)

    @with_category(ai_category)
    def do_timeline(self, line: str) -> None:
        """Alias of ``timeline_browser`` kept for MCP verb parity (lazyown_timeline)."""
        self._delegate("timeline_browser", line)

    def _delegate(self, command: str, line: str) -> None:
        """Forward ``line`` to another shell command verbatim."""
        shell = self._resolve_shell()
        if shell is None:
            print_error("No shell context available.")
            return
        shell.onecmd(f"{command} {line}".strip())

    def _refresh_aliases(self) -> None:
        """Hot-reload declarative aliases after mutating payload context."""
        shell = self._resolve_shell()
        if shell is None:
            return
        try:
            from cli.aliases import load_aliases

            shell.aliases.update(load_aliases(self.params))
        except Exception as exc:
            print_warn(f"aliases refresh failed after auto_populate: {exc}")


__all__ = ["McpBridgeCommandSet"]
