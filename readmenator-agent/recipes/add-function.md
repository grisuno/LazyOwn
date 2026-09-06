# Recipe: Add a Function

1. Find the target file: `grep -rn 'TODO\|FIXME' readmenator-agent/INDEX.md`
2. Read the subsystem context: `cat readmenator-agent/KB_<subsystem>.md`
3. Check dependencies: `grep -n '<filename>' readmenator-agent/ARCHITECTURE.md`
4. Edit the file
5. Regenerate: `readmenator .`

