"""Tests for the LazyAddon creator contract and C2 blueprint.

Covers the SDD contract in ``lazyc2/addon_creator.py`` and the Flask
blueprint in ``lazyc2/blueprints/addons.py``.

BDD scenarios:
    - Given a valid form, when validated and rendered, the document
      loads in the CLI loader schema and round-trips through the store
    - Given an invalid name, when validated, a name issue is reported
    - Given an unknown placeholder, when validated, a field issue is
      reported so the operator cannot ship a typo silently
    - Given a path traversal attempt, when saved, the store rejects it
    - Given a CSRF-less POST, when creating or deleting, the server
      answers 403
    - Given a form POST with the issued token, when creating, the file
      appears under the addons directory and the client is redirected
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml
from flask import Flask
from flask_login import LoginManager, UserMixin, current_user

from lazyc2.addon_creator import (
    AddonCreatorConfig,
    AddonDraft,
    AddonStore,
    AddonValidationError,
    AddonValidator,
    AddonYamlRenderer,
    ParamSpec,
    parse_addon_form,
)
from lazyc2.blueprints.addons import addons_bp

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "templates"


def _valid_draft() -> AddonDraft:
    """Return a draft that passes every validation rule."""
    return AddonDraft(
        name="web_enum",
        description="Enumerates directories and files on a web target.",
        author="LazyOwn",
        version="1.0",
        enabled=True,
        os="any",
        triggers=["http", "https"],
        category="02. Scanning & Enumeration",
        module_type="scanner",
        install_type="git",
        params=[
            ParamSpec(
                name="url",
                type="string",
                required=True,
                description="Target URL to enumerate.",
            ),
            ParamSpec(
                name="depth",
                type="integer",
                required=False,
                description="Recursion depth.",
                default="2",
            ),
        ],
        tool_name="gobuster",
        repo_url="https://github.com/example/gobuster",
        install_path="external/.exploit/gobuster",
        install_command="go build .",
        execute_command="./gobuster dir -u {url} -t {rhost} --depth {depth}",
        upload_file="payload.bin",
        remote_command="whoami",
        download_file="C:\\Users\\admin\\flags.txt",
        lazycommand="encodewinbase64 powershell -c 'whoami'",
        env=["LAZYOWN_AES_KEY: {aes_key}"],
    )


class TestConfig:
    """The config class must centralise every option, pattern, and limit."""

    def test_name_pattern_rejects_traversal(self) -> None:
        config = AddonCreatorConfig()
        assert config.name_pattern.fullmatch("../evil") is None
        assert config.name_pattern.fullmatch("a/b") is None
        assert config.name_pattern.fullmatch("VALID") is None
        assert config.name_pattern.fullmatch("ok_name") is not None

    def test_patterns_accept_canonical_values(self) -> None:
        config = AddonCreatorConfig()
        assert config.version_pattern.fullmatch("1.0")
        assert config.version_pattern.fullmatch("2.1.0")
        assert config.param_name_pattern.fullmatch("rhost")
        assert config.category_pattern.fullmatch("03. Exploitation")
        assert config.rel_path_pattern.fullmatch("external/.exploit/tool")
        assert config.env_pattern.fullmatch("KEY: value")

    def test_os_options_cover_mitre_platforms(self) -> None:
        config = AddonCreatorConfig()
        assert "any" in config.os_options
        assert "windows" in config.os_options
        assert "containers" in config.os_options

    def test_payload_placeholders_cover_core_keys(self) -> None:
        config = AddonCreatorConfig()
        for key in ("rhost", "lhost", "lport", "url", "domain", "wordlist", "aes_key"):
            assert key in config.payload_placeholders


class TestValidator:
    """BDD: validation guards the operator against mistakes."""

    def test_valid_draft_has_no_issues(self) -> None:
        draft = _valid_draft()
        issues = AddonValidator(draft).validate()
        assert issues == []

    def test_missing_name_reports_issue(self) -> None:
        draft = _valid_draft()
        draft.name = ""
        issues = AddonValidator(draft).validate()
        assert any(issue.field == "name" for issue in issues)

    def test_invalid_name_reports_issue(self) -> None:
        for bad_name in ("../evil", "UPPER", "with space", "1starts_digit"):
            draft = _valid_draft()
            draft.name = bad_name
            issues = AddonValidator(draft).validate()
            assert any(issue.field == "name" for issue in issues), bad_name

    def test_missing_description_reports_issue(self) -> None:
        draft = _valid_draft()
        draft.description = "   "
        issues = AddonValidator(draft).validate()
        assert any(issue.field == "description" for issue in issues)

    def test_unknown_os_reports_issue(self) -> None:
        draft = _valid_draft()
        draft.os = "toaster"
        issues = AddonValidator(draft).validate()
        assert any(issue.field == "os" for issue in issues)

    def test_unknown_module_type_reports_issue(self) -> None:
        draft = _valid_draft()
        draft.module_type = "laser"
        issues = AddonValidator(draft).validate()
        assert any(issue.field == "module_type" for issue in issues)

    def test_malformed_category_reports_issue(self) -> None:
        draft = _valid_draft()
        draft.category = "Exploitation"
        issues = AddonValidator(draft).validate()
        assert any(issue.field == "category" for issue in issues)

    def test_uppercase_trigger_reports_issue(self) -> None:
        draft = _valid_draft()
        draft.triggers = ["HTTP"]
        issues = AddonValidator(draft).validate()
        assert any(issue.field == "trigger" for issue in issues)

    def test_missing_execute_command_reports_issue(self) -> None:
        draft = _valid_draft()
        draft.execute_command = "  "
        issues = AddonValidator(draft).validate()
        assert any(issue.field == "execute_command" for issue in issues)

    def test_unknown_placeholder_reports_issue(self) -> None:
        draft = _valid_draft()
        draft.execute_command = "tool -t {typo_token}"
        issues = AddonValidator(draft).validate()
        assert any(issue.field == "execute_command" and "typo_token" in issue.message for issue in issues)

    def test_nested_brace_placeholder_reports_issue(self) -> None:
        draft = _valid_draft()
        draft.execute_command = "tool {{ url }}"
        issues = AddonValidator(draft).validate()
        assert any(issue.field == "execute_command" for issue in issues)

    def test_declared_param_placeholder_is_allowed(self) -> None:
        draft = _valid_draft()
        draft.execute_command = "tool --url {url} --depth {depth}"
        issues = AddonValidator(draft).validate()
        assert not any(issue.field == "execute_command" for issue in issues)

    def test_install_path_without_repo_url_reports_issue(self) -> None:
        draft = _valid_draft()
        draft.repo_url = ""
        issues = AddonValidator(draft).validate()
        assert any(issue.field == "repo_url" for issue in issues)

    def test_traversal_install_path_reports_issue(self) -> None:
        for bad_path in ("../../etc", "..", "external/../sessions"):
            draft = _valid_draft()
            draft.install_path = bad_path
            issues = AddonValidator(draft).validate()
            assert any(issue.field == "install_path" for issue in issues), bad_path

    def test_bad_repo_url_reports_issue(self) -> None:
        for bad_url in ("javascript:alert(1)", "not-a-url", "ftp://host/x"):
            draft = _valid_draft()
            draft.repo_url = bad_url
            issues = AddonValidator(draft).validate()
            assert any(issue.field == "repo_url" for issue in issues), bad_url

    def test_duplicate_param_reports_issue(self) -> None:
        draft = _valid_draft()
        draft.params.append(ParamSpec(name="url", type="string", required=False, description="Again."))
        issues = AddonValidator(draft).validate()
        assert any(issue.field == "params" and "Duplicate" in issue.message for issue in issues)

    def test_param_without_description_reports_issue(self) -> None:
        draft = _valid_draft()
        draft.params.append(ParamSpec(name="bare", type="string", required=False, description=""))
        issues = AddonValidator(draft).validate()
        assert any(issue.field == "params" and "description" in issue.message for issue in issues)

    def test_integer_default_must_parse(self) -> None:
        draft = _valid_draft()
        draft.params.append(
            ParamSpec(name="count", type="integer", required=False, description="How many.", default="many")
        )
        issues = AddonValidator(draft).validate()
        assert any(issue.field == "params" and "integer" in issue.message for issue in issues)

    def test_boolean_default_whitelist(self) -> None:
        draft = _valid_draft()
        draft.params.append(
            ParamSpec(name="verbose", type="boolean", required=False, description="Verbose.", default="maybe")
        )
        issues = AddonValidator(draft).validate()
        assert any(issue.field == "params" and "true" in issue.message for issue in issues)

    def test_too_many_params_reports_issue(self) -> None:
        draft = _valid_draft()
        draft.params = [
            ParamSpec(name=f"p{index}", type="string", required=False, description="Extra.")
            for index in range(AddonCreatorConfig.max_params + 1)
        ]
        issues = AddonValidator(draft).validate()
        assert any(issue.field == "params" for issue in issues)

    def test_malformed_env_entry_reports_issue(self) -> None:
        draft = _valid_draft()
        draft.env = ["BROKEN NO COLON"]
        issues = AddonValidator(draft).validate()
        assert any(issue.field == "env" for issue in issues)

    def test_validation_error_carries_issues(self) -> None:
        draft = _valid_draft()
        draft.name = ""
        error = AddonValidationError(AddonValidator(draft).validate())
        assert error.issues
        assert "name" in str(error)


class TestYamlRenderer:
    """BDD: the rendered document satisfies the CLI loader schema."""

    def test_rendered_document_is_canonical(self) -> None:
        draft = _valid_draft()
        document = AddonYamlRenderer().to_document(draft)
        assert document["name"] == "web_enum"
        assert document["enabled"] is True
        assert document["os"] == "any"
        assert document["trigger"] == ["http", "https"]
        assert document["category"] == "02. Scanning & Enumeration"
        assert document["module_type"] == "scanner"
        assert document["install_type"] == "git"
        assert document["tool"]["repo_url"] == "https://github.com/example/gobuster"
        assert document["tool"]["install_path"] == "external/.exploit/gobuster"
        assert document["tool"]["install_command"] == "go build ."
        assert document["tool"]["execute_command"] == "./gobuster dir -u {url} -t {rhost} --depth {depth}"
        assert document["tool"]["upload_file"] == "payload.bin"
        assert document["tool"]["remote_command"] == "whoami"
        assert document["tool"]["download_file"] == "C:\\Users\\admin\\flags.txt"
        assert document["tool"]["env"] == ["LAZYOWN_AES_KEY: {aes_key}"]
        assert [param["name"] for param in document["params"]] == ["url", "depth"]

    def test_yaml_round_trips_through_loader(self) -> None:
        draft = _valid_draft()
        text = AddonYamlRenderer().render(draft)
        data = yaml.safe_load(text)
        assert isinstance(data, dict)
        assert data["name"] == draft.name
        assert data["tool"]["execute_command"] == draft.execute_command
        assert data["params"][0]["required"] is True

    def test_optional_fields_are_dropped(self) -> None:
        draft = AddonDraft(
            name="bare_tool",
            description="Minimal tool.",
            version="1.0",
            category="03. Exploitation",
            execute_command="tool",
        )
        document = AddonYamlRenderer().to_document(draft)
        assert "module_type" not in document
        assert "install_type" not in document
        assert "trigger" not in document
        assert "repo_url" not in document["tool"]
        assert "params" not in document

    def test_rendered_yaml_has_no_none_values(self) -> None:
        text = AddonYamlRenderer().render(_valid_draft())
        assert "null" not in text
        assert "None" not in text

    def test_default_author_and_version_applied(self) -> None:
        draft = AddonDraft(
            name="tool_x",
            description="Tool.",
            version="",
            category="01. Reconnaissance",
            execute_command="tool",
        )
        document = AddonYamlRenderer().to_document(draft)
        assert document["author"] == AddonCreatorConfig.default_author
        assert document["version"] == AddonCreatorConfig.default_version


class TestAddonStore:
    """BDD: persistence is path-safe, atomic, and idempotent."""

    def test_save_load_delete_round_trip(self, tmp_path: Path) -> None:
        store = AddonStore(base_dir=str(tmp_path))
        path = store.save("web_enum", "name: web_enum\nenabled: true\n")
        assert path.is_file()
        assert store.exists("web_enum")
        document = store.load("web_enum")
        assert document["name"] == "web_enum"
        assert store.delete("web_enum") is True
        assert store.exists("web_enum") is False
        assert store.delete("web_enum") is False

    def test_traversal_name_rejected_on_save(self, tmp_path: Path) -> None:
        store = AddonStore(base_dir=str(tmp_path))
        with pytest.raises(AddonValidationError):
            store.save("../../etc/passwd", "x: 1\n")

    def test_traversal_name_rejected_on_load(self, tmp_path: Path) -> None:
        store = AddonStore(base_dir=str(tmp_path))
        with pytest.raises(AddonValidationError):
            store.load("../sessions/world_model")

    def test_traversal_name_rejected_on_delete(self, tmp_path: Path) -> None:
        store = AddonStore(base_dir=str(tmp_path))
        with pytest.raises(AddonValidationError):
            store.delete("..")

    def test_save_is_atomic_and_leaves_no_temp_files(self, tmp_path: Path) -> None:
        store = AddonStore(base_dir=str(tmp_path))
        store.save("atomic_tool", "name: atomic_tool\n")
        leftovers = list(tmp_path.glob("*.tmp"))
        assert leftovers == []

    def test_save_overwrites_cleanly(self, tmp_path: Path) -> None:
        store = AddonStore(base_dir=str(tmp_path))
        store.save("same_name", "name: v1\n")
        store.save("same_name", "name: v2\n")
        assert store.load("same_name")["name"] == "v2"

    def test_load_missing_raises_file_not_found(self, tmp_path: Path) -> None:
        store = AddonStore(base_dir=str(tmp_path))
        with pytest.raises(FileNotFoundError):
            store.load("ghost_tool")

    def test_list_all_skips_broken_files(self, tmp_path: Path) -> None:
        store = AddonStore(base_dir=str(tmp_path))
        store.save("good_tool", "name: good_tool\nenabled: true\ndescription: ok\n")
        (tmp_path / "broken.yaml").write_text(": : : : not yaml", encoding="utf-8")
        summaries = store.list_all()
        names = [item["name"] for item in summaries]
        assert "good_tool" in names
        assert "broken" not in names

    def test_list_all_is_sorted_and_has_expected_keys(self, tmp_path: Path) -> None:
        store = AddonStore(base_dir=str(tmp_path))
        store.save("zeta_tool", "name: zeta_tool\nenabled: false\n")
        store.save("alpha_tool", "name: alpha_tool\nenabled: true\n")
        summaries = store.list_all()
        assert [item["name"] for item in summaries] == ["alpha_tool", "zeta_tool"]
        assert summaries[0]["enabled"] is True
        assert set(summaries[0]) == {
            "name",
            "filename",
            "description",
            "category",
            "author",
            "os",
            "enabled",
        }

    def test_list_all_reports_file_stem_as_filename(self, tmp_path: Path) -> None:
        (tmp_path / "AdaptixC2.yaml").write_text("name: adaptixc2\nenabled: true\n", encoding="utf-8")
        store = AddonStore(base_dir=str(tmp_path))
        summaries = store.list_all()
        assert summaries[0]["name"] == "adaptixc2"
        assert summaries[0]["filename"] == "AdaptixC2"

    def test_load_accepts_pre_existing_uppercase_names(self, tmp_path: Path) -> None:
        (tmp_path / "AdaptixC2.yaml").write_text("name: AdaptixC2\nenabled: true\ndescription: C2\n", encoding="utf-8")
        store = AddonStore(base_dir=str(tmp_path))
        document = store.load("AdaptixC2")
        assert document["name"] == "AdaptixC2"

    def test_load_accepts_pre_existing_dots_and_hyphens(self, tmp_path: Path) -> None:
        (tmp_path / "copy-fail-CVE-2026-31431.yaml").write_text("name: copy-fail\nenabled: false\n", encoding="utf-8")
        store = AddonStore(base_dir=str(tmp_path))
        assert store.load("copy-fail-CVE-2026-31431")["name"] == "copy-fail"
        assert store.delete("copy-fail-CVE-2026-31431") is True

    def test_load_still_rejects_traversal_through_existing_path(self, tmp_path: Path) -> None:
        store = AddonStore(base_dir=str(tmp_path))
        for bad_name in ("../etc/passwd", "..", "a/b", "..yaml"):
            with pytest.raises(AddonValidationError):
                store.load(bad_name)

    def test_delete_rejects_unsafe_existing_names(self, tmp_path: Path) -> None:
        store = AddonStore(base_dir=str(tmp_path))
        with pytest.raises(AddonValidationError):
            store.delete("../outside")

    def test_missing_directory_lists_empty(self, tmp_path: Path) -> None:
        store = AddonStore(base_dir=str(tmp_path / "does" / "not" / "exist"))
        assert store.list_all() == []

    def test_exists_swallows_invalid_names(self, tmp_path: Path) -> None:
        store = AddonStore(base_dir=str(tmp_path))
        assert store.exists("../../etc") is False

    def test_symlink_escape_rejected_on_load(self, tmp_path: Path) -> None:
        store_dir = tmp_path / "addons"
        store_dir.mkdir()
        outside = tmp_path / "outside.txt"
        outside.write_text("secret: value\n", encoding="utf-8")
        (store_dir / "evil.yaml").symlink_to(outside)
        store = AddonStore(base_dir=str(store_dir))
        with pytest.raises(AddonValidationError):
            store.load("evil")

    def test_symlink_escape_rejected_on_delete(self, tmp_path: Path) -> None:
        store_dir = tmp_path / "addons"
        store_dir.mkdir()
        outside = tmp_path / "outside.txt"
        outside.write_text("keep me", encoding="utf-8")
        (store_dir / "evil.yaml").symlink_to(outside)
        store = AddonStore(base_dir=str(store_dir))
        with pytest.raises(AddonValidationError):
            store.delete("evil")
        assert outside.exists()


class TestParseAddonForm:
    """BDD: raw form data becomes a draft with correct semantics."""

    def test_parse_complete_form(self) -> None:
        form = {
            "name": "web_enum",
            "description": "Enumerates web targets.",
            "author": "LazyOwn",
            "version": "1.0",
            "enabled": "true",
            "os": "any",
            "trigger": ["http", "https"],
            "category": "02. Scanning & Enumeration",
            "module_type": "scanner",
            "install_type": "git",
            "tool_name": "gobuster",
            "repo_url": "https://github.com/example/gobuster",
            "install_path": "external/.exploit/gobuster",
            "install_command": "go build .",
            "execute_command": "./gobuster dir -u {url}",
            "upload_file": "payload.bin",
            "remote_command": "whoami",
            "download_file": "out.txt",
            "lazycommand": "whoami",
            "env": "KEY: value\nOTHER: 1\n",
            "params-0-name": "url",
            "params-0-type": "string",
            "params-0-required": "true",
            "params-0-description": "Target URL.",
            "params-0-default": "",
            "params-1-name": "depth",
            "params-1-type": "integer",
            "params-1-description": "Depth.",
        }
        draft = parse_addon_form(form)
        assert draft.name == "web_enum"
        assert draft.enabled is True
        assert draft.triggers == ["http", "https"]
        assert draft.env == ["KEY: value", "OTHER: 1"]
        assert len(draft.params) == 2
        assert draft.params[0].name == "url"
        assert draft.params[0].required is True
        assert draft.params[1].required is False
        assert draft.params[1].default is None

    def test_unchecked_enabled_becomes_false(self) -> None:
        draft = parse_addon_form({"name": "x", "enabled": ""})
        assert draft.enabled is False

    def test_missing_optional_fields_become_empty(self) -> None:
        draft = parse_addon_form({"name": "x"})
        assert draft.description == ""
        assert draft.triggers == []
        assert draft.env == []
        assert draft.params == []

    def test_single_trigger_string_becomes_list(self) -> None:
        draft = parse_addon_form({"name": "x", "trigger": "http"})
        assert draft.triggers == ["http"]


def _build_test_app(tmp_path: Path) -> Flask:
    """Build a Flask test app with the addons blueprint registered.

    The base layout references many monolith endpoints; stub rules are
    registered so template rendering never depends on ``lazyc2.py``.
    Flask-Login is wired in so the session guard can be exercised.

    Args:
        tmp_path: The directory that receives addon files.

    Returns:
        A configured Flask application.
    """
    app = Flask(__name__, template_folder=str(TEMPLATES_DIR))
    app.config.update(
        SECRET_KEY="test-secret",
        TESTING=True,
        LAZYOWN_ADDONS_DIR=str(tmp_path),
        SESSION_COOKIE_SECURE=False,
        lhost="127.0.0.1",
    )
    stub_endpoints = (
        "index",
        "profile",
        "phishing.list_campaigns",
        "edit_notes",
        "get_event_config_view",
        "list_tools",
        "tasks",
        "cves",
        "report",
        "banners",
        "connect",
        "graph",
        "mitre",
        "palette_view",
        "lazyreport_view",
        "killchain_view",
        "login",
        "logout",
        "register",
    )
    for endpoint in stub_endpoints:
        app.add_url_rule(f"/__stub__/{endpoint}", endpoint=endpoint, view_func=lambda: "stub")

    class _FakeOperator(UserMixin):
        """Minimal Flask-Login user for session simulation."""

    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def _load_user(user_id: str):
        return _FakeOperator() if user_id == "1" else None

    app.context_processor(lambda: {"current_user": current_user})
    app.register_blueprint(addons_bp)
    return app


def _login(client: object) -> None:
    """Log the test client in through the Flask session."""
    with client.session_transaction() as session:
        session["_user_id"] = "1"


class TestBlueprint:
    """BDD: the C2 endpoints guard against CSRF and persist valid forms."""

    def test_unauthenticated_access_redirects_to_login(self, tmp_path: Path) -> None:
        app = _build_test_app(tmp_path)
        client = app.test_client()
        for path in ("/addons", "/addons/create", "/addons/web_enum/view"):
            response = client.get(path)
            assert response.status_code == 302
            assert "/__stub__/login" in response.headers["Location"]

    def test_create_form_issues_csrf_cookie(self, tmp_path: Path) -> None:
        app = _build_test_app(tmp_path)
        client = app.test_client()
        _login(client)
        response = client.get("/addons/create")
        assert response.status_code == 200
        assert b"Create LazyAddon" in response.data
        cookies = client.get_cookie("XSRF-TOKEN")
        assert cookies is not None

    def test_post_without_csrf_is_rejected(self, tmp_path: Path) -> None:
        app = _build_test_app(tmp_path)
        client = app.test_client()
        _login(client)
        response = client.post("/addons/create", data={"name": "sneaky_tool"})
        assert response.status_code == 403

    def test_delete_without_csrf_is_rejected(self, tmp_path: Path) -> None:
        app = _build_test_app(tmp_path)
        client = app.test_client()
        _login(client)
        response = client.post("/addons/some_tool/delete")
        assert response.status_code == 403

    def _form_data(self) -> dict[str, str]:
        """Return a complete valid form payload for the creation route."""
        return {
            "name": "web_enum",
            "description": "Enumerates directories and files on a web target.",
            "author": "LazyOwn",
            "version": "1.0",
            "enabled": "true",
            "os": "any",
            "trigger": "http",
            "category": "02. Scanning & Enumeration",
            "module_type": "scanner",
            "install_type": "git",
            "tool_name": "gobuster",
            "repo_url": "https://github.com/example/gobuster",
            "install_path": "external/.exploit/gobuster",
            "install_command": "go build .",
            "execute_command": "./gobuster dir -u {url}",
            "params-0-name": "url",
            "params-0-type": "string",
            "params-0-required": "true",
            "params-0-description": "Target URL.",
        }

    def _csrf_token(self, client: object) -> str:
        """Fetch the creation page and extract the embedded form token."""
        response = client.get("/addons/create")
        match = re.search(
            r'name="xsrf_token" value="([^"]+)"',
            response.get_data(as_text=True),
        )
        assert match, "create form must embed a csrf token"
        return match.group(1)

    def test_valid_post_creates_addon_and_redirects(self, tmp_path: Path) -> None:
        app = _build_test_app(tmp_path)
        client = app.test_client()
        _login(client)
        data = self._form_data()
        data["xsrf_token"] = self._csrf_token(client)
        response = client.post("/addons/create", data=data)
        assert response.status_code == 302
        assert response.headers["Location"].endswith("/addons/web_enum/view")
        stored = yaml.safe_load((tmp_path / "web_enum.yaml").read_text(encoding="utf-8"))
        assert stored["name"] == "web_enum"
        assert stored["tool"]["execute_command"] == "./gobuster dir -u {url}"

    def test_invalid_post_rerenders_with_field_errors(self, tmp_path: Path) -> None:
        app = _build_test_app(tmp_path)
        client = app.test_client()
        _login(client)
        data = self._form_data()
        data["name"] = "BAD NAME"
        data["xsrf_token"] = self._csrf_token(client)
        response = client.post("/addons/create", data=data)
        assert response.status_code == 200
        assert b"Name must be lowercase" in response.data
        assert not (tmp_path / "web_enum.yaml").exists()

    def test_duplicate_name_rerenders_with_error(self, tmp_path: Path) -> None:
        app = _build_test_app(tmp_path)
        client = app.test_client()
        _login(client)
        data = self._form_data()
        data["xsrf_token"] = self._csrf_token(client)
        assert client.post("/addons/create", data=data).status_code == 302
        second_data = dict(data)
        second_data["xsrf_token"] = self._csrf_token(client)
        response = client.post("/addons/create", data=second_data)
        assert response.status_code == 200
        assert b"already exists" in response.data

    def test_view_page_renders_yaml(self, tmp_path: Path) -> None:
        app = _build_test_app(tmp_path)
        client = app.test_client()
        _login(client)
        data = self._form_data()
        data["xsrf_token"] = self._csrf_token(client)
        client.post("/addons/create", data=data)
        response = client.get("/addons/web_enum/view")
        assert response.status_code == 200
        assert b"web_enum" in response.data
        assert b"./gobuster dir -u {url}" in response.data

    def test_list_page_shows_created_addon(self, tmp_path: Path) -> None:
        app = _build_test_app(tmp_path)
        client = app.test_client()
        _login(client)
        data = self._form_data()
        data["xsrf_token"] = self._csrf_token(client)
        client.post("/addons/create", data=data)
        response = client.get("/addons")
        assert response.status_code == 200
        assert b"web_enum" in response.data
        assert b"Enabled" in response.data

    def test_delete_removes_addon(self, tmp_path: Path) -> None:
        app = _build_test_app(tmp_path)
        client = app.test_client()
        _login(client)
        data = self._form_data()
        data["xsrf_token"] = self._csrf_token(client)
        client.post("/addons/create", data=data)
        delete_data = {"xsrf_token": self._csrf_token(client)}
        response = client.post("/addons/web_enum/delete", data=delete_data)
        assert response.status_code == 302
        assert not (tmp_path / "web_enum.yaml").exists()

    def test_delete_unknown_addon_flashes_and_redirects(self, tmp_path: Path) -> None:
        app = _build_test_app(tmp_path)
        client = app.test_client()
        _login(client)
        response = client.post(
            "/addons/ghost_tool/delete",
            data={"xsrf_token": self._csrf_token(client)},
        )
        assert response.status_code == 302

    def test_view_unknown_addon_redirects_to_list(self, tmp_path: Path) -> None:
        app = _build_test_app(tmp_path)
        client = app.test_client()
        _login(client)
        response = client.get("/addons/ghost_tool/view")
        assert response.status_code == 302

    def test_view_legacy_uppercase_addon_renders(self, tmp_path: Path) -> None:
        (tmp_path / "AdaptixC2.yaml").write_text(
            "name: AdaptixC2\nenabled: true\ndescription: C2\ntool:\n  execute_command: ./run.sh\n",
            encoding="utf-8",
        )
        app = _build_test_app(tmp_path)
        client = app.test_client()
        _login(client)
        response = client.get("/addons/AdaptixC2/view")
        assert response.status_code == 200
        assert b"AdaptixC2" in response.data
        assert b"./run.sh" in response.data

    def test_list_page_links_by_filename_for_legacy_names(self, tmp_path: Path) -> None:
        (tmp_path / "AdaptixC2.yaml").write_text("name: adaptixc2\nenabled: true\n", encoding="utf-8")
        app = _build_test_app(tmp_path)
        client = app.test_client()
        _login(client)
        response = client.get("/addons")
        assert response.status_code == 200
        assert b"/addons/AdaptixC2/view" in response.data
        assert b"/addons/AdaptixC2/delete" in response.data

    def test_delete_legacy_uppercase_addon(self, tmp_path: Path) -> None:
        (tmp_path / "AdaptixC2.yaml").write_text("name: AdaptixC2\nenabled: true\n", encoding="utf-8")
        app = _build_test_app(tmp_path)
        client = app.test_client()
        _login(client)
        response = client.post(
            "/addons/AdaptixC2/delete",
            data={"xsrf_token": self._csrf_token(client)},
        )
        assert response.status_code == 302
        assert not (tmp_path / "AdaptixC2.yaml").exists()

    def test_rendered_addon_passes_cli_schema_contract(self, tmp_path: Path) -> None:
        """The file produced through HTTP satisfies the CLI loader schema."""
        app = _build_test_app(tmp_path)
        client = app.test_client()
        _login(client)
        data = self._form_data()
        data["xsrf_token"] = self._csrf_token(client)
        client.post("/addons/create", data=data)
        stored = yaml.safe_load((tmp_path / "web_enum.yaml").read_text(encoding="utf-8"))
        for field in ("name", "description", "author", "version", "enabled", "os", "trigger", "category", "tool"):
            assert field in stored, f"missing CLI schema field {field}"
        tool = stored["tool"]
        assert tool.get("name")
        assert tool.get("repo_url", "").startswith("https://")
        assert tool.get("execute_command")
        for param in stored.get("params", []):
            assert {"name", "type", "required", "description"} <= set(param)


class TestTemplateSanity:
    """The shipped templates must stay renderable and tooltip rich."""

    def test_creator_template_has_help_affordances(self) -> None:
        text = (TEMPLATES_DIR / "addon_creator.html").read_text(encoding="utf-8")
        assert text.count('data-bs-toggle="tooltip"') >= 10
        assert "placeholder=" in text
        assert "form-text text-muted" in text
        assert "data-drop-target" in text
        assert 'draggable="true"' in text

    def test_creator_template_forbids_emojis_and_console_spam(self) -> None:
        text = (TEMPLATES_DIR / "addon_creator.html").read_text(encoding="utf-8")
        assert "console.log" not in text
        assert not re.search(r"[\U0001F300-\U0001FAFF]", text)

    def test_tools_creator_template_has_no_broken_js(self) -> None:
        text = (TEMPLATES_DIR / "create_tool.html").read_text(encoding="utf-8")
        assert '"microsoft-ds"endif' not in text
        assert "console.log" not in text
        assert "createToolForm" in text
        assert "triggerSelect" in text and "customTriggerInput" in text
