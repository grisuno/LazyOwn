# skills/claude_md_orchestrator

*Community 6 | 37 files | cohesion 0.69*

## Definition

This community groups 37 file(s) rooted at `skills/claude_md_orchestrator` with dominant language py (cohesion 0.69). Central symbols: `AnalyzerResult`, `BddResult`, `BindAddressResolver`, `CheckResult`, `CheckpointSerializer`, `CicdResult`, `CicleState`, `CicleStateFile`. Core file: `static/js/xterm.js` (62 symbols). Documented purpose: DNS exfiltration and covert channel command set.  Phase 09 — commands for DNS tunneling exfiltration, DNS C2 beacon management, and DNS query log monitoring..

## Files

### `skills/claude_md_orchestrator` (13 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/claude_md_orchestrator/__init__.py` | py | utility | 0 | yes |
| `skills/claude_md_orchestrator/bdd_agent.py` | py | utility | 8 | yes |
| `skills/claude_md_orchestrator/boy_scout.py` | py | utility | 5 | yes |
| `skills/claude_md_orchestrator/cicd_agent.py` | py | utility | 7 | yes |

### `skills/hermes-lazyown` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/hermes-lazyown/claudemd_rules.py` | py | business_logic | 14 | yes |
| `skills/hermes-lazyown/config_bridge.py` | py | infrastructure | 16 | yes |
| `skills/hermes-lazyown/constants.py` | py | utility | 15 | yes |

### `contrib/legacy` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazygalazy.py` | py | utility | 7 | no |
| `contrib/legacy/lazygptcli.py` | py | utility | 14 | yes |
| `contrib/legacy/lazygptcli_unified.py` | py | utility | 29 | yes |

### `modules` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/colors.py` | py | utility | 3 | no |
| `modules/dns_beacon.py` | py | utility | 19 | yes |
| `modules/lazyown_bprfuzzer.py` | py | utility | 15 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/dns_exfil.py` | py | utility | 12 | yes |
| `cli/commands/phishing_wizard.py` | py | utility | 17 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `pwntomate.py` | py | utility | 3 | yes |

### `modules/backdoor` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/backdoor/server.c` | c | utility | 1 | no |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/lazyown_mcp_opencode.py` | py | utility | 3 | yes |

### `static/js` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/xterm.js` | js | utility | 62 | no |

### `tests` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_security_sanitizers.py` | py | testing | 45 | yes |

*... and 17 more files in this community.*


## Key Symbols

