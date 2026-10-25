"""Lab runtime: Docker lifecycle for practice targets and cyber ranges.

Pure subprocess-free-of-shell lifecycle helpers shared by the ``lab``
command set, the gym challenge starter and the exit cleanup hook. Every
command runs in argv list form (``shell=False`` semantics) with bounded
timeouts; nothing here talks to a shell.

Scenarios live in :data:`LAB_SCENARIOS`; cyber range profiles in
:data:`RANGE_PROFILES`. Containers are named ``lazyown-lab-<scenario>``
so the cleanup pass can find every machine the framework launched.
"""

from __future__ import annotations

import secrets
import subprocess
from pathlib import Path

from modules.metasploitable_migrations import apply_migrations as _apply_migrations

BASE_DIR = Path(__file__).resolve().parent.parent
LAB_COMPOSE = BASE_DIR / "deploy" / "lab" / "docker-compose.yml"
RANGE_DIR = BASE_DIR / "deploy" / "range"

REGISTRY_PREFIX = "lazyown-lab-"
RANGE_PREFIX = "lazyown-range-"

DOCKER_TIMEOUT_SEC = 10
DOCKER_SHORT_TIMEOUT_SEC = 5
DOCKER_INSPECT_TIMEOUT_SEC = 15

LAB_SCENARIOS: dict[str, dict] = {
    "wordpress": {
        "image": "vulnerables/web-dvwa:latest",
        "ports": {"80/tcp": 8080},
        "description": "Damn Vulnerable Web Application -- OWASP Top 10 practice",
        "difficulty": "easy",
    },
    "ad-lab": {
        "image": "ghcr.io/semperis/lab-ad:latest",
        "ports": {"389/tcp": 389, "445/tcp": 445, "88/tcp": 88},
        "description": "Active Directory lab with domain controller and workstations",
        "difficulty": "medium",
    },
    "metasploitable": {
        "image": "tleemcjr/metasploitable2:latest",
        "ports": {"21/tcp": 2121, "22/tcp": 2222, "80/tcp": 8081, "445/tcp": 1445},
        "description": "Metasploitable2 -- deliberately vulnerable Linux VM",
        "difficulty": "easy",
    },
    "juice-shop": {
        "image": "bkimminich/juice-shop:latest",
        "ports": {"3000/tcp": 3000},
        "description": "OWASP Juice Shop -- modern vulnerable web application",
        "difficulty": "medium",
    },
    "tomcat": {
        "image": "vulhub/tomcat:8.0",
        "ports": {"8080/tcp": 8888},
        "description": "Apache Tomcat 8.0 -- CVE-2017-12615 and more",
        "difficulty": "medium",
    },
    "struts": {
        "image": "vulhub/struts2:2.3.32",
        "ports": {"8080/tcp": 9090},
        "description": "Apache Struts2 -- CVE-2017-5638 and more",
        "difficulty": "hard",
    },
}

RANGE_PROFILES: dict[str, dict] = {
    "ad-mini": {
        "compose": "ad-mini/docker-compose.yml",
        "description": "Vulnerable mini Active Directory with fake users and background traffic",
        "topology": "dc (AD DS), ws01 (implant target), traffic-gen (fake logons); IPs assigned by Docker, resolved at start",
        "difficulty": "medium",
    },
}


def docker_available() -> bool:
    """Return whether the Docker daemon is reachable."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=DOCKER_TIMEOUT_SEC,
            check=False,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False


def _docker(*args: str, timeout: int = DOCKER_INSPECT_TIMEOUT_SEC, text: bool = False) -> subprocess.CompletedProcess:
    """Run one docker argv; never raises for the CLI's own exit codes."""
    try:
        return subprocess.run(["docker", *args], capture_output=True, text=text, timeout=timeout, check=False)
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
        return subprocess.CompletedProcess(args, 127, "", str(exc))


def running_containers() -> list[str]:
    """Return the running lab container names."""
    result = _docker(
        "ps",
        "--format",
        "{{.Names}}",
        "--filter",
        f"name={REGISTRY_PREFIX}",
        timeout=DOCKER_SHORT_TIMEOUT_SEC,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in (result.stdout or "").splitlines() if line.strip()]


