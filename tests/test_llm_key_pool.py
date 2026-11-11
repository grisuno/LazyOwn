"""LLM key-pool BDD contract: round-robin rotation and quota cooldown.

Given a multi-key pool, When keys rotate or hit quota errors, Then the pool
distributes load and parks exhausted keys without ever dropping to zero keys.
A single-key deployment behaves exactly as before.
"""

from __future__ import annotations

from core.llm_key_pool import (
    KeyPool,
    build_from_config,
    note_quota_error,
    refresh_from_config,
    resolve_pooled_key,
)


def test_round_robin_cycles_keys_in_order():
    """Given three keys, When next_key is called, Then it cycles in order."""
    pool = KeyPool()
    pool.set_keys("groq", ["a", "b", "c"])
    got = [pool.next_key("groq") for _ in range(4)]
    assert got == ["a", "b", "c", "a"]


def test_placeholders_and_duplicates_are_dropped():
    """Given noisy keys, When set, Then placeholders and dupes are removed."""
    pool = KeyPool()
    pool.set_keys("groq", ["a", "a", "", "api_key", "YOUR_API_KEY_HERE", "b"])
    assert pool.size("groq") == 2
    assert [pool.next_key("groq") for _ in range(2)] == ["a", "b"]


def test_exhausted_key_is_skipped_during_cooldown():
    """Given a quota error, When rotating, Then the parked key is skipped."""
    pool = KeyPool(cooldown_sec=100.0)
    pool.set_keys("groq", ["a", "b"])
    pool.mark_exhausted("groq", "a", now=1000.0)
    assert pool.next_key("groq", now=1000.0) == "b"
    assert pool.next_key("groq", now=1000.0) == "b"
    assert pool.available("groq", now=1000.0) == 1
    assert pool.next_key("groq", now=1200.0) in {"a", "b"}
    assert pool.available("groq", now=1200.0) == 2


def test_all_cooling_returns_soonest_so_progress_continues():
    """Given every key cooling, When rotating, Then a key is still returned."""
    pool = KeyPool(cooldown_sec=100.0)
    pool.set_keys("groq", ["a", "b"])
    pool.mark_exhausted("groq", "a", now=1000.0)
    pool.mark_exhausted("groq", "b", now=1050.0)
    assert pool.next_key("groq", now=1000.0) == "a"


def test_build_from_config_seeds_primary_first():
    """Given a primary key plus a pool, When built, Then primary is first."""
    pool = build_from_config({"api_key": "primary", "llm_key_pool": ["extra1", "extra2"]})
    assert pool.size("groq") == 3
    assert pool.next_key("groq") == "primary"


def test_build_from_config_supports_per_backend_mapping():
    """Given a mapping pool, When built, Then each backend gets its keys."""
    pool = build_from_config(
        {
            "api_key": "g1",
            "openai_api_key": "o1",
            "llm_key_pool": {"groq": ["g2"], "openai": ["o2", "o3"]},
        }
    )
    assert pool.size("groq") == 2
    assert pool.size("openai") == 3


def test_resolve_pooled_key_is_noop_without_a_pool():
    """Given a single key, When resolved, Then the fallback is returned."""
    refresh_from_config({"api_key": "solo", "llm_key_pool": []})
    assert resolve_pooled_key("groq", {"api_key": "solo"}, "solo") == "solo"


def test_resolve_pooled_key_rotates_with_a_pool():
    """Given a configured pool, When resolved repeatedly, Then keys rotate."""
    config = {"api_key": "primary", "llm_key_pool": ["extra"]}
    refresh_from_config(config)
    first = resolve_pooled_key("groq", config, "primary")
    second = resolve_pooled_key("groq", config, "primary")
    assert {first, second} == {"primary", "extra"}


def test_note_quota_error_parks_global_key():
    """Given a global pool, When a quota error is noted, Then the key cools."""
    config = {"api_key": "primary", "llm_key_pool": ["extra"]}
    refresh_from_config(config)
    note_quota_error("groq", "primary")
    got = {resolve_pooled_key("groq", config, "primary") for _ in range(4)}
    assert "extra" in got
