"""Unified module registry for LazyOwn — catalog, search, use/run workflow.

Scans ``lazyaddons/`` (YAML), ``plugins/`` (Lua + YAML), ``modules/``
(Python), ``tools/`` (pwntomate), and ``playbooks/`` for all discoverable
modules. Every module is indexed with its metadata (name, author, version,
category, description, params) for ``show exploits`` / ``search`` /
``info`` / ``use`` / ``run``.
"""

from __future__ import annotations

import json
from collections import OrderedDict
from pathlib import Path
from typing import Any

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
    ) -> list[ModuleInfo]:
        """Search indexed modules.

        Args:
            query: Free-text search in name, description, author.
            module_type: Filter by type (``exploit``, ``scanner``, ...).
            category: Filter by kill-chain category.
            enabled_only: Only return enabled modules.

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
                row.append(m.name)
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
        f"Description: {m.description.replace(chr(10), ' ').strip()}",
    ]
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
]
