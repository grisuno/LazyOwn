"""Tests for modules/sleep_obfuscation.py — SleepTechnique, SleepObfuscationConfig,
SleepTechniqueCatalog, SleepObfuscationEngine, SleepTechniqueValidator.

Covers:
    - SleepTechnique dataclass construction and immutability
    - SleepObfuscationConfig serialization roundtrip
    - SleepTechniqueCatalog registration, retrieval, listing
    - SleepTechniqueCatalog platform filtering
    - SleepObfuscationEngine select/configure/validate/recommend
    - SleepObfuscationEngine detection_resistance computation
    - SleepObfuscationEngine serialization roundtrip
    - SleepTechniqueValidator edge cases
    - Default catalog composition
    - OsPlatform and TechniqueRisk enum values
"""

from __future__ import annotations

import pytest

from modules.sleep_obfuscation import (
    OsPlatform,
    SleepObfuscationConfig,
    SleepObfuscationEngine,
    SleepTechnique,
    SleepTechniqueCatalog,
    SleepTechniqueValidator,
    TechniqueRisk,
    _build_default_catalog,
)


class TestSleepTechnique:
    def test_construction_and_properties(self):
        tech = SleepTechnique(
            name="test_tech",
            description="A test technique",
            platforms=[OsPlatform.WINDOWS, OsPlatform.LINUX],
            detection_resistance=75,
            risk=TechniqueRisk.LOW,
            params={"key": {"type": "int", "default": 1, "description": "test"}},
        )
        assert tech.name == "test_tech"
        assert tech.detection_resistance == 75
        assert tech.risk == TechniqueRisk.LOW
        assert OsPlatform.WINDOWS in tech.platforms

    def test_defaults(self):
        tech = SleepTechnique(
            name="defaults",
            description="Testing defaults",
            platforms=[OsPlatform.WINDOWS],
            detection_resistance=50,
        )
        assert tech.risk == TechniqueRisk.MEDIUM
        assert tech.min_beacon_version == "1.0"
        assert tech.requires_rop_gadgets is False
        assert tech.params == {}

    def test_immutability(self):
        tech = SleepTechnique(
            name="frozen",
            description="immutable test",
            platforms=[OsPlatform.WINDOWS],
            detection_resistance=50,
        )
        with pytest.raises(Exception):
            tech.name = "changed"


class TestSleepObfuscationConfig:
    def test_default_construction(self):
        config = SleepObfuscationConfig()
        assert config.technique_name == "sleep_mask"
        assert config.enabled is False
        assert config.encrypt_heap is True
        assert config.rwx_to_rw_cycle is True

    def test_serialization_roundtrip(self):
        original = SleepObfuscationConfig(
            technique_name="ekko",
            enabled=True,
            encrypt_heap=False,
            encrypt_stack=False,
            encrypt_peb=True,
            indirect_syscalls=False,
            module_stomp_target="ntdll.dll",
            rop_gadget_count=5,
            custom_params={"mode": "aggressive"},
        )
        restored = SleepObfuscationConfig.from_dict(original.to_dict())
        assert restored.technique_name == original.technique_name
        assert restored.enabled == original.enabled
        assert restored.encrypt_heap == original.encrypt_heap
        assert restored.encrypt_stack == original.encrypt_stack
        assert restored.encrypt_peb == original.encrypt_peb
        assert restored.indirect_syscalls == original.indirect_syscalls
        assert restored.module_stomp_target == original.module_stomp_target
        assert restored.rop_gadget_count == original.rop_gadget_count
        assert restored.custom_params == original.custom_params

    def test_from_dict_empty(self):
        config = SleepObfuscationConfig.from_dict({})
        assert config.technique_name == "sleep_mask"
        assert config.enabled is False

    def test_from_dict_partial(self):
        config = SleepObfuscationConfig.from_dict({"enabled": True, "technique_name": "ekko"})
        assert config.enabled is True
        assert config.technique_name == "ekko"
        assert config.encrypt_heap is True


class TestSleepTechniqueCatalog:
    def test_default_catalog_has_techniques(self):
        catalog = _build_default_catalog()
        techniques = catalog.list_all()
        assert len(techniques) >= 8

    def test_register_and_get(self):
        catalog = SleepTechniqueCatalog()
        tech = SleepTechnique(
            name="custom",
            description="Custom technique",
            platforms=[OsPlatform.WINDOWS],
            detection_resistance=90,
        )
        catalog.register(tech)
        assert catalog.get("custom").name == "custom"

    def test_get_missing_raises_keyerror(self):
        catalog = SleepTechniqueCatalog()
        with pytest.raises(KeyError, match="ghost"):
            catalog.get("ghost")

    def test_list_all_sorted_by_resistance(self):
        catalog = _build_default_catalog()
        techniques = catalog.list_all()
        scores = [t.detection_resistance for t in techniques]
        assert scores == sorted(scores, reverse=True)

    def test_list_by_platform_windows(self):
        catalog = _build_default_catalog()
        windows = catalog.list_by_platform(OsPlatform.WINDOWS)
        assert len(windows) >= 6
        for tech in windows:
            assert OsPlatform.WINDOWS in tech.platforms or len(tech.platforms) >= 1

    def test_list_by_platform_linux(self):
        catalog = _build_default_catalog()
        linux = catalog.list_by_platform(OsPlatform.LINUX)
        assert len(linux) >= 2
        for tech in linux:
            assert OsPlatform.LINUX in tech.platforms

    def test_list_names(self):
        catalog = _build_default_catalog()
        names = catalog.list_names()
        assert "sleep_mask" in names
        assert "ekko" in names
        assert names == sorted(names)


