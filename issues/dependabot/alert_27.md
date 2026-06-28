# Dependabot Alert #27: cryptography

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-39892
- **Created:** 2026-06-07T17:50:23Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/27

## Summary
Cryptography vulnerable to buffer overflow if non-contiguous buffers were passed to APIs

## Description
If a non-contiguous buffer was passed to APIs which accepted Python buffers (e.g. `Hash.update()`), this could lead to buffer overflows. For example:

```python
h = Hash(SHA256())
b.update(buf[::-1])
```

would read past the end of the buffer on Python >3.11
