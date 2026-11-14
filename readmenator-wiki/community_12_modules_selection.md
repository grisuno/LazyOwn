# modules/selection

*Community 12 | 37 files | cohesion 0.66*

## Definition

This community groups 37 file(s) rooted at `modules/selection` with dominant language py (cohesion 0.66). Central symbols: `ActionDecision`, `AdversarySelector`, `AtomicSelector`, `BridgeSelector`, `ChainSelector`, `CredentialSpraySelector`, `EDBSelector`, `HIDDEN_FILE_NAME`. Core file: `tests/test_poc_registry.py` (29 symbols). Documented purpose: Campaign command blacklist loaded from ``sessions/campaign_lessons.jsonl``.  A lesson with ``outcome == "failed"`` blacklists its command head under the lesson'.

## Files

### `modules/selection` (18 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/selection/__init__.py` | py | utility | 0 | yes |
| `modules/selection/_phase_categories.py` | py | utility | 1 | yes |
| `modules/selection/adversary.py` | py | utility | 6 | yes |
| `modules/selection/atomic.py` | py | utility | 2 | yes |
| `modules/selection/base.py` | py | utility | 4 | yes |
| `modules/selection/bridge.py` | py | utility | 2 | yes |
| `modules/selection/chain.py` | py | utility | 3 | yes |
| `modules/selection/cred_spray.py` | py | utility | 2 | yes |

### `tests` (14 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_chain_match_determinism.py` | py | testing | 13 | yes |
| `tests/test_chain_selector.py` | py | testing | 14 | yes |
| `tests/test_intel_selector.py` | py | testing | 16 | yes |
| `tests/test_loop_fire_pending.py` | py | testing | 14 | yes |
| `tests/test_poc_registry.py` | py | testing | 29 | yes |
| `tests/test_selection_bridge.py` | py | testing | 13 | yes |
| `tests/test_selection_lazyscript.py` | py | testing | 10 | yes |

### `modules` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/campaign_blacklist.py` | py | utility | 4 | yes |
| `modules/chain_match.py` | py | utility | 7 | yes |
| `modules/reverse-shell.c` | c | utility | 2 | no |

### `modules/rootkit` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/rootkit/rootkit.c` | c | utility | 13 | yes |

### `static/js` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/select2-4.1.0.min.js` | js | utility | 3 | yes |

*... and 17 more files in this community.*


## Key Symbols

