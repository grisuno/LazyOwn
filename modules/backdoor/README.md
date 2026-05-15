# modules/backdoor

C source for the LazyOwn Linux backdoor module. Used in authorized post-exploitation
research and red team engagements to demonstrate persistence techniques on Linux
systems. For authorized use only.

## Files

| File | Description |
|------|-------------|
| `backdoor.c` | TCP reverse-shell backdoor. Connects to `lhost:lport`, spawns `/bin/sh`, and pipes stdin/stdout over the socket. Minimal footprint. |
| `server.c` | Multi-client listener that accepts incoming backdoor connections and multiplexes them into a simple operator console. |
| `keylogger.h` | Header defining the `ptrace`-based keylogging interface. Included by `backdoor.c` when compiled with `-DENABLE_KEYLOGGER`. |
| `Makefile` | Build rules. Targets: `all` (builds both binaries), `backdoor`, `server`, `clean`. |

## Building

```bash
cd modules/backdoor
make
# Outputs: backdoor, server
```

Cross-compile for a 32-bit Linux target:

```bash
make CC=i686-linux-gnu-gcc
```

## Usage from the CLI

The `do_backdoor` command in `lazyown.py` builds and stages the binary:

```
(LazyOwn) > backdoor
```

It reads `lhost` and `lport` from `payload.json`, patches them into the
source, compiles, strips, and copies the binary to `sessions/backdoor`.

## Operational notes

- The compiled binary has no dependencies beyond glibc. It runs on any
  Linux kernel 2.6.32 or later.
- Strip the binary before delivery: `strip sessions/backdoor`.
- The server binary listens on `lport`. Start it before delivering the backdoor.
- Do not compile with debug symbols in a real engagement.
