"""MCP tool ``lazyown_cve_search`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_cve_search",
    description=(
        "Search the NVD database for CVEs matching a product and optional version. "
        "Results are cached on disk. Returns id, CVSS score, severity, description, published date. "
        "Use this after discovering a service version to find known vulnerabilities."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "product": {
                "type": "string",
                "description": "Product name (e.g. 'openssh', 'apache httpd', 'vsftpd').",
            },
            "version": {
                "type": "string",
                "description": "Version string (e.g. '8.4', '2.4.49'). Optional.",
                "default": "",
            },
            "max_results": {
                "type": "string",
                "description": "Maximum number of CVEs to return (default 10).",
                "default": "10",
            },
        },
        "required": ["product"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_cve_search MCP tool."""
    product = arguments.get("product", "").strip()
    version = arguments.get("version", "").strip()
    max_results = int(arguments.get("max_results", "10") or "10")
    if not product:
        return ctx.text(tool_name, "[cve_search error] 'product' is required.")
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from cve_matcher import CVEMatcher

        matcher = CVEMatcher()
        results = await asyncio.get_event_loop().run_in_executor(
            None, lambda: matcher.search(product, version, max_results=max_results)
        )
        if not results:
            return ctx.text(tool_name, f"No CVEs found for '{product} {version}'.".strip())
        lines = [f"CVEs for {product} {version}:".strip(), ""]
        for r in results:
            lines.append(f"[{r.severity:8s}] {r.id}  CVSS {r.cvss:.1f}  {r.published}")
            lines.append(f"  {r.description[:120]}")
            for ref in r.references:
                lines.append(f"  -> {ref}")
            lines.append("")
        return ctx.text(tool_name, "\n".join(lines))
    except Exception as exc:
        return ctx.text(tool_name, f"[cve_search error] {exc}")
