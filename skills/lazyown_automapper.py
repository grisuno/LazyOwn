#!/usr/bin/env python3
"""
LazyOwn MCP Auto-Mapper
========================
Discovers LazyOwn extensions at startup and returns MCP Tool definitions +
a runtime dispatch table.  Three source types are supported:

  lazyaddons/*.yaml  (enabled: true)  → lazyown_addon_<name>
  tools/*.tool       (active: true)   → lazyown_tool_<name>
  plugins/*.yaml     (enabled: true)  → lazyown_plugin_<name>

All discovered tools are executed by running the LazyOwn shell command or,
for .tool files, by substituting the command template and running it via
subprocess.

Integration in lazyown_mcp.py
──────────────────────────────
    from lazyown_automapper import AutoMapper

    _automapper = AutoMapper(LAZYOWN_DIR)

    # list_tools():
    return STATIC_TOOLS + _automapper.mcp_tools()

    # call_tool():
    result = _automapper.dispatch(name, arguments, config)
    if result is not None:
        return result

Auto-regeneration of lazyown.md
───────────────────────────────
    _automapper.update_skills_md(skills_md_path)

    Appends / replaces the "## Auto-discovered tools" section of lazyown.md
    with a Markdown table of all dynamic tools found at startup.
"""

from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml as _yaml_lib
    _YAML_OK = True
except ImportError:
    _YAML_OK = False

try:
    from mcp import types as mcp_types  # type: ignore
    _MCP_TYPES_OK = True
except ImportError:
    _MCP_TYPES_OK = False

log = logging.getLogger("automapper")

# ── Sanitise tool name for MCP (only [a-z0-9_-] allowed) ────────────────────

_SAFE_RE = re.compile(r"[^a-z0-9_-]")


def _safe_name(raw: str) -> str:
    s = raw.lower().strip()
    s = _SAFE_RE.sub("_", s)
    # collapse repeated underscores
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "tool"


# ── YAML helpers ─────────────────────────────────────────────────────────────

def _load_yaml(path: Path) -> Optional[Dict]:
    if not _YAML_OK:
        # Very minimal YAML loader — handles simple key: value only
        d: Dict[str, Any] = {}
        try:
            for line in path.read_text(errors="replace").splitlines():
                m = re.match(r"^(\w+)\s*:\s*(.+)$", line.strip())
                if m:
                    d[m.group(1)] = m.group(2).strip().strip('"\'')
        except OSError:
            return None
        return d or None

    try:
        with path.open(errors="replace") as fh:
            data = _yaml_lib.safe_load(fh)
        return data if isinstance(data, dict) else None
    except Exception as exc:
        log.debug(f"YAML parse error {path.name}: {exc}")
        return None


# ── Parameter schema builder ─────────────────────────────────────────────────

def _params_to_schema(params: Optional[list]) -> Dict:
    """Convert a lazyaddons/plugins params list to JSON Schema."""
    if not params:
        return {"type": "object", "properties": {}, "required": []}

    props: Dict[str, Dict] = {}
    required: List[str] = []

    for p in params:
        if not isinstance(p, dict):
            continue
        pname = str(p.get("name", "")).strip()
        if not pname:
            continue
        ptype = str(p.get("type", "string")).lower()
        json_type = {
            "string": "string", "str": "string",
            "integer": "integer", "int": "integer",
            "boolean": "boolean", "bool": "boolean",
            "number": "number", "float": "number",
        }.get(ptype, "string")
        props[pname] = {
            "type": json_type,
            "description": str(p.get("description", f"Parameter: {pname}")),
        }
        if p.get("required", False):
            required.append(pname)

    return {"type": "object", "properties": props, "required": required}


# ── Source loaders ────────────────────────────────────────────────────────────

def _load_addons(lazyaddons_dir: Path) -> List[Dict]:
    """Return list of addon spec dicts for enabled lazyaddons."""
    results: List[Dict] = []
    if not lazyaddons_dir.is_dir():
        return results

    for yf in sorted(lazyaddons_dir.glob("*.yaml")):
        data = _load_yaml(yf)
        if not data:
            continue
        # enabled defaults to True if missing — follows lazyown.py behaviour
        if str(data.get("enabled", "true")).lower() == "false":
            continue
        raw_name = str(data.get("name", yf.stem)).strip()
        if not raw_name:
            continue
        results.append({
            "source":      "addon",
            "raw_name":    raw_name,
            "mcp_name":    f"lazyown_addon_{_safe_name(raw_name)}",
            "description": str(data.get("description", f"LazyOwn addon: {raw_name}")).strip(),
            "params":      data.get("params") or [],
            "execute_cmd": (data.get("tool") or {}).get("execute_command", ""),
            "file":        str(yf),
        })

    return results


