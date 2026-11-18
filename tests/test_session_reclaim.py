"""Contract tests for the audited sessions cleanup planner.

The suite pins the single most important property of ``modules.session_reclaim``:
secrets, operator identity and the canonical persona are never placed in a
removable tier, and loot/evidence/memory are removed only when the operator
explicitly opts in. It also covers the dry-run default and the subset path of
``ShellSysCommandSet.do_clean`` so the command cannot regress into deleting
protected state.
"""

from __future__ import annotations

import os
from types import SimpleNamespace

import pytest

from modules import session_reclaim as sc


def _touch(path: str, size: int = 0) -> None:
    with open(path, "wb") as handle:
        handle.write(b"x" * size)


@pytest.fixture()
def sessions_tree(tmp_path):
    root = tmp_path / "sessions"
    root.mkdir()
    protected = [
        "api_keys.json",
        ".secret_key",
        ".auto_crypto_salt",
        "key.aes",
        "team_ca.key",
        "team_ca.pem",
        "rbac.db",
        "permissions.json",
        "soul.md",
        "download_resources.sh",
        "www.py",
    ]
    for name in protected:
        _touch(str(root / name), size=10)
    for name in ("c", "implant", "lin", "win", "php", "operators", "uploads", "phishing"):
        (root / name).mkdir()
        _touch(str(root / name / "seed.txt"), size=5)
    sensitive = [
        "credentials.txt",
        "credentials_admin.txt",
        "world_model.json",
        "notes.txt",
    ]
    for name in sensitive:
        _touch(str(root / name), size=20)
    (root / "evidence").mkdir()
    _touch(str(root / "evidence" / "capture.bin"), size=100)
    reclaim = [
        "scan_10.0.0.1.nmap",
        "transcript_abc.jsonl",
        "atomic_exploit_1.json",
        "linux_beacon.log",
        "session_deadbeef.json",
        "world.exe",
        "pentest_report.md",
        "report_final.md",
        "recon_plan_10.0.0.1.md",
        "digest_t0001.md",
        "killchain_final.html",
    ]
    for name in reclaim:
        _touch(str(root / name), size=30)
    (root / "reports").mkdir()
    _touch(str(root / "reports" / "out.html"), size=50)
    (root / "traffic").mkdir()
    _touch(str(root / "traffic" / "flow.pcap"), size=200)
    (root / "logs").mkdir()
    _touch(str(root / "logs" / "command_output.txt"), size=40)
    (root / "172.17.0.2" / "80").mkdir(parents=True)
    _touch(str(root / "172.17.0.2" / "80" / "nikto.txt"), size=15)
    return root


def test_secrets_identity_persona_are_protected(sessions_tree):
    plan = sc.build_plan(str(sessions_tree))
    protected = {entry.name for entry in plan.by_tier(sc.TIER_PROTECTED)}
    for must_keep in (
        "api_keys.json",
        ".secret_key",
        ".auto_crypto_salt",
        "key.aes",
        "team_ca.key",
        "team_ca.pem",
        "rbac.db",
        "permissions.json",
        "soul.md",
        "operators",
        "uploads",
        "phishing",
        "c",
        "implant",
    ):
        assert must_keep in protected


def test_protected_never_removable(sessions_tree):
    plan = sc.build_plan(str(sessions_tree))
    removable = {entry.name for entry in plan.removable(include_sensitive=True)}
    assert "api_keys.json" not in removable
    assert "soul.md" not in removable
    assert "team_ca.key" not in removable
    assert "rbac.db" not in removable


def test_loot_and_memory_are_sensitive(sessions_tree):
    plan = sc.build_plan(str(sessions_tree))
    sensitive = {entry.name for entry in plan.by_tier(sc.TIER_SENSITIVE)}
    assert {"credentials.txt", "world_model.json", "notes.txt"} <= sensitive
    assert "evidence" in sensitive


def test_generated_reports_are_reclaim(sessions_tree):
    plan = sc.build_plan(str(sessions_tree))
    reclaim = {entry.name for entry in plan.by_tier(sc.TIER_RECLAIM)}
    sensitive = {entry.name for entry in plan.by_tier(sc.TIER_SENSITIVE)}
    generated = {
        "pentest_report.md",
        "report_final.md",
        "recon_plan_10.0.0.1.md",
        "digest_t0001.md",
        "killchain_final.html",
        "reports",
    }
    assert generated <= reclaim
    assert generated.isdisjoint(sensitive)


