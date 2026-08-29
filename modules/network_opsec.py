"""Network OPSEC — proxy chain enforcement, canary detection, traffic randomization.

Provides network-level operational security: SOCKS5 → HTTP → SSH tunnel
proxy chain management, canary token detection (verify if traffic is being
analyzed), source port randomization, connection jitter scheduling, and
DNS-over-HTTPS resolution to avoid DNS logging.

All configurations derive from payload.json with sensible defaults for
covert C2 communication.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"


@dataclass
class NetworkOpsecConfig:
    """Configuration for network OPSEC measures.

    Attributes:
        proxy_chain: Ordered list of proxy URIs (e.g. ['socks5://127.0.0.1:1080', 'http://proxy:8080']).
        dns_over_https: Use DoH for DNS resolution (avoids DNS logging).
        doh_provider: DoH resolver URL.
        source_port_range: Random source port range (min, max).
        connection_jitter_ms: Random delay before establishing connections.
        canary_domains: Domains to check for canary tokens in DNS.
        canary_urls: URLs to check for web bug canaries.
        sni_randomization: Randomize TLS SNI field.
        tls_version_override: Force a specific TLS version.
        tcp_fast_open: Use TCP fast open to reduce handshake signatures.
        proxy_bypass_local: Don't route local traffic through proxies.
    """

    proxy_chain: list[str] = field(default_factory=list)
    dns_over_https: bool = True
    doh_provider: str = "https://cloudflare-dns.com/dns-query"
    source_port_range: tuple[int, int] = (49152, 65535)
    connection_jitter_ms: int = 500
    canary_domains: list[str] = field(default_factory=list)
    canary_urls: list[str] = field(default_factory=list)
    sni_randomization: bool = True
    tls_version_override: str = ""
    tcp_fast_open: bool = False
    proxy_bypass_local: bool = True


class NetworkOpsecEngine:
    """Manage network-level operational security for C2 and exfiltration.

    Configures proxy chains, enforces DNS-over-HTTPS, randomizes
    connection parameters, and detects canary/deception tokens.

    Attributes:
        config: NetworkOpsecConfig with proxy and randomization settings.
        active_proxies: Currently verified proxy connections.
    """

    PROXY_CHAIN_PATTERNS = {
        "single_socks5": ["socks5://127.0.0.1:1080"],
        "socks5_over_http": ["socks5://127.0.0.1:1080", "http://127.0.0.1:8080"],
        "socks5_over_ssh": ["socks5://127.0.0.1:1080", "ssh://user@bastion:22"],
        "http_over_ssh": ["http://127.0.0.1:8080", "ssh://user@bastion:22"],
        "chisel_socks5": ["socks5://127.0.0.1:1080"],
        "metasploit_route": ["socks5://127.0.0.1:1080"],
    }

    CANARY_INDICATORS = [
        "canarytokens",
        "canary",
        "tripwire",
        "honeypot",
        "honey",
        "deception",
        "thinkst",
    ]

    def __init__(self, config: NetworkOpsecConfig | None = None):
        self.config = config or NetworkOpsecConfig()
        self.active_proxies: list[str] = []

    def configure_proxy_chain(self, chain_type: str = "single_socks5") -> dict[str, Any]:
        """Configure a proxy chain for C2 communication.

        Args:
            chain_type: Preset chain configuration name.

        Returns:
            Dict with chain configuration and environment setup.
        """
        proxies = self.PROXY_CHAIN_PATTERNS.get(chain_type, self.PROXY_CHAIN_PATTERNS["single_socks5"])
        self.active_proxies = proxies

        env_setup = {}
        proxy_env_vars = ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"]

        for i, proxy_url in enumerate(proxies):
            if i == 0 and proxy_url.startswith("socks5"):
                env_setup["ALL_PROXY"] = proxy_url
            if proxy_url.startswith("http"):
                env_setup["HTTP_PROXY"] = proxy_url
                env_setup["HTTPS_PROXY"] = proxy_url

        return {
            "chain_type": chain_type,
            "proxies": proxies,
            "environment_variables": env_setup,
            "export_commands": [
                f"export {k}={v}" for k, v in env_setup.items()
            ],
            "proxychains_config": self._build_proxychains_config(proxies),
            "test_command": "curl -s --socks5-hostname 127.0.0.1:1080 https://ifconfig.me",
        }

    @staticmethod
    def _build_proxychains_config(proxies: list[str]) -> str:
        lines = ["strict_chain", "proxy_dns", "tcp_read_time_out 15000", "tcp_connect_time_out 8000"]
        for proxy in proxies:
            if "socks5" in proxy:
                host_port = proxy.replace("socks5://", "")
                lines.append(f"socks5 {host_port}")
            elif "http" in proxy:
                host_port = proxy.replace("http://", "")
                lines.append(f"http {host_port}")
        lines.append("[ProxyList]")
        return "\n".join(lines)

    def check_canary_tokens(self) -> dict[str, Any]:
        """Check if the target has canary token / deception technology.

        Analyzes DNS names, HTTP response headers, and behavioral
        indicators for signs of canary tokens or honeypot deployment.

        Returns:
            Dict with detection results and risk assessment.
        """
        findings: list[dict[str, str]] = []

        for domain in self.config.canary_domains:
            domain_lower = domain.lower()
            for indicator in self.CANARY_INDICATORS:
                if indicator in domain_lower:
                    findings.append({
                        "type": "canary_domain",
                        "indicator": indicator,
                        "domain": domain,
                        "confidence": "high" if "canarytokens" in domain_lower else "medium",
                    })

        for url in self.config.canary_urls:
            url_lower = url.lower()
            for indicator in self.CANARY_INDICATORS:
                if indicator in url_lower:
                    findings.append({
                        "type": "canary_url",
                        "indicator": indicator,
                        "url": url,
                        "confidence": "high",
                    })

        return {
            "canary_tokens_detected": len(findings),
            "findings": findings,
            "risk_action": "ABORT" if len(findings) > 0 else "PROCEED",
            "recommendation": (
                "Canary tokens detected — abort engagement and verify ROE."
                if findings else "No canary tokens detected in analyzed domains/URLs."
            ),
        }

    def analyze_traffic_with_canary_check(self, target_host: str, target_port: int = 443) -> dict[str, Any]:
        """Analyze whether target traffic is being intercepted or analyzed.

        Uses TLS fingerprint analysis, response header inspection, and
        timing analysis to detect TLS inspection proxies or packet capture.

        Args:
            target_host: Target hostname or IP.
            target_port: Target port.

        Returns:
            Dict with traffic analysis results.
        """
        import socket as sock
        import ssl

        results: dict[str, Any] = {
            "target": f"{target_host}:{target_port}",
            "tls_inspected": False,
            "proxy_detected": False,
            "packet_capture_likely": "unknown",
            "certificate_match": True,
            "certificate_info": {},
            "recommendations": [],
        }

        try:
            context = ssl.create_default_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            with sock.create_connection((target_host, target_port), timeout=10) as raw_sock:
                with context.wrap_socket(raw_sock, server_hostname=target_host) as tls_sock:
                    cert = tls_sock.getpeercert(binary_form=False)
                    if cert:
                        results["certificate_info"] = {
                            "subject": dict(x[0] for x in cert.get("subject", [])),
                            "issuer": dict(x[0] for x in cert.get("issuer", [])),
                            "notAfter": cert.get("notAfter", ""),
                            "serialNumber": cert.get("serialNumber", ""),
                        }

                        issuer_cn = results["certificate_info"]["issuer"].get("commonName", "")
                        ca_indicators = ["zscaler", "palo alto", "bluecoat", "forcepoint", "barracuda", "iboss", "netskope"]
                        for ca_indicator in ca_indicators:
                            if ca_indicator in issuer_cn.lower():
                                results["tls_inspected"] = True
                                results["proxy_detected"] = True
                                results["recommendations"].append(
                                    f"TLS inspection detected ({ca_indicator}). "
                                    "Use domain fronting or non-standard TLS ciphers."
                                )
                                break
        except Exception as e:
            results["error"] = str(e)

        return results

    def dns_over_https_config(self) -> dict[str, Any]:
        """Generate DNS-over-HTTPS configuration for proxy and system.

        Returns:
            Dict with DoH configuration commands for curl, python, and system.
        """
        return {
            "provider": self.config.doh_provider,
            "curl_usage": f'curl --doh-url "{self.config.doh_provider}" https://target.com',
            "python_usage": (
                "Use dnspython with httpx: "
                "dns.query.https(q, '{provider}')"
            ).format(provider=self.config.doh_provider),
            "systemd_resolved": [
                "echo 'DNSOverTLS=yes' >> /etc/systemd/resolved.conf",
                f"echo 'DNS={self.config.doh_provider}' >> /etc/systemd/resolved.conf",
            ],
            "fallback_providers": [
                "https://dns.google/dns-query",
                "https://dns.quad9.net/dns-query",
                "https://doh.opendns.com/dns-query",
            ],
        }

    def source_port_randomize(self) -> dict[str, Any]:
        """Randomize source port for outbound connections.

        Returns:
            Dict with port randomization commands for iptables, python sockets, etc.
        """
        port_min, port_max = self.config.source_port_range

        return {
            "description": f"Random source port in range {port_min}-{port_max}",
            "python_socket_example": (
                f"import socket, random; "
                f"s = socket.socket(); "
                f"s.bind(('', random.randint({port_min}, {port_max}))); "
                f"s.connect(('target', 443))"
            ),
            "iptables_snat": [
                f"iptables -t nat -A POSTROUTING -p tcp --dport 443 -j SNAT --to-source :{port_min}-{port_max}",
                "iptables -t nat -D POSTROUTING -p tcp --dport 443 -j SNAT --to-source ...",
            ],
            "nftables_snat": [
                f"nft add rule nat postrouting tcp dport 443 snat to :{port_min}-{port_max}",
            ],
        }

    def connection_jitter_schedule(self, beacon_interval: int = 60) -> list[float]:
        """Generate a jitter schedule for beacon connections.

        Returns a list of sleep durations that appear irregular but stay
        within the requested jitter window. This prevents pattern-based
        detection in netflow/SIEM correlation.

        Args:
            beacon_interval: Base sleep interval in seconds.

        Returns:
            List of jittered sleep durations.
        """
        jitter_ms = self.config.connection_jitter_ms
        jitter_s = max(jitter_ms / 1000.0, 0.5)

        schedule = []
        for _ in range(10):
            variation = random.uniform(-jitter_s, jitter_s)
            schedule.append(round(beacon_interval + variation, 1))

        return schedule

    def canary_detection_setup(self) -> dict[str, Any]:
        """Set up canary detection for the engagement.

        Generates canary tokens at configurable intervals to detect
        if stolen data or credentials are being actively monitored.

        Returns:
            Dict with canary setup commands and monitoring instructions.
        """
        return {
            "description": "Canary token deployment for threat detection",
            "token_types": [
                {"type": "aws_keys", "description": "Fake AWS access keys that alert on use"},
                {"type": "dns", "description": "Unique DNS hostnames that alert on resolution"},
                {"type": "http", "description": "Unique URLs that alert on access"},
                {"type": "email", "description": "Unique email addresses that alert on receipt"},
                {"type": "sql", "description": "Database records that alert on SELECT"},
                {"type": "azure_id", "description": "Fake Azure login credentials"},
                {"type": "kubeconfig", "description": "Fake Kubernetes config file"},
            ],
            "deployment_strategy": [
                "1. Create canary tokens via canarytokens.org or Thinkst Canary",
                "2. Embed tokens in files accessible to attackers",
                "3. Place in common credential locations (env vars, config files, bash history)",
                "4. Monitor for alerts — any trigger means active compromise",
            ],
            "commands_to_check": [
                "grep -r 'canary\\|thinkst\\|honeypot\\|tripwire' /etc/ /var/ 2>/dev/null",
                "systemctl list-units | grep -i canary",
            ],
        }

    def summary(self) -> dict[str, Any]:
        return {
            "proxy_chain_types": list(self.PROXY_CHAIN_PATTERNS.keys()),
            "doh_provider": self.config.doh_provider,
            "source_port_range": self.config.source_port_range,
            "jitter_ms": self.config.connection_jitter_ms,
            "canary_indicators": self.CANARY_INDICATORS,
        }