- `_sanitize_filename` (function, `cli/commands/dns_exfil.py:36`) `def _sanitize_filename(name)` - Return a safe basename from an untrusted input, falling back to a random name.
- `DNSExfilCommandSet` (class, `cli/commands/dns_exfil.py:44`) `class DNSExfilCommandSet(LazyOwnCommandSet)` - DNS exfiltration and covert channel commands.
- `do_dns_beacon` (method, `cli/commands/dns_exfil.py:51`) `def do_dns_beacon(self, line)` - Start a DNS tunneling beacon.
- `do_dns_exfil_listen` (method, `cli/commands/dns_exfil.py:97`) `def do_dns_exfil_listen(self, line)` - Start a DNS exfiltration listener on UDP port 53.
- `do_dns_beacon_status` (method, `cli/commands/dns_exfil.py:183`) `def do_dns_beacon_status(self, line)` - Show status of all DNS beacons.
- `do_http_exfil_server` (method, `cli/commands/dns_exfil.py:204`) `def do_http_exfil_server(self, line)` - Start a minimal HTTP exfiltration receiver.
- `ExfilHandler` (class, `cli/commands/dns_exfil.py:227`) `class ExfilHandler(BaseHTTPRequestHandler)`
- `do_POST` (method, `cli/commands/dns_exfil.py:228`) `def do_POST(self)`
- `log_message` (method, `cli/commands/dns_exfil.py:289`) `def log_message(self, fmt)`
- `do_smb_exfil` (method, `cli/commands/dns_exfil.py:304`) `def do_smb_exfil(self, line)` - Exfiltrate files to an SMB share on the attacker machine.
- `do_exfil_start_server` (method, `cli/commands/dns_exfil.py:338`) `def do_exfil_start_server(self, line)` - Start all required exfiltration listeners.
- `_extract` (method, `cli/commands/dns_exfil.py:384`) `def _extract(args, flag)`
- `PhishingWizardCommandSet` (class, `cli/commands/phishing_wizard.py:183`) `class PhishingWizardCommandSet(LazyOwnCommandSet)` - End-to-end phishing campaign wizard.
- `do_phish_wizard` (method, `cli/commands/phishing_wizard.py:190`) `def do_phish_wizard(self, line)` - Interactive end-to-end phishing campaign wizard.
- `do_phish_serve` (method, `cli/commands/phishing_wizard.py:361`) `def do_phish_serve(self, line)` - Start a lightweight HTTP server for phishing landing pages.
- `PhishingHandler` (class, `cli/commands/phishing_wizard.py:388`) `class PhishingHandler(BaseHTTPRequestHandler)`
- `log_message` (method, `cli/commands/phishing_wizard.py:389`) `def log_message(self, format)`
- `do_GET` (method, `cli/commands/phishing_wizard.py:392`) `def do_GET(self)`
- `do_POST` (method, `cli/commands/phishing_wizard.py:407`) `def do_POST(self)`
- `do_OPTIONS` (method, `cli/commands/phishing_wizard.py:427`) `def do_OPTIONS(self)`
- `do_phish_report` (method, `cli/commands/phishing_wizard.py:443`) `def do_phish_report(self, line)` - Show campaign results and captured credentials.
- `_profile_targets` (function, `cli/commands/phishing_wizard.py:510`) `def _profile_targets(domain)` - Generate target email addresses from common role prefixes.
- `_save_targets` (function, `cli/commands/phishing_wizard.py:522`) `def _save_targets(campaign_dir, targets)` - Save target list to disk.
- `_log_click` (function, `cli/commands/phishing_wizard.py:533`) `def _log_click(campaign_dir, ip, user_agent)` - Log a click event.
- `_ensure_session_key` (function, `cli/commands/phishing_wizard.py:551`) `def _ensure_session_key()` - Provision a machine-local secret key for credential encryption.
- `_log_credentials` (function, `cli/commands/phishing_wizard.py:569`) `def _log_credentials(campaign_dir, email, password, ip)` - Log captured credentials encrypted at rest and hashed in the audit log.
- `_send_smtp_email` (function, `cli/commands/phishing_wizard.py:603`) `def _send_smtp_email(server, port, username, password, to_email, from_addr, subj` - Send an email via SMTP.
- `do_phisher` (function, `cli/commands/phishing_wizard.py:637`) `def do_phisher(self, line)` - Launch a phishing campaign against a target domain.
- `_extract_flag` (function, `cli/commands/phishing_wizard.py:702`) `def _extract_flag(args, flag)` - Extract a ``--flag <value>`` pair from a list of arguments.
- `SamsungKnoxExploitServer` (class, `contrib/legacy/lazygalazy.py:8`) `class SamsungKnoxExploitServer(BaseHTTPRequestHandler)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 64
- Cross-boundary resolved imports (EXTRACTED): 33

## Connections

- [EXTRACTED] depends_on community 6 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/dns_exfil.py imports cli/commands/_base.py.

## Risks

- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`
- [dataflow UNCHECKED_ALLOC] `cli/commands/dns_exfil.py:117` `do_dns_exfil_listen` `sock`: Result of allocator stored in `sock` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazyproxy.py:153` `handle_request` `server_socket`: Result of allocator stored in `server_socket` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazyproxy.py:184` `start_proxy` `proxy_socket`: Result of allocator stored in `proxy_socket` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazyseo.py:50` `results` `content`: Result of allocator stored in `content` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/backdoor/server.c:19` `main` `sock`: Result of allocator stored in `sock` is never checked against NULL.

## Open Questions

- Why do 7 file(s) lack file-level docs (e.g. `contrib/legacy/lazygalazy.py`)? What purpose do they serve?
- Can the cycle `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` be broken with an interface?
- What would break if the most connected file in skills/claude_md_orchestrator changed?
- Should skills/claude_md_orchestrator be split, given cohesion 0.69?

## Sources

- `cli/commands/dns_exfil.py`
- `cli/commands/phishing_wizard.py`
- `contrib/legacy/lazygalazy.py`
- `contrib/legacy/lazygptcli.py`
- `contrib/legacy/lazygptcli_unified.py`
- `contrib/legacy/lazyhttpreverseshell.py`
- `contrib/legacy/lazyproxy.py`
- `contrib/legacy/lazyseo.py`
- `modules/backdoor/server.c`
- `modules/colors.py`
- `modules/dns_beacon.py`
- `modules/lazyown_bprfuzzer.py`
- `modules/security_sanitizers.py`
- `pwntomate.py`
- `skills/claude_md_orchestrator/__init__.py`
- `skills/claude_md_orchestrator/bdd_agent.py`
- `skills/claude_md_orchestrator/boy_scout.py`
- `skills/claude_md_orchestrator/cicd_agent.py`
- `skills/claude_md_orchestrator/config.py`
- `skills/claude_md_orchestrator/documentation_agent.py`
- *... and 17 more*
