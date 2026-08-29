"""Unified plugin loader — YAML addons, Lua plugins, and .tool files."""

from __future__ import annotations

import glob
import json
import os
import re
import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import yaml

try:
    from lupa import LuaRuntime
except ImportError:
    LuaRuntime = None  # type: ignore[assignment,misc]

from config import PayloadConfig

_SHELL_META_RE = re.compile(r"[;&|`$(){}!\n\r]")
_URL_RE = re.compile(r"^https?://[a-zA-Z0-9\-._~:/?#\[\]@!$&'()*+,;=%]+$")


@dataclass
class PluginSpec:
    """Metadata for a single registered command."""

    name: str
    description: str
    source: str  # "yaml" | "lua" | "tool"
    category: str
    os_target: str = "any"
    params: list[dict[str, Any]] = field(default_factory=list)
    enabled: bool = True


def _replace_placeholders(command: str, params: dict[str, Any]) -> str:
    """Replace {key} tokens in a command string with values from params."""

    def _subst(match: re.Match) -> str:
        key = match.group(1).strip()
        val = params.get(key, match.group(0))
        return str(val)

    return re.sub(r"\{([^}]+)\}", _subst, command)


def _validate_clone_url(url: str) -> str:
    """Validate a git clone URL, rejecting shell metacharacters.

    Args:
        url: The repository URL to validate.

    Returns:
        The validated URL.

    Raises:
        ValueError: If the URL contains shell metacharacters or is invalid.
    """
    if not url or not url.strip():
        raise ValueError("Repository URL must not be empty")
    url = url.strip()
    if _SHELL_META_RE.search(url):
        raise ValueError(
            f"Shell metacharacters rejected in URL: {url[:80]}"
        )
    if not _URL_RE.match(url):
        raise ValueError(f"Invalid repository URL format: {url[:80]}")
    return url


