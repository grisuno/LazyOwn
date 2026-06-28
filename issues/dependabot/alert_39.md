# Dependabot Alert #39: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-49460
- **Created:** 2026-06-19T22:06:06Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/39

## Summary
pypdf: Inefficient decoding of FlateDecode PNG predictor streams

## Description
### Impact
An attacker who uses this vulnerability can craft a PDF which leads to long runtimes. This requires accessing a stream which uses the `/FlateDecode` filter with a PNG predictor.

### Patches
This has been fixed in [pypdf==6.12.2](https://github.com/py-pdf/pypdf/releases/tag/6.12.2).

### Workarounds
If you cannot upgrade yet, consider applying the changes from PR [#3806](https://github.com/py-pdf/pypdf/pull/3806).
