# Dependabot Alert #13: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2025-66019
- **Created:** 2026-06-07T17:50:21Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/13

## Summary
pypdf's LZWDecode streams be manipulated to exhaust RAM

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to a memory usage of up to 1 GB per stream. This requires parsing the content stream of a page using the LZWDecode filter.

This is a follow up to [GHSA-jfx9-29x2-rv3j](https://github.com/py-pdf/pypdf/security/advisories/GHSA-jfx9-29x2-rv3j) to align the default limit with the one for *zlib*.

### Patches
This has been fixed in [pypdf==6.4.0](https://github.com/py-pdf/pypdf/releases/tag/6.4.0).

### Workarounds
If users cannot upgrade yet, use the line below to overwrite the default in their code:

```python
pypdf.filters.LZW_MAX_OUTPUT_LENGTH = 75_000_000
```