def existing_containers() -> list[str]:
    """Return every lab container name including stopped ones."""
    result = _docker(
        "ps",
        "-a",
        "--format",
        "{{.Names}}",
        "--filter",
        f"name={REGISTRY_PREFIX}",
        timeout=DOCKER_SHORT_TIMEOUT_SEC,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in (result.stdout or "").splitlines() if line.strip()]


def running_range_containers() -> list[str]:
    """Return the running cyber range container names."""
    result = _docker(
        "ps",
        "--format",
        "{{.Names}}",
        "--filter",
        f"name={RANGE_PREFIX}",
        timeout=DOCKER_SHORT_TIMEOUT_SEC,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in (result.stdout or "").splitlines() if line.strip()]


def container_name(scenario: str) -> str:
    """Return the container name for one lab scenario."""
    return f"{REGISTRY_PREFIX}{scenario}"


def container_ip(container_name: str) -> str:
    """Resolve one container's IPv4 on its Docker network."""
    result = _docker(
        "inspect",
        "--format",
        "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}",
        container_name,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return (result.stdout or "").strip()


def ensure_web(scenario: str, name: str) -> None:
    """Start Apache inside a metasploitable container that booted without it."""
    if scenario != "metasploitable":
        return
    _docker(
        "exec",
        name,
        "sh",
        "-c",
        "service apache2 start >/dev/null 2>&1 || true",
        timeout=30,
    )


def apply_gym_migrations(name: str) -> dict:
    """Apply the metasploitable gym migrations, returning the report."""
    try:
        return dict(_apply_migrations(name) or {})
    except Exception:
        return {}


def start(scenario: str) -> dict:
    """Spin up one lab scenario container.

    Args:
        scenario: Scenario key from :data:`LAB_SCENARIOS`.

    Returns:
        Mapping with ``success``, ``already``, ``container``, ``ip``,
        ``ports`` and ``error`` keys.
    """
    info = LAB_SCENARIOS.get(scenario)
    if info is None:
        return {"success": False, "error": f"unknown scenario: {scenario}", "ports": {}}
    name = container_name(scenario)
    if name in running_containers():
        ensure_web(scenario, name)
        return {
            "success": True,
            "already": True,
            "container": name,
            "ip": container_ip(name),
            "ports": dict(info.get("ports", {})),
            "error": "",
        }
    pull = _docker("pull", info["image"], timeout=600, text=True)
    if pull.returncode != 0:
        return {"success": False, "error": f"pull failed: {(pull.stderr or pull.stdout or '')[-300:]}", "ports": {}}
    stale = name in existing_containers()
    if stale:
        _docker("rm", "-f", name, timeout=DOCKER_INSPECT_TIMEOUT_SEC)
    cmd = ["run", "-d", "-i", "--rm", "--name", name]
    for container_port, host_port in info.get("ports", {}).items():
        cmd.extend(["-p", f"{host_port}:{container_port.split('/')[0]}"])
    cmd.append(info["image"])
    run = _docker(*cmd, timeout=120, text=True)
    if run.returncode != 0:
        return {"success": False, "error": (run.stderr or run.stdout or "")[-300:], "ports": {}}
    ensure_web(scenario, name)
    return {
        "success": True,
        "already": False,
        "container": name,
        "ip": container_ip(name),
        "ports": dict(info.get("ports", {})),
        "error": "",
    }


def stop(scenario: str) -> dict:
    """Stop one lab scenario container.

    Args:
        scenario: Scenario key from :data:`LAB_SCENARIOS`.

    Returns:
        Mapping with ``success`` and ``error`` keys.
    """
    name = container_name(scenario)
    if name not in running_containers():
        return {"success": False, "error": f"{scenario} is not running"}
    result = _docker("stop", name, timeout=DOCKER_INSPECT_TIMEOUT_SEC)
    if result.returncode != 0:
        return {"success": False, "error": (result.stderr or "")[-200:]}
    return {"success": True, "error": ""}


def stop_all() -> dict:
    """Stop every running lab container.

    Returns:
        Mapping with ``stopped`` (container name list) and ``failed``
        (name to error) keys.
    """
    stopped: list[str] = []
    failed: dict[str, str] = {}
    for name in running_containers():
        result = _docker("stop", name, timeout=DOCKER_INSPECT_TIMEOUT_SEC)
        if result.returncode == 0:
            stopped.append(name)
        else:
            failed[name] = (result.stderr or "")[-200:]
    return {"stopped": stopped, "failed": failed}


def range_compose(profile: str) -> Path | None:
    """Return the compose file path for one range profile, or None."""
    info = RANGE_PROFILES.get(profile)
    if info is None:
        return None
    compose = RANGE_DIR / info["compose"]
    return compose if compose.exists() else None


def start_range(profile: str) -> dict:
    """Start one cyber range profile via Docker Compose.

    Args:
        profile: Range profile key from :data:`RANGE_PROFILES`.

    Returns:
        Mapping with ``success``, ``compose`` and ``error`` keys.
    """
    compose = range_compose(profile)
    if compose is None:
        return {"success": False, "error": f"unknown range profile or missing compose: {profile}", "compose": ""}
    admin_password = ensure_range_secret(compose.parent)
    result = _docker_compose(["-f", str(compose), "up", "-d"])
    if result.returncode != 0:
        return {"success": False, "error": (result.stderr or result.stdout or "")[-300:], "compose": str(compose)}
    return {"success": True, "error": "", "compose": str(compose), "admin_password": admin_password}


def stop_range(profile: str) -> dict:
    """Stop one cyber range profile (compose down)."""
    compose = range_compose(profile)
    if compose is None:
        return {"success": False, "error": f"unknown range profile or missing compose: {profile}"}
    result = _docker_compose(["-f", str(compose), "down", "-v"])
    if result.returncode != 0:
        return {"success": False, "error": (result.stderr or result.stdout or "")[-300:]}
    return {"success": True, "error": ""}


def stop_ranges() -> dict:
    """Stop every running cyber range.

    Tries ``docker compose down`` for declared profiles first; any
    remaining ``lazyown-range-*`` containers fall back to ``docker stop``.

    Returns:
        Mapping with ``stopped`` and ``failed`` keys.
    """
    stopped: list[str] = []
    failed: dict[str, str] = {}
    running = running_range_containers()
    if not running:
        return {"stopped": stopped, "failed": failed}
    for profile in RANGE_PROFILES:
        compose = range_compose(profile)
        if compose is None:
            continue
        still = running_range_containers()
        if not still:
            break
        result = _docker_compose(["-f", str(compose), "down", "-v"])
        if result.returncode == 0:
            stopped.extend(name for name in running_range_containers() if name not in still)
    for name in running_range_containers():
        result = _docker("stop", name, timeout=DOCKER_INSPECT_TIMEOUT_SEC)
        if result.returncode == 0:
            stopped.append(name)
        else:
            failed[name] = (result.stderr or "")[-200:]
    return {"stopped": stopped, "failed": failed}


def _docker_compose(args: list[str]) -> subprocess.CompletedProcess:
    """Run one docker compose argv."""
    try:
        return subprocess.run(["docker", "compose", *args], capture_output=True, text=True, timeout=300, check=False)
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
        return subprocess.CompletedProcess(args, 127, "", str(exc))


def ensure_range_secret(profile_dir: Path) -> str:
    """Generate the DC admin secret file when missing.

    Args:
        profile_dir: Range profile directory holding the compose file.

    Returns:
        The Administrator password string, or empty on failure.
    """
    secrets_dir = profile_dir / "secrets"
    secret_file = secrets_dir / "samba-admin-password.txt"
    try:
        if secret_file.exists():
            return secret_file.read_text(encoding="utf-8").strip()
        secrets_dir.mkdir(parents=True, exist_ok=True)
        password = f"Range-{secrets.token_urlsafe(12)}!"
        secret_file.write_text(password, encoding="utf-8")
        try:
            secret_file.chmod(0o600)
        except OSError:
            pass
        return password
    except OSError:
        return ""


__all__ = [
    "BASE_DIR",
    "LAB_COMPOSE",
    "LAB_SCENARIOS",
    "RANGE_DIR",
    "RANGE_PROFILES",
    "RANGE_PREFIX",
    "REGISTRY_PREFIX",
    "apply_gym_migrations",
    "container_ip",
    "container_name",
    "docker_available",
    "ensure_range_secret",
    "ensure_web",
    "existing_containers",
    "range_compose",
    "running_containers",
    "running_range_containers",
    "start",
    "start_range",
    "stop",
    "stop_all",
    "stop_range",
    "stop_ranges",
]
