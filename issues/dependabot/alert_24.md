# Dependabot Alert #24: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-31826
- **Created:** 2026-06-07T17:50:23Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/24

## Summary
pypdf: manipulated stream length values can exhaust RAM

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to large memory usage. This requires parsing a content stream with a rather large `/Length` value, regardless of the actual data length inside the stream.

### Patches
This has been fixed in [pypdf==6.8.0](https://github.com/py-pdf/pypdf/releases/tag/6.8.0).

### Workarounds
If you cannot upgrade yet, consider applying the changes from PR [#3675](https://github.com/py-pdf/pypdf/pull/3675).

As far as we are aware, this mostly affects reading from buffers of unknown size, as returned by `open("file.pdf", mode="rb")` for example. Passing a file path or a `BytesIO` buffer to *pypdf* instead does not seem to trigger the vulnerability.
