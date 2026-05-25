# Color Theme Module

ANSI color and terminal formatting helpers used by the CLI and C2 dashboard.

## Contents

| File | Purpose |
|------|---------|
| `colors.py` | Color constants, gradient generators and terminal-capability detection. |

## Design

All color output in LazyOwn should import from this module instead of hard-coding ANSI escape sequences. This ensures consistent theming and supports terminals with limited color support.
