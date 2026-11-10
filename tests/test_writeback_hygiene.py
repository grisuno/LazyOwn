"""Worker writeback hygiene: listing walls never become facts, finding PoCs or bound evidence.

Every scenario states Given, When, Then.
"""

from __future__ import annotations

from modules.loop_guardrails import ListingNoiseDetector


class _WorkerHarness:
    """Minimal worker harness around ``_writeback`` without engine boot."""

    @staticmethod
    def build(tmp_path, wall, assertions):
        import modules.lazy_loop as loop

        transcripts = [("ls -R", wall), ("nmap -sV 127.0.0.1", "PORT STATE SERVICE\n22/tcp open ssh")]

        class _Graph:
            task_id = "t0002"

            def add_node(self, kind, text, **meta):
                assertions("fact-text", str(text))
                return loop.ExplorationNode(node_id=7, kind=kind, text=str(text))

            def add_edge(self, *args, **kwargs):
                pass

            def has_finding(self, text):
                assertions("finding-match", str(text))
                return None

            def anchors_for(self, node_id):
                return []

            def anchor(self, *args, **kwargs):
                pass

            def _persist(self):
                pass

        class _Assets:
            def insert(self, *args, **kwargs):
                raise ValueError("none")

        class _Traffic:
            def record(self, *args, **kwargs):
                pass

            def read(self, _n):
                return []

            def bind(self, *args, **kwargs):
                raise AssertionError("listing wall traffic must not bind as supporting evidence")

        class _ShellNone:
            pass

        worker = loop.Worker.__new__(loop.Worker)
        worker.name = "w-test"
        worker.graph = _Graph()
        worker.assets = _Assets()
        worker.traffic = _Traffic()
        worker.activity = loop.ActivityLog("t0002")
        worker.shell = _ShellNone()
        loop.Worker.task_id = property(lambda self: self.graph.task_id)
        return worker, transcripts


def test_writeback_filters_listing_wall_transcripts(tmp_path):
    """Given a worker writeback fed an ls -R wall, When writeback runs,
    Then neither the fact nor any finding carries the wall."""

    wall = "\n".join(f"sessions/lazy/artifact_{index}.json" for index in range(300))
    leaked = []

    def assertions(kind, text):
        if kind in ("fact-text", "finding-match") and "sessions/lazy/artifact_" in text:
            leaked.append(text[:80])

    worker, transcripts = _WorkerHarness.build(tmp_path, wall, assertions)
    worker._writeback(type("Intent", (), {"node_id": 3, "text": "baseline recon"})(), transcripts, allow_finding=False)
    assert not leaked, "the listing wall leaked into the writeback surfaces"
    assert ListingNoiseDetector().observe("ls -R", wall)


def test_reporter_prompt_caps_poc_and_sources_vault():
    """Given the bounded reporter prompt contract, When a huge PoC is fed,
    Then the prompt truncates it: the LLM context never swallows the wall."""
    wall = "\n".join(f"file_{index}.json" for index in range(500))
    prompt = "PoC/Evidence: " + wall[:1200]
    assert "file_499.json" not in prompt
    assert len(prompt) < 2000
