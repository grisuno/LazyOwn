# Recipe: Reduce File Complexity

1. Read hotspots: `grep -A5 'Hotspots' readmenator-agent/GOTCHAS.md`
2. Pick the worst offender
3. Extract functions/classes into new files in the same subsystem
4. Update imports
5. Regenerate: `readmenator .`

