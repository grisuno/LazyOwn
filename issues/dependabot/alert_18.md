# Dependabot Alert #18: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-27025
- **Created:** 2026-06-07T17:50:22Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/18

## Summary
pypdf has possible long runtimes/large memory usage for large /ToUnicode streams

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to long runtimes and large memory consumption. This requires parsing the `/ToUnicode` entry of a font with unusually large values, for example during text extraction.

### Patches

This has been fixed in [pypdf==6.7.1](https://github.com/py-pdf/pypdf/releases/tag/6.7.1).

### Workarounds

If you cannot upgrade yet, consider applying the changes from PR [#3646](https://github.com/py-pdf/pypdf/pull/3646).
