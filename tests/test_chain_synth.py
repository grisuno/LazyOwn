"""BDD tests for runtime chain synthesis."""

from __future__ import annotations

from pathlib import Path

import pytest

from modules.chain_synth import facts_for_target, synth_chain_data, write_generated_chain


class TestSynthData:
    """Chain dicts compose the kill-chain spine plus service steps."""

    def test_spine_steps_present(self):
        """Given inputs and one service, Then scope/scan/populate/steps exist."""
        story = "baseline chain never missing"
        data, _notes = synth_chain_data(
            "rocke",
            "10.5.5.5",
            [{"service": "http", "port": 8080}],
        )
        step_ids = [s["id"] for s in data["steps"]]
        assert {"scope", "scan", "auto_populate", "http_enum_8080", "exp_sweep"} <= set(step_ids), story
        assert data["defaults"]["playbook"] == "rocke", story

    def test_service_variants(self):
        """Given ssh/smb facts, Then hydra/enum4linux steps appear once each."""
        story = "repeats collapse"
        data, _n = synth_chain_data(
            "",
            "10.5.5.6",
            [
                {"service": "ssh", "port": 22},
                {"service": "microsoft-ds", "port": 445},
                {"service": "microsoft-ds", "port": 445},
            ],
        )
        ids = [s["id"] for s in data["steps"]]
        assert ids.count("ssh_bruteforce") == 1, story
        assert ids.count("smb_enum") == 1, story

    def test_cred_reuse_and_c2_flags(self):
        """Given has_creds and include_c2=False, Then matching steps react."""
        story = "booleans steer composition"
        with_creds, _ = synth_chain_data("r", "t", [], has_creds=True)
        without_c2, _ = synth_chain_data("r", "t", [], include_c2=False)
        assert "cred_reuse" in {s["id"] for s in with_creds["steps"]}, story
        assert "c2_server start" not in json_text(without_c2), story


def json_text(data) -> str:
    import yaml

    return yaml.safe_dump(data)


class TestGeneratedFile:
    """Generated chains validate before they are written."""

    def test_write_ok_then_registry_sees_it(self, tmp_path: Path):
        """Given valid data, Then the file backs a loadable chain."""
        story = "generated must be registry-grade"
        data, _n = synth_chain_data("rocke", "10.5.5.9", [{"service": "http", "port": 80}])
        assert data["name"] == "apt_rocke_gen", story
        path, errors = write_generated_chain(data, chains_dir=tmp_path / "chains")
        assert errors == [] and path is not None and path.exists(), story

    def test_invalid_data_never_written(self, tmp_path: Path):
        """Given broken step data, Then validation blocks the write."""
        story = "no poisoning of the registry by synthesis"
        data, _n = synth_chain_data("rocke", "10.5.5.9", [])
        data["steps"][0]["id"] = "9starts-with-digit"
        path, errors = write_generated_chain(data, chains_dir=tmp_path / "chains")
        assert path is None and errors, story


class TestFactsForTarget:
    """Fact store drain is fail-soft."""

    def test_unknown_target_empty(self):
        """Given no known host, Then empty service profile."""
        story = "no invented services"
        profile = facts_for_target("203.0.113.77")
        assert profile["services"] == [] and profile["os_hint"] == "", story
