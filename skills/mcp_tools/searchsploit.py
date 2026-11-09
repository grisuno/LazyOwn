"""MCP tool ``lazyown_searchsploit`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_searchsploit",
    description=(
        "Multi-source vulnerability and exploit search — wraps the LazyOwn 'ss' command. "
        "Searches ALL of the following sources in parallel: "
        "(1) searchsploit / ExploitDB — local offline exploit database; "
        "(2) NVD (National Vulnerability Database) — CVE details + CVSS scores via API; "
        "(3) ExploitAlert — community exploit repository API; "
        "(4) PacketStorm Security — exploit archive search; "
        "(5) Metasploit Framework — 'search' across all msf modules (if include_msf=true); "
        "(6) Pompem — multi-database exploit finder (saved to sessions/); "
        "(7) Reference URLs: sploitus.com and exploits.shodan.io for manual follow-up. "
        "Use this IMMEDIATELY after discovering a service version from nmap/pwntomate. "
        "Typical triggers: service banner in nmap output, pwntomate tool results, "
        "whatweb fingerprint, wappalyzer output, or any identified software version. "
        "Examples: "
        "  ss 'apache 2.4.49'        → search all sources for Apache 2.4.49; "
        "  ss 'CVE-2021-41773'        → full multi-source CVE research; "
        "  ss 'vsftpd 2.3.4'          → backdoor and exploit search; "
        "  ss 'smb ms17-010'           → EternalBlue across all sources; "
        "  ss 'php 8.1.0-dev'          → specific version vulnerabilities; "
        "  ss 'IIS 10.0'               → IIS-specific exploits; "
        "  ss 'openssl 1.0.1'          → Heartbleed and other OpenSSL CVEs. "
        "The query should be 'service version' or a CVE ID. "
        "Delegates to the LazyOwn 'ss' command (do_ss) which runs all sources natively. "
        "Timeout: ~120s (msfconsole + network requests)."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "Free-form search query: service+version ('apache 2.4.49'), "
                    "CVE ID ('CVE-2021-41773'), product name ('vsftpd'), "
                    "or technique ('ms17-010'). "
                    "This is the primary parameter — build it from nmap/pwntomate output."
                ),
            },
            "cve": {
                "type": "string",
                "description": "CVE identifier — alternative to query (e.g. CVE-2021-41773).",
                "default": "",
            },
            "service": {
                "type": "string",
                "description": "Service name — combined with version if provided (e.g. 'apache').",
                "default": "",
            },
            "version": {
                "type": "string",
                "description": "Service version — combined with service (e.g. '2.4.49').",
                "default": "",
            },
            "include_msf": {
                "type": "boolean",
                "description": (
                    "Include Metasploit Framework module search (msfconsole -q -x 'search ...'). "
                    "Slower (~30s) but surfaces ready-to-use msf modules. Default: false."
                ),
                "default": False,
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_searchsploit MCP tool."""
    sp_query = arguments.get("query", "").strip()
    sp_cve = arguments.get("cve", "").strip()
    sp_service = arguments.get("service", "").strip()
    sp_version = arguments.get("version", "").strip()
    sp_msf = bool(arguments.get("include_msf", False))

    # Build search term: query > cve > service+version
    if sp_query:
        search_term = sp_query
    elif sp_cve:
        search_term = sp_cve
    elif sp_service:
        search_term = f"{sp_service} {sp_version}".strip()
    else:
        return ctx.text(
            tool_name,
            "[searchsploit] Provide 'query', 'cve', or 'service'. "
            "Example: query='apache 2.4.49' or cve='CVE-2021-41773'",
        )

    # Delegate entirely to do_ss in lazyown.py — it already handles all sources:
    # searchsploit, NVD (find_ss/nvddb), ExploitAlert (find_ea/exploitalert),
    # PacketStorm (find_ps/packetstormsecurity), msfconsole search, pompem,
    # creds_py, and prints sploitus + shodan reference URLs.
    # include_msf is handled natively by do_ss (always calls msfconsole).
    ss_cmd = f"ss {search_term}"
    raw = await asyncio.get_event_loop().run_in_executor(None, lambda: ctx.run_command(ss_cmd, timeout=120))
    if not raw or not raw.strip():
        return ctx.text(tool_name, f"[ss] No output for query '{search_term}'. Check that searchsploit is installed.")
    return ctx.text(tool_name, raw[:8000])
