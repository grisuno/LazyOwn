"""Tests for modules/bof_registry.py — BofEntry, BofCatalog, BofRegistry,
BofMarketplace, BofValidator, BofPlatform, BofCategory.

Covers:
    - BofEntry construction, immutability, and serialization
    - BofCatalog registration, search, list operations
    - BofCatalog persistence (save/load roundtrip)
    - BofRegistry install, uninstall, manifest management
    - BofMarketplace search with install status enrichment
    - BofMarketplace install/uninstall/info/list operations
    - BofMarketplace bulk_install and dependency checking
    - BofValidator hash verification and argument validation
    - BofPlatform and BofCategory enum values
    - Edge cases: missing BOFs, already installed, empty queries
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from modules.bof_registry import (
    BofCatalog,
    BofCategory,
    BofEntry,
    BofMarketplace,
    BofPlatform,
    BofRegistry,
    BofValidator,
    _build_default_catalog,
)


@pytest.fixture
def catalog():
    return _build_default_catalog()


@pytest.fixture
def tmp_sessions():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


class TestBofEntry:
    def test_construction_and_properties(self):
        entry = BofEntry(
            name="test_bof",
            description="A test BOF",
            author="TestAuthor",
            url="https://github.com/test/repo",
            source_file="src/test.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.ENUM,
            required_args=["target"],
            optional_args=["timeout"],
            mitre_technique="T1018",
        )
        assert entry.name == "test_bof"
        assert entry.platform == BofPlatform.WINDOWS
        assert "target" in entry.required_args

    def test_immutability(self):
        entry = BofEntry(name="immutable", description="test", author="x", url="x", source_file="x")
        with pytest.raises(Exception):
            entry.name = "changed"

    def test_to_dict_roundtrip(self):
        original = BofEntry(
            name="roundtrip",
            description="Test serialization",
            author="QA",
            url="https://example.com",
            source_file="bofs/test.c",
            platform=BofPlatform.LINUX,
            category=BofCategory.PERSIST,
            required_args=["arg1", "arg2"],
            mitre_technique="T1053",
            sha256="a" * 64,
        )
        restored = BofEntry.from_dict(original.to_dict())
        assert restored.name == original.name
        assert restored.description == original.description
        assert restored.platform == original.platform
        assert restored.category == original.category
        assert restored.required_args == original.required_args
        assert restored.sha256 == original.sha256

    def test_from_dict_minimal(self):
        entry = BofEntry.from_dict({"name": "minimal"})
        assert entry.name == "minimal"
        assert entry.platform == BofPlatform.WINDOWS
        assert entry.category == BofCategory.GENERAL
        assert entry.required_args == []
        assert entry.optional_args == []
        assert entry.mitre_technique == ""


class TestBofCatalog:
    def test_register_and_get(self, catalog):
        entry = catalog.get("ldap_enum")
        assert entry.name == "ldap_enum"
        assert entry.category == BofCategory.ENUM

    def test_get_missing_raises_keyerror(self, catalog):
        with pytest.raises(KeyError, match="nonexistent_bof"):
            catalog.get("nonexistent_bof")

    def test_search_exact_match(self, catalog):
        results = catalog.search("ldap_enum")
        assert len(results) >= 1
        assert results[0].name == "ldap_enum"

    def test_search_by_category(self, catalog):
        results = catalog.search("credential_access")
        assert len(results) >= 2  # lsass_dump, sam_dump
        assert all(e.category == BofCategory.CRED for e in results)

    def test_search_by_technique(self, catalog):
        results = catalog.search("T1003")
        assert len(results) >= 2
        for entry in results:
            assert entry.mitre_technique == "T1003"

    def test_search_empty_query_returns_all(self, catalog):
        results = catalog.search("")
        assert len(results) == len(catalog.entries)

    def test_list_all_sorted(self, catalog):
        entries = catalog.list_all()
        names = [e.name for e in entries]
        assert names == sorted(names)

    def test_list_by_platform(self, catalog):
        windows = catalog.list_by_platform(BofPlatform.WINDOWS)
        for entry in windows:
            assert entry.platform == BofPlatform.WINDOWS

    def test_list_by_category(self, catalog):
        persist = catalog.list_by_category(BofCategory.PERSIST)
        assert len(persist) >= 3
        for entry in persist:
            assert entry.category == BofCategory.PERSIST

    def test_save_load_roundtrip(self, catalog, tmp_sessions):
        path = tmp_sessions / "bof_catalog_test.json"
        catalog.save(path)
        loaded = BofCatalog.load(path)
        assert set(loaded.entries.keys()) == set(catalog.entries.keys())

    def test_load_missing_file_returns_empty(self, tmp_sessions):
        path = tmp_sessions / "nonexistent.json"
        loaded = BofCatalog.load(path)
        assert len(loaded.entries) == 0

    def test_empty_catalog(self):
        catalog = BofCatalog()
        assert catalog.list_all() == []
        assert catalog.search("anything") == []
        with pytest.raises(KeyError):
            catalog.get("anything")

    def test_register_overwrites(self):
        catalog = BofCatalog()
        entry1 = BofEntry(name="dup", description="first", author="x", url="x", source_file="x")
        entry2 = BofEntry(name="dup", description="second", author="y", url="y", source_file="y")
        catalog.register(entry1)
        catalog.register(entry2)
        assert catalog.get("dup").description == "second"


class TestBofRegistry:
    def test_install_and_check(self, tmp_sessions):
        registry = BofRegistry(tmp_sessions)
        entry = BofEntry(name="test_install", description="test", author="x", url="x", source_file="x")
        path = registry.install(entry)
        assert registry.is_installed("test_install") is True
        assert path.exists()

    def test_uninstall(self, tmp_sessions):
        registry = BofRegistry(tmp_sessions)
        entry = BofEntry(name="test_uninstall", description="test", author="x", url="x", source_file="x")
        registry.install(entry)
        assert registry.uninstall("test_uninstall") is True
        assert registry.is_installed("test_uninstall") is False

    def test_uninstall_nonexistent(self, tmp_sessions):
        registry = BofRegistry(tmp_sessions)
        assert registry.uninstall("ghost") is False

    def test_list_installed(self, tmp_sessions):
        registry = BofRegistry(tmp_sessions)
        entry = BofEntry(name="a_bof", description="test", author="x", url="x", source_file="x")
        registry.install(entry)
        installed = registry.list_installed()
        assert len(installed) == 1
        assert installed[0]["name"] == "a_bof"

    def test_get_install_info(self, tmp_sessions):
        registry = BofRegistry(tmp_sessions)
        entry = BofEntry(name="info_test", description="test", author="x", url="x", source_file="x")
        registry.install(entry)
        info = registry.get_install_info("info_test")
        assert info is not None
        assert info["name"] == "info_test"

    def test_get_install_info_nonexistent(self, tmp_sessions):
        registry = BofRegistry(tmp_sessions)
        assert registry.get_install_info("ghost") is None

    def test_manifest_persistence(self, tmp_sessions):
        registry = BofRegistry(tmp_sessions)
        entry = BofEntry(name="persistent", description="test", author="x", url="x", source_file="x")
        registry.install(entry)
        registry2 = BofRegistry(tmp_sessions)
        assert registry2.is_installed("persistent") is True


class TestBofValidator:
    def test_verify_with_empty_hash_skips(self, tmp_sessions):
        entry = BofEntry(name="no_hash", description="test", author="x", url="x", source_file="x")
        test_file = tmp_sessions / "dummy.c"
        test_file.write_text("int main() { return 0; }")
        ok, reason = BofValidator.verify_entry(entry, test_file)
        assert ok is True
        assert "unaudited" in reason

    def test_compute_sha256_deterministic(self, tmp_sessions):
        test_file = tmp_sessions / "dummy2.c"
        test_file.write_text("hello world")
        h1 = BofValidator.compute_sha256(test_file)
        h2 = BofValidator.compute_sha256(test_file)
        assert h1 == h2
        assert len(h1) == 64

    def test_verify_mismatched_hash(self, tmp_sessions):
        test_file = tmp_sessions / "dummy3.c"
        test_file.write_text("some data")
        entry = BofEntry(
            name="mismatch",
            description="test",
            author="x",
            url="x",
            source_file="x",
            sha256="0" * 64,
        )
        ok, reason = BofValidator.verify_entry(entry, test_file)
        assert ok is False
        assert "mismatch" in reason.lower()

    def test_validate_args_missing_required(self):
        entry = BofEntry(
            name="needs_args",
            description="test",
            author="x",
            url="x",
            source_file="x",
            required_args=["domain", "filter"],
        )
        missing = BofValidator.validate_args(entry, {"domain": "CORP"})
        assert "filter" in missing
        assert "domain" not in missing

    def test_validate_args_all_present(self):
        entry = BofEntry(
            name="has_args",
            description="test",
            author="x",
            url="x",
            source_file="x",
            required_args=["target", "port"],
        )
        missing = BofValidator.validate_args(entry, {"target": "10.0.0.1", "port": "445"})
        assert missing == []

    def test_validate_args_no_required(self):
        entry = BofEntry(
            name="no_args",
            description="test",
            author="x",
            url="x",
            source_file="x",
            required_args=[],
        )
        missing = BofValidator.validate_args(entry, {})
        assert missing == []


class TestBofMarketplace:
    def test_search_enriches_with_install_status(self, tmp_sessions):
        mp = BofMarketplace(tmp_sessions)
        results = mp.search("ldap_enum")
        assert len(results) >= 1
        assert "installed" in results[0]
        assert results[0]["installed"] is False

    def test_info_returns_catalog_and_install_state(self, tmp_sessions):
        mp = BofMarketplace(tmp_sessions)
        info = mp.info("ldap_enum")
        assert "catalog" in info
        assert "installed" in info
        assert info["installed"] is False

    def test_info_missing_bof(self):
        mp = BofMarketplace()
        info = mp.info("nonexistent_bof_xyz")
        assert "error" in info

    def test_install_and_uninstall(self, tmp_sessions):
        mp = BofMarketplace(tmp_sessions)
        result = mp.install("ldap_enum")
        assert result["status"] == "installed"
        assert "install_path" in result
        installed_list = mp.list_installed()
        assert any(i["name"] == "ldap_enum" for i in installed_list)
        uninstall_result = mp.uninstall("ldap_enum")
        assert uninstall_result["status"] == "uninstalled"

    def test_install_already_installed(self, tmp_sessions):
        mp = BofMarketplace(tmp_sessions)
        mp.install("ldap_enum")
        result = mp.install("ldap_enum")
        assert result["status"] == "already_installed"

    def test_install_missing_bof(self):
        mp = BofMarketplace()
        result = mp.install("nonexistent_bof_xyz")
        assert "error" in result

    def test_uninstall_missing_bof(self, tmp_sessions):
        mp = BofMarketplace(tmp_sessions)
        result = mp.uninstall("ghost_bof")
        assert "error" in result

    def test_list_installed_empty_initially(self, tmp_sessions):
        mp = BofMarketplace(tmp_sessions)
        installed = mp.list_installed()
        assert installed == []

    def test_list_missing_dependencies(self, tmp_sessions):
        mp = BofMarketplace(tmp_sessions)
        missing = mp.list_missing_dependencies("ldap_enum")
        assert isinstance(missing, list)

    def test_list_missing_dependencies_unknown_bof(self):
        mp = BofMarketplace()
        missing = mp.list_missing_dependencies("ghost")
        assert missing == []

    def test_bulk_install(self, tmp_sessions):
        mp = BofMarketplace(tmp_sessions)
        results = mp.bulk_install(["ldap_enum", "whoami", "netstat"])
        assert len(results) == 3
        assert all(r["status"] in ("installed", "already_installed") for r in results.values())


class TestBofEnums:
    def test_platform_values(self):
        assert BofPlatform.WINDOWS.value == "windows"
        assert BofPlatform.LINUX.value == "linux"

    def test_category_values(self):
        assert BofCategory.RECON.value == "reconnaissance"
        assert BofCategory.CRED.value == "credential_access"
        assert BofCategory.GENERAL.value == "general"
