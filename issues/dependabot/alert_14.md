# Dependabot Alert #14: pypdf

- **State:** open
- **Severity:** low
- **CVE:** CVE-2026-22690
- **Created:** 2026-06-07T17:50:21Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/14

## Summary
pypdf has possible long runtimes for missing /Root object with large /Size values

## Description
### Impact
An attacker who exploits this vulnerability can craft a PDF which leads to possibly long runtimes for actually invalid files. This can be achieved by omitting the `/Root` entry in the trailer, while using a rather large `/Size` value. Only the non-strict reading mode is affected.

### Patches
This has been fixed in [pypdf==6.6.0](https://github.com/py-pdf/pypdf/releases/tag/6.6.0).

### Workarounds

```python
from pypdf import PdfReader, PdfWriter


# Instead of
reader = PdfReader("file.pdf")
# use the strict mode:
reader = PdfReader("file.pdf", strict=True)

# Instead of
writer = PdfWriter(clone_from="file.pdf")
# use an explicit strict reader:
writer = PdfWriter(clone_from=PdfReader("file.pdf", strict=True))
```

### Resources
This issue has been fixed in #3594.
