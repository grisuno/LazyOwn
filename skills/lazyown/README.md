# skills/lazyown/

Hermes Agent skill definition for the LazyOwn RedTeam Framework.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Formal Hermes skill with frontmatter YAML + full operator playbook |
| `README.md` | This file |

## How it works

Hermes Agent loads `SKILL.md` when the skill is installed via:

```bash
hermes skills install /path/to/LazyOwn/skills/lazyown/SKILL.md
```

The skill provides:
- Campaign SITREP workflow (`lazyown_campaign_sitrep`)
- Command abstraction rules (never write raw flags)
- Kill-chain phase discipline (11 phases)
- Alias reference tables by phase
- Essential MCP tool catalogue
- Setup instructions for the MCP server

## Adding to the skill

1. Edit `SKILL.md` directly.
2. Keep frontmatter valid YAML.
3. Follow the style: concise tables, concrete examples, no prose where a table suffices.
4. Bump `version` in frontmatter on meaningful changes.
