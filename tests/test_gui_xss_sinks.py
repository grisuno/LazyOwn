"""Regression gate for XSS sinks in the C2 dashboard template.

Every ``innerHTML`` sink fed by LLM or command output must pass through
the central ``safeHtml`` helper backed by DOMPurify. Raw interpolation
of server-controlled strings is a stored-XSS vector.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

_TEMPLATE = _ROOT / "templates" / "index.html"


def _read_template() -> str:
    """Return the raw dashboard template text."""
    return _TEMPLATE.read_text(encoding="utf-8")


class SafeHtmlHelperTests(unittest.TestCase):
    def test_helper_is_defined_exactly_once(self) -> None:
        text = _read_template()
        self.assertEqual(len(re.findall(r"function safeHtml\(dirty\)", text)), 1)

    def test_helper_prefers_dompurify_with_text_fallback(self) -> None:
        text = _read_template()
        self.assertIn("DOMPurify.sanitize", text)
        self.assertIn("textContent", text)


class SinkSanitizationTests(unittest.TestCase):
    def test_no_raw_response_interpolation(self) -> None:
        text = _read_template()
        raw = [line for line in text.splitlines() if "innerHTML" in line and "${data.response}" in line]
        self.assertEqual(raw, [])

    def test_no_raw_html_interpolation(self) -> None:
        text = _read_template()
        raw = [
            line for line in text.splitlines() if "innerHTML" in line and "${html}" in line and "safeHtml" not in line
        ]
        self.assertEqual(raw, [])

    def test_no_raw_error_interpolation(self) -> None:
        text = _read_template()
        raw = [
            line
            for line in text.splitlines()
            if "innerHTML" in line
            and ("${data.error}" in line or "${error.message}" in line)
            and "safeHtml" not in line
        ]
        self.assertEqual(raw, [])

    def test_no_raw_output_interpolation(self) -> None:
        text = _read_template()
        raw = [
            line
            for line in text.splitlines()
            if "innerHTML" in line
            and ("${data.output}" in line or "${cleanOutputText}" in line)
            and "safeHtml" not in line
            and line.strip()[:2] != "//"
        ]
        self.assertEqual(raw, [])


if __name__ == "__main__":
    unittest.main()
