# Recipe: Fix a Dependency Cycle

Target cycle: `modules/atomic_exploit_bridge.py` -> `modules/lazy_intel.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/autonomous_exploit_engine.py` -> `modules/atomic_exploit_bridge.py`

1. Read the imports between these files: `grep -n '^import\|^from\|#include' modules/atomic_exploit_bridge.py`, `grep -n '^import\|^from\|#include' modules/lazy_intel.py`, `grep -n '^import\|^from\|#include' modules/lazy_loop.py`, `grep -n '^import\|^from\|#include' modules/loop_ai_bridge.py`, `grep -n '^import\|^from\|#include' skills/hive_mind.py`, `grep -n '^import\|^from\|#include' skills/lazyown_groq_agents.py`, `grep -n '^import\|^from\|#include' skills/lazyown_mcp.py`, `grep -n '^import\|^from\|#include' modules/autonomous_exploit_engine.py`
2. Move the shared symbols into a new leaf module both sides import
3. Verify: `readmenator . && grep -c 'Dependency Cycles' readmenator-agent/GOTCHAS.md`