def test_sensitive_excluded_from_default_removal(sessions_tree):
    plan = sc.build_plan(str(sessions_tree))
    reclaim_only = {entry.name for entry in plan.removable(include_sensitive=False)}
    assert "credentials.txt" not in reclaim_only
    assert "world_model.json" not in reclaim_only
    include_all = {entry.name for entry in plan.removable(include_sensitive=True)}
    assert "credentials.txt" in include_all
    assert "world_model.json" in include_all


def test_reclaim_contains_campaign_noise(sessions_tree):
    plan = sc.build_plan(str(sessions_tree))
    reclaim = {entry.name for entry in plan.by_tier(sc.TIER_RECLAIM)}
    assert {"scan_10.0.0.1.nmap", "transcript_abc.jsonl", "traffic", "logs", "172.17.0.2"} <= reclaim


def test_classify_fallback_is_reclaim():
    tier, label = sc.classify("totally_unknown_artifact_xyz")
    assert tier == sc.TIER_RECLAIM
    assert label


def test_subset_restricts_to_matching_entries(sessions_tree):
    plan = sc.build_plan(str(sessions_tree), subset="nmap")
    names = {entry.name for entry in plan.entries}
    assert names == {"scan_10.0.0.1.nmap"}
    assert not plan.by_tier(sc.TIER_PROTECTED)


def test_unknown_subset_raises(sessions_tree):
    with pytest.raises(ValueError):
        sc.build_plan(str(sessions_tree), subset="bogus")


def test_remove_entries_deletes_only_targets(sessions_tree):
    plan = sc.build_plan(str(sessions_tree))
    targets = plan.removable(include_sensitive=False)
    result = sc.remove_entries(targets)
    assert not result.errors
    assert result.reclaimed_bytes > 0
    assert (sessions_tree / "api_keys.json").exists()
    assert (sessions_tree / "soul.md").exists()
    assert (sessions_tree / "credentials.txt").exists()
    assert not (sessions_tree / "scan_10.0.0.1.nmap").exists()
    assert not (sessions_tree / "traffic").exists()


def test_empty_only_dir_is_cleared_not_removed(sessions_tree):
    plan = sc.build_plan(str(sessions_tree))
    logs = [entry for entry in plan.entries if entry.name == "logs"]
    assert logs and logs[0].empty_only
    sc.remove_entries(logs)
    assert (sessions_tree / "logs").is_dir()
    assert not any((sessions_tree / "logs").iterdir())


def test_human_size_units():
    assert sc.human_size(500) == "500B"
    assert sc.human_size(1024) == "1.0K"
    assert sc.human_size(1024 * 1024) == "1.0M"
    assert sc.human_size(1024 * 1024 * 1024) == "1.0G"


def test_safe_label_escapes_direction_override():
    spoof = "no_priv‮xfdp.exe"
    rendered = sc.safe_label(spoof)
    assert "‮" not in rendered
    assert "\\u202e" in rendered


def test_do_clean_dry_run_deletes_nothing(monkeypatch, sessions_tree):
    from cli.commands.shellsys import ShellSysCommandSet

    monkeypatch.chdir(sessions_tree.parent)
    before = set(os.listdir(sessions_tree))
    ShellSysCommandSet.do_clean(SimpleNamespace(), "")
    after = set(os.listdir(sessions_tree))
    assert before == after


def test_do_clean_subset_force_removes_only_subset(monkeypatch, sessions_tree):
    from cli.commands.shellsys import ShellSysCommandSet

    monkeypatch.chdir(sessions_tree.parent)
    ShellSysCommandSet.do_clean(SimpleNamespace(), "nmap --force")
    assert not (sessions_tree / "scan_10.0.0.1.nmap").exists()
    assert (sessions_tree / "transcript_abc.jsonl").exists()
    assert (sessions_tree / "api_keys.json").exists()
    assert (sessions_tree / "soul.md").exists()


def test_do_clean_rejects_unknown_argument(monkeypatch, sessions_tree):
    from cli.commands.shellsys import ShellSysCommandSet

    monkeypatch.chdir(sessions_tree.parent)
    before = set(os.listdir(sessions_tree))
    ShellSysCommandSet.do_clean(SimpleNamespace(), "--wat")
    after = set(os.listdir(sessions_tree))
    assert before == after
