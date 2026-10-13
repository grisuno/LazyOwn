"""Per-task Docker sandbox for the Lazy autonomous loop.

Ports the per-flow container idea with Lazy semantics: one container per
loop task, built from the existing ``Dockerfile.sandbox`` image
(``lazyown-sandbox`` by default, the same tag ``./run`` uses), with the
repository mounted at ``/app`` exactly like the documented sandbox usage.
Workers keep issuing Lazy shell verbs; the sandbox executor pipes each
verb into the in-container shell over stdin (``<verb>`` + ``exit``) and
captures the cleaned output, so Guard, scope, traffic and intel see the
same transcript shape as host execution.

Safety profile: no privileged flag, all capabilities dropped except
``NET_RAW`` (nmap needs raw sockets), memory/CPU caps, operator-owned
network selection. The image is never auto-built inside a round (a build
takes minutes and would wedge the loop); a missing image returns a
capability-style error the worker records as a fact.

Stdlib only. All Docker interaction goes through the ``docker`` CLI so no
SDK dependency is needed.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import threading

DEFAULT_IMAGE = "lazyown-sandbox"
CONTAINER_PREFIX = "lazy-loop-"
REPO_MOUNT = "/app"
DEFAULT_MEMORY = "2g"
DEFAULT_CPUS = "2.0"
EXEC_TIMEOUT_SEC = 600.0
OUTPUT_TAIL_CHARS = 4000

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[mGKH]")
_CONTAINER_LOCK = threading.Lock()


def _payload_value(key: str, default: str = "") -> str:
    """Read one payload value, falling back to default on any error."""
    try:
        from core.config import load_payload

        value = (load_payload() or {}).get(key, default)
        return str(value or default or "")
    except Exception:
        return str(default or "")


def image_name(configured: str = "") -> str:
    """Resolve the sandbox image name.

    Args:
        configured: Explicit image from the ``--sandbox`` flag.

    Returns:
        Explicit image, payload ``sandbox_image`` override, or default.
    """
    clean = (configured or "").strip()
    if clean:
        return clean
    return _payload_value("sandbox_image", DEFAULT_IMAGE) or DEFAULT_IMAGE


def container_name(task_id: str) -> str:
    """Return the deterministic container name for one task."""
    slug = re.sub(r"[^a-z0-9-]+", "-", str(task_id or "").strip().lower()).strip("-")
    return f"{CONTAINER_PREFIX}{slug or 'task'}"[:120]


def docker_available() -> bool:
    """Return True when the docker CLI is on PATH."""
    return shutil.which("docker") is not None


def image_available(image: str = "") -> bool:
    """Return True when the sandbox image exists locally."""
    if not docker_available():
        return False
    try:
        out = subprocess.run(
            ["docker", "images", "--format", "{{.Repository}}"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return (image or image_name()) in (out.stdout or "").split()
    except Exception:
        return False


def container_running(task_id: str) -> str:
    """Return the container name when it is up, else empty string."""
    if not docker_available():
        return ""
    try:
        out = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        names = (out.stdout or "").split()
        wanted = container_name(task_id)
        return wanted if wanted in names else ""
    except Exception:
        return ""


def ensure_container(task_id: str, image: str = "") -> str:
    """Start the per-task container when needed, return its name or error.

    Args:
        task_id: Loop task identifier.
        image: Explicit image override.

    Returns:
        Container name on success, ``execution failed: ...`` otherwise.
    """
    running = container_running(task_id)
    if running:
        return running
    if not docker_available():
        return "execution failed: docker CLI not installed, cannot sandbox this step"
    resolved = image_name(image)
    if not image_available(resolved):
        return f"execution failed: sandbox image '{resolved}' missing (run: lazy_sandbox build)"
    import os as _os

    repo = str(_os.getcwd())
    try:
        from pathlib import Path as _Path

        repo = str(_Path(__file__).resolve().parent.parent)
    except Exception:
        pass
    network = _payload_value("sandbox_network", "") or "bridge"
    memory = _payload_value("sandbox_memory", DEFAULT_MEMORY) or DEFAULT_MEMORY
    cpus = _payload_value("sandbox_cpus", DEFAULT_CPUS) or DEFAULT_CPUS
    argv = [
        "docker",
        "run",
        "-d",
        "--name",
        container_name(task_id),
        "--cap-drop",
        "ALL",
        "--cap-add",
        "NET_RAW",
        "--memory",
        memory,
        "--cpus",
        cpus,
        "--network",
        network,
        "-v",
        f"{repo}:{REPO_MOUNT}",
        "-w",
        REPO_MOUNT,
        "-e",
        "TERM=xterm-256color",
        resolved,
        "sleep",
        "infinity",
    ]
    with _CONTAINER_LOCK:
        if container_running(task_id):
            return container_name(task_id)
        try:
            proc = subprocess.run(argv, capture_output=True, text=True, timeout=120)
        except Exception as exc:
            return f"execution failed: sandbox start failed: {exc}"
    if proc.returncode != 0:
        return f"execution failed: sandbox start failed: {(proc.stderr or '')[:300]}"
    return container_name(task_id)


def exec_command(task_id: str, command: str, timeout_sec: float = 0.0, image: str = "") -> str:
    """Run one Lazy shell verb inside the task container.

    Args:
        task_id: Loop task identifier.
        command: Lazy shell verb line.
        timeout_sec: Hard timeout for the exec.
        image: Explicit image override.

    Returns:
        Cleaned shell output, timeout notice with partial tail, or error.
    """
    name = ensure_container(task_id, image)
    if name.startswith("execution failed:"):
        return name
    limit = max(30.0, float(timeout_sec or EXEC_TIMEOUT_SEC))
    stdin_data = f"{(command or '').strip()}\nexit\n"
    try:
        proc = subprocess.run(
            ["docker", "exec", "-i", name, "python3", f"{REPO_MOUNT}/lazyown.py"],
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=limit,
        )
    except subprocess.TimeoutExpired as exc:
        partial = _ANSI_RE.sub("", str(exc.stdout or exc.output or ""))
        tail = f"\n[partial output, {len(partial)} chars]\n{partial[-OUTPUT_TAIL_CHARS:]}" if partial.strip() else ""
        return f"TIMEOUT: sandbox verb exceeded {limit}s: {(command or '')[:120]}{tail}"
    except Exception as exc:
        return f"execution failed: sandbox exec failed: {exc}"
    return _ANSI_RE.sub("", proc.stdout or "").strip()


def remove_container(task_id: str) -> bool:
    """Stop and remove the task container. Never raises."""
    try:
        subprocess.run(["docker", "rm", "-f", container_name(task_id)], capture_output=True, timeout=60)
        return True
    except Exception:
        return False


def status(task_id: str = "") -> dict:
    """Describe sandbox readiness and containers.

    Args:
        task_id: Optional task to inspect.

    Returns:
        Readiness dict with docker, image and container state.
    """
    info: dict = {
        "docker": docker_available(),
        "image": image_name(),
        "image_available": image_available(),
    }
    if (task_id or "").strip():
        info["container"] = container_name(task_id)
        info["running"] = bool(container_running(task_id))
    else:
        try:
            out = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True, timeout=30
            )
            info["running"] = [n for n in (out.stdout or "").split() if n.startswith(CONTAINER_PREFIX)]
        except Exception:
            info["running"] = []
    return info


def executor_for(task_id: str, image: str = ""):
    """Build a worker executor routing shell verbs into the sandbox.

    Args:
        task_id: Loop task identifier bound to one container.
        image: Explicit image override from ``--sandbox``.

    Returns:
        Executor callable, or None when Docker is unusable (caller keeps
        host execution and the worker records the gap as usual).
    """
    if not docker_available() or not image_available(image_name(image)):
        return None

    def _sandbox_executor(command: str) -> str:
        return exec_command(task_id, command)

    return _sandbox_executor


__all__ = [
    "container_name",
    "container_running",
    "docker_available",
    "ensure_container",
    "exec_command",
    "executor_for",
    "image_available",
    "image_name",
    "remove_container",
    "status",
]
