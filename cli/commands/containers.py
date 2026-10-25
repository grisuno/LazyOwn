"""Container and Kubernetes attack command set.

Commands for Docker enumeration, Kubernetes cluster reconnaissance,
pod escape detection, and container privilege escalation.
"""

from __future__ import annotations

import json
import os

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    BLUE,
    GREEN,
    RED,
    RESET,
    YELLOW,
    print_error,
    print_msg,
    print_succ,
    print_warn,
)

CONTAINER_CATEGORY = "18. Container & Kubernetes"


class ContainerCommandSet(LazyOwnCommandSet):
    """Container and Kubernetes attack commands."""

    phase = "container"
    category = CONTAINER_CATEGORY

    @cmd2.with_category(CONTAINER_CATEGORY)
    def do_docker_enum(self, _line):
        """Enumerate Docker host: containers, images, privileges, mounts.

        Checks for:
        - Privileged containers
        - Docker socket mounts (escape vector)
        - Sensitive host path mounts
        - Dangerous Linux capabilities

        Usage: docker_enum
        """
        try:
            from modules.lazyk8s import DockerEnumerator
        except ImportError as exc:
            print_error(f"Container module not available: {exc}")
            return

        enumerator = DockerEnumerator()
        print_msg(f"{BLUE}[*] Enumerating Docker environment...{RESET}")

        results = enumerator.full_check()
        sessions_dir = self.params.get("sessions_dir", "sessions")
        os.makedirs(sessions_dir, exist_ok=True)

        with open(os.path.join(sessions_dir, "docker_enum.json"), "w") as f:
            json.dump(results, f, indent=2, default=str)

        print_msg(f"{'=' * 70}")
        print_msg("  Docker Enumeration Results")
        print_msg(f"{'=' * 70}")
        print_msg(f"  Docker socket     : {'ACCESSIBLE' if results.get('docker_socket_accessible') else 'not found'}")
        print_msg(f"  Containers        : {results.get('containers_count', 0)}")
        print_msg(f"  Images            : {results.get('images_count', 0)}")

        priv = results.get("privileged_containers", [])
        if priv:
            print_succ(f"\n{GREEN}[+] PRIVILEGED CONTAINERS ({len(priv)}):{RESET}")
            for p in priv:
                print_msg(f"  {p.get('id', '?')}  {p.get('name', '?')}  [{p.get('image', '?')}]")

        mounts = results.get("sensitive_mounts", [])
        if mounts:
            print_warn(f"\n{YELLOW}[!] SENSITIVE MOUNTS:{RESET}")
            for m in mounts:
                print_msg(
                    f"  {m.get('container_name', '?')}: {m.get('mount_source', '?')} -> {m.get('mount_dest', '?')}"
                )

        socket_mounts = results.get("docker_socket_mounts", [])
        if socket_mounts:
            print_succ(f"\n{GREEN}[+] DOCKER SOCKET MOUNTS (ESCAPE POSSIBLE):{RESET}")
            for s in socket_mounts:
                print_msg(f"  {s.get('container_name', '?')}")
                print_msg(f"    Escape: {s.get('technique', '')}")

        caps = results.get("dangerous_capabilities", [])
        if caps:
            print_warn(f"\n{YELLOW}[!] DANGEROUS CAPABILITIES:{RESET}")
            for c in caps:
                print_msg(f"  {c.get('container_name', '?')}: {', '.join(c.get('dangerous_capabilities', []))}")

        print_succ("\nResults saved to sessions/docker_enum.json")

    @cmd2.with_category(CONTAINER_CATEGORY)
    def do_k8s_enum(self, _line):
        """Enumerate Kubernetes cluster: pods, secrets, SAs, RBAC.

        Checks for:
        - All namespaces and pods
        - Secrets (kubeconfig, tokens, credentials)
        - Service accounts with cluster-admin
        - Pod escape vectors (hostPID, privileged, mounts)

        Usage: k8s_enum
        """
        try:
            from modules.lazyk8s import K8sEnumerator
        except ImportError as exc:
            print_error(f"Container module not available: {exc}")
            return

        enumerator = K8sEnumerator()
        print_msg(f"{BLUE}[*] Enumerating Kubernetes cluster...{RESET}")

        results = enumerator.full_check(
            sessions_dir=self.params.get("sessions_dir", "sessions"),
        )

        print_msg(f"{'=' * 70}")
        print_msg("  Kubernetes Enumeration Results")
        print_msg(f"{'=' * 70}")
        print_msg(f"  Namespaces        : {len(results.get('namespaces', []))}")
        print_msg(f"  Pods total        : {results.get('pods_total', 0)}")
        print_msg(f"  Secrets found     : {len(results.get('secrets', []))}")
        print_msg(f"  Service accounts  : {len(results.get('service_accounts', []))}")

        rbac = results.get("rbac", {})
        print_msg(f"  Can list secrets  : {rbac.get('can_list_secrets', False)}")
        print_msg(f"  Can create pods   : {rbac.get('can_create_pods', False)}")
        if rbac.get("cluster_admin"):
            print_succ(f"  {GREEN}CLUSTER ADMIN{RESET}")

        escape = results.get("escape_vectors", [])
        if escape:
            print_succ(f"\n{GREEN}[+] POD ESCAPE VECTORS:{RESET}")
            for ev in escape:
                print_msg(f"  [{ev.get('severity', '?')}] {ev.get('title', '?')}")
                print_msg(f"    {ev.get('description', '?')}")
                print_msg(f"    MITRE: {ev.get('mitre_technique', '?')}")

        secrets = results.get("secrets", [])
        if secrets:
            print_msg(f"\n{YELLOW}[*] Secrets discovered:{RESET}")
            for s in secrets[:20]:
                ns = s.get("namespace", "default")
                name = s.get("name", "?")
                keys = s.get("data_keys", [])
                decoded = s.get("decoded", {})
                print_msg(f"  {ns}/{name}: keys={keys}")

                if decoded:
                    for key, value in decoded.items():
                        if len(str(value)) > 80:
                            value = str(value)[:80] + "..."
                        print_msg(f"    {key}: {value}")

                creds_file = os.path.join(self.params.get("sessions_dir", "sessions"), f"k8s_secrets_{ns}_{name}.txt")
                with open(creds_file, "w") as f:
                    for key, value in decoded.items():
                        f.write(f"{key}: {value}\n")

    @cmd2.with_category(CONTAINER_CATEGORY)
    def do_container_escape(self, _line):
        """Check current container for known escape vectors.

        Detects:
        - Docker socket mounted
        - Privileged mode
        - Host PID namespace shared
        - Dangerous capabilities (SYS_ADMIN, SYS_PTRACE)
        - Service account tokens (K8s)
        - Sensitive host mounts

        Usage: container_escape
        """
        try:
            from modules.lazyk8s import ContainerEscapeTechniques
        except ImportError as exc:
            print_error(f"Container module not available: {exc}")
            return

        env = ContainerEscapeTechniques.detect_current_environment()

        print_msg(f"{'=' * 70}")
        print_msg("  Container Escape Assessment")
        print_msg(f"{'=' * 70}")
        print_msg(f"  In container      : {env.get('in_container', False)}")
        print_msg(f"  Kubernetes        : {env.get('is_kubernetes', False)}")
        print_msg(f"  Privileged        : {env.get('privileged', False)}")
        print_msg(f"  Host PID namespace: {env.get('host_pid_namespace', False)}")
        print_msg(f"  Docker socket     : {env.get('docker_socket_accessible', False)}")

        caps = env.get("capabilities", [])
        if caps:
            print_msg("\n  Capabilities:")
            for cap in caps:
                print_msg(f"    {cap}")

        print_msg(f"\n{'=' * 70}")
        print_msg("  Applicable Escape Techniques")
        print_msg(f"{'=' * 70}")

        applicable: list[dict] = []
        for tech in ContainerEscapeTechniques.ESCAPE_TECHNIQUES:
            requires = set(tech.get("requires", []))
            satisfied = True
            for req in requires:
                if req == "privileged" and not env.get("privileged"):
                    satisfied = False
                elif req == "docker_socket" and not env.get("docker_socket_accessible"):
                    satisfied = False
                elif req == "SYS_ADMIN" and not any("sys_admin" in c.lower() for c in caps):
                    satisfied = False
                elif req == "SYS_PTRACE" and not any("sys_ptrace" in c.lower() for c in caps):
                    satisfied = False
                elif req == "host_pid" and not env.get("host_pid_namespace"):
                    satisfied = False
                elif req == "k8s_sa_token" and not env.get("is_kubernetes"):
                    satisfied = False
            if satisfied:
                applicable.append(tech)

        if applicable:
            for tech in applicable:
                print_succ(f"\n  {GREEN}[+] {tech['name']}{RESET}")
                print_msg(f"    {tech['description']}")
                print_msg(f"    MITRE: {tech['mitre']}")
                print_msg(f"    {tech['command']}")
        else:
            print_warn("  No applicable escape techniques detected.")

    @cmd2.with_category(CONTAINER_CATEGORY)
    def do_k8s_pods(self, line):
        """List Kubernetes pods with security-relevant details.

        Shows pod status, hostNetwork, hostPID, privileged status,
        and namespace for each pod.

        Usage:
            k8s_pods
            k8s_pods <namespace>
        """
        try:
            from modules.lazyk8s import K8sEnumerator
        except ImportError as exc:
            print_error(f"Container module not available: {exc}")
            return

        namespace = line.strip()
        enumerator = K8sEnumerator()
        pods = enumerator.list_pods(namespace)

        if not pods:
            print_warn("No pods found or kubectl not configured.")
            return

        print_msg(f"{'NAME':<50} {'NAMESPACE':<20} {'STATUS':<12} {'HOSTNET':<8} {'HOSTPID':<8}")
        print_msg(f"{'-' * 50} {'-' * 20} {'-' * 12} {'-' * 8} {'-' * 8}")

        for pod in pods:
            metadata = pod.get("metadata", {})
            spec = pod.get("spec", {})
            status = pod.get("status", {})

            name = metadata.get("name", "?")[:48]
            ns = metadata.get("namespace", "default")[:18]
            phase = status.get("phase", "?")
            host_net = "YES" if spec.get("hostNetwork", False) else "no"
            host_pid = "YES" if spec.get("hostPID", False) else "no"

            phase_color = GREEN if phase == "Running" else YELLOW
            print_msg(f"  {name:<48}  {ns:<18}  {phase_color}{phase:<10}{RESET}  {host_net:<6}  {host_pid:<6}")

        print_msg(f"\n  Total pods: {len(pods)}")

    @cmd2.with_category(CONTAINER_CATEGORY)
    def do_k8s_secrets(self, line):
        """List and decode Kubernetes secrets.

        Extracts and decodes all secrets from the cluster, writing
        credentials and tokens to sessions/k8s_secrets_*.txt files.

        Usage:
            k8s_secrets
            k8s_secrets <namespace>
        """
        try:
            from modules.lazyk8s import K8sEnumerator
        except ImportError as exc:
            print_error(f"Container module not available: {exc}")
            return

        namespace = line.strip()
        enumerator = K8sEnumerator()
        secrets = enumerator.list_secrets(namespace)

        if not secrets:
            print_warn("No secrets found or insufficient permissions.")
            return

        sessions_dir = self.params.get("sessions_dir", "sessions")
        os.makedirs(sessions_dir, exist_ok=True)
        creds_file = os.path.join(sessions_dir, "k8s_credentials.txt")

        with open(creds_file, "w") as out:
            for s in secrets:
                ns = s.get("namespace", "default")
                name = s.get("name", "?")
                stype = s.get("type", "")
                decoded = s.get("decoded", {})
                print_succ(f"\n{GREEN}[+] {ns}/{name} ({stype}){RESET}")

                if decoded:
                    for key, value in decoded.items():
                        out.write(f"[{ns}/{name}] {key}: {value}\n")
                        if len(str(value)) > 100:
                            value = str(value)[:100] + "..."
                        print_msg(f"    {key}: {value}")
                else:
                    keys = s.get("data_keys", [])
                    print_msg(f"    keys: {', '.join(keys)}")
                    for key in keys:
                        out.write(f"[{ns}/{name}] {key}: [base64-encoded]\n")

        print_succ(f"\nCredentials written to {creds_file}")

    @cmd2.with_category(CONTAINER_CATEGORY)
    def do_container_detect(self, _line):
        """Auto-detect container runtime and escape primitives.

        Detects the container runtime (Docker, containerd, CRI-O, Podman,
        LXC, Kubernetes, systemd-nspawn), then enumerates dangerous mounts,
        capabilities, and applicable escape techniques.

        Usage: container_detect
        """
        try:
            from modules.lazyk8s import ContainerRuntimeDetector
        except ImportError as exc:
            print_error(f"Container module not available: {exc}")
            return

        print_msg(f"{BLUE}[*] Auto-detecting container environment...{RESET}")
        results = ContainerRuntimeDetector.auto_detect_all()

        runtime = results["runtime"]
        env = results["environment"]

        print_msg(f"{'=' * 70}")
        print_msg("  Container Auto-Detection Report")
        print_msg(f"{'=' * 70}")
        print_msg(f"  Runtime detected   : {runtime['runtime']} (confidence: {runtime['confidence']})")
        print_msg(f"  Indicators         : {', '.join(runtime['indicators'][:5])}")
        if runtime.get("all_scores") and len(runtime["all_scores"]) > 1:
            others = {k: v for k, v in runtime["all_scores"].items() if k != runtime["runtime"]}
            if others:
                print_msg(f"  Other runtimes     : {others}")

        print_msg(f"\n  In container       : {env.get('in_container', False)}")
        print_msg(f"  Privileged         : {env.get('privileged', False)}")
        print_msg(f"  Host PID namespace : {env.get('host_pid_namespace', False)}")
        print_msg(f"  Docker socket      : {env.get('docker_socket_accessible', False)}")
        print_msg(f"  Is Kubernetes      : {env.get('is_kubernetes', False)}")

        mounts = results.get("dangerous_mounts", {})
        if mounts:
            print_warn(f"\n{YELLOW}[!] DANGEROUS MOUNTS:{RESET}")
            for category, entries in mounts.items():
                for entry in entries:
                    print_msg(f"  [{category}] {entry}")

        caps = results.get("dangerous_capabilities", [])
        if caps:
            print_warn(f"\n{YELLOW}[!] DANGEROUS CAPABILITIES:{RESET}")
            for cap in caps:
                print_msg(f"  {cap}")

        techniques = results.get("applicable_techniques", [])
        if techniques:
            print_succ(f"\n{GREEN}[+] APPLICABLE ESCAPE TECHNIQUES ({len(techniques)}):{RESET}")
            for tech in techniques:
                print_succ(f"  {GREEN}{tech['name']}{RESET}")
                print_msg(f"    {tech['description']}")
                print_msg(f"    MITRE: {tech['mitre']}")
                print_msg(f"    Command: {tech['command']}")
        else:
            print_warn("\n  No applicable escape techniques automatically detected.")

        print_msg(f"\n{YELLOW}Escape Score: {results['escape_score']}/100{RESET}")
        severity_color = RED if results["escape_score"] >= 90 else YELLOW if results["escape_score"] >= 50 else RESET
        print_msg(f"  {severity_color}{results['assessment_summary']}{RESET}")

        sessions_dir = self.params.get("sessions_dir", "sessions")
        os.makedirs(sessions_dir, exist_ok=True)
        out_path = os.path.join(sessions_dir, "container_detect.json")
        with open(out_path, "w") as f:
            json.dump(
                {
                    "runtime": results["runtime"],
                    "environment": results["environment"],
                    "mounts": {k: v for k, v in results["dangerous_mounts"].items()},
                    "capabilities": results["dangerous_capabilities"],
                    "techniques": [t["name"] for t in techniques],
                    "score": results["escape_score"],
                    "summary": results["assessment_summary"],
                },
                f,
                indent=2,
                default=str,
            )
        print_msg(f"\nResults saved to {out_path}")


__all__ = ["ContainerCommandSet"]
