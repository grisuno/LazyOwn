"""Unified module registry for LazyOwn — catalog, search, use/run workflow.

Scans ``lazyaddons/`` (YAML), ``plugins/`` (Lua + YAML), ``modules/``
(Python), ``tools/`` (pwntomate), and ``playbooks/`` for all discoverable
modules. Every module is indexed with its metadata (name, author, version,
category, description, params) for ``show exploits`` / ``search`` /
``info`` / ``use`` / ``run``.
"""

from __future__ import annotations

import json
import logging
from collections import OrderedDict
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

try:
    import yaml
except ImportError:
    yaml = None

BASE_DIR = Path(__file__).resolve().parent.parent


_MODULE_TYPES = {
    "02. Scanning & Enumeration": "scanner",
    "03. Exploitation": "exploit",
    "04. Post-Exploitation": "post",
    "05. Persistence": "post",
    "06. Privilege Escalation": "post",
    "07. Credential Access": "auxiliary",
    "08. Lateral Movement": "post",
    "09. Data Exfiltration": "post",
    "10. Command & Control": "payload",
    "11. Reporting": "auxiliary",
    "12. Miscellaneous": "auxiliary",
    "13. AI Agents": "auxiliary",
    "14. Yaml Addon.": "auxiliary",
    "15. Pwntomate Tools": "auxiliary",
    "01. Reconnaissance": "scanner",
}


def _classify(category: str) -> str:
    for prefix, mtype in _MODULE_TYPES.items():
        if category.startswith(prefix.rstrip(".")):
            return mtype
    return "auxiliary"


_MODULE_TYPE_CATEGORY: dict[str, str] = {
    "scanner": "02. Scanning & Enumeration",
    "exploit": "03. Exploitation",
    "post": "04. Post-Exploitation",
    "payload": "10. Command & Control",
    "auxiliary": "12. Miscellaneous",
}


_SCANNER_KEYWORDS = [
    "scan", "nmap", "enum", "discover", "recon", "fingerprint",
    "gobuster", "ffuf", "dirb", "nikto", "nuclei", "whatweb",
]
_EXPLOIT_KEYWORDS = [
    "exploit", "cve", "poc", "rce", "overflow", "injection",
    "bypass", "shell", "code_exec", "cmd_exec", "sqli", "xss",
]
_POST_KEYWORDS = [
    "privesc", "persist", "lateral", "exfil", "pivot", "creds",
    "impacket", "mimikatz", "bloodhound", "kerberoast", "asreproast",
]
_PAYLOAD_KEYWORDS = [
    "payload", "shellcode", "stager", "beacon", "implant", "dropper",
    "loader", "c2", "reverse", "bind",
]


def _classify_module_source(name: str, source: str) -> str:
    """Classify a Python module by its name and source content."""
    combined = f"{name} {source}".lower()
    for kw in _EXPLOIT_KEYWORDS:
        if kw in combined:
            return "exploit"
    for kw in _POST_KEYWORDS:
        if kw in combined:
            return "post"
    for kw in _PAYLOAD_KEYWORDS:
        if kw in combined:
            return "payload"
    for kw in _SCANNER_KEYWORDS:
        if kw in combined:
            return "scanner"
    return "auxiliary"


def _extract_docstring_summary(source: str) -> str:
    """Extract the first line of a module's docstring."""
    import ast
    try:
        tree = ast.parse(source)
        doc = ast.get_docstring(tree)
        if doc:
            return doc.split("\n")[0].strip()[:120]
    except SyntaxError:
        pass
    return ""


class ModuleInfo:
    """Metadata for a single discoverable module.

    Attributes:
        name: Short module name (e.g. ``nuclei``).
        module_type: One of ``exploit``, ``scanner``, ``auxiliary``,
            ``post``, ``payload``.
        author: Original author or tool maintainer.
        version: Tool version string.
        description: Human-readable summary.
        category: Kill-chain category label.
        path: Absolute filesystem path to the module definition.
        source: Where it was loaded from (``yaml``, ``lua``, ``python``,
            ``pwntomate``, ``playbook``).
        params: List of parameter dicts (name, type, required, default,
            description).
        enabled: Whether the module is active.
        deprecated: Whether the module is superseded.
        replaced_by: Name of the replacement module.
        deprecation_message: Human-readable migration guidance.
    """

    def __init__(
        self,
        name: str,
        module_type: str = "auxiliary",
        author: str = "",
        version: str = "",
        description: str = "",
        category: str = "",
        path: str = "",
        source: str = "yaml",
        params: list[dict[str, Any]] | None = None,
        enabled: bool = True,
        deprecated: bool = False,
        replaced_by: str = "",
        deprecation_message: str = "",
    ) -> None:
        self.name = name
        self.module_type = module_type
        self.author = author
        self.version = version
        self.description = description
        self.category = category
        self.path = path
        self.source = source
        self.params = params or []
        self.enabled = enabled
        self.deprecated = deprecated
        self.replaced_by = replaced_by
        self.deprecation_message = deprecation_message

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "type": self.module_type,
            "author": self.author,
            "version": self.version,
            "description": self.description,
            "category": self.category,
            "path": self.path,
            "source": self.source,
            "params": self.params,
            "enabled": self.enabled,
            "deprecated": self.deprecated,
            "replaced_by": self.replaced_by,
            "deprecation_message": self.deprecation_message,
        }

    def __repr__(self) -> str:
        return f"<ModuleInfo {self.module_type}/{self.name}>"


