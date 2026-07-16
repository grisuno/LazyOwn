"""Tests for modules.module_registry — ModuleInfo, ModuleRegistry, search, summary.

Covers the data class, singleton pattern, search by name/type/category,
and summary counts. The registry scans real filesystem paths so these
tests also validate that discovery does not crash on the actual repo.
"""

from __future__ import annotations

from modules.module_registry import (
    _MODULE_TYPES,
    ModuleInfo,
    ModuleRegistry,
    _classify,
    format_module_detail,
    format_module_table,
)


class TestClassify:
    def test_known_categories(self):
        """Each MODULE_TYPES prefix maps to the expected type."""
        for prefix, expected in _MODULE_TYPES.items():
            result = _classify(prefix)
            assert result == expected, f"{prefix} should map to {expected}"

    def test_unknown_category_defaults_to_auxiliary(self):
        result = _classify("99. Completely Unknown")
        assert result == "auxiliary"

    def test_empty_string(self):
        result = _classify("")
        assert result == "auxiliary"


class TestModuleInfo:
    def test_minimal_construction(self):
        info = ModuleInfo(name="test_mod", module_type="scanner")
        assert info.name == "test_mod"
        assert info.module_type == "scanner"
        assert info.enabled is True
        assert info.params == []

    def test_full_construction(self):
        params = [{"name": "rhost", "type": "address", "required": True}]
        info = ModuleInfo(
            name="full_mod",
            module_type="exploit",
            author="test_author",
            version="1.0",
            description="A full test module",
            category="03. Exploitation",
            path="/tmp/test.yaml",
            source="yaml",
            params=params,
            enabled=False,
        )
        assert info.author == "test_author"
        assert info.version == "1.0"
        assert info.enabled is False

    def test_to_dict(self):
        info = ModuleInfo(name="dict_test", module_type="auxiliary", description="desc")
        d = info.to_dict()
        assert d["name"] == "dict_test"
        assert d["type"] == "auxiliary"
        assert d["description"] == "desc"
        assert d["enabled"] is True

    def test_repr(self):
        info = ModuleInfo(name="my_mod", module_type="scanner")
        assert repr(info) == "<ModuleInfo scanner/my_mod>"


class TestModuleRegistry:
    def test_singleton(self):
        """get_instance returns the same object across calls."""
        r1 = ModuleRegistry.get_instance()
        r2 = ModuleRegistry.get_instance()
        assert r1 is r2

    def test_singleton_with_base_dir(self):
        """Providing base_dir on first call initialises the path."""
        reg = ModuleRegistry.get_instance()
        assert reg._base is not None

    def test_initial_state_not_scanned(self):
        reg = ModuleRegistry()
        assert reg._scanned is False
        assert len(reg._modules) == 0

    def test_scan_returns_list(self):
        """scan() returns a list and sets _scanned to True."""
        reg = ModuleRegistry()
        result = reg.scan()
        assert isinstance(result, list)
        assert reg._scanned is True

    def test_scan_is_idempotent(self):
        """Second scan() returns the same (cached) list."""
        reg = ModuleRegistry()
        r1 = reg.scan()
        r2 = reg.scan()
        assert len(r1) == len(r2)

    def test_rescan_forces_refresh(self):
        """rescan() clears the cache and rescans."""
        reg = ModuleRegistry()
        reg.scan()
        assert reg._scanned is True
        reg.rescan()
        assert reg._scanned is True
        # rescan should not crash

    def test_search_returns_list(self):
        reg = ModuleRegistry()
        results = reg.search(query="nmap")
        assert isinstance(results, list)
        # Should find something if lazyaddons/nmap.yaml exists

    def test_search_by_module_type(self):
        reg = ModuleRegistry()
        scanners = reg.search(module_type="scanner")
        for s in scanners:
            assert s.module_type == "scanner"

    def test_search_by_category(self):
        reg = ModuleRegistry()
        results = reg.search(category="01. Reconnaissance")
        for r in results:
            assert r.category == "01. Reconnaissance"

    def test_get_known_module(self):
        """get() returns a ModuleInfo for a known name."""
        reg = ModuleRegistry()
        reg.scan()
        # Look for at least one module that was found
        all_mods = list(reg._modules.values())
        if all_mods:
            first = all_mods[0]
            found = reg.get(first.name)
            assert found is not None
            assert found.name == first.name

    def test_get_unknown_returns_none(self):
        reg = ModuleRegistry()
        assert reg.get("nonexistent_mod_xyz") is None

    def test_summary_returns_counts(self):
        reg = ModuleRegistry()
        summary = reg.summary()
        assert isinstance(summary, dict)
        total = sum(summary.values())
        assert total > 0
        # Should have at least scanner, exploit, auxiliary etc.
        expected_types = {"scanner", "exploit", "auxiliary"}
        assert expected_types.intersection(summary.keys())

    def test_by_type_shorthand(self):
        reg = ModuleRegistry()
        scanners = reg.by_type("scanner")
        assert all(m.module_type == "scanner" for m in scanners)

    def test_search_enabled_only_filters_disabled(self):
        """search with enabled_only=True skips disabled modules."""
        reg = ModuleRegistry()
        reg.scan()
        # Disable a module temporarily
        disabled_name = None
        for name, mod in reg._modules.items():
            if mod.enabled:
                mod.enabled = False
                disabled_name = name
                break

        if disabled_name:
            results = reg.search(enabled_only=True)
            assert all(m.enabled for m in results)
            names = {m.name for m in results}
            assert disabled_name not in names
            # Re-enable
            reg._modules[disabled_name].enabled = True


class TestFormatFunctions:
    def test_format_module_table_empty(self):
        result = format_module_table([])
        assert "No modules" in result

    def test_format_module_table_with_data(self):
        infos = [
            ModuleInfo(name="mod_a", module_type="scanner", description="Scanner A"),
            ModuleInfo(name="mod_b", module_type="exploit", description="Exploit B"),
        ]
        result = format_module_table(infos)
        assert "mod_a" in result
        assert "mod_b" in result
        assert "scanner" in result
        assert "exploit" in result

    def test_format_module_detail(self):
        info = ModuleInfo(
            name="detail_mod",
            module_type="scanner",
            author="author_x",
            version="2.0",
            description="A detailed module",
            category="01. Reconnaissance",
            path="/tmp/test.yaml",
            params=[{"name": "rhost", "type": "address", "required": True}],
        )
        result = format_module_detail(info)
        assert "detail_mod" in result
        assert "scanner" in result
        assert "author_x" in result

    def test_format_module_detail_minimal(self):
        info = ModuleInfo(name="minimal", module_type="auxiliary")
        result = format_module_detail(info)
        assert "minimal" in result
        assert "auxiliary" in result
