# Subsystem: test

## test/config.py
- Doc: o config.py
- Layer: infrastructure
- Language: py
- Symbols:
  - `encrypt_data` (function, line 24) `def encrypt_data(data)`
  - `decrypt_data` (function, line 33) `def decrypt_data(b64_data)`
- Imported by: `test/test_commands.py`

## test/test_commands.py
- Doc: send_command_via_web: Simula enviar un comando vía interfaz web /issue_command con autenticación...
- Layer: testing
- Language: py
- Symbols:
  - `send_command_via_web` (function, line 36) `def send_command_via_web(command)`
  - `get_encrypted_command` (function, line 51) `def get_encrypted_command()`
  - `post_result` (function, line 59) `def post_result(result_data)`
  - `test_migrate` (function, line 79) `def test_migrate()`
  - `test_uac_bypass` (function, line 89) `def test_uac_bypass()`
  - `test_portscan` (function, line 99) `def test_portscan()`
  - `test_discover` (function, line 110) `def test_discover()`
  - `test_proxy` (function, line 121) `def test_proxy()`
  - `test_download` (function, line 138) `def test_download()`
  - `test_upload` (function, line 159) `def test_upload()`
  - `test_persistence` (function, line 176) `def test_persistence()`
  - `test_softenum` (function, line 186) `def test_softenum()`
  - `test_simulate` (function, line 196) `def test_simulate()`
  - `test_reverse_shell` (function, line 206) `def test_reverse_shell()`
  - `test_shutdown` (function, line 216) `def test_shutdown()`
- Depends on: `test/config.py`
