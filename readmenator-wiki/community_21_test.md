# test

*Community 21 | 2 files | cohesion 1.00*

## Definition

This community groups 2 file(s) rooted at `test` with dominant language py (cohesion 1.00). Central symbols: `decrypt_data`, `encrypt_data`, `get_encrypted_command`, `post_result`, `send_command_via_web`, `test_discover`, `test_download`, `test_migrate`. Core file: `test/test_commands.py` (15 symbols). Documented purpose: o config.py.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `test/config.py` | py | infrastructure | 2 | yes |
| `test/test_commands.py` | py | testing | 15 | yes |

## Key Symbols

- `encrypt_data` (function, `test/config.py:23`) `def encrypt_data(data)`
- `decrypt_data` (function, `test/config.py:31`) `def decrypt_data(b64_data)`
- `send_command_via_web` (function, `test/test_commands.py:35`) `def send_command_via_web(command)` - Simula enviar un comando vía interfaz web /issue_command con autenticación básica
- `get_encrypted_command` (function, `test/test_commands.py:49`) `def get_encrypted_command()` - Obtiene el comando cifrado del endpoint GET
- `post_result` (function, `test/test_commands.py:56`) `def post_result(result_data)` - Envía el resultado cifrado al C2
- `test_migrate` (function, `test/test_commands.py:69`) `def test_migrate()`
- `test_uac_bypass` (function, `test/test_commands.py:78`) `def test_uac_bypass()`
- `test_portscan` (function, `test/test_commands.py:87`) `def test_portscan()`
- `test_discover` (function, `test/test_commands.py:97`) `def test_discover()`
- `test_proxy` (function, `test/test_commands.py:107`) `def test_proxy()`
- `test_download` (function, `test/test_commands.py:123`) `def test_download()`
- `test_upload` (function, `test/test_commands.py:143`) `def test_upload()`
- `test_persistence` (function, `test/test_commands.py:160`) `def test_persistence()`
- `test_softenum` (function, `test/test_commands.py:169`) `def test_softenum()`
- `test_simulate` (function, `test/test_commands.py:178`) `def test_simulate()`
- `test_reverse_shell` (function, `test/test_commands.py:187`) `def test_reverse_shell()`
- `test_shutdown` (function, `test/test_commands.py:196`) `def test_shutdown()`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 1
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in test changed?
- Should test be split, given cohesion 1.00?

## Sources

- `test/config.py`
- `test/test_commands.py`
