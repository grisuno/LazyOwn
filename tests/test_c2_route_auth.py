"""Guard the C2 route-level auth boundaries.

Every operator-facing dashboard/data endpoint must require authentication.
The intentionally-public surface (beacon channel, phishing victims, login,
health/metrics) must remain open so implant callbacks and campaign links
keep working. This test parses ``lazyc2.py`` with the AST so a missing or
accidentally-removed decorator fails deterministically.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
LAZYC2 = REPO_ROOT / "lazyc2.py"

_AUTH_DECORATORS = frozenset(
    {"requires_auth", "requires_auth_or_session", "login_required", "csrf_protect"}
)

# Operator-facing routes that must reject anonymous access.
PROTECTED_ENDPOINTS: frozenset[str] = frozenset(
    {
        "/graph",
        "/task/<int:task_id>",
        "/gettasks",
        "/tasks",
        "/task/<int:task_id>/edit",
        "/cves",
        "/cve/<int:cve_id>",
        "/cve/<int:cve_id>/edit",
        "/notes",
        "/getnotes",
        "/view_note",
        "/edit_event/<event_name>",
        "/event_config",
        "/event_config_view",
        "/events",
        "/tools",
        "/tools/create",
        "/tools/<toolname>",
        "/tools/<toolname>/update",
        "/tools/<toolname>/delete",
        "/config.json",
        "/surface",
        "/surface_live",
        "/api/surface_live",
        "/data",
        "/lazyphishingai",
    }
)

# Intentionally open: beacons use the client_id channel, phishing links must
# be reachable by victims, and auth/bootstrap/health endpoints are public.
PUBLIC_ENDPOINTS: frozenset[str] = frozenset(
    {
        "/command/<client_id>",
        "/upload",
        "/download_file",
        "/download/<path:file_path>",
        "/log/<path:data>",
        "/track/<short_url>",
        "/<short_url>",
        "/s/<filename>",
        "/register",
        "/login",
        "/mfa/verify",
        "/health",
        "/metrics",
    }
)


def _route_decorators() -> dict[str, set[str]]:
    """Map every ``@app.route(path)`` to its non-route decorator stack."""
    tree = ast.parse(LAZYC2.read_text(encoding="utf-8"))
    result: dict[str, set[str]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        path: str | None = None
        decorators: set[str] = set()
        for dec in node.decorator_list:
            if (
                isinstance(dec, ast.Call)
                and isinstance(dec.func, ast.Attribute)
                and dec.func.attr == "route"
                and isinstance(dec.func.value, ast.Name)
                and dec.func.value.id == "app"
                and dec.args
                and isinstance(dec.args[0], ast.Constant)
                and isinstance(dec.args[0].value, str)
            ):
                path = dec.args[0].value
            elif isinstance(dec, ast.Name):
                decorators.add(dec.id)
            elif isinstance(dec, ast.Attribute):
                decorators.add(dec.attr)
        if path is not None:
            result[path] = decorators
    return result


@pytest.fixture(scope="module")
def routes():
    return _route_decorators()


def test_protected_endpoints_require_auth(routes):
    unprotected = [
        path
        for path in PROTECTED_ENDPOINTS
        if not (routes.get(path, set()) & _AUTH_DECORATORS)
    ]
    assert unprotected == [], f"operator endpoints missing auth: {unprotected}"


def test_public_endpoints_stay_open(routes):
    protected = [
        path
        for path in PUBLIC_ENDPOINTS
        if routes.get(path, set()) & _AUTH_DECORATORS
    ]
    assert protected == [], f"public endpoints accidentally locked: {protected}"


def test_all_protected_endpoints_exist(routes):
    missing = [path for path in PROTECTED_ENDPOINTS if path not in routes]
    assert missing == [], f"expected endpoints not found: {missing}"
