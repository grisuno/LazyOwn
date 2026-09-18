# scripts

*Community 17 | 3 files | cohesion 1.00*

## Definition

This community groups 3 file(s) rooted at `scripts` with dominant language py (cohesion 1.00). Central symbols: `FakeRunner`, `Journal`, `JournalConfig`, `JournalError`, `__call__`, `__init__`, `_build_parser`, `_default_runner`. Core file: `scripts/journal.py` (14 symbols). Documented purpose: Read-before-you-write journal over GitHub Discussions.  I keep a durable engineering journal in a GitHub Discussion category. Every unit of work appends one ent.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/journal.py` | py | utility | 14 | yes |
| `scripts/read_journal.py` | py | utility | 2 | yes |
| `tests/test_journal.py` | py | testing | 10 | yes |

## Key Symbols

- `JournalError` (class, `scripts/journal.py:48`) `class JournalError(RuntimeError)` - Raised when the GitHub API call fails or the category is missing.
- `JournalConfig` (class, `scripts/journal.py:53`) `class JournalConfig` - Configuration for the engineering journal.
- `from_git_remote` (method, `scripts/journal.py:71`) `def from_git_remote(cls, remote, category)` - Build a config from the ``origin`` remote of the current checkout.
- `_run_git` (method, `scripts/journal.py:90`) `def _run_git(args)` - Run a git command and return its standard output.
- `_git_remote_slug` (method, `scripts/journal.py:114`) `def _git_remote_slug()` - Return the ``owner/name`` slug of the ``origin`` remote.
- `_default_runner` (method, `scripts/journal.py:124`) `def _default_runner(args)` - Run ``gh`` with an argument list and return its standard output.
- `Journal` (class, `scripts/journal.py:149`) `class Journal` - GitHub Discussions backed journal.
- `_graphql` (method, `scripts/journal.py:163`) `def _graphql(self, query, variables)` - Run a GraphQL query through ``gh`` and return the ``data`` payload.
- `repo_id` (method, `scripts/journal.py:184`) `def repo_id(self)` - The GraphQL node id of the repository.
- `category_id` (method, `scripts/journal.py:192`) `def category_id(self)` - The GraphQL node id of the journal category.
- `post` (method, `scripts/journal.py:206`) `def post(self, title, body)` - Create a journal entry and return its number, url, and title.
- `entries` (method, `scripts/journal.py:223`) `def entries(self, limit)` - Return the most recently updated journal entries.
- `_build_parser` (method, `scripts/journal.py:245`) `def _build_parser()` - Build the command line parser.
- `main` (method, `scripts/journal.py:264`) `def main(argv)` - Run the journal CLI and return the process exit code.
- `_build_parser` (function, `scripts/read_journal.py:19`) `def _build_parser()` - Build the command line parser.
- `main` (function, `scripts/read_journal.py:29`) `def main(argv)` - Print the recent journal entries and return the process exit code.
- `FakeRunner` (class, `tests/test_journal.py:16`) `class FakeRunner` - Return canned GraphQL payloads keyed by a query fragment.
- `__init__` (method, `tests/test_journal.py:19`) `def __init__(self, responses)` - Store the responses keyed by a fragment of the query string.
- `__call__` (method, `tests/test_journal.py:24`) `def __call__(self, args)` - Record the call and return the matching payload as JSON.
- `_success_responses` (method, `tests/test_journal.py:34`) `def _success_responses()`
- `test_config_from_remote_slug` (method, `tests/test_journal.py:49`) `def test_config_from_remote_slug()` - A repository slug resolves without touching git.
- `test_config_rejects_bare_name` (method, `tests/test_journal.py:56`) `def test_config_rejects_bare_name()` - A slug without a separator is rejected.
- `test_post_entry_uses_resolved_ids` (method, `tests/test_journal.py:62`) `def test_post_entry_uses_resolved_ids()` - The create mutation receives the repository and category ids.
- `test_entries_returns_nodes` (method, `tests/test_journal.py:71`) `def test_entries_returns_nodes()` - Reading returns the discussion nodes.
- `test_missing_category_raises` (method, `tests/test_journal.py:79`) `def test_missing_category_raises()` - A category that is not present raises instead of silently posting.
- `test_graphql_errors_raise` (method, `tests/test_journal.py:91`) `def test_graphql_errors_raise()` - A GraphQL error payload raises a JournalError.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 2
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in scripts changed?
- Should scripts be split, given cohesion 1.00?

## Sources

- `scripts/journal.py`
- `scripts/read_journal.py`
- `tests/test_journal.py`
