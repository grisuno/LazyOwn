"""Lab environment commands -- spin up vulnerable practice targets.

Provides on-demand CTF-style lab scenarios powered by Docker containers.
Operators can practice techniques against realistic targets without
risking production systems.
"""

from __future__ import annotations

import subprocess
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
        """Check if Docker is installed and running."""
        try:
            subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=5,
                check=False,
            )
            return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
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

        Examples:
            lab start metasploitable
            lab start wordpress
            lab list
            lab status
            lab stop metasploitable

        Requires Docker. Lab containers are isolated and safe for practice.
        """
        args = line.strip().split()
        if not args:
            print_msg("Usage: lab [list|start|stop|status] [scenario]")
            print_msg("Try: lab list")
            return

        action = args[0].lower()
        scenario = args[1] if len(args) > 1 else ""

        if action == "list":
            self._lab_list()
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
            print_error(f"Unknown action: {action}. Use list, start, stop, or status.")

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
