"""MCP tool ``lazyown_campaign_sitrep`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lazyown_mcp_helpers import evidence_freshness, is_likely_credential
from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_campaign_sitrep",
    description=(
        "MASTER CAMPAIGN SITUATION REPORT — single call that aggregates ALL campaign state files "
        "into one concise operator briefing. Reads and synthesizes: "
        "(1) world_model.json — host states, services, credentials, phase; "
        "(2) sessions/tasks.json — task board (New/Started/Done/Blocked); "
        "(3) sessions/objectives.jsonl — active objectives queue; "
        "(4) sessions/sessionLazyOwn.json — operator credentials, hashes, implants, notes; "
        "(5) sessions/credentials*.txt — captured credential files; "
        "(6) sessions/campaign.json — campaign scope, milestones; "
        "(7) sessions/campaign_lessons.jsonl — derived lessons from completed objectives; "
        "(8) sessions/autonomous_status.json — daemon phase and step counter; "
        "(9) sessions/autonomous_events.jsonl — last 10 autonomous actions; "
        "(10) sessions/LazyOwn_session_report.csv — command count and success rate summary. "
        "Returns a structured SITREP: PHASE / HOSTS / CREDS / TASKS / OBJECTIVES / LESSONS / DAEMON. "
        "Use this at the start of every operator shift and before any strategic decision. "
        "Pass format='json' to get structured output (preferred for agents)."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "format": {
                "type": "string",
                "description": "Output format: 'pretty' (banner, default) or 'json' (structured dict).",
                "enum": ["pretty", "json"],
                "default": "pretty",
            },
        },
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_campaign_sitrep MCP tool."""
    import csv as _csv

    sitrep_format = (arguments.get("format") or "pretty").lower()
    sitrep_struct: dict[str, Any] = {
        "world_model": None,
        "session_json": None,
        "credentials_files": [],
        "tasks": None,
        "objectives": None,
        "campaign": None,
        "lessons": None,
        "daemon": None,
        "auto_events": [],
        "session_csv": None,
    }
    lines = ["=" * 60, "CAMPAIGN SITREP", "=" * 60]

    # 1. World model
    wm_file = ctx.sessions_dir / "world_model.json"
    if wm_file.exists():
        try:
            wm = json.loads(wm_file.read_text())
            hosts = wm.get("hosts", {})
            creds_wm = wm.get("credentials", [])
            phase_counts: dict = {}
            for h in hosts.values():
                s = h.get("state", "unscanned")
                phase_counts[s] = phase_counts.get(s, 0) + 1
            lines.append(f"\n[WORLD MODEL] hosts={len(hosts)} | states={phase_counts}")
            for ip, h in list(hosts.items())[:10]:
                svcs = ", ".join(f"{p}/{v.get('name', '?')}" for p, v in h.get("services", {}).items())
                lines.append(f"  {ip} [{h.get('state', '?')}] os={h.get('os_hint', '?')} svc={svcs or '(none)'}")
            if creds_wm:
                lines.append(f"  Credentials in world model: {len(creds_wm)}")
                for c in creds_wm[:5]:
                    lines.append(f"    {c.get('value', '?')} on {c.get('host', '?')} ({c.get('service', '?')})")
        except Exception as e:
            lines.append(f"[WORLD MODEL] error: {e}")
    else:
        lines.append("[WORLD MODEL] not found")

    # 2. Session JSON (credentials, hashes, implants, notes)
    sj_file = ctx.sessions_dir / "sessionLazyOwn.json"
    if sj_file.exists():
        try:
            sj = json.loads(sj_file.read_text())
            creds_sj = sj.get("credentials", [])
            hashes_sj = sj.get("hashes", [])
            implants = sj.get("implants", [])
            notes_sj = sj.get("notes") or ""
            plan_sj = sj.get("plan") or ""
            id_rsas = sj.get("id_rsa", [])
            lines.append(
                f"\n[SESSION JSON] ts={sj.get('timestamp', '?')} creds={len(creds_sj)} hashes={len(hashes_sj)} implants={len(implants)} id_rsa={len(id_rsas)}"
            )
            for c in creds_sj[:5]:
                lines.append(f"  cred: {c.get('username', '?')}:{c.get('contraseña', '?')}")
            for h in hashes_sj[:3]:
                lines.append(f"  hash: {h}")
            if notes_sj:
                lines.append(f"  notes: {str(notes_sj)[:200]}")
            if plan_sj:
                lines.append(f"  plan: {str(plan_sj)[:200]}")
        except Exception as e:
            lines.append(f"[SESSION JSON] error: {e}")

    # 3. Credentials files
    import glob as _glob

    cred_files = _glob.glob(str(ctx.sessions_dir / "credentials*.txt"))
    if cred_files:
        lines.append(f"\n[CRED FILES] {len(cred_files)} files")
        for cf in cred_files[:5]:
            try:
                content = Path(cf).read_text().strip()
                lines.append(f"  {Path(cf).name}: {content[:120]}")
            except Exception:
                pass

    # 4. Tasks
    tasks_file = ctx.sessions_dir / "tasks.json"
    if tasks_file.exists():
        try:
            tasks = json.loads(tasks_file.read_text())
            by_status: dict = {}
            for t in tasks:
                s = t.get("status", "?")
                by_status[s] = by_status.get(s, 0) + 1
            lines.append(f"\n[TASKS] total={len(tasks)} {by_status}")
            for t in tasks:
                if t.get("status") not in ("Done",):
                    lines.append(f"  [{t.get('status', '?')}] #{t.get('id', '?')}: {t.get('title', '')[:80]}")
        except Exception as e:
            lines.append(f"[TASKS] error: {e}")

    # 5. Objectives
    obj_file = ctx.sessions_dir / "objectives.jsonl"
    if obj_file.exists():
        try:
            objs = [json.loads(line) for line in obj_file.read_text().splitlines() if line.strip()]
            pending = [o for o in objs if o.get("status") == "pending"]
            done = [o for o in objs if o.get("status") == "done"]
            lines.append(f"\n[OBJECTIVES] total={len(objs)} pending={len(pending)} done={len(done)}")
            for o in pending[:5]:
                lines.append(f"  [pending] {o.get('title', '?')[:80]} (p={o.get('priority', '?')})")
        except Exception as e:
            lines.append(f"[OBJECTIVES] error: {e}")

    # 6. Campaign
    camp_file = ctx.sessions_dir / "campaign.json"
    if camp_file.exists():
        try:
            camp = json.loads(camp_file.read_text())
            lines.append(
                f"\n[CAMPAIGN] name={camp.get('name', '?')} scope={camp.get('scope', [])} status={camp.get('status', '?')}"
            )
            for hdata in camp.get("hosts", {}).values():
                lines.append(
                    f"  {hdata.get('ip', '?')} phase={hdata.get('phase', '?')} milestones={len(hdata.get('milestones', []))}"
                )
        except Exception as e:
            lines.append(f"[CAMPAIGN] error: {e}")

    # 7. Campaign lessons
    lessons_file = ctx.sessions_dir / "campaign_lessons.jsonl"
    if lessons_file.exists():
        try:
            lessons = [json.loads(line) for line in lessons_file.read_text().splitlines() if line.strip()]
            lines.append(
                f"\n[LESSONS] {len(lessons)} lessons from {len(set(line.get('campaign_id') for line in lessons))} campaigns"
            )
            for les in lessons[-3:]:
                lines.append(f"  [{les.get('topic', '?')}] {les.get('lesson', '')[:120]}")
        except Exception as e:
            lines.append(f"[LESSONS] error: {e}")

    # 8. Autonomous daemon status
    aut_status = ctx.sessions_dir / "autonomous_status.json"
    if aut_status.exists():
        try:
            st = json.loads(aut_status.read_text())
            lines.append(
                f"\n[DAEMON] running={st.get('running')} phase={st.get('phase')} step={st.get('steps_done')}/{st.get('max_steps')} obj={str(st.get('current_objective', ''))[:60]}"
            )
        except Exception as e:
            lines.append(f"[DAEMON] error: {e}")

    # 9. Last 5 autonomous events
    aut_events = ctx.sessions_dir / "autonomous_events.jsonl"
    if aut_events.exists():
        try:
            evts = [json.loads(line) for line in aut_events.read_text().splitlines() if line.strip()]
            lines.append(f"\n[AUTO EVENTS] last {min(5, len(evts))}")
            for ev in evts[-5:]:
                p = ev.get("payload", {})
                lines.append(
                    f"  [{ev.get('type', '?')}] {str(p.get('command') or p.get('objective') or p.get('phase') or '')[:60]}"
                )
        except Exception as e:
            lines.append(f"[AUTO EVENTS] error: {e}")

    # 10. CSV summary
    csv_file = ctx.sessions_dir / "LazyOwn_session_report.csv"
    if csv_file.exists():
        try:
            with open(str(csv_file), newline="", errors="replace") as f:
                rows = list(_csv.DictReader(f))
            total = len(rows)
            cmds = set(r.get("command", "") for r in rows)
            lines.append(f"\n[SESSION CSV] {total} command rows, {len(cmds)} unique commands")
        except Exception as e:
            lines.append(f"[SESSION CSV] error: {e}")

    lines.append("\n" + "=" * 60)

    if sitrep_format == "json":
        wm_file = ctx.sessions_dir / "world_model.json"
        if wm_file.exists():
            try:
                wm = json.loads(wm_file.read_text())
                from modules.killchain import KillChain

                sitrep_struct["world_model"] = {
                    "phase": KillChain.current_phase(world_model_path=wm_file),
                    "host_count": len(wm.get("hosts", {})),
                    "credentials": [
                        {
                            **c,
                            "is_likely_credential": is_likely_credential(str(c.get("value", "")))[0],
                            "confidence": is_likely_credential(str(c.get("value", "")))[1],
                        }
                        for c in wm.get("credentials", [])[:50]
                    ],
                    "hosts": wm.get("hosts", {}),
                }
            except Exception as exc:
                sitrep_struct["world_model"] = {"error": str(exc)}

        sj_file = ctx.sessions_dir / "sessionLazyOwn.json"
        if sj_file.exists():
            try:
                sitrep_struct["session_json"] = json.loads(sj_file.read_text())
            except Exception as exc:
                sitrep_struct["session_json"] = {"error": str(exc)}

        cred_paths = sorted(ctx.sessions_dir.glob("credentials*.txt"))
        for cp in cred_paths[:10]:
            try:
                sitrep_struct["credentials_files"].append(
                    {
                        "name": cp.name,
                        "preview": cp.read_text(errors="replace")[:240],
                        "freshness": evidence_freshness(cp),
                    }
                )
            except OSError:
                pass

        tasks_file = ctx.sessions_dir / "tasks.json"
        if tasks_file.exists():
            try:
                tdata = json.loads(tasks_file.read_text())
                by_status: dict = {}
                for t in tdata:
                    by_status[t.get("status", "?")] = by_status.get(t.get("status", "?"), 0) + 1
                sitrep_struct["tasks"] = {
                    "total": len(tdata),
                    "by_status": by_status,
                    "pending_preview": [
                        {"id": t.get("id"), "status": t.get("status"), "title": t.get("title", "")[:140]}
                        for t in tdata
                        if t.get("status") != "Done"
                    ][:20],
                }
            except Exception as exc:
                sitrep_struct["tasks"] = {"error": str(exc)}

        obj_file = ctx.sessions_dir / "objectives.jsonl"
        if obj_file.exists():
            try:
                objs = [json.loads(line) for line in obj_file.read_text().splitlines() if line.strip()]
                sitrep_struct["objectives"] = {
                    "total": len(objs),
                    "pending": [o for o in objs if o.get("status") == "pending"][:10],
                }
            except Exception as exc:
                sitrep_struct["objectives"] = {"error": str(exc)}

        camp_file = ctx.sessions_dir / "campaign.json"
        if camp_file.exists():
            try:
                sitrep_struct["campaign"] = json.loads(camp_file.read_text())
            except Exception as exc:
                sitrep_struct["campaign"] = {"error": str(exc)}

        lessons_file = ctx.sessions_dir / "campaign_lessons.jsonl"
        if lessons_file.exists():
            try:
                sitrep_struct["lessons"] = [
                    json.loads(line) for line in lessons_file.read_text().splitlines() if line.strip()
                ][-10:]
            except Exception as exc:
                sitrep_struct["lessons"] = {"error": str(exc)}

        aut_status = ctx.sessions_dir / "autonomous_status.json"
        if aut_status.exists():
            try:
                sitrep_struct["daemon"] = json.loads(aut_status.read_text())
            except Exception as exc:
                sitrep_struct["daemon"] = {"error": str(exc)}

        aut_events = ctx.sessions_dir / "autonomous_events.jsonl"
        if aut_events.exists():
            try:
                evts = [json.loads(line) for line in aut_events.read_text().splitlines() if line.strip()]
                sitrep_struct["auto_events"] = evts[-10:]
            except Exception as exc:
                sitrep_struct["auto_events"] = [{"error": str(exc)}]

        csv_file = ctx.sessions_dir / "LazyOwn_session_report.csv"
        if csv_file.exists():
            try:
                with open(str(csv_file), newline="", errors="replace") as f:
                    rows = list(_csv.DictReader(f))
                sitrep_struct["session_csv"] = {
                    "rows": len(rows),
                    "unique_commands": len(set(r.get("command", "") for r in rows)),
                }
            except Exception as exc:
                sitrep_struct["session_csv"] = {"error": str(exc)}

        return ctx.text(tool_name, json.dumps(sitrep_struct, indent=2, default=str))

    return ctx.text(tool_name, "\n".join(lines))
