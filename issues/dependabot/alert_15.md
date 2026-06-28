# Dependabot Alert #15: pypdf

- **State:** open
- **Severity:** low
- **CVE:** CVE-2026-22691
- **Created:** 2026-06-07T17:50:22Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/15

## Summary
pypdf has possible long runtimes for malformed startxref

## Description
### Impact
An attacker who exploits this vulnerability can craft a PDF which leads to possibly long runtimes for invalid `startxref` entries. When rebuilding the cross-reference table, PDF files with lots of whitespace characters become problematic. Only the non-strict reading mode is affected.

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
