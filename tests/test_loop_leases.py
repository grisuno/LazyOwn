"""Tests for modules.loop.leases."""

from __future__ import annotations

import threading

import pytest

from modules.loop.leases import DEFAULT_LEASE_TTL_SEC, LeaseStore


@pytest.fixture()
def store(tmp_path):
    """Lease store on a throwaway database."""
    return LeaseStore(db_path=str(tmp_path / "leases.db"))


def test_first_claim_wins(store):
    lease = store.try_claim("t1", 7, "worker-a")
    assert lease is not None
    assert lease.node_id == 7
    assert lease.worker == "worker-a"


def test_second_claim_while_held_fails(store):
    assert store.try_claim("t1", 7, "worker-a") is not None
    assert store.try_claim("t1", 7, "worker-b") is None


def test_settled_intent_never_reclaims(store):
    store.try_claim("t1", 7, "worker-a")
    assert store.settle("t1", 7) is True
    assert store.try_claim("t1", 7, "worker-b") is None
    assert store.settle("t1", 7) is False


def test_expired_lease_reclaimable(store):
    import time

    store.try_claim("t1", 7, "worker-a", ttl_sec=0.0)
    time.sleep(0.01)
    assert store.try_claim("t1", 7, "worker-b") is not None


def test_expired_claim_freed_by_sweep(store):
    store.try_claim("t1", 7, "worker-a", ttl_sec=0.0)
    freed = store.sweep()
    assert ("t1", 7) in freed
    assert store.try_claim("t1", 7, "worker-b") is not None
    assert store.sweep() == []


def test_heartbeat_extends_live_lease_only(store):
    store.try_claim("t1", 7, "worker-a", ttl_sec=DEFAULT_LEASE_TTL_SEC)
    assert store.heartbeat("t1", 7, ttl_sec=DEFAULT_LEASE_TTL_SEC) is True
    store.settle("t1", 7)
    assert store.heartbeat("t1", 7, ttl_sec=DEFAULT_LEASE_TTL_SEC) is False
    assert store.heartbeat("tX", 99) is False


def test_release_makes_intent_claimable(store):
    store.try_claim("t1", 7, "worker-a")
    assert store.release("t1", 7) is True
    assert store.active("t1", 7) is False
    assert store.release("t1", 7) is False
    assert store.try_claim("t1", 7, "worker-b") is not None


def test_active_and_counts(store):
    store.try_claim("t1", 1, "w1")
    store.try_claim("t1", 2, "w2")
    store.settle("t1", 2)
    assert store.active("t1", 1) is True
    assert store.active("t1", 2) is False
    counts = store.counts()
    assert counts["live"] == 1
    assert counts["settled"] == 1
    assert counts["expired"] == 0


def test_independent_tasks_do_not_collide(store):
    assert store.try_claim("t1", 7, "w1") is not None
    assert store.try_claim("t2", 7, "w2") is not None


def test_cross_process_claim_via_second_connection(tmp_path):
    first = LeaseStore(db_path=str(tmp_path / "leases.db"))
    second = LeaseStore(db_path=str(tmp_path / "leases.db"))
    assert first.try_claim("t1", 7, "w1") is not None
    assert second.try_claim("t1", 7, "w2") is None
    first.release("t1", 7)
    assert second.try_claim("t1", 7, "w2") is not None


def test_threads_do_not_share_connection_state(store):
    results = []

    def claim(target):
        lease = store.try_claim("t1", 7, f"w{target}")
        results.append(lease is not None)

    threads = [threading.Thread(target=claim, args=(i,)) for i in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert results.count(True) == 1
