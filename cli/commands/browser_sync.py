"""BrowserSync shell commands: operator browser identity into the proxy."""

from __future__ import annotations

import shlex

import cmd2

from cli.commands._base import LazyOwnCommandSet, extract_flag
from utils import CYAN, GREEN, RESET, miscellaneous_category, print_error, print_msg, print_succ, print_warn


class BrowserSyncCommandSet(LazyOwnCommandSet):
    """Expose the browser identity sync receiver to the operator."""

    phase = "credential_access"
    category = miscellaneous_category

    @cmd2.with_category(miscellaneous_category)
    def do_browsersync(self, line):
        """Sync the real browser session into the recorder proxy.

        Usage:
            browsersync start [port]    start the loopback receiver
            browsersync stop            stop the receiver
            browsersync status          running state, profile stats, token
            browsersync token           print the receiver token
            browsersync reset-token     regenerate the receiver token
            browsersync show [domain] [--full]   list synced cookies (masked by default)
            browsersync jar             print the Netscape jar path and curl usage
            browsersync rules           show the Burp-style Match and Replace rules file
            browsersync test [path] [--http]   preview injected headers for the payload rhost
            browsersync clear           delete the synced profile and cookie jar

        Load browser_sync_extension/ in Chrome or Brave, paste the token in
        the popup and every auto_loop / apt_chain / auto_pwn request that
        goes through the recorder proxy carries your real cookies.
        """
        from modules import browser_sync

        args = shlex.split(line.strip()) if line.strip() else []
        if not args:
            print_msg("Usage: browsersync start|stop|status|token|reset-token|show|jar|rules|test|clear")
            return
        action = args[0]
        if action == "start":
            port = None
            if len(args) > 1:
                try:
                    port = max(0, int(args[1]))
                except ValueError:
                    print_error("start expects a port number (browsersync start [port])")
                    return
            if port is None:
                try:
                    port = int((self.params or {}).get("browser_sync_port", browser_sync.DEFAULT_SYNC_PORT) or browser_sync.DEFAULT_SYNC_PORT)
                except (TypeError, ValueError):
                    port = browser_sync.DEFAULT_SYNC_PORT
            status = browser_sync.start_receiver(port=port)
            if not status.get("running"):
                print_error("receiver failed to start")
                return
            print_succ(f"receiver on {status['host']}:{status['port']}")
            print_msg(f"  endpoint: {CYAN}{status['endpoint']}{RESET}")
            print_msg(f"  token:    {GREEN}{status['token']}{RESET}")
            print_msg("Load browser_sync_extension/ in Chrome or Brave and paste the token.")
            return
        if action == "stop":
            status = browser_sync.stop_receiver()
            if status.get("running"):
                print_error("receiver still running")
                return
            print_succ("receiver stopped")
            return
        if action == "status":
            status = browser_sync.get_receiver().status()
            state = f"{GREEN}running{RESET}" if status.get("running") else "stopped"
            print_msg(f"receiver: {state}")
            if status.get("running"):
                print_msg(f"  endpoint: {status['endpoint']}")
                print_msg(f"  syncs: {status.get('syncs', 0)}  last: {status.get('last_sync', 0.0)}")
            print_msg(f"  cookies: {status.get('cookies', 0)}  age: {status.get('age_sec', 0.0):.0f}s")
            domains = status.get("domains") or []
            preview = ", ".join(domains[:8]) + (f" (+{len(domains) - 8})" if len(domains) > 8 else "")
            print_msg(f"  domains: {preview or '(none)'}")
            return
        if action == "token":
            print_msg(f"{GREEN}{browser_sync.token()}{RESET}")
            return
        if action == "reset-token":
            print_succ(f"new token: {GREEN}{browser_sync.reset_token()}{RESET}")
            print_warn("paste it into the extension popup again")
            return
        if action == "show":
            full = "--full" in args
            domain = extract_flag(args, "--domain") or ""
            positional = [a for a in args[1:] if not a.startswith("--")]
            if positional and not domain:
                domain = positional[0]
            rows = browser_sync.masked_rows(browser_sync.load_profile(), domain, full)
            if not rows:
                print_msg("no synced cookies match")
                return
            if full:
                print_warn("raw cookie values shown; treat output as sensitive material")
            for row in rows:
                print(f"  {row}")
            return
        if action == "jar":
            path = browser_sync.jar_path()
            print_msg(f"cookie jar: {CYAN}{path}{RESET}")
            print_msg("  curl:      curl --cookie '" + path + "' <url>")
            print_msg("  requests:  requests.get(url, cookies=..., headers=...)")
            print_msg("  env:       export CURL_COOKIES=1  (recorder proxy injects them anyway)")
            return
        if action == "rules":
            path = browser_sync._rules_path()
            print_msg(f"rules file: {CYAN}{path}{RESET}")
            print_msg("  types: header_replace | header_add | header_set | header_remove | body_replace")
            print_msg("  example:")
            print_msg('    [{"type": "header_set", "match": "Referer", "replace": "https://example.com/"}]')
            try:
                import json

                text = path.read_text(encoding="utf-8") if path.is_file() else ""
                if text.strip():
                    print(f"  current: {json.dumps(json.loads(text))[:400]}")
            except (OSError, ValueError):
                pass
            return
        if action == "test":
            rhost = str((self.params or {}).get("rhost") or "")
            if not rhost:
                print_error("rhost not set in payload.json")
                return
            positional = [a for a in args[1:] if not a.startswith("--")]
            path = positional[0] if positional else "/"
            scheme = "http" if "--http" in args else "https"
            headers = {"User-Agent": "curl/8.0", "Host": rhost}
            before = dict(headers)
            applied_headers, applied_body = browser_sync.apply_identity_headers(
                rhost, headers, b"", path=path, scheme=scheme
            )
            print_msg(f"request: {scheme}://{rhost}{path}")
            print_msg("before:")
            for name, value in before.items():
                print(f"    {name}: {value}")
            print_msg("after (identity + rules):")
            for name, value in applied_headers.items():
                print(f"    {CYAN}{name}{RESET}: {value}")
            if applied_body:
                print(f"    body bytes: {len(applied_body)}")
            return
        if action == "clear":
            result = browser_sync.clear_profile()
            print_succ(f"removed: {', '.join(result.get('removed') or []) or '(nothing)'}")
            return
        print_error(f"unknown action {action!r}")
