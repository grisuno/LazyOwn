"""Tier 0 foundation tests.

Verify the changes applied during the foundation tier:
- Config class deduplicated in utils.py
- pyproject.toml / setup.py packaging metadata fixed and extended
- requirements-dev.txt present with expected tooling
- pre-commit config valid
- CI workflows present and valid
- gitignore protects sensitive material
"""

import ast
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_toml(path: Path) -> dict:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


class TestConfigDeduplication:
    """The Config class must be defined exactly once across the framework.

    After Tier 1 the canonical location is ``core/config.py``; ``utils.py``
    re-exports it for backwards compatibility but must not redefine it.
    """

    def test_config_class_defined_exactly_once_in_core(self):
        core_config = REPO_ROOT / "core" / "config.py"
        tree = ast.parse(core_config.read_text(encoding="utf-8"))
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == "Config"]
        assert len(classes) == 1, f"Expected 1 Config in core/config.py, found {len(classes)}"

    def test_config_class_not_redefined_in_utils(self):
        utils_path = REPO_ROOT / "utils.py"
        tree = ast.parse(utils_path.read_text(encoding="utf-8"))
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == "Config"]
        assert classes == [], f"Config still redefined in utils.py at {[c.lineno for c in classes]}"

    @staticmethod
    def _run_in_subprocess(snippet: str) -> str:
        """Run a snippet in a clean subprocess so utils.py's argv parsing does not interfere."""
        import subprocess

        result = subprocess.run(
            [sys.executable, "-c", snippet],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            timeout=30,
        )
        if result.returncode != 0:
            pytest.fail(f"subprocess failed: {result.stderr}")
        return result.stdout.strip()

    def test_config_attribute_access_works(self):
        out = self._run_in_subprocess(
            "import sys; sys.argv=['utils']; "
            "from utils import Config; "
            "cfg=Config({'rhost':'127.0.0.1','lport':1234}); "
            "print(cfg.rhost, cfg.lport)"
        )
        assert out == "127.0.0.1 1234"

    def test_config_getitem_returns_value(self):
        out = self._run_in_subprocess(
            "import sys; sys.argv=['utils']; from utils import Config; print(Config({'rhost':'10.0.0.1'})['rhost'])"
        )
        assert out == "10.0.0.1"

    def test_config_getitem_returns_none_for_missing_key(self):
        out = self._run_in_subprocess(
            "import sys; sys.argv=['utils']; "
            "from utils import Config; "
            "print(Config({'rhost':'1.2.3.4'})['nonexistent_key'])"
        )
        assert out == "None"


class TestPyProjectToml:
    """pyproject.toml must parse, list valid deps, and define tooling sections."""

    @pytest.fixture(scope="class")
    def pyproject(self) -> dict:
        return _load_toml(REPO_ROOT / "pyproject.toml")

    def test_parses(self, pyproject):
        assert pyproject["project"]["name"] == "lazyown"

    def test_has_no_typo_dependency(self, pyproject):
        deps = pyproject["project"]["dependencies"]
        bad = [d for d in deps if d.startswith("instal ") or d == "instal flask-wtf"]
        assert bad == [], f"typo deps still present: {bad}"

    def test_does_not_list_stdlib_ast_as_dep(self, pyproject):
        deps = pyproject["project"]["dependencies"]
        assert "ast" not in deps, "stdlib 'ast' should not be a third-party dep"

    def test_lists_flask_wtf_correctly(self, pyproject):
        deps = pyproject["project"]["dependencies"]
        assert "flask-wtf" in deps

    def test_has_dev_optional_dependencies(self, pyproject):
        dev = pyproject["project"].get("optional-dependencies", {}).get("dev", [])
        joined = " ".join(dev)
        for tool in ("ruff", "pytest", "mypy", "bandit", "detect-secrets", "pip-audit"):
            assert tool in joined, f"dev extra missing tool: {tool}"

    def test_has_ruff_section(self, pyproject):
        assert "ruff" in pyproject["tool"]
        assert pyproject["tool"]["ruff"]["line-length"] == 120

    def test_has_pytest_section(self, pyproject):
        assert "pytest" in pyproject["tool"]
        assert "tests" in pyproject["tool"]["pytest"]["ini_options"]["testpaths"]

    def test_has_mypy_section(self, pyproject):
        assert "mypy" in pyproject["tool"]
        assert pyproject["tool"]["mypy"]["ignore_missing_imports"] is True

    def test_has_bandit_section(self, pyproject):
        assert "bandit" in pyproject["tool"]


