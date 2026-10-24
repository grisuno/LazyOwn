"""F4 hardening: verb watchdog, chain fact spool, ctf CLI, foothold chain."""

from __future__ import annotations

import subprocess
import tempfile
import threading
import time
import unittest
from pathlib import Path
from types import SimpleNamespace

from modules.chain_facts import spool_chain_outputs
from modules.chain_registry import Chain, load_all
from modules.chain_runner import ChainRunner, ChainStep


def _chain(steps: list[ChainStep]) -> Chain:
    """Build a minimal chain fixture for the runner."""
    return Chain(name="fixture", steps=steps)


class VerbWatchdogSpec(unittest.TestCase):
    """The SIGALRM watchdog fails hung verb steps without stalling the chain."""

    def test_hung_verb_times_out(self):
        class Shell:
            aliases: dict = {}

            def do_hang(self, line: str) -> None:
                time.sleep(60)

            def onecmd(self, command: str):
                verb, _, args = command.partition(" ")
                return getattr(self, f"do_{verb}")(args)

        chain = _chain([ChainStep(id="hang", run="hang", timeout=1)])
        started = time.monotonic()
        result = ChainRunner(chain, shell=Shell(), retry_backoff=0).run()
        elapsed = time.monotonic() - started
        self.assertEqual(result.steps[0].status, "timeout")
        self.assertIn("timeout", str(result.steps[0].reason))
        self.assertLess(elapsed, 10.0)

    def test_hung_verb_fails_whole_chain(self):
        class Shell:
            aliases: dict = {}

            def do_hang(self, line: str) -> None:
                time.sleep(60)

            def onecmd(self, command: str):
                verb, _, args = command.partition(" ")
                return getattr(self, f"do_{verb}")(args)

        chain = _chain(
            [
                ChainStep(id="turn", run="true"),
                ChainStep(id="hang", run="hang", timeout=1),
                ChainStep(id="after", run="true"),
            ]
        )
        result = ChainRunner(chain, shell=Shell(), retry_backoff=0).run()
        statuses = {step.id: step.status for step in result.steps}
        self.assertEqual(statuses["turn"], "ok")
        self.assertEqual(statuses["hang"], "timeout")
        self.assertNotIn("after", statuses)
        self.assertTrue(result.aborted)

    def test_fast_verb_still_on_main_thread(self):
        seen: list[bool] = []

        class Shell:
            aliases: dict = {}

            def do_ping(self, line: str) -> None:
                seen.append(threading.main_thread() is threading.current_thread())

            def onecmd(self, command: str):
                verb, _, args = command.partition(" ")
                return getattr(self, f"do_{verb}")(args)

        chain = _chain([ChainStep(id="ping", run="ping", timeout=2)])
        result = ChainRunner(chain, shell=Shell(), retry_backoff=0).run()
        self.assertEqual(result.steps[0].status, "ok")
        self.assertEqual(seen, [True])


class ChainFactsSpoolSpec(unittest.TestCase):
    """Chain outputs spool into the FactStore-readable layout."""

    def test_spool_writes_and_ingests(self):
        ingested: list[str] = []

        class FakeStore:
            def ingest_text(self, path: Path, host_hint: str = "") -> int:
                ingested.append(path.name)
                return 1

            def save(self) -> None:
                pass

        with tempfile.TemporaryDirectory() as tmp:
            result = SimpleNamespace(
                run_id="run1",
                target="10.0.0.5",
                variables={"target": "10.0.0.5"},
                steps=[
                    SimpleNamespace(id="exec", phase="post", output="uid=0(root) shell"),
                    SimpleNamespace(id="dump", phase="enum", output="password=Plain42"),
                    SimpleNamespace(id="empty", phase="", output=""),
                ],
            )
            spooled = spool_chain_outputs(
                result,
                sessions_dir=tmp,
                fact_store_factory=FakeStore,
            )
            self.assertEqual(spooled, 2)
            self.assertEqual(ingested, ["10.0.0.5_exec.txt", "10.0.0.5_dump.txt"])

    def test_empty_chain_spools_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = SimpleNamespace(run_id="r", target="", variables={}, steps=[])
            self.assertEqual(spool_chain_outputs(result, sessions_dir=tmp), 0)


class CtfCliSpec(unittest.TestCase):
    """The capture CLI is deterministic and scriptable."""

    def test_capture_cli_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp) / "uid.txt"
            evidence.write_text("uid=0(root) gid=0(root)")
            proc = subprocess.run(
                [
                    "python3",
                    "modules/ctf_capture.py",
                    "capture",
                    "vsftpd_backdoor",
                    "172.17.0.2",
                    "--output-file",
                    str(evidence),
                    "--sessions-dir",
                    tmp,
                    "--json-out",
                ],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr[:400])
            self.assertIn('"status": "captured"', proc.stdout)

            report = subprocess.run(
                ["python3", "modules/ctf_capture.py", "report", "--sessions-dir", tmp],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            self.assertEqual(report.returncode, 0)


class FootholdChainSpec(unittest.TestCase):
    """chains/gym_ms2_foothold.yaml renders deterministically."""

    def test_chain_loads_and_renders_tokens(self):
        chain = load_all().get("gym_ms2_foothold")
        self.assertIsNotNone(chain)
        resolved = chain.resolve(
            {"target": "172.17.0.2", "vuln": "vsftpd_backdoor", "exploit": "vsftpd_backdoor"}
        )
        ids = [step["id"] for step in resolved]
        self.assertEqual(
            ids,
            [
                "scope",
                "wait_beacon",
                "exploit",
                "deploy_agent",
                "beacon_settle",
                "ctf_capture",
                "sync",
            ],
        )
        ctf_step = next(step for step in resolved if step["id"] == "ctf_capture")
        self.assertIn("vsftpd_backdoor", ctf_step["run"])
        self.assertIn("172.17.0.2", ctf_step["run"])


if __name__ == "__main__":
    unittest.main()
