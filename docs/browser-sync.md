# Browser Sync: real browser session into the framework

The browser sync feature reuses the operator's genuine browser session in
every automated request the framework sends. A Chrome/Brave extension pushes
the real cookie store and fingerprint headers to a local, token
authenticated receiver; the recorder proxy then blends that identity into
the traffic of `auto_loop`, `apt_chain`, `auto_pwn`, the lazy burp fuzzer
and anything else routed through it, so targets see the same session the
browser would send instead of anonymous automation traffic.

## Why it exists

Automated requests typically fail walls that the operator's browser passes:
WAF bot fingerprints, CSRF/session cookies, logged-in-only endpoints, and
rate limiting keyed to a session. With browser sync enabled, every proxied
request carries the synced cookies, the exact `User-Agent`, the browser's
language list and the `Sec-CH-UA` client hints, which keeps the traffic
looking like the operator's own session.

**Scope limitation.** Browser sync solves the session layer, not the full
fingerprint layer. The proxied requests still differ from real browser
traffic in TLS fingerprint (JA3/JA4 of the HTTP client), HTTP/2 settings,
`Sec-Fetch-Site`/`Sec-Fetch-Mode`/`Sec-Fetch-Dest` headers, `Accept` and
the exact header order. A stack that correlates TLS and header order can
still detect the automation. Treat the feature as session reuse against
cookie- and UA-based walls, not as a full browser impersonation; for
targets at that level use a real browser driven through the recorder
proxy instead.

## Quick start

1. Start the receiver in LazyOwn:

   ```
   browsersync start
   ```

   Note the endpoint (`http://127.0.0.1:8898/__lazyown/sync` by default) and
   the token printed on start.

2. Load the extension in Chrome or Brave: open `chrome://extensions`,
   enable Developer mode, click Load unpacked and select the
   `browser_sync_extension/` directory.

3. Click the extension icon, paste the token, keep or adjust the endpoint,
   press Save, then Sync now. Auto-sync repeats every 15 minutes by
   default (configurable in the popup) and also fires on page navigation.

4. Run any loop, chain or fuzzer command. From this point the traffic
   inherits the synced identity automatically.

## What gets synced

- All cookies of the current profile (`chrome.cookies.getAll`), including
  `HttpOnly`, `Secure`, `hostOnly` and expiry metadata.
- `User-Agent` and `navigator.languages`.
- `Sec-CH-UA`, `Sec-CH-UA-Mobile`, `Sec-CH-UA-Platform` client hints.

Artefacts are stored under `sessions/browser_sync/`:

| File | Contents |
|------|----------|
| `profile.json` | Full synced identity: cookies, user agent, languages, client hints |
| `cookies.jar` | Netscape-format cookie jar for `curl --cookie` and other tools |
| `token` | Receiver auth token (mode 600) |
| `rules.json` | Operator-defined Match and Replace rules (see below) |

## Command reference

`browsersync` subcommands:

| Subcommand | Effect |
|------------|--------|
| `start [port]` | Start the receiver (default from `browser_sync_port`, port argument overrides) |
| `stop` | Stop the receiver |
| `status` | Running state, sync count, cookie count, synced domains |
| `token` | Print the receiver token |
| `reset-token` | Regenerate the token (paste it into the extension again) |
| `show [domain] [--full]` | List synced cookies, masked by default |
| `jar` | Print the cookie jar path and usage snippets |
| `rules` | Show the Match and Replace rules file and types |
| `test [path] [--http]` | Preview the headers injected for the payload `rhost`; optional request path and `--http` to preview over plain HTTP |
| `clear` | Delete the synced profile and cookie jar |

## Proxy injection

`modules/lazy_proxy.py` calls `modules/browser_sync.apply_identity_headers`
on every forwarded exchange (plain HTTP and MITM HTTPS, websockets
included). Injection rules:

- Cookies are matched per host: exact hosts (`hostOnly`) or domain
  suffixes.
- Cookies are filtered and ordered like a browser sends them: RFC 6265
  path match, `Secure` cookies only over https, expired cookies dropped,
  longest path first.
