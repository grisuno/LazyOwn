# Dependabot Alert #40: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-54531
- **Created:** 2026-06-19T22:26:26Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/40

## Summary
pypdf: Possible infinite loop when processing outlines/bookmarks in writer

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to an infinite loop. This requires merging a file with outlines into a writer.

### Patches

This has been fixed in [pypdf==6.13.0](https://github.com/py-pdf/pypdf/releases/tag/6.13.0).

### Workarounds

If you cannot upgrade yet, consider applying the changes from PR [#3830](https://github.com/py-pdf/pypdf/pull/3830).
