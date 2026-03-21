"""
modules/lazyown_bridge.py
==========================
Full-coverage structured catalog of all LazyOwn do_ commands mapped to
attack phases, MITRE ATT&CK tactics, and discovered service types.

Integrates with the MCP auto_loop to provide phase-aware, service-matched
command selection without modifying lazyown.py.

Design (SOLID)
--------------
- Single Responsibility : CommandCatalog owns only the command registry;
                          PhaseSelector owns only phase-to-command resolution;
                          ServiceMatcher owns only service-type detection;
                          ContextEnricher owns only arg substitution.
- Open/Closed           : add new phases/tactics via CatalogEntry, no edits needed.
- Liskov                : all Selector subclasses honour Optional[CatalogEntry] contract.
- Interface Segregation : BridgeDispatcher exposes only what auto_loop needs.
- Dependency Inversion  : BridgeDispatcher depends on AbstractSelector abstraction.

Phases
------
recon       -> 01. Reconnaissance
enum        -> 02. Scanning & Enumeration
exploit     -> 03. Exploitation
postexp     -> 04. Post-Exploitation
persist     -> 05. Persistence
privesc     -> 06. Privilege Escalation
cred        -> 07. Credential Access
lateral     -> 08. Lateral Movement
exfil       -> 09. Data Exfiltration
c2          -> 10. Command & Control
report      -> 11. Reporting
"""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------

@dataclass
class CatalogEntry:
    """A single LazyOwn command with metadata for intelligent selection."""
    command: str
    phase: str
    mitre_tactic: str
    services: List[str] = field(default_factory=list)
    requires_creds: bool = False
    requires_port: bool = False
    description: str = ""
    priority: int = 5
    arg_template: str = ""
    os_target: str = "any"  # "linux", "windows", "any"
    tags: List[str] = field(default_factory=list)  # e.g. ["ad", "kerberos", "web"]

    def build_command(
        self,
        target: str = "",
        port: str = "",
        user: str = "",
        password: str = "",
        domain: str = "",
        url: str = "",
        wordlist: str = "",
        lhost: str = "",
        lport: str = "",
    ) -> str:
        """Return 'command [args]' with known values substituted."""
        args = self.arg_template
        subs = {
            "{target}": target,
            "{port}": port,
            "{user}": user,
            "{password}": password,
            "{domain}": domain,
            "{url}": url or (f"http://{target}" if target else ""),
            "{wordlist}": wordlist or "/usr/share/wordlists/rockyou.txt",
            "{lhost}": lhost,
            "{lport}": lport or "4444",
        }
        for placeholder, value in subs.items():
            if value:
                args = args.replace(placeholder, value)
        args = re.sub(r"\{[^}]+\}", "", args).strip()
        return f"{self.command} {args}".strip() if args else self.command

    def matches_service(self, services: List[str]) -> bool:
        if not self.services:
            return True
        for svc in services:
            svc_lower = svc.lower()
            for required in self.services:
                if required.lower() in svc_lower or svc_lower in required.lower():
                    return True
        return False

    def matches_os(self, os_hint: str) -> bool:
        if self.os_target == "any":
            return True
        return self.os_target.lower() == os_hint.lower()


# ---------------------------------------------------------------------------
# Catalog
# ---------------------------------------------------------------------------

