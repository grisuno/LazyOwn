# Dependabot Alert #23: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-28804
- **Created:** 2026-06-07T17:50:23Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/23

## Summary
pypdf vulnerable to inefficient decoding of ASCIIHexDecode streams

## Description
### Impact
An attacker who uses this vulnerability can craft a PDF which leads to long runtimes. This requires accessing a stream which uses the `/ASCIIHexDecode` filter.

### Patches
This has been fixed in [pypdf==6.7.5](https://github.com/py-pdf/pypdf/releases/tag/6.7.5).

### Workarounds
If you cannot upgrade yet, consider applying the changes from PR [#3666](https://github.com/py-pdf/pypdf/pull/3666).
