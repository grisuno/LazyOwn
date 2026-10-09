"""Disposable infrastructure commands -- redirectors, C2, cloud IaC.

Provides ``infra redirector``, ``infra deploy`` and ``infra destroy``
workflows on top of ``deploy/`` assets. Local Docker is the default;
cloud providers (DigitalOcean/AWS) run through Terraform when available.

Discovery is automatic: ``cli.registry.register_command_sets`` finds this
``CommandSet`` because it subclasses ``LazyOwnCommandSet``.
"""

from __future__ import annotations

import json
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

import cmd2

from cli.commands._base import LazyOwnCommandSet, extract_flag
from cli.confirm import confirm
from utils import (
    command_and_control_category,
    print_error,
    print_msg,
    print_succ,
    print_warn,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEPLOY_DIR = BASE_DIR / "deploy"
REDIRECTOR_COMPOSE = DEPLOY_DIR / "redirector" / "docker-compose.yml"
C2_COMPOSE = DEPLOY_DIR / "c2" / "docker-compose.yml"
TERRAFORM_DIR = DEPLOY_DIR / "infra" / "providers"
CF_LOG = BASE_DIR / "cf.log"
REDIRECTOR_STATE = BASE_DIR / "sessions" / "redirectors.json"

TUNNEL_URL_PATTERN = re.compile(r"https://[-0-9a-z]+\.trycloudflare\.com")
VALID_PROVIDERS = frozenset({"local", "docker", "digitalocean", "aws"})
VALID_REGIONS_DO = frozenset({"nyc1", "nyc3", "sfo3", "ams3", "fra1"})
DEFAULT_C2_PORT = 4444
TERRAFORM_TIMEOUT = 600
STALE_AFTER_SECONDS = 86400
SPAWN_POLL_ATTEMPTS = 9
SPAWN_POLL_INTERVAL = 5


def _run_capture(argv: list[str], timeout: int = 60) -> subprocess.CompletedProcess[str]:
    """Run a command capturing output without shell injection.

    Args:
        argv: Argument vector, never a shell string.
        timeout: Seconds before aborting.

    Returns:
        CompletedProcess with captured text output.
    """
    return subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False)


def _binary_present(name: str) -> bool:
    """Check whether a binary exists on PATH.

    Args:
        name: Binary name to locate.

    Returns:
        True when found on PATH.
    """
    return shutil.which(name) is not None


def _parse_tunnel_urls(log_text: str) -> list[str]:
    """Extract unique trycloudflare URLs from cloudflared logs.

    Args:
        log_text: Raw log content.

    Returns:
        Deduplicated URL list preserving order.
    """
    seen: list[str] = []
    for match in TUNNEL_URL_PATTERN.findall(log_text):
        if match not in seen:
            seen.append(match)
    return seen


