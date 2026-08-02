"""Tests for modules/categories.py — category constants and look-up tables."""

from __future__ import annotations

from modules.categories import (
    ALL_CATEGORIES,
    CATEGORY_TO_SHORT,
    SHORT_TO_CATEGORY,
    ai_category,
    cloud_attack_category,
    command_and_control_category,
    container_k8s_category,
    credential_access_category,
    exfiltration_category,
    exploitation_category,
    lateral_movement_category,
    lua_plugin_category,
    miscellaneous_category,
    persistence_category,
    post_exploitation_category,
    privilege_escalation_category,
    recon_category,
    reporting_category,
    scanning_category,
)


class TestCategoryConstants:
    def test_all_recon_values(self) -> None:
        assert recon_category == "01. Reconnaissance"

    def test_all_scanning_values(self) -> None:
        assert scanning_category == "02. Scanning & Enumeration"

    def test_all_exploitation_values(self) -> None:
        assert exploitation_category == "03. Exploitation"

    def test_all_post_exploitation_values(self) -> None:
        assert post_exploitation_category == "04. Post-Exploitation"

    def test_all_persistence_values(self) -> None:
        assert persistence_category == "05. Persistence"

    def test_all_privesc_values(self) -> None:
        assert privilege_escalation_category == "06. Privilege Escalation"

    def test_all_cred_access_values(self) -> None:
        assert credential_access_category == "07. Credential Access"

    def test_all_lateral_values(self) -> None:
        assert lateral_movement_category == "08. Lateral Movement"

    def test_all_exfil_values(self) -> None:
        assert exfiltration_category == "09. Data Exfiltration"

    def test_all_c2_values(self) -> None:
        assert command_and_control_category == "10. Command & Control"

    def test_all_reporting_values(self) -> None:
        assert reporting_category == "11. Reporting"

    def test_all_misc_values(self) -> None:
        assert miscellaneous_category == "12. Miscellaneous"

    def test_all_lua_values(self) -> None:
        assert lua_plugin_category == "13. Lua Plugin"

    def test_all_ai_values(self) -> None:
        assert ai_category == "16. Artificial Intelligence"

    def test_all_cloud_values(self) -> None:
        assert cloud_attack_category == "17. Cloud Attacks"

    def test_all_container_values(self) -> None:
        assert container_k8s_category == "18. Container & Kubernetes"


class TestShortToCategory:
    def test_recon_to_category(self) -> None:
        assert SHORT_TO_CATEGORY["recon"] == recon_category

    def test_scanning_to_category(self) -> None:
        assert SHORT_TO_CATEGORY["scanning"] == scanning_category

    def test_enum_to_scanning_category(self) -> None:
        assert SHORT_TO_CATEGORY["enum"] == scanning_category

    def test_exploit_to_category(self) -> None:
        assert SHORT_TO_CATEGORY["exploit"] == exploitation_category

    def test_post_to_category(self) -> None:
        assert SHORT_TO_CATEGORY["post"] == post_exploitation_category

    def test_persistence_to_category(self) -> None:
        assert SHORT_TO_CATEGORY["persistence"] == persistence_category

    def test_privesc_to_category(self) -> None:
        assert SHORT_TO_CATEGORY["privesc"] == privilege_escalation_category

    def test_credential_to_category(self) -> None:
        assert SHORT_TO_CATEGORY["credential"] == credential_access_category

    def test_lateral_to_category(self) -> None:
        assert SHORT_TO_CATEGORY["lateral"] == lateral_movement_category

    def test_exfil_to_category(self) -> None:
        assert SHORT_TO_CATEGORY["exfil"] == exfiltration_category

    def test_c2_to_category(self) -> None:
        assert SHORT_TO_CATEGORY["c2"] == command_and_control_category

    def test_reporting_to_category(self) -> None:
        assert SHORT_TO_CATEGORY["reporting"] == reporting_category

    def test_misc_to_category(self) -> None:
        assert SHORT_TO_CATEGORY["misc"] == miscellaneous_category

    def test_ai_to_category(self) -> None:
        assert SHORT_TO_CATEGORY["ai"] == ai_category

    def test_unknown_short_name_raises_key_error(self) -> None:
        import pytest
        with pytest.raises(KeyError):
            _ = SHORT_TO_CATEGORY["nonexistent_phase"]


class TestCategoryToShort:
    def test_recon_reverse_lookup(self) -> None:
        assert CATEGORY_TO_SHORT[recon_category] == "recon"

    def test_exploitation_reverse_lookup(self) -> None:
        assert CATEGORY_TO_SHORT[exploitation_category] == "exploit"

    def test_privesc_reverse_lookup(self) -> None:
        assert CATEGORY_TO_SHORT[privilege_escalation_category] == "privesc"

    def test_c2_reverse_lookup(self) -> None:
        assert CATEGORY_TO_SHORT[command_and_control_category] == "c2"

    def test_reverse_lookup_roundtrip(self) -> None:
        dupe_shorts = {"scanning", "enum"}
        for short_name, category in SHORT_TO_CATEGORY.items():
            reverse = CATEGORY_TO_SHORT.get(category)
            if short_name in dupe_shorts:
                assert reverse in dupe_shorts
            else:
                assert reverse == short_name

    def test_reverse_lookup_less_than_or_equal_forward(self) -> None:
        assert len(CATEGORY_TO_SHORT) <= len(SHORT_TO_CATEGORY)


class TestAllCategories:
    def test_every_short_key_in_all_categories(self) -> None:
        mapping_values = set(SHORT_TO_CATEGORY.values())
        all_set = set(ALL_CATEGORIES)
        for val in mapping_values:
            assert val in all_set, f"{val} missing from ALL_CATEGORIES"

    def test_all_categories_non_empty(self) -> None:
        for category in ALL_CATEGORIES:
            assert category, f"ALL_CATEGORIES contains an empty string"

    def test_no_duplicate_all_categories(self) -> None:
        assert len(ALL_CATEGORIES) == len(set(ALL_CATEGORIES))

    def test_all_categories_count(self) -> None:
        assert len(ALL_CATEGORIES) >= 17


class TestBijectionInvariant:
    def test_forward_and_reverse_match(self) -> None:
        dupe_shorts = {"scanning", "enum"}
        for short_name, category_long in SHORT_TO_CATEGORY.items():
            reverse = CATEGORY_TO_SHORT.get(category_long)
            if short_name in dupe_shorts:
                assert reverse in dupe_shorts, (
                    f"Mismatch: {short_name} -> {category_long} -> {reverse}"
                )
            else:
                assert reverse == short_name, (
                    f"Mismatch: {short_name} -> {category_long} -> {reverse}"
                )
