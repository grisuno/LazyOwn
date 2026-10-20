# Coding standards (enforced by review)

1. **English only.** Identifiers, strings, logs, docstrings. Translate Spanish remnants when you touch them.
2. **No comments.** Self-explanatory names + docstrings. Single-line note OK for non-obvious constraint or CVE ref.
3. **No emojis** in code/logs/docs unless operator asked. Banner ASCII art OK.
4. **Docstrings on every public function/class**:
   ```python
   def foo(bar: str) -> dict:
       """One-line summary.

       Args:
           bar: …
       Returns:
           …
       Raises:
           …
       """
   ```
5. **No magic numbers** — constants in `class Config` (shared) or `UPPER_SNAKE_CASE` module-level.
6. **No hardcoded paths/ports/IPs/wordlists/creds** — `payload.json` if reused, module constant if local.
7. **SOLID**:
   - **S**: one reason to change per class/fn.
   - **O**: extend via new addon/MCP tool/selector — don't edit hot paths.
   - **L**: new selector honours `BaseSelector.suggest()` contract.
   - **I**: small role-specific protocols (recon/exploit/cred/lateral/privesc).
   - **D**: orchestration depends on `LLMBackend`/`MemoryStore`/`Selector` abstractions, not Groq/ChromaDB directly.
8. **Consistency beats novelty** — when two patterns fit, pick the one already used.
9. **No partial implementations** — end-to-end (CLI ↔ payload.json ↔ MCP ↔ `sessions/` artefact) or not merged.
10. **No backwards-compat shims** for unshipped code — just change it.
11. **Every new directory gets a README** (see §2 rules). No exceptions.
12. **Boy-scout law (tech debt).** When a fix / refactor / new feature uncovers tech debt or a vulnerability that can be addressed **without breaking public surface or shipped behaviour**, address it in the same change and call it out in the PR body. Plan with `/graphify` first so the blast radius is understood — never refactor blindly. If the cleanup is unsafe within the change, open a follow-up task; do **not** silently leave the broken window.
13. **Smart consolidation (DRY+SOLID).** When two or more code paths duplicate logic (~10 LOC or one decision tree), consolidate into a single class/function honouring SOLID. Shared values go to `class Config` / `payload.json` if globally reused, module-level `UPPER_SNAKE_CASE` if local. Refactor must keep every existing call site working and ship with tests that pin behaviour **before** the move. No silent simplifications — feature parity is mandatory.
14. **Tests trend to 100%.** Every change ships with tests. If a touched module gains testable code, the change must raise coverage, not lower it. `pytest -q` must stay green. No `skip` / `xfail` without an issue link in the same PR.
15. **Docs follow code.** When a public surface (CLI verb, MCP tool, payload key, blueprint route, addon schema) is added or renamed, update the matching `docs/<topic>.md` and regenerate `COMMANDS.md` / `UTILS.md` via `python3 readmeneitor.py lazyown.py` and `python3 readmeneitor.py utils.py`. Missing or empty docstrings on new public API block merge. Extend `readmeneitor.py` itself when a new source file deserves auto-generated reference docs.