class InfraCommandSet(LazyOwnCommandSet):
    """Manage disposable C2 infrastructure and redirectors."""

    phase = "c2"
    category = command_and_control_category

    def _c2_port(self) -> int:
        """Resolve the C2 port from params with a safe default.

        Returns:
            C2 port number.
        """
        try:
            return int(self.params.get("c2_port", DEFAULT_C2_PORT))
        except (TypeError, ValueError):
            return DEFAULT_C2_PORT

    def _load_state(self) -> dict:
        """Load redirector state file.

        Returns:
            State dict, empty when missing or corrupt.
        """
        try:
            if REDIRECTOR_STATE.exists():
                return json.loads(REDIRECTOR_STATE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass
        return {"redirectors": []}

    def _save_state(self, state: dict) -> None:
        """Persist redirector state file.

        Args:
            state: State dict to write.
        """
        try:
            REDIRECTOR_STATE.parent.mkdir(parents=True, exist_ok=True)
            REDIRECTOR_STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")
        except OSError as exc:
            print_warn(f"Could not persist redirector state: {exc}")

    @cmd2.with_category(command_and_control_category)
    def do_infra(self, line):
        """Manage disposable C2 infrastructure.

        Usage:
            infra redirector spawn [--count N] [--port PORT]
            infra redirector list
            infra redirector kill --all
            infra deploy --provider local|docker|digitalocean|aws [--region nyc1]
            infra destroy --provider local|docker|digitalocean|aws
            infra status

        Examples:
            infra redirector spawn --count 2
            infra deploy --provider local
            infra deploy --provider digitalocean --region nyc1
            infra destroy --provider local
        """
        args = shlex.split(line)
        if not args:
            print_msg("Usage: infra [redirector|deploy|destroy|status] [options]")
            return
        action = args[0].lower()
        rest = args[1:]
        if action == "redirector":
            self._infra_redirector(rest)
        elif action == "deploy":
            self._infra_deploy(rest)
        elif action == "destroy":
            self._infra_destroy(rest)
        elif action == "status":
            self._infra_status()
        else:
            print_error(f"Unknown infra action: {action}")

    def _infra_redirector(self, args: list[str]) -> None:
        """Dispatch redirector subcommands.

        Args:
            args: Tokens after ``redirector``.
        """
        if not args:
            print_msg("Usage: infra redirector [spawn|list|kill] [options]")
            return
        sub = args[0].lower()
        rest = args[1:]
        if sub == "spawn":
            count = extract_flag(rest, "--count") or "1"
            port = extract_flag(rest, "--port") or str(self._c2_port())
            try:
                count_int = max(1, min(5, int(count)))
            except ValueError:
                print_error("--count must be an integer 1-5")
                return
            try:
                port_int = int(port)
            except ValueError:
                print_error("--port must be an integer")
                return
            self._redirector_spawn(count_int, port_int)
        elif sub == "list":
            self._redirector_list()
        elif sub == "kill":
            self._redirector_kill(rest)
        else:
            print_error(f"Unknown redirector action: {sub}")

    def _redirector_spawn(self, count: int, port: int) -> None:
        """Spawn disposable cloudflared redirectors via Docker Compose.

        Args:
            count: Number of redirector replicas.
            port: Local C2 port to expose through the tunnel.
        """
        if not _binary_present("docker"):
            print_error("Docker is required. Install: sudo apt install docker.io")
            return
        if not REDIRECTOR_COMPOSE.exists():
            print_error(f"Missing compose file: {REDIRECTOR_COMPOSE}")
            return
        print_msg(f"[*] Spawning {count} disposable redirector(s) for C2 port {port} ...")
        cmd = ["docker", "compose", "-f", str(REDIRECTOR_COMPOSE), "up", "-d", "--scale", f"redirector={count}"]
        try:
            result = _run_capture(cmd, timeout=120)
        except (subprocess.TimeoutExpired, OSError) as exc:
            print_error(f"Docker compose failed: {exc}")
            return
        if result.returncode != 0:
            print_error(f"Docker compose failed: {result.stderr[-2000:]}")
            return
        print_succ("Redirector containers started. Waiting for fresh tunnel URLs ...")
        known_before = {entry.get("url", "") for entry in self._load_state().get("redirectors", [])}
        fresh: list[str] = []
        for _attempt in range(SPAWN_POLL_ATTEMPTS):
            try:
                logs = _run_capture(
                    ["docker", "compose", "-f", str(REDIRECTOR_COMPOSE), "logs", "--tail", "200"],
                    timeout=30,
                )
                for url in _parse_tunnel_urls(logs.stdout + logs.stderr):
                    if url not in known_before and url not in fresh:
                        fresh.append(url)
            except (subprocess.TimeoutExpired, OSError):
                pass
            if fresh:
                break
            try:
                time.sleep(SPAWN_POLL_INTERVAL)
            except OSError:
                break
        now = int(time.time())
        state = self._load_state()
        for url in fresh:
            entry = {"url": url, "port": port, "provider": "cloudflared-quick", "created_at": now}
            if not any(r.get("url") == url for r in state["redirectors"]):
                state["redirectors"].append(entry)
        self._save_state(state)
        if fresh:
            print_succ(f"Fresh tunnel URLs ({len(fresh)}):")
            for url in fresh:
                print_msg(f"  {url} -> 127.0.0.1:{port} (filtered: /gmail/* only)")
            print_msg("Next step (order matters, URLs bake into the beacon at build time):")
            print_msg(f"  assign c2_fallback_urls {','.join(fresh)}")
            print_msg("  c2 linux 2   (rebuilds the beacon with these redirectors)")
        else:
            print_warn("No fresh tunnel URL yet. Tunnels can take ~60s; retry: infra redirector list")

    def _redirector_list(self) -> None:
        """List known redirector URLs with age, pruning stale entries."""
        state = self._load_state()
        known = state.get("redirectors", [])
        if CF_LOG.exists():
            try:
                for url in _parse_tunnel_urls(CF_LOG.read_text(errors="replace")):
                    if not any(r.get("url") == url for r in known):
                        known.append({"url": url, "port": self._c2_port(), "provider": "cloudflared-quick"})
            except OSError:
                pass
        now = int(time.time())
        fresh_known = [r for r in known if now - int(r.get("created_at", now)) <= STALE_AFTER_SECONDS]
        pruned = len(known) - len(fresh_known)
        if pruned:
            state["redirectors"] = fresh_known
            self._save_state(state)
            print_warn(f"Pruned {pruned} stale redirector(s) older than 24h. Quick tunnels die with their container.")
        if not fresh_known:
            print_msg("No redirectors registered. Use: infra redirector spawn --count 2")
            return
        print_msg(f"Redirectors ({len(fresh_known)}):")
        for entry in fresh_known:
            age_hours = (now - int(entry.get("created_at", now))) // 3600
            print_msg(f"  {entry.get('url')} -> 127.0.0.1:{entry.get('port')} [{entry.get('provider')}, {age_hours}h old]")
        print_warn("Quick-tunnel URLs die when their container stops. Rebuild the beacon after every fresh spawn.")

    def _redirector_kill(self, args: list[str]) -> None:
        """Tear down redirector containers and clear state.

        Args:
            args: Expected to contain ``--all``.
        """
        if "--all" not in args:
            print_error("Usage: infra redirector kill --all")
            return
        if REDIRECTOR_COMPOSE.exists() and _binary_present("docker"):
            try:
                _run_capture(["docker", "compose", "-f", str(REDIRECTOR_COMPOSE), "down", "-v"], timeout=60)
            except (subprocess.TimeoutExpired, OSError) as exc:
                print_warn(f"Compose down reported: {exc}")
        self._save_state({"redirectors": []})
        print_succ("All redirectors destroyed and state cleared.")

    def _infra_deploy(self, args: list[str]) -> None:
        """Deploy ephemeral C2 infrastructure locally or in the cloud.

        Args:
            args: CLI tokens including ``--provider`` and ``--region``.
        """
        provider = (extract_flag(args, "--provider") or "").lower()
        region = (extract_flag(args, "--region") or "nyc1").lower()
        if not provider:
            provider = self._ask_provider()
        if provider not in VALID_PROVIDERS:
            print_error(f"Provider must be one of: {sorted(VALID_PROVIDERS)}")
            return
        if provider in ("local", "docker"):
            self._deploy_local()
        else:
            self._deploy_cloud(provider, region)

    def _ask_provider(self) -> str:
        """Interactively ask for local vs cloud deployment.

        Returns:
            Provider string, defaulting to local on non-interactive stdin.
        """
        if not sys.stdin.isatty():
            return "local"
        try:
            answer = input("Deploy locally or in the cloud? [local/cloud] (local): ").strip().lower()
        except (EOFError, KeyboardInterrupt, OSError):
            return "local"
        if answer in ("cloud", "digitalocean"):
            return "digitalocean"
        if answer in ("aws",):
            return "aws"
        return "local"

    def _deploy_local(self) -> None:
        """Bring up the local C2 stack with automatic TLS via Caddy."""
        if not _binary_present("docker"):
            print_error("Docker is required for local deploy.")
            return
        if not C2_COMPOSE.exists():
            print_error(f"Missing compose file: {C2_COMPOSE}")
            return
        print_msg("[*] Deploying local ephemeral C2 stack (lazyown + caddy TLS) ...")
        try:
            result = _run_capture(["docker", "compose", "-f", str(C2_COMPOSE), "up", "-d"], timeout=180)
        except (subprocess.TimeoutExpired, OSError) as exc:
            print_error(f"Local deploy failed: {exc}")
            return
        if result.returncode != 0:
            print_error(f"Local deploy failed: {result.stderr[-2000:]}")
            return
        print_succ("Local C2 deployed. Caddy terminates TLS, lazyown listens on 127.0.0.1:4444.")
        print_msg("Next: infra redirector spawn --count 2")

    def _deploy_cloud(self, provider: str, region: str) -> None:
        """Deploy cloud infrastructure through Terraform.

        Args:
            provider: Cloud provider id (digitalocean/aws).
            region: Region slug, validated for DigitalOcean.
        """
        if not _binary_present("terraform"):
            print_error("Terraform is required for cloud deploy. See deploy/infra/README.md")
            return
        if provider == "digitalocean" and region not in VALID_REGIONS_DO:
            print_error(f"Region must be one of: {sorted(VALID_REGIONS_DO)}")
            return
        tf_dir = TERRAFORM_DIR / provider
        if not tf_dir.exists():
            print_error(f"No Terraform module for provider: {provider} ({tf_dir})")
            return
        print_warn(f"This will create billable {provider} resources in {region}.")
        if not confirm(f"Deploy ephemeral C2 to {provider}/{region}?", default=False):
            print_msg("Deploy cancelled.")
            return
        print_msg(f"[*] terraform init/apply in {tf_dir} ...")
        try:
            init = _run_capture(["terraform", "-chdir=" + str(tf_dir), "init", "-input=false"], timeout=180)
            if init.returncode != 0:
                print_error(f"terraform init failed: {init.stderr[-2000:]}")
                return
            apply = _run_capture(
                ["terraform", "-chdir=" + str(tf_dir), "apply", "-auto-approve", "-input=false", f"-var=region={region}"],
                timeout=TERRAFORM_TIMEOUT,
            )
        except (subprocess.TimeoutExpired, OSError) as exc:
            print_error(f"Terraform deploy failed: {exc}")
            return
        if apply.returncode != 0:
            print_error(f"terraform apply failed: {apply.stderr[-3000:]}")
            return
        print_succ(f"Cloud C2 provisioned on {provider}/{region}. Check terraform output for IPs.")
        print_msg("Next: configure DNS + infra redirector spawn --count 2")

    def _infra_destroy(self, args: list[str]) -> None:
        """Destroy ephemeral infrastructure for a provider.

        Args:
            args: CLI tokens including ``--provider``.
        """
        provider = (extract_flag(args, "--provider") or "local").lower()
        if provider in ("local", "docker"):
            if C2_COMPOSE.exists() and _binary_present("docker"):
                try:
                    _run_capture(["docker", "compose", "-f", str(C2_COMPOSE), "down", "-v"], timeout=120)
                except (subprocess.TimeoutExpired, OSError) as exc:
                    print_warn(f"Compose down reported: {exc}")
            self._redirector_kill(["--all"])
            print_succ("Local ephemeral infrastructure destroyed.")
            return
        tf_dir = TERRAFORM_DIR / provider
        if not tf_dir.exists() or not _binary_present("terraform"):
            print_error(f"Cannot destroy: missing terraform module or binary for {provider}")
            return
        if not confirm(f"Destroy ALL {provider} infra managed by {tf_dir}?", default=False):
            print_msg("Destroy cancelled.")
            return
        try:
            result = _run_capture(["terraform", "-chdir=" + str(tf_dir), "destroy", "-auto-approve", "-input=false"], timeout=TERRAFORM_TIMEOUT)
        except (subprocess.TimeoutExpired, OSError) as exc:
            print_error(f"Terraform destroy failed: {exc}")
            return
        if result.returncode != 0:
            print_error(f"terraform destroy failed: {result.stderr[-3000:]}")
            return
        print_succ(f"Cloud infrastructure on {provider} destroyed.")

    def _infra_status(self) -> None:
        """Show local containers, terraform state, and redirector URLs."""
        print_msg("Infrastructure status:")
        if _binary_present("docker"):
            try:
                result = _run_capture(["docker", "ps", "--format", "{{.Names}} {{.Status}}"], timeout=15)
                lazy = [line for line in result.stdout.splitlines() if "lazyown" in line or "caddy" in line or "redirector" in line or "cloudflared" in line]
                if lazy:
                    for line_out in lazy:
                        print_msg(f"  [docker] {line_out}")
                else:
                    print_msg("  [docker] no lazyown/caddy/redirector containers running")
            except (subprocess.TimeoutExpired, OSError):
                print_warn("  [docker] status unavailable")
        else:
            print_msg("  [docker] not installed")
        self._redirector_list()


__all__ = ["InfraCommandSet"]
