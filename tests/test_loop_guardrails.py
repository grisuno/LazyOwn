"""Loop guardrails: repetition detection, EDR pacing, target caps,
vector fact memory. Stdlib-only contracts for the autonomous loop."""

from __future__ import annotations

import threading
import time

from modules.loop_guardrails import EdrPacer, FactVectorStore, RepeatDetector, TargetLimiter


def test_repeat_detector_flags_identical_window():
    """Given five identical commands, When recorded, Then the window is stuck."""
    detector = RepeatDetector(window=5)
    for _ in range(4):
        assert detector.record("nmap -sS 10.0.0.1") is False
    assert detector.record("nmap -sS 10.0.0.1") is True
    assert detector.last_commands()[0] == "nmap -sS 10.0.0.1"


def test_repeat_detector_recovery_on_variation():
    """Given a stuck window, When a different command arrives, Then the
    detector clears."""
    detector = RepeatDetector(window=3)
    detector.record("same")
    detector.record("same")
    detector.record("same")
    assert detector.stuck is True
    detector.reset()
    assert detector.stuck is False
    detector.record("different")
    assert detector.stuck is False


def test_edr_pacer_slow_scan_raises_level():
    """Given a recon command over the latency threshold, When observed,
    Then the pacer inserts delays and downgrades noisy scans."""
    pacer = EdrPacer(duration_threshold=30.0)
    assert pacer.level == 0
    pacer.observe("nmap -sS -T4 10.0.0.1", 45.0, "scan finished")
    assert pacer.level == 1
    assert pacer.inter_step_delay() > 0.0
    quiet = pacer.quieten("nmap -sS -T4 10.0.0.1")
    assert quiet.startswith("nmap -sT -T2")


def test_edr_pacer_connection_reset_raises_and_decays():
    """Given a reset-in-output step, When observed then decayed, Then
    the level rises on the signal and cools afterwards."""
    pacer = EdrPacer(duration_threshold=2.0)
    pacer.observe("smbclient -L host", 1.0, "Connection reset by peer")
    assert pacer.level == 1
    assert "reset" in pacer.signal
    pacer.decay()
    pacer.decay()
    assert pacer.level == 0


def test_edr_pacer_calm_level_returns_command_unchanged():
    """Given no anomalies, When quieten is called, Then the command is
    returned untouched."""
    pacer = EdrPacer()
    assert pacer.quieten("nikto -h target") == "nikto -h target"
    assert pacer.inter_step_delay() == 0.0


def test_target_limiter_caps_concurrency():
    """Given four threads and a cap of two, When each grabs a slot,
    Then at most two run at once."""
    limiter = TargetLimiter(max_concurrent=2)
    active = {"now": 0, "peak": 0}
    lock = threading.Lock()
    started = threading.Barrier(4)

    def _work() -> None:
        started.wait(timeout=5)
        with limiter.slot("10.0.0.1"):
            with lock:
                active["now"] += 1
                active["peak"] = max(active["peak"], active["now"])
            time.sleep(0.15)
            with lock:
                active["now"] -= 1

    threads = [threading.Thread(target=_work, daemon=True) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=10)
    assert active["peak"] == 2


def test_target_limiter_is_reentrant_per_thread():
    """Given one worker holding a target slot, When it grabs the same
    slot again, Then no deadlock occurs and one release frees it."""
    limiter = TargetLimiter(max_concurrent=1)
    probe = {"depth": 0}

    def _work() -> None:
        with limiter.slot("10.0.0.7"):
            probe["depth"] += 1
            with limiter.slot("10.0.0.7"):
                probe["depth"] += 1

    thread = threading.Thread(target=_work, daemon=True)
    thread.start()
    thread.join(timeout=5)
    assert not thread.is_alive()
    assert probe["depth"] == 2


def test_target_limiter_empty_target_bypasses():
    """Given an empty target, When a slot is taken, Then the semaphore
    is never touched and active targets stay zero."""
    limiter = TargetLimiter(max_concurrent=1)
    with limiter.slot(""):
        with limiter.slot(""):
            assert limiter.active_targets == 0


def test_fact_vector_store_roundtrip_and_search(tmp_path):
    """Given stored facts, When queried with related text, Then the
    most relevant fact ranks first and survives a reload."""
    path = tmp_path / "facts.json"
    store = FactVectorStore(path)
    assert store.add("nmap found port 445 smb open on 10.0.0.1", meta={"target": "10.0.0.1"})
    assert store.add("hydra brute forced ssh on 10.0.0.5 with rockyou")
    assert store.add("smbclient listed shares finance hr") is True
    duplicate = store.add("nmap found port 445 smb open on 10.0.0.1")
    assert duplicate is False

    hits = store.search("smb 445 shares", k=2)
    assert hits and "445" in hits[0]["text"]

    reloaded = FactVectorStore(path)
    assert len(reloaded) == 3
    rehit = reloaded.search("ssh bruteforce", k=1)
    assert rehit and "hydra" in rehit[0]["text"]


def test_fact_vector_store_search_block_rendering(tmp_path):
    """Given matching facts, When rendered as a block, Then every line
    is bullet-prefixed and short inputs are rejected."""
    store = FactVectorStore(tmp_path / "facts.json")
    assert store.add("world_model shows phase exploit on 10.0.0.1")
    block = store.search_block("world model phase exploit", k=3)
    assert block.startswith("- ")
    empty = FactVectorStore(tmp_path / "empty.json")
    assert empty.search_block("anything") == ""
