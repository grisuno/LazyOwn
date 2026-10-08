# Recipe: Fix a Dependency Cycle

Target cycle: `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`

1. Read the imports between these files: `grep -n '^import\|^from\|#include' utils.py`, `grep -n '^import\|^from\|#include' skills/claude_md_orchestrator/parser.py`, `grep -n '^import\|^from\|#include' skills/claude_md_orchestrator/models.py`, `grep -n '^import\|^from\|#include' cli/commands/enum.py`, `grep -n '^import\|^from\|#include' cli/commands/_base.py`
2. Move the shared symbols into a new leaf module both sides import
3. Verify: `readmenator . && grep -c 'Dependency Cycles' readmenator-agent/GOTCHAS.md`