class TestSleepTechniqueValidator:
    def test_valid_config_passes(self):
        catalog = _build_default_catalog()
        tech = catalog.get("sleep_mask")
        config = SleepObfuscationConfig(technique_name="sleep_mask")
        validator = SleepTechniqueValidator()
        errors = validator.validate(config, tech)
        assert errors == []

    def test_ekko_requires_rop_gadgets(self):
        catalog = _build_default_catalog()
        tech = catalog.get("ekko")
        config = SleepObfuscationConfig(technique_name="ekko", rop_gadget_count=0)
        validator = SleepTechniqueValidator()
        errors = validator.validate(config, tech)
        assert any("rop_gadget_count" in e.lower() for e in errors)

    def test_excessive_rop_gadget_count(self):
        catalog = _build_default_catalog()
        tech = catalog.get("ekko")
        config = SleepObfuscationConfig(technique_name="ekko", rop_gadget_count=100)
        validator = SleepTechniqueValidator()
        errors = validator.validate(config, tech)
        assert len(errors) >= 1

    def test_negative_sleep_delay(self):
        catalog = _build_default_catalog()
        tech = catalog.get("sleep_mask")
        config = SleepObfuscationConfig(technique_name="sleep_mask", sleep_delay_ms=-10)
        validator = SleepTechniqueValidator()
        errors = validator.validate(config, tech)
        assert any("sleep_delay_ms" in e.lower() for e in errors)

    def test_excessive_sleep_delay(self):
        catalog = _build_default_catalog()
        tech = catalog.get("sleep_mask")
        config = SleepObfuscationConfig(technique_name="sleep_mask", sleep_delay_ms=99999)
        validator = SleepTechniqueValidator()
        errors = validator.validate(config, tech)
        assert any("sleep_delay_ms" in e.lower() for e in errors)

    def test_validate_config_enabled_without_name(self):
        validator = SleepTechniqueValidator()
        config = SleepObfuscationConfig(technique_name="", enabled=True)
        errors = validator.validate_config(config)
        assert any("technique_name" in e.lower() for e in errors)


class TestSleepObfuscationEngine:
    def test_default_engine(self):
        engine = SleepObfuscationEngine()
        assert engine.detection_resistance == 65
        assert engine.config.enabled is False
        assert engine.config.technique_name == "sleep_mask"

    def test_select_existing_technique(self):
        engine = SleepObfuscationEngine()
        tech = engine.select("ekko")
        assert tech.name == "ekko"
        assert tech.detection_resistance == 85

    def test_select_missing_technique(self):
        engine = SleepObfuscationEngine()
        with pytest.raises(KeyError, match="ghost_tech"):
            engine.select("ghost_tech")

    def test_configure_updates_config(self):
        engine = SleepObfuscationEngine()
        tech = engine.select("sleep_mask")
        config = engine.configure(tech, {"encrypt_heap": False, "indirect_syscalls": False})
        assert config.technique_name == "sleep_mask"
        assert config.enabled is True
        assert config.encrypt_heap is False
        assert config.indirect_syscalls is False

    def test_configure_without_overrides(self):
        engine = SleepObfuscationEngine()
        tech = engine.select("ekko")
        config = engine.configure(tech)
        assert config.technique_name == "ekko"
        assert config.enabled is True

    def test_validate_valid_config(self):
        engine = SleepObfuscationEngine()
        errors = engine.validate()
        assert errors == []

    def test_validate_unknown_technique(self):
        engine = SleepObfuscationEngine()
        engine._config = SleepObfuscationConfig(technique_name="ghost")
        errors = engine.validate()
        assert len(errors) >= 1

    def test_recommend_windows(self):
        engine = SleepObfuscationEngine()
        recs = engine.recommend(OsPlatform.WINDOWS)
        assert len(recs) >= 6
        assert recs[0].detection_resistance >= recs[-1].detection_resistance

    def test_recommend_linux(self):
        engine = SleepObfuscationEngine()
        recs = engine.recommend(OsPlatform.LINUX)
        assert len(recs) >= 2
        for tech in recs:
            assert OsPlatform.LINUX in tech.platforms

    def test_to_dict(self):
        engine = SleepObfuscationEngine()
        d = engine.to_dict()
        assert "config" in d
        assert "available_techniques" in d
        assert "active_detection_resistance" in d
        assert d["active_detection_resistance"] == 65

    def test_from_dict_roundtrip(self):
        engine = SleepObfuscationEngine()
        tech = engine.select("ekko")
        engine.configure(tech, {"encrypt_heap": False})
        d = engine.to_dict()
        restored = SleepObfuscationEngine.from_dict(d)
        assert restored.config.technique_name == "ekko"
        assert restored.config.encrypt_heap is False
        assert restored.detection_resistance == 85

    def test_from_dict_empty(self):
        engine = SleepObfuscationEngine.from_dict({})
        assert engine.config.technique_name == "sleep_mask"
        assert engine.config.enabled is False

    def test_custom_catalog(self):
        custom_catalog = SleepTechniqueCatalog()
        tech = SleepTechnique(
            name="only_tech",
            description="Only technique",
            platforms=[OsPlatform.WINDOWS],
            detection_resistance=99,
        )
        custom_catalog.register(tech)
        engine = SleepObfuscationEngine(catalog=custom_catalog)
        assert engine.detection_resistance == 99
        assert engine.catalog.list_names() == ["only_tech"]


class TestBedEnumValues:
    def test_os_platform_values(self):
        assert OsPlatform.WINDOWS.value == "windows"
        assert OsPlatform.LINUX.value == "linux"

    def test_technique_risk_values(self):
        assert TechniqueRisk.LOW.value == "low"
        assert TechniqueRisk.MEDIUM.value == "medium"
        assert TechniqueRisk.HIGH.value == "high"