class TestSetupPy:
    """setup.py must parse, import os, and not contain the previous typos."""

    @pytest.fixture(scope="class")
    def setup_tree(self) -> ast.Module:
        return ast.parse((REPO_ROOT / "setup.py").read_text(encoding="utf-8"))

    @pytest.fixture(scope="class")
    def setup_text(self) -> str:
        return (REPO_ROOT / "setup.py").read_text(encoding="utf-8")

    def test_parses(self, setup_tree):
        assert setup_tree is not None

    def test_imports_os(self, setup_tree):
        imports = [alias.name for node in ast.walk(setup_tree) if isinstance(node, ast.Import) for alias in node.names]
        assert "os" in imports, "setup.py must import os because it calls os.path.exists"

    def test_no_typo_dep(self, setup_text):
        assert "instal flask-wtf" not in setup_text

    def test_no_stdlib_ast_dep(self, setup_text):
        assert '"ast",' not in setup_text


class TestRequirementsDev:
    """requirements-dev.txt must list expected tooling."""

    @pytest.fixture(scope="class")
    def deps(self) -> list[str]:
        return [
            line.strip()
            for line in (REPO_ROOT / "requirements-dev.txt").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

    @pytest.mark.parametrize(
        "tool",
        ["ruff", "pytest", "pytest-cov", "mypy", "bandit", "detect-secrets", "pip-audit", "pre-commit"],
    )
    def test_lists_tool(self, deps, tool):
        joined = " ".join(deps)
        assert tool in joined, f"{tool} missing from requirements-dev.txt"


class TestPreCommitConfig:
    """.pre-commit-config.yaml must be valid and include core hooks."""

    @pytest.fixture(scope="class")
    def cfg(self) -> dict:
        return _load_yaml(REPO_ROOT / ".pre-commit-config.yaml")

    def test_parses(self, cfg):
        assert "repos" in cfg
        assert isinstance(cfg["repos"], list)
        assert len(cfg["repos"]) > 0

    def test_has_ruff_repo(self, cfg):
        repos = [r["repo"] for r in cfg["repos"]]
        assert any("ruff-pre-commit" in r for r in repos)

    def test_has_detect_secrets_repo(self, cfg):
        repos = [r["repo"] for r in cfg["repos"]]
        assert any("detect-secrets" in r for r in repos)

    def test_has_core_hygiene_hooks(self, cfg):
        hook_ids: set[str] = set()
        for repo in cfg["repos"]:
            for hook in repo.get("hooks", []):
                hook_ids.add(hook["id"])
        for required in ("end-of-file-fixer", "trailing-whitespace", "check-yaml", "check-toml", "detect-private-key"):
            assert required in hook_ids, f"missing hygiene hook: {required}"


class TestCIWorkflows:
    """All Tier 0 GitHub Actions workflows must parse and define expected jobs."""

    @pytest.fixture(scope="class")
    def lint_wf(self) -> dict:
        return _load_yaml(REPO_ROOT / ".github/workflows/lint.yml")

    @pytest.fixture(scope="class")
    def test_wf(self) -> dict:
        return _load_yaml(REPO_ROOT / ".github/workflows/test.yml")

    @pytest.fixture(scope="class")
    def security_wf(self) -> dict:
        return _load_yaml(REPO_ROOT / ".github/workflows/security.yml")

    def test_lint_workflow_has_ruff_and_mypy_jobs(self, lint_wf):
        jobs = set(lint_wf["jobs"].keys())
        assert "ruff" in jobs
        assert "mypy" in jobs

    def test_test_workflow_runs_pytest(self, test_wf):
        assert "pytest" in test_wf["jobs"]
        steps_text = str(test_wf["jobs"]["pytest"])
        assert "pytest" in steps_text

    def test_security_workflow_has_three_jobs(self, security_wf):
        jobs = set(security_wf["jobs"].keys())
        for required in ("bandit", "detect-secrets", "pip-audit"):
            assert required in jobs, f"missing job: {required}"

    @pytest.mark.parametrize(
        "wf_path",
        [".github/workflows/lint.yml", ".github/workflows/test.yml", ".github/workflows/security.yml"],
    )
    def test_workflow_triggers_on_push_and_pr(self, wf_path):
        wf = _load_yaml(REPO_ROOT / wf_path)
        on = wf.get(True) if True in wf else wf.get("on")
        assert on is not None, f"{wf_path} missing 'on' triggers"
        assert "push" in on
        assert "pull_request" in on


class TestGitIgnore:
    """.gitignore must protect sensitive material."""

    @pytest.fixture(scope="class")
    def patterns(self) -> list[str]:
        return [
            line.strip()
            for line in (REPO_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

    @pytest.mark.parametrize(
        "pattern",
        ["payload.json", "*.pem", "*.key", ".env", "sessions/*"],
    )
    def test_pattern_present(self, patterns, pattern):
        assert pattern in patterns, f"sensitive pattern missing from .gitignore: {pattern}"


class TestSourceFilesParse:
    """Top-level source files must still parse after Tier 0 edits."""

    @pytest.mark.parametrize("filename", ["lazyown.py", "lazyc2.py", "utils.py", "setup.py"])
    def test_parses(self, filename):
        path = REPO_ROOT / filename
        ast.parse(path.read_text(encoding="utf-8"))