- Synced cookie names win over names already in the request; unrelated
  existing cookies are preserved.
- `User-Agent`, `Accept-Language` and the client hints replace the
  automation defaults only when a profile exists; with no sync or with
  injection disabled, traffic stays anonymous.

### Framework inheritance

`browser_sync.ensure_wiring()` starts the receiver and the recorder proxy
and applies the proxy environment. It is invoked from:

- `ChainRunner.run` (covers `apt_chain`, recovery runs, gym chains and
  `chain_loop`)
- the loop runner (`_start_browser_sync`, alongside `proxy_autostart`)

Once the proxy environment is applied, every `run_command` subprocess
(curl in the loop, chain steps, the fuzzer) and every in-process
`requests` call inherits the routing and receives the synced identity.
The lazy burp fuzzer additionally injects the identity directly in its
proxy handler and `send_request` via
`browser_sync.apply_identity_to_url(url, headers, body)`, the shared
entry point for any requests-based module.

## Match and Replace rules

Edit `sessions/browser_sync/rules.json`:

```json
[
  {"type": "header_set", "match": "Referer", "replace": "https://example.com/"},
  {"type": "header_remove", "match": "X-Debug"},
  {"type": "body_replace", "match": "password=[^&]*", "replace": "password=x"}
]
```

| Type | Effect |
|------|--------|
| `header_replace` | Regex over the value of headers matching `match` |
| `header_add` | Add the header only when absent |
| `header_set` | Add or overwrite the header |
| `header_remove` | Delete matching headers |
| `body_replace` | Regex over the raw request body |

The `Host` header is never rewritten. When a rule changes the body, the
proxy recomputes `Content-Length`.

## Configuration

| payload.json key | Default | Meaning |
|------------------|---------|---------|
| `browser_sync_enabled` | `True` | Start the receiver with the loop and chains |
| `browser_sync_port` | `8898` | Loopback port of the receiver (also the fallback when the key is missing) |
| `browser_sync_inject` | `True` | Inject synced identity into proxied traffic |

`assign browser_sync_inject False` keeps the receiver running but stops
the injection without touching anything else.

## Security model

- The receiver binds `127.0.0.1` only and requires a runtime-generated
  token compared with `hmac.compare_digest`.
- `profile.json`, `cookies.jar` and `token` are all written with mode
  0600; the profile holds live session cookies, so treat the directory as
  sensitive material.
- By default the extension pushes the whole cookie store. Set the
  optional **Domain filter** in the popup (comma separated, e.g.
  `example.com, target.org`) to restrict the push to engagement domains;
  an empty filter keeps the full store.
- Request bodies are capped (8 MB) and drained so clients can always read
  the rejection; cookie counts and values are capped.
- Every stored header value is stripped of CR, LF and NUL; client hint
  names outside the `Sec-CH-UA` family are dropped at ingest.
- `browsersync show` masks values by default; `--full` is an explicit
  operator decision and is announced with a warning.
- The whole pipeline never raises: a broken or stale sync degrades to
  anonymous traffic instead of breaking the loop.
- Under pytest the wiring is disabled through `tests/conftest.py`
  (`browser_sync.WIRING_ENABLED`).

## Testing your setup

1. `browsersync status` shows the receiver, sync count and domains.
2. `browsersync test` prints the before/after headers for the payload
   `rhost`.
3. Confirm the extension popup reports `synced: <n> cookies`.
4. Run a proxied request and check the recorder:

   ```
   auto_loop
   lazy_traffic search-body "Cookie"
   ```

   Or point any tool at the recorder proxy port and observe the cookies
   arriving upstream.

## Files

| Path | Role |
|------|------|
| `browser_sync_extension/` | Chrome/Brave MV3 extension (manifest, service worker, popup) |
| `modules/browser_sync.py` | Receiver, profile store, Netscape jar, injection, rules, wiring |
| `cli/commands/browser_sync.py` | `browsersync` command set |
| `tests/test_browser_sync.py` | Receiver and injection contract tests |
| `tests/test_bprfuzzer_identity.py` | Fuzzer identity-inheritance tests |
