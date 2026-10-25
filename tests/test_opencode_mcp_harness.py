"""Opencode shim harness tool tests."""

from __future__ import annotations

import asyncio
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import lazyown_mcp_opencode as shim  # noqa: E402


class OpencodeShimHarnessSpec(unittest.TestCase):
    """Harness helpers surface through the curated opencode bridge."""

    def test_harness_tools_listed(self):
        tools = asyncio.run(shim.list_tools())
        names = {tool.name for tool in tools}
        for expected in ("harness_status", "golden_paths_show", "golden_paths_push", "ctf_report"):
            self.assertIn(expected, names)

    def test_harness_status_shape(self):
        result = asyncio.run(shim.call_tool("harness_status", {}))
        text = result[0].text
        self.assertIn("harness_enabled", text)
        self.assertIn("active_profile", text)
        self.assertIn("plan_llm_allowed", text)

    def test_golden_paths_and_ctf(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            from modules import golden_path as solver

            solver.build(sessions_dir=tmp)
            result = asyncio.run(shim.call_tool("golden_paths_show", {"top_k": 2}))
            self.assertIn('"paths"', result[0].text)
        push = asyncio.run(shim.call_tool("golden_paths_push", {}))
        self.assertIn("pushed", push[0].text)
        report = asyncio.run(shim.call_tool("ctf_report", {}))
        self.assertIn("ctf", report[0].text)
        self.assertIn("matrix", report[0].text)

    def test_unknown_tool_rejected(self):
        with self.assertRaises(ValueError):
            asyncio.run(shim.call_tool("definitely_not_a_tool", {}))


if __name__ == "__main__":
    unittest.main()
