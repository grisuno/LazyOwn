"""Tests for cli/cli_enhancements.py and the audit CommandSet.

Each primitive is small and pure; tests cover happy + sad paths without
spinning up cmd2 except where strictly required (audit CommandSet wiring).
"""

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.aliases import load_aliases  # noqa: E402
from cli.cli_enhancements import (  # noqa: E402
    AddonHotReloader,
    CommandInfo,
    DictPayloadProvider,
    DynamicAliasResolver,
    FormField,
    FormSpec,
    FuzzyCommandIndex,
    InteractiveForm,
    LiveStatusTail,
    PayloadAwareCompleter,
    StaticCommandLister,
    TranscriptStore,
    commands_from_cmd2_shell,
)

# ── Fuzzy index ─────────────────────────────────────────────────────────────

@pytest.fixture
def fixture_index() -> FuzzyCommandIndex:
    cmds = [
        CommandInfo("lazynmap", "Full TCP/UDP nmap with vuln scripts.",
                    aliases=("nmap",)),
        CommandInfo("gobuster", "Directory brute-force.", aliases=()),
        CommandInfo("ffuf", "HTTP fuzzer.", aliases=("fuzz",)),
        CommandInfo("evil", "evil-winrm session.", aliases=("evil-winrm",)),
        CommandInfo("secretsdump", "Impacket secretsdump.", aliases=()),
    ]
    return FuzzyCommandIndex(StaticCommandLister(cmds))


def test_fuzzy_exact_match_scores_one(fixture_index):
    matches = fixture_index.search("lazynmap", limit=3)
    assert matches[0].info.name == "lazynmap"
    assert matches[0].score == 1.0


def test_fuzzy_alias_resolves_to_command(fixture_index):
    matches = fixture_index.search("nmap", limit=3)
    assert matches[0].info.name == "lazynmap"
    assert matches[0].matched_field == "alias"


def test_fuzzy_substring_match(fixture_index):
    matches = fixture_index.search("dump", limit=3)
    assert any(m.info.name == "secretsdump" for m in matches)


def test_fuzzy_empty_query_lists_all(fixture_index):
    matches = fixture_index.search("", limit=10)
    assert len(matches) == 5


def test_fuzzy_returns_empty_on_garbage(fixture_index):
    matches = fixture_index.search("zzzzzz_no_match", limit=3)
    assert matches == []


# ── Payload-aware completer ─────────────────────────────────────────────────

def test_completer_set_lists_payload_keys():
    payload = DictPayloadProvider({"rhost": "10.0.0.1", "lhost": "10.0.0.2"})
    c = PayloadAwareCompleter(payload)
    suggestions = c.complete("set", "")
    names = {s.text for s in suggestions}
    assert "rhost" in names
    assert "lhost" in names


def test_completer_target_lists_targets_and_rhost():
    payload = DictPayloadProvider({
        "rhost": "10.0.0.1",
        "targets": [{"ip": "10.0.0.2", "notes": "WS01"},
                    {"ip": "10.0.0.3", "notes": ""}],
    })
    c = PayloadAwareCompleter(payload)
    ips = {s.text for s in c.complete("target", "")}
    assert {"10.0.0.1", "10.0.0.2", "10.0.0.3"} <= ips


def test_completer_wordlist_keys_only_when_set():
    payload = DictPayloadProvider({"dirwordlist": "/usr/share/wordlists/dl.txt"})
    c = PayloadAwareCompleter(payload)
    out = c.complete("gobuster", "")
    assert any(s.text == "dirwordlist" for s in out)


def test_completer_addon_lister_used_for_run():
    payload = DictPayloadProvider({})
    c = PayloadAwareCompleter(payload, addon_lister=lambda: ["foo", "bar"])
    out = c.complete("run", "")
    names = {s.text for s in out}
    assert names == {"foo", "bar"}


def test_completer_filters_by_partial():
    payload = DictPayloadProvider({"rhost": "x", "lhost": "y", "lport": 1})
    c = PayloadAwareCompleter(payload)
    out = c.complete("set", "lh")
    assert {s.text for s in out} == {"lhost"}


def test_completer_ignores_unknown_command():
    payload = DictPayloadProvider({"rhost": "x"})
    c = PayloadAwareCompleter(payload)
    assert c.complete("totally_unknown_command", "") == []


# ── DynamicAliasResolver ────────────────────────────────────────────────────

def test_dynamic_resolver_renders_against_current_payload():
    resolver = DynamicAliasResolver()
    template = "sh nuclei sessions/scan_{rhost}.nmap.xml on {domain}"
    payload = DictPayloadProvider({"rhost": "10.10.11.5", "domain": "target.htb"})
    out = resolver.expand("autonuclei", template, payload)
    assert out == "sh nuclei sessions/scan_10.10.11.5.nmap.xml on target.htb"


def test_dynamic_resolver_missing_keys_become_empty():
    resolver = DynamicAliasResolver()
    out = resolver.expand("x", "echo {nope}_done", DictPayloadProvider({}))
    assert out == "echo _done"


