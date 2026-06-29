# Dependabot Alert #41: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-54530
- **Created:** 2026-06-19T22:26:48Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/41

## Summary
pypdf: Possible infinite loop when retrieving fonts for layout-mode text extraction

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to an infinite loop. This requires extracting the text in layout mode.

### Patches

This has been fixed in [pypdf==6.13.0](https://github.com/py-pdf/pypdf/releases/tag/6.13.0).

### Workarounds

If you cannot upgrade yet, consider applying the changes from PR [#3830](https://github.com/py-pdf/pypdf/pull/3830).