class CommandCatalog:
    """Full registry of CatalogEntry objects for all LazyOwn phases."""

    def __init__(self) -> None:
        self._entries: List[CatalogEntry] = []
        self._populate()

    def _populate(self) -> None:
        add = self._entries.append

        # ====================================================================
        # 01. RECONNAISSANCE
        # ====================================================================
        add(CatalogEntry("lazynmap", "recon", "T1046",
            description="Full TCP/UDP nmap scan with service version detection",
            priority=1, tags=["network"]))
        add(CatalogEntry("batchnmap", "recon", "T1046",
            description="Batch nmap scan covering common ports quickly",
            priority=2, tags=["network"]))
        add(CatalogEntry("recon", "recon", "T1595",
            description="Full passive + active recon runner (built-in LazyOwn module)",
            priority=1, tags=["network", "osint"]))
        add(CatalogEntry("serveralive2", "recon", "T1018",
            description="ICMP-based host discovery across subnet",
            priority=3, tags=["network"]))
        add(CatalogEntry("arpscan", "recon", "T1018",
            description="ARP scan for live hosts on local network",
            priority=3, tags=["network"]))
        add(CatalogEntry("ping", "recon", "T1018",
            description="ICMP ping to check host reachability",
            priority=5, arg_template="{target}"))
        add(CatalogEntry("ports", "recon", "T1046",
            description="Quick port check using built-in port scanner",
            priority=4, arg_template="{target}"))
        add(CatalogEntry("trace", "recon", "T1040",
            description="Traceroute for network path mapping",
            priority=6, arg_template="{target}"))
        add(CatalogEntry("dig", "recon", "T1590",
            description="DNS query for A/MX/NS/TXT records",
            priority=4, tags=["dns"]))
        add(CatalogEntry("dnsenum", "recon", "T1590",
            description="DNS enumeration and subdomain brute-force",
            priority=2, arg_template="{domain}", tags=["dns"]))
        add(CatalogEntry("dnsmap", "recon", "T1590",
            description="DNS map — subdomain enumeration via dictionary",
            priority=3, arg_template="{domain}", tags=["dns"]))
        add(CatalogEntry("dnstool_py", "recon", "T1590",
            description="Python DNS tool for advanced record querying",
            priority=5, tags=["dns"]))
        add(CatalogEntry("dnschef", "recon", "T1557",
            description="DNS server for spoofing/MITM analysis",
            priority=7, tags=["dns", "mitm"]))
        add(CatalogEntry("finalrecon", "recon", "T1595",
            services=["http", "https"],
            description="Passive web OSINT: WHOIS, headers, SSL, links",
            priority=3, tags=["web", "osint"]))
        add(CatalogEntry("whatweb", "recon", "T1518",
            services=["http", "https"],
            description="Web technology fingerprinting",
            priority=3, arg_template="{url}", tags=["web"]))
        add(CatalogEntry("sslscan", "recon", "T1590",
            services=["https", "443"],
            description="SSL/TLS cipher and certificate analysis",
            priority=4, arg_template="{target}", tags=["ssl"]))
        add(CatalogEntry("openssl_sclient", "recon", "T1590",
            services=["https", "443", "tls"],
            description="Manual SSL inspection with openssl s_client",
            priority=6, arg_template="{target}", tags=["ssl"]))
        add(CatalogEntry("ipinfo", "recon", "T1590",
            description="IP geolocation and ASN lookup via ipinfo.io",
            priority=6, arg_template="{target}", tags=["osint"]))
        add(CatalogEntry("sherlock", "recon", "T1593",
            description="Username OSINT across social networks",
            priority=7, tags=["osint", "social"]))
        add(CatalogEntry("waybackmachine", "recon", "T1593",
            services=["http", "https"],
            description="Historical URL harvesting from Wayback Machine",
            priority=5, arg_template="{domain}", tags=["web", "osint"]))
        add(CatalogEntry("gospider", "recon", "T1595",
            services=["http", "https"],
            description="Web spider for endpoint and link discovery",
            priority=4, arg_template="-s {url}", tags=["web"]))
        add(CatalogEntry("httprobe", "recon", "T1595",
            description="Probe list of domains for live HTTP/HTTPS",
            priority=5, tags=["web"]))
        add(CatalogEntry("metabigor", "recon", "T1596",
            description="OSINT tool: ASN, IP ranges, certs",
            priority=6, tags=["osint"]))
        add(CatalogEntry("cve", "recon", "T1588",
            description="Search CVE via CIRCL API for target service versions",
            priority=5, arg_template="{target}", tags=["vuln"]))
        add(CatalogEntry("graudit", "recon", "T1587",
            description="Static code analysis for hardcoded secrets/vulns",
            priority=7, tags=["code"]))
        add(CatalogEntry("trufflehog", "recon", "T1552",
            description="Secret/credential hunting in git history",
            priority=6, tags=["osint", "secrets"]))
        add(CatalogEntry("tcpdump_capture", "recon", "T1040",
            description="Packet capture on local interface",
            priority=6, tags=["network", "passive"]))
        add(CatalogEntry("tcpdump_icmp", "recon", "T1040",
            description="Capture ICMP traffic for host discovery",
            priority=7, tags=["network", "passive"]))
        add(CatalogEntry("tshark_analyze", "recon", "T1040",
            description="Network traffic analysis with tshark",
            priority=7, tags=["network", "passive"]))
        add(CatalogEntry("binarycheck", "recon", "T1518",
            description="Check SUID/SGID binaries on target system",
            priority=4, os_target="linux", tags=["privesc-recon"]))
        add(CatalogEntry("getcap", "recon", "T1518",
            description="Enumerate Linux capabilities on binaries",
            priority=4, os_target="linux", tags=["privesc-recon"]))
        add(CatalogEntry("apache_users", "recon", "T1592",
            services=["http", "https"],
            description="Enumerate Apache mod_userdir usernames",
            priority=6, tags=["web"]))
        add(CatalogEntry("windapsearchscrapeusers", "recon", "T1087",
            services=["ldap", "389"],
            description="Scrape users via LDAP windapsearch with no creds",
            priority=3, tags=["ad", "ldap"]))
        add(CatalogEntry("launchpad", "recon", "T1593",
            description="Search Launchpad for user accounts",
            priority=8, tags=["osint"]))
        add(CatalogEntry("proxy", "recon", "T1090",
            description="Configure HTTP proxy for traffic inspection",
            priority=8, tags=["network"]))

        # ====================================================================
        # 02. SCANNING & ENUMERATION
        # ====================================================================
        add(CatalogEntry("gobuster", "enum", "T1083",
            services=["http", "https"],
            description="Directory and vhost brute-force",
            priority=1, requires_port=True,
            arg_template="dir -u http://{target}:{port}", tags=["web"]))
        add(CatalogEntry("feroxbuster", "enum", "T1083",
            services=["http", "https"],
            description="Recursive directory brute-force (fast, recursive)",
            priority=1, requires_port=True,
            arg_template="-u http://{target}:{port}", tags=["web"]))
        add(CatalogEntry("dirsearch", "enum", "T1083",
            services=["http", "https"],
            description="Web path enumeration with extensions",
            priority=2, arg_template="-u http://{target}", tags=["web"]))
        add(CatalogEntry("wfuzz", "enum", "T1083",
            services=["http", "https"],
            description="Multi-purpose web fuzzer (params, paths, headers)",
            priority=3, tags=["web"]))
        add(CatalogEntry("nikto", "enum", "T1595",
            services=["http", "https"],
            description="Web server vulnerability scanner",
            priority=2, arg_template="-h {target}", tags=["web"]))
        add(CatalogEntry("nuclei", "enum", "T1595",
            services=["http", "https"],
            description="Template-based vulnerability scanner (thousands of templates)",
            priority=1, arg_template="-u {url}", tags=["web", "vuln"]))
        add(CatalogEntry("wpscan", "enum", "T1595",
            services=["http", "https"],
            description="WordPress vulnerability scanner",
            priority=2, arg_template="--url {url}", tags=["web", "cms"]))
        add(CatalogEntry("skipfish", "enum", "T1595",
            services=["http", "https"],
            description="Skipfish active web application scan",
            priority=5, arg_template="-o /tmp/skipfish {url}", tags=["web"]))
        add(CatalogEntry("arjun", "enum", "T1592",
            services=["http", "https"],
            description="HTTP parameter discovery tool",
            priority=4, arg_template="-u {url}", tags=["web"]))
        add(CatalogEntry("parth", "enum", "T1592",
            services=["http", "https"],
            description="Gather known parameters from open-source datasets",
            priority=5, tags=["web"]))
        add(CatalogEntry("parsero", "enum", "T1592",
            services=["http", "https"],
            description="robots.txt analysis for disallowed paths",
            priority=6, tags=["web"]))
        add(CatalogEntry("loxs", "enum", "T1059",
            services=["http", "https"],
            description="XSS/SQLI/LFI/SSTI multi-scanner",
            priority=3, tags=["web", "vuln"]))
        add(CatalogEntry("blazy", "enum", "T1110",
            services=["http", "https"],
            description="Multi-protocol brute-forcer (HTTP basic/form/proxy)",
            priority=4, requires_port=True, tags=["web", "bruteforce"]))
        add(CatalogEntry("changeme", "enum", "T1078",
            description="Default credential scanner across many services",
            priority=2, tags=["creds", "default"]))
        add(CatalogEntry("davtest", "enum", "T1105",
            services=["http", "https", "webdav"],
            description="WebDAV server test — upload, execute methods",
            priority=3, arg_template="-url {url}", tags=["web", "webdav"]))
        add(CatalogEntry("fuzz", "enum", "T1592",
            services=["http", "https"],
            description="Generic fuzzer for web parameters/headers",
            priority=4, tags=["web"]))
        add(CatalogEntry("openredirex", "enum", "T1598",
            services=["http", "https"],
            description="Open redirect vulnerability scanner",
            priority=6, tags=["web"]))
        add(CatalogEntry("lazynmap", "enum", "T1046",
            description="Full nmap scan (also used for detailed enum after initial recon)",
            priority=1, arg_template="{target}", tags=["network"]))
        add(CatalogEntry("nmapscript", "enum", "T1046",
            services=["http", "https", "smb", "ftp", "ssh", "mssql"],
            description="NSE script scan for service-specific vulnerabilities",
            requires_port=True, priority=2,
            arg_template="{port}", tags=["network", "vuln"]))
        add(CatalogEntry("osmedeus", "enum", "T1595",
            description="Full automated recon workflow (passive + active)",
            priority=4, tags=["automation", "osint"]))
        add(CatalogEntry("bbot", "enum", "T1595",
            description="Recursive OSINT and attack surface scanning",
            priority=3, tags=["osint", "automation"]))
        add(CatalogEntry("amass", "enum", "T1590",
            description="ASN/subdomain enumeration and graph mapping",
            priority=2, arg_template="enum -d {domain}", tags=["osint", "dns"]))
        add(CatalogEntry("allin", "enum", "T1595",
            description="All-in-one scanner launcher (nmap+gobuster+nikto)",
            priority=3, tags=["automation"]))
        add(CatalogEntry("magicrecon", "enum", "T1595",
            description="Automated recon wrapper for bug bounty-style scanning",
            priority=5, tags=["automation"]))
        add(CatalogEntry("dmitry", "enum", "T1590",
            description="Deepmagic Information Gathering Tool",
            priority=6, arg_template="{target}", tags=["osint"]))
        # SMB/NetBIOS
        add(CatalogEntry("enum4linux", "enum", "T1087",
            services=["smb", "netbios", "445", "139"],
            description="Linux/Samba/Windows SMB enumeration",
            priority=1, arg_template="{target}", tags=["smb", "ad"]))
        add(CatalogEntry("enum4linux_ng", "enum", "T1087",
            services=["smb", "netbios", "445"],
            description="Next-gen enum4linux with LDAP/RPC/SMB/Kerberos",
            priority=1, arg_template="{target}", tags=["smb", "ad"]))
        add(CatalogEntry("smbclient", "enum", "T1083",
            services=["smb", "445"],
            description="SMB client for share listing and file access",
            priority=2, arg_template="-L //{target}", tags=["smb"]))
        add(CatalogEntry("smbclient_py", "enum", "T1083",
            services=["smb", "445"],
            description="Impacket smbclient.py for SMB share enumeration",
            priority=2, requires_creds=True, tags=["smb", "impacket"]))
        add(CatalogEntry("smbclient_impacket", "enum", "T1083",
            services=["smb", "445"],
            description="Impacket SMB client with advanced options",
            priority=3, tags=["smb", "impacket"]))
        add(CatalogEntry("smbmap", "enum", "T1083",
            services=["smb", "445"],
            description="SMB share mapper with read/write access check",
            priority=1, arg_template="-H {target}", tags=["smb"]))
        add(CatalogEntry("smbattack", "enum", "T1021",
            services=["smb", "445"],
            description="SMB attack suite (relay, poisoning, auth)",
            priority=4, tags=["smb", "exploit"]))
        add(CatalogEntry("nbtscan", "enum", "T1018",
            services=["netbios", "137", "139"],
            description="NetBIOS name and MAC scanner",
            priority=4, arg_template="{target}", tags=["smb"]))
        add(CatalogEntry("netexec", "enum", "T1087",
            services=["smb", "winrm", "ldap"],
            description="NetExec (nxc) - modern CrackMapExec successor",
            priority=1, arg_template="smb {target}", tags=["smb", "ad", "win"]))
        add(CatalogEntry("cme", "enum", "T1087",
            services=["smb", "winrm"],
            description="CrackMapExec SMB/WinRM/LDAP enumeration",
            priority=1, arg_template="smb {target}", tags=["smb", "ad"]))
        add(CatalogEntry("rpcclient", "enum", "T1087",
            services=["smb", "rpc", "445"],
            description="Windows RPC client for user/group/share enum",
            priority=2, arg_template="{target}", tags=["smb", "rpc"]))
        add(CatalogEntry("rpcdump", "enum", "T1135",
            services=["rpc", "135"],
            description="Dump RPC endpoints via Impacket rpcdump.py",
            priority=3, arg_template="{target}", tags=["rpc", "impacket"]))
        add(CatalogEntry("rpcmap_py", "enum", "T1135",
            services=["rpc", "135"],
            description="Map RPC UUIDs with impacket rpcmap.py",
            priority=4, tags=["rpc", "impacket"]))
        add(CatalogEntry("samrdump", "enum", "T1087",
            services=["smb", "445"],
            description="Impacket samrdump — enumerate SAM database remotely",
            priority=3, tags=["smb", "impacket", "creds"]))
        add(CatalogEntry("netview", "enum", "T1018",
            services=["smb", "445"],
            description="Enumerate logged-on users via NetView/impacket",
            priority=5, tags=["smb", "ad"]))
        # LDAP / Active Directory
        add(CatalogEntry("ldapsearch", "enum", "T1087",
            services=["ldap", "389", "636"],
            description="LDAP directory search for users/groups/OUs",
            priority=1, arg_template="{target}", tags=["ldap", "ad"]))
        add(CatalogEntry("ldapdomaindump", "enum", "T1087",
            services=["ldap", "389"],
            description="Full LDAP domain dump to HTML/JSON/CSV",
            requires_creds=True, priority=1,
            arg_template="{domain}", tags=["ldap", "ad"]))
        add(CatalogEntry("bloodhound", "enum", "T1087",
            services=["ldap", "kerberos", "389"],
            description="BloodHound data collection for AD attack path analysis",
            requires_creds=True, priority=1, tags=["ad", "bloodhound"]))
        add(CatalogEntry("ad_ldap_enum", "enum", "T1087",
            services=["ldap", "389"],
            description="AD LDAP enumeration — users, computers, groups",
            priority=2, tags=["ldap", "ad"]))
        add(CatalogEntry("windapsearch", "enum", "T1087",
            services=["ldap", "389"],
            description="LDAP windapsearch for users/computers/privileged groups",
            priority=2, arg_template="-d {domain} --dc {target}", tags=["ldap", "ad"]))
        add(CatalogEntry("lookupsid", "enum", "T1087",
            services=["smb", "445"],
            description="Impacket lookupsid — brute-force SIDs to enumerate users",
            priority=3, arg_template="{target}", tags=["smb", "ad", "impacket"]))
        add(CatalogEntry("lookupsid_py", "enum", "T1087",
            services=["smb", "445"],
            description="Python lookupsid for anonymous SID brute-force",
            priority=3, tags=["smb", "ad", "impacket"]))
        add(CatalogEntry("pre2k", "enum", "T1087",
            services=["kerberos", "88"],
            description="Enumerate pre-Win2000 compatible accounts (AS-REP roastable)",
            priority=3, tags=["ad", "kerberos"]))
        add(CatalogEntry("hound", "enum", "T1087",
            services=["ldap", "389"],
            description="BloodHound-CE data ingestor",
            priority=2, tags=["ad", "bloodhound"]))
        # Kerberos
        add(CatalogEntry("kerbrute", "enum", "T1110",
            services=["kerberos", "88"],
            description="Kerberos user enumeration and password spray",
            priority=1, arg_template="userenum --dc {target} -d {domain}",
            tags=["kerberos", "ad"]))
        add(CatalogEntry("pykerbrute", "enum", "T1110",
            services=["kerberos", "88"],
            description="Python Kerbrute for AS-REQ user enumeration",
            priority=2, tags=["kerberos", "ad"]))
        add(CatalogEntry("getnpusers", "enum", "T1558",
            services=["kerberos", "88"],
            description="Impacket GetNPUsers — AS-REP roasting (no creds needed)",
            priority=1, arg_template="{domain}/",
            tags=["kerberos", "ad", "impacket"]))
        # SNMP
        add(CatalogEntry("snmpwalk", "enum", "T1602",
            services=["snmp", "161"],
            description="SNMP walk for service enumeration and config leakage",
            priority=1, arg_template="{target}", tags=["snmp"]))
        add(CatalogEntry("snmpcheck", "enum", "T1602",
            services=["snmp", "161"],
            description="SNMP check for users, shares, processes, software",
            priority=2, arg_template="{target}", tags=["snmp"]))
        # SMTP
        add(CatalogEntry("smtpuserenum", "enum", "T1087",
            services=["smtp", "25"],
            description="SMTP VRFY/RCPT user enumeration",
            priority=2, arg_template="-t {target}", tags=["smtp"]))
        add(CatalogEntry("swaks", "enum", "T1566",
            services=["smtp", "25"],
            description="Swiss Army Knife for SMTP testing",
            priority=3, arg_template="--server {target}", tags=["smtp"]))
        # Other protocols
        add(CatalogEntry("finger_user_enum", "enum", "T1087",
            services=["finger", "79"],
            description="Finger protocol user enumeration",
            priority=5, tags=["legacy"]))
        add(CatalogEntry("mqtt_check_py", "enum", "T1040",
            services=["mqtt", "1883"],
            description="MQTT broker check for anonymous access",
            priority=5, tags=["iot"]))
        add(CatalogEntry("certipy", "enum", "T1649",
            services=["ldap", "kerberos", "389"],
            description="AD certificate services enumeration and exploitation",
            priority=1, arg_template="find -u {user}@{domain} -p {password} -dc-ip {target}",
            tags=["adcs", "ad", "kerberos"]))
        add(CatalogEntry("certipy_ad", "enum", "T1649",
            services=["ldap", "kerberos"],
            description="CertiPy AD CS attack and abuse automation",
            priority=1, requires_creds=True,
            arg_template="find -u {user}@{domain} -p {password}",
            tags=["adcs", "ad"]))
        add(CatalogEntry("breacher", "enum", "T1552",
            services=["http", "https"],
            description="Admin panel and login page finder",
            priority=4, tags=["web"]))
        add(CatalogEntry("odat", "enum", "T1078",
            services=["oracle", "1521"],
            description="Oracle Database Attack Tool",
            priority=2, tags=["oracle", "database"]))
        add(CatalogEntry("lynis", "enum", "T1518",
            description="System security auditing (local Linux)",
            priority=3, os_target="linux", tags=["privesc-recon"]))
        add(CatalogEntry("sawks", "enum", "T1046",
            description="Service-aware well-known service scanner",
            priority=4, tags=["network"]))
        add(CatalogEntry("vscan", "enum", "T1046",
            description="Vulnerability scanner wrapper for common services",
            priority=4, tags=["vuln"]))
        add(CatalogEntry("portdiscover", "enum", "T1046",
            description="Light port discovery on target subnet",
            priority=4, arg_template="{target}", tags=["network"]))
        add(CatalogEntry("portservicediscover", "enum", "T1046",
            description="Map open ports to known service banners",
            priority=5, tags=["network"]))
        add(CatalogEntry("rdp_check_py", "enum", "T1046",
            services=["rdp", "3389"],
            description="Check RDP availability and version via impacket",
            priority=3, arg_template="{target}", tags=["rdp", "windows"]))
        add(CatalogEntry("net_rpc_addmem", "enum", "T1087",
            services=["smb", "445"],
            description="Add member to domain group via net rpc",
            priority=6, requires_creds=True, tags=["ad", "smb"]))
        add(CatalogEntry("sessionssh", "enum", "T1021",
            services=["ssh", "22"],
            description="SSH session enumeration and command runner",
            priority=3, requires_creds=True, tags=["ssh"]))
        add(CatalogEntry("evil_ssdp", "enum", "T1557",
            description="SSDP/UPnP poisoning for NTLM credential capture",
            priority=5, tags=["mitm", "ntlm"]))

        # ====================================================================
        # 03. EXPLOITATION
        # ====================================================================
        add(CatalogEntry("sqlmap", "exploit", "T1190",
            services=["http", "https"],
            description="SQL injection detection and exploitation",
            priority=1, arg_template="-u {url}", tags=["web", "sqli"]))
        add(CatalogEntry("sqli", "exploit", "T1190",
            services=["http", "https"],
            description="Manual SQL injection helper/payload generator",
            priority=2, tags=["web", "sqli"]))
        add(CatalogEntry("sqli_mssql_test", "exploit", "T1190",
            services=["mssql", "1433", "http"],
            description="MSSQL-specific SQL injection test suite",
            priority=2, tags=["mssql", "sqli"]))
        add(CatalogEntry("sqsh", "exploit", "T1078",
            services=["mssql", "1433"],
            description="Sybase/MSSQL command-line client",
            priority=3, requires_creds=True, tags=["mssql"]))
        add(CatalogEntry("commix", "exploit", "T1059",
            services=["http", "https"],
            description="Command injection detection and exploitation",
            priority=1, arg_template="--url {url}", tags=["web", "cmdi"]))
        add(CatalogEntry("xss", "exploit", "T1059",
            services=["http", "https"],
            description="XSS payload injection and capture",
            priority=3, tags=["web", "xss"]))
        add(CatalogEntry("xsstrike", "exploit", "T1059",
            services=["http", "https"],
            description="Advanced XSS scanner and exploitation",
            priority=2, arg_template="-u {url}", tags=["web", "xss"]))
        add(CatalogEntry("lfi", "exploit", "T1083",
            services=["http", "https"],
            description="Local File Inclusion exploitation",
            priority=2, tags=["web", "lfi"]))
        add(CatalogEntry("upload_bypass", "exploit", "T1105",
            services=["http", "https"],
            description="File upload restriction bypass techniques",
            priority=3, tags=["web"]))
        add(CatalogEntry("filtering", "exploit", "T1059",
            services=["http", "https"],
            description="WAF bypass and input filter circumvention",
            priority=4, tags=["web", "bypass"]))
        add(CatalogEntry("unicode_WAFbypass", "exploit", "T1059",
            services=["http", "https"],
            description="Unicode normalization WAF bypass",
            priority=4, tags=["web", "bypass"]))
        add(CatalogEntry("utf", "exploit", "T1059",
            services=["http", "https"],
            description="UTF-8 encoding bypass for web filters",
            priority=5, tags=["web", "bypass"]))
        add(CatalogEntry("padbuster", "exploit", "T1552",
            services=["http", "https"],
            description="Padding oracle attack against CBC-mode encryption",
            priority=3, tags=["web", "crypto"]))
        add(CatalogEntry("pyoracle2", "exploit", "T1552",
            services=["http", "https"],
            description="Python padding oracle attack tool",
            priority=3, tags=["web", "crypto"]))
        add(CatalogEntry("jwt_tool", "exploit", "T1552",
            services=["http", "https"],
            description="JWT attack toolkit: none-alg, brute, injection",
            priority=2, tags=["web", "jwt"]))
        add(CatalogEntry("shellshock", "exploit", "T1190",
            services=["http", "https", "cgi"],
            description="Shellshock (CVE-2014-6271) exploitation",
            priority=2, arg_template="-u {url}", tags=["cgi", "rce"]))
        add(CatalogEntry("download_exploit", "exploit", "T1190",
            description="Download and stage exploits from ExploitDB",
            priority=4, tags=["exploit"]))
        add(CatalogEntry("ms08_067_netapi", "exploit", "T1203",
            services=["smb", "445", "139"],
            description="MS08-067 NetAPI exploit (EternalBlue predecessor)",
            priority=3, os_target="windows", tags=["smb", "exploit"]))
        add(CatalogEntry("eternal", "exploit", "T1203",
            services=["smb", "445"],
            description="EternalBlue MS17-010 exploitation",
            priority=2, os_target="windows", tags=["smb", "exploit"]))
        add(CatalogEntry("iis_webdav_upload_asp", "exploit", "T1190",
            services=["http", "webdav"],
            description="IIS WebDAV ASP upload and execution",
            priority=3, os_target="windows", tags=["iis", "webdav", "rce"]))
        add(CatalogEntry("rejetto_hfs_exec", "exploit", "T1190",
            services=["http"],
            description="Rejetto HFS 2.3 remote code execution",
            priority=3, tags=["hfs", "rce"]))
        add(CatalogEntry("cacti_exploit", "exploit", "T1190",
            services=["http", "https"],
            description="Cacti network monitor exploitation",
            priority=4, tags=["web", "rce"]))
        add(CatalogEntry("printerbug_py", "exploit", "T1187",
            services=["smb", "445"],
            description="PrinterBug — force NTLM authentication via spooler",
            priority=3, os_target="windows", tags=["smb", "ntlm", "coerce"]))
        add(CatalogEntry("gettgtpkinit_py", "exploit", "T1558",
            services=["kerberos", "88"],
            description="Get TGT via PKINIT (certificate-based Kerberos auth)",
            priority=2, os_target="windows", tags=["kerberos", "adcs"]))
        add(CatalogEntry("gets4uticket_py", "exploit", "T1558",
            services=["kerberos", "88"],
            description="S4U2Self/S4U2Proxy ticket request (constrained delegation)",
            priority=3, os_target="windows", tags=["kerberos", "delegation"]))
        add(CatalogEntry("aclpwn_py", "exploit", "T1098",
            services=["ldap", "389"],
            description="ACL-based privilege escalation in Active Directory",
            priority=2, os_target="windows",
            arg_template="-f {user} -ft user -t {domain} -d {domain}",
            tags=["ad", "acl"]))
        add(CatalogEntry("addspn_py", "exploit", "T1098",
            services=["ldap", "389"],
            description="Add SPN to AD account for Kerberoasting setup",
            priority=3, os_target="windows", tags=["ad", "kerberos"]))
        add(CatalogEntry("owneredit", "exploit", "T1098",
            services=["ldap", "389"],
            description="Edit AD object ownership for privilege escalation",
            priority=3, requires_creds=True, tags=["ad", "acl"]))
        add(CatalogEntry("dacledit", "exploit", "T1098",
            services=["ldap", "389"],
            description="Edit DACL permissions on AD objects",
            priority=3, requires_creds=True, tags=["ad", "acl"]))
        add(CatalogEntry("autoblody", "exploit", "T1098",
            services=["ldap", "445"],
            description="Automated AD privilege escalation (bloodyAD wrapper)",
            priority=2, requires_creds=True, tags=["ad", "acl"]))
        add(CatalogEntry("krbrelayx_py", "exploit", "T1558",
            services=["kerberos", "88"],
            description="Kerberos relaying and unconstrained delegation attack",
            priority=2, os_target="windows", tags=["kerberos", "relay"]))
        add(CatalogEntry("ticketer", "exploit", "T1558",
            services=["kerberos", "88"],
            description="Impacket ticketer — forge Silver/Golden tickets",
            priority=2, requires_creds=True, tags=["kerberos", "impacket"]))
        add(CatalogEntry("pywhisker", "exploit", "T1649",
            services=["ldap", "389"],
            description="Shadow Credentials attack via msDS-KeyCredentialLink",
            priority=2, tags=["adcs", "ad"]))
        add(CatalogEntry("kusa", "exploit", "T1059",
            description="KUSA — kernel userland shellcode agent",
            priority=5, os_target="linux", tags=["shellcode"]))
        add(CatalogEntry("sireprat", "exploit", "T1059",
            services=["http", "https"],
            description="SirepRAT Windows IoT Core RCE exploit",
            priority=5, tags=["iot", "rce"]))
        add(CatalogEntry("lol", "exploit", "T1218",
            description="Living-off-the-land binary execution helper",
            priority=4, os_target="windows", tags=["lolbas"]))
        add(CatalogEntry("psexec", "exploit", "T1569",
            services=["smb", "445"],
            description="Sysinternals PsExec for remote command execution",
            priority=1, requires_creds=True, os_target="windows",
            arg_template="\\\\{target} -u {user} -p {password} cmd",
            tags=["smb", "exec"]))
        add(CatalogEntry("psexec_py", "exploit", "T1569",
            services=["smb", "445"],
            description="Impacket psexec.py — SMB service-based RCE",
            priority=1, requires_creds=True, os_target="windows",
            arg_template="{domain}/{user}:{password}@{target}",
            tags=["smb", "exec", "impacket"]))
        add(CatalogEntry("sshexploit", "exploit", "T1190",
            services=["ssh", "22"],
            description="SSH vulnerability exploitation (known CVEs)",
            priority=4, tags=["ssh"]))
        add(CatalogEntry("downloader", "exploit", "T1105",
            description="Download and execute remote payload via HTTP",
            priority=5, arg_template="{url}"))
        add(CatalogEntry("rev", "exploit", "T1059",
            description="One-liner reverse shell generator and clipboard copy",
            priority=3, arg_template="{lhost} {lport}"))
        add(CatalogEntry("lazypwn", "exploit", "T1203",
            description="LazyOwn automated exploitation framework launcher",
            priority=2, arg_template="{target}"))
        add(CatalogEntry("pyautomate", "exploit", "T1059",
            services=["http", "https"],
            description="Automated exploitation workflow",
            priority=4))
        add(CatalogEntry("powerserver", "exploit", "T1105",
            services=["http", "https"],
            description="PowerShell web delivery server",
            priority=4, os_target="windows", tags=["powershell"]))
        add(CatalogEntry("www", "exploit", "T1105",
            description="Quick HTTP server for payload delivery",
            priority=3, arg_template="{lport}"))
        add(CatalogEntry("cp", "exploit", "T1105",
            description="Copy file to web delivery directory",
            priority=5))
        add(CatalogEntry("ss", "exploit", "T1003",
            description="Shadow file/SAM secrets extraction helper",
            priority=5, os_target="linux"))
        add(CatalogEntry("digdug", "exploit", "T1071",
            description="DNS tunneling exploitation framework",
            priority=6, tags=["dns", "tunnel"]))
        add(CatalogEntry("template_helper_serializer", "exploit", "T1059",
            services=["http", "https"],
            description="SSTI and deserialization template payload helper",
            priority=3, tags=["web", "ssti"]))
        add(CatalogEntry("ntpdate", "exploit", "T1562",
            description="Sync time with target DC for Kerberos attacks",
            priority=3, arg_template="{target}", tags=["kerberos"]))
        add(CatalogEntry("seo", "exploit", "T1190",
            services=["http", "https"],
            description="SEO injection exploitation helper",
            priority=7))
        add(CatalogEntry("unicode_WAFbypass", "exploit", "T1059",
            services=["http", "https"],
            description="Unicode-based WAF bypass for web exploits",
            priority=4))
        add(CatalogEntry("sharpshooter", "exploit", "T1587",
            description="SharpShooter payload generator (.NET-based)",
            priority=5, os_target="windows", tags=["payload", "bypass"]))
        add(CatalogEntry("greatSCT", "exploit", "T1587",
            description="GreatSCT payload bypass tool (MSF + AV evasion)",
            priority=5, os_target="windows", tags=["payload", "av_bypass"]))
        add(CatalogEntry("excelntdonut", "exploit", "T1587",
            description="Donut shellcode in Excel macro payload",
            priority=5, os_target="windows", tags=["payload", "office"]))
        add(CatalogEntry("winbase64payload", "exploit", "T1027",
            description="Windows base64-encoded powershell payload generator",
            priority=4, os_target="windows", tags=["powershell", "payload"]))
        add(CatalogEntry("wrapper", "exploit", "T1059",
            description="Payload wrapper for bypass techniques",
            priority=5))
        add(CatalogEntry("shellfire", "exploit", "T1059",
            description="Shellfire exploit integration helper",
            priority=6))
        add(CatalogEntry("img2cookie", "exploit", "T1185",
            services=["http", "https"],
            description="Cookie stealing via image tag injection",
            priority=5, tags=["web", "xss"]))
        add(CatalogEntry("createcookie", "exploit", "T1539",
            description="Create forged session cookies",
            priority=5, tags=["web"]))
        add(CatalogEntry("createdll", "exploit", "T1574",
            description="Create malicious DLL for hijacking",
            priority=4, os_target="windows", tags=["dll", "hijack"]))

        # ====================================================================
        # 04. POST-EXPLOITATION
        # ====================================================================
        add(CatalogEntry("ssh_cmd", "postexp", "T1021",
            services=["ssh", "22"],
            description="Remote command execution over SSH",
            priority=1, requires_creds=True,
            arg_template="-h {target} -p {port}", tags=["ssh"]))
        add(CatalogEntry("lazywebshell", "postexp", "T1505",
            services=["http", "https"],
            description="Web shell deployment and interactive control",
            priority=1, tags=["webshell"]))
        add(CatalogEntry("issue_command_to_c2", "postexp", "T1105",
            description="Issue command to connected C2 implant",
            priority=1))
        add(CatalogEntry("mimikatzpy", "postexp", "T1003",
            services=["smb", "445"],
            description="Impacket mimikatz.py for in-memory credential extraction",
            priority=1, requires_creds=True, os_target="windows",
            arg_template="{domain}/{user}:{password}@{target}",
            tags=["creds", "windows"]))
        add(CatalogEntry("rubeus", "postexp", "T1558",
            description="Rubeus Kerberos attack toolkit (TGT, TGS, roasting)",
            priority=1, os_target="windows", tags=["kerberos"]))
        add(CatalogEntry("scavenger", "postexp", "T1083",
            description="Post-exploitation file and credential scavenger",
            priority=2, tags=["enum", "creds"]))
        add(CatalogEntry("find", "postexp", "T1083",
            description="Find SUID/world-writable files, cron jobs, secrets",
            priority=2, os_target="linux", tags=["privesc-recon"]))
        add(CatalogEntry("cports", "postexp", "T1049",
            description="Connected ports enumeration on compromised host",
            priority=3))
        add(CatalogEntry("msfshellcoder", "postexp", "T1587",
            description="MSFvenom shellcode generator in C format",
            priority=3, arg_template="{lhost} {lport}"))
        add(CatalogEntry("shellcode", "postexp", "T1055",
            description="Shellcode injection helper",
            priority=3, tags=["shellcode"]))
        add(CatalogEntry("shellcode2elf", "postexp", "T1587",
            description="Convert shellcode to ELF binary",
            priority=4, os_target="linux", tags=["shellcode"]))
        add(CatalogEntry("shellcode2sylk", "postexp", "T1587",
            description="Embed shellcode in Excel SYLK file",
            priority=5, os_target="windows", tags=["shellcode", "office"]))
        add(CatalogEntry("shellcode_search", "postexp", "T1588",
            description="Search for usable shellcode patterns",
            priority=5))
        add(CatalogEntry("hex2shellcode", "postexp", "T1027",
            description="Convert hex string to shellcode bytes",
            priority=5))
        add(CatalogEntry("bin2shellcode", "postexp", "T1027",
            description="Extract shellcode from compiled binary",
            priority=5))
        add(CatalogEntry("aes_pe", "postexp", "T1027",
            description="AES-encrypt PE payload for AV bypass",
            priority=3, os_target="windows", tags=["av_bypass", "payload"]))
        add(CatalogEntry("createpayload", "postexp", "T1587",
            description="Create MSFvenom reverse shell payload",
            priority=2, arg_template="{lhost} {lport}", tags=["payload"]))
        add(CatalogEntry("ofuscate_string", "postexp", "T1027",
            description="Obfuscate strings for AV/EDR bypass",
            priority=4, tags=["bypass"]))
        add(CatalogEntry("ofuscatesh", "postexp", "T1027",
            description="Obfuscate shell script content",
            priority=4, os_target="linux", tags=["bypass"]))
        add(CatalogEntry("ofuscatorps1", "postexp", "T1027",
            description="Obfuscate PowerShell script",
            priority=4, os_target="windows", tags=["powershell", "bypass"]))
        add(CatalogEntry("powershell_cmd_stager", "postexp", "T1059",
            description="PowerShell stager for multi-stage payload delivery",
            priority=3, os_target="windows", tags=["powershell", "stager"]))
        add(CatalogEntry("disableav", "postexp", "T1562",
            description="Disable AV/defender on compromised Windows host",
            priority=4, os_target="windows", tags=["defense_evasion"]))
        add(CatalogEntry("follina", "postexp", "T1203",
            services=["http", "https"],
            description="Follina (CVE-2022-30190) MSDT exploitation",
            priority=3, os_target="windows", tags=["office", "rce"]))
        add(CatalogEntry("adversary_yaml", "postexp", "T1059",
            description="Execute adversary playbook from YAML steps",
            priority=2))
        add(CatalogEntry("adversary", "postexp", "T1059",
            description="Execute interactive adversary simulation",
            priority=2))
        add(CatalogEntry("atomic_lazyown", "postexp", "T1059",
            description="Run Atomic Red Team test via LazyOwn",
            priority=3, tags=["atomic", "simulation"]))
        add(CatalogEntry("ai_playbook", "postexp", "T1059",
            description="AI-generated offensive playbook from scan results",
            priority=4, tags=["ai"]))
        add(CatalogEntry("scp", "postexp", "T1105",
            services=["ssh", "22"],
            description="Secure copy file to/from compromised host",
            priority=3, requires_creds=True, tags=["ssh"]))
        add(CatalogEntry("extract_yaml", "postexp", "T1083",
            description="Extract YAML-encoded data from adversary configs",
            priority=6))
        add(CatalogEntry("exe2bin", "postexp", "T1027",
            description="Convert EXE to binary shellcode for injection",
            priority=5, os_target="windows"))
        add(CatalogEntry("exe2donutbin", "postexp", "T1027",
            description="Convert EXE to Donut position-independent shellcode",
            priority=4, os_target="windows", tags=["donut", "shellcode"]))
        add(CatalogEntry("pezorsh", "postexp", "T1027",
            description="PEzor shellcode + PE loader for AV bypass",
            priority=4, os_target="windows", tags=["pe", "bypass"]))
        add(CatalogEntry("path2hex", "postexp", "T1027",
            description="Convert path string to hex for evasion",
            priority=6))
        add(CatalogEntry("d3monizedshell", "postexp", "T1505",
            description="Deploy d3monized interactive web shell",
            priority=3, tags=["webshell"]))
        add(CatalogEntry("apt_proxy", "postexp", "T1090",
            description="Configure APT to use attacker proxy on Linux target",
            priority=6, os_target="linux"))
        add(CatalogEntry("pip_proxy", "postexp", "T1090",
            description="Route Python pip through attacker proxy",
            priority=6, os_target="linux"))
        add(CatalogEntry("service_ssh", "postexp", "T1021",
            description="Start/manage SSH service on compromised host",
            priority=5, os_target="linux", tags=["ssh", "persistence"]))
        add(CatalogEntry("py3ttyup", "postexp", "T1059",
            description="Upgrade shell to full interactive PTY (Python3)",
            priority=2, os_target="linux", tags=["pty"]))
        add(CatalogEntry("sessionsshstrace", "postexp", "T1056",
            description="SSH session tracing with strace for credential capture",
            priority=5, os_target="linux", tags=["capture"]))
        add(CatalogEntry("create_synthetic", "postexp", "T1087",
            description="Create synthetic training data from session output",
            priority=7, tags=["ml"]))

        # ====================================================================
        # 05. PERSISTENCE
        # ====================================================================
        add(CatalogEntry("backdoor_factory", "persist", "T1543",
            description="Patch PE binaries with backdoor payload",
            priority=2, os_target="windows", tags=["backdoor", "pe"]))
        add(CatalogEntry("createwebshell", "persist", "T1505",
            services=["http", "https"],
            description="Deploy web shell (PHP/ASPX/JSP) to web root",
            priority=1, tags=["webshell"]))
        add(CatalogEntry("weevely", "persist", "T1505",
            services=["http", "https"],
            description="Weevely steganographic PHP web shell",
            priority=2, tags=["webshell", "php"]))
        add(CatalogEntry("weevelygen", "persist", "T1505",
            description="Generate weevely web shell payload",
            priority=3, tags=["webshell", "php"]))
        add(CatalogEntry("generate_revshell", "persist", "T1059",
            description="Generate reverse shell one-liner or payload",
            priority=2, arg_template="{lhost} {lport}"))
        add(CatalogEntry("createrevshell", "persist", "T1059",
            description="Create staged reverse shell script",
            priority=3, arg_template="{lhost} {lport}"))
        add(CatalogEntry("createwinrevshell", "persist", "T1059",
            description="Create Windows reverse shell (.bat/.ps1)",
            priority=3, os_target="windows", arg_template="{lhost} {lport}"))
        add(CatalogEntry("conptyshell", "persist", "T1059",
            description="ConPtyShell — fully interactive Windows reverse shell",
            priority=2, os_target="windows", arg_template="{lhost} {lport}"))
        add(CatalogEntry("listener_py", "persist", "T1095",
            description="Python reverse shell listener",
            priority=2, arg_template="{lport}"))
        add(CatalogEntry("listener_go", "persist", "T1095",
            description="Go-based reverse shell listener",
            priority=3, arg_template="{lport}"))
        add(CatalogEntry("pwncat", "persist", "T1095",
            description="pwncat — advanced reverse shell handler with persistence",
            priority=1, arg_template="-l {lport}", tags=["pwncat"]))
        add(CatalogEntry("pwncatcs", "persist", "T1095",
            description="pwncat-cs C&C server mode",
            priority=1, tags=["pwncat"]))
        add(CatalogEntry("rdp", "persist", "T1021",
            services=["rdp", "3389"],
            description="Enable/connect RDP on Windows target",
            priority=3, requires_creds=True, os_target="windows"))
        add(CatalogEntry("ssh", "persist", "T1021",
            services=["ssh", "22"],
            description="SSH connection with key or password",
            priority=2, requires_creds=True, arg_template="{user}@{target}"))
        add(CatalogEntry("toctoc", "persist", "T1205",
            description="Port knocking implementation for covert persistence",
            priority=5, tags=["stealth"]))
        add(CatalogEntry("knokknok", "persist", "T1205",
            description="Port knocking sequence sender",
            priority=5, tags=["stealth"]))
        add(CatalogEntry("darkarmour", "persist", "T1027",
            description="DarkArmour PE packer/crypter for AV bypass",
            priority=4, os_target="windows", tags=["av_bypass"]))
        add(CatalogEntry("scarecrow", "persist", "T1027",
            description="ScareCrow — EDR bypass payload generation",
            priority=3, os_target="windows", tags=["edr_bypass"]))
        add(CatalogEntry("veil", "persist", "T1027",
            description="Veil-Evasion AV bypass framework",
            priority=4, os_target="windows", tags=["av_bypass"]))
        add(CatalogEntry("ivy", "persist", "T1027",
            description="Ivy payload bypass framework (Go-based)",
            priority=4, os_target="windows", tags=["av_bypass"]))
        add(CatalogEntry("revwin", "persist", "T1059",
            description="Windows reverse shell generator (multiple methods)",
            priority=3, os_target="windows"))
        add(CatalogEntry("ftp", "persist", "T1021",
            services=["ftp", "21"],
            description="FTP client for file transfer on compromised host",
            priority=5, tags=["ftp"]))
        add(CatalogEntry("asprevbase64", "persist", "T1027",
            description="Base64-encoded ASP reverse shell for IIS",
            priority=4, os_target="windows", tags=["asp", "iis"]))
        add(CatalogEntry("msfpc", "persist", "T1587",
            description="MSFvenom payload creator — automated multi-platform",
            priority=2, arg_template="{lhost} {lport}"))
        add(CatalogEntry("grisun0", "persist", "T1136",
            description="Create backdoor admin user (Linux)",
            priority=2, os_target="linux", tags=["user_creation"]))
        add(CatalogEntry("grisun0w", "persist", "T1136",
            description="Create backdoor admin user (Windows)",
            priority=2, os_target="windows", tags=["user_creation"]))
        add(CatalogEntry("paranoid_meterpreter", "persist", "T1573",
            description="Encrypted meterpreter reverse HTTPS with certificate pinning",
            priority=3, tags=["meterpreter"]))
        add(CatalogEntry("setoolKits", "persist", "T1566",
            description="Social Engineering Toolkit launcher",
            priority=6, tags=["phishing"]))
        add(CatalogEntry("dr0p1t", "persist", "T1587",
            description="dr0p1t payload dropper framework",
            priority=5, os_target="windows", tags=["dropper"]))
        add(CatalogEntry("service", "persist", "T1543",
            description="Install backdoor as system service",
            priority=4, tags=["service"]))

        # ====================================================================
        # 06. PRIVILEGE ESCALATION
        # ====================================================================
        add(CatalogEntry("responder", "privesc", "T1557",
            description="Responder — LLMNR/NBT-NS/MDNS poisoning for hash capture",
            priority=1, tags=["mitm", "ntlm", "hash_capture"]))
        add(CatalogEntry("smbserver", "privesc", "T1557",
            description="Impacket SMB server for NTLM relay/capture",
            priority=1, arg_template="TMP {target}", tags=["smb", "ntlm", "relay"]))

        # ====================================================================
        # 07. CREDENTIAL ACCESS
        # ====================================================================
        add(CatalogEntry("hydra", "cred", "T1110",
            services=["ssh", "ftp", "http", "smb", "rdp", "winrm"],
            description="Multi-protocol online brute-force",
            priority=1, requires_port=True,
            arg_template="-l {user} -P {wordlist} {target} ssh",
            tags=["bruteforce"]))
        add(CatalogEntry("medusa", "cred", "T1110",
            services=["ssh", "ftp", "smb"],
            description="Parallel brute-force tool",
            priority=2, requires_port=True, tags=["bruteforce"]))
        add(CatalogEntry("hashcat", "cred", "T1110",
            description="GPU-accelerated hash cracking",
            priority=1, tags=["hash", "offline"]))
        add(CatalogEntry("john2hash", "cred", "T1110",
            description="John the Ripper hash cracking",
            priority=2, tags=["hash", "offline"]))
        add(CatalogEntry("john2keepas", "cred", "T1555",
            description="Crack KeePass database with John",
            priority=3, tags=["keepass", "hash"]))
        add(CatalogEntry("john2zip", "cred", "T1110",
            description="Crack ZIP archive password with John",
            priority=3, tags=["zip", "hash"]))
        add(CatalogEntry("keepass", "cred", "T1555",
            description="KeePass database attack and extraction",
            priority=2, tags=["keepass"]))
        add(CatalogEntry("smalldic", "cred", "T1110",
            description="Small dictionary brute-force helper",
            priority=4, tags=["bruteforce"]))
        add(CatalogEntry("cubespraying", "cred", "T1110",
            description="Password spraying with cube-style word lists",
            priority=3, tags=["spray"]))
        add(CatalogEntry("passwordspray", "cred", "T1110",
            services=["smb", "ldap", "kerberos"],
            description="Active Directory password spraying",
            priority=1, arg_template="-d {domain} -u {user} -p {password}",
            tags=["spray", "ad"]))
        add(CatalogEntry("spraykatz", "cred", "T1110",
            services=["smb", "445"],
            description="Credential spraying + mimikatz remotely",
            priority=2, requires_creds=True, tags=["spray", "ad"]))
        add(CatalogEntry("adsso_spray", "cred", "T1110",
            services=["http", "https"],
            description="Azure AD SSO password spraying",
            priority=3, tags=["azure", "spray"]))
        add(CatalogEntry("cewl", "cred", "T1589",
            services=["http", "https"],
            description="Custom wordlist generator from website content",
            priority=3, arg_template="{url}", tags=["wordlist"]))
        add(CatalogEntry("crunch", "cred", "T1110",
            description="Wordlist generator with patterns and charsets",
            priority=4, tags=["wordlist"]))
        add(CatalogEntry("generatedic", "cred", "T1589",
            description="Generate targeted dictionary from target info",
            priority=4, tags=["wordlist"]))
        add(CatalogEntry("username_anarchy", "cred", "T1589",
            description="Generate username permutations from full names",
            priority=3, tags=["wordlist", "users"]))
        add(CatalogEntry("createcredentials", "cred", "T1078",
            description="Create credentials.txt for session tracking",
            priority=5, arg_template="{user} {password}"))
        add(CatalogEntry("createhash", "cred", "T1110",
            description="Generate various hash types for testing",
            priority=6))
        add(CatalogEntry("searchhash", "cred", "T1110",
            description="Search cracking databases for known hash",
            priority=3, tags=["hash"]))
        add(CatalogEntry("crack_cisco_7_password", "cred", "T1552",
            description="Decrypt Cisco type-7 passwords",
            priority=5, tags=["cisco"]))
        add(CatalogEntry("passtightvnc", "cred", "T1552",
            description="Decrypt TightVNC stored passwords",
            priority=4, tags=["vnc"]))
        add(CatalogEntry("sshkey", "cred", "T1552",
            description="SSH private key extraction and usage",
            priority=2, tags=["ssh"]))
        add(CatalogEntry("rocky", "cred", "T1110",
            description="RockYou-style attack via cached wordlists",
            priority=3, tags=["wordlist"]))
        add(CatalogEntry("sudo", "cred", "T1078",
            description="Enumerate sudo privileges on local system",
            priority=2, os_target="linux", tags=["privesc"]))
        add(CatalogEntry("cred", "cred", "T1078",
            description="Display stored credentials from session",
            priority=3))
        add(CatalogEntry("creds_py", "cred", "T1552",
            description="Python credential parser for common formats",
            priority=4))
        add(CatalogEntry("dacledit", "cred", "T1098",
            description="Edit DACL to gain write access for credential reset",
            priority=3, requires_creds=True, tags=["ad"]))
        add(CatalogEntry("refill_password", "cred", "T1552",
            description="Extract passwords from browser/app configs",
            priority=4, tags=["browser"]))
        add(CatalogEntry("transform", "cred", "T1027",
            description="Transform credential format (hash->NTLM, etc.)",
            priority=5))
        add(CatalogEntry("addusers", "cred", "T1136",
            description="Bulk user creation for testing/attack scenarios",
            priority=7))
        add(CatalogEntry("createusers_and_hashs", "cred", "T1136",
            description="Create user list with corresponding hashes",
            priority=7))
        add(CatalogEntry("createmail", "cred", "T1566",
            description="Generate phishing email payload",
            priority=6, tags=["phishing"]))

        # ====================================================================
        # 08. LATERAL MOVEMENT
        # ====================================================================
        add(CatalogEntry("evil_winrm", "lateral", "T1021",
            services=["winrm", "5985", "5986"],
            description="WinRM evil-winrm interactive shell",
            priority=1, requires_creds=True, os_target="windows",
            arg_template="-i {target} -u {user} -p {password}", tags=["winrm"]))
        add(CatalogEntry("wmiexec", "lateral", "T1047",
            services=["smb", "445", "135"],
            description="WMI-based remote command execution",
            priority=1, requires_creds=True, os_target="windows",
            arg_template="{domain}/{user}:{password}@{target}",
            tags=["wmi", "impacket"]))
        add(CatalogEntry("wmiexecpro", "lateral", "T1047",
            services=["smb", "445"],
            description="WmiExec-Pro for WMI operations without disk writes",
            priority=2, requires_creds=True, os_target="windows",
            tags=["wmi"]))
        add(CatalogEntry("dcomexec", "lateral", "T1021",
            services=["smb", "445", "135"],
            description="Impacket dcomexec — DCOM-based lateral movement",
            priority=3, requires_creds=True, os_target="windows",
            arg_template="{domain}/{user}:{password}@{target}",
            tags=["dcom", "impacket"]))
        add(CatalogEntry("lateral_mov_lin", "lateral", "T1021",
            services=["ssh", "22"],
            description="SSH-based lateral movement — installs LazyOwn on pivot",
            priority=1, requires_creds=True, os_target="linux", tags=["ssh"]))
        add(CatalogEntry("bloodyAD", "lateral", "T1098",
            services=["ldap", "389"],
            description="BloodyAD privilege escalation via LDAP",
            priority=2, requires_creds=True, tags=["ad", "acl"]))
        add(CatalogEntry("chisel", "lateral", "T1090",
            description="TCP/UDP tunneling via chisel reverse proxy",
            priority=1, arg_template="server -p {lport} --reverse", tags=["tunnel", "proxy"]))
        add(CatalogEntry("ligolo", "lateral", "T1090",
            description="Ligolo-ng reverse tunneling agent",
            priority=1, tags=["tunnel", "proxy"]))
        add(CatalogEntry("socat", "lateral", "T1090",
            description="Socat relay for port forwarding and pivoting",
            priority=2, arg_template="TCP-L:{lport},fork TCP:{target}:{port}",
            tags=["tunnel", "forward"]))
        add(CatalogEntry("regeorg", "lateral", "T1090",
            services=["http", "https"],
            description="ReGeorg SOCKS proxy via web shell tunnel",
            priority=3, tags=["tunnel", "proxy"]))
        add(CatalogEntry("shadowsocks", "lateral", "T1090",
            description="SOCKS5 encrypted tunnel via shadowsocks",
            priority=3, tags=["tunnel", "proxy"]))
        add(CatalogEntry("ngrok", "lateral", "T1572",
            description="Ngrok tunnel for C2 callback over internet",
            priority=4, tags=["tunnel", "c2"]))
        add(CatalogEntry("set_proxychains", "lateral", "T1090",
            description="Configure proxychains for pivot routing",
            priority=2, tags=["proxy"]))
        add(CatalogEntry("tord", "lateral", "T1090",
            description="Route traffic through Tor for anonymisation",
            priority=5, tags=["tor", "anon"]))
        add(CatalogEntry("gospherus", "lateral", "T1090",
            description="Gopherus SSRF payload generator for pivoting",
            services=["http", "https"],
            priority=4, tags=["ssrf", "pivot"]))
        add(CatalogEntry("mssqlcli", "lateral", "T1021",
            services=["mssql", "1433"],
            description="MSSQL client for lateral movement via xp_cmdshell",
            priority=2, requires_creds=True, tags=["mssql"]))
        add(CatalogEntry("getTGT", "lateral", "T1558",
            services=["kerberos", "88"],
            description="Impacket getTGT — request Kerberos TGT",
            priority=2, requires_creds=True,
            arg_template="{domain}/{user}:{password}", tags=["kerberos", "impacket"]))
        add(CatalogEntry("targetedKerberoas", "lateral", "T1558",
            services=["kerberos", "88"],
            description="Targeted Kerberoasting of specific service accounts",
            priority=1, requires_creds=True,
            arg_template="-u {user}@{domain} -p {password} -dc {target}",
            tags=["kerberos", "roasting"]))
        add(CatalogEntry("stormbreaker", "lateral", "T1021",
            services=["http", "https"],
            description="Stormbreaker — access camera/mic via HTTPS link",
            priority=6, tags=["social"]))
        add(CatalogEntry("nc", "lateral", "T1095",
            description="Netcat for port forwarding and pivot channels",
            priority=3, arg_template="-lvnp {lport}", tags=["netcat"]))
        add(CatalogEntry("id_rsa", "lateral", "T1552",
            services=["ssh", "22"],
            description="Extract and use discovered SSH private key",
            priority=2, tags=["ssh", "key"]))
        add(CatalogEntry("penelope", "lateral", "T1095",
            description="Penelope shell handler with auto-upgrade",
            priority=2, arg_template="{lport}", tags=["shell"]))
        add(CatalogEntry("rnc", "lateral", "T1095",
            description="Reverse netcat shell handler",
            priority=4, arg_template="{lport}"))
        add(CatalogEntry("wifipass", "lateral", "T1555",
            description="Extract saved WiFi passwords from host",
            priority=5, os_target="windows", tags=["wifi"]))
        add(CatalogEntry("upload_c2", "lateral", "T1105",
            description="Upload file to target via C2 channel",
            priority=3))
        add(CatalogEntry("addcli", "lateral", "T1136",
            description="Add CLI tool or implant to compromised host",
            priority=5))
        add(CatalogEntry("sshd", "lateral", "T1021",
            description="Start SSHD on compromised host for persistent access",
            priority=4, os_target="linux", tags=["ssh"]))
        add(CatalogEntry("vpn", "lateral", "T1090",
            description="Configure VPN tunnel for pivoting",
            priority=5, tags=["tunnel"]))

        # ====================================================================
        # 09. DATA EXFILTRATION
        # ====================================================================
        add(CatalogEntry("secretsdump", "exfil", "T1003",
            services=["smb", "445"],
            description="Impacket secretsdump — dump SAM/LSA/NTDS secrets",
            priority=1, requires_creds=True,
            arg_template="{domain}/{user}:{password}@{target}",
            tags=["creds", "windows", "impacket"]))
        add(CatalogEntry("evilwinrm", "exfil", "T1021",
            services=["winrm", "5985"],
            description="EvilWinRM for file download/upload and credential access",
            priority=1, requires_creds=True, tags=["winrm"]))
        add(CatalogEntry("mimikatzpy", "exfil", "T1003",
            services=["smb", "445"],
            description="Remote mimikatz via impacket for LSASS dump",
            priority=1, requires_creds=True, tags=["creds", "windows"]))
        add(CatalogEntry("getnthash_py", "exfil", "T1003",
            services=["smb", "445"],
            description="Impacket getNTHash — extract NTLM hash via RPC",
            priority=2, requires_creds=True, tags=["creds", "impacket"]))
        add(CatalogEntry("getuserspns", "exfil", "T1558",
            services=["kerberos", "88"],
            description="Impacket GetUserSPNs — Kerberoast service account hashes",
            priority=1, requires_creds=True,
            arg_template="{domain}/{user}:{password} -dc-ip {target} -request",
            tags=["kerberos", "roasting"]))
        add(CatalogEntry("getadusers", "exfil", "T1087",
            services=["ldap", "445"],
            description="Impacket GetADUsers — enumerate domain users",
            priority=2, requires_creds=True, tags=["ad", "impacket"]))
        add(CatalogEntry("dploot", "exfil", "T1555",
            services=["smb", "445"],
            description="DPAPI secret looting from Windows target",
            priority=2, requires_creds=True,
            arg_template="all -d {domain} -u {user} -p {password} -dc-ip {target}",
            tags=["dpapi", "windows"]))
        add(CatalogEntry("reg_py", "exfil", "T1012",
            services=["smb", "445"],
            description="Impacket reg.py — read SAM/SYSTEM/SECURITY registry hives",
            priority=2, requires_creds=True, tags=["registry", "impacket"]))
        add(CatalogEntry("samdump2", "exfil", "T1003",
            description="Extract password hashes from SAM and SYSTEM files",
            priority=2, os_target="linux", tags=["hash"]))
        add(CatalogEntry("adgetpass", "exfil", "T1555",
            services=["ldap", "389"],
            description="Active Directory credential extraction",
            priority=2, requires_creds=True, tags=["ad"]))
        add(CatalogEntry("gmsadumper", "exfil", "T1555",
            services=["ldap", "389"],
            description="Dump gMSA (Group Managed Service Account) passwords",
            priority=2, requires_creds=True, tags=["ad", "gmsa"]))
        add(CatalogEntry("gitdumper", "exfil", "T1213",
            services=["http", "https"],
            description="Dump exposed .git repository contents",
            priority=2, arg_template="{url}/.git/", tags=["web", "git"]))
        add(CatalogEntry("rsync", "exfil", "T1105",
            description="Rsync file exfiltration from compromised host",
            priority=3, requires_creds=True, tags=["file_transfer"]))
        add(CatalogEntry("download_c2", "exfil", "T1105",
            description="Download file from C2 server to attacker",
            priority=3))
        add(CatalogEntry("evidence", "exfil", "T1005",
            description="Collect and package evidence from target system",
            priority=4))
        add(CatalogEntry("decrypt", "exfil", "T1027",
            description="Decrypt captured encrypted files",
            priority=5))
        add(CatalogEntry("encrypt", "exfil", "T1022",
            description="Encrypt exfiltrated data for transport",
            priority=5))
        add(CatalogEntry("upload_gofile", "exfil", "T1537",
            description="Upload exfiltrated data to gofile.io (anonymous)",
            priority=5, tags=["upload"]))
        add(CatalogEntry("unzip", "exfil", "T1083",
            description="Extract password-protected archives from target",
            priority=5))

        # ====================================================================
        # 10. COMMAND & CONTROL
        # ====================================================================
        add(CatalogEntry("msfrpc", "c2", "T1095",
            description="Metasploit RPC daemon for remote API control",
            priority=1, tags=["msf"]))
        add(CatalogEntry("automsf", "c2", "T1095",
            description="Automated Metasploit exploitation and listener setup",
            priority=2, arg_template="{target}", tags=["msf"]))
        add(CatalogEntry("c2", "c2", "T1095",
            description="LazyOwn C2 console — manage active sessions",
            priority=1))
        add(CatalogEntry("empire", "c2", "T1071",
            description="PowerShell Empire C2 framework launcher",
            priority=3, os_target="windows", tags=["empire", "powershell"]))
        add(CatalogEntry("emp3r0r", "c2", "T1095",
            description="Emp3r0r Linux/Windows C2 framework",
            priority=3, tags=["c2_framework"]))
        add(CatalogEntry("sliver_server", "c2", "T1095",
            description="Sliver C2 server — mTLS/WireGuard/HTTP listeners",
            priority=2, tags=["sliver"]))
        add(CatalogEntry("caldera", "c2", "T1059",
            description="MITRE Caldera adversary emulation platform",
            priority=3, tags=["caldera", "simulation"]))
        add(CatalogEntry("atomic_agent", "c2", "T1059",
            description="Atomic Red Team agent for technique execution",
            priority=3, tags=["atomic"]))
        add(CatalogEntry("atomic_gen", "c2", "T1059",
            description="Generate Atomic Red Team test commands",
            priority=4, tags=["atomic"]))
        add(CatalogEntry("atomic_tests", "c2", "T1059",
            description="List and run Atomic Red Team tests",
            priority=4, tags=["atomic"]))
        add(CatalogEntry("generate_playbook", "c2", "T1059",
            description="Generate AI attack playbook from current session state",
            priority=3))
        add(CatalogEntry("attack_plan", "c2", "T1059",
            description="Generate structured attack plan for target",
            priority=3, arg_template="{target}"))
        add(CatalogEntry("my_playbook", "c2", "T1059",
            description="Show or execute saved custom playbook",
            priority=4))
        add(CatalogEntry("mitre_test", "c2", "T1059",
            description="Run LazyOwn MITRE ATT&CK simulation tests",
            priority=4, tags=["mitre", "simulation"]))

        # ====================================================================
        # 11. REPORTING
        # ====================================================================
        add(CatalogEntry("process_scans", "report", "T0000",
            description="Process CSV scan results into Shodan-like JSON DB",
            priority=1))
        add(CatalogEntry("vulns", "report", "T0000",
            description="Show all discovered vulnerabilities from session",
            priority=2))
        add(CatalogEntry("groq", "report", "T0000",
            description="Query Groq LLM for attack guidance or summary",
            priority=3))
        add(CatalogEntry("gpt", "report", "T0000",
            description="Query GPT for contextual attack recommendations",
            priority=4))
        add(CatalogEntry("ai_playbook", "report", "T0000",
            description="AI-generated offensive playbook from nmap/session data",
            priority=2))
        add(CatalogEntry("eyewitness", "report", "T1125",
            services=["http", "https"],
            description="Screenshot web services for visual triage",
            priority=3, arg_template="--web"))
        add(CatalogEntry("eyewitness_py", "report", "T1125",
            services=["http", "https"],
            description="Python EyeWitness web screenshot tool",
            priority=3))
        add(CatalogEntry("gowitness", "report", "T1125",
            services=["http", "https"],
            description="Go-based web screenshot tool with report",
            priority=3, arg_template="scan {url}"))
        add(CatalogEntry("extract_ports", "report", "T1046",
            description="Extract open ports from nmap/masscan output",
            priority=4))
        add(CatalogEntry("create_session_json", "report", "T0000",
            description="Create structured JSON from current session findings",
            priority=2))
        add(CatalogEntry("createjsonmachine", "report", "T0000",
            description="Create JSON host machine descriptor from session",
            priority=3))
        add(CatalogEntry("name_the_hash", "report", "T0000",
            description="Identify hash type from captured hash string",
            priority=4))
        add(CatalogEntry("pth_net", "report", "T0000",
            description="Pass-the-hash via smbclient for network enumeration",
            priority=3))
        add(CatalogEntry("banners", "report", "T0000",
            description="Collect and display service banners from session",
            priority=5))
        add(CatalogEntry("get_avaible_actions", "report", "T0000",
            description="List all available LazyOwn actions for current state",
            priority=5))

    def by_phase(self, phase: str) -> List[CatalogEntry]:
        return sorted(
            [e for e in self._entries if e.phase == phase],
            key=lambda e: e.priority,
        )

    def by_mitre(self, technique_id: str) -> List[CatalogEntry]:
        tid = technique_id.upper()
        return [e for e in self._entries if tid in e.mitre_tactic.upper()]

    def by_service(self, service_name: str) -> List[CatalogEntry]:
        svc = service_name.lower()
        return [e for e in self._entries if any(
            s.lower() in svc or svc in s.lower() for s in e.services
        )]

    def by_tag(self, tag: str) -> List[CatalogEntry]:
        return [e for e in self._entries if tag.lower() in e.tags]

    def by_os(self, os_hint: str) -> List[CatalogEntry]:
        return [e for e in self._entries if e.matches_os(os_hint)]

    def all_phases(self) -> Set[str]:
        return {e.phase for e in self._entries}

    def get(self, command: str) -> Optional[CatalogEntry]:
        for e in self._entries:
            if e.command == command:
                return e
        return None

    def count(self) -> int:
        return len(self._entries)


