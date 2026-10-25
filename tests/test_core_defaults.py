"""Build-time defaults are data, not literals.

SDD contract: ``config/defaults.toml`` owns fallback ports, wordlists
and paths; ``core/defaults.py`` is its only reader. Migrated call
sites must resolve through the typed helpers so editing the TOML
changes behavior without touching Python.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from core import defaults

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def _fresh_cache():
    defaults.clear_cache()
    yield
    defaults.clear_cache()


class TestLoader:
    def test_sections_present(self) -> None:
        doc = defaults.load_defaults()
        assert set(("ports", "wordlists", "paths")) <= set(doc)

    def test_typed_helpers(self) -> None:
        assert defaults.default_lport() == 1337
        assert defaults.default_rport() == 443
        assert defaults.rockyou_wordlist() == "/usr/share/wordlists/rockyou.txt"
        assert defaults.common_wordlists()[0] == "/usr/share/wordlists/rockyou.txt"
        assert len(defaults.common_wordlists()) == 5
        assert defaults.sessions_dir() == "sessions"

    def test_missing_file_fails_closed(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            defaults.load_defaults(tmp_path / "nope.toml")

    def test_get_fallback(self) -> None:
        assert defaults.get("ports", "missing", 9) == 9
        assert defaults.get("nope", "missing", 9) == 9


class TestCallSitesMigrated:
    SITES = {
        "modules/hash_cracker.py": "COMMON_WORDLISTS",
        "cli/commands/cred_migrated.py": "rockyou_wordlist",
        "lazyown.py": "default_lport",
        "modules/autonomous_exploit_engine.py": "default_lport",
    }

    def test_no_hardcoded_rockyou_in_logic(self) -> None:
        for rel in ("modules/hash_cracker.py", "cli/commands/cred_migrated.py"):
            tree = ast.parse((REPO_ROOT / rel).read_text(encoding="utf-8"))
            literals = [
                n.value
                for n in ast.walk(tree)
                if isinstance(n, ast.Constant) and n.value == "/usr/share/wordlists/rockyou.txt"
            ]
            assert not literals, f"{rel} must resolve rockyou via core.defaults"

    def test_no_hardcoded_default_lport(self) -> None:
        for rel in ("lazyown.py", "modules/autonomous_exploit_engine.py"):
            tree = ast.parse((REPO_ROOT / rel).read_text(encoding="utf-8"))
            hits = [
                n
                for n in ast.walk(tree)
                if isinstance(n, ast.Constant) and n.value == 1337
            ]
            assert not hits, f"{rel} must resolve the default lport via core.defaults"

    def test_helpers_imported(self) -> None:
        for rel, name in self.SITES.items():
            src = (REPO_ROOT / rel).read_text(encoding="utf-8")
            assert name in src, f"{rel} must reference {name}"


class TestWizardAndGui:
    def test_wizard_command_exists(self) -> None:
        tree = ast.parse(
            (REPO_ROOT / "cli" / "commands" / "defaults.py").read_text(encoding="utf-8")
        )
        commands = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name == "do_defaults"
        }
        assert commands == {"do_defaults"}

    def test_overrides_map_to_schema_keys(self) -> None:
        from core.payload_schema import SCHEMA

        src = (REPO_ROOT / "cli" / "commands" / "defaults.py").read_text(encoding="utf-8")
        assert '"wordlist"' in src and '"lport"' in src and '"rport"' in src
        for key in ("wordlist", "lport", "rport"):
            assert key in SCHEMA, f"override target {key} must be a schema key"

    def test_gui_routes_exist(self) -> None:
        src = (REPO_ROOT / "lazyc2" / "blueprints" / "api.py").read_text(encoding="utf-8")
        assert '@api_bp.route("/defaults", methods=["GET"])' in src
        assert '@api_bp.route("/defaults", methods=["POST"])' in src
        assert "@require_api_auth_with_store\ndef set_default" in src

    def test_gui_never_rewrites_toml(self) -> None:
        src = (REPO_ROOT / "lazyc2" / "blueprints" / "api.py").read_text(encoding="utf-8")
        view = src.split("def set_default")[1]
        assert "save_payload" in view
        assert ".toml" not in view and "tomli_w" not in view and "tomlkit" not in view


class TestGuiFunctional:
    @pytest.fixture()
    def client(self, tmp_path, monkeypatch):
        flask = pytest.importorskip("flask")
        pytest.importorskip("flask_login")
        monkeypatch.chdir(tmp_path)
        app = flask.Flask(__name__)
        from lazyc2.blueprints.api import api_bp

        app.register_blueprint(api_bp)
        app.config["TESTING"] = True
        return app.test_client()

    def test_get_defaults(self, client) -> None:
        response = client.get("/api/defaults")
        assert response.status_code == 200
        body = response.get_json()
        assert body["defaults"]["ports"]["default_lport"] == 1337
        assert "live" in body

    def test_post_defaults_rejects_unknown(self, client) -> None:
        response = client.post("/api/defaults", json={"name": "nope", "value": 1})
        assert response.status_code in (400, 401, 403)

    def test_post_defaults_rejects_bad_port(self, client) -> None:
        response = client.post("/api/defaults", json={"name": "lport", "value": 99999})
        assert response.status_code in (400, 401, 403)
