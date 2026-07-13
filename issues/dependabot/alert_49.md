# Dependabot Alert #49: soupsieve

- **State:** open
- **Severity:** high
- **CVE:** CVE-2026-49476
- **Created:** 2026-07-10T20:18:18Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/49

## Summary
Soup Sieve has Memory Exhaustion via Large Comma-Separated Selector Lists

## Description
### Summary

The CSS selector parser in soupsieve (the CSS selector engine for Beautiful Soup 4) allocates unbounded memory when compiling large comma-separated selector lists. An attacker who can supply a crafted CSS selector string to `soupsieve.compile()` or Beautiful Soup's `.select()` / `.select_one()` can cause the application to allocate hundreds of megabytes of heap memory from a relatively small input, leading to memory exhaustion and denial of service.

To be completely transparent, AI tools helped surface this issue. However, it was independently reproduced and carefully validated. Researchers follow responsible disclosure practices and originally shared this report privately.

A **500 KB** selector string triggers allocation of approximately **244 MB** of heap memory - a 488x— amplification ratio**.

### Details

**Affected code:** `soupsieve/css_parser.py`, lines ~204, 925, 1106

The soupsieve CSS parser splits comma-separated selector lists and creates one `CSSSelector` object per list item. Each `CSSSelector` object contains parsed selector data structures including `SelectorList`, `Selector`, and associated tag/attribute/pseudo-class metadata.

When a selector string such as `a,a,a,...` (with 250,000 comma-separated items) is passed to `sv.compile()`, the parser:

1. Tokenises the entire string and identifies each comma-delimited segment (line ~1106)
2. Parses each segment into a full `Selector` object with all associated metadata (line ~925)
3. Stores all parsed selectors in a `SelectorList` (line ~204)

**Root cause:** No limit is enforced on the number of selectors in a comma-separated list. The parser will attempt to parse and store an arbitrary number of selectors, with each selector object consuming approximately **976 bytes** of heap memory. The total allocation scales linearly with the number of list items, but the amplification ratio (output memory / input bytes) is extremely high because each single-character selector like `a` expands into a complex object graph.

**Attack surface:** Any application that passes user-supplied CSS selectors to `soupsieve.compile()` or Beautiful Soup's `.select()` / `.select_one()`.

### Proof of Concept

```python
import tracemalloc
import soupsieve as sv

tracemalloc.start()

# Build a 500 KB selector string: "a,a,a,...,a" (250,000 items)
count = 250_000
selector = ",".join("a" for _ in range(count))
print(f"Selector string size: {len(selector):,} bytes ({len(selector) / 1024:.0f} KB)")

# Compile the selector â€” this allocates ~244 MB
compiled = sv.compile(selector)

current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"Compiled selector count: {len(compiled.selectors):,}")
print(f"Current memory: {current / 1024 / 1024:.1f} MB")
print(f"Peak memory: {peak / 1024 / 1024:.1f} MB")
print(f"Amplification ratio: {peak / len(selector):.0f}x")

# Expected output:
# Selector string size: 499,999 bytes (488 KB)
# Compiled selector count: 250,000
# Current memory: ~244 MB
# Peak memory: ~244 MB
# Amplification ratio: ~488x
```

### Impact

**Severity: High**

An attacker can exhaust available memory on any server-side Python application that compiles user-supplied CSS selectors via soupsieve. This can cause:

- **OOM kills** in containerised deployments (Kubernetes pods, Docker containers) with memory limits
- **Swap thrashing** on bare-metal servers, degrading performance for all co-located processes
- **Process termination** via Python's `MemoryError` exception if the system runs out of addressable memory

| Parameter | Value |
|---|---|
| Input size | ~500 KB selector string |
| Memory allocated | ~244 MB |
| Amplification ratio | ~488Ã— |
| Per-object overhead | ~976 bytes per selector |
| Authentication required | None |
| User interaction required | None |

**Scalability of attack:** The memory allocation scales linearly - doubling the selector count doubles memory usage. An attacker can tune the payload to exactly exhaust a target's memory limits. Multiple concurrent requests multiply the effect.

**Downstream exposure:** soupsieve is an automatic dependency of `beautifulsoup4`, one of the most widely installed Python packages. Any web application accepting CSS selectors from users (e.g., web scraping APIs, content filtering tools, CMS preview features) is potentially affected.

---
### Credit

Discovered by a security research team from the University of Sydney, focused on detecting open source software vulnerabilities.
Liyi Zhou: https://lzhou1110.github.io/
Ziyue Wang: https://zyy0530.github.io/
Strick: https://str1ckl4nd.github.io/
Maurice: https://maurice.busystar.org/
Chenchen Yu: https://7thparkk.github.io/
