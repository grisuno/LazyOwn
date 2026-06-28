# Dependabot Alert #20: pypdf

- **State:** open
- **Severity:** low
- **CVE:** CVE-2026-27628
- **Created:** 2026-06-07T17:50:22Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/20

## Summary
pypdf has a possible infinite loop when loading circular /Prev entries in cross-reference streams

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to an infinite loop. This requires reading the file.

### Patches

This has been fixed in [pypdf==6.7.2](https://github.com/py-pdf/pypdf/releases/tag/6.7.2).

### Workarounds

If users cannot upgrade yet, consider applying the changes from PR [#3655](https://github.com/py-pdf/pypdf/pull/3655).
