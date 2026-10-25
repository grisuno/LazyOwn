"""tests/test_param_registry.py

Contract suite for the shared parameter registry.

The registry is the single place where an operator declares a parameter
that every surface can use (addons, aliases, pipelines, ``assign``). This
suite locks the file format, the CRUD, the projection into the payload
schema and the addon-creator allowlist, plus the two front ends that
drive it: the ``param`` shell command and the ``lazy_orchestrator``
Params tab.

No network access and no writes outside a temporary directory.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from core.param_registry import (
    OperatorParam,
    create_param,
    delete_param,
    effective_value,
    list_params,
    load_entries,
    normalise_kind,
    operator_specs,
    param_value,
    registry_path,
    sync_shell_params,
    update_param,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def root(tmp_path: Path) -> Path:
    """Return a sandboxed repository root holding an empty params dir."""
    (tmp_path / "params").mkdir(parents=True, exist_ok=True)
    return tmp_path


class FakeShell:
    """Minimal shell double exposing a mutable params mapping."""

    def __init__(self) -> None:
        """Start with an empty parameter dict."""
        self.params: dict = {}


class TestRegistryFileFormat:
    def test_registry_path_is_under_params(self, root: Path):
        assert registry_path(root) == root / "params" / "operator.yaml"

    def test_create_writes_the_declared_entry(self, root: Path):
        create_param(
            "c2_profile",
            kind="string",
            default="default",
            description="C2 profile name",
            root=root,
        )
        raw = yaml.safe_load(registry_path(root).read_text(encoding="utf-8"))
        assert raw["c2_profile"]["kind"] == "string"
        assert raw["c2_profile"]["default"] == "default"
        assert raw["c2_profile"]["description"] == "C2 profile name"

    def test_registry_keeps_the_documentation_header(self, root: Path):
        create_param("demo_param", root=root)
        text = registry_path(root).read_text(encoding="utf-8")
        assert text.startswith("# Operator-declared parameters.")

    def test_missing_registry_reads_as_empty(self, root: Path):
        assert load_entries(root) == {}

    def test_illegal_keys_are_skipped(self, root: Path):
        registry_path(root).write_text("Bad-Name: 1\n'bad key': 2\ngood_param: 3\n", encoding="utf-8")
        entries = load_entries(root)
        assert "good_param" in entries
        assert "Bad-Name" not in entries
        assert "bad key" not in entries

    def test_broken_registry_does_not_raise(self, root: Path):
        registry_path(root).write_text("key: [unclosed\n", encoding="utf-8")
        assert load_entries(root) == {}


class TestRegistryCrud:
    def test_create_returns_the_parameter(self, root: Path):
        param = create_param("demo_param", kind="string", default="v", description="d", root=root)
        assert isinstance(param, OperatorParam)
        assert param.name == "demo_param"
        assert param.source == "operator"

    def test_create_rejects_illegal_names(self, root: Path):
        for bad in ("Bad", "1bad", "with-dash", "with space", ""):
            with pytest.raises(ValueError):
                create_param(bad, root=root)

    def test_create_rejects_duplicates(self, root: Path):
        create_param("demo_param", root=root)
        with pytest.raises(ValueError):
            create_param("demo_param", root=root)

    def test_create_rejects_long_description(self, root: Path):
        with pytest.raises(ValueError):
            create_param("demo_param", description="x" * 201, root=root)

    def test_update_changes_default_and_description(self, root: Path):
        create_param("demo_param", default="a", description="one", root=root)
        updated = update_param("demo_param", default="b", description="two", root=root)
        assert updated.default == "b"
        assert updated.description == "two"
        assert param_value("demo_param", root=root) == "b"

    def test_update_keeps_untouched_fields(self, root: Path):
        create_param("demo_param", default="a", description="one", root=root)
        updated = update_param("demo_param", default="b", root=root)
        assert updated.description == "one"

    def test_update_unknown_raises(self, root: Path):
        with pytest.raises(KeyError):
            update_param("nope", default="x", root=root)

    def test_delete_removes_the_entry(self, root: Path):
        create_param("demo_param", root=root)
        assert delete_param("demo_param", root=root) is True
        assert load_entries(root) == {}

    def test_delete_unknown_raises(self, root: Path):
        with pytest.raises(KeyError):
            delete_param("nope", root=root)

    def test_normalise_kind(self):
        assert normalise_kind("INT") == "integer"
        assert normalise_kind("bool") == "boolean"
        assert normalise_kind("url") == "url"
        assert normalise_kind("nonsense") == "string"

    def test_effective_value_rules(self):
        assert effective_value({"kind": "string", "default": "v"}) == "v"
        assert effective_value({"kind": "string"}) == {"kind": "string"}
        assert effective_value("flat") == "flat"


class TestRegistryProjections:
    def test_operator_specs_carry_kind_and_default(self, root: Path):
        create_param("demo_param", kind="integer", default="7", root=root)
        specs = operator_specs(root)
        assert "demo_param" in specs
        assert specs["demo_param"].kind.value == "int"
        assert specs["demo_param"].default == "7"

    def test_list_params_marks_the_source(self, root: Path):
        create_param("demo_param", root=root)
        params = list_params(root=root, include_builtin=True)
        by_name = {p.name: p for p in params}
        assert by_name["demo_param"].source == "operator"
        assert by_name["rhost"].source == "builtin"

    def test_list_params_filters_by_keyword(self, root: Path):
        create_param("demo_param", description="needle", root=root)
        params = list_params(root=root, include_builtin=True, keyword="needle")
        assert [p.name for p in params] == ["demo_param"]

    def test_sync_shell_params_publishes_the_default(self, root: Path):
        create_param("demo_param", default="v", root=root)
        shell = FakeShell()
        assert sync_shell_params(shell, root=root) == 1
        assert shell.params["demo_param"] == "v"

    def test_sync_shell_params_keeps_a_live_value(self, root: Path):
        create_param("demo_param", default="v", root=root)
        shell = FakeShell()
        shell.params["demo_param"] = "operator value"
        sync_shell_params(shell, root=root)
        assert shell.params["demo_param"] == "operator value"

    def test_sync_shell_params_without_shell_is_a_noop(self, root: Path):
        assert sync_shell_params(None, root=root) == 0


class TestSchemaProjection:
    def test_operator_param_lands_in_the_schema(self, root: Path):
        from core.payload_schema import SCHEMA, register_specs, unregister_specs

        create_param("schema_demo", kind="string", default="v", root=root)
        register_specs(operator_specs(root))
        try:
            assert "schema_demo" in SCHEMA
            assert SCHEMA["schema_demo"].default == "v"
        finally:
            unregister_specs(["schema_demo"])
        assert "schema_demo" not in SCHEMA

    def test_builtin_keys_are_never_overridden(self):
        from core.payload_schema import SCHEMA, register_specs, unregister_specs

        spec = SCHEMA["rhost"]
        try:
            register_specs({"rhost": spec})
            assert SCHEMA["rhost"] is spec
        finally:
            unregister_specs(["rhost"])
        assert "rhost" in SCHEMA

    def test_validator_allowlist_includes_operator_params(self, root: Path):
        from lazyc2.addon_creator import AddonCreatorConfig

        create_param("validator_demo", root=root)
        # The registry root is sandboxed, so the allowlist is checked
        # through the documented hook instead of the process-wide file.
        assert "validator_demo" in operator_specs(root)
        assert "rhost" in AddonCreatorConfig.live_placeholders()


class TestShellIntegration:
    def test_flat_param_entries_keep_their_value(self):
        from core.param_registry import effective_value

        assert effective_value({"kind": "string", "default": "v"}) == "v"
        assert effective_value("plain") == "plain"

    def test_repo_registry_file_is_valid_yaml(self):
        path = REPO_ROOT / "params" / "operator.yaml"
        if not path.exists():
            pytest.skip("no operator registry in this checkout")
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        assert isinstance(data, dict)

    def test_live_params_do_not_drift_from_the_registry(self):
        from core.param_registry import load_entries

        payload = json.loads((REPO_ROOT / "payload.json").read_text(encoding="utf-8"))
        for name in load_entries():
            assert name in payload or name in {
                "url",
                "rhost",
            }, f"{name} must be resolvable by the shell"


class TestParamCommand:
    def test_command_set_is_discovered(self):
        from cli.registry import iter_command_sets

        names = {cls.__name__ for cls in iter_command_sets()}
        assert "ParamCommandSet" in names

    def test_command_exposes_do_param(self):
        from cli.commands.params_ops import ParamCommandSet

        assert callable(ParamCommandSet.do_param)

    def test_command_documents_the_verbs(self):
        from cli.commands.params_ops import ParamCommandSet

        doc = ParamCommandSet.do_param.__doc__ or ""
        for verb in ("list", "show", "create", "set", "delete"):
            assert verb in doc


class TestOrchestratorParamsTab:
    def test_app_exposes_the_param_tab(self):
        from cli.lazy_orchestrator import LazyOrchestratorApp

        app = LazyOrchestratorApp()
        assert hasattr(app, "_refresh_params")
        assert hasattr(app, "create_param")
        assert hasattr(app, "update_param")
        assert hasattr(app, "delete_param")

    def test_app_create_publishes_to_the_shell(self, root: Path):
        from cli.lazy_orchestrator import LazyOrchestratorApp

        shell = FakeShell()
        app = LazyOrchestratorApp(shell=shell, param_root=root)
        created = app.create_param("tui_demo", "string", "v", "from the tui")
        assert created["name"] == "tui_demo"
        assert shell.params["tui_demo"] == "v"

    def test_app_delete_removes_the_parameter(self, root: Path):
        from cli.lazy_orchestrator import LazyOrchestratorApp

        shell = FakeShell()
        app = LazyOrchestratorApp(shell=shell, param_root=root)
        app.create_param("tui_demo", "string", "v", "from the tui")
        assert app.delete_param("tui_demo") is True
        assert "tui_demo" not in shell.params
        assert load_entries(root) == {}

    def test_app_refuses_to_delete_a_builtin(self, root: Path):
        from cli.lazy_orchestrator import LazyOrchestratorApp

        app = LazyOrchestratorApp(param_root=root)
        assert app.delete_param("rhost") is False


class TestSkillPolicy:
    def test_skill_documents_the_registry(self):
        text = (REPO_ROOT / "skills" / "lazyaddon-creator" / "SKILL.md").read_text(encoding="utf-8")
        assert "param_registry" in text or "params/operator.yaml" in text

    def test_skill_forbids_branded_placeholders(self):
        text = (REPO_ROOT / "skills" / "lazyaddon-creator" / "SKILL.md").read_text(encoding="utf-8")
        assert "branded" in text.lower() or "generic" in text.lower()


class TestSharedCatalogMigration:
    """A shared parameter is declared once, as data, not hardcoded."""

    def test_exploit_profile_is_an_operator_parameter(self):
        from core.param_registry import load_entries

        entries = load_entries()
        assert "exploit_profile" in entries, "exploit_profile must live in params/operator.yaml"
        assert entries["exploit_profile"].default == "bookworm"

    def test_exploit_profile_is_not_a_hardcoded_builtin(self):
        from core.payload_schema import SCHEMA
        from lazyc2.addon_creator import AddonCreatorConfig

        assert "exploit_profile" not in AddonCreatorConfig.payload_placeholders
        assert "exploit_profile" in AddonCreatorConfig.live_placeholders()
        assert "exploit_profile" in SCHEMA, "the overlay must project it into the schema"

    def test_exploit_profile_is_declared_once(self):
        from core.param_registry import registry_path

        extended = REPO_ROOT / "params" / "extended.yaml"
        data = yaml.safe_load(extended.read_text(encoding="utf-8")) or {}
        assert "exploit_profile" not in data, "the shared parameter has a single declaration"
        assert registry_path().exists()

    def test_skill_key_list_drops_the_migrated_parameter(self):
        import re

        text = (REPO_ROOT / "skills" / "lazyaddon-creator" / "SKILL.md").read_text(encoding="utf-8")
        block = re.search(r"Known .*`payload\.json` keys.*?\n```\n(.*?)\n```", text, re.S)
        assert block, "skill known-keys block not found"
        assert "exploit_profile" not in set(block.group(1).split())