class ModuleRegistry:
    """Scans and indexes all discoverable modules in the framework.

    The registry is a singleton per process — call
    :func:`ModuleRegistry.get_instance` or just construct one and reuse it.

    Args:
        base_dir: Root directory of the LazyOwn project.
    """

    _instance: ModuleRegistry | None = None

    def __init__(self, base_dir: str | Path | None = None) -> None:
        self._base = Path(base_dir) if base_dir else BASE_DIR
        self._modules: dict[str, ModuleInfo] = OrderedDict()
        self._scanned = False

    @classmethod
    def get_instance(cls, base_dir: str | Path | None = None) -> ModuleRegistry:
        """Return the singleton registry instance."""
        if cls._instance is None:
            cls._instance = cls(base_dir)
        return cls._instance

    def scan(self) -> list[ModuleInfo]:
        """Scan all module directories and return the full list."""
        if self._scanned:
            return list(self._modules.values())
        self._modules.clear()
        self._scan_yaml_addons()
        self._scan_plugins()
        self._scan_python_modules()
        self._scan_tools()
        self._scan_playbooks()
        self._scanned = True
        return list(self._modules.values())

    def rescan(self) -> list[ModuleInfo]:
        """Force a full rescan and return modules."""
        self._scanned = False
        return self.scan()

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(self, name: str) -> ModuleInfo | None:
        """Get a module by name."""
        if not self._scanned:
            self.scan()
        return self._modules.get(name)

    def search(
        self,
        query: str = "",
        module_type: str | None = None,
        category: str | None = None,
        enabled_only: bool = True,
        include_deprecated: bool = False,
    ) -> list[ModuleInfo]:
        """Search indexed modules.

        Args:
            query: Free-text search in name, description, author.
            module_type: Filter by type (``exploit``, ``scanner``, ...).
            category: Filter by kill-chain category.
            enabled_only: Only return enabled modules.
            include_deprecated: Include deprecated modules in results.

        Returns:
            List of matching :class:`ModuleInfo`.
        """
        if not self._scanned:
            self.scan()
        q = query.lower().strip()
        results: list[ModuleInfo] = []
        for m in self._modules.values():
            if enabled_only and not m.enabled:
                continue
            if not include_deprecated and m.deprecated:
                continue
            if module_type and m.module_type != module_type:
                continue
            if category and m.category != category:
                continue
            if q:
                if (
                    q in m.name.lower()
                    or q in m.description.lower()
                    or q in m.author.lower()
                ):
                    results.append(m)
            else:
                results.append(m)
        return results

    def deprecated_modules(self) -> list[ModuleInfo]:
        """Return all deprecated modules."""
        if not self._scanned:
            self.scan()
        return [m for m in self._modules.values() if m.deprecated]

    def by_type(self, module_type: str) -> list[ModuleInfo]:
        """Shorthand for ``search(module_type=module_type)``."""
        return self.search(module_type=module_type)

    def summary(self) -> dict[str, int]:
        """Return counts by module type."""
        if not self._scanned:
            self.scan()
        counts: dict[str, int] = {}
        for m in self._modules.values():
            counts[m.module_type] = counts.get(m.module_type, 0) + 1
        return counts

    # ------------------------------------------------------------------
    # Internal scanners
    # ------------------------------------------------------------------

    def _scan_yaml_addons(self) -> None:
        addons_dir = self._base / "lazyaddons"
        if not addons_dir.is_dir():
            return
        for fpath in sorted(addons_dir.glob("*.yaml")):
            try:
                data = self._load_yaml(fpath)
                if not data or not data.get("enabled", True):
                    continue
                name = data.get("name", fpath.stem)
                cat = data.get("category", "12. Miscellaneous")
                mtype = _classify(cat)
                data.get("tool", {})
                deprecated = data.get("deprecated", False)
                replaced_by = data.get("replaced_by", "")
                deprecation_message = data.get("deprecation_message", "")
                if deprecated:
                    logger.warning(
                        "Module %r is deprecated%s%s",
                        name,
                        f" — replaced by {replaced_by!r}" if replaced_by else "",
                        f": {deprecation_message}" if deprecation_message else "",
                    )
                self._modules[name] = ModuleInfo(
                    name=name,
                    module_type=mtype,
                    author=data.get("author", ""),
                    version=data.get("version", ""),
                    description=data.get("description", ""),
                    category=cat,
                    path=str(fpath),
                    source="yaml",
                    params=data.get("params", []),
                    enabled=data.get("enabled", True),
                    deprecated=deprecated,
                    replaced_by=replaced_by,
                    deprecation_message=deprecation_message,
                )
            except Exception:
                continue

    def _scan_plugins(self) -> None:
        plugins_dir = self._base / "plugins"
        if not plugins_dir.is_dir():
            return
        for fpath in sorted(plugins_dir.glob("*.yaml")):
            try:
                data = self._load_yaml(fpath)
                if not data:
                    continue
                name = data.get("name", fpath.stem)
                cat = data.get("category", "12. Miscellaneous")
                mtype = _classify(cat)
                deprecated = data.get("deprecated", False)
                replaced_by = data.get("replaced_by", "")
                deprecation_message = data.get("deprecation_message", "")
                if deprecated:
                    logger.warning(
                        "Plugin %r is deprecated%s%s",
                        name,
                        f" — replaced by {replaced_by!r}" if replaced_by else "",
                        f": {deprecation_message}" if deprecation_message else "",
                    )
                self._modules[name] = ModuleInfo(
                    name=name,
                    module_type=mtype,
                    author=data.get("author", ""),
                    version=data.get("version", ""),
                    description=data.get("description", ""),
                    category=cat,
                    path=str(fpath),
                    source="lua",
                    params=data.get("params", []),
                    enabled=True,
                    deprecated=deprecated,
                    replaced_by=replaced_by,
                    deprecation_message=deprecation_message,
                )
            except Exception:
                continue

    def _scan_tools(self) -> None:
        tools_dir = self._base / "tools"
        category_map = {
            "websrv": "scanner",
            "smb": "auxiliary",
            "dns": "scanner",
            "ldap": "auxiliary",
            "http": "scanner",
        }
        if not tools_dir.is_dir():
            return
        for fpath in sorted(tools_dir.glob("*.tool")):
            try:
                data = json.loads(fpath.read_text())
                name = data.get("name", fpath.stem)
                trigger = data.get("trigger", "")
                mtype = "auxiliary"
                for prefix, t in category_map.items():
                    if trigger.startswith(prefix):
                        mtype = t
                        break
                tool_cat = data.get("category", "15. Pwntomate Tools")
                self._modules[name] = ModuleInfo(
                    name=name,
                    module_type=mtype,
                    description=data.get("description", ""),
                    category=tool_cat,
                    path=str(fpath),
                    source="pwntomate",
                    enabled=True,
                )
            except Exception:
                continue

    def _scan_playbooks(self) -> None:
        pb_dir = self._base / "playbooks"
        if not pb_dir.is_dir():
            return
        for fpath in sorted(pb_dir.glob("*.json")):
            try:
                data = json.loads(fpath.read_text())
                name = data.get("name", fpath.stem)
                self._modules[name] = ModuleInfo(
                    name=name,
                    module_type="post",
                    description=data.get("description", f"APT playbook: {name}"),
                    category="04. Post-Exploitation",
                    path=str(fpath),
                    source="playbook",
                    enabled=True,
                )
            except Exception:
                continue

    def _scan_python_modules(self) -> None:
        """Scan ``modules/`` for Python files with discoverable entry points."""
        modules_dir = self._base / "modules"
        if not modules_dir.is_dir():
            return
        for fpath in sorted(modules_dir.glob("*.py")):
            if fpath.stem.startswith("_") or fpath.stem in ("cli", "gui"):
                continue
            try:
                source = fpath.read_text(errors="replace")
            except OSError:
                continue
            name = fpath.stem
            mtype = _classify_module_source(name, source)
            if not self._looks_discoverable(source):
                continue
            desc = _extract_docstring_summary(source) or f"Python module: {name}"
            self._modules[name] = ModuleInfo(
                name=name,
                module_type=mtype,
                author="LazyOwn",
                version="",
                description=desc,
                category=_MODULE_TYPE_CATEGORY.get(mtype, "12. Miscellaneous"),
                path=str(fpath),
                source="python",
                enabled=True,
            )

    @staticmethod
    def _looks_discoverable(source: str) -> bool:
        """Heuristic: a module is discoverable if it defines a runnable entry point."""
        import re
        markers = [
            r"def\s+main\s*\(.*\)\s*(?:->.*)?\s*:",
            r"def\s+run\s*\(.*\)\s*(?:->.*)?\s*:",
            r"def\s+execute\s*\(.*\)\s*(?:->.*)?\s*:",
            r"class\s+\w+\(.*\)\s*:",
            r"class\s+\w+\s*:",
        ]
        return any(re.search(m, source, re.MULTILINE) for m in markers)

    @staticmethod
    def _load_yaml(path: Path) -> dict | None:
        if yaml is None:
            return None
        try:
            with open(path) as f:
                return yaml.safe_load(f)
        except Exception:
            return None

    def __len__(self) -> int:
        if not self._scanned:
            self.scan()
        return len(self._modules)

    def __iter__(self):
        if not self._scanned:
            self.scan()
        return iter(self._modules.values())

    def __contains__(self, name: str) -> bool:
        if not self._scanned:
            self.scan()
        return name in self._modules


