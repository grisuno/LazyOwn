# `modules.traffic_morpher`

> Source: [modules/traffic_morpher.py:1](../../modules/traffic_morpher.py#L1) | language `py` | coverage 91.7% | [API index](../index.md)

C2 traffic obfuscation: domain fronting, protocol mimicking, and traffic shaping.

Provides multiple strategies for disguising C2 traffic to blend in with
legitimate network traffic. Supports Cloudflare Workers proxy, domain
fronting against CDN providers, HTTPS certificate pinning, and traffic
morphing for popular protocols (HTTP/2, WebSocket, DNS, ICMP).

## Contents

- **Classes:** [`TrafficMorpher`](#trafficmorpher)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_traffic_morpher_py__TrafficMorpher_generate_beacon_profile(["TrafficMorpher.generate_beacon_profile"])
    n_modules_traffic_morpher_py__TrafficMorpher_get_random_http_headers(["TrafficMorpher.get_random_http_headers"])
    n_modules_traffic_morpher_py__TrafficMorpher_generate_beacon_profile --> n_modules_traffic_morpher_py__TrafficMorpher_get_random_http_headers
```

## Classes

<a id="trafficmorpher"></a>

### `TrafficMorpher`

`class` | [modules/traffic_morpher.py:18](../../modules/traffic_morpher.py#L18)

```python
class TrafficMorpher
```

Transform C2 traffic patterns to mimic legitimate protocols.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`HTTP2_FINGERPRINTS`](#trafficmorpher-http2_fingerprints) |  | `[{'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'accept_language': 'en-US,en;q=0.9', 'accept_encoding': 'gzip, deflate, br', 'sec_ch_ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'}, {'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'accept_language': 'en-US,en;q=0.9', 'accept_encoding': 'gzip, deflate, br'}, {'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'accept_language': 'en-US,en;q=0.5', 'accept_encoding': 'gzip, deflate, br'}]` |  |
| [`CDN_DOMAINS`](#trafficmorpher-cdn_domains) |  | `{'cloudflare': ['cloudflare.com', 'cdn.cloudflare.net', 'cloudflare-dns.com', 'cloudflare-ech.com'], 'azure': ['azureedge.net', 'azurewebsites.net', 'cloudapp.net', 'trafficmanager.net', 'azure-api.net'], 'aws': ['cloudfront.net', 'amazonaws.com', 's3.amazonaws.com', 'elasticbeanstalk.com'], 'google': ['googleapis.com', 'cloudfunctions.net', 'run.app', 'firebaseio.com', 'appspot.com'], 'fastly': ['fastly.net', 'global.ssl.fastly.net', 'fastlylb.net']}` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#trafficmorpher-__init__) | constructor |  |
| [`get_random_http_headers`](#trafficmorpher-get_random_http_headers) | method | Return a randomized set of HTTP headers mimicking a real browser. |
| [`get_cdn_fronting_hosts`](#trafficmorpher-get_cdn_fronting_hosts) | method | Return CDN domains suitable for domain fronting. |
| [`generate_traffic_padding`](#trafficmorpher-generate_traffic_padding) | method | Generate random padding bytes to normalize packet sizes. |
| [`generate_jitter`](#trafficmorpher-generate_jitter) | method | Calculate a sleep delay with jitter. |
| [`generate_dns_tunnel_payload`](#trafficmorpher-generate_dns_tunnel_payload) | method | Encode data as DNS query subdomains for tunneling. |
| [`generate_icmp_exfil_payload`](#trafficmorpher-generate_icmp_exfil_payload) | method | Generate ICMP echo payloads for data exfiltration. |
| [`generate_websocket_masking`](#trafficmorpher-generate_websocket_masking) | method | Apply WebSocket frame masking with random key. |
| [`generate_cloudflare_worker_proxy_config`](#trafficmorpher-generate_cloudflare_worker_proxy_config) | method | Generate a Cloudflare Worker script that proxies C2 traffic. |
| [`generate_beacon_profile`](#trafficmorpher-generate_beacon_profile) | method | Generate a complete C2 beacon profile configuration. |

<a id="trafficmorpher-__init__"></a>

#### `TrafficMorpher.__init__`

`constructor` | [modules/traffic_morpher.py:77](../../modules/traffic_morpher.py#L77)

```python
def __init__(self) -> None
```

*Called by:* [`PersistMigratedCommandSet.do_beaconcfg`](cli.commands.persist_migrated.py.md#persistmigratedcommandset-do_beaconcfg)

<a id="trafficmorpher-get_random_http_headers"></a>

#### `TrafficMorpher.get_random_http_headers`

`method` | [modules/traffic_morpher.py:81](../../modules/traffic_morpher.py#L81)

```python
def get_random_http_headers(self) -> dict[str, str]
```

Return a randomized set of HTTP headers mimicking a real browser.

**Returns:** `dict[str, str]` - Dictionary of HTTP headers.

*Called by:* [`TrafficMorpher.generate_beacon_profile`](#trafficmorpher-generate_beacon_profile)

<a id="trafficmorpher-get_cdn_fronting_hosts"></a>

#### `TrafficMorpher.get_cdn_fronting_hosts`

`method` | [modules/traffic_morpher.py:91](../../modules/traffic_morpher.py#L91)

```python
def get_cdn_fronting_hosts(self, provider: str = 'cloudflare', count: int = 3) -> list[str]
```

Return CDN domains suitable for domain fronting.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `provider` | `str` | `'cloudflare'` | CDN provider name (cloudflare, azure, aws, google, fastly). |
| `count` | `int` | `3` | Number of domain suggestions to return. |

**Returns:** `list[str]` - List of high-reputation CDN domain names.

*Called by:* [`PersistMigratedCommandSet.do_beaconcfg`](cli.commands.persist_migrated.py.md#persistmigratedcommandset-do_beaconcfg)

<a id="trafficmorpher-generate_traffic_padding"></a>

#### `TrafficMorpher.generate_traffic_padding`

`method` | [modules/traffic_morpher.py:108](../../modules/traffic_morpher.py#L108)

```python
def generate_traffic_padding(self, min_bytes: int = 64, max_bytes: int = 4096) -> bytes
```

Generate random padding bytes to normalize packet sizes.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `min_bytes` | `int` | `64` | Minimum padding size. |
| `max_bytes` | `int` | `4096` | Maximum padding size. |

**Returns:** `bytes` - Random bytes for traffic padding.

<a id="trafficmorpher-generate_jitter"></a>

#### `TrafficMorpher.generate_jitter`

`method` | [modules/traffic_morpher.py:125](../../modules/traffic_morpher.py#L125)

```python
def generate_jitter(self, base_delay: float, jitter_pct: float = 0.3) -> float
```

Calculate a sleep delay with jitter.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `base_delay` | `float` |  | Base sleep time in seconds. |
| `jitter_pct` | `float` | `0.3` | Percentage of jitter to apply (0.0 - 1.0). |

**Returns:** `float` - Adjusted sleep time with random jitter applied.

<a id="trafficmorpher-generate_dns_tunnel_payload"></a>

#### `TrafficMorpher.generate_dns_tunnel_payload`

`method` | [modules/traffic_morpher.py:138](../../modules/traffic_morpher.py#L138)

```python
def generate_dns_tunnel_payload(self, data: bytes, domain: str = 'cdn.cloudflare.net') -> list[str]
```

Encode data as DNS query subdomains for tunneling.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` | `bytes` |  | Raw data to tunnel. |
| `domain` | `str` | `'cdn.cloudflare.net'` | Base domain for DNS queries. |

**Returns:** `list[str]` - List of DNS query names.

*Called by:* [`PersistMigratedCommandSet.do_beaconcfg`](cli.commands.persist_migrated.py.md#persistmigratedcommandset-do_beaconcfg)

<a id="trafficmorpher-generate_icmp_exfil_payload"></a>

#### `TrafficMorpher.generate_icmp_exfil_payload`

`method` | [modules/traffic_morpher.py:164](../../modules/traffic_morpher.py#L164)

```python
def generate_icmp_exfil_payload(self, data: bytes, chunk_size: int = 48) -> list[bytes]
```

Generate ICMP echo payloads for data exfiltration.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` | `bytes` |  | Data to exfiltrate. |
| `chunk_size` | `int` | `48` | Bytes per ICMP packet. |

**Returns:** `list[bytes]` - List of ICMP payload byte sequences.

<a id="trafficmorpher-generate_websocket_masking"></a>

#### `TrafficMorpher.generate_websocket_masking`

`method` | [modules/traffic_morpher.py:190](../../modules/traffic_morpher.py#L190)

```python
def generate_websocket_masking(self, data: bytes) -> bytes
```

Apply WebSocket frame masking with random key.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` | `bytes` |  | Raw data to mask as WebSocket frame. |

**Returns:** `bytes` - Masked WebSocket frame bytes.

<a id="trafficmorpher-generate_cloudflare_worker_proxy_config"></a>

#### `TrafficMorpher.generate_cloudflare_worker_proxy_config`

`method` | [modules/traffic_morpher.py:205](../../modules/traffic_morpher.py#L205)

```python
def generate_cloudflare_worker_proxy_config(self, c2_host: str, c2_port: int, auth_token: str | None = None) -> str
```

Generate a Cloudflare Worker script that proxies C2 traffic.

The worker acts as a reverse proxy, forwarding traffic from the
CDN edge to the real C2 server while rewriting Host headers.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `c2_host` | `str` |  | Real C2 server hostname or IP. |
| `c2_port` | `int` |  | Real C2 server port. |
| `auth_token` | `str \| None` | `None` | Optional pre-shared authentication token. |

**Returns:** `str` - Complete Cloudflare Worker JavaScript code.

*Called by:* [`PersistMigratedCommandSet.do_beaconcfg`](cli.commands.persist_migrated.py.md#persistmigratedcommandset-do_beaconcfg)

<a id="trafficmorpher-generate_beacon_profile"></a>

#### `TrafficMorpher.generate_beacon_profile`

`method` | [modules/traffic_morpher.py:270](../../modules/traffic_morpher.py#L270)

```python
def generate_beacon_profile(self, name: str = 'default', protocol: str = 'https', jitter_pct: float = 0.2, user_agent: str | None = None) -> dict[str, Any]
```

Generate a complete C2 beacon profile configuration.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | `'default'` | Profile name. |
| `protocol` | `str` | `'https'` | Beacon protocol (https, dns, icmp, websocket). |
| `jitter_pct` | `float` | `0.2` | Jitter percentage for beacon timing. |
| `user_agent` | `str \| None` | `None` | Custom user agent string. |

**Returns:** `dict[str, Any]` - Beacon profile dictionary.

*Calls:* [`TrafficMorpher.get_random_http_headers`](#trafficmorpher-get_random_http_headers)

*Called by:* [`PersistMigratedCommandSet.do_beaconcfg`](cli.commands.persist_migrated.py.md#persistmigratedcommandset-do_beaconcfg)

---
