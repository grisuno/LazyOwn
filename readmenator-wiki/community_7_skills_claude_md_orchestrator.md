# skills/claude_md_orchestrator

*Community 7 | 30 files | cohesion 0.77*

## Definition

This community groups 30 file(s) rooted at `skills/claude_md_orchestrator` with dominant language py (cohesion 0.77). Central symbols: `AnalyzerResult`, `BddResult`, `BindAddressResolver`, `CheckResult`, `CheckpointSerializer`, `CicdResult`, `CicleState`, `CicleStateFile`. Core file: `tests/test_security_sanitizers.py` (45 symbols). Documented purpose: Phishing Wizard command set.  End-to-end phishing campaign wizard with step-by-step interactive flow: target profiling -> template selection -> landing page gen.

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

### `modules` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/__init__.py` | py | utility | 0 | no |
| `modules/lazyown_bprfuzzer.py` | py | utility | 15 | yes |
| `modules/security_sanitizers.py` | py | utility | 25 | yes |

### `contrib/legacy` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazygalazy.py` | py | utility | 7 | no |
| `contrib/legacy/lazyhttpreverseshell.py` | py | utility | 10 | no |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `pwntomate.py` | py | utility | 3 | yes |

### `cli/commands` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/phishing_wizard.py` | py | utility | 17 | yes |

### `modules/backdoor` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/backdoor/server.c` | c | utility | 1 | no |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/lazyown_mcp_opencode.py` | py | utility | 3 | yes |

### `tests` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_security_sanitizers.py` | py | testing | 45 | yes |

*... and 10 more files in this community.*


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

- Internal resolved imports (EXTRACTED): 55
- Cross-boundary resolved imports (EXTRACTED): 18

## Connections

- [EXTRACTED] depends_on community 1 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/dns_exfil.py imports modules/backdoor/server.c.
- [EXTRACTED] depends_on community 7 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/phishing_wizard.py imports modules/phishing_orchestrator.py.

## Risks

- [taint high] `cli/banner_config.py` -> `modules/backdoor/server.c` via `subprocess` (5 hops)
- [taint high] `cli/banner_config.py` -> `skills/claude_md_orchestrator/parser.py` via `subprocess` (5 hops)
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`
- [dataflow UNCHECKED_ALLOC] `modules/backdoor/server.c:19` `main` `sock`: Result of allocator stored in `sock` is never checked against NULL.

## Open Questions

- Why do 4 file(s) lack file-level docs (e.g. `contrib/legacy/lazygalazy.py`)? What purpose do they serve?
- Can the cycle `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` be broken with an interface?
- What would break if the most connected file in skills/claude_md_orchestrator changed?
- Should skills/claude_md_orchestrator be split, given cohesion 0.77?

## Sources

- `cli/commands/phishing_wizard.py`
- `contrib/legacy/lazygalazy.py`
- `contrib/legacy/lazyhttpreverseshell.py`
- `modules/__init__.py`
- `modules/backdoor/server.c`
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
