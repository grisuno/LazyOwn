# Porting Windows BOFs to Linux

LazyOwn ships the only open-source C2 beacon with first-class Beacon Object
File support for Linux targets. This document explains how to port an
existing Windows BOF to Linux and how to run it through BlackSandBeacon.

Audience: operators and tool authors comfortable with C, the Windows BOF
contract, and Linux internals (syscalls, ELF, `/proc`, `dlopen`).

---

## What is a Linux BOF in LazyOwn

A Linux BOF is a position-independent ELF shared object (`.so`) loaded into
the running BlackSandBeacon process via `dlopen` and invoked through a
function pointer obtained with `dlsym`. The BOF runs in the beacon's
address space, can read and write the beacon's memory, and returns output
to the operator through the same `datap` callback API used by Windows BOFs.

It is not a separate process. It is not written to disk on the target
after delivery (the loader stages it in memory). It cannot be reused after
the beacon exits because the mapping disappears with the process.

Compare this with the Windows BOF model:

| Aspect | Windows BOF | LazyOwn Linux BOF |
|---|---|---|
| Object format | COFF | ELF shared object |
| Loader | Cobalt Strike / Sliver COFF loader | `dlopen` against PIC `.so` |
| Resolution | Custom COFF symbol resolver | Standard `dlsym` |
| API contract | `datap` + `BeaconPrintf` + `BeaconOutput` | Same names, same signatures |
| Entry point | `go(char *args, int alen)` | `go(char *args, int alen)` |
| Build flags | `cl /c` or MinGW `-c` | `gcc -shared -fPIC -nostartfiles` |

Because the `datap` API is preserved, the porting effort is concentrated
in (a) replacing Win32 calls and (b) updating includes and types.

---

## Minimum viable Linux BOF

`beacon.h` is shipped by the BlackSandBeacon SDK at
`external/.exploit/blacksandbeacon/include/beacon.h` after the
`blacksandbeacon` addon clones and builds the runtime. Include it from
that path or copy it next to your BOF source.

```c
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include "beacon.h"

void go(char *args, int alen) {
    datap parser;
    BeaconDataParse(&parser, args, alen);
    int interval = BeaconDataInt(&parser);
    BeaconPrintf(0x00, "linux bof received interval=%d uid=%d", interval, getuid());
}
```

Build:

```
gcc -shared -fPIC -nostartfiles -o sample.so sample.c
```

Stage and deliver:

```
cp sample.so sessions/sample.so
blacksandbeacon_bof sessions/sample.so
```

The loader delivers `sample.so` to a live beacon, the beacon resolves
`go` via `dlsym`, calls it, and pipes any `BeaconPrintf` output back over
the C2 channel.

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

These functions are exported by the BlackSandBeacon runtime and resolved
by the dynamic linker at load time. Source-compatible with Windows BOF.

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

1. Compile the BOF as a PIC shared object:
   ```
   gcc -shared -fPIC -nostartfiles -O2 -o mybof.so mybof.c
   ```
   The `-nostartfiles` flag avoids pulling `crt1.o` into the BOF.
2. Strip it to remove debug symbols that would help defenders:
   ```
   strip --strip-unneeded mybof.so
   ```
3. Stage to LazyOwn's sessions directory:
   ```
   cp mybof.so sessions/mybof.so
   ```
4. Push it to an active beacon:
   ```
   blacksandbeacon_bof sessions/mybof.so
   ```

   The addon reads `lhost` and `lport` from `payload.json`, fetches the
   loader if needed, and instructs the beacon to `dlopen` the BOF and
   invoke `go`.

---

## Pitfalls

- **Forgetting `-fPIC`.** Without position-independent code the loader
  cannot relocate the BOF and `dlopen` returns null. The beacon logs the
  `dlerror` string back to the operator.
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
  `sessions/mybof-x86_64.so` and `sessions/mybof-aarch64.so`.
- **Using thread-local storage.** TLS in dynamically loaded `.so` files
  has historical glibc bugs. Avoid `__thread` unless you have tested it
  against the libc on the target.

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

1. Adds the source to the BlackSandBeacon repository under `bofs/<name>/`.
2. Adds a `lazyaddons/<name>_bof.yaml` entry to LazyOwn that wires up
   compile + stage + deliver.
3. Adds a row to `docs/ATTACK_MATRIX.md` if it covers a new technique.
4. Includes a short test note: which kernel, which distro, which beacon
   build you tested against.

We do not accept BOFs whose only purpose is destruction (wiping disks,
disabling logging permanently) — see the impact section of
`docs/ATTACK_MATRIX.md`.
