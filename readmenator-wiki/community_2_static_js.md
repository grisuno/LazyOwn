# static/js

*Community 2 | 18 files | cohesion 0.54*

## Definition

This community groups 18 file(s) rooted at `static/js` with dominant language js (cohesion 0.54). Central symbols: `A`, `As`, `B`, `BackgroundSize`, `BezierCurve`, `Bk`, `Bounds`, `Break`. Core file: `static/js/html2pdf.bundle.min.js` (695 symbols). Documented purpose: ``assign`` business logic.  Extracted from :class:`LazyOwnShell.do_assign` so the persistence and validation behaviour can be unit-tested without booting the cm.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/assign.py` | py | utility | 1 | yes |
| `cli/show.py` | py | utility | 1 | yes |
| `lazyc2/state.py` | py | utility | 0 | yes |
| `lazyown-docker/init.sh` | sh | utility | 0 | no |
| `modules/rootkit/rootkit.c` | c | utility | 13 | yes |
| `static/js/bootstrap-4.5.2.min.js` | js | infrastructure | 7 | yes |
| `static/js/bootstrap-5.3.0.bundle.min.js` | js | infrastructure | 28 | yes |
| `static/js/chart.min.js` | js | utility | 88 | yes |
| `static/js/html2pdf.bundle.min.js` | js | utility | 695 | no |
| `static/js/jquery-3.5.1.slim.min.js` | js | data_access | 6 | yes |
| `static/js/particles.js` | js | utility | 10 | yes |
| `static/js/popper-2.5.4.min.js` | js | utility | 1 | no |
| `static/js/quill-2.0.3.js` | js | presentation | 124 | yes |
| `static/js/tippy-6.js` | js | utility | 3 | no |
| `static/js/vis-network-9.1.2.min.js` | js | business_logic | 135 | no |
| `static/js/vis-network.min.js` | js | business_logic | 135 | no |
| `static/js/xterm.js` | js | utility | 62 | no |
| `tests/test_cli_assign.py` | py | testing | 36 | yes |

## Key Symbols

- `apply_assign` (function, `cli/assign.py:36`) `def apply_assign(params, key, value)` - Validate, mutate and persist a single payload assignment.
- `format_payload` (function, `cli/show.py:14`) `def format_payload(params)` - Render ``params`` as a sorted, aligned ``key = value`` block.
- `HIDDEN_PROCESS_NAME` (macro, `modules/rootkit/rootkit.c:26`) `#define HIDDEN_PROCESS_NAME`
- `HIDDEN_FILE_NAME` (macro, `modules/rootkit/rootkit.c:27`) `#define HIDDEN_FILE_NAME`
- `LISTENER_IP` (macro, `modules/rootkit/rootkit.c:28`) `#define LISTENER_IP`
- `LISTENER_PORT` (macro, `modules/rootkit/rootkit.c:29`) `#define LISTENER_PORT`
- `SPECIAL_STRING` (macro, `modules/rootkit/rootkit.c:31`) `#define SPECIAL_STRING`
- `SPECIAL_STRING_PORT` (macro, `modules/rootkit/rootkit.c:34`) `#define SPECIAL_STRING_PORT`
- `regs_override_return` (function, `modules/rootkit/rootkit.c:43`) `static inline void regs_override_return(struct pt_regs *regs, long new_ret)` - Define regs_override_return function
- `hooked_getdents` (function, `modules/rootkit/rootkit.c:75`) `static int hooked_getdents(struct kretprobe_instance *ri, struct pt_regs *regs)` - Hooked getdents function
- `hooked_getdents64` (function, `modules/rootkit/rootkit.c:101`) `static int hooked_getdents64(struct kretprobe_instance *ri, struct pt_regs *regs` - Hooked getdents64 function
- `hooked_read` (function, `modules/rootkit/rootkit.c:127`) `static int hooked_read(struct kretprobe_instance *ri, struct pt_regs *regs)` - Hooked read function to create a backdoor
- `disable_module_signature_verification` (function, `modules/rootkit/rootkit.c:181`) `static void disable_module_signature_verification(void)` - Function to disable module signature verification
- `hook_syscalls` (function, `modules/rootkit/rootkit.c:195`) `static int __init hook_syscalls(void)` - Function to hook system calls
- `unhook_syscalls` (function, `modules/rootkit/rootkit.c:208`) `static void __exit unhook_syscalls(void)` - Function to unhook system calls
- `r` (function, `static/js/bootstrap-4.5.2.min.js:6`) - ! Bootstrap v4.5.2 (https://getbootstrap.com/) Copyright 2011-2020 The Bootstrap Authors (https://gi
- `i` (function, `static/js/bootstrap-4.5.2.min.js:6`) - ! Bootstrap v4.5.2 (https://getbootstrap.com/) Copyright 2011-2020 The Bootstrap Authors (https://gi
- `n` (function, `static/js/bootstrap-4.5.2.min.js:6`) - ! Bootstrap v4.5.2 (https://getbootstrap.com/) Copyright 2011-2020 The Bootstrap Authors (https://gi
- `s` (function, `static/js/bootstrap-4.5.2.min.js:6`) - ! Bootstrap v4.5.2 (https://getbootstrap.com/) Copyright 2011-2020 The Bootstrap Authors (https://gi
- `d` (function, `static/js/bootstrap-4.5.2.min.js:6`) - ! Bootstrap v4.5.2 (https://getbootstrap.com/) Copyright 2011-2020 The Bootstrap Authors (https://gi
- `h` (function, `static/js/bootstrap-4.5.2.min.js:6`) - ! Bootstrap v4.5.2 (https://getbootstrap.com/) Copyright 2011-2020 The Bootstrap Authors (https://gi
- `i` (function, `static/js/bootstrap-4.5.2.min.js:6`) - ! Bootstrap v4.5.2 (https://getbootstrap.com/) Copyright 2011-2020 The Bootstrap Authors (https://gi
- `n` (function, `static/js/bootstrap-5.3.0.bundle.min.js:6`) - ! Bootstrap v5.3.0 (https://getbootstrap.com/) Copyright 2011-2023 The Bootstrap Authors (https://gi
- `i` (function, `static/js/bootstrap-5.3.0.bundle.min.js:6`) - ! Bootstrap v5.3.0 (https://getbootstrap.com/) Copyright 2011-2023 The Bootstrap Authors (https://gi
- `o` (function, `static/js/bootstrap-5.3.0.bundle.min.js:6`) - ! Bootstrap v5.3.0 (https://getbootstrap.com/) Copyright 2011-2023 The Bootstrap Authors (https://gi
- `a` (function, `static/js/bootstrap-5.3.0.bundle.min.js:6`) - ! Bootstrap v5.3.0 (https://getbootstrap.com/) Copyright 2011-2023 The Bootstrap Authors (https://gi
- `r` (function, `static/js/bootstrap-5.3.0.bundle.min.js:6`) - ! Bootstrap v5.3.0 (https://getbootstrap.com/) Copyright 2011-2023 The Bootstrap Authors (https://gi
- `n` (function, `static/js/bootstrap-5.3.0.bundle.min.js:6`) - ! Bootstrap v5.3.0 (https://getbootstrap.com/) Copyright 2011-2023 The Bootstrap Authors (https://gi
- `i` (function, `static/js/bootstrap-5.3.0.bundle.min.js:6`) - ! Bootstrap v5.3.0 (https://getbootstrap.com/) Copyright 2011-2023 The Bootstrap Authors (https://gi
- `n` (function, `static/js/bootstrap-5.3.0.bundle.min.js:6`) - ! Bootstrap v5.3.0 (https://getbootstrap.com/) Copyright 2011-2023 The Bootstrap Authors (https://gi

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 176
- Cross-boundary resolved imports (EXTRACTED): 40

## Connections

- [EXTRACTED] depends_on community 2 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/assign.py imports core/payload_schema.py.
- [EXTRACTED] depends_on community 0 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/misc_migrated.py imports cli/assign.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- Why do 7 file(s) lack file-level docs (e.g. `lazyown-docker/init.sh`)? What purpose do they serve?
- What would break if the most connected file in static/js changed?
- Should static/js be split, given cohesion 0.54?

## Sources

- `cli/assign.py`
- `cli/show.py`
- `lazyc2/state.py`
- `lazyown-docker/init.sh`
- `modules/rootkit/rootkit.c`
- `static/js/bootstrap-4.5.2.min.js`
- `static/js/bootstrap-5.3.0.bundle.min.js`
- `static/js/chart.min.js`
- `static/js/html2pdf.bundle.min.js`
- `static/js/jquery-3.5.1.slim.min.js`
- `static/js/particles.js`
- `static/js/popper-2.5.4.min.js`
- `static/js/quill-2.0.3.js`
- `static/js/tippy-6.js`
- `static/js/vis-network-9.1.2.min.js`
- `static/js/vis-network.min.js`
- `static/js/xterm.js`
- `tests/test_cli_assign.py`