# ---------------------------------------------------------------------------
# Abstract selector
# ---------------------------------------------------------------------------

class AbstractSelector(ABC):

    @abstractmethod
    def select(
        self,
        catalog: CommandCatalog,
        phase: str,
        services: List[str],
        has_creds: bool,
        excluded: Set[str],
        os_hint: str = "any",
    ) -> Optional[CatalogEntry]:
        ...


# ---------------------------------------------------------------------------
# Concrete selectors
# ---------------------------------------------------------------------------

class ServiceAwareSelector(AbstractSelector):
    """Priority + service matching selector with credential gate."""

    def select(
        self,
        catalog: CommandCatalog,
        phase: str,
        services: List[str],
        has_creds: bool,
        excluded: Set[str],
        os_hint: str = "any",
    ) -> Optional[CatalogEntry]:
        candidates = catalog.by_phase(phase)
        # Pass 1: strict match — service + os + creds
        for entry in candidates:
            if entry.command in excluded:
                continue
            if entry.requires_creds and not has_creds:
                continue
            if os_hint and os_hint != "any" and not entry.matches_os(os_hint):
                continue
            if services and not entry.matches_service(services):
                continue
            return entry
        # Pass 2: relax service filter
        for entry in candidates:
            if entry.command in excluded:
                continue
            if entry.requires_creds and not has_creds:
                continue
            if os_hint and os_hint != "any" and not entry.matches_os(os_hint):
                continue
            return entry
        # Pass 3: relax everything except excluded
        for entry in candidates:
            if entry.command not in excluded:
                return entry
        return None


