# templates/landing_pages/

Stand-alone HTML landing pages overlaid on top of the default phishing
harness (`templates/phishing/malicious_login.html`). The phishing engine
loads a landing page here when the campaign config sets
`landing_template: <stem>` — the stem maps to `<stem>.html` inside this
directory.

## Files

| File | Pretext | Notes |
|------|---------|-------|
| `fake_login.html` | Generic single-sign-on portal | Hand-authored baseline. Posts `username`/`password` back to `/phishing/login/<campaign_id>`. |

## How it works

1. Operator creates a campaign and selects `fake_login` (or another stem) as the landing page.
2. The phishing runtime renders `<stem>.html` inside the page returned by `/phishing/login/<campaign_id>`.
3. Capture goes to `sessions/phishing/tracking.db` (`captures` table) keyed by `campaign_id` + `target_email`.

## Adding a landing page

- Single file per pretext; filename pattern `^[a-zA-Z0-9_-]+\.html$` (same validator as `templates/phishing/`).
- Form action must be relative (`/phishing/login/{{ campaign_id }}`) so the page survives DNS / IP rebinding.
- Avoid loading remote assets (CDN-hosted CSS/JS leaks the operator's network). Inline everything or serve from `static/`.
- Never include a real brand logo or trademark; ship a generic placeholder and let the operator swap it in for the engagement.
- Update this table in the same commit as the new file.
