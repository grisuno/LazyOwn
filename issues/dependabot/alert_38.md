# Dependabot Alert #38: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-49461
- **Created:** 2026-06-19T22:06:03Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/38

## Summary
pypdf: Possible large memory usage for form XObjects during text extraction

## Description
### Impact
An attacker who uses this vulnerability can craft a PDF which leads to large memory usage. This requires extracting the text of a page which contains a form XObject with self-references.

### Patches
This has been fixed in [pypdf==6.12.2](https://github.com/py-pdf/pypdf/releases/tag/6.12.2).

### Workarounds
If you cannot upgrade yet, consider applying the changes from PR [#3805](https://github.com/py-pdf/pypdf/pull/3805).