class MitreAlignedSelector(AbstractSelector):
    """Prefer MITRE-matching commands; fall back to ServiceAwareSelector."""

    def __init__(self, technique_id: str) -> None:
        self._tid = technique_id
        self._fallback = ServiceAwareSelector()

    def select(
        self,
        catalog: CommandCatalog,
        phase: str,
        services: List[str],
        has_creds: bool,
        excluded: Set[str],
        os_hint: str = "any",
    ) -> Optional[CatalogEntry]:
        for entry in catalog.by_mitre(self._tid):
            if entry.command in excluded:
                continue
            if entry.phase != phase:
                continue
            if entry.requires_creds and not has_creds:
                continue
            if services and not entry.matches_service(services):
                continue
            return entry
        return self._fallback.select(catalog, phase, services, has_creds, excluded, os_hint)


class TagSelector(AbstractSelector):
    """Select commands by tag (e.g. 'kerberos', 'web', 'impacket')."""

    def __init__(self, tag: str) -> None:
        self._tag = tag
        self._fallback = ServiceAwareSelector()

    def select(
        self,
        catalog: CommandCatalog,
        phase: str,
        services: List[str],
        has_creds: bool,
        excluded: Set[str],
        os_hint: str = "any",
    ) -> Optional[CatalogEntry]:
        candidates = [
            e for e in catalog.by_tag(self._tag)
            if e.phase == phase
            and e.command not in excluded
            and not (e.requires_creds and not has_creds)
        ]
        candidates.sort(key=lambda e: e.priority)
        if candidates:
            return candidates[0]
        return self._fallback.select(catalog, phase, services, has_creds, excluded, os_hint)


