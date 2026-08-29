"""LazyAddon creator blueprint for the C2 dashboard.

Exposes the addon lifecycle under ``/addons``: a list page, the guided
creation form (GET and POST), a rendered YAML preview page, and a
delete endpoint. All mutating routes enforce the per-session CSRF token
issued on the form page.

Design (SOLID):
    - Single Responsibility: this module only adapts HTTP requests to
      the ``lazyc2.addon_creator`` contract and templates
    - Open/Closed: new pages reuse the same store and policy helpers
    - Liskov: every route returns plain Flask responses like the rest
      of the dashboard
    - Interface Segregation: small helpers, no shared mutable globals
    - Dependency Inversion: depends on the addon creator contract,
      never on the ``lazyc2.py`` monolith internals
"""

from __future__ import annotations

import re
import secrets
from collections.abc import Callable
from functools import wraps
from typing import Any

import yaml
from flask import (
    Blueprint,
    Response,
    current_app,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

from lazyc2.addon_creator import (
    AddonCreatorConfig,
    AddonDraft,
    AddonStore,
    AddonValidationError,
    AddonValidator,
    AddonYamlRenderer,
    ParamSpec,
    ValidationIssue,
    parse_addon_form,
)
from lazyc2.blueprints.session_auth import require_operator_session
from lazyc2.extensions.decoy import decoy_response
from lazyc2.security.csrf import CSRFPolicy

addons_bp = Blueprint("addons", __name__)

require_operator_session(addons_bp)

_CSRF_EXTENSION = "lazyown_addons_csrf"
_BP_CONFIG = AddonCreatorConfig()
_BP_BASE_DIR: str | None = None
_SAFE_CLIENT_ID = re.compile(r"^[A-Za-z0-9_-]{43}$")


def init_addons_bp(base_dir: str | None = None) -> None:
    """Configure the blueprint state before registration.

    Args:
        base_dir: Optional addons directory override. When omitted the
            value stored on the app config under ``LAZYOWN_ADDONS_DIR``
            or the contract default is used.
    """
    global _BP_BASE_DIR
    _BP_BASE_DIR = base_dir


def _store() -> AddonStore:
    """Return an AddonStore bound to the configured addons directory."""
    base_dir = _BP_BASE_DIR or current_app.config.get("LAZYOWN_ADDONS_DIR") or _BP_CONFIG.addons_dir
    return AddonStore(config=_BP_CONFIG, base_dir=base_dir)


def _csrf_policy() -> CSRFPolicy:
    """Return the app-scoped CSRF policy for addon mutation routes."""
    policy = current_app.extensions.get(_CSRF_EXTENSION)
    if policy is None:
        policy = CSRFPolicy()
        current_app.extensions[_CSRF_EXTENSION] = policy
    return policy


def csrf_protect(view: Callable[..., Response]) -> Callable[..., Response]:
    """Decorate a view so mutating requests must echo the CSRF token.

    Safe methods pass through untouched; unsafe methods must present a
    token bound to the stable client cookie issued on the form page.

    Args:
        view: The Flask view function to wrap.

    Returns:
        The wrapped view returning 403 JSON when the token is invalid.
    """

    @wraps(view)
    def wrapper(*args: Any, **kwargs: Any) -> Response:
        policy = _csrf_policy()
        session_id = request.cookies.get(policy.cookie_name) or ""
        if not policy.check_request(session_id, request):
            return jsonify({"error": "csrf token missing or invalid"}), 403
        return view(*args, **kwargs)

    return wrapper


def _issue_csrf(response: Response, policy: CSRFPolicy) -> str:
    """Bind a CSRF token to a stable client cookie and expose it.

    The cookie carries a random client identifier that never changes
    between requests, unlike the Flask session cookie which is re-signed
    whenever flash messages are consumed. The token itself stays in the
    policy store and travels inside the form.

    Args:
        response: The outgoing response that receives the cookie.
        policy: The policy issuing the token.

    Returns:
        The token string to embed in the form.
    """
    client_id = request.cookies.get(policy.cookie_name)
    if not client_id or not _SAFE_CLIENT_ID.fullmatch(client_id):
        client_id = secrets.token_urlsafe(32)
    token = policy.issue(client_id)
    response.set_cookie(
        policy.cookie_name,
        client_id,
        httponly=True,
        samesite="Lax",
        secure=current_app.config.get("SESSION_COOKIE_SECURE", True),
    )
    return token


def _issue_map(issues: list[ValidationIssue]) -> dict[str, list[str]]:
    """Group validation issues by field for template rendering.

    Args:
        issues: The flat list of ValidationIssue instances.

    Returns:
        A mapping of field name to message list.
    """
    grouped: dict[str, list[str]] = {}
    for issue in issues:
        grouped.setdefault(issue.field, []).append(issue.message)
    return grouped


def _form_context(
    draft: AddonDraft,
    issues: list[ValidationIssue],
) -> dict[str, Any]:
    """Build the template context shared by the form renders.

    Args:
        draft: The current form state.
        issues: Validation findings to surface per field.

    Returns:
        The context dict consumed by ``addon_creator.html``.
    """
    return {
        "draft": draft,
        "issue_map": _issue_map(issues),
        "os_options": _BP_CONFIG.os_options,
        "category_options": _BP_CONFIG.category_options,
        "module_type_options": _BP_CONFIG.module_type_options,
        "install_type_options": _BP_CONFIG.install_type_options,
        "trigger_options": _BP_CONFIG.trigger_options,
        "param_types": _BP_CONFIG.param_types,
        "max_params": _BP_CONFIG.max_params,
        "payload_placeholders": sorted(_BP_CONFIG.payload_placeholders),
        "default_author": _BP_CONFIG.default_author,
        "default_version": _BP_CONFIG.default_version,
    }


def _render_create(draft: AddonDraft, issues: list[ValidationIssue]) -> Response:
    """Render the creation form with a fresh CSRF token.

    Args:
        draft: The current form state.
        issues: Validation findings to surface per field.

    Returns:
        The rendered form response with the CSRF cookie set.
    """
    policy = _csrf_policy()
    response = make_response("")
    token = _issue_csrf(response, policy)
    response.set_data(
        render_template(
            "addon_creator.html",
            xsrf_token=token,
            **_form_context(draft, issues),
        )
    )
    return response


def _draft_from_document(document: dict[str, Any]) -> AddonDraft:
    """Convert a persisted document back into a renderable draft.

    Args:
        document: The parsed addon mapping.

    Returns:
        A draft whose YAML rendering is canonical.
    """
    tool = document.get("tool") or {}
    params = []
    for raw_param in document.get("params") or []:
        params.append(
            ParamSpec(
                name=str(raw_param.get("name", "")),
                type=str(raw_param.get("type", "string")),
                required=bool(raw_param.get("required", False)),
                description=str(raw_param.get("description", "")),
                default=raw_param.get("default"),
            )
        )
    return AddonDraft(
        name=str(document.get("name", "")),
        description=str(document.get("description", "")),
        author=str(document.get("author", "")),
        version=str(document.get("version", "")),
        enabled=bool(document.get("enabled", True)),
        os=str(document.get("os", "any")),
        triggers=[str(item) for item in (document.get("trigger") or [])],
        category=str(document.get("category", "")),
        module_type=str(document.get("module_type", "")),
        install_type=str(document.get("install_type", "")),
        params=params,
        tool_name=str(tool.get("name", "")),
        repo_url=str(tool.get("repo_url", "")),
        install_path=str(tool.get("install_path", "")),
        install_command=str(tool.get("install_command", "")),
        execute_command=str(tool.get("execute_command", "")),
        upload_file=str(tool.get("upload_file", "")),
        remote_command=str(tool.get("remote_command", "")),
        download_file=str(tool.get("download_file", "")),
        lazycommand=str(tool.get("lazycommand", "")),
        env=[str(item) for item in (tool.get("env") or [])],
    )


@addons_bp.route("/addons")
def list_addons():
    """Render the addon dashboard list page with a fresh CSRF token."""
    decoy = decoy_response()
    if decoy:
        return decoy
    policy = _csrf_policy()
    response = make_response("")
    token = _issue_csrf(response, policy)
    response.set_data(render_template("addons.html", addons=_store().list_all(), xsrf_token=token))
    return response


@addons_bp.route("/addons/create", methods=["GET", "POST"])
@csrf_protect
def create_addon():
    """Render the creation form and persist valid addon submissions.

    Returns:
        On GET the guided form. On POST either the re-rendered form
        with per-field errors or a redirect to the YAML preview.
    """
    decoy = decoy_response()
    if decoy:
        return decoy
    store = _store()
    if request.method == "POST":
        draft = parse_addon_form(request.form)
        issues = AddonValidator(draft).validate()
        if not issues and store.exists(draft.name.strip()):
            issues.append(
                ValidationIssue(
                    "name",
                    f"Addon '{draft.name.strip()}' already exists. Pick another "
                    "name or delete the existing file first.",
                )
            )
        if issues:
            for field_name, messages in _issue_map(issues).items():
                for message in messages:
                    flash(f"{field_name}: {message}", "danger")
            return _render_create(draft, issues)
        try:
            yaml_text = AddonYamlRenderer().render(draft)
            store.save(draft.name.strip(), yaml_text)
        except (OSError, AddonValidationError, yaml.YAMLError) as exc:
            flash(f"Could not save the addon: {exc}", "danger")
            return _render_create(draft, issues)
        flash(
            f"Addon '{draft.name.strip()}' created under the addons directory. Run 'reload' in the CLI to register it.",
            "success",
        )
        return redirect(url_for("addons.view_addon", name=draft.name.strip()))

    return _render_create(AddonDraft(), [])


@addons_bp.route("/addons/<name>/view")
def view_addon(name: str):
    """Render the persisted YAML document for an addon.

    Args:
        name: The addon name to preview.

    Returns:
        The preview page or a redirect to the list when missing.
    """
    decoy = decoy_response()
    if decoy:
        return decoy
    store = _store()
    try:
        document = store.load(name)
        yaml_text = AddonYamlRenderer().render(_draft_from_document(document))
    except (AddonValidationError, FileNotFoundError, ValueError, yaml.YAMLError):
        flash(f"Addon '{name}' not found or unreadable.", "danger")
        return redirect(url_for("addons.list_addons"))
    return render_template("addon_view.html", name=name, yaml_text=yaml_text)


@addons_bp.route("/addons/<name>/delete", methods=["POST"])
@csrf_protect
def delete_addon(name: str):
    """Delete an addon file.

    Args:
        name: The addon name to remove.

    Returns:
        A redirect to the list page with a status flash.
    """
    decoy = decoy_response()
    if decoy:
        return decoy
    store = _store()
    try:
        removed = store.delete(name)
    except AddonValidationError:
        flash(f"Addon '{name}' not found.", "danger")
        return redirect(url_for("addons.list_addons"))
    if removed:
        flash(f"Addon '{name}' deleted.", "success")
    else:
        flash(f"Addon '{name}' not found.", "danger")
    return redirect(url_for("addons.list_addons"))
