# Recipe: Fix a Security Finding

1. Read findings: `grep -n '<file>' readmenator-agent/SECURITY.md`
2. Check API contract: `grep -A10 '<function>' readmenator-agent/API.md`
3. Apply fix
4. Verify: `readmenator . --audit && grep -c 'CRITICAL\|HIGH' readmenator-agent/SECURITY.md`