# ---------------------------------------------------------------------------
# Context enricher
# ---------------------------------------------------------------------------

class ContextEnricher:
    """Builds final command strings from CatalogEntry + WorldModel facts."""

    def enrich(
        self,
        entry: CatalogEntry,
        target: str,
        world_snapshot: Optional[Dict] = None,
    ) -> str:
        snapshot = world_snapshot or {}
        hosts = snapshot.get("hosts", {})
        host_info = hosts.get(target, {})
        services_dict = host_info.get("services", {})
        creds_list = snapshot.get("credentials", [])

        user, password = "", ""
        if creds_list:
            first = creds_list[0] if isinstance(creds_list[0], dict) else {}
            user = first.get("username", "")
            password = first.get("password", "")

        port = ""
        for port_str, svc_info in services_dict.items():
            if not isinstance(svc_info, dict):
                continue
            svc_name = svc_info.get("name", "").lower()
            if entry.matches_service([svc_name]):
                port = port_str
                break

        domain = snapshot.get("domain", "")
        lhost = snapshot.get("lhost", "")
        lport = snapshot.get("lport", "4444")

        return entry.build_command(
            target=target,
            port=port,
            user=user,
            password=password,
            domain=domain,
            lhost=lhost,
            lport=str(lport) if lport else "4444",
        )


