"""Tests for cli/graph_advisor.py.

The suite is driven by a small synthetic graphify-style JSON fixture so it
runs deterministically without the full 1500-node LazyOwn graph. The real
graph is exercised via the smoke test ``test_real_graph_summary_when_available``
which becomes a no-op when ``graphify-out/graph_lazyown.json`` is missing.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.graph_advisor import (  # noqa: E402
    GraphAdvisor,
    GraphAdvisorConfig,
    GraphIndex,
    GraphLoader,
    GraphScorer,
    format_god_nodes,
    format_neighbors,
    format_search_table,
    format_suggestions,
)


@pytest.fixture
def small_graph_data() -> dict:
    return {
        "directed": False,
        "multigraph": False,
        "nodes": [
            {"id": "lazyown_do_lazynmap", "label": "do_lazynmap()", "community": 1, "file_type": "code", "source_file": "lazyown.py", "source_location": "L1000"},
            {"id": "lazyown_do_ping", "label": "do_ping()", "community": 1, "file_type": "code", "source_file": "lazyown.py", "source_location": "L500"},
            {"id": "lazyown_do_assign", "label": "do_assign()", "community": 2, "file_type": "code", "source_file": "lazyown.py", "source_location": "L100"},
            {"id": "utils_run_command", "label": "run_command()", "community": 2, "file_type": "code", "source_file": "utils.py", "source_location": "L42"},
            {"id": "modules_kerberoast", "label": "kerberoast", "community": 3, "file_type": "code", "source_file": "modules/kerberoast.py", "source_location": "L1"},
            {"id": "isolated_node", "label": "lonely", "community": 4, "file_type": "code", "source_file": "lonely.py", "source_location": "L1"},
        ],
        "links": [
            {"source": "lazyown_do_lazynmap", "target": "utils_run_command", "relation": "calls", "confidence": "EXTRACTED", "confidence_score": 1.0, "weight": 1.0},
            {"source": "lazyown_do_ping", "target": "utils_run_command", "relation": "calls", "confidence": "EXTRACTED", "confidence_score": 1.0, "weight": 1.0},
            {"source": "lazyown_do_assign", "target": "utils_run_command", "relation": "uses", "confidence": "INFERRED", "confidence_score": 0.7, "weight": 1.0},
            {"source": "lazyown_do_lazynmap", "target": "modules_kerberoast", "relation": "conceptually_related_to", "confidence": "INFERRED", "confidence_score": 0.6, "weight": 1.0},
        ],
    }


@pytest.fixture
def small_graph_path(tmp_path: Path, small_graph_data: dict) -> Path:
    path = tmp_path / "graph.json"
    path.write_text(json.dumps(small_graph_data), encoding="utf-8")
    return path


@pytest.fixture
def advisor(small_graph_path: Path) -> GraphAdvisor:
    GraphLoader.clear_cache()
    return GraphAdvisor.from_path(small_graph_path)


def test_loader_resolves_explicit_path(tmp_path, small_graph_data):
    file_path = tmp_path / "alt.json"
    file_path.write_text(json.dumps(small_graph_data), encoding="utf-8")
    loader = GraphLoader(GraphAdvisorConfig())
    data = loader.load(file_path)
    assert data is not None
    assert len(data["nodes"]) == 6


def test_loader_returns_none_when_missing(tmp_path):
    loader = GraphLoader(GraphAdvisorConfig(graphify_dir=str(tmp_path / "nope")))
    assert loader.resolve_path() is None
    assert loader.load() is None


def test_index_builds_adjacency_and_degree(small_graph_data):
    index = GraphIndex(small_graph_data)
    assert {n.id for n in index.nodes()} == {
        "lazyown_do_lazynmap", "lazyown_do_ping", "lazyown_do_assign",
        "utils_run_command", "modules_kerberoast", "isolated_node",
    }
    assert set(index.neighbors("utils_run_command")) == {
        "lazyown_do_lazynmap", "lazyown_do_ping", "lazyown_do_assign",
    }
    assert index.degree("utils_run_command") == 3
    assert index.degree("isolated_node") == 0
    top = index.degree_ranked()
    assert top[0][0] == "utils_run_command"


def test_scorer_prefers_prefix_match(small_graph_data):
    scorer = GraphScorer(GraphAdvisorConfig())
    index = GraphIndex(small_graph_data)
    ranked = scorer.rank(index.nodes(), "do_lazynmap")
    assert ranked[0].node.id == "lazyown_do_lazynmap"
    assert ranked[0].matched_field == "label"


def test_scorer_returns_empty_for_unrelated_query(small_graph_data):
    scorer = GraphScorer(GraphAdvisorConfig())
    index = GraphIndex(small_graph_data)
    assert scorer.rank(index.nodes(), "xyzzy_qwerty_nothingmatches") == []


def test_advisor_summary_reports_topology(advisor):
    summary = advisor.summary()
    assert summary["available"] is True
    assert summary["nodes"] == 6
    assert summary["edges"] == 4
    assert summary["communities"] == 4


def test_advisor_search_returns_ranked_nodes(advisor):
    results = advisor.search("lazynmap", limit=3)
    assert results
    assert results[0]["label"] == "do_lazynmap()"
    assert "score" in results[0]
    assert "community" in results[0]


def test_advisor_neighbors_returns_layered_walk(advisor):
    result = advisor.neighbors("utils_run_command", depth=1)
    assert result["matched"]["id"] == "utils_run_command"
    neighbour_labels = {entry["node"]["label"] for entry in result["neighbors"]}
    assert neighbour_labels == {"do_lazynmap()", "do_ping()", "do_assign()"}
    for entry in result["neighbors"]:
        assert entry["edges"], "every neighbour must carry edge metadata"


def test_advisor_neighbors_respects_depth(advisor):
    one_hop = advisor.neighbors("lazyown_do_ping", depth=1)
    two_hop = advisor.neighbors("lazyown_do_ping", depth=2)
    assert len(two_hop["neighbors"]) >= len(one_hop["neighbors"])


def test_advisor_god_nodes_ranks_by_degree(advisor):
    god = advisor.god_nodes(limit=5)
    assert god[0]["id"] == "utils_run_command"
    assert god[0]["degree"] == 3


def test_advisor_suggest_next_walks_from_recent(advisor):
    suggestions = advisor.suggest_next(["do_lazynmap"], limit=5)
    ids = [entry["id"] for entry in suggestions]
    assert "utils_run_command" in ids
    assert "modules_kerberoast" in ids
    assert "lazyown_do_lazynmap" not in ids


def test_advisor_did_you_mean_returns_close_labels(advisor):
    suggestions = advisor.did_you_mean("kerber")
    assert suggestions
    assert any("kerber" in s.lower() for s in suggestions)


def test_advisor_truncate_respects_token_budget(advisor):
    payload = {"results": advisor.search("o", limit=20)}
    trimmed = advisor.truncate_to_budget(payload, budget_tokens=20)
    assert len(trimmed["results"]) < 20 or len(json.dumps(trimmed)) <= 20 * 4 + 200


def test_advisor_handles_missing_graph_gracefully(tmp_path):
    GraphLoader.clear_cache()
    cfg = GraphAdvisorConfig(graphify_dir=str(tmp_path / "missing"))
    advisor = GraphAdvisor(config=cfg)
    assert advisor.is_available() is False
    assert advisor.search("anything") == []
    assert advisor.god_nodes() == []
    summary = advisor.summary()
    assert summary["available"] is False
    assert "no graphify graph" in summary["reason"]


def test_advisor_reads_recent_commands_from_csv(tmp_path, advisor):
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    csv_path = sessions / "LazyOwn_session_report.csv"
    csv_path.write_text(
        "timestamp,tool,args,domain,output_path\n"
        "1,do_ping,,target.htb,foo\n"
        "2,do_lazynmap,,target.htb,bar\n",
        encoding="utf-8",
    )
    cfg = GraphAdvisorConfig(sessions_dir=str(sessions))
    advisor = GraphAdvisor(config=cfg, index=advisor._index)
    recent = advisor.read_recent_commands()
    assert recent == ["do_ping", "do_lazynmap"]


# --- Format helpers ------------------------------------------------------


def test_format_search_table_renders_rows(advisor):
    results = advisor.search("lazynmap", limit=3)
    table = format_search_table(results)
    assert "lazynmap" in table
    assert "community" in table.lower() or "1" in table


def test_format_neighbors_renders_when_match_found(advisor):
    rendered = format_neighbors(advisor.neighbors("utils_run_command"))
    assert "run_command" in rendered
    assert "calls" in rendered


def test_format_god_nodes_handles_empty():
    assert format_god_nodes([]) == "no god nodes"


def test_format_suggestions_handles_empty():
    assert "no suggestions" in format_suggestions([])


# --- Smoke against the real graph (skipped when missing) ----------------


def test_real_graph_summary_when_available():
    GraphLoader.clear_cache()
    real_advisor = GraphAdvisor.from_path()
    if not real_advisor.is_available():
        pytest.skip("real graphify-out/graph_lazyown.json is not present")
    summary = real_advisor.summary()
    assert summary["nodes"] > 0
    assert summary["edges"] > 0
    god = real_advisor.god_nodes(limit=3)
    assert len(god) >= 1
    search = real_advisor.search("lazynmap", limit=3)
    assert search
