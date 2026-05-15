# modules/win_rootkit

Windows ring-3 rootkit research code for authorized red team engagements and
security research. Ring-3 means all code runs in user space — no kernel driver
required, making it easier to deploy but also easier for defenders to detect
with kernel-level visibility tools. For authorized use only.

## Files

| File | Description |
|------|-------------|
| `mrhyde.c` | C implementation. Uses DLL injection and API hooking (`NtQueryDirectoryFile`, `NtQuerySystemInformation`) to hide files and processes from user-space enumeration tools. |
| `win_ring3_rootkit.c` | Alternative C implementation with focus on network socket hiding via Winsock2 hook. |
| `win_ring3_rootkit.cpp` | C++ variant with RAII resource management and exception safety. |
| `win_ring3_rootkit.cs` | C# implementation. Deployed as a managed assembly via reflection loading. Useful when native code execution is blocked but .NET is available. |
| `backup.c` | Minimal backup/restore utility for hooked API functions. Included by the other modules to uninstall hooks cleanly. |

## Building

Cross-compile from Linux:

```bash
# C version (x64)
x86_64-w64-mingw32-gcc -shared -o win_ring3_rootkit.dll win_ring3_rootkit.c

# C++ version
x86_64-w64-mingw32-g++ -shared -o win_ring3_rootkit.dll win_ring3_rootkit.cpp

# C# version (requires Mono or Windows .NET SDK)
mcs -target:library -out:win_ring3_rootkit.dll win_ring3_rootkit.cs
```

## Deployment

The compiled DLL is injected into a target process using the LazyOwn
`do_inject` command or the `GoPEInjection` lazyaddon:

```
(LazyOwn) > inject sessions/win_ring3_rootkit.dll
```

## Detection notes

Ring-3 hooks are visible to:
- Kernel-level EDR agents (CrowdStrike, SentinelOne)
- `Process Hacker` / `Process Monitor` with kernel access
- ETW-based detection

Use in combination with AMSI bypass and ETW patching for better OpSec.