- `_lessons_path` (function, `modules/campaign_blacklist.py:22`) `def _lessons_path()` - Return the lessons file path, resolved at call time for test isolation.
- `_load` (function, `modules/campaign_blacklist.py:27`) `def _load()` - Parse the lessons file into a context -> blacklisted command-head map.
- `campaign_blacklist` (function, `modules/campaign_blacklist.py:53`) `def campaign_blacklist()` - Return the cached blacklist, reloading when the lessons file changes.
- `blocked_commands` (function, `modules/campaign_blacklist.py:63`) `def blocked_commands(category)` - Return command heads blacklisted for a category plus the global ``any``.
- `normalize_tags` (function, `modules/chain_match.py:49`) `def normalize_tags(tags)` - Return a chain's tags lowercased and aliased to the shared vocabulary.
- `service_tokens` (function, `modules/chain_match.py:65`) `def service_tokens(services)` - Normalise discovered service names into the chain tag vocabulary.
- `platform_ok` (function, `modules/chain_match.py:75`) `def platform_ok(platforms, os_hint)` - Return True when a chain's platforms admit the target OS hint.
- `score` (function, `modules/chain_match.py:86`) `def score(tags, phase, svc_tokens)` - Score one chain's tags for the phase and discovered services.
- `reset_cache` (function, `modules/chain_match.py:101`) `def reset_cache()` - Clear the process-wide registry scan cache (tests, long-lived loops).
- `load_rows` (function, `modules/chain_match.py:109`) `def load_rows(allow_lab, ttl)` - Return enabled, valid, non-lab chain rows, cached for the TTL.
- `best_chain` (function, `modules/chain_match.py:139`) `def best_chain(phase, os_hint, services, exclude, allow_lab, rows, ttl)` - Return the ``(name, reason)`` of the best matching chain, or None.
- `reverse_shell_init` (function, `modules/reverse-shell.c:12`) `static int __init reverse_shell_init(void)` - call_usermodehelper function is used to create user mode processes from kernel space
- `reverse_shell_exit` (function, `modules/reverse-shell.c:16`) `static void __exit reverse_shell_exit(void)`
- `HIDDEN_PROCESS_NAME` (macro, `modules/rootkit/rootkit.c:30`) `#define HIDDEN_PROCESS_NAME`
- `HIDDEN_FILE_NAME` (macro, `modules/rootkit/rootkit.c:33`) `#define HIDDEN_FILE_NAME`
- `LISTENER_IP` (macro, `modules/rootkit/rootkit.c:36`) `#define LISTENER_IP`
- `LISTENER_PORT` (macro, `modules/rootkit/rootkit.c:39`) `#define LISTENER_PORT`
- `SPECIAL_STRING` (macro, `modules/rootkit/rootkit.c:42`) `#define SPECIAL_STRING`
- `SPECIAL_STRING_PORT` (macro, `modules/rootkit/rootkit.c:45`) `#define SPECIAL_STRING_PORT`
- `regs_override_return` (function, `modules/rootkit/rootkit.c:54`) `static inline void regs_override_return(struct pt_regs *regs, long new_ret)` - Define regs_override_return function
- `hooked_getdents` (function, `modules/rootkit/rootkit.c:86`) `static int hooked_getdents(struct kretprobe_instance *ri, struct pt_regs *regs)` - Hooked getdents function
- `hooked_getdents64` (function, `modules/rootkit/rootkit.c:112`) `static int hooked_getdents64(struct kretprobe_instance *ri, struct pt_regs *regs` - Hooked getdents64 function
- `hooked_read` (function, `modules/rootkit/rootkit.c:138`) `static int hooked_read(struct kretprobe_instance *ri, struct pt_regs *regs)` - Hooked read function to create a backdoor
- `disable_module_signature_verification` (function, `modules/rootkit/rootkit.c:192`) `static void disable_module_signature_verification(void)` - Function to disable module signature verification
- `hook_syscalls` (function, `modules/rootkit/rootkit.c:206`) `static int __init hook_syscalls(void)` - Function to hook system calls
- `unhook_syscalls` (function, `modules/rootkit/rootkit.c:219`) `static void __exit unhook_syscalls(void)` - Function to unhook system calls
- `categories_for` (function, `modules/selection/_phase_categories.py:23`) `def categories_for(phase)` - Return the lookup categories for a kill-chain phase.
- `load_profiles` (function, `modules/selection/adversary.py:26`) `def load_profiles(adversaries_dir)` - Load every adversary profile dictionary shipped in the repo.
- `_goal_tokens` (function, `modules/selection/adversary.py:75`) `def _goal_tokens(goal)` - Split the goal into comparable whole words (underscores kept).
- `resolve_profile` (function, `modules/selection/adversary.py:80`) `def resolve_profile(goal, adversaries_dir)` - Resolve the adversary profile the goal names, if any.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 94
- Cross-boundary resolved imports (EXTRACTED): 62

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- [cycle] `skills/lazyown_parquet_db.py` -> `modules/selection/parquet.py` -> `skills/lazyown_parquet_db.py`

## Open Questions

- Why do 2 file(s) lack file-level docs (e.g. `modules/reverse-shell.c`)? What purpose do they serve?
- Can the cycle `skills/lazyown_parquet_db.py` -> `modules/selection/parquet.py` be broken with an interface?
- What would break if the most connected file in modules/selection changed?
- Should modules/selection be split, given cohesion 0.66?

## Sources

- `modules/campaign_blacklist.py`
- `modules/chain_match.py`
- `modules/reverse-shell.c`
- `modules/rootkit/rootkit.c`
- `modules/selection/__init__.py`
- `modules/selection/_phase_categories.py`
- `modules/selection/adversary.py`
- `modules/selection/atomic.py`
- `modules/selection/base.py`
- `modules/selection/bridge.py`
- `modules/selection/chain.py`
- `modules/selection/cred_spray.py`
- `modules/selection/edb.py`
- `modules/selection/intel.py`
- `modules/selection/lazyscript.py`
- `modules/selection/module.py`
- `modules/selection/parquet.py`
- `modules/selection/playbook.py`
- `modules/selection/poc.py`
- `modules/selection/registry.py`
- *... and 17 more*
