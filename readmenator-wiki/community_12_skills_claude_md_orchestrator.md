# skills/claude_md_orchestrator

*Community 12 | 30 files | cohesion 0.68*

## Definition

This community groups 30 file(s) rooted at `skills/claude_md_orchestrator` with dominant language py (cohesion 0.68). Central symbols: `AnalyzerResult`, `BddResult`, `BindAddressResolver`, `BprfuzzerIdentitySpec`, `CheckResult`, `CheckpointSerializer`, `CicdResult`, `CicleState`. Core file: `tests/test_security_sanitizers.py` (45 symbols). Documented purpose: Browser identity sync between the operator browser and the recorder proxy.  A Chrome/Brave extension (``browser_sync_extension/``) pushes the real cookie store .

## Files

### `skills/claude_md_orchestrator` (13 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/claude_md_orchestrator/__init__.py` | py | utility | 0 | yes |
| `skills/claude_md_orchestrator/bdd_agent.py` | py | utility | 8 | yes |
| `skills/claude_md_orchestrator/boy_scout.py` | py | utility | 5 | yes |
| `skills/claude_md_orchestrator/cicd_agent.py` | py | utility | 7 | yes |
| `skills/claude_md_orchestrator/config.py` | py | infrastructure | 15 | yes |

### `skills/hermes-lazyown` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/hermes-lazyown/claudemd_rules.py` | py | business_logic | 14 | yes |
| `skills/hermes-lazyown/config_bridge.py` | py | infrastructure | 16 | yes |
| `skills/hermes-lazyown/constants.py` | py | utility | 15 | yes |
| `skills/hermes-lazyown/executor.py` | py | utility | 13 | yes |
| `skills/hermes-lazyown/hermes_sync.py` | py | utility | 14 | yes |

### `modules` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/browser_sync.py` | py | utility | 44 | yes |
| `modules/lazy_oob.py` | py | utility | 18 | yes |
| `modules/lazyown_bprfuzzer.py` | py | utility | 15 | yes |
| `modules/security_sanitizers.py` | py | utility | 25 | yes |

### `contrib/legacy` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazygalazy.py` | py | utility | 7 | no |
| `contrib/legacy/lazyhttpreverseshell.py` | py | utility | 10 | no |

### `tests` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_bprfuzzer_identity.py` | py | testing | 10 | yes |
| `tests/test_security_sanitizers.py` | py | testing | 45 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `pwntomate.py` | py | utility | 3 | yes |

### `modules/backdoor` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/backdoor/server.c` | c | utility | 1 | no |

*... and 10 more files in this community.*


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

- Internal resolved imports (EXTRACTED): 56
- Cross-boundary resolved imports (EXTRACTED): 26

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`
- [dataflow UNCHECKED_ALLOC] `modules/backdoor/server.c:19` `main` `sock`: Result of allocator stored in `sock` is never checked against NULL.

## Open Questions

- Why do 3 file(s) lack file-level docs (e.g. `contrib/legacy/lazygalazy.py`)? What purpose do they serve?
- Can the cycle `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` be broken with an interface?
- What would break if the most connected file in skills/claude_md_orchestrator changed?
- Should skills/claude_md_orchestrator be split, given cohesion 0.68?

## Sources

- `contrib/legacy/lazygalazy.py`
- `contrib/legacy/lazyhttpreverseshell.py`
- `modules/backdoor/server.c`
- `modules/browser_sync.py`
- `modules/lazy_oob.py`
- `modules/lazyown_bprfuzzer.py`
- `modules/security_sanitizers.py`
- `pwntomate.py`
- `skills/claude_md_orchestrator/__init__.py`
- `skills/claude_md_orchestrator/bdd_agent.py`
- `skills/claude_md_orchestrator/boy_scout.py`
- `skills/claude_md_orchestrator/cicd_agent.py`
- `skills/claude_md_orchestrator/config.py`
- `skills/claude_md_orchestrator/documentation_agent.py`
- `skills/claude_md_orchestrator/models.py`
- `skills/claude_md_orchestrator/orchestrator.py`
- `skills/claude_md_orchestrator/parser.py`
- `skills/claude_md_orchestrator/reviewer_agent.py`
- `skills/claude_md_orchestrator/sdd_agent.py`
- `skills/claude_md_orchestrator/tdd_agent.py`
- *... and 10 more*
