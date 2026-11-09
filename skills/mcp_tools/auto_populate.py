"""MCP tool ``lazyown_auto_populate`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_auto_populate",
    description=(
        "Parse the latest nmap XML scan file for a target and auto-populate payload.json "
        "with discovered domain, OS, open services, and additional hosts. "
        "Call this immediately after any nmap/lazynmap/rustscan command completes to ensure "
        "subsequent commands have correct target context without manual operator intervention. "
        "Also reads sessions/credentials.txt and auto-fills start_user/start_pass if not set."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "Target IP or hostname to load XML for (default: reads rhost from payload.json).",
                "default": "",
            },
            "force": {
                "type": "boolean",
                "description": "Overwrite existing payload fields even if already set (default false).",
                "default": False,
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_auto_populate MCP tool."""
    import xml.etree.ElementTree as _ET

    force_overwrite = bool(arguments.get("force", False))
    payload_file = ctx.lazyown_dir / "payload.json"
    try:
        pl = json.loads(payload_file.read_text())
    except Exception:
        pl = {}
    ap_target = (arguments.get("target") or "").strip() or pl.get("rhost", "")
    if not ap_target:
        return ctx.text(tool_name, "No target specified and rhost not set in payload.json.")
    changed: list = []
    # ── Parse nmap XML ─────────────────────────────────────────────────────
    xml_path = ctx.sessions_dir / f"scan_{ap_target}.nmap.xml"
    services_found: list = []
    if xml_path.exists():
        try:
            tree = _ET.parse(str(xml_path))
            root = tree.getroot()
            # Domain from hostnames
            for hn in root.iter("hostname"):
                hn_name = hn.get("name", "")
                if hn_name and "." in hn_name:
                    if force_overwrite or not pl.get("domain"):
                        pl["domain"] = hn_name
                        changed.append(f"domain={hn_name}")
                    break
            # Open services
            for port_el in root.iter("port"):
                state_el = port_el.find("state")
                if state_el is not None and state_el.get("state") == "open":
                    portid = port_el.get("portid", "")
                    svc_el = port_el.find("service")
                    svc_name = svc_el.get("name", "") if svc_el is not None else ""
                    if svc_name:
                        services_found.append(f"{portid}/{svc_name}")
            # OS match
            for osmatch in root.iter("osmatch"):
                os_name = osmatch.get("name", "").lower()
                if os_name:
                    os_id = "2" if "windows" in os_name else "1"
                    if force_overwrite or not pl.get("os_id"):
                        pl["os_id"] = os_id
                        changed.append(f"os_id={os_id} ({os_name[:40]})")
                    break
            # Additional hosts
            for addr_el in root.iter("address"):
                if addr_el.get("addrtype") == "ipv4":
                    extra_ip = addr_el.get("addr", "")
                    if extra_ip and extra_ip != ap_target:
                        changed.append(f"discovered_host={extra_ip}")
        except Exception as xml_err:
            changed.append(f"XML parse error: {xml_err}")
    else:
        changed.append(f"No XML at {xml_path} — run lazynmap first")
    # ── Load credentials from credentials.txt ─────────────────────────────
    cred_file = ctx.sessions_dir / "credentials.txt"
    if cred_file.exists():
        for line in cred_file.read_text(errors="replace").splitlines():
            line = line.split("#")[0].strip()
            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2 and parts[0] and parts[1]:
                    if force_overwrite or not pl.get("start_user"):
                        pl["start_user"] = parts[0].strip()
                        pl["start_pass"] = parts[1].strip()
                        changed.append(f"start_user={parts[0].strip()}")
                    break
    # ── Write back ────────────────────────────────────────────────────────
    if changed:
        try:
            payload_file.write_text(json.dumps(pl, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as we:
            return ctx.text(tool_name, f"Error writing payload.json: {we}")
    lines = [f"AUTO-POPULATE for target={ap_target}", ""]
    if services_found:
        lines.append("Services: " + ", ".join(services_found[:20]))
    if changed:
        lines.append("payload.json updated:")
        for c in changed:
            lines.append(f"  + {c}")
    else:
        lines.append("No changes — payload.json already populated.")
    return ctx.text(tool_name, "\n".join(lines))
