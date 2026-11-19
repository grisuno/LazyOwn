# skills/hermes-lazyown

*Community 11 | 14 files | cohesion 0.56*

## Definition

This community groups 14 file(s) rooted at `skills/hermes-lazyown` with dominant language py (cohesion 0.56). Central symbols: `BprfuzzerIdentitySpec`, `CheckpointSerializer`, `CompactionResult`, `CompactionStrategy`, `ConfigBridge`, `ConfigBridgeError`, `ConfigKeys`, `DefaultCompaction`. Core file: `modules/browser_sync.py` (44 symbols). Documented purpose: Browser identity sync between the operator browser and the recorder proxy.  A Chrome/Brave extension (``browser_sync_extension/``) pushes the real cookie store .

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazygalazy.py` | py | utility | 7 | no |
| `contrib/legacy/lazyhttpreverseshell.py` | py | utility | 10 | no |
| `modules/backdoor/server.c` | c | utility | 1 | no |
| `modules/browser_sync.py` | py | utility | 44 | yes |
| `modules/lazy_oob.py` | py | utility | 18 | yes |
| `modules/lazyown_bprfuzzer.py` | py | utility | 15 | yes |
| `skills/hermes-lazyown/claudemd_rules.py` | py | business_logic | 14 | yes |
| `skills/hermes-lazyown/config_bridge.py` | py | infrastructure | 16 | yes |
| `skills/hermes-lazyown/constants.py` | py | utility | 15 | yes |
| `skills/hermes-lazyown/executor.py` | py | utility | 13 | yes |
| `skills/hermes-lazyown/hermes_sync.py` | py | utility | 14 | yes |
| `skills/hermes-lazyown/mcp_server.py` | py | utility | 28 | yes |
| `skills/hermes-lazyown/output_compactor.py` | py | utility | 20 | yes |
| `tests/test_bprfuzzer_identity.py` | py | testing | 10 | yes |

## Key Symbols

- `SamsungKnoxExploitServer` (class, `contrib/legacy/lazygalazy.py:8`) `class SamsungKnoxExploitServer(BaseHTTPRequestHandler)`
- `do_GET` (method, `contrib/legacy/lazygalazy.py:11`) `def do_GET(self)`
- `apk_bytes` (method, `contrib/legacy/lazygalazy.py:33`) `def apk_bytes(self)`
- `launch_html` (method, `contrib/legacy/lazygalazy.py:36`) `def launch_html(self)`
- `exploit_js` (method, `contrib/legacy/lazygalazy.py:49`) `def exploit_js(self)`
- `rand_word` (method, `contrib/legacy/lazygalazy.py:93`) `def rand_word(self)`
- `main` (function, `contrib/legacy/lazygalazy.py:97`) `def main()`
- `encrypt` (function, `contrib/legacy/lazyhttpreverseshell.py:14`) `def encrypt(data)`
- `decrypt` (function, `contrib/legacy/lazyhttpreverseshell.py:17`) `def decrypt(data)`
- `compress` (function, `contrib/legacy/lazyhttpreverseshell.py:20`) `def compress(data)`
- `decompress` (function, `contrib/legacy/lazyhttpreverseshell.py:23`) `def decompress(data)`
- `reverse_http_shell_client` (function, `contrib/legacy/lazyhttpreverseshell.py:26`) `def reverse_http_shell_client(lhost, rhost, rport)`
- `reverse_http_shell_server` (function, `contrib/legacy/lazyhttpreverseshell.py:50`) `def reverse_http_shell_server(lhost, lport)`
- `RequestHandler` (class, `contrib/legacy/lazyhttpreverseshell.py:51`) `class RequestHandler(BaseHTTPRequestHandler)`
- `do_GET` (method, `contrib/legacy/lazyhttpreverseshell.py:52`) `def do_GET(self)`
- `do_POST` (method, `contrib/legacy/lazyhttpreverseshell.py:65`) `def do_POST(self)`
- `parse_arguments` (function, `contrib/legacy/lazyhttpreverseshell.py:88`) `def parse_arguments(args)`
- `main` (function, `modules/backdoor/server.c:10`) `int main()`
- `_sessions_dir` (function, `modules/browser_sync.py:71`) `def _sessions_dir()` - Return the browser sync directory under sessions.
- `_profile_path` (function, `modules/browser_sync.py:77`) `def _profile_path()` - Return the profile JSON path.
- `_jar_path` (function, `modules/browser_sync.py:82`) `def _jar_path()` - Return the Netscape cookie jar path.
- `_rules_path` (function, `modules/browser_sync.py:87`) `def _rules_path()` - Return the Match and Replace rules path.
- `_token_path` (function, `modules/browser_sync.py:92`) `def _token_path()` - Return the receiver token path.
- `_sanitize_header_value` (function, `modules/browser_sync.py:97`) `def _sanitize_header_value(value)` - Strip CR, LF and NUL from a header value.
- `token` (function, `modules/browser_sync.py:112`) `def token(create)` - Return the receiver auth token, generating it on first use.
- `reset_token` (function, `modules/browser_sync.py:138`) `def reset_token()` - Regenerate the receiver token.
- `load_profile` (function, `modules/browser_sync.py:151`) `def load_profile()` - Load the last synced browser identity profile.
- `profile_stats` (function, `modules/browser_sync.py:164`) `def profile_stats()` - Summarise the synced profile.
- `cookie_matches_host` (function, `modules/browser_sync.py:183`) `def cookie_matches_host(cookie, host)` - Return True when a synced cookie applies to a request host.
- `cookie_matches_path` (function, `modules/browser_sync.py:202`) `def cookie_matches_path(cookie, request_path)` - Return True when a synced cookie applies to one request path.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 19
- Cross-boundary resolved imports (EXTRACTED): 17

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- [dataflow UNCHECKED_ALLOC] `modules/backdoor/server.c:19` `main` `sock`: Result of allocator stored in `sock` is never checked against NULL.

## Open Questions

- Why do 3 file(s) lack file-level docs (e.g. `contrib/legacy/lazygalazy.py`)? What purpose do they serve?
- What would break if the most connected file in skills/hermes-lazyown changed?
- Should skills/hermes-lazyown be split, given cohesion 0.56?

## Sources

- `contrib/legacy/lazygalazy.py`
- `contrib/legacy/lazyhttpreverseshell.py`
- `modules/backdoor/server.c`
- `modules/browser_sync.py`
- `modules/lazy_oob.py`
- `modules/lazyown_bprfuzzer.py`
- `skills/hermes-lazyown/claudemd_rules.py`
- `skills/hermes-lazyown/config_bridge.py`
- `skills/hermes-lazyown/constants.py`
- `skills/hermes-lazyown/executor.py`
- `skills/hermes-lazyown/hermes_sync.py`
- `skills/hermes-lazyown/mcp_server.py`
- `skills/hermes-lazyown/output_compactor.py`
- `tests/test_bprfuzzer_identity.py`
