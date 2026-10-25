# skills/awesome-windows-security/

Windows offensive router skill for the LazyOwn RedTeam framework.

Built from the ATT&CK-organised catalogue
[chryzsh/awesome-windows-security](https://github.com/chryzsh/awesome-windows-security).
The upstream repo is a reading list; this skill is the execution router —
objective → technique → the LazyOwn surface that runs it → evidence.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill definition with frontmatter YAML, routing tables and the operating contract |
| `hermes/SKILL.md` | Same body with Hermes frontmatter (version, author, license, platforms, metadata.hermes) |
| `README.md` | This file |

## What the skill does

1. Classifies the objective onto the upstream ATT&CK taxonomy and
   normalises the legacy technique IDs (T1208 → T1558.003, T1081 →
   T1552.001, T1171 → T1557.001, ...).
2. Routes it through one of four paths:
   - **Route A — native**: LazyOwn already ships the command (preferred).
   - **Route B — addon**: the upstream tool is not in LazyOwn yet, so it is
     wrapped with `/lazyaddon-creator`.
   - **Route C — atomic**: the technique has an Atomic Red Team test —
     translated to concrete GUIDs, artefacts generated, executed against an
     in-scope target.
   - **Route D — chain**: full adversary emulation through `apt_chain` or
     the autonomous loop.
3. States the preconditions (scope, credentials file, Windows agent path,
   platform flag, elevation).
4. Records the result as a finding (`lazy_finding`, `share_finding`,
   `db_creds`) and cleans the target (`atomic_clean`).

## How it works

Hermes Agent loads `SKILL.md` when the skill is installed via:

```bash
hermes skills install /path/to/LazyOwn/skills/awesome-windows-security/SKILL.md
```

## Adding to the skill

1. Edit `SKILL.md` directly, then regenerate the Hermes copy:

   ```bash
   python3 - <<'EOF'
   from pathlib import Path
   src = Path('skills/awesome-windows-security/SKILL.md').read_text()
   body = src.split('---\n', 2)[2].lstrip('\n')
   front = Path('skills/awesome-windows-security/hermes/SKILL.md').read_text().split('---\n', 2)[1]
   Path('skills/awesome-windows-security/hermes/SKILL.md').write_text(f"---\n{front}---\n\n{body}")
   EOF
   ```

2. Keep frontmatter valid YAML.
3. Follow the style: tables over prose, concrete commands, no invented flags.
4. Bump `version` in the Hermes frontmatter on meaningful changes.
5. Every command cited in the router table must exist in
   `cli/command_index.json` or be a shipped lazyaddon.
