"""BDD tests for the typed verb manifest store."""

from __future__ import annotations

from pathlib import Path

import pytest

from modules.chain_registry import ChainStep
from modules.verb_manifest import FactPredicate, parse_manifest, plan_check


@pytest.fixture
def manifest_path(tmp_path: Path) -> Path:
    """Isolated manifest file so tests never read the operator seed."""
    path = tmp_path / "verb_manifests.yaml"
    path.write_text(
        """
version: 1
manifests:
  lazynmap:
    version: 1
    phase: recon
    cost: {tokens: 300, seconds: 600, toolcalls: 1}
    noise: {weight: 0.7, why: loud probe, sigma: [LAZ-010]}
    preconditions:
      - {fact: host_known, host: "{target}"}
    effects:
      - {fact: services_discovered, host: "{target}"}
      - {fact: scan_completed, host: "{target}"}
    idempotent: true
  gobuster:
    version: 1
    phase: enum
    noise: {weight: 0.4}
    preconditions:
      - {fact: service_open, host: "{target}", service: http}
    effects:
      - {fact: min_version_collected, host: "{target}"}
  badverb:
    version: 1
    preconditions:
      - {fact: not_in_vocabulary, host: "{target}"}
""",
        encoding="utf-8",
    )
    return path


class TestSchema:
    """Manifest parsing is strict but fail-safe."""

    def test_valid_manifest_parses(self, manifest_path: Path):
        """Given a seeded store, Then typed verbs exist with cores."""
        from modules.verb_manifest import manifests

        store = manifests(manifest_path)
        assert "lazynmap" in store, "seed verbs survive parsing"
        noise = store["lazynmap"].noise
        assert noise.weight == pytest.approx(0.7), "noise prior must be kept"
        assert store["lazynmap"].cost.toolcalls == 1
        assert any(p.fact == "scan_completed" for p in store["lazynmap"].effects), "effects carry produced facts"
        assert store["lazynmap"].idempotent, "idempotency is part of the signature"

    def test_unknown_fact_id_dropped(self, manifest_path: Path):
        """Given a bad fact id, Then that manifest disappears, the rest stays."""
        from modules.verb_manifest import manifests

        store = manifests(manifest_path)
        assert "badverb" not in store, "invalid manifests vanish, never block the loop"
        assert "lazynmap" in store

    def test_parse_manifest_rejects_junk(self):
        """Given junk input, Then ValueError with a reason."""
        with pytest.raises(ValueError):
            parse_manifest("1bad", {})
        with pytest.raises(ValueError):
            parse_manifest("okverb", "not a mapping")


class TestPlanCheck:
    """Semantic chain checking beyond token resolution."""

    def test_unmet_precondition_reported(self, manifest_path: Path):
        """Given gobuster without any http fact, Then one warning."""
        steps = [ChainStep(id="gob", run="gobuster dir --url http://{target} -w w")]
        facts = [FactPredicate(fact="host_known", host="{target}")]
        problems = plan_check(steps, {"target": "10.0.0.1"}, path=manifest_path, facts=facts)
        assert any("gob (gobuster) needs service_open" in p for p in problems), "provably unmet preconditions surface"

    def test_effect_paid_forward(self, manifest_path: Path):
        """Given a scan step first, Then later effects may unlock nothing wrong."""
        steps = [
            ChainStep(id="scan", run="lazynmap {target}"),
            ChainStep(id="gob", run="gobuster dir --url http://{target} -w w"),
        ]
        facts = [FactPredicate(fact="host_known", host="{target}")]
        problems = plan_check(steps, {"target": "10.0.0.1"}, path=manifest_path, facts=facts)
        assert not [p for p in problems if "scan (lazynmap)" in p], (
            "host_known is a world-model fact the scan itself may satisfy"
        )
        assert any("needs service_open" in p for p in problems), "services_discovered is not service_open"

    def test_world_model_facts_default(self):
        """Given no injected facts, Then the world model projection applies."""
        steps = [ChainStep(id="bh", run="bloodhound {target}")]
        problems = plan_check(steps, {"target": "172.17.0.2"})
        assert [p for p in problems if "needs credentials" in p] != [], (
            "real-world data still flows through semantic checks"
        )

    def test_fallback_when_store_empty(self, tmp_path: Path):
        """Given a path with no file, Then no crash and no nag."""
        problems = plan_check([ChainStep(run="hydra x")], {}, path=tmp_path / "none.yaml")
        assert problems == []


class TestNoiseAndCost:
    """The prior travels to surfaces that need it, values bounded."""

    def test_noise_clamped(self):
        """Given an out-of-range weight, Then the value is clamped."""
        from modules.verb_manifest import _parse_noise

        assert _parse_noise({"weight": 9}).weight == pytest.approx(1.0)
        assert _parse_noise({"weight": -1}).weight == pytest.approx(0.0)
        assert _parse_noise({"weight": "x"}).weight == pytest.approx(0.0)

    def test_cost_tolerates_junk(self):
        """Given a junk cost block, Then defaults apply."""
        from modules.verb_manifest import _parse_cost

        cost = _parse_cost({"tokens": "many", "seconds": None})
        assert cost.tokens == 0 and cost.seconds == 0.0 and cost.toolcalls == 1
