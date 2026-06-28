# Dependabot Alert #19: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-27026
- **Created:** 2026-06-07T17:50:22Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/19

## Summary
pypdf possibly has long runtimes for malformed FlateDecode streams

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to long runtimes. This requires a malformed `/FlateDecode` stream, where the byte-by-byte decompression is used.

### Patches

This has been fixed in [pypdf==6.7.1](https://github.com/py-pdf/pypdf/releases/tag/6.7.1).

### Workarounds

If you cannot upgrade yet, consider applying the changes from PR [#3644](https://github.com/py-pdf/pypdf/pull/3644).
