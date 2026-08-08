# Dependabot Alert #69: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-71870
- **Created:** 2026-08-08T01:34:22Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/69

## Summary
pypdf: Possible large memory usage for large /ToUnicode streams

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to large memory consumption. This requires parsing the `/ToUnicode` entry of a font with unusually large values, for example during text extraction.

### Patches

This has been fixed in [pypdf==6.15.0](https://github.com/py-pdf/pypdf/releases/tag/6.15.0).

### Workarounds

If you cannot upgrade yet, consider applying the changes from PR [#3944](https://github.com/py-pdf/pypdf/pull/3944).
