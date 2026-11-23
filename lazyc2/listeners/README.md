# lazyc2.listeners

Listener management REST surface for the C2 server.

## Files

| File | Purpose |
|------|---------|
| `blueprint.py` | `listeners_bp` — `/api/listeners` CRUD (list, create, start, stop, delete). |

## Contract

- The manager handle is read from `current_app.config["listener_manager"]`
  (set by the C2 boot from `modules.listener_manager.ListenerManager`).
- Every route is gated by `lazyc2.security.auth.requires_auth` (HTTP Basic).
- The blueprint never imports the monolith, so `lazyc2.app_factory` or any
  standalone app can register it after binding the manager into config.

Wiring: `lazyc2.py` registers `listeners_bp`; the `/listener` dashboard
route, the `/listener` socket handlers and the reverse-shell catch-back
thread remain monolith-owned until the terminal extraction lands.
