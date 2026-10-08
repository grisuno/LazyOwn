# skills/hermes-lazyown

*Community 8 | 17 files | cohesion 0.64*

## Definition

This community groups 17 file(s) rooted at `skills/hermes-lazyown` with dominant language py (cohesion 0.64). Central symbols: `BindAddressResolver`, `CheckpointSerializer`, `CommandRedactor`, `CompactionResult`, `CompactionStrategy`, `ConfigBridge`, `ConfigBridgeError`, `ConfigKeys`. Core file: `tests/test_security_sanitizers.py` (45 symbols). Documented purpose: Phishing Wizard command set.  End-to-end phishing campaign wizard with step-by-step interactive flow: target profiling -> template selection -> landing page gen.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/phishing_wizard.py` | py | utility | 17 | yes |
| `contrib/legacy/lazygalazy.py` | py | utility | 7 | no |
| `contrib/legacy/lazyhttpreverseshell.py` | py | utility | 10 | no |
| `modules/__init__.py` | py | utility | 0 | no |
| `modules/backdoor/server.c` | c | utility | 1 | no |
| `modules/lazyown_bprfuzzer.py` | py | utility | 15 | yes |
| `modules/security_sanitizers.py` | py | utility | 25 | yes |
| `pwntomate.py` | py | utility | 3 | yes |
| `skills/hermes-lazyown/claudemd_rules.py` | py | business_logic | 14 | yes |
| `skills/hermes-lazyown/config_bridge.py` | py | infrastructure | 16 | yes |
| `skills/hermes-lazyown/constants.py` | py | utility | 15 | yes |
| `skills/hermes-lazyown/executor.py` | py | utility | 13 | yes |
| `skills/hermes-lazyown/hermes_sync.py` | py | utility | 14 | yes |
| `skills/hermes-lazyown/mcp_server.py` | py | utility | 28 | yes |
| `skills/hermes-lazyown/output_compactor.py` | py | utility | 20 | yes |
| `skills/lazyown_mcp_opencode.py` | py | utility | 3 | yes |
| `tests/test_security_sanitizers.py` | py | testing | 45 | yes |

## Key Symbols

- `PhishingWizardCommandSet` (class, `cli/commands/phishing_wizard.py:183`) `class PhishingWizardCommandSet(LazyOwnCommandSet)` - End-to-end phishing campaign wizard.
- `do_phish_wizard` (method, `cli/commands/phishing_wizard.py:190`) `def do_phish_wizard(self, line)` - Interactive end-to-end phishing campaign wizard.
- `do_phish_serve` (method, `cli/commands/phishing_wizard.py:361`) `def do_phish_serve(self, line)` - Start a lightweight HTTP server for phishing landing pages.
- `PhishingHandler` (class, `cli/commands/phishing_wizard.py:388`) `class PhishingHandler(BaseHTTPRequestHandler)`
- `log_message` (method, `cli/commands/phishing_wizard.py:389`) `def log_message(self, format)`
- `do_GET` (method, `cli/commands/phishing_wizard.py:392`) `def do_GET(self)`
- `do_POST` (method, `cli/commands/phishing_wizard.py:407`) `def do_POST(self)`
- `do_OPTIONS` (method, `cli/commands/phishing_wizard.py:427`) `def do_OPTIONS(self)`
- `do_phish_report` (method, `cli/commands/phishing_wizard.py:443`) `def do_phish_report(self, line)` - Show campaign results and captured credentials.
- `_profile_targets` (method, `cli/commands/phishing_wizard.py:510`) `def _profile_targets(domain)` - Generate target email addresses from common role prefixes.
- `_save_targets` (method, `cli/commands/phishing_wizard.py:522`) `def _save_targets(campaign_dir, targets)` - Save target list to disk.
- `_log_click` (method, `cli/commands/phishing_wizard.py:533`) `def _log_click(campaign_dir, ip, user_agent)` - Log a click event.
- `_ensure_session_key` (method, `cli/commands/phishing_wizard.py:551`) `def _ensure_session_key()` - Provision a machine-local secret key for credential encryption.
- `_log_credentials` (method, `cli/commands/phishing_wizard.py:569`) `def _log_credentials(campaign_dir, email, password, ip)` - Log captured credentials encrypted at rest and hashed in the audit log.
- `_send_smtp_email` (method, `cli/commands/phishing_wizard.py:603`) `def _send_smtp_email(server, port, username, password, to_email, from_addr, subj` - Send an email via SMTP.
- `do_phisher` (method, `cli/commands/phishing_wizard.py:637`) `def do_phisher(self, line)` - Launch a phishing campaign against a target domain.
- `_extract_flag` (method, `cli/commands/phishing_wizard.py:702`) `def _extract_flag(args, flag)` - Extract a ``--flag <value>`` pair from a list of arguments.
- `SamsungKnoxExploitServer` (class, `contrib/legacy/lazygalazy.py:8`) `class SamsungKnoxExploitServer(BaseHTTPRequestHandler)`
- `do_GET` (method, `contrib/legacy/lazygalazy.py:11`) `def do_GET(self)`
- `apk_bytes` (method, `contrib/legacy/lazygalazy.py:33`) `def apk_bytes(self)`
- `launch_html` (method, `contrib/legacy/lazygalazy.py:36`) `def launch_html(self)`
- `exploit_js` (method, `contrib/legacy/lazygalazy.py:49`) `def exploit_js(self)`
- `rand_word` (method, `contrib/legacy/lazygalazy.py:93`) `def rand_word(self)`
- `main` (method, `contrib/legacy/lazygalazy.py:97`) `def main()`
- `encrypt` (function, `contrib/legacy/lazyhttpreverseshell.py:14`) `def encrypt(data)`
- `decrypt` (function, `contrib/legacy/lazyhttpreverseshell.py:17`) `def decrypt(data)`
- `compress` (function, `contrib/legacy/lazyhttpreverseshell.py:20`) `def compress(data)`
- `decompress` (function, `contrib/legacy/lazyhttpreverseshell.py:23`) `def decompress(data)`
- `reverse_http_shell_client` (function, `contrib/legacy/lazyhttpreverseshell.py:26`) `def reverse_http_shell_client(lhost, rhost, rport)`
- `reverse_http_shell_server` (function, `contrib/legacy/lazyhttpreverseshell.py:50`) `def reverse_http_shell_server(lhost, lport)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 21
- Cross-boundary resolved imports (EXTRACTED): 15

## Connections

- [EXTRACTED] depends_on community 1 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/commands/dns_exfil.py imports modules/backdoor/server.c.
- [EXTRACTED] depends_on community 8 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/phishing_wizard.py imports modules/phishing_orchestrator.py.

## Risks

- [taint high] `cli/banner_config.py` -> `modules/backdoor/server.c` via `subprocess` (5 hops)
- [dataflow UNCHECKED_ALLOC] `modules/backdoor/server.c:19` `main` `sock`: Result of allocator stored in `sock` is never checked against NULL.

## Open Questions

- Why do 4 file(s) lack file-level docs (e.g. `contrib/legacy/lazygalazy.py`)? What purpose do they serve?
- What would break if the most connected file in skills/hermes-lazyown changed?
- Should skills/hermes-lazyown be split, given cohesion 0.64?

## Sources

- `cli/commands/phishing_wizard.py`
- `contrib/legacy/lazygalazy.py`
- `contrib/legacy/lazyhttpreverseshell.py`
- `modules/__init__.py`
- `modules/backdoor/server.c`
- `modules/lazyown_bprfuzzer.py`
- `modules/security_sanitizers.py`
- `pwntomate.py`
- `skills/hermes-lazyown/claudemd_rules.py`
- `skills/hermes-lazyown/config_bridge.py`
- `skills/hermes-lazyown/constants.py`
- `skills/hermes-lazyown/executor.py`
- `skills/hermes-lazyown/hermes_sync.py`
- `skills/hermes-lazyown/mcp_server.py`
- `skills/hermes-lazyown/output_compactor.py`
- `skills/lazyown_mcp_opencode.py`
- `tests/test_security_sanitizers.py`
