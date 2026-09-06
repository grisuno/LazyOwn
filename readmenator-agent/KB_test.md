# Subsystem: test

## test/config.py
- Layer: infrastructure
- Doc: conftest.py o config.py
- Language: py
- Symbols:
  - `encrypt_data` (function, line 23) `def encrypt_data(data)`
  - `decrypt_data` (function, line 31) `def decrypt_data(b64_data)`
- Imported by: `test/test_commands.py`

## test/test_commands.py
- Layer: testing
- Doc: test_commands.py
- Language: py
- Symbols:
  - `send_command_via_web` (function, line 35) `def send_command_via_web(command)`
  - `get_encrypted_command` (function, line 49) `def get_encrypted_command()`
  - `post_result` (function, line 56) `def post_result(result_data)`
  - `test_migrate` (function, line 69) `def test_migrate()`
  - `test_uac_bypass` (function, line 78) `def test_uac_bypass()`
  - `test_portscan` (function, line 87) `def test_portscan()`
  - `test_discover` (function, line 97) `def test_discover()`
  - `test_proxy` (function, line 107) `def test_proxy()`
  - `test_download` (function, line 123) `def test_download()`
  - `test_upload` (function, line 143) `def test_upload()`
  - `test_persistence` (function, line 160) `def test_persistence()`
  - `test_softenum` (function, line 169) `def test_softenum()`
  - `test_simulate` (function, line 178) `def test_simulate()`
  - `test_reverse_shell` (function, line 187) `def test_reverse_shell()`
  - `test_shutdown` (function, line 196) `def test_shutdown()`
- Depends on: `test/config.py`
