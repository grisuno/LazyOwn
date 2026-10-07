# Recipe: Change a File Safely

Riskiest file: `core/logging.py` (123 dependents)

1. Who depends on it: `grep -n -- '-> `<file>`' readmenator-agent/ARCHITECTURE*.md`
2. Its public surface: `grep -n '`<file>:' readmenator-agent/API*.md`
3. Known risks: `grep -n '<file>' readmenator-agent/GOTCHAS.md readmenator-agent/SECURITY.md`
4. Keep signatures stable or update every importer found in step 1
5. Regenerate: `readmenator .`
