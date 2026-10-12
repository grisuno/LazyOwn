# `.claude/skills/run-lazyown/driver.sh`

> Source: [.claude/skills/run-lazyown/driver.sh:1](../../.claude/skills/run-lazyown/driver.sh#L1) | language `sh` | coverage 100.0% | [API index](../index.md)

Build and drive LazyOwn inside its Docker sandbox (Debian container).

LazyOwn is a Linux-targeted cmd2 shell; it does not run natively on a non-Linux host (Linux venv paths, shells out to `ip a`, Linux-only deps). The sandbox image is the supported way to launch it anywhere Docker runs. This driver builds the image and drives the shell through its headless runner, which exits with a status code and emits one JSON object per command instead of entering the interactive loop.  Usage, from the repo root: bash .claude/skills/run-lazyown/driver.sh                # smoke test bash .claude/skills/run-lazyown/driver.sh "help"         # one command bash .claude/skills/run-lazyown/driver.sh "a; b; c"      # command chain  Exit code mirrors the headless runner: 0 = all commands OK.