class PluginLoader:
    """Load and register all plugin types into a command registry.

    The registry is a plain dict mapping command names to callables.
    This class is framework-agnostic — the Textual app owns the dispatch loop.
    """

    def __init__(
        self,
        config: PayloadConfig,
        base_dir: str | Path = ".",
    ) -> None:
        self.config = config
        self.base_dir = Path(base_dir)
        self.registry: dict[str, Callable[[str], str | None]] = {}
        self.specs: dict[str, PluginSpec] = {}
        self.lua_runtime: Any = None
        self._setup_lua()

    # -- Lua runtime bootstrap ------------------------------------------------

    def _setup_lua(self) -> None:
        if LuaRuntime is None:
            return
        self.lua_runtime = LuaRuntime(unpack_returned_tuples=True)
        lua_globals = self.lua_runtime.globals()
        lua_globals["register_command"] = self._lua_register
        lua_globals["app"] = _LuaAppProxy(self.config)
        lua_globals["list_files_in_directory"] = self._list_files

    def _lua_register(self, name: str, func: Any) -> None:
        """Bridge: Lua calls register_command(name, fn) -> we wrap it."""

        def wrapper(arg: str = "") -> str | None:
            result = func(arg)
            if result is not None:
                return str(result)
            return None

        self.registry[name] = wrapper
        self.specs[name] = PluginSpec(
            name=name,
            description=f"Lua plugin: {name}",
            source="lua",
            category="13. Lua Plugin",
        )

    def _list_files(self, directory: str) -> list[str]:
        try:
            return os.listdir(directory)
        except OSError:
            return []

    # -- Public load methods --------------------------------------------------

    def load_all(self) -> dict[str, PluginSpec]:
        """Load yaml addons, lua plugins, and .tool files. Return specs."""
        self._load_yaml_addons()
        self._load_lua_plugins()
        self._load_tool_files()
        return dict(self.specs)

    # -- YAML addons (lazyaddons/*.yaml) --------------------------------------

    def _load_yaml_addons(self) -> None:
        addons_dir = self.base_dir / "lazyaddons"
        if not addons_dir.is_dir():
            return
        for path in sorted(addons_dir.glob("*.yaml")):
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not data or not data.get("enabled", False):
                continue
            self._register_yaml_addon(data)

    def _register_yaml_addon(self, data: dict[str, Any]) -> None:
        name = data["name"]
        tool = data.get("tool", {})
        description = data.get("description", "")
        category = data.get("category", "14. Yaml Addon")
        params_def = data.get("params", [])
        execute_cmd = tool.get("execute_command", "")
        install_path = tool.get("install_path", "")
        repo_url = tool.get("repo_url", "")
        install_cmd = tool.get("install_command", "")

        def wrapper(arg: str = "") -> str | None:
            params = dict(self.config._data)

            if install_path:
                full_install = self.base_dir / install_path
                if not full_install.exists() and repo_url:
                    validated_url = _validate_clone_url(repo_url)
                    subprocess.run(
                        ["git", "clone", validated_url, str(full_install)],
                        shell=False,
                        capture_output=True,
                        text=True,
                        timeout=120,
                    )
                    if install_cmd:
                        ic = _replace_placeholders(install_cmd, params)
                        subprocess.run(
                            ic,
                            shell=True,
                            capture_output=True,
                            text=True,
                            timeout=300,
                            cwd=str(full_install),
                        )

            if execute_cmd:
                cmd = _replace_placeholders(execute_cmd, params)
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                output = result.stdout + result.stderr
                return output.strip() if output.strip() else None
            return None

        wrapper.__doc__ = description
        self.registry[name] = wrapper
        self.specs[name] = PluginSpec(
            name=name,
            description=description,
            source="yaml",
            category=category,
            os_target=data.get("os", "any"),
            params=params_def,
        )

    # -- Lua plugins (plugins/*.lua + plugins/*.yaml) -------------------------

    def _load_lua_plugins(self) -> None:
        if self.lua_runtime is None:
            return
        plugins_dir = self.base_dir / "plugins"
        if not plugins_dir.is_dir():
            return
        for lua_path in sorted(plugins_dir.glob("*.lua")):
            yaml_path = lua_path.with_suffix(".yaml")
            if yaml_path.name == "init_plugins.yaml":
                continue
            if yaml_path.exists():
                try:
                    meta = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
                    if not meta.get("enabled", False):
                        continue
                except Exception:
                    continue
            try:
                script = lua_path.read_text(encoding="utf-8")
                self.lua_runtime.execute(script)
            except Exception as e:
                print(f"[!] Lua plugin error {lua_path.name}: {e}")

    # -- .tool files (tools/*.tool) -------------------------------------------

    def _load_tool_files(self) -> None:
        tools_dir = self.base_dir / "tools"
        if not tools_dir.is_dir():
            return
        for tool_path in sorted(tools_dir.glob("*.tool")):
            try:
                data = json.loads(tool_path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not data.get("active", False):
                continue
            self._register_tool(data)

    def _register_tool(self, data: dict[str, Any]) -> None:
        name = data.get("toolname", "")
        command = data.get("command", "")
        category = data.get("category", "15. Pwntomate Tools")
        description = data.get("description", "")
        if not name or not command:
            return

        def wrapper(arg: str = "") -> str | None:
            params = dict(self.config._data)
            cmd = _replace_placeholders(command, params)
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300,
            )
            output = result.stdout + result.stderr
            return output.strip() if output.strip() else None

        self.registry[name] = wrapper
        self.specs[name] = PluginSpec(
            name=name,
            description=description,
            source="tool",
            category=category,
        )


class _LuaAppProxy:
    """Minimal proxy exposed to Lua plugins as the global ``app`` object."""

    def __init__(self, config: PayloadConfig) -> None:
        self._config = config

    @property
    def params(self) -> dict[str, Any]:
        return self._config._data

    def one_cmd(self, cmd: str) -> None:
        subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            timeout=300,
        )
