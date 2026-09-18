# modules/legacy

*Community 13 | 5 files | cohesion 0.80*

## Definition

This community groups 5 file(s) rooted at `modules/legacy` with dominant language py (cohesion 0.80). Central symbols: `base64_decode`, `base64_encode`, `caesar_cipher`, `caesar_decipher`, `decode`, `decode_string`, `encode`, `encode_string`. Core file: `modules/lazyencoder_decoder.py` (10 symbols).

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/lazyencoder_decoder.py` | py | utility | 10 | no |
| `modules/legacy/lazycreate_webshell.py` | py | utility | 0 | no |
| `modules/legacy/lazylogpoisoning.py` | py | utility | 3 | no |
| `modules/legacy/lazyreversentlmv2.py` | py | utility | 2 | no |
| `modules/test_lazyencoder_decoder.py` | py | testing | 0 | no |

## Key Symbols

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
- `ensure_http_prefix` (function, `modules/legacy/lazylogpoisoning.py:39`) `def ensure_http_prefix(url)`
- `signal_handler` (function, `modules/legacy/lazylogpoisoning.py:45`) `def signal_handler(sig, frame)`
- `main` (function, `modules/legacy/lazylogpoisoning.py:53`) `def main()`
- `parse_hash_file` (function, `modules/legacy/lazyreversentlmv2.py:11`) `def parse_hash_file(file_path)`
- `reverse_shell` (function, `modules/legacy/lazyreversentlmv2.py:58`) `def reverse_shell(target_ip, username, domain, lmhash, nthash, callback_ip, call`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 4
- Cross-boundary resolved imports (EXTRACTED): 1

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- Why do 5 file(s) lack file-level docs (e.g. `modules/lazyencoder_decoder.py`)? What purpose do they serve?
- What would break if the most connected file in modules/legacy changed?
- Should modules/legacy be split, given cohesion 0.80?

## Sources

- `modules/lazyencoder_decoder.py`
- `modules/legacy/lazycreate_webshell.py`
- `modules/legacy/lazylogpoisoning.py`
- `modules/legacy/lazyreversentlmv2.py`
- `modules/test_lazyencoder_decoder.py`
