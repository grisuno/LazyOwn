# Dependabot Alert #26: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-33699
- **Created:** 2026-06-07T17:50:23Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/26

## Summary
pypdf: Possible infinite loop during recovery attempts in DictionaryObject.read_from_stream

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to an infinite loop. This requires reading a file in non-strict mode.

### Patches

This has been fixed in [pypdf==6.9.2](https://github.com/py-pdf/pypdf/releases/tag/6.9.2).

### Workarounds

If users cannot upgrade yet, consider applying the changes from PR [#3693](https://github.com/py-pdf/pypdf/pull/3693).