def format_module_table(
    modules: list[ModuleInfo],
    cols: tuple[str, ...] = ("name", "type", "author", "description"),
) -> str:
    """Format a list of modules as an aligned text table.

    Args:
        modules: Module list to format.
        cols: Column keys to include (in order). Valid keys: ``id``,
            ``name``, ``type``, ``author``, ``version``, ``description``.

    Returns:
        Multi-line string with aligned columns.
    """
    if not modules:
        return "No modules found."

    rows: list[list[str]] = []
    for i, m in enumerate(modules, 1):
        row = []
        for col in cols:
            if col == "id":
                row.append(str(i))
            elif col == "name":
                row.append(f"[DEPRECATED] {m.name}" if m.deprecated else m.name)
            elif col == "type":
                row.append(m.module_type)
            elif col == "author":
                row.append(m.author or "-")
            elif col == "version":
                row.append(m.version or "-")
            elif col == "description":
                desc = m.description.replace("\n", " ")[:70]
                row.append(desc)
            else:
                row.append("")
        rows.append(row)

    widths = [max(len(r[i]) for r in rows + [[c for c in cols]]) for i in range(len(cols))]
    header = "  ".join(c.ljust(w) for c, w in zip(cols, widths, strict=False))
    sep = "  ".join("-" * w for w in widths)
    lines = [header, sep]
    for row in rows:
        lines.append("  ".join(v.ljust(w) for v, w in zip(row, widths, strict=False)))
    return "\n".join(lines)


