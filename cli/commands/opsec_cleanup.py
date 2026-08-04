"""OPSEC and cleanup commands — scoring, log tamper, forensic cleaner, timestomp, memory, network.

Provides:
    opsec_score             — Real-time OPSEC risk assessment with action gating (v2)
    log_tamper              — Cross-platform log clearing (Windows/Linux/macOS)
    forensic_clean          — Remove forensic artifacts (Prefetch, Shimcache, Amcache, etc.)
    timestomp               — Manipulate file MACB timestamps
    memory_clean            — Clear memory artifacts (tickets, clipboard, env, credentials)
    network_opsec           — Proxy chains, DoH, canary detection, traffic analysis
    auditd_disable          — Disable Linux auditd
    sysmon_disable          — Disable Windows Sysmon
"""

from __future__ import annotations

import cmd2

from cli.commands._base import LazyOwnCommandSet


class OpsecCleanupCommandSet(LazyOwnCommandSet):
    """OPSEC scoring, log tampering, forensic cleaning, timestomping, memory/network OPSEC."""

    phase = "evasion"
    category = "09. OPSEC & Cleanup"

    def do_opsec_score(self, line: str) -> None:
        """Real-time OPSEC risk assessment with contextual action gating (v2).

Usage: opsec_score <command> [--phase <phase>] [--env <environment>] [--edr] [--siem] [--priv]

Performs context-aware OPSEC scoring considering:
    - Kill-chain phase
    - Target environment type (enterprise, smb, government, cloud, critical_infrastructure)
    - EDR/SIEM presence
    - Privilege level
    - Evasion status
    - Artifact count and session duration

Returns risk level, noise score, detection surface, gate action (ALLOW/WARN/CONFIRM/BLOCK),
and ranked mitigations.

Examples:
    opsec_score mimikatz --phase credential_access --env enterprise --edr --siem
    opsec_score secretsdump --phase credential_access --env government
    opsec_score nmap --phase scanning
    opsec_score psexec --env enterprise --edr
"""
        from modules.opsec_scorer_v2 import OpsecScorerV2, OpsecContext

        if not line.strip():
            self._cmd.perror("Usage: opsec_score <command> [options]")
            return

        args = line.strip().split()
        command = args[0]

        context = OpsecContext()
        for i, a in enumerate(args[1:]):
            if a == "--phase" and i + 2 < len(args):
                context.killchain_phase = args[i + 2]
            elif a == "--env" and i + 2 < len(args):
                context.target_environment = args[i + 2]
            elif a == "--edr":
                context.edr_detected = True
            elif a == "--siem":
                context.siem_detected = True
            elif a == "--priv":
                context.is_privileged = True

        scorer = OpsecScorerV2(context=context)
        assessment = scorer.assess(command)

        risk_colors = {"LOW": "green", "MEDIUM": "yellow", "HIGH": "orange", "CRITICAL": "red"}
        risk_color = risk_colors.get(assessment.risk_label, "white")

        self._cmd.poutput(f"\n[ OPSEC Assessment: {command} ]")
        self._cmd.poutput(f"    Noise Score     : {assessment.noise_score}/10")
        self._cmd.poutput(f"    Risk Level      : {assessment.risk_label}")
        self._cmd.poutput(f"    Gate Action     : {assessment.gate_action.name}")
        self._cmd.poutput(f"    Detection       : {', '.join(assessment.detection_surface) if assessment.detection_surface else 'none'}")
        self._cmd.poutput(f"    Explanation     : {assessment.explanation}")

        if assessment.mitigations:
            self._cmd.poutput(f"\n    Mitigations:")
            for m in assessment.mitigations[:5]:
                self._cmd.poutput(f"        - {m}")

        if assessment.alternative_commands:
            self._cmd.poutput(f"\n    Alternatives:")
            for alt in assessment.alternative_commands[:3]:
                self._cmd.poutput(f"        - {alt}")

        trend = scorer.get_trend()
        self._cmd.poutput(f"\n    Session Trend   : {trend['trend']} (avg noise {trend.get('recent_avg_noise', '?')})")

    def do_log_tamper(self, line: str) -> None:
        """Cross-platform log clearing commands.

Usage: log_tamper <platform> [--no-eventlog-suspend] [--no-verify]

Platforms: windows, linux, macos, all

Windows: 13 Event Logs + EventLog service suspend + Sysmon
Linux: journald, auth.log, wtmp/btmp, shell history, auditd
macOS: unified log, system.log, TCC.db, diagnostic reports

Examples:
    log_tamper windows
    log_tamper linux
    log_tamper all
"""
        from modules.log_tamper import LogTamper, LogTamperConfig

        if not line.strip():
            self._cmd.perror("Usage: log_tamper <windows|linux|macos|all>")
            return

        platform = line.strip().split()[0].lower()

        config = LogTamperConfig(target_platform=platform)
        tamper = LogTamper(config=config)

        if platform == "all":
            all_cmds = tamper.generate_all()
            for plat, data in all_cmds.items():
                cmds = data.get(f"{plat}_commands", data.get("powershell_commands", data.get("bash_commands", data.get("zsh_commands", []))))
                self._cmd.poutput(f"\n--- {plat.upper()} Log Tampering ({len(cmds)} commands) ---")
                for cmd in cmds[:10]:
                    self._cmd.poutput(f"    {cmd}")
            return

        result = tamper.generate_all().get(platform, {})

        cmds_key = f"{platform}_commands"
        if platform == "windows":
            cmds_key = "powershell_commands"
        elif platform == "linux":
            cmds_key = "bash_commands"

        cmds = result.get(cmds_key, result.get("powershell_commands", result.get("bash_commands", result.get("zsh_commands", result.get("commands", [])))))

        self._cmd.poutput(f"\n[ Log Tampering — {platform.upper()} ]")
        for cmd in cmds[:15]:
            self._cmd.poutput(f"    {cmd}")

        verification = result.get("verification", [])
        if verification:
            self._cmd.poutput(f"\n[ Verification ]")
            for cmd in verification:
                self._cmd.poutput(f"    {cmd}")

    def do_forensic_clean(self, line: str) -> None:
        """Clean forensic artifacts — Prefetch, Shimcache, Amcache, Jump Lists, etc.

Usage: forensic_clean <platform> [--no-prefetch] [--no-amcache] [--mft]

Platforms: windows, linux, macos, all

Windows cleans: Prefetch, Shimcache, Amcache, Jump Lists, Recent files,
                Shellbags, LNK files, MRU registry, thumbnail cache, USN journal, MFT.

Examples:
    forensic_clean windows
    forensic_clean windows --mft
    forensic_clean all
"""
        from modules.forensic_cleaner import ForensicCleaner, ForensicCleanerConfig

        if not line.strip():
            self._cmd.perror("Usage: forensic_clean <windows|linux|macos|all>")
            return

        platform = line.strip().split()[0].lower()
        config = ForensicCleanerConfig(target_platform=platform)
        cleaner = ForensicCleaner(config=config)

        if platform == "windows":
            result = cleaner.windows_cleanup()
            cmds = result.get("cleanup_commands", {})
            self._cmd.poutput(f"\n[ Forensic Cleaner — WINDOWS ]")
            for category, commands in cmds.items():
                self._cmd.poutput(f"\n    [{category}]")
                for cmd in commands[:3]:
                    self._cmd.poutput(f"        {cmd}")
        elif platform == "linux":
            result = cleaner.linux_cleanup()
            self._cmd.poutput(f"\n[ Forensic Cleaner — LINUX ]")
            for cmd in result["commands"][:10]:
                self._cmd.poutput(f"    {cmd}")
        elif platform == "macos":
            result = cleaner.macos_cleanup()
            self._cmd.poutput(f"\n[ Forensic Cleaner — MACOS ]")
            for cmd in result["commands"][:8]:
                self._cmd.poutput(f"    {cmd}")
        elif platform == "all":
            for p in ["windows", "linux", "macos"]:
                config.target_platform = p
                c = ForensicCleaner(config=config)
                if p == "windows":
                    result = c.windows_cleanup()
                    self._cmd.poutput(f"\n--- WINDOWS ({len(result['cleanup_commands'])} categories) ---")
                elif p == "linux":
                    result = c.linux_cleanup()
                    self._cmd.poutput(f"\n--- LINUX ({len(result['commands'])} commands) ---")
                elif p == "macos":
                    result = c.macos_cleanup()
                    self._cmd.poutput(f"\n--- MACOS ({len(result['commands'])} commands) ---")

    def do_timestomp(self, line: str) -> None:
        """Manipulate file MACB timestamps to evade forensic timeline analysis.

Usage: timestomp <target_path> [--ref <reference_file>] [--platform <windows|linux|macos>] [--randomize]

Clones timestamps from a legitimate system file onto target files.
Supports batch directory timestomping and randomized timestamp windows.

Examples:
    timestomp /tmp/beacon.exe --platform windows
    timestomp /tmp/staged/ --ref /etc/passwd --platform linux
    timestomp ~/Library/LaunchAgents/backdoor.plist --platform macos --randomize
"""
        from modules.timestomper import Timestomper, TimestompConfig

        if not line.strip():
            self._cmd.perror("Usage: timestomp <target_path> [--ref <ref>] [--platform <os>]")
            return

        args = line.strip().split()
        target = args[0]
        platform = "linux"
        reference = ""
        randomize = False

        for i, a in enumerate(args[1:]):
            if a == "--platform" and i + 2 < len(args):
                platform = args[i + 2]
            elif a == "--ref" and i + 2 < len(args):
                reference = args[i + 2]
            elif a == "--randomize":
                randomize = True

        config = TimestompConfig(
            target_platform=platform,
            reference_path=reference,
            target_paths=[target],
        )
        stomper = Timestomper(config=config)

        if platform == "windows":
            result = stomper.windows_timestomp_powershell()
            self._cmd.poutput(f"\n[ Timestomp — WINDOWS ]")
            self._cmd.poutput(f"    Reference: {result['reference_file']}")
            for cmd in result["commands"][:8]:
                if cmd.strip():
                    self._cmd.poutput(f"    {cmd}")
        elif platform == "linux":
            result = stomper.linux_timestomp_commands()
            self._cmd.poutput(f"\n[ Timestomp — LINUX ]")
            self._cmd.poutput(f"    Reference: {result['reference_file']}")
            for cmd in result["commands"][:8]:
                if cmd.strip():
                    self._cmd.poutput(f"    {cmd}")
        elif platform == "macos":
            result = stomper.macos_timestomp_commands()
            self._cmd.poutput(f"\n[ Timestomp — MACOS ]")
            self._cmd.poutput(f"    Reference: {result['reference_file']}")
            for cmd in result["commands"][:8]:
                if cmd.strip():
                    self._cmd.poutput(f"    {cmd}")

        if randomize:
            ts = stomper.generate_random_timestamps(1609459200.0, 7)
            self._cmd.poutput(f"\n    Randomized timestamps (7-day window):")
            self._cmd.poutput(f"        Created:  {ts['created']}")
            self._cmd.poutput(f"        Modified: {ts['modified']}")
            self._cmd.poutput(f"        Accessed: {ts['accessed']}")

    def do_memory_clean(self, line: str) -> None:
        """Clean memory artifacts — Kerberos tickets, clipboard, env vars, credentials.

Usage: memory_clean <platform> [--no-tickets] [--no-clipboard]

Platforms: windows, linux, macos, all

Windows: Kerberos purge, NTLM cache, clipboard, env vars, PSReadline, DPAPI
Linux: env vars, GNOME keyring, ssh-agent, clipboard (xclip), kdestroy
macOS: Keychain, pasteboard, ssh-agent, kdestroy, env scrub

Examples:
    memory_clean windows
    memory_clean all
"""
        from modules.memory_cleaner import MemoryCleaner, MemoryCleanerConfig

        if not line.strip():
            self._cmd.perror("Usage: memory_clean <windows|linux|macos|all>")
            return

        platform = line.strip().split()[0].lower()
        config = MemoryCleanerConfig(target_platform=platform)
        cleaner = MemoryCleaner(config=config)

        if platform == "windows":
            result = cleaner.windows_memory_cleanup()
            cmds = result["cleanup_commands"]
        elif platform == "linux":
            result = cleaner.linux_memory_cleanup()
            cmds = result["cleanup_commands"]
        elif platform == "macos":
            result = cleaner.macos_memory_cleanup()
            cmds = result["cleanup_commands"]
        else:
            self._cmd.poutput(f"\n[ Memory Cleanup — ALL PLATFORMS ]")
            for p in ["windows", "linux", "macos"]:
                config.target_platform = p
                c = MemoryCleaner(config=config)
                if p == "windows":
                    r = c.windows_memory_cleanup()
                elif p == "linux":
                    r = c.linux_memory_cleanup()
                else:
                    r = c.macos_memory_cleanup()
                self._cmd.poutput(f"\n    [{p}] ({len(r['cleanup_commands'])} commands)")
                for cmd in r["cleanup_commands"][:4]:
                    self._cmd.poutput(f"        {cmd}")
            return

        self._cmd.poutput(f"\n[ Memory Cleanup — {platform.upper()} ]")
        for cmd in cmds[:10]:
            self._cmd.poutput(f"    {cmd}")

    def do_network_opsec(self, line: str) -> None:
        """Network OPSEC — proxy chains, DoH, canary detection, traffic analysis.

Usage: network_opsec <method> [options]

Methods:
    proxy_chain  — Configure proxy chain (socks5, http, ssh tunnels)
    doh          — DNS-over-HTTPS configuration
    port_rand    — Source port randomization
    jitter       — Connection jitter schedule generation
    canary_check — Detect canary tokens and honeypots
    traffic      — Analyze TLS inspection and proxy detection

Examples:
    network_opsec proxy_chain --type socks5_over_ssh
    network_opsec doh
    network_opsec canary_check --domains target.local,admin.target.local
    network_opsec traffic --host target.com --port 443
"""
        from modules.network_opsec import NetworkOpsecEngine, NetworkOpsecConfig

        if not line.strip():
            self._cmd.output(f"\n[ Network OPSEC Methods ]")
            for m in ["proxy_chain", "doh", "port_rand", "jitter", "canary_check", "traffic"]:
                self._cmd.poutput(f"    {m}")
            self._cmd.poutput(f"\nUsage: network_opsec <method> [options]")
            return

        args = line.strip().split()
        method = args[0].lower()
        config = NetworkOpsecConfig()
        engine = NetworkOpsecEngine(config=config)

        if method == "proxy_chain":
            chain_type = "single_socks5"
            for i, a in enumerate(args[1:]):
                if a == "--type" and i + 2 < len(args):
                    chain_type = args[i + 2]
            result = engine.configure_proxy_chain(chain_type)
            self._cmd.poutput(f"\n[ Proxy Chain: {chain_type} ]")
            self._cmd.poutput(f"    Proxies:")
            for p in result["proxies"]:
                self._cmd.poutput(f"        {p}")
            self._cmd.poutput(f"\n    Export commands:")
            for cmd in result.get("export_commands", []):
                self._cmd.poutput(f"        $ {cmd}")

        elif method == "doh":
            result = engine.dns_over_https_config()
            self._cmd.poutput(f"\n[ DNS-over-HTTPS ]")
            self._cmd.poutput(f"    Provider: {result['provider']}")
            self._cmd.poutput(f"\n    Fallback providers:")
            for f in result.get("fallback_providers", []):
                self._cmd.poutput(f"        {f}")

        elif method == "port_rand":
            result = engine.source_port_randomize()
            self._cmd.poutput(f"\n[ Source Port Randomization ]")
            self._cmd.poutput(f"    Range: {config.source_port_range}")
            self._cmd.poutput(f"    Python example: {result['python_socket_example'][:150]}...")

        elif method == "jitter":
            schedule = engine.connection_jitter_schedule(60)
            self._cmd.poutput(f"\n[ Connection Jitter Schedule ]")
            self._cmd.poutput(f"    Jitter: {config.connection_jitter_ms}ms")
            self._cmd.poutput(f"    Schedule (seconds): {schedule}")

        elif method == "canary_check":
            domains = []
            for i, a in enumerate(args[1:]):
                if a == "--domains" and i + 2 < len(args):
                    domains = args[i + 2].split(",")
            config.canary_domains = domains
            result = engine.check_canary_tokens()
            self._cmd.poutput(f"\n[ Canary Token Detection ]")
            self._cmd.poutput(f"    Tokens detected: {result['canary_tokens_detected']}")
            self._cmd.poutput(f"    Risk action    : {result['risk_action']}")
            self._cmd.poutput(f"    Recommendation : {result['recommendation']}")
            for f in result.get("findings", []):
                self._cmd.poutput(f"        [{f['confidence']}] {f['type']}: {f.get('domain', f.get('url', ''))}")

        elif method == "traffic":
            host = "target.com"
            port = 443
            for i, a in enumerate(args[1:]):
                if a == "--host" and i + 2 < len(args):
                    host = args[i + 2]
                elif a == "--port" and i + 2 < len(args):
                    port = int(args[i + 2])
            result = engine.analyze_traffic_with_canary_check(host, port)
            self._cmd.poutput(f"\n[ Traffic Analysis: {host}:{port} ]")
            self._cmd.poutput(f"    TLS Inspected     : {result['tls_inspected']}")
            self._cmd.poutput(f"    Proxy Detected    : {result['proxy_detected']}")
            cert_info = result.get('certificate_info', {})
            if cert_info:
                self._cmd.poutput(f"    Certificate Issuer: {cert_info.get('issuer', {}).get('commonName', 'N/A')}")
            if result.get("recommendations"):
                for r in result["recommendations"]:
                    self._cmd.poutput(f"    RECOMMENDATION: {r}")

        else:
            self._cmd.perror(f"Unknown method: {method}")

    def do_auditd_disable(self, line: str) -> None:
        """Generate commands to disable Linux auditd.

Usage: auditd_disable [--restore]
"""
        from modules.log_tamper import LogTamper

        tamper = LogTamper()
        result = tamper.auditd_disable_commands()

        if "--restore" in line:
            self._cmd.poutput(f"\n[ Auditd — RESTORE ]")
            for cmd in result.get("restore", []):
                self._cmd.poutput(f"    {cmd}")
        else:
            self._cmd.poutput(f"\n[ Auditd — DISABLE ]")
            self._cmd.poutput(f"\n    Service control:")
            for cmd in result.get("service_control", []):
                self._cmd.poutput(f"        $ {cmd}")
            self._cmd.poutput(f"\n    Rule removal:")
            for cmd in result.get("rule_removal", []):
                self._cmd.poutput(f"        $ {cmd}")

    def do_sysmon_disable(self, line: str) -> None:
        """Generate commands to disable Windows Sysmon.

Usage: sysmon_disable [--restore]
"""
        from modules.log_tamper import LogTamper

        tamper = LogTamper()
        result = tamper.sysmon_disable_commands()

        if "--restore" in line:
            self._cmd.poutput(f"\n[ Sysmon — RESTORE ]")
            for cmd in result.get("restore", []):
                self._cmd.poutput(f"    {cmd}")
        else:
            self._cmd.poutput(f"\n[ Sysmon — DISABLE ]")
            self._cmd.poutput(f"\n    Service control:")
            for cmd in result.get("service_control", []):
                self._cmd.poutput(f"        $ {cmd}")
            self._cmd.poutput(f"\n    Registry disable:")
            for cmd in result.get("registry_disable", []):
                self._cmd.poutput(f"        $ {cmd}")
