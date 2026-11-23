# lazyc2.phishing

Phishing domain contracts for the C2 server.

## Files

| File | Purpose |
|------|---------|
| `paths.py` | Canonical storage layout (campaigns, templates, tracking DB, short-URL registry) plus idempotent `ensure_storage`. |
| `short_urls_store.py` | Single `short_urls.json` load/save implementation. |
| `campaigns.py` | `phishing_bp` — campaign list/create, tracking pixel, report, LLM orchestration, multi-vector creation, landing pages; plus the access/execution log parsers and behavioral/campaign LLM analyzers. |

## Contract

- Storage paths are constants in `paths.py`; the C2 monolith imports them
  instead of redefining its own copies.
- `init_campaigns_bp(gmail_address, gmail_app_password, sessions_dir_fn)`
  binds SMTP credentials and the tenant-switchable sessions provider.
- Monolith-owned validated helpers (`load_yaml_safely`, `clean_json`) are
  lazy-imported at call time to avoid import cycles.
- Campaign routes keep their original decorators: operator pages use
  `login_required`; victim-facing endpoints (`track_pixel`,
  `serve_landing_page`) stay public.

Wiring: `lazyc2.py` calls `ensure_storage()` at boot, initialises the
blueprint with credentials and registers `phishing_bp`. The short-URL
HTTP routes (`/create_short_url`, `/track/<code>`, `/update_short_url`,
`/<code>`) and `/s/<filename>` remain monolith-owned until the short-URL
extraction session; the `lazyc2/blueprints/phishing.py` redirect blueprint
stays the app-factory-path surface with its own containment test.
