"""LazyOob shell commands: local OOB canary for blind SSRF/RCE callbacks."""

from __future__ import annotations

import shlex

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    CYAN,
    GREEN,
    RESET,
    miscellaneous_category,
    print_error,
    print_msg,
    print_succ,
    print_warn,
)


class LazyOobCommandSet(LazyOwnCommandSet):
    """Operate the local out-of-band callback canary."""

    @cmd2.with_category(miscellaneous_category)
    def do_lazyoob(self, line):
        """Run a local HTTP callback canary.

        Usage:
            lazyoob start [host] [port]   start listener (defaults: lhost, ephemeral)
            lazyoob url [token]           print the callback URL
            lazyoob hits [token]          show observed callbacks
            lazyoob stop                  stop the listener
        """
        from modules import lazy_oob

        args = shlex.split(line.strip()) if line.strip() else []
        action = args[0].lower() if args else "hits"
        if action == "start":
            host = args[1] if len(args) > 1 else ""
            try:
                port = int(args[2]) if len(args) > 2 else 0
            except ValueError:
                print_error("port must be a number")
                return
            result = lazy_oob.start(host=host, port=port)
            if not result.get("ok"):
                print_error(f"canary start failed: {result.get('error')}")
                return
            state = "already running" if result.get("already") else "started"
            print_succ(f"OOB canary {state}")
            print_msg(f"  Callback URL: {CYAN}{result['url']}{RESET}")
            print_msg(f"  Inject into payloads and check: lazyoob hits {result['token']}")
            return
        if action == "url":
            target = args[1] if len(args) > 1 else ""
            callback = lazy_oob.url(target)
            if not callback:
                print_warn("Canary not running; use: lazyoob start")
                return
            print_msg(f"  {GREEN}{callback}{RESET}")
            return
        if action == "hits":
            target = args[1] if len(args) > 1 else ""
            rows = lazy_oob.hits(target)
            if not rows:
                print_msg("No callbacks observed yet.")
                return
            for row in rows:
                print(f"  {CYAN}{row['token']}{RESET} {row['method']} {row['source']} -> {row['path']}")
            return
        if action == "stop":
            result = lazy_oob.stop()
            if result.get("ok"):
                print_succ(f"Canary stopped ({result['hits']} hit(s) recorded)")
            else:
                print_error(f"stop failed: {result.get('error')}")
            return
        print_error("Unknown action; usage: lazyoob start|url|hits|stop")
