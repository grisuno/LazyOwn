# Dependabot Alert #28: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-40260
- **Created:** 2026-06-07T17:50:23Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/28

## Summary
pypdf: Manipulated XMP metadata entity declarations can exhaust RAM

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to large memory usage. This requires parsing the XMP metadata.

### Patches
This has been fixed in [pypdf==6.10.0](https://github.com/py-pdf/pypdf/releases/tag/6.10.0).

### Workarounds
If you cannot upgrade yet, consider applying the changes from PR [#3724](https://github.com/py-pdf/pypdf/pull/3724).
