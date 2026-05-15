# templates

Jinja2 templates served by `lazyc2.py`. Every page in the C2 web interface
renders from a template in this directory. All templates extend `base.html`
and follow the naming convention validated by `validate_template_name`
(`^[a-zA-Z0-9_-]+\.html$`).

## Layout partials

| File | Role |
|------|------|
| `base.html` | Root layout. Includes the Bootstrap 5 navbar, particles background, and `{% block content %}` slot. |
| `header.html` | `<head>` with CSS imports and meta tags. Included by `base.html`. |

## Operator UI pages

| File | Route | Purpose |
|------|-------|---------|
| `index.html` | `/` | Connected beacon / host overview with OS filter, search, and kill-chain progress. |
| `connect.html` | `/connect` | Reverse shell listener and beacon delivery console. |
| `terminal.html` | `/terminal` | xterm.js terminal proxied over Socket.IO `/terminal` namespace. |
| `banners.html` | `/banners` | Target service banner aggregation view. |
| `surface.html` | `/surface` | D3.js network graph of discovered hosts and Bloodhound relationships. |
| `bots.html` | `/bots` | AI bot chat interface (chatbot, vuln bot, task bot). |
| `campaigns.html` | `/campaigns` | Phishing campaign list and status overview. |
| `cve.html` / `cves.html` | `/cve`, `/cves` | CVE detail and CVE search views. |
| `tasks.html` | — | Campaign task list driven by `sessions/tasks.json`. |
| `notes.html` / `edit_note.html` | — | Operator notes CRUD. |
| `collab.html` | `/collab/` | Multi-operator team dashboard: SSE event feed, operator presence, target locking, chat broadcast. |
| `teamserver.html` | `/teamserver` | Engagement metadata form (assessment info, objectives, executive summary). Data written to `static/body_report.json`. |
| `report.html` | `/report` | PDF-ready engagement report rendered from `static/body_report.json`. |
| `mitre.html` | `/mitre` | MITRE ATT&CK technique browser backed by the parquet knowledge base. |
| `graph.html` | `/graph` | Atomic Red Team test navigator. |
| `profile.html` | `/profile` | Operator profile and session settings. |
| `decoy.html` | `/` (non-operator) | Fake landing site rendered for non-operator IPs. Captures webcam and audio. |

## Error pages

| File | Status |
|------|--------|
| `404.html` | 404 Not Found |
| `500.html` | 500 Internal Server Error |

## Subdirectories

| Directory | Contents |
|-----------|---------|
| `phishing/` | Templates for phishing campaign pages: login forms, lure pages, confirmation screens. |
| `emails/` | Email body templates used by the phishing module. Jinja2 with `{name}`, `{beacon_url}`, and `{tracking_pixel}` placeholders. |
| `landing_pages/` | Decoy landing page variants for different target profiles. |

## Rules for new templates

- Always extend `base.html` via `{% extends "base.html" %}`.
- Pass typed context dicts from the view — never pass raw `request` objects.
- Mark `|safe` only when the input is provably HTML you produced. Never mark
  user-supplied strings safe.
- Filenames must match `^[a-zA-Z0-9_-]+\.html$`. Names that fail
  `validate_template_name` in `lazyc2.py` will be rejected.
- Phishing templates go in `templates/phishing/`, not in the root.
