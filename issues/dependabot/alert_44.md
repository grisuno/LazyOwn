# Dependabot Alert #44: msgpack

- **State:** open
- **Severity:** high
- **CVE:** N/A
- **Created:** 2026-06-20T15:39:20Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/44

## Summary
MessagePack for Python: Out-of-bounds read / crash on Unpacker reuse after a caught error

## Description
### Impact

If the Unpacker is used repeatedly after an error occurs, the process may crash with a SEGV.

If the Unpacker is used repeatedly to unpack untrusted input from external sources, it may be vulnerable to a DoS attack.

### Patches

v1.2.1

### Workarounds

Users should create a new Unpacker instead of reusing the same Unpacker after an error occurs.

Applying the above patch can prevent SEGV, but reusing the Streaming Unpacker after it has encountered an error will not yield correct data. If an error occurs during Streaming Unpacking, the Stream and Streaming Unpacker should be discarded.

Therefore, this is not just a workaround but the correct solution. The above patch only prevents crashes from incorrect usage.
