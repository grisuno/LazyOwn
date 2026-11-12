"""Concurrency contract for the per-task exploration graph.

Separate graph instances share one on-disk file across threads and processes
(the CLI, the daemon and the C2 each open their own). A commit must merge the
on-disk state before writing and allocate ids under a cross-process lock, so
concurrent additions never lose each other and never collide on an id, while a
delete committed after the merge is not resurrected from disk.
"""

from __future__ import annotations

import threading

import modules.lazy_loop as loop


def _fresh_store(tmp_path, monkeypatch):
    monkeypatch.setattr(loop, "STORE_DIR", tmp_path, raising=False)


def test_concurrent_adds_do_not_lose_updates(tmp_path, monkeypatch):
    _fresh_store(tmp_path, monkeypatch)
    barrier = threading.Barrier(8)

    def _add(i: int) -> None:
        barrier.wait()
        loop.ExplorationGraph("t6").add_node("finding", f"finding number {i}")

    threads = [threading.Thread(target=_add, args=(i,)) for i in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    final = loop.ExplorationGraph("t6")
    assert len(final.nodes) == 8
    assert len(set(final.nodes)) == 8


def test_merge_adopts_other_writers_nodes(tmp_path, monkeypatch):
    _fresh_store(tmp_path, monkeypatch)
    graph_a = loop.ExplorationGraph("t6")
    graph_b = loop.ExplorationGraph("t6")
    graph_a.add_node("finding", "from a")
    graph_b.add_node("finding", "from b")
    reloaded = loop.ExplorationGraph("t6")
    texts = sorted(node.text for node in reloaded.nodes.values())
    assert texts == ["from a", "from b"]


def test_remove_nodes_is_not_resurrected_by_merge(tmp_path, monkeypatch):
    _fresh_store(tmp_path, monkeypatch)
    graph = loop.ExplorationGraph("t6")
    node = graph.add_node("intent", "remove me")
    assert graph.remove_nodes([node.node_id]) == 1
    reloaded = loop.ExplorationGraph("t6")
    assert node.node_id not in reloaded.nodes
