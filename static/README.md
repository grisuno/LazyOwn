# static

Static web assets served by `lazyc2.py` at `/static/`. Includes JavaScript
libraries, CSS stylesheets, report configuration, and image icons used by the
operator dashboard.

## Subdirectories

| Directory | Contents |
|-----------|---------|
| `css/` | Custom stylesheets for the C2 web UI. `style.css` is the main operator theme. `xterm.css` styles the in-browser terminal. |
| `js/` | JavaScript libraries and configuration. `xterm.js` drives the `/terminal` PTY page. `particles.js` renders the animated background. `particles.json` is its configuration. |
| `images/` | Node icons for the network graph (`user.png`, `computer.png`, `domain.png`, `group.png`, etc.). Also contains the security dashboard screenshot and the framework logo. |

## Key files in root

| File | Purpose |
|------|---------|
| `body_report.json` | Engagement report field store. Written by the `/teamserver` form, read by `/report` to render the PDF-ready report. |
| `favicon.ico` | Browser tab icon for the C2 web UI. |

## Notes

- Never commit sensitive data into `static/`. The directory is served publicly
  to any HTTP client that reaches the C2 port — anything here is readable.
- The `body_report.json` file contains operator-entered engagement metadata.
  It is excluded from git but should be archived with the engagement record.
- Icon PNGs in `static/images/` are used by the D3 network graph in
  `templates/surface.html`. Adding a new node type requires a matching icon
  here and an entry in the graph renderer JavaScript.
