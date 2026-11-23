"""Native payload builders: Donut shellcode and Garble obfuscated builds.

Single home for the two native build pipelines the framework ships:

- :func:`build_donut_shellcode` wraps the optional ``donut`` package
  (same dependency ``do_lazymetashellcode`` uses) and reads its knobs
  from ``payload.json`` (``donut_*`` keys).
- :func:`build_garble` drives the ``garble`` Go obfuscator binary with
  ``core.safe_exec.safe_run_argv`` (``shell=False`` always) and reads
  its knobs from the ``garble_*`` keys.

Both builders raise :class:`PayloadNativeError` on missing tools or
failed builds so CLI surfaces can print a single typed error.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from core.safe_exec import safe_run_argv

DONUT_ARCH_CODES: dict[str, int] = {"x86": 1, "x64": 2, "x86+x64": 3, "any": 3}
DONUT_FORMAT_CODES: dict[str, int] = {"bin": 1, "exe": 2, "raw": 1, "dll": 2}
DONUT_EXIT_CODES: dict[str, int] = {"thread": 1, "process": 2, "none": 3}
GARBLE_LEVEL_FLAGS: dict[str, tuple[str, ...]] = {
    "minimal": (),
    "standard": ("-literals",),
    "max": ("-literals", "-tiny"),
}
GARBLE_BUILD_TIMEOUT_SEC = 900.0


class PayloadNativeError(RuntimeError):
    """Raised when a native payload build cannot produce its artefact."""


def _payload() -> dict[str, Any]:
    from core.config import load_payload

    return load_payload()


def build_donut_shellcode(
    input_file: str,
    *,
    config: dict[str, Any] | None = None,
    output: str | None = None,
) -> Path:
    """Generate shellcode from an executable with the Donut engine.

    Args:
        input_file: PE/EXE/.NET assembly input path.
        config: Payload dict; loaded lazily when omitted.
        output: Override for the ``donut_out`` artefact path.

    Returns:
        The written shellcode artefact path.

    Raises:
        PayloadNativeError: When ``donut`` is not importable, the input
            is missing or the engine fails.
    """
    try:
        import donut
    except ImportError as exc:
        raise PayloadNativeError("donut package not available: pip install donut-shellcode") from exc
    source = Path(input_file)
    if not source.is_file():
        raise PayloadNativeError(f"input file not found: {source}")
    payload = config if config is not None else _payload()
    arch = str(payload.get("donut_arch", "x64") or "x64")
    fmt = str(payload.get("donut_format", "bin") or "bin")
    exit_opt = str(payload.get("donut_exit_opt", "thread") or "thread")
    kwargs: dict[str, Any] = {"file": str(source)}
    attempts: tuple[dict[str, Any], ...] = (
        {
            "arch": DONUT_ARCH_CODES.get(arch, 2),
            "o_format": DONUT_FORMAT_CODES.get(fmt, 1),
            "exit_opt": DONUT_EXIT_CODES.get(exit_opt, 1),
            "bypass": bool(payload.get("donut_bypass", True)),
            "compress": bool(payload.get("donut_compress", True)),
        },
        kwargs,
    )
    result = None
    last_error: Exception | None = None
    for attempt in attempts:
        try:
            result = donut.create(**attempt)
            break
        except TypeError as exc:
            last_error = exc
        except Exception as exc:
            raise PayloadNativeError(f"donut build failed: {exc}") from exc
    if result is None:
        raise PayloadNativeError(f"donut build failed: {last_error}")
    out_path = Path(output or str(payload.get("donut_out", "sessions/donut.bin") or "sessions/donut.bin"))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(bytes(result))
    return out_path


def garble_command(
    level: str,
    seed: str,
    lit: bool,
    tiny: bool,
    source: str,
    output: str,
) -> list[str]:
    """Return the argv for one ``garble build`` invocation.

    Args:
        level: Obfuscation level (``minimal``/``standard``/``max``).
        seed: ``random`` or a fixed hex seed.
        lit: Whether to add ``-literals``.
        tiny: Whether to add ``-tiny``.
        source: Go package directory or import path to build.
        output: Output binary path for ``-o``.

    Returns:
        The argv list (``garble`` binary resolved by the caller).
    """
    argv = ["garble"]
    flags = list(GARBLE_LEVEL_FLAGS.get(level, ()))
    if lit and "-literals" not in flags:
        flags.append("-literals")
    if tiny and "-tiny" not in flags:
        flags.append("-tiny")
    argv.extend(flags)
    if seed and seed != "random":
        argv.extend(["-seed", seed])
    argv.extend(["build", "-o", output, source])
    return argv


def build_garble(
    source: str,
    *,
    config: dict[str, Any] | None = None,
    output: str | None = None,
) -> Path:
    """Build an obfuscated Go binary with garble.

    Args:
        source: Go package directory or import path to build.
        config: Payload dict; loaded lazily when omitted.
        output: Override for the output binary path (defaults under
            ``garble_out``).

    Returns:
        The built binary path.

    Raises:
        PayloadNativeError: When the ``garble`` binary is missing or the
            build fails.
    """
    garble_path = shutil.which("garble")
    if not garble_path:
        raise PayloadNativeError("garble binary not found: go install mvdan.cc/garble@latest")
    payload = config if config is not None else _payload()
    level = str(payload.get("garble_level", "standard") or "standard")
    seed = str(payload.get("garble_seed", "random") or "random")
    lit = bool(payload.get("garble_lit", False))
    tiny = bool(payload.get("garble_tiny", False))
    out_dir = Path(str(payload.get("garble_out", "sessions/garble_build") or "sessions/garble_build"))
    out_dir.mkdir(parents=True, exist_ok=True)
    binary_name = Path(source).name or "garble_build"
    out_path = Path(output) if output else out_dir / binary_name
    argv = [garble_path, *garble_command(level, seed, lit, tiny, source, str(out_path))[1:]]
    result = safe_run_argv(argv, timeout=GARBLE_BUILD_TIMEOUT_SEC)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise PayloadNativeError(f"garble build failed (rc={result.returncode}): {detail[-500:]}")
    if not out_path.is_file():
        raise PayloadNativeError(f"garble build produced no artefact: {out_path}")
    return out_path
