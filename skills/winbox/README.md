# WinBox Lab Skill

Agent skill for the WinBox isolated Windows vulnerability-research lab
integrated into LazyOwn (`scenario: winbox`).

- Skill definition: [SKILL.md](SKILL.md)
- Module: `modules/winbox_gym.py` (catalogue + CLI adapter)
- CommandSet: `cli/commands/winbox_gym.py` (`winbox` shell command)
- Gym catalogue: `playbooks/gym_winbox.yaml`, `exploits/winbox_*.yaml`,
  `chains/gym_winbox_*.yaml`, `gyms/winbox_*.yaml`
- MCP: `lazyown_winbox_*` tools in `skills/lazyown_mcp.py`

Upstream platform: https://github.com/totekuh/winbox (MIT).
