"""Tests for modules/live_surface.py.

The suite drives the builder with synthetic world-model snapshots shaped like
the real ``sessions/world_model.json`` (hosts with services, credentials and a
network graph). It pins compromise/pulse classification, edge derivation,
centrality-driven sizing and graceful degradation on empty or malformed input.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from modules.live_surface import (  # noqa: E402
    COMPROMISED_STATES,
    GROUP_HOST,
    GROUP_SERVICE,
    build_live_graph,
)


def _world() -> dict:
    return {
        "hosts": {
            "10.0.0.1": {
                "ip": "10.0.0.1",
                "state": "owned",
                "services": {"22": {"name": "ssh", "version": "OpenSSH 8.4"}},
            },
            "10.0.0.2": {
                "ip": "10.0.0.2",
                "state": "scanned",
                "services": {"80": {"name": "http", "version": "nginx"}},
            },
        },
        "credentials": [{"value": "root:toor", "host": "10.0.0.1", "confirmed": True}],
        "network_graph": {
            "nodes": ["host:10.0.0.1", "service:ssh"],
            "relations": [
                {
                    "source": "host:10.0.0.1",
                    "target": "service:ssh",
                    "relation": "runs_service",
                    "weight": 1.0,
                    "attributes": {},
                }
            ],
        },
    }


def test_empty_world_is_well_formed():
    graph = build_live_graph({})
    assert graph["nodes"] == []
    assert graph["edges"] == []
    assert graph["stats"]["hosts"] == 0
    assert graph["stats"]["pivots"] == []


def test_none_world_is_tolerated():
    graph = build_live_graph(None)
    assert graph["nodes"] == []


def test_hosts_and_services_become_nodes():
    graph = build_live_graph(_world())
    ids = {n["id"]: n for n in graph["nodes"]}
    assert "host:10.0.0.1" in ids
    assert "host:10.0.0.2" in ids
    assert "service:ssh" in ids
    assert ids["host:10.0.0.1"]["group"] == GROUP_HOST
    assert ids["service:ssh"]["group"] == GROUP_SERVICE
    assert ids["host:10.0.0.1"]["label"] == "10.0.0.1"


def test_owned_host_pulses_and_counts_as_compromised():
    graph = build_live_graph(_world())
    ids = {n["id"]: n for n in graph["nodes"]}
    assert ids["host:10.0.0.1"]["pulse"] is True
    assert ids["host:10.0.0.2"]["pulse"] is False
    assert graph["stats"]["compromised"] == 1


def test_host_with_credential_pulses_even_if_not_owned():
    world = _world()
    world["hosts"]["10.0.0.2"]["state"] = "scanned"
    world["credentials"].append({"value": "a:b", "host": "10.0.0.2"})
    ids = {n["id"]: n for n in build_live_graph(world)["nodes"]}
    assert ids["host:10.0.0.2"]["pulse"] is True


def test_runs_service_edge_is_emitted_once():
    graph = build_live_graph(_world())
    ssh_edges = [e for e in graph["edges"] if e["from"] == "host:10.0.0.1" and e["to"] == "service:ssh"]
    assert len(ssh_edges) == 1
    assert ssh_edges[0]["relation"] == "runs_service"


def test_stats_block_counts():
    stats = build_live_graph(_world())["stats"]
    assert stats["hosts"] == 2
    assert stats["services"] == 2
    assert stats["credentials"] == 1


def test_malformed_host_entry_is_skipped():
    world = {"hosts": {"bad": "not-a-dict", "10.0.0.9": {"state": "scanned", "services": {}}}}
    ids = {n["id"] for n in build_live_graph(world)["nodes"]}
    assert "host:10.0.0.9" in ids
    assert "host:bad" not in ids


def test_compromised_states_constant_matches_world_model():
    assert "owned" in COMPROMISED_STATES
    assert "exploited" in COMPROMISED_STATES
    assert "scanned" not in COMPROMISED_STATES
