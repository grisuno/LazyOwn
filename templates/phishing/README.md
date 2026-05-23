# templates/phishing/

Jinja2 templates served by the `phishing_bp` blueprint registered in
`lazyc2.py:289`. The blueprint declares `template_folder='templates/phishing'`,
so every `render_template(...)` call inside `modules/phishing*.py`
resolves against this directory first.

## Files

| File | Purpose | Served by (blueprint route) |
|------|---------|------------------------------|
| `campaigns.html` | Operator dashboard listing active phishing campaigns. | `/phishing/campaigns` |
| `new_campaign.html` | Form for creating a single-vector phishing campaign. | `/phishing/new` |
| `create_multivector_campaign.html` | Multi-channel campaign builder (email + SMS + landing). | `/phishing/multivector` |
| `orchestrate_campaign.html` | Live orchestration view (send queue, success rate, captured creds). | `/phishing/orchestrate/<id>` |
| `malicious_login.html` | Default credential-harvesting landing page (target-agnostic). | `/phishing/login/<id>` |
| `report.html` | Per-campaign report (timeline, hits, exfil). | `/phishing/report/<id>` |
| `emails/` | YAML email payload templates consumed by the AI email composer. See `emails/README.md`. |
| `landing_pages/` | HTML landing pages overlaid on top of `malicious_login.html`. See `landing_pages/README.md`. |

## How it works

1. `phishing_bp` is registered on the main Flask app in `lazyc2.py`. The blueprint reads `LAZYOWN_CONFIG` from `current_app.config` to pull `lhost`, `c2_port` and the SQLite path.
2. Operator-facing routes are decorated with `@requires_auth` (HTTP Basic) + `@login_required` (flask-login session).
3. Victim-facing routes (e.g. `malicious_login.html`) are unauthenticated and persist captures into `sessions/phishing/tracking.db`.
4. Every template extends `base.html` and re-uses `header.html` / `nav.html` / `footer.html` from the root `templates/` dir.

## Adding a template

- Filename pattern: `^[a-zA-Z0-9_-]+\.html$` (enforced by `lazyc2/security/validators.py::validate_template_name`).
- Always extend `base.html`. Reuse the shared partials before introducing new HTML.
- Never bake `lhost` / `lport` / `c2_user` into the template — read from the Jinja context populated by the route.
- For pages that capture data, write to SQLite or `sessions/phishing/` only — never to filesystem paths outside `sessions/`.
- Update this table in the same commit as the new template.
