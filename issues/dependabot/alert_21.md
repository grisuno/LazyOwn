# Dependabot Alert #21: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-27888
- **Created:** 2026-06-07T17:50:22Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/21

## Summary
pypdf: Manipulated FlateDecode XFA streams can exhaust RAM

## Description
### Impact
An attacker who uses this vulnerability can craft a PDF which leads to the RAM being exhausted. This requires accessing the `xfa` property of a reader or writer and the corresponding stream being compressed using `/FlateDecode`.

### Patches
This has been fixed in [pypdf==6.7.3](https://github.com/py-pdf/pypdf/releases/tag/6.7.3).

### Workarounds
If projects cannot upgrade yet, consider applying the changes from PR [#3658](https://github.com/py-pdf/pypdf/pull/3658).
