"""Report generation for LazyOwn engagements — direct Python, no template engine.

Generates clean HTML and Markdown reports from session data, world model
state, credential files, and command history.
"""

from __future__ import annotations

import csv
import datetime
import json
import os
from pathlib import Path
from typing import Any

_LAZYOWN_DIR = Path(os.environ.get("LAZYOWN_DIR", str(Path(__file__).resolve().parent.parent)))
SESSIONS_DIR = _LAZYOWN_DIR / "sessions"


def _fmt_size(size: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


class ReportGenerator:
    """Generates engagement reports from session data."""

    def __init__(self, sessions_dir: Path | None = None) -> None:
        self._sessions_dir = sessions_dir or SESSIONS_DIR

    def generate(self, fmt: str = "html", output_path: str = "", standalone: bool = True) -> str:
        ctx = self._collect_context()
        if fmt == "html":
            rendered = self._render_html(ctx, standalone=standalone)
        else:
            rendered = self._render_md(ctx)
        if output_path:
            Path(output_path).write_text(rendered, encoding="utf-8")
        return rendered

    def _render_html(self, ctx: dict[str, Any], standalone: bool = True) -> str:
        def esc(s: Any) -> str:
            return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

        lines = []
        if standalone:
<<<<<<< HEAD
            lines.append("""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title><style>
=======
            lines.append(
                """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title><style>
>>>>>>> dev
:root{--bg:#0d1117;--fg:#c9d1d9;--accent:#58a6ff;--border:#30363d;--card:#161b22;--red:#f85149;--green:#3fb950;--amber:#d2991d}
*{box-sizing:border-box;margin:0;padding:0}body{background:var(--bg);color:var(--fg);font-family:system-ui,sans-serif;line-height:1.6;padding:2rem}
h1{color:var(--accent);border-bottom:2px solid var(--border);padding-bottom:.5rem;margin-bottom:1rem}
h2{color:var(--amber);margin:2rem 0 1rem}h3{color:var(--accent);margin:1.5rem 0 .5rem}
.card{background:var(--card);border:1px solid var(--border);border-radius:6px;padding:1rem;margin:1rem 0}
table{width:100%%;border-collapse:collapse}th,td{text-align:left;padding:.5rem;border-bottom:1px solid var(--border)}th{color:var(--accent)}
.severity-critical{color:var(--red);font-weight:bold}.severity-high{color:var(--red)}.severity-medium{color:var(--amber)}.severity-low{color:var(--green)}
pre{background:var(--bg);border:1px solid var(--border);border-radius:4px;padding:.8rem;overflow-x:auto;font-size:.85rem}
<<<<<<< HEAD
</style></head><body>""" % esc(ctx["title"]))
            lines.append(f"<h1>{esc(ctx['title'])}</h1>")
        lines.append(f"<div class='card'><p><strong>Target:</strong> {esc(ctx['target'])}</p><p><strong>Generated:</strong> {esc(ctx['generated'])}</p><p><strong>Engine:</strong> LazyOwn RedTeam Framework {esc(ctx['version'])}</p></div>")
=======
</style></head><body>"""
                % esc(ctx["title"])
            )  # noqa: UP031
            lines.append(f"<h1>{esc(ctx['title'])}</h1>")
        lines.append(
            f"<div class='card'><p><strong>Target:</strong> {esc(ctx['target'])}</p><p><strong>Generated:</strong> {esc(ctx['generated'])}</p><p><strong>Engine:</strong> LazyOwn RedTeam Framework {esc(ctx['version'])}</p></div>"
        )
>>>>>>> dev

        # Kill-chain
        lines.append("<h2>Kill-Chain Progress</h2><div style='display:flex;gap:.5rem;flex-wrap:wrap;margin:1rem 0'>")
        for ph in ctx["kill_chain"]:
<<<<<<< HEAD
            cls = "background:rgba(63,185,80,.1);border-color:#3fb950" if ph["status"] == "complete" else ("background:rgba(88,166,255,.1);border-color:#58a6ff" if ph["status"] == "active" else "")
            lines.append(f"<span style='padding:.5rem 1rem;border-radius:4px;background:var(--card);border:1px solid var(--border);font-size:.8rem;{cls}'>{esc(ph['name'])}</span>")
=======
            cls = (
                "background:rgba(63,185,80,.1);border-color:#3fb950"
                if ph["status"] == "complete"
                else ("background:rgba(88,166,255,.1);border-color:#58a6ff" if ph["status"] == "active" else "")
            )
            lines.append(
                f"<span style='padding:.5rem 1rem;border-radius:4px;background:var(--card);border:1px solid var(--border);font-size:.8rem;{cls}'>{esc(ph['name'])}</span>"
            )
>>>>>>> dev
        lines.append("</div>")

        # Hosts
        hosts = ctx["hosts"]
        if hosts:
<<<<<<< HEAD
            lines.append("<h2>Discovered Hosts</h2><table><tr><th>IP</th><th>Hostname</th><th>OS</th><th>Open Ports</th><th>Services</th></tr>")
            for h in hosts:
                lines.append(f"<tr><td>{esc(h['ip'])}</td><td>{esc(h.get('hostname') or 'N/A')}</td><td>{esc(h.get('os') or 'Unknown')}</td><td>{esc(', '.join(map(str, h.get('ports', []))))}</td><td>{esc(', '.join(h.get('services', [])))}</td></tr>")
=======
            lines.append(
                "<h2>Discovered Hosts</h2><table><tr><th>IP</th><th>Hostname</th><th>OS</th><th>Open Ports</th><th>Services</th></tr>"
            )
            for h in hosts:
                lines.append(
                    f"<tr><td>{esc(h['ip'])}</td><td>{esc(h.get('hostname') or 'N/A')}</td><td>{esc(h.get('os') or 'Unknown')}</td><td>{esc(', '.join(map(str, h.get('ports', []))))}</td><td>{esc(', '.join(h.get('services', [])))}</td></tr>"
                )
>>>>>>> dev
            lines.append("</table>")

        # Vulns
        vulns = ctx["vulns"]
        if vulns:
<<<<<<< HEAD
            lines.append("<h2>Vulnerabilities</h2><table><tr><th>CVE/ID</th><th>Service</th><th>Severity</th><th>Description</th></tr>")
            for v in vulns:
                sev = str(v.get("severity", "")).lower()
                lines.append(f"<tr><td>{esc(v.get('id',''))}</td><td>{esc(v.get('service',''))}</td><td class='severity-{sev}'>{esc(v.get('severity',''))}</td><td>{esc(v.get('description',''))}</td></tr>")
=======
            lines.append(
                "<h2>Vulnerabilities</h2><table><tr><th>CVE/ID</th><th>Service</th><th>Severity</th><th>Description</th></tr>"
            )
            for v in vulns:
                sev = str(v.get("severity", "")).lower()
                lines.append(
                    f"<tr><td>{esc(v.get('id', ''))}</td><td>{esc(v.get('service', ''))}</td><td class='severity-{sev}'>{esc(v.get('severity', ''))}</td><td>{esc(v.get('description', ''))}</td></tr>"
                )
>>>>>>> dev
            lines.append("</table>")

        # Creds
        creds = ctx["creds"]
        if creds:
<<<<<<< HEAD
            lines.append("<h2>Compromised Credentials</h2><table><tr><th>Username</th><th>Type</th><th>Source</th></tr>")
            for c in creds:
                lines.append(f"<tr><td>{esc(c['username'])}</td><td>{esc(c['type'])}</td><td>{esc(c['source'])}</td></tr>")
=======
            lines.append(
                "<h2>Compromised Credentials</h2><table><tr><th>Username</th><th>Type</th><th>Source</th></tr>"
            )
            for c in creds:
                lines.append(
                    f"<tr><td>{esc(c['username'])}</td><td>{esc(c['type'])}</td><td>{esc(c['source'])}</td></tr>"
                )
>>>>>>> dev
            lines.append("</table>")

        # Loot
        loot = ctx["loot"]
        if loot:
            lines.append("<h2>Exfiltrated Loot</h2><table><tr><th>File</th><th>Size</th><th>Source</th></tr>")
<<<<<<< HEAD
            for l in loot:
                lines.append(f"<tr><td>{esc(l['name'])}</td><td>{esc(l['size'])}</td><td>{esc(l['source'])}</td></tr>")
=======
            for entry in loot:
                lines.append(
                    f"<tr><td>{esc(entry['name'])}</td><td>{esc(entry['size'])}</td><td>{esc(entry['source'])}</td></tr>"
                )
>>>>>>> dev
            lines.append("</table>")

        # Commands
        cmds = ctx["commands"]
        if cmds:
            shown = cmds[:50]
            lines.append("<h2>Commands Executed</h2><table><tr><th>#</th><th>Command</th><th>Timestamp</th></tr>")
            for i, c in enumerate(shown, 1):
                lines.append(f"<tr><td>{i}</td><td><code>{esc(c['cmd'])}</code></td><td>{esc(c['ts'])}</td></tr>")
            if len(cmds) > 50:
<<<<<<< HEAD
                lines.append(f"<tr><td colspan='3' style='color:#484f58;font-style:italic'>... and {len(cmds) - 50} more</td></tr>")
=======
                lines.append(
                    f"<tr><td colspan='3' style='color:#484f58;font-style:italic'>... and {len(cmds) - 50} more</td></tr>"
                )
>>>>>>> dev
            lines.append("</table>")

        # Notes
        notes = ctx["notes"]
        lines.append("<h2>Appendix: Notes</h2><div class='card'>")
        if notes:
            for n in notes:
                lines.append(f"<p><strong>{esc(n['ts'])}:</strong> {esc(n['text'])}</p>")
        else:
            lines.append("<p style='color:#484f58;font-style:italic'>No notes recorded.</p>")
        lines.append("</div>")
        if standalone:
            lines.append("<p style='color:#484f58'>Generated by LazyOwn RedTeam Framework</p></body></html>")
        else:
            lines.append("<p class='text-muted mt-4'>Generated by LazyOwn RedTeam Framework</p>")
        return "\n".join(lines)

    def _render_md(self, ctx: dict[str, Any]) -> str:
        lines = []
        lines.append(f"# {ctx['title']}\n")
        lines.append(f"**Target:** `{ctx['target']}`")
        lines.append(f"**Generated:** {ctx['generated']}")
        lines.append(f"**Engine:** LazyOwn RedTeam Framework {ctx['version']}\n")

        lines.append("## Kill-Chain Progress\n")
        for ph in ctx["kill_chain"]:
            mark = "x" if ph["status"] == "complete" else " "
            lines.append(f"- [{mark}] {ph['name']}")
        lines.append("")

        hosts = ctx["hosts"]
        if hosts:
            lines.append("## Discovered Hosts\n\n| IP | Hostname | OS | Open Ports | Services |\n|---|---|---|---|---|")
            for h in hosts:
<<<<<<< HEAD
                lines.append(f"| {h['ip']} | {h.get('hostname') or 'N/A'} | {h.get('os') or 'Unknown'} | {', '.join(map(str, h.get('ports', [])))} | {', '.join(h.get('services', []))} |")
=======
                lines.append(
                    f"| {h['ip']} | {h.get('hostname') or 'N/A'} | {h.get('os') or 'Unknown'} | {', '.join(map(str, h.get('ports', [])))} | {', '.join(h.get('services', []))} |"
                )
>>>>>>> dev
            lines.append("")

        vulns = ctx["vulns"]
        if vulns:
            lines.append("## Vulnerabilities\n\n| CVE/ID | Service | Severity | Description |\n|---|---|---|---|")
            for v in vulns:
<<<<<<< HEAD
                lines.append(f"| {v.get('id','')} | {v.get('service','')} | {v.get('severity','')} | {v.get('description','')} |")
=======
                lines.append(
                    f"| {v.get('id', '')} | {v.get('service', '')} | {v.get('severity', '')} | {v.get('description', '')} |"
                )
>>>>>>> dev
            lines.append("")

        creds = ctx["creds"]
        if creds:
            lines.append("## Compromised Credentials\n\n| Username | Type | Source |\n|---|---|---|")
            for c in creds:
                lines.append(f"| {c['username']} | {c['type']} | {c['source']} |")
            lines.append("")

        loot = ctx["loot"]
        if loot:
            lines.append("## Exfiltrated Loot\n\n| File | Size | Source |\n|---|---|---|")
<<<<<<< HEAD
            for l in loot:
                lines.append(f"| {l['name']} | {l['size']} | {l['source']} |")
=======
            for entry in loot:
                lines.append(f"| {entry['name']} | {entry['size']} | {entry['source']} |")
>>>>>>> dev
            lines.append("")

        cmds = ctx["commands"]
        if cmds:
            shown = cmds[:50]
            lines.append("## Commands Executed\n\n| # | Command | Timestamp |\n|---|---|---|")
            for i, c in enumerate(shown, 1):
                lines.append(f"| {i} | `{c['cmd']}` | {c['ts']} |")
            lines.append("")

        notes = ctx["notes"]
        lines.append("## Appendix: Notes\n")
        if notes:
            for n in notes:
                lines.append(f"- **[{n['ts']}]:** {n['text']}")
        else:
            lines.append("No notes recorded.")
        lines.append("")
        lines.append("---\n*Generated by LazyOwn RedTeam Framework*")
        return "\n".join(lines)

    def _collect_context(self) -> dict[str, Any]:
        sessions = self._sessions_dir
        return {
            "title": "LazyOwn Engagement Report",
            "target": self._read_payload_target(),
            "generated": datetime.datetime.now(datetime.UTC).isoformat(),
            "version": self._read_version(),
            "kill_chain": self._read_kill_chain(),
            "hosts": self._read_hosts(sessions),
            "vulns": self._read_vulns(sessions),
            "creds": self._read_credentials(sessions),
            "loot": self._read_loot(sessions),
            "commands": self._read_commands(sessions),
            "notes": self._read_notes(sessions),
        }

    @staticmethod
    def _read_payload_target() -> str:
        try:
            return json.loads((_LAZYOWN_DIR / "payload.json").read_text(encoding="utf-8"))["rhost"]
        except Exception:
            return "unknown"

    @staticmethod
    def _read_version() -> str:
        try:
            return json.loads((_LAZYOWN_DIR / "version.json").read_text())["version"]
        except Exception:
            return "0.0.0"

    @staticmethod
    def _read_kill_chain() -> list[dict[str, str]]:
        from modules.killchain import KillChain as _KC
<<<<<<< HEAD
=======

>>>>>>> dev
        phases = [(p[0], p[1]) for p in _KC.phases_for_display()]
        try:
            current = _KC.current_phase()
            progress = _KC.get_progress()
            completed = {p.key for p in progress if p.status == "done"}
        except Exception:
            current = "recon"
            completed = set()
        result = []
        for ph_id, ph_name in phases:
            if ph_id in completed:
                status = "complete"
            elif ph_id == current:
                status = "active"
            else:
                status = "future"
            result.append({"name": ph_name, "id": ph_id, "status": status})
        return result

    @staticmethod
    def _read_hosts(sessions: Path) -> list[dict[str, Any]]:
        try:
            wm = json.loads((sessions / "world_model.json").read_text(encoding="utf-8"))
            hosts = wm.get("hosts", {})
        except Exception:
            hosts = {}
        result = []
        for ip, info in hosts.items():
            if isinstance(info, dict):
<<<<<<< HEAD
                result.append({"ip": ip, "hostname": info.get("hostname", ""), "os": info.get("os", ""), "ports": info.get("ports", []), "services": info.get("services", [])})
=======
                result.append(
                    {
                        "ip": ip,
                        "hostname": info.get("hostname", ""),
                        "os": info.get("os", ""),
                        "ports": info.get("ports", []),
                        "services": info.get("services", []),
                    }
                )
>>>>>>> dev
        return result

    @staticmethod
    def _read_vulns(sessions: Path) -> list[dict[str, Any]]:
        try:
<<<<<<< HEAD
            return json.loads((sessions / "world_model.json").read_text(encoding="utf-8")).get("vulnerabilities", []) or []
=======
            return (
                json.loads((sessions / "world_model.json").read_text(encoding="utf-8")).get("vulnerabilities", []) or []
            )
>>>>>>> dev
        except Exception:
            return []

    @staticmethod
    def _read_credentials(sessions: Path) -> list[dict[str, Any]]:
        result = []
        for fpath in sorted(sessions.glob("credentials*.txt")):
            try:
                for line in fpath.read_text(encoding="utf-8", errors="ignore").splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split(":", 2)
<<<<<<< HEAD
                    result.append({"username": parts[0] if parts else "", "type": parts[1] if len(parts) > 1 else "password", "source": fpath.name})
=======
                    result.append(
                        {
                            "username": parts[0] if parts else "",
                            "type": parts[1] if len(parts) > 1 else "password",
                            "source": fpath.name,
                        }
                    )
>>>>>>> dev
            except OSError:
                pass
        return result

    @staticmethod
    def _read_loot(sessions: Path) -> list[dict[str, Any]]:
        loot_dir = sessions / "loot"
        if not loot_dir.exists():
            return []
        result = []
        for fpath in sorted(loot_dir.iterdir()):
            if fpath.is_file():
                result.append({"name": fpath.name, "size": _fmt_size(fpath.stat().st_size), "source": "loot/"})
        return result

    @staticmethod
    def _read_commands(sessions: Path) -> list[dict[str, str]]:
        report_path = sessions / "LazyOwn_session_report.csv"
        if not report_path.exists():
            return []
        result = []
        try:
            with open(report_path, newline="", encoding="utf-8", errors="ignore") as fh:
                for row in csv.DictReader(fh):
                    result.append({"cmd": row.get("command", row.get("tool", "")), "ts": row.get("timestamp", "")})
        except Exception:
            pass
        return result

    @staticmethod
    def _read_notes(sessions: Path) -> list[dict[str, str]]:
        notes_path = sessions / "notes.txt"
        if not notes_path.exists():
            return []
        try:
<<<<<<< HEAD
            return [{"ts": "", "text": line.strip()} for line in notes_path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()]
=======
            return [
                {"ts": "", "text": line.strip()}
                for line in notes_path.read_text(encoding="utf-8", errors="ignore").splitlines()
                if line.strip()
            ]
>>>>>>> dev
        except OSError:
            return []


def generate_report(fmt: str = "html", output: str = "") -> str:
    gen = ReportGenerator()
    path = output or f"sessions/report_{datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M%S')}.{fmt}"
    gen.generate(fmt=fmt, output_path=path)
    return path


__all__ = ["ReportGenerator", "generate_report"]
