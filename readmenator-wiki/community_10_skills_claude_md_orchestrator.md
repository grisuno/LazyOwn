# skills/claude_md_orchestrator

*Community 10 | 17 files | cohesion 0.75*

## Definition

This community groups 17 file(s) rooted at `skills/claude_md_orchestrator` with dominant language py (cohesion 0.75). Central symbols: `AnalyzerResult`, `BddResult`, `BindAddressResolver`, `CheckResult`, `CicdResult`, `CicleState`, `CicleStateFile`, `CommandRedactor`. Core file: `tests/test_security_sanitizers.py` (45 symbols). Documented purpose: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Licencia: GPL v3  Descripción: Lazy Burp-Like Fuzzer co.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/lazyown_bprfuzzer.py` | py | utility | 15 | yes |
| `modules/security_sanitizers.py` | py | utility | 25 | yes |
| `pwntomate.py` | py | utility | 3 | yes |
| `skills/claude_md_orchestrator/__init__.py` | py | utility | 0 | yes |
| `skills/claude_md_orchestrator/bdd_agent.py` | py | utility | 8 | yes |
| `skills/claude_md_orchestrator/boy_scout.py` | py | utility | 5 | yes |
| `skills/claude_md_orchestrator/cicd_agent.py` | py | utility | 7 | yes |
| `skills/claude_md_orchestrator/config.py` | py | infrastructure | 15 | yes |
| `skills/claude_md_orchestrator/documentation_agent.py` | py | utility | 7 | yes |
| `skills/claude_md_orchestrator/models.py` | py | business_logic | 32 | yes |
| `skills/claude_md_orchestrator/orchestrator.py` | py | utility | 21 | yes |
| `skills/claude_md_orchestrator/parser.py` | py | utility | 13 | yes |
| `skills/claude_md_orchestrator/reviewer_agent.py` | py | utility | 10 | yes |
| `skills/claude_md_orchestrator/sdd_agent.py` | py | utility | 6 | yes |
| `skills/claude_md_orchestrator/tdd_agent.py` | py | utility | 7 | yes |
| `skills/claude_md_orchestrator/validators.py` | py | utility | 21 | yes |
| `tests/test_security_sanitizers.py` | py | testing | 45 | yes |

## Key Symbols

- `_load_security_config` (function, `modules/lazyown_bprfuzzer.py:45`) `def _load_security_config()` - Return a :class:`SecurityConfig` from ``payload.json`` when present.
- `load_headers_from_file` (function, `modules/lazyown_bprfuzzer.py:93`) `def load_headers_from_file(file_path)`
- `load_data_from_file` (function, `modules/lazyown_bprfuzzer.py:99`) `def load_data_from_file(file_path)`
- `signal_handler` (function, `modules/lazyown_bprfuzzer.py:105`) `def signal_handler(sig, frame)`
- `ProxyHandler` (class, `modules/lazyown_bprfuzzer.py:114`) `class ProxyHandler(BaseHTTPRequestHandler)`
- `do_GET` (method, `modules/lazyown_bprfuzzer.py:115`) `def do_GET(self)`
- `do_POST` (method, `modules/lazyown_bprfuzzer.py:118`) `def do_POST(self)`
- `_handle_request` (method, `modules/lazyown_bprfuzzer.py:121`) `def _handle_request(self, method)`
- `run_proxy` (function, `modules/lazyown_bprfuzzer.py:162`) `def run_proxy(port)`
- `edit_file_with_nano` (function, `modules/lazyown_bprfuzzer.py:169`) `def edit_file_with_nano(content)`
- `send_request` (function, `modules/lazyown_bprfuzzer.py:179`) `def send_request(url, method, headers, params, data, json_data, proxies, hide_co` - Envía una solicitud HTTP y devuelve la respuesta.
- `repeater` (function, `modules/lazyown_bprfuzzer.py:203`) `def repeater(url, method, headers, params, data, json_data, proxies, hide_code)` - Funcionalidad de Repeater que permite enviar solicitudes múltiples veces con posibilidad de modifica
- `lazyfuzz` (function, `modules/lazyown_bprfuzzer.py:233`) `def lazyfuzz(url, method, headers, params, data, json_data, proxies, wordlist_pa` - Funcionalidad de fuzzing que reemplaza LAZYFUZZ con palabras de una wordlist.
- `parse_arguments` (function, `modules/lazyown_bprfuzzer.py:278`) `def parse_arguments()` - Parsear los argumentos de la línea de comandos.
- `main` (function, `modules/lazyown_bprfuzzer.py:302`) `def main()`
- `SecurityConfig` (class, `modules/security_sanitizers.py:37`) `class SecurityConfig` - Immutable tunables consumed by every sanitizer in this module.
- `from_payload` (method, `modules/security_sanitizers.py:68`) `def from_payload(cls, payload)` - Build a configuration object from a ``payload.json`` mapping.
- `HeaderValueSanitizer` (class, `modules/security_sanitizers.py:101`) `class HeaderValueSanitizer` - Validate HTTP header names and values before transmission.
- `__init__` (method, `modules/security_sanitizers.py:115`) `def __init__(self, config)` - Bind the sanitizer to a configuration instance.
- `is_valid_name` (method, `modules/security_sanitizers.py:129`) `def is_valid_name(self, name)` - Return True iff ``name`` is a syntactically valid header token.
- `sanitize_value` (method, `modules/security_sanitizers.py:139`) `def sanitize_value(self, value)` - Return a header value that cannot smuggle a response split.
- `SessionPathResolver` (class, `modules/security_sanitizers.py:162`) `class SessionPathResolver` - Resolve untrusted filenames against a fixed base directory.
- `__init__` (method, `modules/security_sanitizers.py:174`) `def __init__(self, base_dir, config)` - Bind the resolver to an absolute, real base directory.
- `base_dir` (method, `modules/security_sanitizers.py:192`) `def base_dir(self)` - The resolved, absolute base directory.
- `resolve` (method, `modules/security_sanitizers.py:196`) `def resolve(self, untrusted_name)` - Return ``(absolute, relative)`` for a safe filename.
- `file_exists` (method, `modules/security_sanitizers.py:238`) `def file_exists(self, untrusted_name)` - Return True iff ``untrusted_name`` resolves to an existing file.
- `BindAddressResolver` (class, `modules/security_sanitizers.py:256`) `class BindAddressResolver` - Pick the address a server socket should bind to.
- `__init__` (method, `modules/security_sanitizers.py:269`) `def __init__(self, config, preferred_addresses)` - Build a resolver with a prioritised list of candidate addresses.
- `_is_well_formed` (method, `modules/security_sanitizers.py:285`) `def _is_well_formed(self, candidate)` - Return True iff ``candidate`` is a parseable IP literal.
- `resolve` (method, `modules/security_sanitizers.py:298`) `def resolve(self)` - Return the address sockets should bind to.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 37
- Cross-boundary resolved imports (EXTRACTED): 11

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`

## Open Questions

- Can the cycle `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` be broken with an interface?
- What would break if the most connected file in skills/claude_md_orchestrator changed?
- Should skills/claude_md_orchestrator be split, given cohesion 0.75?

## Sources

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
- `skills/claude_md_orchestrator/validators.py`
- `tests/test_security_sanitizers.py`