def format_module_detail(m: ModuleInfo) -> str:
    """Format a single module's full metadata."""
    lines = [
        f"Name       : {m.name}",
        f"Type       : {m.module_type}",
        f"Author     : {m.author or '-'}",
        f"Version    : {m.version or '-'}",
        f"Category   : {m.category}",
        f"Source     : {m.source}",
        f"Path       : {m.path}",
        f"Enabled    : {'yes' if m.enabled else 'no'}",
    ]
    if m.deprecated:
        lines.append(f"Deprecated : yes")
        if m.replaced_by:
            lines.append(f"Replaced by: {m.replaced_by}")
        if m.deprecation_message:
            lines.append(f"Message    : {m.deprecation_message}")
    lines.append(f"Description: {m.description.replace(chr(10), ' ').strip()}")
    if m.params:
        lines.append("")
        lines.append("Options:")
        lines.append(f"  {'Name':<20} {'Required':<10} {'Default':<20} {'Description'}")
        lines.append(f"  {'-'*20} {'-'*10} {'-'*20} {'-'*30}")
        for p in m.params:
            pname = p.get("name", "")
            required = "yes" if p.get("required", False) else "no"
            default = str(p.get("default", ""))
            desc = p.get("description", "")[:40]
            lines.append(f"  {pname:<20} {required:<10} {default:<20} {desc}")
    return "\n".join(lines)


__all__ = [
    "ModuleRegistry",
    "ModuleInfo",
    "format_module_table",
    "format_module_detail",
    "_classify",
    "_classify_module_source",
    "_extract_docstring_summary",
]