def _load_dottools(tools_dir: Path) -> List[Dict]:
    """Return list of spec dicts for active pwntomate .tool files."""
    results: List[Dict] = []
    if not tools_dir.is_dir():
        return results

    for tf in sorted(tools_dir.glob("*.tool")):
        if tf.stem.startswith("_"):
            continue
        try:
            data = json.loads(tf.read_text(errors="replace"))
        except Exception:
            continue
        if not data.get("active", True):
            continue

        toolname = str(data.get("toolname", tf.stem)).strip()
        command  = str(data.get("command", "")).strip()
        triggers = data.get("trigger", [])
        if isinstance(triggers, str):
            triggers = [triggers]

        results.append({
            "source":      "tool",
            "raw_name":    toolname,
            "mcp_name":    f"lazyown_tool_{_safe_name(toolname)}",
            "description": (
                f"Run {toolname} against a target. "
                f"Triggers on services: {', '.join(triggers) or 'any'}. "
                f"Command template: {command[:80]}{'…' if len(command) > 80 else ''}"
            ),
            "command":     command,
            "triggers":    triggers,
            "file":        str(tf),
        })

    return results


def _load_plugins(plugins_dir: Path) -> List[Dict]:
    """Return list of spec dicts for enabled plugins (Lua+YAML pairs)."""
    results: List[Dict] = []
    if not plugins_dir.is_dir():
        return results

    for yf in sorted(plugins_dir.glob("*.yaml")):
        data = _load_yaml(yf)
        if not data:
            continue
        if str(data.get("enabled", "true")).lower() == "false":
            continue
        raw_name = str(data.get("name", yf.stem)).strip()
        if not raw_name or raw_name.startswith("template") or "template" in yf.stem.lower():
            continue

        results.append({
            "source":      "plugin",
            "raw_name":    raw_name,
            "mcp_name":    f"lazyown_plugin_{_safe_name(raw_name)}",
            "description": str(data.get("description", f"LazyOwn plugin: {raw_name}")).strip(),
            "params":      data.get("params") or [],
            "file":        str(yf),
        })

    return results


# ── Command template expander ─────────────────────────────────────────────────

def _expand_tool_command(template: str, ip: str, port: str, ssl: bool,
                         outputdir: str, toolname: str) -> str:
    """Fill pwntomate-style {placeholders} in a .tool command template."""
    s = "s" if ssl else ""
    cmd = template
    cmd = cmd.replace("{ip}",        ip)
    cmd = cmd.replace("{port}",      port)
    cmd = cmd.replace("{s}",         s)
    cmd = cmd.replace("{outputdir}", outputdir)
    cmd = cmd.replace("{toolname}",  toolname)
    # Also handle {domain} and {url} with simple defaults
    cmd = cmd.replace("{domain}",    ip)
    cmd = cmd.replace("{url}",       f"http{s}://{ip}:{port}")
    return cmd


# ── MCP Tool builders ─────────────────────────────────────────────────────────

def _addon_to_mcp_tool(spec: Dict) -> Optional[Any]:
    if not _MCP_TYPES_OK:
        return None
    schema = _params_to_schema(spec.get("params"))
    # Always add optional 'args' string for extra freeform args
    schema["properties"]["args"] = {
        "type": "string",
        "description": "Additional freeform arguments to append to the command.",
    }
    return mcp_types.Tool(
        name=spec["mcp_name"],
        description=f"[addon] {spec['description'][:200]}",
        inputSchema=schema,
    )


def _tool_to_mcp_tool(spec: Dict) -> Optional[Any]:
    if not _MCP_TYPES_OK:
        return None
    return mcp_types.Tool(
        name=spec["mcp_name"],
        description=f"[pwntomate] {spec['description'][:200]}",
        inputSchema={
            "type": "object",
            "properties": {
                "ip": {
                    "type": "string",
                    "description": "Target IP address (default: rhost from config).",
                },
                "port": {
                    "type": "string",
                    "description": "Target port number.",
                    "default": "80",
                },
                "ssl": {
                    "type": "boolean",
                    "description": "Use HTTPS (adds 's' to http{s} placeholder).",
                    "default": False,
                },
                "outputdir": {
                    "type": "string",
                    "description": "Directory for output files (default: sessions/<ip>/<port>/<toolname>).",
                },
            },
            "required": [],
        },
    )


def _plugin_to_mcp_tool(spec: Dict) -> Optional[Any]:
    if not _MCP_TYPES_OK:
        return None
    schema = _params_to_schema(spec.get("params"))
    schema["properties"]["args"] = {
        "type": "string",
        "description": "Additional freeform arguments.",
    }
    return mcp_types.Tool(
        name=spec["mcp_name"],
        description=f"[plugin] {spec['description'][:200]}",
        inputSchema=schema,
    )


