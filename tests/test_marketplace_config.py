"""Marketplace registry and settings: formats, toggles, CRUD."""

from __future__ import annotations

import json

import yaml

from cli import marketplace_config as mp


def _registry(tmp_path, monkeypatch):
    lazyaddons = tmp_path / "lazyaddons"
    plugins = tmp_path / "plugins"
    tools = tmp_path / "tools"
    yara = tmp_path / "yara_rules"
    for directory in (lazyaddons, plugins, tools, yara):
        directory.mkdir()
    monkeypatch.setattr(
        mp.AddonRegistry,
        "_TAB_SOURCES",
        {
            "lazyaddons": (lazyaddons, ("*.yaml",)),
            "plugins": (plugins, ("*.yaml",)),
            "tools": (tools, ("*.tool",)),
        },
    )
    monkeypatch.setattr(mp, "YARA_DIR", yara)
    monkeypatch.setattr(mp, "_NUCLEI_CANDIDATES", [tmp_path / "nuclei-templates"])
    return mp.AddonRegistry(), lazyaddons, plugins, tools, yara


def test_tool_rows_use_json_and_active_key(tmp_path, monkeypatch):
    """``.tool`` rows parse JSON and toggle the ``active`` key in JSON."""
    registry, _lazy, _plugins, tools, _yara = _registry(tmp_path, monkeypatch)
    path = tools / "demo.tool"
    path.write_text(
        json.dumps(
            {
                "toolname": "demo",
                "command": "echo {ip}",
                "trigger": ["http"],
                "active": True,
                "description": "demo tool",
            }
        ),
        encoding="utf-8",
    )
    row = registry.scan("tools")[0]
    assert row.name == "demo"
    assert row.state_key == "active"
    assert row.data_format == "json"
    assert row.toggleable is True
    assert row.toggle_enabled() is True
    assert row.enabled is False
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["active"] is False
    assert data["toolname"] == "demo"


def test_plugin_rows_skip_lua_and_templates(tmp_path, monkeypatch):
    """Only YAML metadata is listed; Lua code and templates are hidden."""
    registry, _lazy, plugins, _tools, _yara = _registry(tmp_path, monkeypatch)
    (plugins / "real.yaml").write_text(
        yaml.safe_dump({"name": "real", "enabled": True, "description": "plugin"}), encoding="utf-8"
    )
    (plugins / "real.lua").write_text("function real() end", encoding="utf-8")
    (plugins / "tiers.yaml").write_text("tiers: {}", encoding="utf-8")
    (plugins / "01 - template_plugins_yaml.yaml").write_text("name: template", encoding="utf-8")
    rows = registry.scan("plugins")
    assert [row.name for row in rows] == ["real"]
    assert rows[0].toggle_enabled() is True
    assert yaml.safe_load((plugins / "real.yaml").read_text(encoding="utf-8"))["enabled"] is False


def test_read_only_tabs_never_toggle_or_delete(tmp_path, monkeypatch):
    """YARA and Nuclei rows are preview-only."""
    registry, _lazy, _plugins, _tools, yara = _registry(tmp_path, monkeypatch)
    rule = yara / "rule.yar"
    rule.write_text('rule demo { meta: description = "demo" condition: true }', encoding="utf-8")
    row = registry.scan("yara")[0]
    assert row.toggleable is False
    assert row.toggle_enabled() is False
    assert registry.delete_addon(row) is False
    assert rule.exists()
    assert registry.tab_is_read_only("nuclei") is True


def test_create_and_delete_across_tabs(tmp_path, monkeypatch):
    """Templates are valid per format and deletion is confined."""
    registry, lazyaddons, plugins, tools, _yara = _registry(tmp_path, monkeypatch)
    addon = registry.create_addon("lazyaddons", "My Addon")
    plugin = registry.create_addon("plugins", "my_plugin")
    tool = registry.create_addon("tools", "my_tool")
    assert addon and addon.exists()
    assert plugin and yaml.safe_load(plugin.read_text(encoding="utf-8"))["name"] == "my_plugin"
    assert tool and json.loads(tool.read_text(encoding="utf-8"))["toolname"] == "my_tool"
    assert registry.create_addon("yara", "nope") is None

    assert registry.delete_addon(registry.scan("tools")[0]) is True
    assert not (tools / "my_tool.tool").exists()
    assert (lazyaddons / "My_Addon.yaml").exists() or (lazyaddons / "MyAddon.yaml").exists()


def test_settings_toggle_tracks_only_success(tmp_path, monkeypatch):
    """The in-memory state mirrors successful on-disk toggles."""
    registry, _lazy, _plugins, _tools, yara = _registry(tmp_path, monkeypatch)
    tool = _tools / "x.tool"
    tool.write_text(json.dumps({"toolname": "x", "active": True}), encoding="utf-8")
    (yara / "x.yar").write_text("rule x { condition: true }", encoding="utf-8")
    settings = mp.MarketplaceSettings()
    tool_row = registry.scan("tools")[0]
    assert settings.toggle(tool_row) is True
    assert settings.is_enabled("tools", "x") is False
    assert settings.toggle(registry.scan("yara")[0]) is False


def test_marketplace_app_filters_rows(tmp_path, monkeypatch):
    """The Textual app exposes a filtered table per tab."""
    import asyncio

    registry, _lazy, _plugins, _tools, yara = _registry(tmp_path, monkeypatch)
    tool = _tools / "alpha.tool"
    tool.write_text(json.dumps({"toolname": "alpha", "active": True, "description": "one"}), encoding="utf-8")
    beta = _tools / "beta.tool"
    beta.write_text(json.dumps({"toolname": "beta", "active": True, "description": "two"}), encoding="utf-8")

    async def _drive():
        app = mp.MarketplaceConfigApp(mp.MarketplaceConfig(), registry, mp._build_initial_settings(registry))
        async with app.run_test() as pilot:
            await pilot.pause(0.3)
            app.query_one("#market-tabs").active = "market-tab-tools"
            await pilot.pause(0.2)
            before = app.query_one("#market-tools").row_count
            app.query_one("#market-filter").value = "alpha"
            await pilot.pause(0.2)
            after = app.query_one("#market-tools").row_count
        return before, after

    before, after = asyncio.run(_drive())
    assert before == 2
    assert after == 1


def test_filter_input_keeps_printable_keys(tmp_path, monkeypatch):
    """App bindings do not steal letters typed into the filter box."""
    import asyncio

    registry, _lazy, _plugins, _tools, _yara = _registry(tmp_path, monkeypatch)

    async def _drive():
        app = mp.MarketplaceConfigApp(mp.MarketplaceConfig(), registry, mp._build_initial_settings(registry))
        async with app.run_test() as pilot:
            await pilot.pause(0.2)
            await pilot.press("a", "d", "m")
            await pilot.pause(0.1)
            return app.query_one("#market-filter").value
        return ""

    assert asyncio.run(_drive()) == "adm"
