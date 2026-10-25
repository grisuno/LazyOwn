# Recipe: Add a Function

1. Find the target file by purpose: `grep -in '<topic>' readmenator-agent/INDEX*.md`
2. Reuse before writing: `grep -in '<verb or noun>' readmenator-agent/SYMBOLS*.md`
3. Read the subsystem context: `cat readmenator-agent/KB_<subsystem>.md`
4. Check dependencies: `grep -n '<filename>' readmenator-agent/ARCHITECTURE*.md`
5. Edit the file
6. Regenerate: `readmenator .`