# ---------------------------------------------------------------------------
# Phase mapper
# ---------------------------------------------------------------------------

class PhaseMapper:
    """Maps WorldModel EngagementPhase values to bridge phase strings."""

    # Bridge-native phase names (pass-through)
    _NATIVE: Set[str] = {"recon", "enum", "exploit", "postexp", "cred",
                         "lateral", "privesc", "persist", "exfil", "c2", "report"}

    _MAP: Dict[str, str] = {
        "recon":             "recon",
        "scanning":          "recon",
        "enumeration":       "enum",
        "exploitation":      "exploit",
        "post_exploitation": "postexp",
        "lateral_movement":  "lateral",
        "exfiltration":      "exfil",
        "reporting":         "report",
        "persistence":       "persist",
        "privilege_escalation": "privesc",
        "credential_access": "cred",
        "command_and_control": "c2",
        "completed":         "report",
        "unknown":           "recon",
        # lazyown policy category names
        "intrusion":         "exploit",
        "credential":        "cred",
        "privesc":           "privesc",
        "lateral":           "lateral",
        "exfil":             "exfil",
        "c2":                "c2",
        "report":            "report",
    }

    def to_bridge_phase(self, wm_phase: str) -> str:
        lower = wm_phase.lower()
        if lower in self._NATIVE:
            return lower
        return self._MAP.get(lower, "recon")

    def kill_chain_order(self) -> List[str]:
        """Ordered list of bridge phases following the kill chain."""
        return ["recon", "enum", "exploit", "postexp", "cred",
                "lateral", "privesc", "persist", "exfil", "c2", "report"]


