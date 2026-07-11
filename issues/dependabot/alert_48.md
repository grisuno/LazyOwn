# Dependabot Alert #48: soupsieve

- **State:** open
- **Severity:** high
- **CVE:** CVE-2026-49477
- **Created:** 2026-07-10T20:17:53Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/48

## Summary
Soup Sieve: Regular Expression Denial of Service (ReDoS) via Selector Parser

## Description
### Summary

The CSS selector parser in soupsieve (the CSS selector engine for Beautiful Soup 4) contains a regular expression vulnerable to catastrophic backtracking. When processing an attribute selector with an unterminated quoted value, the `VALUE` regex pattern in `css_parser.py` enters exponential backtracking. A payload of only **300 bytes** causes the regex engine to hang for **over 3 seconds**, enabling a trivial Regular Expression Denial of Service (ReDoS) attack.

To be completely transparent, AI tools helped surface this issue. However, this was independently reproduced and carefully validated.

Any application that passes untrusted CSS selector strings to `soupsieve.compile()` or Beautiful Soup's `.select()` / `.select_one()` is affected.

### Details

**Affected code:** `soupsieve/css_parser.py`, line ~121 - `RE_VALUES` / `VALUE` regex pattern

The soupsieve CSS parser uses a compiled regular expression to tokenise attribute selector values. This pattern matches both quoted strings (`"value"` or `'value'`) and unquoted identifiers. The regex contains alternation branches for:

1. Double-quoted strings: `"[^"\\]*(?:\\.[^"\\]*)*"`
2. Single-quoted strings: `'[^'\\]*(?:\\.[^'\\]*)*'`
3. Unquoted identifiers

When an attribute selector contains an **unterminated quoted value** - e.g., `[a="xxxx...` (opening `"` but no closing `"`) -” the regex engine attempts to match the quoted-string branch. After that branch fails (no closing quote), the engine backtracks and attempts to match the remaining input against subsequent alternation branches and parent patterns. The structure of the pattern causes **catastrophic backtracking** where the number of backtracking steps grows exponentially with the length of the content between the opening quote and the end of the string.

**Root cause:** The regex pattern does not anchor or guard against the case where a quoted string is never terminated. The overlapping character classes across alternation branches create exponential backtracking when the quoted-string branch fails on long input.

**Key characteristics:**
- **Input size:** Only 300 bytes are needed to trigger a >3 second hang
- **Amplification:** Each additional character approximately doubles the backtracking time
- **No memory impact:** The attack consumes CPU only (regex backtracking is compute-bound)

### Proof of Concept

```python
import time
import soupsieve as sv

PAYLOAD_LEN = 300

# Control: well-formed selector with terminated quote (completes instantly)
well_formed = '[a="' + ('x' * PAYLOAD_LEN) + '"]'
start = time.perf_counter()
try:
    sv.compile(well_formed)
except Exception:
    pass
control_time = time.perf_counter() - start
print(f"Well-formed selector ({len(well_formed)} bytes): {control_time:.4f}s")

# Exploit: unterminated quote triggers catastrophic regex backtracking
malformed = '[a="' + ('x' * PAYLOAD_LEN)
start = time.perf_counter()
try:
    sv.compile(malformed)  # WARNING: This will hang for >3 seconds
except Exception:
    pass
exploit_time = time.perf_counter() - start
print(f"Malformed selector ({len(malformed)} bytes): {exploit_time:.4f}s")

slowdown = exploit_time / max(control_time, 1e-9)
print(f"Slowdown: {slowdown:.0f}x")

# Expected output:
# Well-formed selector (306 bytes): ~0.001s
# Malformed selector (304 bytes): >3.0s (may need to be killed)
# Slowdown: >3000x
#
# NOTE: On some systems the malformed selector may hang indefinitely.
# Use a timeout mechanism (signal.alarm, threading.Timer) when testing.
```

**Safe testing variant with timeout:**

```python
import signal
import soupsieve as sv

def timeout_handler(signum, frame):
    raise TimeoutError("ReDoS confirmed: regex backtracking exceeded timeout")

PAYLOAD_LEN = 300
malformed = '[a="' + ('x' * PAYLOAD_LEN)

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(3)  # 3-second timeout

try:
    sv.compile(malformed)
    print("Selector compiled (not vulnerable)")
except TimeoutError as e:
    print(f"VULNERABLE: {e}")
except Exception as e:
    print(f"Other error: {e}")
finally:
    signal.alarm(0)  # Cancel the alarm
```

### Impact

**Severity: High**

An attacker can cause CPU exhaustion on any server-side Python application that compiles user-supplied CSS selectors via soupsieve. The attack is particularly dangerous because:

1. **Tiny payload:** Only 300 bytes are needed - well within typical URL parameter, form field, or API request limits
2. **No special characters:** The payload consists entirely of printable ASCII characters (`[a="xxx...`)
3. **Exponential scaling:** Each additional byte approximately doubles the backtracking time, making the attack easily tuneable
4. **Thread blocking:** The regex engine blocks the calling thread with no opportunity for interruption (except via OS signals)

| Parameter | Value |
|---|---|
| Input size | 300 bytes |
| CPU time consumed | >3 seconds (exponential with payload length) |
| Memory consumed | Negligible (CPU-only attack) |
| Authentication required | None |
| User interaction required | None |

**Deployment impact:** In threaded or async web applications, a single malicious request blocks a worker thread for the duration of the backtracking. An attacker can submit multiple concurrent requests to exhaust all available workers, causing complete service denial. The small payload size makes the attack easy to deliver and difficult to detect via request size limits.

**Downstream exposure:** soupsieve is an automatic dependency of `beautifulsoup4`, one of the most widely installed Python packages. Any web application, API, or service that accepts CSS selectors from users is potentially affected.

---

### Credit

The vulnerability was discovered by a security research team from the University of Sydney, whose focus is detecting open source software vulnerabilities.
Liyi Zhou: https://lzhou1110.github.io/
Ziyue Wang: https://zyy0530.github.io/
Strick: https://str1ckl4nd.github.io/
Maurice: https://maurice.busystar.org/
Chenchen Yu: https://7thparkk.github.io/
