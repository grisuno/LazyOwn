"""Authentication and authorisation blueprint for the LazyOwn C2 server.

Login, logout, registration, MFA setup/verification, profile, and
admin user/tenant management routes. Registered from within
``lazyc2.py`` so that ``url_for('index')`` and other lazyc2.py
routes are available.
"""

from __future__ import annotations

from flask import (
    Blueprint,
    Response,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from lazyc2.extensions.decoy import decoy_response

try:
    from modules.lazy_rbac import Role, require_role
except ImportError:
    Role = None
    require_role = lambda role: lambda f: f  # no-op fallback

auth_bp = Blueprint("auth", __name__)


# ── Helpers ────────────────────────────────────────────────────────────────


def _rbac_available() -> bool:
    """Check if RBAC is available from app config."""
    return current_app.config.get("RBAC_AVAILABLE", False)


def _get_rbac_store():
    """Resolve the RBAC store from the C2 monolith."""
    if not _rbac_available():
        return None
    try:
        from lazyc2 import get_rbac_store as _get_store
        return _get_store()
    except (ImportError, AttributeError):
        return None


def _get_rbac_user_obj(flask_user) -> object | None:
    """Resolve the RBAC user object for a Flask-Login user."""
    try:
        from lazyc2 import _get_rbac_user_obj
        return _get_rbac_user_obj(flask_user)
    except (ImportError, AttributeError):
        return None


def _get_tenant_manager():
    """Resolve the tenant manager from the C2 monolith."""
    try:
        from lazyc2 import get_tenant_manager
        return get_tenant_manager()
    except (ImportError, AttributeError):
        return None


# ── Register ────────────────────────────────────────────────────────────────


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    decoy = decoy_response()
    if decoy:
        return decoy
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            flash("Username and password are mandatory.", "error")
            return redirect(url_for("auth.register"))
        if len(password) < 12:
            flash("Password must be at least 12 chars.", "error")
            return redirect(url_for("auth.register"))

        if _rbac_available():
            from modules.lazy_rbac import Role, ROLE_DEFAULT
            store = _get_rbac_store()
            if store and store.find_by_username(username):
                flash("Username already exists.", "error")
                return redirect(url_for("auth.register"))
            role = Role.ADMIN.value if not any(
                u.role == Role.ADMIN.value for u in store.load_all()
            ) else ROLE_DEFAULT
            store.create_user(
                username=username,
                password_hash=generate_password_hash(password),
                role=role,
            )
            flash("Registration successful. Please login.", "success")
            return redirect(url_for("auth.login"))

        from lazyc2.extensions.users import load_users, save_users
        users = load_users()
        if any(u["username"] == username for u in users):
            flash("Username already exists.", "error")
            return redirect(url_for("auth.register"))
        ROLE_DEFAULT = current_app.config.get("ROLE_DEFAULT", "user")
        new_user = {
            "id": len(users) + 1,
            "username": username,
            "password_hash": generate_password_hash(password),
            "elo": 0,
            "role": ROLE_DEFAULT,
            "mfa_enabled": False,
            "mfa_secret": "",
            "recovery_codes": [],
            "tenant_id": "default",
        }
        users.append(new_user)
        save_users(users)
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")


# ── Login ───────────────────────────────────────────────────────────────────


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    decoy = decoy_response()
    if decoy:
        return decoy
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if _rbac_available():
            from lazyc2 import User
            store = _get_rbac_store()
            rbac_user = store.find_by_username(username) if store else None
            if rbac_user and check_password_hash(rbac_user.password_hash, password):
                user = User(rbac_user.to_dict())
                login_user(user)
                if rbac_user.mfa_enabled:
                    session["mfa_user_id"] = user.id
                    return redirect(url_for("auth.mfa_verify"))
                session.pop("mfa_user_id", None)
                session["mfa_verified"] = True
                flash("Welcome to LazyOwn.", "success")
                return redirect(url_for("auth.profile"))
            flash("Invalid login credentials.", "error")
            return render_template("login.html")

        from lazyc2.extensions.users import load_users
        users = load_users()
        user_data = next((u for u in users if u["username"] == username), None)
        if user_data and check_password_hash(user_data["password_hash"], password):
            from lazyc2 import User
            login_user(User(user_data))
            flash("Welcome to LazyOwn.", "success")
            return redirect(url_for("auth.profile"))
        flash("Invalid login credentials.", "error")
    return render_template("login.html")


# ── MFA ─────────────────────────────────────────────────────────────────────


@auth_bp.route("/mfa/setup", methods=["GET", "POST"])
@login_required
def mfa_setup():
    import pyotp
    if not _rbac_available():
        flash("RBAC module not available.", "error")
        return redirect(url_for("auth.profile"))
    decoy = decoy_response()
    if decoy:
        return decoy
    store = _get_rbac_store()
    rbac_user = _get_rbac_user_obj(current_user)
    if not rbac_user:
        flash("User not found.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        action = request.form.get("action", "")
        if action == "enable":
            updated = store.enable_mfa(rbac_user.id)
            if updated:
                session["mfa_setup_secret"] = updated.mfa_secret
                session["mfa_setup_username"] = updated.username
                flash("MFA enabled. Scan the QR code with your authenticator app.", "success")
                return redirect(url_for("auth.mfa_setup"))
            flash("Failed to enable MFA.", "error")
        elif action == "disable":
            token = request.form.get("mfa_code", "").strip()
            if rbac_user and rbac_user.verify_totp(token):
                store.disable_mfa(rbac_user.id)
                session.pop("mfa_setup_secret", None)
                flash("MFA disabled.", "success")
                return redirect(url_for("auth.profile"))
            flash("Invalid TOTP code. MFA not disabled.", "error")
        elif action == "disable_recovery":
            code = request.form.get("mfa_code", "").strip()
            if rbac_user and rbac_user.verify_recovery_code(code):
                store.consume_recovery_code(rbac_user.id, code)
                store.disable_mfa(rbac_user.id)
                session.pop("mfa_setup_secret", None)
                flash("MFA disabled via recovery code.", "success")
                return redirect(url_for("auth.profile"))
            flash("Invalid recovery code.", "error")
        elif action == "verify_setup":
            token = request.form.get("mfa_code", "").strip()
            secret = session.get("mfa_setup_secret", "")
            if secret and pyotp.TOTP(secret).verify(token, valid_window=1):
                session.pop("mfa_setup_secret", None)
                flash("MFA setup verified successfully!", "success")
                return redirect(url_for("auth.profile"))
            flash("Invalid TOTP code. Please try again.", "error")

    secret = session.get("mfa_setup_secret", "") or rbac_user.mfa_secret
    recovery_codes = rbac_user.recovery_codes if rbac_user.recovery_codes else []
    qr_url = ""
    if secret:
        try:
            from modules.lazy_rbac import generate_mfa_qr_url
            qr_url = generate_mfa_qr_url(secret, rbac_user.username)
        except Exception:
            pass
    return render_template(
        "mfa_setup.html",
        user=current_user,
        mfa_enabled=rbac_user.mfa_enabled,
        mfa_secret=secret,
        qr_url=qr_url,
        recovery_codes=recovery_codes,
    )


@auth_bp.route("/mfa/qr/<username>")
@login_required
def mfa_qr(username):
    import pyotp
    try:
        from modules.lazy_rbac import generate_qr_svg
        store = _get_rbac_store()
        if not store:
            return Response("RBAC not available", status=500)
        user = store.find_by_username(username)
        if not user or not user.mfa_secret:
            return Response("User or MFA secret not found", status=404)
        MFA_ISSUER = current_app.config.get("MFA_ISSUER", "LazyOwn")
        uri = pyotp.totp.TOTP(user.mfa_secret).provisioning_uri(
            name=user.username, issuer_name=MFA_ISSUER
        )
        svg = generate_qr_svg(uri)
        return Response(svg, mimetype="image/svg+xml")
    except Exception as e:
        current_app.logger.error("QR generation failed: %s", e)
        return Response("QR generation failed", status=500)


@auth_bp.route("/mfa/verify", methods=["GET", "POST"])
def mfa_verify():
    if not _rbac_available():
        return redirect(url_for("auth.login"))
    decoy = decoy_response()
    if decoy:
        return decoy
    user_id = session.get("mfa_user_id")
    if not user_id:
        return redirect(url_for("auth.login"))
    store = _get_rbac_store()
    rbac_user = store.find_by_id(int(user_id))
    if not rbac_user:
        session.pop("mfa_user_id", None)
        flash("Session expired. Please login again.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        code = request.form.get("mfa_code", "").strip()
        use_recovery = request.form.get("use_recovery") == "1"
        if use_recovery:
            if rbac_user.verify_recovery_code(code):
                store.consume_recovery_code(rbac_user.id, code)
                session["mfa_verified"] = True
                session.pop("mfa_user_id", None)
                pending = session.pop("mfa_pending_route", url_for("auth.profile"))
                flash("Authenticated via recovery code.", "success")
                return redirect(pending)
            flash("Invalid recovery code.", "error")
        else:
            if rbac_user.verify_totp(code):
                session["mfa_verified"] = True
                session.pop("mfa_user_id", None)
                pending = session.pop("mfa_pending_route", url_for("auth.profile"))
                flash("MFA verified successfully.", "success")
                return redirect(pending)
            flash("Invalid TOTP code.", "error")
    return render_template("mfa_verify.html", has_recovery=bool(rbac_user.recovery_codes))


# ── Profile ─────────────────────────────────────────────────────────────────


@auth_bp.route("/profile")
@login_required
def profile():
    decoy = decoy_response()
    if decoy:
        return decoy
    from lazyc2 import get_karma_name
    ROLE_DEFAULT = current_app.config.get("ROLE_DEFAULT", "user")
    karma_name = get_karma_name(current_user.elo)
    user_role = getattr(current_user, "role", ROLE_DEFAULT)
    mfa_enabled = getattr(current_user, "mfa_enabled", False)
    rbac_user = _get_rbac_user_obj(current_user)
    if rbac_user:
        user_role = rbac_user.role
        mfa_enabled = rbac_user.mfa_enabled
    return render_template(
        "profile.html",
        user=current_user,
        karma_name=karma_name,
        user_role=user_role,
        mfa_enabled=mfa_enabled,
    )


@auth_bp.route("/logout")
@login_required
def logout():
    decoy = decoy_response()
    if decoy:
        return decoy
    session.pop("mfa_verified", None)
    session.pop("mfa_user_id", None)
    session.pop("mfa_setup_secret", None)
    session.pop("mfa_pending_route", None)
    logout_user()
    flash("Successfully logged out.", "success")
    return redirect(url_for("index"))


# ── Admin: Users ────────────────────────────────────────────────────────────


@auth_bp.route("/admin/users")
@login_required
@require_role(Role.ADMIN.value)
def admin_users():
    if not _rbac_available():
        flash("RBAC module not available.", "error")
        return redirect(url_for("auth.profile"))
    from modules.lazy_rbac import Role
    decoy = decoy_response()
    if decoy:
        return decoy
    store = _get_rbac_store()
    users_list = store.load_all()
    return render_template("admin_users.html", users=users_list, roles=Role, current_user=current_user)


@auth_bp.route("/admin/users/<int:user_id>/role", methods=["POST"])
@login_required
@require_role(Role.ADMIN.value)
def admin_set_role(user_id):
    if not _rbac_available():
        return jsonify({"error": "RBAC not available"}), 500
    from modules.lazy_rbac import Role
    new_role = request.form.get("role", "").strip()
    if new_role not in Role.valid_roles():
        flash("Invalid role.", "error")
        return redirect(url_for("auth.admin_users"))
    store = _get_rbac_store()
    admin_user = _get_rbac_user_obj(current_user)
    if not admin_user or not admin_user.can_manage_role(new_role):
        flash("You cannot assign this role.", "error")
        return redirect(url_for("auth.admin_users"))
    store.update_role(user_id, new_role)
    flash(f"User role updated to {new_role}.", "success")
    return redirect(url_for("auth.admin_users"))


@auth_bp.route("/admin/users/<int:user_id>/mfa/reset", methods=["POST"])
@login_required
@require_role(Role.ADMIN.value)
def admin_reset_mfa(user_id):
    if not _rbac_available():
        return jsonify({"error": "RBAC not available"}), 500
    store = _get_rbac_store()
    store.disable_mfa(user_id)
    flash("MFA reset for user.", "success")
    return redirect(url_for("auth.admin_users"))


@auth_bp.route("/admin/users/<int:user_id>/delete", methods=["POST"])
@login_required
@require_role(Role.ADMIN.value)
def admin_delete_user(user_id):
    if not _rbac_available():
        return jsonify({"error": "RBAC not available"}), 500
    admin_user = _get_rbac_user_obj(current_user)
    if admin_user and admin_user.id == user_id:
        flash("Cannot delete your own account.", "error")
        return redirect(url_for("auth.admin_users"))
    store = _get_rbac_store()
    store.delete_user(user_id)
    flash("User deleted.", "success")
    return redirect(url_for("auth.admin_users"))


# ── Admin: Tenants ──────────────────────────────────────────────────────────


@auth_bp.route("/admin/tenants")
@login_required
def admin_tenants():
    if not _rbac_available():
        flash("RBAC module not available.", "error")
        return redirect(url_for("auth.profile"))
    from modules.lazy_rbac import Role
    decoy = decoy_response()
    if decoy:
        return decoy
    tm = _get_tenant_manager()
    tenants = tm.list_tenants()
    active = tm.get_active()
    return render_template(
        "admin_tenants.html",
        tenants=tenants,
        active=active,
        current_user=current_user,
    )


@auth_bp.route("/admin/tenants/create", methods=["POST"])
@login_required
def admin_create_tenant():
    if not _rbac_available():
        return jsonify({"error": "RBAC not available"}), 500
    name = request.form.get("name", "").strip()
    if not name:
        flash("Tenant name is required.", "error")
        return redirect(url_for("auth.admin_tenants"))
    tm = _get_tenant_manager()
    try:
        tc = tm.create_tenant(name)
        flash(f'Tenant "{tc.name}" created.', "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("auth.admin_tenants"))


@auth_bp.route("/admin/tenants/<tenant_id>/switch", methods=["POST"])
@login_required
def admin_switch_tenant(tenant_id):
    if not _rbac_available():
        return jsonify({"error": "RBAC not available"}), 500
    tm = _get_tenant_manager()
    try:
        tc = tm.switch_tenant(tenant_id)
        flash(f'Switched to tenant "{tc.name}". Sessions: {tc.sessions_dir}', "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("auth.admin_tenants"))
