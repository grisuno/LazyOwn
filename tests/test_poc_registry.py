"""PoC verb registry contract tests.

The catalogued PoC scripts (``modules/49803.py``, ``CVE-2023-28432.py``,
...) become loop-routable verbs whose arguments render from
``payload.json`` placeholders: these tests lock the rendering, the
trigger-matched proposals and the selector wiring that makes the PoCs
reachable from auto_loop and apt_chain.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from modules import poc_registry
from modules.selection.base import SelectionContext
from modules.selection.poc import PoCSelector

CATALOG = Path("config/poc_verbs.yaml")


class TestCatalog:
    """The shipped catalog parses into typed verbs."""

    def test_catalog_loads_every_declared_poc(self):
        verbs = poc_registry.poc_verbs()
        raw = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))["pocs"]
        assert set(verbs) == {name.lower() for name in raw}

    def test_every_verb_has_script_and_interpreter(self):
        for verb in poc_registry.poc_verbs().values():
            assert verb.script
            assert verb.interpreter in poc_registry.INTERPRETERS
            assert (Path("modules") / verb.script).is_file(), verb.script

    def test_unknown_verb_is_none(self):
        assert poc_registry.get_poc("no_such_poc") is None


class TestRendering:
    """Placeholder rendering resolves payload, target and overrides."""

    def test_minio_renders_url_from_target_and_override(self):
        verb = poc_registry.get_poc("minio_info")
        rendered = poc_registry.render_argv(
            verb, {"rhost": "10.0.0.9", "rport": "443"}, target="10.10.11.5", overrides={"rport": "9000"}
        )
        assert rendered.argv[-2:] == ("--url", "http://10.10.11.5:9000")
        assert rendered.missing == ()

    def test_openplc_renders_all_five_placeholders(self):
        verb = poc_registry.get_poc("openplc_rce")
        params = {
            "rhost": "10.10.11.5",
            "rport": "8080",
            "lhost": "10.9.9.9",
            "lport": "4444",
            "username": "openplc",
            "password": "secret",
        }
        rendered = poc_registry.render_argv(verb, params)
        assert "-u" in rendered.argv and "http://10.10.11.5:8080" in rendered.argv
        assert "-l" in rendered.argv and "openplc" in rendered.argv
        assert "-p" in rendered.argv and "secret" in rendered.argv
        assert "-i" in rendered.argv and "10.9.9.9" in rendered.argv
        assert "-r" in rendered.argv and "4444" in rendered.argv
        assert rendered.resolved.get("password") == "***"

    def test_unresolved_placeholder_without_default_is_refused(self):
        verb = poc_registry.get_poc("minio_info")
        rendered = poc_registry.render_argv(verb, {})
        assert "rhost" in rendered.missing
        assert "--url" not in rendered.argv

    def test_default_applies_when_placeholder_unresolved(self):
        verb = poc_registry.get_poc("libreoffice_uno")
        rendered = poc_registry.render_argv(verb, {}, target="10.10.11.5")
        assert ("--port", "2002") in zip(rendered.argv, rendered.argv[1:])
        assert rendered.missing == ()

    def test_mitmdump_addon_form(self):
        verb = poc_registry.get_poc("amt_auth_bypass")
        rendered = poc_registry.render_argv(verb, {})
        assert rendered.argv[0] == "mitmdump"
        assert rendered.argv[1] == "-s"
        assert rendered.argv[2].endswith("amt_auth_bypass.py")

    def test_positional_php_args_render(self):
        verb = poc_registry.get_poc("laravel_rce")
        rendered = poc_registry.render_argv(verb, {}, overrides={"app_key": "b64key", "payload": "O:8:..."})
        assert rendered.argv[-2:] == ("b64key", "O:8:...")
        assert rendered.missing == ()


class TestProposals:
    """Trigger matching produces runnable intent lines."""

    def test_minio_service_proposes_intent_with_port_override(self):
        lines = poc_registry.propose_intents(["10.10.11.5:9000 minio http"], "10.10.11.5")
        assert lines == ["lazy_poc run minio_info 10.10.11.5 rport=9000"]

    def test_non_matching_service_yields_nothing(self):
        assert poc_registry.propose_intents(["https alt-svc h2"], "10.10.11.5") == []

    def test_disabled_verb_is_never_proposed(self, tmp_path):
        raw = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
        raw["pocs"]["minio_info"]["enabled"] = False
        alt = tmp_path / "poc_verbs.yaml"
        alt.write_text(yaml.safe_dump(raw), encoding="utf-8")
        assert poc_registry.propose_intents(["minio"], "10.10.11.5", catalog_path=alt) == []


class TestPoCSelector:
    """The shared selector proposes PoC runs for matching services."""

    def _ctx(self, target="10.10.11.5", services=("minio", "http"), exclude=()):
        return SelectionContext(target=target, services=services, exclude=frozenset(exclude))

    def test_selector_proposes_minio_verb(self):
        decision = PoCSelector().propose(self._ctx())
        assert decision is not None
        assert decision.command == "lazy_poc run minio_info 10.10.11.5 rport=9000"
        assert decision.source == "poc"

    def test_selector_excludes_already_proposed_verb(self):
        decision = PoCSelector().propose(
            self._ctx(exclude=("lazy_poc run minio_info 10.10.11.5 rport=9000",))
        )
        assert decision is None

    def test_selector_abstains_without_target(self):
        assert PoCSelector().propose(SelectionContext(target="", services=("minio",))) is None

    def test_selector_in_default_cascade(self):
        from modules.selection import all_selectors

        names = [selector.name for selector in all_selectors()]
        assert "poc" in names


class TestRouting:
    """The loop routing surface recognises lazy_poc lines."""

    def test_lazy_poc_is_routable(self):
        from modules.auto_registry import is_routable_command

        assert is_routable_command("lazy_poc run minio_info 10.10.11.5 rport=9000")

    def test_auto_poc_verb_builds_run_line(self):
        from modules.auto_registry import steps_for

        steps = steps_for("auto poc:minio_info 10.10.11.5")
        assert steps == ["lazy_poc run minio_info 10.10.11.5"]

    def test_auto_poc_unknown_verb_is_none(self):
        from modules.auto_registry import steps_for

        assert steps_for("auto poc:no_such_poc 10.10.11.5") is None

    def test_target_extraction_from_lazy_poc_line(self):
        from modules.auto_registry import auto_verb_target

        line = "lazy_poc run minio_info 10.10.11.5 rport=9000"
        assert auto_verb_target(line) == "10.10.11.5"
        assert auto_verb_target("lazy_poc run minio_info rport=9000") == ""


class TestVerbCatalogSurfaces:
    """PoC verbs appear in the operator catalog as poc:<name>."""

    def test_poc_pseudo_verbs_in_discoveries(self, tmp_path):
        import modules.verb_catalog as vc

        cfg = vc.VerbCatalogConfig(
            catalog_path=tmp_path / "verbs.yaml",
            index_path=tmp_path / "index.json",
            addons_dir=None,
            poc_catalog_path=Path("config/poc_verbs.yaml"),
        )
        rows = vc._poc_discoveries(cfg)
        assert "poc:minio_info" in rows
        assert rows["poc:minio_info"]["phase"] == "exploit"

    def test_sandbox_config_has_no_poc_discoveries(self, tmp_path):
        import modules.verb_catalog as vc

        cfg = vc.VerbCatalogConfig(
            catalog_path=tmp_path / "verbs.yaml",
            index_path=tmp_path / "index.json",
            addons_dir=None,
        )
        assert vc._poc_discoveries(cfg) == {}
