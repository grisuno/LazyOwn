# LazyOwn Browser Sync Extension

Chrome/Brave (Manifest V3) extension that pushes the real cookie store and
fingerprint headers (User-Agent, languages, Sec-CH-UA client hints) to the
LazyOwn browser sync receiver, so every request the recorder proxy forwards
(`auto_loop`, `apt_chain`, `auto_pwn`, or anything routed through it) reuses
your genuine browser session instead of anonymous automation traffic.

## Install

1. Start the receiver in LazyOwn and copy the token:

   ```
   browsersync start
   ```

2. Open `chrome://extensions` (also works in Brave), enable **Developer
   mode**, click **Load unpacked** and select this directory
   (`browser_sync_extension/`).

3. Click the extension icon, paste the receiver token, adjust the endpoint
   (`http://127.0.0.1:8898/__lazyown/sync` by default) and press **Save**,
   then **Sync now**.

## What it sends

- All cookies of the current profile (`chrome.cookies.getAll`).
- `User-Agent` and `navigator.languages`.
- `Sec-CH-UA`, `Sec-CH-UA-Mobile`, `Sec-CH-UA-Platform` client hints.

The payload goes to loopback only and is authenticated with the runtime
token shown by `browsersync token`. Values never leave the machine unless
the proxied targets receive them.

## How the proxy uses it

`modules/browser_sync.py` stores the profile in `sessions/browser_sync/`
(`profile.json` + a Netscape `cookies.jar`) and `modules/lazy_proxy.py`
injects the matching cookies and fingerprint headers into every exchange.
Burp-style Match and Replace rules can be added to
`sessions/browser_sync/rules.json`:

```json
[
  {"type": "header_set", "match": "Referer", "replace": "https://example.com/"},
  {"type": "body_replace", "match": "password=[^&]*", "replace": "password=x"}
]
```

Rule types: `header_replace`, `header_add`, `header_set`, `header_remove`,
`body_replace`.

Toggle the whole behaviour with `assign browser_sync_inject False`.
