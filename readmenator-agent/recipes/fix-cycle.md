# Recipe: Fix a Dependency Cycle

Target cycle: `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/lazy_loop.py`

1. Read the imports between these files: `grep -n '^import\|^from\|#include' modules/lazy_loop.py`, `grep -n '^import\|^from\|#include' modules/loop_triggers.py`, `grep -n '^import\|^from\|#include' modules/trigger_policy.py`, `grep -n '^import\|^from\|#include' modules/orchestrator_config.py`, `grep -n '^import\|^from\|#include' modules/auto_registry.py`, `grep -n '^import\|^from\|#include' modules/lazy_orchestrator_feedback.py`, `grep -n '^import\|^from\|#include' modules/lazy_intel.py`
2. Move the shared symbols into a new leaf module both sides import
3. Verify: `readmenator . && grep -c 'Dependency Cycles' readmenator-agent/GOTCHAS.md`
