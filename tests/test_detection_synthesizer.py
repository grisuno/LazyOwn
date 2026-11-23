"""Detection synthesizer tests: sigma/yara generation, determinism, save."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from modules.detection_synthesizer import (
    ActionFingerprint,
    save_rules,
    stable_rule_id,
    synthesize_sigma,
    synthesize_yara,
)


@pytest.fixture()
def fingerprint() -> ActionFingerprint:
    return ActionFingerprint(
        name="mimikatz",
        command="mimikatz.exe sekurlsa::logonpasswords -d 10.0.0.5",
        technique_id="T1003.001",
        category="credential",
        target_host="10.0.0.5",
        artifacts=["/tmp/lazymimi.exe", "mimidrv.sys"],
    )


class TestSigma:
    def test_yaml_parses_and_has_detection(self, fingerprint):
        rule = synthesize_sigma(fingerprint)
        data = list(yaml.safe_load_all(rule))[0]
        assert data["detection"]["condition"]
        assert data["status"] == "experimental"
        assert data["title"].startswith("LazyOwn Red Action")

    def test_deterministic_id(self, fingerprint):
        assert synthesize_sigma(fingerprint) == synthesize_sigma(fingerprint)
        assert stable_rule_id(fingerprint, "sigma") == stable_rule_id(fingerprint, "sigma")

    def test_technique_and_tactic_tags(self, fingerprint):
        rule = synthesize_sigma(fingerprint)
        assert "attack.t1003.001" in rule
        assert "attack.credential_access" in rule

    def test_unknown_category_falls_back_to_execution(self):
        fp = ActionFingerprint(name="x", command="zzz", category="zzz")
        assert "attack.execution" in synthesize_sigma(fp)

    def test_flags_are_not_signature_tokens(self, fingerprint):
        rule = synthesize_sigma(fingerprint)
        assert "'-d'" not in rule


class TestYara:
    def test_empty_without_artifacts(self):
        fp = ActionFingerprint(name="mimikatz", command="mimikatz")
        assert synthesize_yara(fp) == ""

    def test_artifacts_become_strings(self, fingerprint):
        rule = synthesize_yara(fingerprint)
        assert "lazymimi.exe" in rule
        assert "mimidrv.sys" in rule
        assert rule.strip().endswith("}")

    def test_rule_name_is_identifier(self):
        fp = ActionFingerprint(name="weird name!!", command="cmd", artifacts=["payload.bin"])
        rule = synthesize_yara(fp)
        assert "rule LazyOwn_" in rule


class TestSaveRules:
    def test_writes_sigma_and_yara(self, tmp_path, monkeypatch):
        monkeypatch.setattr("modules.detection_synthesizer.RULES_DIRNAME", str(tmp_path))
        monkeypatch.setattr("modules.detection_synthesizer.KIT_SIGMA_DIR", tmp_path / "kit")
        fp = ActionFingerprint(name="mimikatz", command="mimikatz -d 1", artifacts=["a.exe"])
        written = save_rules(fp)
        assert Path(written["sigma"]).exists()
        assert Path(written["yara"]).exists()
        assert "detection:" in Path(written["sigma"]).read_text()

    def test_install_copies_to_kit(self, tmp_path, monkeypatch):
        monkeypatch.setattr("modules.detection_synthesizer.RULES_DIRNAME", str(tmp_path))
        monkeypatch.setattr("modules.detection_synthesizer.KIT_SIGMA_DIR", tmp_path / "kit")
        fp = ActionFingerprint(name="mimikatz", command="mimikatz -d 1")
        written = save_rules(fp, install=True)
        assert Path(written["kit_sigma"]).exists()
