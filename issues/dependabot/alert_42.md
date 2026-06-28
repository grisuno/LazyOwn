# Dependabot Alert #42: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** N/A
- **Created:** 2026-06-20T08:07:14Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/42

## Summary
pypdf: Missing stream length values ignore defined limits

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to large memory usage, as `MAX_DECLARED_STREAM_LENGTH` is sometimes ignored. This requires parsing a content stream without a `/Length` value.

### Patches
This has been fixed in [pypdf==6.13.3](https://github.com/py-pdf/pypdf/releases/tag/6.13.3).

### Workarounds
If you cannot upgrade yet, consider applying the changes from PR [#3871](https://github.com/py-pdf/pypdf/pull/3871).
