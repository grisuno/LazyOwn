# Dependabot Alert #16: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-24688
- **Created:** 2026-06-07T17:50:22Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/16

## Summary
pypdf has possible Infinite Loop when processing outlines/bookmarks

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to an infinite loop. This requires accessing the outlines/bookmarks.

### Patches

This has been fixed in [pypdf 6.6.2](https://github.com/py-pdf/pypdf/releases/tag/6.6.2).

### Workarounds

If projects cannot upgrade yet, consider applying the changes from PR [#3610](https://github.com/py-pdf/pypdf/pull/3610).
