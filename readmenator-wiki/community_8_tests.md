# tests

*Community 8 | 3 files | cohesion 0.50*

## Definition

This community groups 3 file(s) rooted at `tests` with dominant language py (cohesion 0.50). Central symbols: `CommandAllowlist`, `CommandDecision`, `CommandRejectionReason`, `TestAuditLog`, `TestBasicAllow`, `TestCaseInsensitive`, `TestEmptyInput`, `TestShellMetachars`. Core file: `tests/test_command_allowlist.py` (14 symbols). Documented purpose: Command allowlist policy for the LazyOwn C2 ``/api/run`` endpoint.  Contract: this module gates arbitrary command execution so only commands whose first whitesp.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/command_allowlist.py` | py | utility | 8 | yes |
| `tests/test_command_allowlist.py` | py | testing | 14 | yes |
| `tests/test_command_allowlist_behavior.py` | py | testing | 3 | yes |

## Key Symbols

- `CommandRejectionReason` (class, `lazyc2/security/command_allowlist.py:36`) `class CommandRejectionReason(StrEnum)` - Why a command was rejected by :class:`CommandAllowlist`.
- `CommandDecision` (class, `lazyc2/security/command_allowlist.py:48`) `class CommandDecision` - The outcome of a single command allowlist check.
- `to_dict` (method, `lazyc2/security/command_allowlist.py:61`) `def to_dict(self)` - Return a JSON-serializable dict for the audit log.
- `CommandAllowlist` (class, `lazyc2/security/command_allowlist.py:70`) `class CommandAllowlist` - Allowlist gate for the ``/api/run`` endpoint.
- `__init__` (method, `lazyc2/security/command_allowlist.py:82`) `def __init__(self, allowed, audit_log_path)`
- `allowed` (method, `lazyc2/security/command_allowlist.py:94`) `def allowed(self)` - Return the immutable set of allowed first tokens (lowercased).
- `check` (method, `lazyc2/security/command_allowlist.py:98`) `def check(self, command)` - Return the :class:`CommandDecision` for ``command``.
- `_audit` (method, `lazyc2/security/command_allowlist.py:126`) `def _audit(self, decision, command)`
- `TestBasicAllow` (class, `tests/test_command_allowlist.py:29`) `class TestBasicAllow` - Verify the happy path.
- `test_known_command_is_allowed` (method, `tests/test_command_allowlist.py:32`) `def test_known_command_is_allowed(self)`
- `test_unknown_command_is_denied` (method, `tests/test_command_allowlist.py:38`) `def test_unknown_command_is_denied(self)`
- `TestShellMetachars` (class, `tests/test_command_allowlist.py:45`) `class TestShellMetachars` - Verify that metacharacters always result in rejection.
- `test_metachar_rejected` (method, `tests/test_command_allowlist.py:60`) `def test_metachar_rejected(self, payload)`
- `TestEmptyInput` (class, `tests/test_command_allowlist.py:70`) `class TestEmptyInput` - Verify edge cases on the input shape.
- `test_empty_string_rejected` (method, `tests/test_command_allowlist.py:73`) `def test_empty_string_rejected(self)`
- `test_whitespace_only_rejected` (method, `tests/test_command_allowlist.py:79`) `def test_whitespace_only_rejected(self)`
- `test_non_string_rejected` (method, `tests/test_command_allowlist.py:85`) `def test_non_string_rejected(self)`
- `TestCaseInsensitive` (class, `tests/test_command_allowlist.py:92`) `class TestCaseInsensitive` - Verify case-insensitive matching.
- `test_uppercase_token_matches` (method, `tests/test_command_allowlist.py:95`) `def test_uppercase_token_matches(self)`
- `TestAuditLog` (class, `tests/test_command_allowlist.py:101`) `class TestAuditLog` - Verify the audit log is written line-by-line JSON.
- `test_audit_log_appends_jsonl` (method, `tests/test_command_allowlist.py:104`) `def test_audit_log_appends_jsonl(self, tmp_path)`
- `test_audit_log_disabled_is_noop` (method, `tests/test_command_allowlist.py:116`) `def test_audit_log_disabled_is_noop(self, tmp_path)`
- `test_given_allowlisted_ping_when_checked_then_allowed` (function, `tests/test_command_allowlist_behavior.py:11`) `def test_given_allowlisted_ping_when_checked_then_allowed()` - Given a whitelisted first token, the gate allows the command.
- `test_given_rm_when_checked_then_denied` (function, `tests/test_command_allowlist_behavior.py:18`) `def test_given_rm_when_checked_then_denied()` - Given a non-allowlisted verb, the gate denies.
- `test_given_injection_when_checked_then_denied` (function, `tests/test_command_allowlist_behavior.py:26`) `def test_given_injection_when_checked_then_denied(tmp_path)` - Given a metachar injection, the gate denies and the attempt is audited.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 2
- Cross-boundary resolved imports (EXTRACTED): 2

## Connections

- [EXTRACTED] depends_on community 8 <-> 1 (strength 0.9): Extracted import edge crosses communities: lazyc2/security/command_allowlist.py imports cli/commands/enum.py.
- [EXTRACTED] depends_on community 4 <-> 8 (strength 0.9): Extracted import edge crosses communities: lazyc2.py imports lazyc2/security/command_allowlist.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in tests changed?
- Should tests be split, given cohesion 0.50?

## Sources

- `lazyc2/security/command_allowlist.py`
- `tests/test_command_allowlist.py`
- `tests/test_command_allowlist_behavior.py`