def test_dynamic_resolver_payload_changes_propagate():
    resolver = DynamicAliasResolver()
    payload = DictPayloadProvider({"rhost": "A"})
    template = "scan {rhost}"
    assert resolver.expand("a", template, payload) == "scan A"
    payload.update({"rhost": "B"})
    assert resolver.expand("a", template, payload) == "scan B"


def test_dynamic_resolver_passes_through_literal_braces():
    resolver = DynamicAliasResolver()
    template = "echo not-a-placeholder"
    out = resolver.expand("a", template, DictPayloadProvider({}))
    assert out == template


def test_load_aliases_lazy_preserves_placeholders(tmp_path):
    p = tmp_path / "aliases.yaml"
    p.write_text("greet: 'echo hello {rhost}'\n")
    out = load_aliases({"rhost": "TARGET"}, path=p, lazy=True)
    assert out == {"greet": "echo hello {rhost}"}


def test_load_aliases_eager_substitutes(tmp_path):
    p = tmp_path / "aliases.yaml"
    p.write_text("greet: 'echo hello {rhost}'\n")
    out = load_aliases({"rhost": "TARGET"}, path=p, lazy=False)
    assert out == {"greet": "echo hello TARGET"}


# ── AddonHotReloader ────────────────────────────────────────────────────────

def test_hot_reloader_detects_new_file(tmp_path):
    addons = tmp_path / "addons"
    addons.mkdir()
    seen: list[Path] = []
    reloader = AddonHotReloader([addons], on_change=seen.append)
    reloader.poll_once()
    (addons / "new.yaml").write_text("name: x\n")
    changed = reloader.poll_once()
    assert any(p.name == "new.yaml" for p in changed)
    assert any(p.name == "new.yaml" for p in seen)


def test_hot_reloader_detects_modification(tmp_path):
    addons = tmp_path / "addons"
    addons.mkdir()
    fp = addons / "x.yaml"
    fp.write_text("name: x\n")
    seen: list[Path] = []
    reloader = AddonHotReloader([addons], on_change=seen.append, tick_seconds=0.1)
    reloader.poll_once()  # baseline
    fp.write_text("name: y\n")
    import os
    new_t = fp.stat().st_mtime + 5
    os.utime(fp, (new_t, new_t))
    changed = reloader.poll_once()
    assert fp in changed


def test_hot_reloader_ignores_non_addon_files(tmp_path):
    addons = tmp_path / "addons"
    addons.mkdir()
    (addons / "irrelevant.txt").write_text("x")
    seen: list[Path] = []
    reloader = AddonHotReloader([addons], on_change=seen.append)
    reloader.poll_once()
    assert seen == []


# ── LiveStatusTail ──────────────────────────────────────────────────────────

def test_status_tail_extracts_open_ports():
    raw = dedent("""
        Starting Nmap 7.94
        PORT    STATE SERVICE
        22/tcp  open  ssh
        80/tcp  open  http
        443/tcp open  https
        Stats: about 47.2% done; ETC: 12:30
    """).strip()
    update = LiveStatusTail().parse(raw)
    assert update.ports_seen == 3
    assert update.open_ports == (22, 80, 443)
    assert update.completed_pct == pytest.approx(47.2)
    assert "Stats" in update.last_line or update.last_line


def test_status_tail_handles_empty():
    update = LiveStatusTail().parse("")
    assert update.ports_seen == 0
    assert update.open_ports == ()
    assert update.completed_pct is None


def test_status_tail_no_ports_falls_back_to_stats():
    raw = "Stats: 12 open found; ETC: 12:30"
    update = LiveStatusTail().parse(raw)
    assert update.ports_seen == 12
    assert update.completed_pct is None


# ── TranscriptStore ─────────────────────────────────────────────────────────

def test_transcript_grep_matches_recent_output(tmp_path):
    store = TranscriptStore(tmp_path)
    store.append("lazynmap", "22/tcp open ssh\n80/tcp open http\n")
    store.append("gobuster", "/admin (Status: 200)\n/login (Status: 302)\n")
    matches = store.grep(r"open\s+ssh")
    assert matches and matches[0]["command"] == "lazynmap"


def test_transcript_grep_command_filter(tmp_path):
    store = TranscriptStore(tmp_path)
    store.append("lazynmap", "admin: ignored\n")
    store.append("gobuster", "found admin path\n")
    matches = store.grep("admin", command_filter="gobuster")
    assert all(m["command"] == "gobuster" for m in matches)


def test_transcript_grep_invalid_regex(tmp_path):
    store = TranscriptStore(tmp_path)
    store.append("x", "y")
    out = store.grep("(unbalanced")
    assert out and "error" in out[0]


def test_transcript_persists_and_reloads(tmp_path):
    store_a = TranscriptStore(tmp_path)
    store_a.append("foo", "hello world")
    store_b = TranscriptStore(tmp_path)
    listed = store_b.list(limit=5)
    assert listed and listed[0]["command"] == "foo"


