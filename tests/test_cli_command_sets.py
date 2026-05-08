"""``cli`` package declarativeness and ``CommandSet`` registration tests.

Validate the ``cli/`` package layout, the YAML-driven aliases loader and the
``CommandSet`` registry so ``lazyown.py`` no longer needs an inline aliases
dict yet preserves every legacy alias name and substitution.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
LAZYOWN_PATH = REPO_ROOT / "lazyown.py"
ALIASES_YAML = REPO_ROOT / "cli" / "aliases.yaml"


@pytest.fixture(scope="module", autouse=True)
def _add_repo_root_to_syspath() -> None:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))


def _load_yaml() -> dict[str, str]:
    with ALIASES_YAML.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _legacy_alias_keys_from_lazyown() -> set[str]:
    """Snapshot of the historical aliases dict keys.

    The inline dict in ``lazyown.py`` was replaced by a YAML-driven loader.
    This snapshot is embedded so the test does not depend on git or the
    previous file revision.
    """
    return {
        "amnesiac",
        "aslr",
        "asm",
        "atomic_update",
        "auto",
        "autonuclei",
        "available_filter_functions",
        "available_filter_functions_addrs",
        "available_filter_functions_addrs_debug",
        "available_filter_functions_debug",
        "backdoor",
        "beef_payload",
        "bettercap_netrecon",
        "caja",
        "cc",
        "chown",
        "cloudflare_tunnel",
        "coerce_plus",
        "control_dynamic_debug",
        "creds",
        "diable_selinux",
        "disable_apparmor",
        "disable_aslr",
        "disable_ftrace",
        "disable_ftrace_proc",
        "discovery",
        "dolphin",
        "duckdns",
        "ed",
        "empire_client",
        "empire_server",
        "enable_aslr",
        "enabled_ftrace",
        "enabled_functions",
        "enabled_functions_debug",
        "enabled_search_by_hidden_pids",
        "event_trace",
        "ftpd",
        "ftpsniff",
        "gdb",
        "get_all_domains",
        "halt",
        "hash",
        "hosts",
        "hosts_discover",
        "iasniff",
        "info",
        "install_shark",
        "ipy",
        "kallsyms",
        "kvpn",
        "loot",
        "ls",
        "lsof",
        "man",
        "mitre_update",
        "moo",
        "nf",
        "nmap",
        "nmap_ldap_rootdse",
        "nmcli",
        "notes",
        "now",
        "ntlmrelayx",
        "ntp",
        "ntp_rhost",
        "nxcridbrute",
        "p",
        "pass",
        "poison",
        "powersploit",
        "pwnat",
        "py",
        "q",
        "qq",
        "randomuser",
        "report",
        "rtpflood",
        "rustrevmakerlin",
        "rustrevmakerwin",
        "s3_annon_enum_aws",
        "s3_annon_sync_aws",
        "ses",
        "showmount",
        "smbd",
        "sniff",
        "spiderfoot",
        "sshr",
        "start_apt",
        "start_ntp",
        "start_ollama",
        "start_squid",
        "status",
        "stop_apt",
        "stop_ntp",
        "stop_ollama",
        "stop_squid",
        "stop_tor",
        "t",
        "tcpdump",
        "tcpdumpl",
        "tcpdumpt",
        "tor",
        "touched_functions",
        "trace",
        "unshadow",
        "update",
        "venom",
        "vmallocinfo",
        "vuln",
        "word",
        "wps",
        "ww",
        "zrc",
    }


class TestAliasYamlIntegrity:
    def test_yaml_loads(self):
        data = _load_yaml()
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_yaml_keys_match_legacy_set(self):
        yaml_keys = set(_load_yaml().keys())
        legacy = _legacy_alias_keys_from_lazyown()
        missing = legacy - yaml_keys
        extra = yaml_keys - legacy
        assert missing == set(), f"YAML lost legacy aliases: {sorted(missing)}"
        assert extra == set(), f"YAML introduced unknown aliases: {sorted(extra)}"

    def test_yaml_count_is_114(self):
        assert len(_load_yaml()) == 114

    def test_all_values_are_strings(self):
        for name, value in _load_yaml().items():
            assert isinstance(value, str), f"alias {name} must be a string, got {type(value).__name__}"

    def test_vuln_alias_carries_ansi_escape(self):
        assert "\x1b[33m" in _load_yaml()["vuln"]

    def test_ls_is_unchanged(self):
        assert _load_yaml()["ls"] == "list"

    def test_q_is_exit(self):
        assert _load_yaml()["q"] == "exit"


class TestAliasLoaderSubstitution:
    def test_load_aliases_substitutes_payload_values(self):
        from cli.aliases import load_aliases

        payload = {
            "rhost": "10.0.0.5",
            "lhost": "10.0.0.1",
            "lport": 9999,
            "c2_port": 4444,
            "domain": "example.htb",
            "api_key": "test-key",
            "device": "tun0",
            "start_user": "alice",
            "start_pass": "s3cr3t",
        }
        aliases = load_aliases(payload)
        assert "10.0.0.5" in aliases["backdoor"]
        assert "{rhost}" not in aliases["backdoor"]
        assert "alice" in aliases["coerce_plus"]
        assert "s3cr3t" in aliases["coerce_plus"]
        assert "10.0.0.1" in aliases["coerce_plus"]
        assert "example.htb" in aliases["coerce_plus"]

    def test_missing_keys_substitute_to_empty_string(self):
        from cli.aliases import load_aliases

        aliases = load_aliases({"rhost": "1.2.3.4"})
        assert "{lhost}" not in aliases["coerce_plus"]
        assert "1.2.3.4" in aliases["coerce_plus"]

    def test_none_values_substitute_to_empty_string(self):
        from cli.aliases import load_aliases

        aliases = load_aliases({"rhost": "1.2.3.4", "lhost": None})
        assert "{lhost}" not in aliases["backdoor"]

    def test_aliases_with_no_placeholders_unchanged(self):
        from cli.aliases import load_aliases

        aliases = load_aliases({"rhost": "x"})
        assert aliases["ls"] == "list"
        assert aliases["q"] == "exit"
        assert aliases["zrc"] == "sh nano ~/.zshrc"

    def test_loader_rejects_non_mapping(self, tmp_path):
        from cli.aliases import load_aliases

        bad = tmp_path / "bad.yaml"
        bad.write_text("- a\n- b\n", encoding="utf-8")
        with pytest.raises(TypeError):
            load_aliases({}, path=bad)

    def test_loader_rejects_non_string_value(self, tmp_path):
        from cli.aliases import load_aliases

        bad = tmp_path / "bad.yaml"
        bad.write_text("good_key: 42\n", encoding="utf-8")
        with pytest.raises(ValueError):
            load_aliases({}, path=bad)

    def test_loader_handles_empty_file(self, tmp_path):
        from cli.aliases import load_aliases

        empty = tmp_path / "empty.yaml"
        empty.write_text("", encoding="utf-8")
        assert load_aliases({}, path=empty) == {}

    def test_real_yaml_loads_with_real_payload(self):
        from cli.aliases import load_aliases
        from core.config import load_payload

        aliases = load_aliases(load_payload())
        assert len(aliases) == 114
        for name, command in aliases.items():
            assert "{rhost}" not in command, f"unsubstituted placeholder in {name}"
            assert "{lhost}" not in command, f"unsubstituted placeholder in {name}"
            assert "{lport}" not in command, f"unsubstituted placeholder in {name}"


class TestLazyOwnRefactor:
    @pytest.fixture(scope="class")
    def lazyown_text(self) -> str:
        return LAZYOWN_PATH.read_text(encoding="utf-8")

    def test_no_inline_aliases_dict_with_entries(self, lazyown_text):
        match = re.search(r"^    aliases\s*=\s*\{", lazyown_text, re.MULTILINE)
        if not match:
            return
        start = match.start()
        line_end = lazyown_text.index("\n", start)
        first_line = lazyown_text[start:line_end]
        assert first_line.endswith("{}"), f"lazyown.py still has multi-line inline aliases dict: {first_line!r}"

    def test_imports_cli_aliases_loader(self, lazyown_text):
        assert "from cli.aliases import load_aliases" in lazyown_text

    def test_imports_cli_registry(self, lazyown_text):
        assert "from cli.registry import register_command_sets" in lazyown_text

    def test_init_populates_aliases_at_runtime(self, lazyown_text):
        assert "self.aliases.update(" in lazyown_text

    def test_init_registers_command_sets(self, lazyown_text):
        assert "_register_command_sets(self)" in lazyown_text


class TestCommandSetDiscovery:
    def test_discovery_excludes_underscore_modules(self):
        from cli.registry import iter_command_sets

        names = [c.__name__ for c in iter_command_sets()]
        assert "LazyOwnCommandSet" not in names, "base class should be excluded from discovery"

    def test_discovers_diagnostics_pilot(self):
        from cli.registry import iter_command_sets

        names = [c.__name__ for c in iter_command_sets()]
        assert "DiagnosticsCommandSet" in names

    def test_pilot_commandset_subclasses_base(self):
        from cli.commands._base import LazyOwnCommandSet
        from cli.commands.diagnostics import DiagnosticsCommandSet

        assert issubclass(DiagnosticsCommandSet, LazyOwnCommandSet)

    def test_pilot_commandset_declares_phase(self):
        from cli.commands.diagnostics import DiagnosticsCommandSet

        assert DiagnosticsCommandSet.phase == "diagnostics"

    def test_pilot_commandset_has_do_methods(self):
        from cli.commands.diagnostics import DiagnosticsCommandSet

        do_methods = [m for m in dir(DiagnosticsCommandSet) if m.startswith("do_")]
        assert "do_lazy_runtime" in do_methods
        assert "do_lazy_payload_keys" in do_methods


class TestRegisterCommandSets:
    def test_registers_on_a_minimal_cmd2_instance(self):
        import cmd2

        from cli.registry import register_command_sets

        class _Bare(cmd2.Cmd):
            pass

        shell = _Bare()
        registered = register_command_sets(shell)
        assert any(c.__class__.__name__ == "DiagnosticsCommandSet" for c in registered)

    def test_register_skips_failing_commandset_without_aborting(self, monkeypatch):
        import cmd2

        from cli import registry

        class _ExplosiveCommandSet(cmd2.CommandSet):
            def __init__(self):
                raise RuntimeError("boom")

        def fake_iter():
            yield _ExplosiveCommandSet
            from cli.commands.diagnostics import DiagnosticsCommandSet

            yield DiagnosticsCommandSet

        monkeypatch.setattr(registry, "iter_command_sets", fake_iter)

        class _Bare(cmd2.Cmd):
            pass

        shell = _Bare()
        registered = registry.register_command_sets(shell)
        assert any(c.__class__.__name__ == "DiagnosticsCommandSet" for c in registered)


class TestLazyOwnStillParses:
    def test_ast_parse(self):
        ast.parse(LAZYOWN_PATH.read_text(encoding="utf-8"))
