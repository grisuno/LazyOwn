"""BDD tests for the engagement timeline snapshots, diffs and zombies."""

from __future__ import annotations

import json

from modules import lazy_timeline


def _snap(path, ts: float, hosts: dict, dns: dict | None = None):
    """Write one snapshot file the way record() does."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "ts": ts,
        "hosts": hosts,
        "dns": dns or {},
    }), encoding="utf-8", )
    return path


HOSTS_A = {
    "10.66.44.7": {"state": "scanned", "services": {
        "22": {"name": "openssh", "version": "9.6", "state": "open"},
    }},
    "10.66.44.9": {"state": "scanned", "services": {
        "80": {"name": "nginx", "version": "1.26", "state": "open"},
    }},
}
HOSTS_B = {
    "10.66.44.7": {"state": "scanned", "services": {
        "22": {"name": "openssh", "version": "9.6", "state": "open"},
        "3389": {"name": "ms-wbt-server", "version": "", "state": "open"},
    }},
}
DNS_A = {"lab.lazyown.local": "10.66.44.9"}
DNS_B = {"lab.lazyown.local": ""}


class TestDiff:
    def test_new_gone_host_kinds(self, tmp_path):
        story = "hosts that appear or vanish produce their change kinds"
        a = _snap(tmp_path / "a.json", 1000.0, HOSTS_A)
        b = _snap(tmp_path / "b.json", 2000.0, HOSTS_B)
        result = lazy_timeline.diff(a, b)
        kinds = {(change["kind"], change["host"]) for change in result["changes"]}
        assert (lazy_timeline.KIND_HOST_GONE, "10.66.44.9") in kinds, story
        assert (lazy_timeline.KIND_HOST_NEW, "") not in kinds, story

    def test_port_and_version_kinds(self, tmp_path):
        story = "opened ports and version changes are detected"
        a = _snap(tmp_path / "a.json", 1000.0, HOSTS_A)
        b = _snap(tmp_path / "b.json", 2000.0, HOSTS_B)
        result = lazy_timeline.diff(a, b)
        kinds = {(change["kind"], change["port"]) for change in result["changes"]}
        assert (lazy_timeline.KIND_PORT_OPENED, 3389) in kinds, story

    def test_version_changed_kind(self, tmp_path):
        story = "a version bump on the same port is its own kind"
        newer = {
            "10.66.44.7": {"state": "scanned", "services": {
                "22": {"name": "openssh", "version": "9.8", "state": "open"},
            }},
        }
        a = _snap(tmp_path / "a.json", 1000.0, HOSTS_A)
        b = _snap(tmp_path / "b.json", 2000.0, newer)
        result = lazy_timeline.diff(a, b)
        assert any(change["kind"] == lazy_timeline.KIND_VERSION_CHANGED and change["port"] == 22
                   for change in result["changes"]), story

    def test_zombie_via_lost_dns(self, tmp_path):
        story = "a name that stops resolving while its host still serves flags a zombie"
        a = _snap(tmp_path / "a.json", 1000.0, HOSTS_A, DNS_A)
        b = _snap(tmp_path / "b.json", 2000.0, HOSTS_A, DNS_B)
        result = lazy_timeline.diff(a, b)
        assert result["zombies"] == ["10.66.44.9"], story

    def test_zombie_requires_services(self, tmp_path):
        story = "a dead name whose host has no services is not a zombie"
        quiet = {"10.66.44.9": {"state": "scanned", "services": {}}}
        a = _snap(tmp_path / "a.json", 1000.0, HOSTS_A, DNS_A)
        b = _snap(tmp_path / "b.json", 2000.0, quiet, DNS_B)
        result = lazy_timeline.diff(a, b)
        assert result["zombies"] == [], story

    def test_unreadable_inputs(self, tmp_path):
        story = "unreadable snapshots degrade to empty results"
        result = lazy_timeline.diff(tmp_path / "none", tmp_path / "none2")
        assert result == {"changes": [], "zombies": [], "a_ts": None, "b_ts": None}, story


class TestRecordAndShow:
    def test_record_writes_and_prunes(self, tmp_path):
        story = "record writes a snapshot and prunes beyond retention"
        for _ in range(3):
            result = lazy_timeline.record(state_path=tmp_path / "wm.json", snaps_dir=tmp_path, keep=2)
            assert result["path"], story
        snapshots = lazy_timeline.find_snapshots(tmp_path)
        assert len(snapshots) <= 2, story

    def test_record_from_world_state(self, tmp_path):
        story = "record reads a world-model state file into host/service shape"
        state = tmp_path / "wm.json"
        state.write_text(json.dumps({"hosts": {
            "10.66.44.7": {"state": "scanned", "services": {
                "22": {"port": 22, "name": "openssh", "version": "9.6"}
            }},
        }}), encoding="utf-8")
        result = lazy_timeline.record(state_path=state, snaps_dir=tmp_path, keep=2)
        assert result["hosts"] == 1, story
        snaps = lazy_timeline.find_snapshots(tmp_path)
        loaded = json.loads(snaps[-1].read_text(encoding="utf-8"))
        assert loaded["hosts"]["10.66.44.7"]["services"]["22"]["name"] == "openssh", story

    def test_show_summaries(self, tmp_path):
        story = "show lists snapshot summaries"
        _snap(tmp_path / "snap_1.json", 1.0, HOSTS_A)
        _snap(tmp_path / "snap_2.json", 2.0, HOSTS_B)
        rows = lazy_timeline.show(snaps_dir=tmp_path, last=2)
        assert [row["hosts"] for row in rows] == [2, 1], story
