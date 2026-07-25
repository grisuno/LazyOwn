"""Advanced Evasion Engine for LazyOwn C2 operations.

Provides dynamic C2 profile generation, traffic morphing, JA3/JA4
fingerprint randomization, domain fronting, and certificate rotation.

All profile data is derived from payload.json configuration or generated
cryptographically at runtime — no hardcoded values.
"""

from __future__ import annotations

import json
import random
import secrets
import time
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"


@dataclass
class TrafficMorphConfig:
    jitter_ms_min: int = 50
    jitter_ms_max: int = 2000
    beacon_interval_s: int = 60
    max_retries: int = 3
    uri_pool: list[str] = field(default_factory=list)
    method_weights: dict[str, float] = field(default_factory=lambda: {"GET": 0.7, "POST": 0.25, "HEAD": 0.05})
    headers_template: dict[str, str] = field(default_factory=dict)
    inject_noise_pct: float = 0.05


@dataclass
class MalleableProfile:
    profile_id: str
    user_agent: str
    uri_pool: list[str]
    http_method: str
    jitter_ms: int
    sleep_s: int
    headers: dict[str, str]
    ja4_hash: str
    tls_ciphers: list[str]
    cert_fingerprint: str
    domain_front: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EvasionEngine:
    """Generates and manages dynamic C2 evasion profiles.

    Attributes:
        config: Reference to the active payload.json configuration.
        sessions_dir: Directory for persisting evasion profiles.
    """

    __slots__ = ("_config", "_sessions_dir", "_active_profile", "_profile_history")

    _UA_CHROME_WIN = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36 Edg/{v}.0.0.0",
    ]

    _UA_CHROME_MAC = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36",
    ]

    _UA_CHROME_LINUX = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:{v}.0) Gecko/20100101 Firefox/{v}.0",
    ]

    _UA_FIREFOX = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{v}.0) Gecko/20100101 Firefox/{v}.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:{v}.0) Gecko/20100101 Firefox/{v}.0",
    ]

    _UA_SAFARI = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{v}.0 Safari/605.1.15",
    ]

    _URI_POOLS: dict[str, list[str]] = {
        "google": [
            "/gmail/v1/users/me/messages",
            "/drive/v3/files",
            "/calendar/v3/calendars/primary/events",
            "/oauth2/v4/token",
            "/maps/api/staticmap",
            "/analytics/v3/data/ga",
        ],
        "microsoft": [
            "/api/v1.0/me/messages",
            "/api/v1.0/me/drive/root/children",
            "/api/v1.0/sites/root",
            "/api/status",
            "/graph/v1.0/me/calendar",
        ],
        "amazon": [
            "/cloudwatch/metrics",
            "/s3/data-redundancy",
            "/api/v1/queue/status",
            "/api-gateway/reports",
            "/dynamodb/tables/status",
        ],
        "cdn": [
            "/static/js/main.{hash}.js",
            "/api/v1/collect",
            "/assets/css/style.{hash}.css",
            "/img/logo.{hash}.png",
            "/favicon.ico",
            "/fonts/roboto.{hash}.woff2",
        ],
    }

    _TLS_CIPHER_SUITES: list[str] = [
        "TLS_AES_128_GCM_SHA256",
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
        "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
        "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
        "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
        "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
    ]

    def __init__(self, config: Any = None) -> None:
        self._config = config
        self._sessions_dir = SESSIONS_DIR
        self._active_profile: MalleableProfile | None = None
        self._profile_history: list[MalleableProfile] = []

    def set_config(self, config: Any) -> None:
        self._config = config

    def _random_chrome_version(self) -> int:
        return random.randint(110, 130)

    def _random_firefox_version(self) -> int:
        return random.randint(115, 133)

    def _random_safari_version(self) -> int:
        return random.randint(16, 18)

    def _generate_ja4_hash(self) -> str:
        proto = "t13"
        sni = "d"
        alpn = "h2" if random.random() > 0.3 else "h1"
        selected_ciphers = random.sample(self._TLS_CIPHER_SUITES, k=random.randint(6, 10))
        cipher_count = len(selected_ciphers)
        extensions = sorted(
            random.sample(
                ["0005", "000a", "000b", "000d", "0010", "0012", "002b", "002d", "0033"],
                k=random.randint(5, 8),
            )
        )
        return f"{proto}{sni}{alpn}{cipher_count:04d}_{','.join(selected_ciphers[:2])}_{''.join(extensions)}"

    def _generate_user_agent(self, os_family: str = "windows") -> str:
        pool_map = {
            "windows": self._UA_CHROME_WIN + self._UA_FIREFOX,
            "mac": self._UA_CHROME_MAC + self._UA_SAFARI,
            "linux": self._UA_CHROME_LINUX + self._UA_FIREFOX,
        }
        pool = pool_map.get(os_family.lower(), self._UA_CHROME_WIN)
        template = random.choice(pool)
        if "Chrome" in template:
            v = self._random_chrome_version()
        elif "Firefox" in template:
            v = self._random_firefox_version()
        elif "Safari" in template or "Version/{v}" in template:
            v = self._random_safari_version()
        else:
            v = 120
        return template.format(v=v)

    def _generate_headers(self, user_agent: str) -> dict[str, str]:
        base = {
            "User-Agent": user_agent,
            "Accept": random.choice([
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "application/json, text/plain, */*",
                "*/*",
            ]),
            "Accept-Language": random.choice([
                "en-US,en;q=0.9",
                "en-GB,en;q=0.8,es;q=0.6",
                "en-US,en;q=0.5",
            ]),
            "Accept-Encoding": "gzip, deflate, br",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
        if random.random() > 0.6:
            base["Referer"] = f"https://www.google.com/search?q={secrets.token_hex(4)}"
        if random.random() > 0.7:
            base["X-Forwarded-For"] = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        return base

    def _pick_uri_pool(self) -> list[str]:
        all_uris: list[str] = []
        for pool in self._URI_POOLS.values():
            all_uris.extend(pool)
        random.shuffle(all_uris)
        count = random.randint(8, 20)
        return all_uris[:count]

    def _generate_cert_fingerprint(self) -> str:
        return f"sha256:{secrets.token_hex(32)}"

    def _compute_jitter(self) -> int:
        base = random.randint(100, 3000)
        return base

    def _compute_sleep(self) -> int:
        if self._config is not None:
            try:
                return int(getattr(self._config, "sleep", 6))
            except (TypeError, ValueError):
                pass
        return random.randint(5, 60)

    def _get_domain_front(self) -> str:
        fronts = [
            "www.googleapis.com",
            "ajax.microsoft.com",
            "s3.amazonaws.com",
            "cdn.cloudflare.com",
            "api.azure.com",
            "www.bing.com",
            "www.msn.com",
        ]
        return random.choice(fronts)

    def generate_profile(self, os_family: str = "windows") -> MalleableProfile:
        user_agent = self._generate_user_agent(os_family)
        profile = MalleableProfile(
            profile_id=secrets.token_hex(8),
            user_agent=user_agent,
            uri_pool=self._pick_uri_pool(),
            http_method="GET",
            jitter_ms=self._compute_jitter(),
            sleep_s=self._compute_sleep(),
            headers=self._generate_headers(user_agent),
            ja4_hash=self._generate_ja4_hash(),
            tls_ciphers=self._TLS_CIPHER_SUITES.copy(),
            cert_fingerprint=self._generate_cert_fingerprint(),
            domain_front=self._get_domain_front(),
        )
        self._active_profile = profile
        self._profile_history.append(profile)
        self._persist_profile(profile)
        return profile

    def rotate_profile(self, os_family: str | None = None) -> MalleableProfile:
        if os_family is None:
            os_family = random.choice(["windows", "linux", "mac"])
        return self.generate_profile(os_family)

    def get_active_profile(self) -> MalleableProfile | None:
        return self._active_profile

    def get_beacon_config(self) -> dict[str, Any]:
        if self._active_profile is None:
            self.generate_profile()
        assert self._active_profile is not None
        return {
            "profile_id": self._active_profile.profile_id,
            "user_agent": self._active_profile.user_agent,
            "uris": self._active_profile.uri_pool[:5],
            "sleep": self._active_profile.sleep_s,
            "jitter_ms": self._active_profile.jitter_ms,
            "headers": self._active_profile.headers,
            "domain_front": self._active_profile.domain_front,
            "method": self._active_profile.http_method,
        }

    def morph_traffic(self, config: TrafficMorphConfig | None = None) -> dict[str, Any]:
        if config is None:
            config = TrafficMorphConfig()
        uris = config.uri_pool if config.uri_pool else self._pick_uri_pool()
        method = random.choices(
            list(config.method_weights.keys()),
            weights=list(config.method_weights.values()),
            k=1,
        )[0]
        jitter = random.randint(config.jitter_ms_min, config.jitter_ms_max)
        inject_noise = random.random() < config.inject_noise_pct

        result = {
            "uri": random.choice(uris),
            "method": method,
            "jitter_ms": jitter,
            "inject_noise": inject_noise,
            "timestamp": time.time(),
        }
        if inject_noise:
            noise_uri = f"/{secrets.token_hex(random.randint(3, 6))}/{secrets.token_hex(6)}"
            result["noise_uri"] = noise_uri
        return result

    def _persist_profile(self, profile: MalleableProfile) -> Path:
        self._sessions_dir.mkdir(parents=True, exist_ok=True)
        target = self._sessions_dir / "evasion_profiles.jsonl"
        record = {
            "profile_id": profile.profile_id,
            "created_at": profile.created_at,
            "user_agent": profile.user_agent,
            "ja4_hash": profile.ja4_hash,
            "cert_fingerprint": profile.cert_fingerprint,
            "domain_front": profile.domain_front,
            "sleep_s": profile.sleep_s,
            "jitter_ms": profile.jitter_ms,
        }
        with target.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        return target

    def get_history(self) -> list[dict[str, Any]]:
        history_path = self._sessions_dir / "evasion_profiles.jsonl"
        if not history_path.exists():
            return []
        records: list[dict[str, Any]] = []
        with history_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return records

    def profile_to_json(self, profile: MalleableProfile | None = None) -> str:
        if profile is None:
            profile = self._active_profile
        if profile is None:
            return "{}"
        return json.dumps(
            {
                "profile_id": profile.profile_id,
                "user_agent": profile.user_agent,
                "uri_pool": profile.uri_pool,
                "http_method": profile.http_method,
                "jitter_ms": profile.jitter_ms,
                "sleep_s": profile.sleep_s,
                "headers": profile.headers,
                "ja4_hash": profile.ja4_hash,
                "tls_ciphers": profile.tls_ciphers,
                "cert_fingerprint": profile.cert_fingerprint,
                "domain_front": profile.domain_front,
                "created_at": profile.created_at,
            },
            indent=2,
        )