# ── AutoMapper ────────────────────────────────────────────────────────────────

class AutoMapper:
    """
    Discover and cache all dynamic MCP tools from lazyaddons/, tools/, plugins/.

    Call .mcp_tools() to get the list of types.Tool objects.
    Call .dispatch(name, arguments, config) → Optional[str] to execute.
    Call .update_skills_md(path) to regenerate the auto-discovered section.
    """

    def __init__(self, lazyown_dir: Path) -> None:
        self._root       = lazyown_dir
        self._addons_dir = lazyown_dir / "lazyaddons"
        self._tools_dir  = lazyown_dir / "tools"
        self._plugins_dir = lazyown_dir / "plugins"
        self._specs: List[Dict] = []
        self._index: Dict[str, Dict] = {}
        self._scan()

    def _scan(self) -> None:
        specs = (
            _load_addons(self._addons_dir)
            + _load_dottools(self._tools_dir)
            + _load_plugins(self._plugins_dir)
        )
        # Deduplicate by mcp_name — last writer wins
        seen: Dict[str, Dict] = {}
        for s in specs:
            seen[s["mcp_name"]] = s
        self._specs = list(seen.values())
        self._index = {s["mcp_name"]: s for s in self._specs}
        log.info(
            f"automapper: {len([s for s in self._specs if s['source']=='addon'])} addons, "
            f"{len([s for s in self._specs if s['source']=='tool'])} tools, "
            f"{len([s for s in self._specs if s['source']=='plugin'])} plugins"
        )

    def rescan(self) -> None:
        """Force a rescan of all source directories."""
        self._scan()

    def mcp_tools(self) -> List[Any]:
        """Return list of mcp types.Tool objects for all discovered extensions."""
        if not _MCP_TYPES_OK:
            return []
        result = []
        for spec in self._specs:
            try:
                if spec["source"] == "addon":
                    t = _addon_to_mcp_tool(spec)
                elif spec["source"] == "tool":
                    t = _tool_to_mcp_tool(spec)
                elif spec["source"] == "plugin":
                    t = _plugin_to_mcp_tool(spec)
                else:
                    continue
                if t is not None:
                    result.append(t)
            except Exception as exc:
                log.debug(f"mcp_tools skip {spec.get('mcp_name')}: {exc}")
        return result

    def dispatch(
        self,
        name: str,
        arguments: Dict[str, Any],
        config: Dict[str, Any],
        run_command_fn: Any = None,  # _run_lazyown_command(cmd, timeout) -> str
    ) -> Optional[str]:
        """
        Execute a dynamic tool.  Returns the output string or None if name
        is not a known dynamic tool (caller should fall through to static dispatch).

        run_command_fn: callable(cmd: str, timeout: int=30) → str
            When provided, addon/plugin calls go through the LazyOwn shell.
            .tool commands always run via subprocess.
        """
        spec = self._index.get(name)
        if spec is None:
            return None

        source = spec["source"]

        if source == "addon":
            return self._run_addon(spec, arguments, config, run_command_fn)
        elif source == "tool":
            return self._run_dottool(spec, arguments, config)
        elif source == "plugin":
            return self._run_plugin(spec, arguments, config, run_command_fn)
        return None

    # ── addon dispatch ────────────────────────────────────────────────────────

    def _run_addon(
        self, spec: Dict, arguments: Dict, config: Dict, run_fn: Any
    ) -> str:
        raw_name = spec["raw_name"]
        # Build positional args from params
        param_parts: List[str] = []
        for p in (spec.get("params") or []):
            pname = p.get("name", "")
            if pname and pname in arguments:
                val = str(arguments[pname]).strip()
                if val:
                    param_parts.append(val)
        extra = str(arguments.get("args", "")).strip()
        if extra:
            param_parts.append(extra)

        cmd = raw_name
        if param_parts:
            cmd += " " + " ".join(param_parts)

        if run_fn is not None:
            try:
                return run_fn(cmd, 60)
            except Exception as exc:
                return f"[addon error] {exc}"

        # Fallback: run execute_command from YAML via shell
        exec_cmd = spec.get("execute_cmd", "")
        if exec_cmd:
            return self._shell_run(exec_cmd)
        return f"[addon] no run_fn and no execute_command for {raw_name}"

    # ── .tool dispatch ────────────────────────────────────────────────────────

    def _run_dottool(self, spec: Dict, arguments: Dict, config: Dict) -> str:
        ip       = str(arguments.get("ip", "") or config.get("rhost", "127.0.0.1")).strip()
        port     = str(arguments.get("port", "80")).strip()
        ssl      = bool(arguments.get("ssl", False))
        toolname = spec["raw_name"]

        outputdir = str(arguments.get("outputdir", "")).strip()
        if not outputdir:
            sessions = self._root / "sessions" / ip / port / toolname
            sessions.mkdir(parents=True, exist_ok=True)
            outputdir = str(sessions)

        try:
            cmd = _expand_tool_command(
                spec["command"], ip=ip, port=port, ssl=ssl,
                outputdir=outputdir, toolname=toolname
            )
        except Exception as exc:
            return f"[tool error] template expansion failed: {exc}"

        return self._shell_run(cmd)

    # ── plugin dispatch ───────────────────────────────────────────────────────

    def _run_plugin(
        self, spec: Dict, arguments: Dict, config: Dict, run_fn: Any
    ) -> str:
        raw_name = spec["raw_name"]
        param_parts: List[str] = []
        for p in (spec.get("params") or []):
            pname = p.get("name", "")
            if pname and pname in arguments:
                val = str(arguments[pname]).strip()
                if val:
                    param_parts.append(val)
        extra = str(arguments.get("args", "")).strip()
        if extra:
            param_parts.append(extra)

        cmd = raw_name
        if param_parts:
            cmd += " " + " ".join(param_parts)

        if run_fn is not None:
            try:
                return run_fn(cmd, 60)
            except Exception as exc:
                return f"[plugin error] {exc}"

        return f"[plugin] {raw_name}: no run_fn configured"

    # ── subprocess helper ─────────────────────────────────────────────────────

    @staticmethod
    def _shell_run(cmd: str, timeout: int = 120) -> str:
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            out = (result.stdout or "") + (result.stderr or "")
            return out.strip() or f"(no output — exit {result.returncode})"
        except subprocess.TimeoutExpired:
            return f"(timeout after {timeout}s — command continues in background)"
        except Exception as exc:
            return f"[shell error] {exc}"

    # ── Skills MD auto-regeneration ───────────────────────────────────────────

    _MD_HEADER = "## Auto-discovered tools"
    _MD_FOOTER = "<!-- end auto-discovered -->"

    def update_skills_md(self, skills_md_path: Path) -> None:
        """
        Append / replace the auto-discovered section in skills/lazyown.md.
        The section is delimited by HTML comments so it can be replaced cleanly.
        """
        if not skills_md_path.exists():
            log.debug(f"skills_md not found: {skills_md_path}")
            return

        lines = skills_md_path.read_text(errors="replace").splitlines()

        # Remove existing auto block
        start_idx: Optional[int] = None
        end_idx: Optional[int] = None
        for i, line in enumerate(lines):
            if line.strip() == self._MD_HEADER:
                start_idx = i
            if line.strip() == self._MD_FOOTER and start_idx is not None:
                end_idx = i
                break

        if start_idx is not None and end_idx is not None:
            lines = lines[:start_idx] + lines[end_idx + 1:]

        # Build new section
        new_block: List[str] = [
            "",
            self._MD_HEADER,
            "",
            "Discovered at server startup. Run `mcp restart` to refresh.",
            "",
            "| MCP Tool Name | Source | Description |",
            "|---|---|---|",
        ]

        for spec in sorted(self._specs, key=lambda s: s["mcp_name"]):
            desc = spec["description"].replace("|", "\\|")[:80]
            source_label = spec["source"]
            new_block.append(f"| `{spec['mcp_name']}` | {source_label} | {desc} |")

        new_block += ["", self._MD_FOOTER, ""]

        skills_md_path.write_text("\n".join(lines + new_block))
        log.info(f"skills_md updated: {len(self._specs)} dynamic tools written")

    # ── Stats ─────────────────────────────────────────────────────────────────

    def stats(self) -> str:
        counts = {"addon": 0, "tool": 0, "plugin": 0}
        for s in self._specs:
            counts[s["source"]] = counts.get(s["source"], 0) + 1
        return (
            f"AutoMapper: {sum(counts.values())} dynamic tools  "
            f"({counts['addon']} addons, {counts['tool']} pwntomate tools, "
            f"{counts['plugin']} plugins)"
        )

    def list_specs(self) -> List[Dict]:
        """Return raw spec dicts (useful for debugging / reporting)."""
        return list(self._specs)


# ── CLI helper ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    root = Path(__file__).parent.parent
    mapper = AutoMapper(root)
    print(mapper.stats())
    if "--list" in sys.argv or "-l" in sys.argv:
        for s in mapper.list_specs():
            print(f"  [{s['source']:6s}] {s['mcp_name']}")
    if "--update-md" in sys.argv:
        md_path = root / "skills" / "lazyown.md"
        mapper.update_skills_md(md_path)
        print(f"Updated: {md_path}")
