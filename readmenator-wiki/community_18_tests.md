# tests

*Community 18 | 4 files | cohesion 1.00*

## Definition

This community groups 4 file(s) rooted at `tests` with dominant language py (cohesion 1.00). Central symbols: `backup_files`, `main`, `restore_files`, `run_all`, `run_tests`, `title`. Core file: `tests/mutation_common.py` (5 symbols). Documented purpose: Shared driver for curated mutation runners.  Provides backup/restore, the scoped pytest invocation and the standard report so each runner file only declares its.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/mutation_common.py` | py | testing | 5 | yes |
| `tests/run_mutation_loop_cli_catalog.py` | py | testing | 1 | yes |
| `tests/run_mutation_trigger_policy.py` | py | business_logic | 1 | yes |
| `tests/run_mutation_verb_catalog.py` | py | testing | 1 | yes |

## Key Symbols

- `backup_files` (function, `tests/mutation_common.py:20`) `def backup_files(mutations, base_dir)` - Snapshot original file contents.
- `restore_files` (function, `tests/mutation_common.py:30`) `def restore_files(backups, base_dir, mutations)` - Restore original file contents.
- `run_tests` (function, `tests/mutation_common.py:37`) `def run_tests(test_targets)` - Run the scoped suite and return True on success.
- `title` (function, `tests/mutation_common.py:49`) `def title(name)` - Print the runner banner.
- `run_all` (function, `tests/mutation_common.py:56`) `def run_all(mutations, test_targets)` - Execute baseline, every mutant and restore the source.
- `main` (function, `tests/run_mutation_loop_cli_catalog.py:50`) `def main()` - Execute baseline, every mutant and restore the source.
- `main` (function, `tests/run_mutation_trigger_policy.py:52`) `def main()` - Execute baseline, every mutant and restore the source.
- `main` (function, `tests/run_mutation_verb_catalog.py:52`) `def main()` - Execute baseline, every mutant and restore the source.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 3
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in tests changed?
- Should tests be split, given cohesion 1.00?

## Sources

- `tests/mutation_common.py`
- `tests/run_mutation_loop_cli_catalog.py`
- `tests/run_mutation_trigger_policy.py`
- `tests/run_mutation_verb_catalog.py`
