"""Plugin/addon marketplace commands.

Discover, install, and manage community plugins, lazyaddons, and Lua
payload generators from local and remote sources.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import cmd2

from cli.commands._base import LazyOwnCommandSet
from cli.marketplace_config import (
    AddonRegistry,
    configure_marketplace_interactive,
    marketplace_summary,
)
from modules.module_registry import ModuleRegistry
from utils import (
    miscellaneous_category,
    print_error,
    print_msg,
    print_warn,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LAZYADDONS_DIR = BASE_DIR / "lazyaddons"
PLUGINS_DIR = BASE_DIR / "plugins"
TOOLS_DIR = BASE_DIR / "tools"

COMMUNITY_REPO = "https://github.com/grisuno/lazyown-community-plugins.git"
MARKETPLACE_CACHE = BASE_DIR / "sessions" / "marketplace"


def _safe_git_clone(repo_url: str, dest: Path, depth: int = 1) -> bool:
    """Clone a git repository shallow, returning success."""
    try:
        subprocess.run(
            ["git", "clone", "--depth", str(depth), repo_url, str(dest)],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        return dest.exists()
    except FileNotFoundError:
        return False


class MarketplaceCommandSet(LazyOwnCommandSet):
    """Browse and install community plugins, addons, and tool integrations."""

    phase = "marketplace"
    category = "12. Miscellaneous"

    def _registry(self) -> ModuleRegistry:
        shell = self._resolve_shell()
        if shell is not None and getattr(shell, "_module_registry", None) is not None:
            return shell._module_registry
        return ModuleRegistry()

    def _installed_plugins(self) -> dict[str, list[str]]:
        """Return dict of category -> list of installed names."""
        installed: dict[str, list[str]] = {
            "lazyaddons": [],
            "plugins": [],
            "tools": [],
        }
        if LAZYADDONS_DIR.exists():
            installed["lazyaddons"] = sorted([f.stem for f in LAZYADDONS_DIR.glob("*.yaml")])
        if PLUGINS_DIR.exists():
            installed["plugins"] = sorted(
                [f.stem for f in PLUGINS_DIR.glob("*.yaml")] + [f.stem for f in PLUGINS_DIR.glob("*.lua")]
            )
        if TOOLS_DIR.exists():
            installed["tools"] = sorted([f.stem for f in TOOLS_DIR.glob("*.tool")])
        return installed

    @cmd2.with_category(miscellaneous_category)
    def do_marketplace(self, line):
        """Discover and install community plugins, addons, and tools.

        Usage:
            marketplace list           — show installed plugins/addons
            marketplace search <name>  — search for available plugins
            marketplace install <name> — install a plugin by name
            marketplace update         — refresh community plugin index
            marketplace info <name>    — show details about a plugin
            marketplace config         — interactive enable/disable wizard

        Examples:
            marketplace list
            marketplace search c2
            marketplace install phantom2
            marketplace config
        """
        args = line.strip().split()
        if not args:
            print_msg("Usage: marketplace [list|search|install|update|info|config] [name]")
            print_msg("Try: marketplace list")
            return

        action = args[0].lower()
        name = args[1] if len(args) > 1 else ""

        if action == "list":
            self._mp_list()
        elif action == "search":
            if not name:
                print_error("Specify a search term. Try: marketplace search c2")
                return
            self._mp_search(name)
        elif action == "install":
            if not name:
                print_error("Specify a plugin name. Try: marketplace search")
                return
            self._mp_install(name)
        elif action == "update":
            self._mp_update()
        elif action == "info":
            if not name:
                print_error("Specify a plugin name. Try: marketplace list")
                return
            self._mp_info(name)
        elif action == "config":
            self._mp_interactive_config()
        else:
            print_error(f"Unknown action: {action}. Use list, search, install, update, info, or config.")

    def _mp_list(self):
        """Display installed plugins grouped by category."""
        installed = self._installed_plugins()
        total = sum(len(v) for v in installed.values())

        print_msg(f"\nInstalled plugins, addons, and tools ({total} total):\n")

        for category, names in installed.items():
            if names:
                print_msg(f"  [{category}] ({len(names)})")
                for name in names:
                    print_msg(f"    - {name}")

        if total == 0:
            print_warn("No plugins installed. Use 'marketplace update && marketplace search' to browse.")
            return

        print_msg("")
        print_msg(f"  lazyaddons/  -> {LAZYADDONS_DIR} ({len(installed['lazyaddons'])} YAML)")
        print_msg(f"  plugins/     -> {PLUGINS_DIR} ({len(installed['plugins'])} YAML/Lua)")
        print_msg(f"  tools/       -> {TOOLS_DIR} ({len(installed['tools'])} .tool)")

    def _mp_search(self, query: str):
        """Search installed and suggest community plugins."""
        query_lower = query.lower()
        installed = self._installed_plugins()
        registry = self._registry()

        print_msg(f"\nSearching for '{query}' ...\n")

        found = 0

        print_msg("  [local]")
        for category, names in installed.items():
            for name in names:
                if query_lower in name.lower():
                    found += 1
                    print_msg(f"    {category}/{name}  (installed)")

        try:
            modules = registry.list_all() if hasattr(registry, "list_all") else []
            print_msg("\n  [modules]")
            for mod in modules:
                mod_name = mod.get("name", "")
                mod_desc = mod.get("description", "")
                if query_lower in mod_name.lower() or query_lower in mod_desc.lower():
                    found += 1
                    mod_type = mod.get("type", "module")
                    print_msg(f"    modules/{mod_name}  [{mod_type}] {mod_desc[:60]}")
        except Exception:
            pass

        if found == 0:
            print_msg(f"    No matches for '{query}'.")
            print_msg("    Try: marketplace update (to refresh community index)")
        else:
            print_msg(f"\n  {found} match(es) found.")
            print_msg("  Use: marketplace install <name> to install.")

    def _mp_install(self, name: str):
        """Install a plugin from the community repository."""
        installed = self._installed_plugins()

        for category, names in installed.items():
            if name in names:
                print_warn(f"'{name}' is already installed in {category}/.")
                return

        registry = self._registry()
        try:
            modules = registry.list_all() if hasattr(registry, "list_all") else []
            for mod in modules:
                if mod.get("name") == name:
                    print_msg(f"'{name}' is a built-in module (no install needed).")
                    print_msg(f"  {mod.get('description', '')}")
                    return
        except Exception:
            pass

        MARKETPLACE_CACHE.mkdir(parents=True, exist_ok=True)

        if not (MARKETPLACE_CACHE / "community").exists():
            print_msg("Pulling community plugin index ...")
            ok = _safe_git_clone(COMMUNITY_REPO, MARKETPLACE_CACHE / "community")
            if not ok:
                print_error("Failed to fetch community index. Check your network.")
                print_error(f"Repo: {COMMUNITY_REPO}")
                return

        community_dir = MARKETPLACE_CACHE / "community"

        for src, dest_dir, ext in [
            ("lazyaddons", LAZYADDONS_DIR, ".yaml"),
            ("plugins", PLUGINS_DIR, ".yaml"),
            ("tools", TOOLS_DIR, ".tool"),
        ]:
            candidate = community_dir / src / f"{name}{ext}"
            if candidate.exists():
                import shutil

                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(candidate, dest_dir / f"{name}{ext}")
                print_msg(f"Installed: {name}{ext} -> {src}/")
                return

            candidate_lua = community_dir / src / f"{name}.lua"
            if candidate_lua.exists():
                import shutil

                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(candidate_lua, dest_dir / f"{name}.lua")
                print_msg(f"Installed: {name}.lua -> {src}/")
                return

        print_error(f"Plugin '{name}' not found in community repository.")
        print_msg(f"Try: marketplace search {name}")
        print_msg(f"Contribute: {COMMUNITY_REPO}")

    def _mp_update(self):
        """Refresh the community plugin index."""
        MARKETPLACE_CACHE.mkdir(parents=True, exist_ok=True)

        community_path = MARKETPLACE_CACHE / "community"
        if community_path.exists():
            print_msg("Updating community plugin index ...")
            try:
                subprocess.run(
                    ["git", "-C", str(community_path), "pull", "--ff-only"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                print_msg("Community index updated.")
            except FileNotFoundError:
                print_error("Git not found. Cannot update.")
        else:
            print_msg("Cloning community plugin index ...")
            ok = _safe_git_clone(COMMUNITY_REPO, community_path)
            if ok:
                print_msg("Community index downloaded.")
            else:
                print_error(f"Failed to clone {COMMUNITY_REPO}")
                return

        installed = self._installed_plugins()
        total = sum(len(v) for v in installed.values())
        print_msg(f"Local install: {total} plugins/addons/tools ready.")
        print_msg("Use: marketplace list  (to see what's installed)")
        print_msg("Use: marketplace search <term>")

    def _mp_info(self, name: str):
        """Show detailed information about a plugin."""
        installed = self._installed_plugins()
        found = False

        for category, names in installed.items():
            if name in names:
                found = True
                base = {"lazyaddons": LAZYADDONS_DIR, "plugins": PLUGINS_DIR, "tools": TOOLS_DIR}[category]
                for ext in (".yaml", ".lua", ".tool"):
                    path = base / f"{name}{ext}"
                    if path.exists():
                        size = path.stat().st_size
                        print_msg(f"\n  Name:     {name}")
                        print_msg(f"  Category: {category}")
                        print_msg(f"  Path:     {path}")
                        print_msg(f"  Size:     {size} bytes ({size / 1024:.1f} KB)")
                        try:
                            content = path.read_text(encoding="utf-8", errors="replace")
                            lines = content.splitlines()
                            description = next(
                                (
                                    line.strip().lstrip("# ").lstrip("- ")
                                    for line in lines[:10]
                                    if line.strip() and not line.strip().startswith("---")
                                ),
                                "",
                            )
                            if description:
                                print_msg(f"  Desc:     {description[:100]}")
                        except Exception:
                            pass
                        break

        if not found:
            print_error(f"Plugin '{name}' is not installed.")
            print_msg("Use: marketplace search <name>")

    def _mp_interactive_config(self):
        """Launch the interactive marketplace configurator (curses TUI)."""
        result = configure_marketplace_interactive()
        if result is None:
            print_warn("marketplace configuration cancelled, no changes made")
            return
        enabled_count = sum(len(v) for v in result.enabled.values())
        total = sum(1 for tab in ("lazyaddons", "plugins", "tools") for _ in result.enabled.get(tab, set()))
        print_msg(f"marketplace config saved: {enabled_count}/{total} addons enabled")
        print_msg(marketplace_summary())

    @cmd2.with_category(miscellaneous_category)
    def do_marketplace_config(self, line):
        """Interactive marketplace manager (curses TUI).

        Opens a Powerlevel10k-style wizard to browse, enable/disable,
        edit (``e``), and create (``c``) lazyaddons, plugins, and tools.

        Usage:
            marketplace_config            — open the interactive wizard
            marketplace_config show       — print a text summary
            marketplace_config enable <n> — enable a plugin by name
            marketplace_config disable <n> — disable a plugin by name

        The wizard mirrors ``config_banner``: Arrow keys move, Space
        toggles, ``a``/``n`` enable/disable all, ``e`` edits in $EDITOR,
        ``c`` creates a new lazyaddon from template, Enter saves, Escape
        cancels.
        """
        args = (line or "").strip().split()
        action = args[0].lower() if args else ""

        if action in {"show", "list", "status"}:
            print_msg(marketplace_summary())
            return

        if action == "enable" and len(args) > 1:
            self._mp_toggle_addon(args[1], True)
            return

        if action == "disable" and len(args) > 1:
            self._mp_toggle_addon(args[1], False)
            return

        if action in {"enable", "disable"} and len(args) == 1:
            print_error("Specify an addon name. Try: marketplace_config show")
            return

        if action and action not in {"show", "list", "status"}:
            print_msg("Opening wizard directly. Use 'marketplace_config show' for a text summary.")
            print_msg("Use 'marketplace_config enable/disable <name>' for quick toggles.")

        self._mp_interactive_config()

    def _mp_toggle_addon(self, name: str, enable_state: bool):
        """Enable or disable an addon by name across all directories."""
        registry = AddonRegistry()
        found = False
        for tab in ("lazyaddons", "plugins", "tools"):
            for addon in registry.scan(tab):
                if addon.name == name:
                    if addon.enabled != enable_state:
                        addon.set_enabled(enable_state)
                    state = "enabled" if enable_state else "disabled"
                    print_msg(f"'{name}': {state}")
                    found = True
                    break
            if found:
                break
        if not found:
            print_error(f"Addon '{name}' not found. Try: marketplace list")
