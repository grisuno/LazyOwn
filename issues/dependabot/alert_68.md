# Dependabot Alert #68: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-71852
- **Created:** 2026-08-08T01:34:22Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/68

## Summary
pypdf: Possible long runtimes/large memory usage for large CID font width ranges

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to long runtimes and large memory consumption. This requires parsing the font width entries of a font with unusually large values, for example during text extraction.

### Patches

This has been fixed in [pypdf==6.15.0](https://github.com/py-pdf/pypdf/releases/tag/6.15.0).

### Workarounds

If you cannot upgrade yet, consider applying the changes from PR [#3946](https://github.com/py-pdf/pypdf/pull/3946).
