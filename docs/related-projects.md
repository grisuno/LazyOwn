## Related Projects

LazyOwn ships as the "all-in-one" front of a small ecosystem of focused
red-team tools. Each project below stands on its own and can be wired into
LazyOwn through `lazyaddons/*.yaml`, the C2 implant pipeline, or the MCP
`lazyown_palette --info` view (which exposes the graphify-derived `calls`
and `related` neighbours of every command).

### Lightweight beacons (C / ASM)

Drop-in replacements for the bundled Go beacon when you need a smaller
footprint or per-architecture artefacts:

- **[beacon](https://github.com/grisuno/beacon)** — minimalist Windows beacon in C with BOF support via Early Bird APC injection and NT Native API calls. Pairs with LazyOwn's malleable C2 profile. Wired in via `lazyaddons/beacon.yaml`.
- **[blacksandbeacon](https://github.com/grisuno/blacksandbeacon)** — Linux-native beacon in C with first-class **Linux BOF (Beacon Object File)** support via ELF shared-object injection and direct syscalls. BOFs are loaded at runtime through a `dlopen` runtime — the same extensibility model as Windows BOF but targeting Linux kernel internals. **No commercial C2 framework (including Cobalt Strike) offers Linux BOF support.** Wired in via `lazyaddons/blacksandbeacon.yaml`; BOF loader via `lazyaddons/blacksandbeacon_bof.yaml`.
- **[blackzincbeacon](https://github.com/grisuno/blackzincbeacon)** — ARM build of the same family, for embedded / IoT engagements.

### Lightweight C2 frameworks

Alternative C2 surfaces that speak the same beacon protocol as `lazyc2.py`
or that can serve as a teamserver back-end:

- **[BlackObsidianC2](https://github.com/grisuno/BlackObsidianC2)** — small, fast Go C2 server intended as a stripped-down companion to `lazyc2.py`.
- **[LazyOwnBT](https://github.com/grisuno/LazyOwnBT)** — Bluetooth / proximity-aware C2 PoC; useful when the engagement scope explicitly covers RF.

### AI / orchestration

Drop into LazyOwn through MCP, the `toposwarm` lazyaddon, or directly:

- **[toposwarm](https://github.com/grisuno/toposwarm)** — natural-language router on top of the LazyOwn command catalogue; ships as both a lazyaddon and a Claude Code skill.
- **[LazyOwnOpenCodeAdapter](https://github.com/grisuno/LazyOwnOpenCodeAdapter)** — bridge between LazyOwn and OpenCode-style coding agents.

### Loaders, shellcode runners and post-exploitation

Used both by humans through pwntomate `.tool` files and by the autonomous
daemon when the reactive selector recommends an in-memory technique:

- **[gomulti_loader](https://github.com/grisuno/gomulti_loader)** — multi-platform Go shellcode loader (Linux + Windows). Wired in via `lazyaddons/gomulti_loader_linux.yaml` and `gomulti_loader_windows.yaml`.
- **[win_shellcode](https://github.com/grisuno/win_shellcode)** — collection of Windows shellcode templates ready to be linked from a beacon stub.
- **[ejecutarShellcode](https://github.com/grisuno/ejecutarShellcode)** — minimal "execute-this-shellcode" loaders for quick PoCs.
- **[ShellcodeFluctuation_crosscompile](https://github.com/grisuno/ShellcodeFluctuation_crosscompile)** — cross-compilable port of the ShellcodeFluctuation memory-encryption trick.
- **[LazyLoader](https://github.com/grisuno/LazyLoader)** — generic loader scaffold designed to be extended per engagement.
- **[OverRide](https://github.com/grisuno/OverRide)** — DLL hijack / DLL search-order-override toolkit for Windows persistence.
- **[ShadowLink](https://github.com/grisuno/ShadowLink)** — link-time / symbol-rewrite tooling for Linux ELF stagers.
- **[netsh_helper_dll](https://github.com/grisuno/netsh_helper_dll)** — `netsh` helper-DLL persistence template for Windows.

### Defensive bypass / instrumentation

- **[amsi](https://github.com/grisuno/amsi)** — AMSI bypass research and PoCs; invoked from LazyOwn payloads when AV/EDR is the limiting factor.

### Exploits and CVE PoCs

LazyOwn already vendors several recent kernel-class PoCs through the addon
system (`lazyaddons/copyfail.yaml`, `lazyaddons/dirtyfrag.yaml`,
`lazyaddons/CVE-2022-22077.yaml`, `lazyaddons/CVE_2025_24071_PoC.yaml`,
`lazyaddons/ebird3.yaml`). The original repositories are listed here for
auditability and citation:

- **[CVE-2022-22077](https://github.com/grisuno/CVE-2022-22077)** — RTCore64.sys arbitrary R/W IOCTL — used by the LazyOwn BYOVD chain.
- **[copy-fail-CVE-2026-31431](https://github.com/grisuno/copy-fail-CVE-2026-31431)** — next-gen Dirty Pipe variant. Backed by the `copyfail` lazyaddon.
- **[ebird3](https://github.com/grisuno/ebird3)** — Early-Bird APC injection + NT Native API loader; produces stealthy in-memory Windows payloads.

> **Want to add yours?** Drop a `lazyaddons/<name>.yaml` describing
> `repo_url`, `install_command` and `execute_command`; LazyOwn will pick it
> up automatically and surface it through the MCP `lazyown_palette` view.
