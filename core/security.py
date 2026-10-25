"""Security helpers for LazyOwn — anti-debug, certificate generation.

Extracted from ``utils.py`` to break the giant monolith and keep
security-critical code in one auditable location.
"""

from __future__ import annotations

import ctypes
import logging
import os
import subprocess
from pathlib import Path

log = logging.getLogger("core.security")


def anti_debug() -> None:
    """Check for debugger attachment and exit if found.

    Reads ``/proc/self/status`` for ``TracerPid``. If a tracer is
    attached and we are not running under a legitimate dev tool
    (gdb, strace, ltrace will show), the process exits immediately.

    This is called at import time by both ``lazyown.py`` and
    ``lazyc2.py``.
    """
    tracer_pid = 0
    try:
        with open("/proc/self/status") as f:
            for line in f:
                if line.startswith("TracerPid:"):
                    tracer_pid = int(line.split(":")[1].strip())
                    break
    except (OSError, ValueError, IndexError):
        return

    if tracer_pid > 0:
        try:
            PR_SET_PTRACER = 0x59616D61
            libc = ctypes.CDLL("libc.so.6")
            libc.prctl(PR_SET_PTRACER, 0, 0, 0, 0)
        except Exception:
            pass

    # ptrace-attempt based anti-debug — if we can ptrace ourselves,
    # no one else is attached. If the call fails, we are being traced.
    try:
        libc = ctypes.CDLL("libc.so.6")
        PTRACE_TRACEME = 0
        result = libc.ptrace(PTRACE_TRACEME, 0, 0, 0)
        if result == -1:
            os._exit(1)
    except Exception:
        os._exit(1)


def generate_certificates(output_dir: str | None = None) -> tuple[str, str]:
    """Generate a self-signed CA certificate and key pair.

    Creates ``cert.pem`` and ``key.pem`` in the current directory (or
    ``output_dir`` if specified). Uses OpenSSL with 4096-bit RSA and
    a 3650-day validity period.

    Args:
        output_dir: Optional directory to write the certificate files
            into. Defaults to the current working directory.

    Returns:
        Tuple of ``(cert_path, key_path)`` absolute paths.
    """
    base = Path(output_dir) if output_dir else Path.cwd()
    cert_path = base / "cert.pem"
    key_path = base / "key.pem"

    if cert_path.exists() and key_path.exists():
        return str(cert_path), str(key_path)

    subj = "/C=XX/ST=LazyOwn/L=RedTeam/O=LazyOwn/CN=LazyOwn C2"
    try:
        subprocess.run(
            [
                "openssl",
                "req",
                "-new",
                "-x509",
                "-days",
                "3650",
                "-nodes",
                "-newkey",
                "rsa:4096",
                "-subj",
                subj,
                "-keyout",
                str(key_path),
                "-out",
                str(cert_path),
            ],
            capture_output=True,
            check=True,
        )
        os.chmod(str(key_path), 0o600)
        os.chmod(str(cert_path), 0o644)
        log.info("Generated certificates: %s, %s", cert_path, key_path)
    except subprocess.CalledProcessError as exc:
        log.error("Certificate generation failed: %s", exc.stderr.decode(errors="replace")[:200])

    return str(cert_path), str(key_path)