# ---------------------------------------------------------------------------
# Bridge dispatcher
# ---------------------------------------------------------------------------

class BridgeDispatcher:
    """
    Public facade used by the MCP auto_loop and MCP tool handlers.
    Combines catalog + selector + enricher into a single suggest() call.
    """

    def __init__(
        self,
        catalog: Optional[CommandCatalog] = None,
        selector: Optional[AbstractSelector] = None,
        enricher: Optional[ContextEnricher] = None,
        phase_mapper: Optional[PhaseMapper] = None,
    ) -> None:
        self._catalog = catalog or CommandCatalog()
        self._selector = selector or ServiceAwareSelector()
        self._enricher = enricher or ContextEnricher()
        self._phase_mapper = phase_mapper or PhaseMapper()

    def suggest(
        self,
        phase: str,
        target: str = "",
        services: Optional[List[str]] = None,
        has_creds: bool = False,
        excluded: Optional[Set[str]] = None,
        world_snapshot: Optional[Dict] = None,
        mitre_hint: str = "",
        tag_hint: str = "",
        os_hint: str = "any",
    ) -> Optional[Tuple[str, CatalogEntry]]:
        """
        Return (command_string, entry) or None.

        Parameters
        ----------
        phase       : WorldModel or bridge phase string (auto-translated)
        target      : IP/hostname for arg substitution
        services    : discovered service strings ["http:80", "smb:445", ...]
        has_creds   : credentials known in WorldModel
        excluded    : command names to skip
        world_snapshot : WorldModel.snapshot() dict
        mitre_hint  : prefer commands matching this MITRE technique
        tag_hint    : prefer commands with this tag (e.g. "kerberos")
        os_hint     : "linux", "windows", or "any"
        """
        bridge_phase = self._phase_mapper.to_bridge_phase(phase)
        svc_list = services or []
        excl = excluded or set()

        if mitre_hint:
            selector: AbstractSelector = MitreAlignedSelector(mitre_hint)
        elif tag_hint:
            selector = TagSelector(tag_hint)
        else:
            selector = self._selector

        entry = selector.select(self._catalog, bridge_phase, svc_list,
                                has_creds, excl, os_hint)
        if entry is None:
            return None

        cmd = self._enricher.enrich(entry, target, world_snapshot)
        return cmd, entry

    def suggest_sequence(
        self,
        phase: str,
        target: str = "",
        services: Optional[List[str]] = None,
        has_creds: bool = False,
        excluded: Optional[Set[str]] = None,
        world_snapshot: Optional[Dict] = None,
        limit: int = 5,
    ) -> List[Tuple[str, CatalogEntry]]:
        """Return up to `limit` non-excluded suggestions for the phase."""
        bridge_phase = self._phase_mapper.to_bridge_phase(phase)
        candidates = self._catalog.by_phase(bridge_phase)
        svc_list = services or []
        excl = excluded or set()
        results: List[Tuple[str, CatalogEntry]] = []
        for entry in candidates:
            if len(results) >= limit:
                break
            if entry.command in excl:
                continue
            if entry.requires_creds and not has_creds:
                continue
            if svc_list and not entry.matches_service(svc_list):
                continue
            cmd = self._enricher.enrich(entry, target, world_snapshot)
            results.append((cmd, entry))
        return results

    def suggest_for_wm_phase(
        self,
        wm_phase_value: str,
        target: str = "",
        services: Optional[List[str]] = None,
        has_creds: bool = False,
        excluded: Optional[Set[str]] = None,
        world_snapshot: Optional[Dict] = None,
    ) -> Optional[Tuple[str, CatalogEntry]]:
        return self.suggest(
            phase=wm_phase_value,
            target=target,
            services=services,
            has_creds=has_creds,
            excluded=excluded,
            world_snapshot=world_snapshot,
        )

    def list_phase(self, phase: str) -> List[CatalogEntry]:
        bridge_phase = self._phase_mapper.to_bridge_phase(phase)
        return self._catalog.by_phase(bridge_phase)

    def all_phases(self) -> Set[str]:
        return self._catalog.all_phases()

    def catalog_summary(self) -> Dict[str, List[str]]:
        summary: Dict[str, List[str]] = {}
        for phase in self._phase_mapper.kill_chain_order():
            entries = self._catalog.by_phase(phase)
            if entries:
                summary[phase] = [e.command for e in entries]
        return summary

    def catalog_count(self) -> int:
        return self._catalog.count()

    def phase_kill_chain(self) -> List[str]:
        return self._phase_mapper.kill_chain_order()


# ---------------------------------------------------------------------------
# Module singleton
# ---------------------------------------------------------------------------

_dispatcher: Optional[BridgeDispatcher] = None


def get_dispatcher() -> BridgeDispatcher:
    global _dispatcher
    if _dispatcher is None:
        _dispatcher = BridgeDispatcher()
    return _dispatcher
