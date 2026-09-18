# modules/backdoor

*Community 12 | 2 files | cohesion 1.00*

## Definition

This community groups 2 file(s) rooted at `modules/backdoor` with dominant language c (cohesion 1.00). Central symbols: `Shell`, `WinMain`, `bootRun`, `bzero`, `logg`, `str_cut`. Core file: `modules/backdoor/backdoor.c` (5 symbols).

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/backdoor/backdoor.c` | c | utility | 5 | no |
| `modules/backdoor/keylogger.h` | h | infrastructure | 1 | no |

## Key Symbols

- `bzero` (macro, `modules/backdoor/backdoor.c:14`) `#define bzero(p, size)`
- `bootRun` (function, `modules/backdoor/backdoor.c:18`) `int bootRun()`
- `str_cut` (function, `modules/backdoor/backdoor.c:49`) `char * str_cut(char str[], int slice_from, int slice_to)`
- `Shell` (function, `modules/backdoor/backdoor.c:84`) `void Shell()`
- `WinMain` (function, `modules/backdoor/backdoor.c:125`) `int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrev, LPSTR lpCmdLine, int`
- `logg` (function, `modules/backdoor/keylogger.h:1`) `DWORD WINAPI logg(LPVOID lpParam)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 1
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- [dataflow UNCHECKED_ALLOC] `modules/backdoor/backdoor.c:79` `str_cut` `buffer`: Result of allocator stored in `buffer` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/backdoor/backdoor.c:145` `WinMain` `sock`: Result of allocator stored in `sock` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/backdoor/keylogger.h:95` `logg` `kh`: Result of allocator stored in `kh` is never checked against NULL.

## Open Questions

- Why do 2 file(s) lack file-level docs (e.g. `modules/backdoor/backdoor.c`)? What purpose do they serve?
- What would break if the most connected file in modules/backdoor changed?
- Should modules/backdoor be split, given cohesion 1.00?

## Sources

- `modules/backdoor/backdoor.c`
- `modules/backdoor/keylogger.h`
