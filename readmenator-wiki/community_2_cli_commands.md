# cli/commands

*Community 2 | 3 files | cohesion 0.50*

## Definition

This community groups 3 file(s) rooted at `cli/commands` with dominant language py (cohesion 0.50). Central symbols: `AddonHotReloader`, `AliasResolver`, `AuditCommandSet`, `CommandInfo`, `CommandLister`, `CompletionResult`, `DictPayloadProvider`, `DynamicAliasResolver`. Core file: `cli/cli_enhancements.py` (69 symbols). Documented purpose: CLI enhancement primitives for the LazyOwn interactive shell.  This module exposes SOLID, framework-agnostic building blocks used by the ``cli/commands/audit.py.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/cli_enhancements.py` | py | utility | 69 | yes |
| `cli/commands/audit.py` | py | infrastructure | 13 | yes |
| `tests/test_cli_enhancements.py` | py | testing | 50 | yes |

## Key Symbols

- `PayloadProvider` (class, `cli/cli_enhancements.py:40`) `class PayloadProvider(Protocol)` - Read-only view onto ``payload.json`` style configuration.
- `get` (method, `cli/cli_enhancements.py:43`) `def get(self, key, default)`
- `keys` (method, `cli/cli_enhancements.py:44`) `def keys(self)`
- `CommandLister` (class, `cli/cli_enhancements.py:47`) `class CommandLister(Protocol)` - Source of command metadata for indexing / fuzzy matching.
- `commands` (method, `cli/cli_enhancements.py:50`) `def commands(self)`
- `TerminalIO` (class, `cli/cli_enhancements.py:53`) `class TerminalIO(Protocol)` - Minimal duck-typed prompt/print pair so tests can fake it.
- `prompt` (method, `cli/cli_enhancements.py:56`) `def prompt(self, message, default)`
- `emit` (method, `cli/cli_enhancements.py:57`) `def emit(self, line)`
- `CommandInfo` (class, `cli/cli_enhancements.py:61`) `class CommandInfo` - Lightweight description of a shell command.
- `FuzzyMatch` (class, `cli/cli_enhancements.py:75`) `class FuzzyMatch` - A scored fuzzy match against a CommandInfo.
- `FuzzyCommandIndex` (class, `cli/cli_enhancements.py:83`) `class FuzzyCommandIndex` - Search a command catalogue with token-aware fuzzy matching.
- `__init__` (method, `cli/cli_enhancements.py:91`) `def __init__(self, source)`
- `search` (method, `cli/cli_enhancements.py:94`) `def search(self, query, limit)` - Return the top ``limit`` matches ordered by descending score.
- `_score` (method, `cli/cli_enhancements.py:109`) `def _score(info, q)`
- `CompletionResult` (class, `cli/cli_enhancements.py:138`) `class CompletionResult` - A single tab-completion suggestion.
- `PayloadAwareCompleter` (class, `cli/cli_enhancements.py:145`) `class PayloadAwareCompleter` - Suggest values from ``payload.json`` for context-sensitive arguments.
- `__init__` (method, `cli/cli_enhancements.py:164`) `def __init__(self, payload, addon_lister, plugin_lister, credential_lister)`
- `complete` (method, `cli/cli_enhancements.py:176`) `def complete(self, command, partial)` - Return suggestions for ``partial`` given the leading ``command``.
- `_suggest_payload_keys` (method, `cli/cli_enhancements.py:196`) `def _suggest_payload_keys(self, partial)`
- `_suggest_targets` (method, `cli/cli_enhancements.py:202`) `def _suggest_targets(self, partial)`
- `_suggest_wordlist_keys` (method, `cli/cli_enhancements.py:213`) `def _suggest_wordlist_keys(self, partial)`
- `_suggest_addons` (method, `cli/cli_enhancements.py:221`) `def _suggest_addons(self, partial)`
- `_suggest_plugins` (method, `cli/cli_enhancements.py:224`) `def _suggest_plugins(self, partial)`
- `_suggest_credentials` (method, `cli/cli_enhancements.py:227`) `def _suggest_credentials(self, partial)`
- `AliasResolver` (class, `cli/cli_enhancements.py:234`) `class AliasResolver(ABC)` - Resolves alias templates into executable command strings.
- `expand` (method, `cli/cli_enhancements.py:238`) `def expand(self, alias_name, raw_template, payload)` - Return the alias rendered against the current payload.
- `DynamicAliasResolver` (class, `cli/cli_enhancements.py:242`) `class DynamicAliasResolver(AliasResolver)` - Resolve placeholders at execution time, not at shell load.
- `expand` (method, `cli/cli_enhancements.py:255`) `def expand(self, alias_name, raw_template, payload)`
- `_sub` (method, `cli/cli_enhancements.py:256`) `def _sub(m)`
- `HotReloader` (class, `cli/cli_enhancements.py:270`) `class HotReloader(ABC)` - Notify subscribers when a watched directory changes.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 6
- Cross-boundary resolved imports (EXTRACTED): 5

## Connections

- [EXTRACTED] depends_on community 2 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/audit.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 1 <-> 2 (strength 0.9): Extracted import edge crosses communities: lazyown.py imports cli/cli_enhancements.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in cli/commands changed?
- Should cli/commands be split, given cohesion 0.50?

## Sources

- `cli/cli_enhancements.py`
- `cli/commands/audit.py`
- `tests/test_cli_enhancements.py`
