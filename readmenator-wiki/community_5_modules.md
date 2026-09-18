# modules

*Community 5 | 6 files | cohesion 0.83*

## Definition

This community groups 6 file(s) rooted at `modules` with dominant language py (cohesion 0.83). Central symbols: `DotNetPayloadConfig`, `DotNetPayloadFactory`, `LinuxAdvancedConfig`, `LinuxAdvancedPayloadFactory`, `MacOSPayloadConfig`, `MacOSPayloadFactory`, `MutationConfig`, `MutationResult`. Core file: `modules/polymorphic_engine.py` (19 symbols). Documented purpose: Payload arsenal commands — dotnet, reflective DLL, staged delivery, polymorphic, macOS/Linux payloads.  Provides: dotnet_payload          — Generate .NET/C# pay.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/payload_arsenal.py` | py | utility | 7 | yes |
| `modules/dotnet_payload.py` | py | utility | 12 | yes |
| `modules/linux_advanced_payloads.py` | py | utility | 17 | yes |
| `modules/macos_payloads.py` | py | utility | 16 | yes |
| `modules/polymorphic_engine.py` | py | utility | 19 | yes |
| `modules/staged_delivery.py` | py | utility | 18 | yes |

## Key Symbols

- `PayloadArsenalCommandSet` (class, `cli/commands/payload_arsenal.py:23`) `class PayloadArsenalCommandSet(LazyOwnCommandSet)` - Dotnet, reflective DLL, staged delivery, polymorphic, macOS/Linux advanced payloads.
- `do_dotnet_payload` (method, `cli/commands/payload_arsenal.py:29`) `def do_dotnet_payload(self, line)` - Generate a .NET/C# payload.
- `do_arsenal_show` (method, `cli/commands/payload_arsenal.py:114`) `def do_arsenal_show(self, line)` - Show payload arsenal items.
- `do_staged_delivery` (method, `cli/commands/payload_arsenal.py:172`) `def do_staged_delivery(self, line)` - Generate staged delivery artifacts (HTA, VBA, LNK, ISO, VHD).
- `do_polymorphic` (method, `cli/commands/payload_arsenal.py:261`) `def do_polymorphic(self, line)` - Apply polymorphic mutation to shellcode.
- `do_macos_payload` (method, `cli/commands/payload_arsenal.py:328`) `def do_macos_payload(self, line)` - Generate macOS payloads (.app bundles, persistence, TCC bypass).
- `do_linux_advanced_payload` (method, `cli/commands/payload_arsenal.py:401`) `def do_linux_advanced_payload(self, line)` - Generate advanced Linux payloads (LD_PRELOAD, eBPF, PAM, kernel module).
- `DotNetPayloadConfig` (class, `modules/dotnet_payload.py:298`) `class DotNetPayloadConfig` - Configuration for a .NET payload compilation.
- `DotNetPayloadFactory` (class, `modules/dotnet_payload.py:320`) `class DotNetPayloadFactory` - Generate, compile, and format .NET/C# payloads.
- `__init__` (method, `modules/dotnet_payload.py:332`) `def __init__(self, output_dir)`
- `_detect_compiler` (method, `modules/dotnet_payload.py:338`) `def _detect_compiler()`
- `list_templates` (method, `modules/dotnet_payload.py:369`) `def list_templates()` - Return available .NET payload template names.
- `_resolve_template` (method, `modules/dotnet_payload.py:373`) `def _resolve_template(self, config)`
- `generate_source` (method, `modules/dotnet_payload.py:394`) `def generate_source(self, config)` - Generate C# source code from a template.
- `compile` (method, `modules/dotnet_payload.py:408`) `def compile(self, config, source_code)` - Compile C# source to an assembly.
- `generate` (method, `modules/dotnet_payload.py:459`) `def generate(self, config)` - Generate a .NET payload — source code plus optional binary.
- `generate_powershell_reflective` (method, `modules/dotnet_payload.py:486`) `def generate_powershell_reflective(self, config)` - Generate a PowerShell script that reflectively loads a .NET assembly.
- `generate_inline_assembly` (method, `modules/dotnet_payload.py:505`) `def generate_inline_assembly(self, config)` - Generate self-decompiling inline .NET assembly load command.
- `to_format` (method, `modules/dotnet_payload.py:525`) `def to_format(self, data, fmt)` - Convert a payload result to the requested output format.
- `LinuxAdvancedConfig` (class, `modules/linux_advanced_payloads.py:64`) `class LinuxAdvancedConfig` - Configuration for advanced Linux payload generation.
- `LinuxAdvancedPayloadFactory` (class, `modules/linux_advanced_payloads.py:92`) `class LinuxAdvancedPayloadFactory` - Generate advanced Linux payloads for persistence, evasion, and escalation.
- `__init__` (method, `modules/linux_advanced_payloads.py:107`) `def __init__(self, config, output_dir)`
- `generate_ld_preload_rootkit` (method, `modules/linux_advanced_payloads.py:112`) `def generate_ld_preload_rootkit(self)` - Generate a C source file for an LD_PRELOAD rootkit.
- `generate_ebpf_payload` (method, `modules/linux_advanced_payloads.py:237`) `def generate_ebpf_payload(self)` - Generate an eBPF C program for network manipulation.
- `_ip_to_hex` (method, `modules/linux_advanced_payloads.py:307`) `def _ip_to_hex(ip_str)`
- `generate_pam_backdoor` (method, `modules/linux_advanced_payloads.py:313`) `def generate_pam_backdoor(self)` - Generate a PAM (Pluggable Authentication Module) backdoor.
- `generate_systemd_persistence` (method, `modules/linux_advanced_payloads.py:400`) `def generate_systemd_persistence(self)` - Generate systemd service and timer units for persistent callbacks.
- `generate_ssh_persistence` (method, `modules/linux_advanced_payloads.py:462`) `def generate_ssh_persistence(self)` - Generate an SSH persistence script for authorized_keys injection.
- `generate_kernel_module` (method, `modules/linux_advanced_payloads.py:523`) `def generate_kernel_module(self)` - Generate a Linux kernel module (LKM) rootkit.
- `generate_process_masquerade` (method, `modules/linux_advanced_payloads.py:636`) `def generate_process_masquerade(self)` - Generate a process masquerading script.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 8
- Cross-boundary resolved imports (EXTRACTED): 1

## Connections

- [EXTRACTED] depends_on community 5 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/payload_arsenal.py imports cli/commands/_base.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in modules changed?
- Should modules be split, given cohesion 0.83?

## Sources

- `cli/commands/payload_arsenal.py`
- `modules/dotnet_payload.py`
- `modules/linux_advanced_payloads.py`
- `modules/macos_payloads.py`
- `modules/polymorphic_engine.py`
- `modules/staged_delivery.py`
