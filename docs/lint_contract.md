# Lint contract archive

I keep the current lint contract in `CLAUDE.md` and the historical record
here. The contract is short on purpose: `ruff check .` passes with zero
errors, `ruff format --check` passes on every file the change touches, and
each lint fix ships with one mutation probe that must die.

The scope decision dates from 2026-09-09. Generated mutmut output under
`mutants/` stays excluded through `extend-exclude` in `pyproject.toml`.
`ruff format --check .` still fails on roughly 400 legacy files that this
work did not touch. Only touched files must be format clean. I do not
reformat `lazyc2.py`, a 7415-line god class, so the diff stays minimal.

## Methodology gate

The order of operations is mandatory for every lint fix.

1. SDD. Inventory the findings with `ruff check . --output-format concise`
   and classify them as auto-fixable (I001, F401, W292, UP) or manual
   (F821, E402, syntax).
2. TDD. Record the baseline before editing: the `pytest` result and the
   `ruff` count. Pre-existing failures stay pre-existing. New failures
   block the change.
3. BDD. Validate after editing: `ruff check .` returns zero, `pytest`
   matches baseline, a behavioral spot-check of each rewritten module
   passes, and one mutation probe dies.
4. Boy scout. Every touched file also gets English only, docstrings on
   public symbols, no comments, no emojis, a centralized config class with
   no magic numbers and no hardcoded paths, dead code removed, no
   `sys.stdout` redirection, and `subprocess` in list form with timeouts.

## Bugs closed in the 2026-09-09 pass

All F821 findings were real runtime faults.

- `modules/morse.py`. The file did not parse because of an indentation
  syntax error across the `__main__` driver. I rewrote it to contract:
  `MorseConfig`, `text_to_morse`, `morse_to_text`, `run_driver`, a
  snake_case API, and the legacy `textToMorse`, `morseToText`,
  `reverseMorseCode` aliases kept.
- `modules/bot.py`. `Path` was undefined at runtime, identifiers were in
  Spanish, and `open('output.txt', 'w')` hijacked `sys.stdout`. I rewrote
  it as `BotConfig`, `find_new_repos`, `render_repos`, `format_output`,
  `main`, kept the `buscar_repos_nuevos` alias, and added UTF-8 writes and
  a request timeout.
- `modules/command_executor.py`. `sys` was undefined in the streaming
  loop. Fixed with a top-level `import sys`.
- `slack_c2_bot.py`. `config` was used three lines before assignment,
  which raised `NameError` on import. I moved `Config(load_payload())`
  above its first use.
- `poc_tui/app.py`. `except Exception as e` leaked into a `lambda` that
  ran on another thread after `e` was deleted. I bound the message as a
  default argument.
- `lazyc2.py`. E402, `import hmac` sat below module code. Moved to the top
  imports.

## Validation record 2026-09-09

`ruff check .` returned all checks passed. `pytest` on hardening v1, v3,
v4, v5 and killchain_unified_v2 reported 179 passed and 8 failed. The
eight failures were identical to the baseline: missing `flask_login` and
`textual` in the environment, plus ICMP and crypto expectation drift. None
related to the change. The mutation probe on the `text_to_morse`
separator died.

## Boy-scout pass 2026-09-12

I restored the broken contract. The `hardening` commit had left five
findings in `modules/legacy/` and `modules/playbook_engine.py`, and two
`ruff format` targets had drifted. The fixes are import ordering in
`lazyarpspoofing.py` and `lazyhoneypot.py`, removal of an unused `os`
import in `lazymidm.py`, removal of an unused `subprocess` import in
`playbook_engine.py`, and formatting in `cli/assign.py`,
`cli/commands/ai.py`, `scripts/sync_doc_stats.py`, and
`scripts/top_tier_check.py`. `cli/command_index.json` was stale and is now
regenerated from the 741 commands on disk.
