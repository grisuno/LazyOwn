"""Tests for modules/engage_summary.py.

Covers marker extraction, per-tool detail parsing, held-scan ports,
text/markdown rendering and report persistence. All fixtures are
synthetic; no shell or network involved.
"""

from __future__ import annotations

from pathlib import Path

from modules.engage_summary import (
    detail_for,
    full_output,
    held_scan_ports,
    marker_lines,
    render_markdown,
    render_text,
    write_report,
)


PING_OUTPUT = (
    "[+] rhost assign to 127.0.0.1  [+]\n"
    "    [+] Try... ping -c 1 127.0.0.1  [+]\n"
    "    [+] TTL:64 [+]\n"
    "    [+] Host alive likely Linux [+]\n"
    "    [+] os_id set to 1 (Linux) — persisted to payload.json [+]"
)

POPULATE_OUTPUT = (
    "[+] AUTO-POPULATE for target=127.0.0.1 [+]\n"
    "[+] Services: 4000/remoteanything, 6060/x11, 11434/ollama [+]\n"
    "[+] No changes — payload already populated. [+]"
)

SCAN_XML = """<?xml version="1.0"?>
<nmaprun><host><address addr="127.0.0.1" addrtype="ipv4"/>
<ports>
<port protocol="tcp" portid="4000"><state state="open"/><service name="remoteanything"/></port>
<port protocol="tcp" portid="22"><state state="closed"/><service name="ssh"/></port>
</ports></host></nmaprun>"""


def _step(command: str, **extra) -> dict:
    """Build one step result dict for rendering tests."""
    base = {"phase": "recon", "label": command, "command": command,
            "success": True, "skipped_reason": "", "switched_from": "",
            "evidence": "", "output_tail": ""}
    base.update(extra)
    return base


def test_marker_lines_drop_panels_and_bars():
    """Only [+] log lines survive; suggestion panels vanish."""
    text = PING_OUTPUT + "\n╭──── suggestions ────╮\n│ gobuster 56% │\n╰──╯\n"
    lines = marker_lines(text)
    assert any("TTL:64" in line for line in lines)
    assert not any("gobuster" in line for line in lines)


def test_detail_for_ping_extracts_os():
    """Ping detail surfaces TTL, liveness and os_id."""
    facts = detail_for("ping", PING_OUTPUT)
    assert any("TTL:64" in fact for fact in facts)
    assert any("Linux" in fact for fact in facts)


def test_detail_for_populate_extracts_services():
    """Populate detail surfaces services and change state."""
    facts = detail_for("auto_populate", POPULATE_OUTPUT)
    assert any("4000/remoteanything" in fact for fact in facts)
    assert any("No changes" in fact for fact in facts)


def test_detail_for_empty_search_is_honest():
    """A Not Found search reports no candidates, never invented ones."""
    facts = detail_for("searchsploit", "WARNING Not Found")
    assert facts == ["no candidates (Not Found)"]


def test_held_scan_ports_reads_xml(tmp_path: Path):
    """Held scan XMLs yield open ports and skip closed ones."""
    (tmp_path / "scan_127.0.0.1.nmap.xml").write_text(SCAN_XML, encoding="utf-8")
    ports, sources = held_scan_ports("127.0.0.1", tmp_path)
    assert "4000/remoteanything" in ports
    assert not any(p.startswith("22/") for p in ports)
    assert sources == ["scan_127.0.0.1.nmap.xml"]


def test_render_text_shows_skip_with_held_ports(tmp_path: Path):
    """Skipped scans still report the held ports in the summary."""
    (tmp_path / "scan_127.0.0.1.nmap.xml").write_text(SCAN_XML, encoding="utf-8")
    steps = [
        _step("ping", output_tail=PING_OUTPUT),
        _step("lazynmap", success=False, skipped_reason="scan_already_held"),
    ]
    text = render_text("abc123", "127.0.0.1", False, steps, tmp_path)
    assert "TTL:64" in text
    assert "scan_already_held" in text
    assert "4000/remoteanything" in text


def test_full_output_prefers_evidence(tmp_path: Path):
    """Evidence vault beats the truncated tail when a hash exists."""
    from modules.evidence import EvidenceStore
    vault = EvidenceStore(tmp_path / "evidence")
    digest = vault.put(b"full-fidelity-output")
    step = _step("ping", evidence=digest, output_tail="truncated")
    assert full_output(step, tmp_path) == "full-fidelity-output"
    assert full_output(_step("ping", output_tail="tail-only"), tmp_path) == "tail-only"


def test_write_report_persists_markdown(tmp_path: Path):
    """The engagement report lands under sessions/engagements/."""
    steps = [_step("ping", output_tail=PING_OUTPUT)]
    path = write_report("abc123", "127.0.0.1", False, steps, tmp_path)
    assert path == str(tmp_path / "engagements" / "engage_abc123.md")
    body = Path(path).read_text(encoding="utf-8")
    assert "# Engagement abc123" in body
    assert "TTL:64" in body
    assert "## Next actions" in body


def test_render_markdown_lists_evidence_and_next():
    """Markdown carries evidence hashes and next actions."""
    steps = [_step("ping", evidence="ab" * 32, output_tail=PING_OUTPUT)]
    upcoming = [{"action": "gobuster", "command": "gobuster -u http://t", "reasons": []}]
    body = render_markdown("abc123", "127.0.0.1", False, steps, upcoming, "sessions")
    assert "abababababab" in body
    assert "gobuster" in body
