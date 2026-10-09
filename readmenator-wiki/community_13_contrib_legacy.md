# contrib/legacy

*Community 13 | 5 files | cohesion 0.80*

## Definition

This community groups 5 file(s) rooted at `contrib/legacy` with dominant language py (cohesion 0.80). Central symbols: `base64_decode`, `base64_encode`, `caesar_cipher`, `caesar_decipher`, `decode`, `decode_string`, `encode`, `encode_string`. Core file: `modules/lazyencoder_decoder.py` (10 symbols).

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazycreate_webshell.py` | py | utility | 0 | no |
| `contrib/legacy/lazylogpoisoning.py` | py | utility | 3 | no |
| `contrib/legacy/lazyreversentlmv2.py` | py | utility | 2 | no |
| `modules/lazyencoder_decoder.py` | py | utility | 10 | no |
| `modules/test_lazyencoder_decoder.py` | py | testing | 0 | no |

## Key Symbols

- `ensure_http_prefix` (function, `contrib/legacy/lazylogpoisoning.py:39`) `def ensure_http_prefix(url)`
- `signal_handler` (function, `contrib/legacy/lazylogpoisoning.py:45`) `def signal_handler(sig, frame)`
- `main` (function, `contrib/legacy/lazylogpoisoning.py:53`) `def main()`
- `parse_hash_file` (function, `contrib/legacy/lazyreversentlmv2.py:11`) `def parse_hash_file(file_path)`
- `reverse_shell` (function, `contrib/legacy/lazyreversentlmv2.py:58`) `def reverse_shell(target_ip, username, domain, lmhash, nthash, callback_ip, call`
- `base64_encode` (function, `modules/lazyencoder_decoder.py:4`) `def base64_encode(data)`
- `base64_decode` (function, `modules/lazyencoder_decoder.py:8`) `def base64_decode(data)`
- `caesar_cipher` (function, `modules/lazyencoder_decoder.py:13`) `def caesar_cipher(text, shift)`
- `caesar_decipher` (function, `modules/lazyencoder_decoder.py:27`) `def caesar_decipher(text, shift)`
- `key_substitution` (function, `modules/lazyencoder_decoder.py:31`) `def key_substitution(text, key)`
- `key_substitution_reverse` (function, `modules/lazyencoder_decoder.py:47`) `def key_substitution_reverse(text, key)`
- `encode` (function, `modules/lazyencoder_decoder.py:63`) `def encode(data, shift, key)`
- `encode_string` (function, `modules/lazyencoder_decoder.py:75`) `def encode_string(data, shift, key)`
- `decode` (function, `modules/lazyencoder_decoder.py:82`) `def decode(data, shift, key)`
- `decode_string` (function, `modules/lazyencoder_decoder.py:94`) `def decode_string(data, shift, key)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 4
- Cross-boundary resolved imports (EXTRACTED): 1

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- [taint high] `cli/banner_config.py` -> `modules/lazyencoder_decoder.py` via `subprocess` (5 hops)

## Open Questions

- Why do 5 file(s) lack file-level docs (e.g. `contrib/legacy/lazycreate_webshell.py`)? What purpose do they serve?
- What would break if the most connected file in contrib/legacy changed?
- Should contrib/legacy be split, given cohesion 0.80?

## Sources

- `contrib/legacy/lazycreate_webshell.py`
- `contrib/legacy/lazylogpoisoning.py`
- `contrib/legacy/lazyreversentlmv2.py`
- `modules/lazyencoder_decoder.py`
- `modules/test_lazyencoder_decoder.py`
