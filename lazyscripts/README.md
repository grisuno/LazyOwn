# lazyscripts

LazyOwn script files (`.ls` extension). Small recipes that chain multiple
CLI commands together and are loaded with `run_script <name>`. Think of them
as engagement playbooks written in the LazyOwn command language rather than
bash.

## How to run a script

```
(LazyOwn) > run_script lazyscripts/lazynmap.ls
(LazyOwn) > run_script lazyscripts/smb.ls
```

Or pass the name without the directory prefix if the shell can resolve it:

```
(LazyOwn) > run_script lazynmap
```

## Available scripts

| File | What it does |
|------|-------------|
| `lazynmap.ls` | Full port scan followed by service version detection and NSE vuln scripts. |
| `smb.ls` | SMB enumeration chain: `enum4linux`, `crackmapexec`, `smbclient` listing. |
| `adversary.ls` | MITRE ATT&CK adversary emulation sequence for the current target OS. |
| `atomic_agent.ls` | Runs an Atomic Red Team test sequence against a Linux target. |
| `atomic_agent_win.ls` | Same for Windows targets. |
| `certipy_ad.ls` | Active Directory certificate services enumeration and ESC attack chain. |
| `dploot.ls` | DPAPI secret extraction sequence (credentials, browser data, certificates). |
| `lazyquit.ls` | Clean shutdown sequence: saves session, exports report, closes listeners. |
| `lazyscript.ls` | Template script — copy this to start a new recipe. |
| `pyautomate.ls` | Python-driven automation helper for targets with restricted shell access. |
| `startup.ls` | First-run script: sets defaults, pings the target, runs a quick scan. |

## Writing a script

Each line is a LazyOwn CLI command, executed in order. Comments start with
`#`. Parameters are read from `payload.json` at execution time — no
substitution syntax needed in the script itself.

```
# Example: quick web enumeration recipe
gobuster
ffuf
nikto
```

Scripts run synchronously. If a command fails, execution continues unless the
command calls `exit`. Long-running commands (`lazynmap`, `pwntomate`) detach
and return immediately.

## Naming convention

- Use lowercase with underscores.
- Name the script after what it accomplishes, not the tools it uses.
  `smb_enum.ls` is better than `enum4linux_crackmapexec.ls`.