def test_transcript_capacity(tmp_path):
    store = TranscriptStore(tmp_path, capacity=3)
    for i in range(10):
        store.append(f"cmd{i}", f"out{i}")
    listed = store.list(limit=10)
    assert len(listed) == 3
    assert listed[0]["command"] == "cmd9"


# ── InteractiveForm ─────────────────────────────────────────────────────────

class FakeIO:
    def __init__(self, replies: list[str]) -> None:
        self.replies = list(replies)
        self.emitted: list[str] = []

    def prompt(self, message: str, default: str = "") -> str:
        if not self.replies:
            return default
        return self.replies.pop(0)

    def emit(self, line: str) -> None:
        self.emitted.append(line)


def test_form_collects_values_with_defaults():
    spec = FormSpec(
        command="venom",
        fields=(
            FormField("payload", "msfvenom payload", required=True,
                      default="windows/x64/meterpreter/reverse_tcp"),
            FormField("lport", "port", default="4444"),
        ),
    )
    fake = FakeIO(replies=["", "9001"])  # accept default for first, override second
    out = InteractiveForm(io=fake).render(spec)
    assert out["payload"] == "windows/x64/meterpreter/reverse_tcp"
    assert out["lport"] == "9001"


def test_form_options_constraint_falls_back_to_default():
    spec = FormSpec(
        command="x",
        fields=(
            FormField("ssl", "use ssl", default="false",
                      options=("true", "false")),
        ),
    )
    fake = FakeIO(replies=["maybe"])
    out = InteractiveForm(io=fake).render(spec)
    assert out["ssl"] == "false"
    assert any("not in allowed options" in line for line in fake.emitted)


def test_form_required_reprompted():
    spec = FormSpec(
        command="x",
        fields=(FormField("token", "token", required=True),),
    )
    fake = FakeIO(replies=["", "abc123"])
    out = InteractiveForm(io=fake).render(spec)
    assert out["token"] == "abc123"


# ── commands_from_cmd2_shell ────────────────────────────────────────────────

class _ShellLike:
    aliases = {"nmap": "lazynmap"}

    def do_lazynmap(self, _):
        """Full TCP/UDP nmap with vuln scripts."""

    def do_gobuster(self, _):
        """Directory brute-force."""


def test_commands_from_cmd2_shell_extracts_doc_and_aliases():
    out = commands_from_cmd2_shell(_ShellLike())
    by_name = {c.name: c for c in out}
    assert "lazynmap" in by_name
    assert "gobuster" in by_name
    assert by_name["lazynmap"].summary.startswith("Full TCP/UDP")
    assert "nmap" in by_name["lazynmap"].aliases


# ── Audit CommandSet smoke (without full cmd2 boot) ─────────────────────────

class _MiniShell:
    """Just enough cmd2 surface to instantiate AuditCommandSet helpers."""

    def __init__(self, tmp: Path) -> None:
        self.params = {"rhost": "10.10.11.5", "domain": "target.htb",
                       "dirwordlist": "/usr/share/wordlists/dl.txt"}
        self.aliases = {"nmap": "lazynmap"}
        self.sessions_dir = str(tmp / "sessions")
        self.lazyaddons_dir = str(tmp / "lazyaddons")
        self.plugins_dir = str(tmp / "plugins")
        Path(self.sessions_dir).mkdir(exist_ok=True)
        Path(self.lazyaddons_dir).mkdir(exist_ok=True)
        Path(self.plugins_dir).mkdir(exist_ok=True)
        self.outputs: list[str] = []
        self.last_result = None

    def poutput(self, msg: str) -> None:
        self.outputs.append(str(msg))

    def get_all_commands(self):
        return ["lazynmap", "gobuster"]

    def do_lazynmap(self, _):
        """nmap vuln scan"""

    def do_gobuster(self, _):
        """dir brute"""


def test_audit_fz_command_emits_results(tmp_path):
    from cli.commands.audit import AuditCommandSet

    cs = AuditCommandSet()
    cs._CommandSet__cmd_internal = _MiniShell(tmp_path)
    cs.do_fz("nmap")
    out = "\n".join(cs._cmd.outputs)
    assert "lazynmap" in out


def test_audit_status_tail_reports_no_evidence(tmp_path):
    from cli.commands.audit import AuditCommandSet

    cs = AuditCommandSet()
    cs._CommandSet__cmd_internal = _MiniShell(tmp_path)
    cs.do_status_tail("")
    out = "\n".join(cs._cmd.outputs)
    assert "no scan output" in out


def test_audit_grep_log_handles_empty_store(tmp_path):
    from cli.commands.audit import AuditCommandSet

    cs = AuditCommandSet()
    cs._CommandSet__cmd_internal = _MiniShell(tmp_path)
    cs.do_grep_log("admin")
    out = "\n".join(cs._cmd.outputs)
    assert "no matches" in out


def test_audit_form_unknown_lists_known(tmp_path):
    from cli.commands.audit import AuditCommandSet

    cs = AuditCommandSet()
    cs._CommandSet__cmd_internal = _MiniShell(tmp_path)
    cs.do_form("totally_unknown_command")
    out = "\n".join(cs._cmd.outputs)
    assert "no form" in out
