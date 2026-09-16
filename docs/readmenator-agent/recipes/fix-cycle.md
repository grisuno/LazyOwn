# Recipe: Fix a Dependency Cycle

1. Read cycles: `grep -A5 'Dependency Cycles' readmenator-agent/GOTCHAS.md`
2. Pick the cycle to break
3. Introduce an interface/abstraction to decouple
4. Verify: `readmenator . && grep -c 'cycle' readmenator-agent/GOTCHAS.md`

