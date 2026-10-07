# API (page 3 of 20)
Previous: [API_p2.md](API_p2.md)

## cli/commands/privilege_escalation.py
Depends on: `cli/commands/_base.py`, `utils.py`
Imported by: `tests/test_shell_semantics.py`
- `PrivilegeEscalationCommandSet.do_smbserver` (method) `cli/commands/privilege_escalation.py:139` `def do_smbserver(self, line)` -- Stand up an Impacket SMB server with three relay variants.
- `PrivilegeEscalationCommandSet.do_responder` (method) `cli/commands/privilege_escalation.py:197` `def do_responder(self, line)` -- Run Responder on the configured ``device`` with elevated privileges.
- `PrivilegeEscalationCommandSet.do_sudo` (method) `cli/commands/privilege_escalation.py:222` `def do_sudo(self, line)` -- Re-launch the framework with root privileges when missing.
- `PrivilegeEscalationCommandSet.do_linpeas` (method) `cli/commands/privilege_escalation.py:235` `def do_linpeas(self, line)` -- Serve ``linpeas.sh`` over HTTP and print the target one-liner.
- `PrivilegeEscalationCommandSet.do_winpeas` (method) `cli/commands/privilege_escalation.py:271` `def do_winpeas(self, line)` -- Serve a winPEAS variant over HTTP and print the target one-liner.
- `PrivilegeEscalationCommandSet.do_les` (method) `cli/commands/privilege_escalation.py:310` `def do_les(self, line)` -- Run Linux Exploit Suggester against a kernel version.
- `PrivilegeEscalationCommandSet.do_suid_check` (method) `cli/commands/privilege_escalation.py:350` `def do_suid_check(self, line)` -- Print SUID/SGID enumeration commands ready to paste on the target.
- `PrivilegeEscalationCommandSet.do_pspy` (method) `cli/commands/privilege_escalation.py:369` `def do_pspy(self, line)` -- Serve the ``pspy`` process monitor over HTTP.
- `PrivilegeEscalationCommandSet.do_gtfo` (method) `cli/commands/privilege_escalation.py:403` `def do_gtfo(self, line)` -- Look up a binary in GTFOBins and LOLBas parquet knowledge bases.
- `PrivilegeEscalationCommandSet.do_whoami_priv` (method) `cli/commands/privilege_escalation.py:450` `def do_whoami_priv(self, line)` -- Print privilege enumeration commands for the target OS.
- `PrivilegeEscalationCommandSet.do_sudo_privesc` (method) `cli/commands/privilege_escalation.py:512` `def do_sudo_privesc(self, line)` -- Analyse sudo -l output and cross-reference with GTFOBins.
- `PrivilegeEscalationCommandSet.do_printspoofer` (method) `cli/commands/privilege_escalation.py:610` `def do_printspoofer(self, line)` -- Serve PrintSpoofer over HTTP for Windows privilege escalation.
- `PrivilegeEscalationCommandSet.do_juicypotato` (method) `cli/commands/privilege_escalation.py:632` `def do_juicypotato(self, line)` -- Serve JuicyPotato over HTTP for Windows privilege escalation.
- `PrivilegeEscalationCommandSet.do_privesc_cmd_by_os` (method) `cli/commands/privilege_escalation.py:754` `def do_privesc_cmd_by_os(self, line)` -- Prepare and send a linpeas/winpeas command to a C2 client.

## cli/commands/purple_team.py
Depends on: `cli/commands/_base.py`, `cli/purple_tui.py`, `core/config.py`, `modules/auto_purple.py`
- `PurpleTeamCommandSet.do_purple_exec` (method) `cli/commands/purple_team.py:144` `def do_purple_exec(self, line)` -- Execute a red action and measure if LazyOwnBT detects it.
- `PurpleTeamCommandSet.do_purple_test` (method) `cli/commands/purple_team.py:203` `def do_purple_test(self, args)` -- Test if LazyOwnBT would detect a command (no execution).
- `PurpleTeamCommandSet.do_purple_score` (method) `cli/commands/purple_team.py:223` `def do_purple_score(self, line)` -- Show current engagement detection score.
- `PurpleTeamCommandSet.do_purple_report` (method) `cli/commands/purple_team.py:271` `def do_purple_report(self, line)` -- Generate full engagement report with datasets.
- `PurpleTeamCommandSet.do_purple_methods` (method) `cli/commands/purple_team.py:285` `def do_purple_methods(self, line)` -- List available LazyOwnBT detection methods.
- `PurpleTeamCommandSet.do_purple_config` (method) `cli/commands/purple_team.py:297` `def do_purple_config(self, args)` -- Show or update purple team configuration (payload.json).
- `PurpleTeamCommandSet.do_purple_dashboard` (method) `cli/commands/purple_team.py:350` `def do_purple_dashboard(self, line)` -- Launch the Purple Team TUI dashboard.
- `PurpleTeamCommandSet.do_purple_history` (method) `cli/commands/purple_team.py:367` `def do_purple_history(self, args)` -- Show recent purple team action results.

## cli/commands/pwn.py
Depends on: `cli/commands/_base.py`, `core/safe_exec.py`, `core/validators.py`, `modules/ai_exploit_chain.py`, `modules/autonomous_exploit_engine.py`, `modules/dashboard_engine.py`, `modules/exploit_recommender.py`, `modules/rich_tui.py`, `modules/world_model.py`, `utils.py`
Imported by: `contrib/legacy/lazybinenc.py`, `contrib/legacy/lazypwn.py`, `contrib/legacy/lazyvsftp.py`, `contrib/legacy/sql.py`
- `PwnCommandSet.do_auto_pwn` (method) `cli/commands/pwn.py:35` `def do_auto_pwn(self, line)` -- Run the full autonomous exploitation chain against the target.
- `PwnCommandSet.do_rich_tui` (method) `cli/commands/pwn.py:99` `def do_rich_tui(self, line)` -- Launch the Rich-based live dashboard TUI.
- `PwnCommandSet.do_exploit_chain` (method) `cli/commands/pwn.py:148` `def do_exploit_chain(self, line)` -- AI-driven multi-step exploit chaining with fallback strategies.
- `PwnCommandSet.do_lolbas_list` (method) `cli/commands/pwn.py:235` `def do_lolbas_list(self, line)` -- List available LOLBAS (Living Off The Land) techniques from plugins.
- `PwnCommandSet.do_lolbas_use` (method) `cli/commands/pwn.py:292` `def do_lolbas_use(self, line)` -- Execute a specific LOLBAS technique.
- `PwnCommandSet.do_stealth_on` (method) `cli/commands/pwn.py:384` `def do_stealth_on(self, line)` -- Enable stealth mode for subsequent operations.
- `PwnCommandSet.do_stealth_off` (method) `cli/commands/pwn.py:412` `def do_stealth_off(self, line)` -- Disable stealth mode.

## cli/commands/recon.py
Depends on: `cli/commands/_base.py`, `cli/exploit_advisor.py`, `cli/lazynmap_post.py`, `core/console.py`, `modules/intelligence_engine.py`, `utils.py`
- `ReconCommandSet.do_batchnmap` (method) `cli/commands/recon.py:47` `def do_batchnmap(self, line)` -- Runs the internal module `modules/lazynmap.sh` for multiple Nmap scans.
- `ReconCommandSet.do_lazynmap` (method) `cli/commands/recon.py:74` `def do_lazynmap(self, line)` -- Runs the internal module `modules/lazynmap.sh` with target mode.
- `ReconCommandSet.do_dig` (method) `cli/commands/recon.py:154` `def do_dig(self, line)` -- Executes the `dig` command to query DNS information.
- `ReconCommandSet.do_dnsenum` (method) `cli/commands/recon.py:186` `def do_dnsenum(self, line)` -- Performs DNS enumeration using `dnsenum` to identify subdomains for a given domain.
- `ReconCommandSet.do_dnsmap` (method) `cli/commands/recon.py:222` `def do_dnsmap(self, line)` -- Performs DNS enumeration using `dnsmap` to discover subdomains for a specified domain.
- `ReconCommandSet.do_whatweb` (method) `cli/commands/recon.py:255` `def do_whatweb(self, line)` -- Performs a web technology fingerprinting scan using `whatweb`.
- `ReconCommandSet.do_nbtscan` (method) `cli/commands/recon.py:292` `def do_nbtscan(self, line)` -- Performs network scanning using `nbtscan` to discover NetBIOS names and addresses in a specified range.
- `ReconCommandSet.do_nikto` (method) `cli/commands/recon.py:320` `def do_nikto(self, line)` -- Runs the `nikto` tool to perform a web server vulnerability scan against the specified target host.
- `ReconCommandSet.do_finalrecon` (method) `cli/commands/recon.py:429` `def do_finalrecon(self, line)` -- Runs the `finalrecon` tool to perform a web server vulnerability scan against the specified target host.
- `ReconCommandSet.do_openssl_sclient` (method) `cli/commands/recon.py:461` `def do_openssl_sclient(self, line)` -- Uses `openssl s_client` to connect to a specified host and port, allowing for testing and debugging of SSL/TLS...
- `ReconCommandSet.do_ss` (method) `cli/commands/recon.py:491` `def do_ss(self, line)` -- Search all exploit sources and map findings to the next LazyOwn command.
- `ReconCommandSet.do_wfuzz` (method) `cli/commands/recon.py:654` `def do_wfuzz(self, line)` -- Uses `wfuzz` to perform fuzzing based on provided parameters.

## cli/commands/recon_migrated.py
Depends on: `cli/aliases.py`, `cli/assign.py`, `cli/commands/_base.py`, `cli/surface_tui.py`, `core/config.py`, `utils.py`
- `ReconMigratedCommandSet.do_surface` (method) `cli/commands/recon_migrated.py:43` `def do_surface(self, line)` -- Render the network surface graph in the terminal.
- `ReconMigratedCommandSet.do_getcap` (method) `cli/commands/recon_migrated.py:97` `def do_getcap(self, line)` -- Retrieve and display file capabilities on the system.
- `ReconMigratedCommandSet.do_launchpad` (method) `cli/commands/recon_migrated.py:131` `def do_launchpad(self, line)` -- Searches for packages on Launchpad based on the provided search term and extracts codenames from the results.
- `ReconMigratedCommandSet.do_ping` (method) `cli/commands/recon_migrated.py:177` `def do_ping(self, line)` -- Perform a ping to check host availability and infer the operating system based on TTL values.
- `ReconMigratedCommandSet.do_gospider` (method) `cli/commands/recon_migrated.py:275` `def do_gospider(self, line)` -- Try gospider for web spidering.
- `ReconMigratedCommandSet.do_proxy` (method) `cli/commands/recon_migrated.py:363` `def do_proxy(self, line)` -- Runs a small proxy server to modify HTTP requests on the fly.
- `ReconMigratedCommandSet.do_ports` (method) `cli/commands/recon_migrated.py:401` `def do_ports(self, line)` -- Lists all open TCP and UDP ports on the local system.
- `ReconMigratedCommandSet.do_tcpdump_icmp` (method) `cli/commands/recon_migrated.py:443` `def do_tcpdump_icmp(self, line)` -- Starts `tcpdump` to capture ICMP traffic on the specified interface.
- `ReconMigratedCommandSet.do_tcpdump_capture` (method) `cli/commands/recon_migrated.py:476` `def do_tcpdump_capture(self, line)` -- Starts packet capture using `tcpdump` on the specified interface.
- `ReconMigratedCommandSet.do_tshark_analyze` (method) `cli/commands/recon_migrated.py:517` `def do_tshark_analyze(self, line)` -- Analyzes a packet capture file using `tshark` based on the provided remote host IP.
- `ReconMigratedCommandSet.do_waybackmachine` (method) `cli/commands/recon_migrated.py:583` `def do_waybackmachine(self, line)` -- Fetch URLs from the Wayback Machine for a given website.
- `ReconMigratedCommandSet.do_sslscan` (method) `cli/commands/recon_migrated.py:623` `def do_sslscan(self, line)` -- Run an SSL scan on the specified remote host.
- `ReconMigratedCommandSet.do_graudit` (method) `cli/commands/recon_migrated.py:664` `def do_graudit(self, line)` -- Executes the graudit command to perform a static code analysis with the specified options.
- `ReconMigratedCommandSet.do_sherlock` (method) `cli/commands/recon_migrated.py:695` `def do_sherlock(self, line)` -- Executes the Sherlock tool to find usernames across social networks.
- `ReconMigratedCommandSet.do_trufflehog` (method) `cli/commands/recon_migrated.py:736` `def do_trufflehog(self, line)` -- Executes trufflehog to search for secrets in a given Git repository URL.
- `ReconMigratedCommandSet.do_apache_users` (method) `cli/commands/recon_migrated.py:774` `def do_apache_users(self, line)` -- Performs enumeration of users from a target system using `apache-users`.
- `ReconMigratedCommandSet.do_trace` (method) `cli/commands/recon_migrated.py:821` `def do_trace(self, line)` -- Traces the DNS information for a given self.params['domain'] using the FreeDNS service.
- `ReconMigratedCommandSet.do_alterx` (method) `cli/commands/recon_migrated.py:864` `def do_alterx(self, line)` -- Executes the 'alterx' command for subdomain enumeration on the provided self.params['domain'].
- `ReconMigratedCommandSet.do_windapsearchscrapeusers` (method) `cli/commands/recon_migrated.py:941` `def do_windapsearchscrapeusers(self, line)` -- Extracts usernames from a JSON output generated by go-windapsearch and appends them to the file sessions/users.txt.
- `ReconMigratedCommandSet.do_cve` (method) `cli/commands/recon_migrated.py:977` `def do_cve(self, line)` -- Search for a CVE using the CIRCL API.
- `ReconMigratedCommandSet.do_serveralive2` (method) `cli/commands/recon_migrated.py:1026` `def do_serveralive2(self, line)` -- Command serveralive2: Uses Impacket to connect to a remote MSRPC interface and retrieves the server bindings.
- `ReconMigratedCommandSet.do_binarycheck` (method) `cli/commands/recon_migrated.py:1060` `def do_binarycheck(self, line)` -- Performs various checks on a selected binary to gather information and protections.
- `ReconMigratedCommandSet.do_dnstool_py` (method) `cli/commands/recon_migrated.py:1105` `def do_dnstool_py(self, line)` -- Executes the dnstool.py tool to modify Active Directory-integrated DNS records.
- `ReconMigratedCommandSet.do_metabigor` (method) `cli/commands/recon_migrated.py:1151` `def do_metabigor(self, line)` -- Executes Metabigor commands for OSINT and scanning tasks with guided input or predefined arguments.
- `ReconMigratedCommandSet.do_httprobe` (method) `cli/commands/recon_migrated.py:1227` `def do_httprobe(self, line)` -- Executes the httprobe tool to probe domains for working HTTP and HTTPS servers.
- `ReconMigratedCommandSet.do_recon` (method) `cli/commands/recon_migrated.py:1270` `def do_recon(self, line)` -- Performs reconnaissance on a specified self.params['domain'] using crt.sh (the target must be visible on internet)...
- `ReconMigratedCommandSet.do_dnschef` (method) `cli/commands/recon_migrated.py:1324` `def do_dnschef(self, line)` -- Executes the DNSChef tool to monitor DNS queries and intercept responses.
- `ReconMigratedCommandSet.do_ipinfo` (method) `cli/commands/recon_migrated.py:1359` `def do_ipinfo(self, line)` -- Retrieves detailed information about an IP address using the ARIN API.

## cli/commands/redteam_gym.py
Depends on: `cli/commands/_base.py`, `modules/redteam_gym.py`, `utils.py`
- `RedTeamGymCommandSet.do_gym` (method) `cli/commands/redteam_gym.py:39` `def do_gym(self, line)` -- Red Team Gym — gamified pentest training with ELO scoring.

## cli/commands/resource_scripting.py
Depends on: `cli/commands/_base.py`, `modules/resource_script.py`, `utils.py`
- `ResourceCommandSet.on_cmd` (method) `cli/commands/resource_scripting.py:35` `def on_cmd(cmd)`
- `ResourceCommandSet.on_print` (method) `cli/commands/resource_scripting.py:39` `def on_print(msg)`
- `ResourceCommandSet.do_resource` (method) `cli/commands/resource_scripting.py:49` `def do_resource(self, line)` -- Run an enhanced resource script.
- `ResourceCommandSet.do_makerc` (method) `cli/commands/resource_scripting.py:88` `def do_makerc(self, line)` -- Record session commands to a resource script.
- `ResourceCommandSet.do_spool` (method) `cli/commands/resource_scripting.py:122` `def do_spool(self, line)` -- Log session output to a file.
- `ResourceCommandSet.do_mkrc` (method) `cli/commands/resource_scripting.py:152` `def do_mkrc(self, line)` -- Alias for makerc — record commands to a script.

## cli/commands/scan.py
Depends on: `cli/commands/_base.py`, `utils.py`
- `ScanCommandSet.do_gobuster` (method) `cli/commands/scan.py:56` `def do_gobuster(self, line)` -- Uses `gobuster` for directory and virtual host fuzzing based on provided parameters.
- `ScanCommandSet.do_arpscan` (method) `cli/commands/scan.py:129` `def do_arpscan(self, line)` -- Executes an ARP scan using `arp-scan`.
- `ScanCommandSet.do_dirsearch` (method) `cli/commands/scan.py:170` `def do_dirsearch(self, line)` -- Runs the `dirsearch` tool to perform directory and file enumeration on a specified URL.
- `ScanCommandSet.do_dmitry` (method) `cli/commands/scan.py:213` `def do_dmitry(self, line)` -- This function constructs and executes a command for the 'dmitry' tool.
- `ScanCommandSet.do_feroxbuster` (method) `cli/commands/scan.py:248` `def do_feroxbuster(self, line)` -- Command feroxbuster: Installs and runs Feroxbuster for performing forced browsing and directory brute-forcing.
- `ScanCommandSet.do_nmapscript` (method) `cli/commands/scan.py:316` `def do_nmapscript(self, line)` -- Perform an Nmap scan using a specified script and port.
- `ScanCommandSet.do_nuclei` (method) `cli/commands/scan.py:350` `def do_nuclei(self, line)` -- Executes a Nuclei scan on a specified target URL or host.
- `ScanCommandSet.do_amass` (method) `cli/commands/scan.py:392` `def do_amass(self, line)` -- Executes Amass to perform a passive enumeration on a given domain.
- `ScanCommandSet.do_bbot` (method) `cli/commands/scan.py:422` `def do_bbot(self, line)` -- Executes a BBOT scan to perform various reconnaissance tasks.
- `ScanCommandSet.do_osmedeus` (method) `cli/commands/scan.py:473` `def do_osmedeus(self, line)` -- Executes Osmedeus scans with guided input for various scanning scenarios.
- `ScanCommandSet.do_magicrecon` (method) `cli/commands/scan.py:548` `def do_magicrecon(self, line)` -- Command magicrecon: Automates the setup and usage of MagicRecon to perform various types of reconnaissance and...
- `ScanCommandSet.do_hostdiscover` (method) `cli/commands/scan.py:606` `def do_hostdiscover(self, line)` -- Discover active hosts in a subnet by performing a ping sweep.
- `ScanCommandSet.do_portdiscover` (method) `cli/commands/scan.py:664` `def do_portdiscover(self, line)` -- Scan all ports on a specified host to identify open ports.
- `ScanCommandSet.do_portservicediscover` (method) `cli/commands/scan.py:724` `def do_portservicediscover(self, line)` -- Scan all ports on a specified host to identify open ports and associated services.
- `ScanCommandSet.do_skipfish` (method) `cli/commands/scan.py:789` `def do_skipfish(self, line)` -- This function executes the web security scanning tool Skipfish using the provided configuration and parameters.
- `ScanCommandSet.do_vscan` (method) `cli/commands/scan.py:839` `def do_vscan(self, line)` -- Perform port scanning using vscan with the provided parameters.

## cli/commands/scan_migrated.py
Depends on: `cli/commands/_base.py`, `utils.py`
- `ScanMigratedCommandSet.do_cme` (method) `cli/commands/scan_migrated.py:33` `def do_cme(self, line)` -- Execute CrackMapExec (CME) for SMB enumeration and authentication attempts against a target.
- `ScanMigratedCommandSet.do_ldapdomaindump` (method) `cli/commands/scan_migrated.py:159` `def do_ldapdomaindump(self, line)` -- Dumps LDAP information using `ldapdomaindump` with credentials from a file.
- `ScanMigratedCommandSet.do_bloodhound` (method) `cli/commands/scan_migrated.py:206` `def do_bloodhound(self, line)` -- Perform LDAP enumeration using bloodhound-python with credentials from a file.
- `ScanMigratedCommandSet.do_swaks` (method) `cli/commands/scan_migrated.py:255` `def do_swaks(self, line)` -- Sends an email using `swaks` (Swiss Army Knife for SMTP).
- `ScanMigratedCommandSet.do_samrdump` (method) `cli/commands/scan_migrated.py:300` `def do_samrdump(self, line)` -- Run `impacket-samrdump` to dump SAM data from specified ports.
- `ScanMigratedCommandSet.do_lynis` (method) `cli/commands/scan_migrated.py:355` `def do_lynis(self, line)` -- Performs a Lynis audit on the specified remote system.
- `ScanMigratedCommandSet.do_snmpcheck` (method) `cli/commands/scan_migrated.py:384` `def do_snmpcheck(self, line)` -- Performs an SNMP check on the specified target host.
- `ScanMigratedCommandSet.do_snmpwalk` (method) `cli/commands/scan_migrated.py:411` `def do_snmpwalk(self, line)` -- Performs an SNMP check on the specified target host.
- `ScanMigratedCommandSet.do_smtpuserenum` (method) `cli/commands/scan_migrated.py:438` `def do_smtpuserenum(self, line)` -- Enumerates SMTP users using the `smtp-user-enum` tool with the VRFY method.
- `ScanMigratedCommandSet.do_sessionssh` (method) `cli/commands/scan_migrated.py:477` `def do_sessionssh(self, line)` -- Execute a command to list active SSH connections.
- `ScanMigratedCommandSet.do_smbattack` (method) `cli/commands/scan_migrated.py:501` `def do_smbattack(self, line)` -- Scans for hosts with SMB service open on port 445 in the specified target network.
- `ScanMigratedCommandSet.find_tgts` (method) `cli/commands/scan_migrated.py:530` `def find_tgts(subnet)` -- Finds and returns a list of target hosts with port 445 open in the specified subnet.
- `ScanMigratedCommandSet.setup_handler` (method) `cli/commands/scan_migrated.py:551` `def setup_handler(config_file, lhost, lport)` -- Sets up a Metasploit multi/handler configuration in the given config file.
- `ScanMigratedCommandSet.conficker_exploit` (method) `cli/commands/scan_migrated.py:571` `def conficker_exploit(config_file, host, lhost, lport)` -- Configures and writes a Metasploit exploit for the Conficker vulnerability to the given config file.
- `ScanMigratedCommandSet.smb_brute` (method) `cli/commands/scan_migrated.py:591` `def smb_brute(config_file, host, passwd_file, lhost, lport)` -- Configures and writes a Metasploit SMB brute force exploit for the given host to the provided config file.
- `ScanMigratedCommandSet.do_parsero` (method) `cli/commands/scan_migrated.py:632` `def do_parsero(self, line)` -- Executes a parsero scan on a specified target URL or host.
- `ScanMigratedCommandSet.do_changeme` (method) `cli/commands/scan_migrated.py:664` `def do_changeme(self, line)` -- Executes a changeme scan on a specified target URL or host.
- `ScanMigratedCommandSet.do_enum4linux_ng` (method) `cli/commands/scan_migrated.py:695` `def do_enum4linux_ng(self, line)` -- Performs enumeration of information from a target system using `enum4linux-ng`.
- `ScanMigratedCommandSet.do_fuzz` (method) `cli/commands/scan_migrated.py:733` `def do_fuzz(self, line)` -- Executes a web server fuzzing script with user-provided parameters.
- `ScanMigratedCommandSet.do_kerbrute` (method) `cli/commands/scan_migrated.py:778` `def do_kerbrute(self, line)` -- Executes the Kerbrute tool to enumerate user accounts against a specified target self.params['domain'] controller.
- `ScanMigratedCommandSet.do_davtest` (method) `cli/commands/scan_migrated.py:864` `def do_davtest(self, line)` -- Tests WebDAV server configurations using `davtest`.
- `ScanMigratedCommandSet.do_evil_ssdp` (method) `cli/commands/scan_migrated.py:906` `def do_evil_ssdp(self, line)` -- Runs evil-ssdp with various options and user-selected templates.
- `ScanMigratedCommandSet.do_netexec` (method) `cli/commands/scan_migrated.py:952` `def do_netexec(self, line)` -- Executes netexec with various options for network protocol operations.
- `ScanMigratedCommandSet.install_netexec` (method) `cli/commands/scan_migrated.py:978` `def install_netexec()`
- `ScanMigratedCommandSet.install_netexec_pipx` (method) `cli/commands/scan_migrated.py:983` `def install_netexec_pipx()`
- `ScanMigratedCommandSet.do_allin` (method) `cli/commands/scan_migrated.py:1172` `def do_allin(self, line)` -- Execute the AlliN.py tool with various scan modes and parameters.
- `ScanMigratedCommandSet.do_windapsearch` (method) `cli/commands/scan_migrated.py:1245` `def do_windapsearch(self, line)` -- Execute the windapsearch tool to perform Active Directory Domain enumeration through LDAP queries.
- `ScanMigratedCommandSet.do_ldapsearch` (method) `cli/commands/scan_migrated.py:1359` `def do_ldapsearch(self, line)` -- Executes an LDAP search against a target remote host (self.params['rhost']) and saves the results.
- `ScanMigratedCommandSet.do_arjun` (method) `cli/commands/scan_migrated.py:1411` `def do_arjun(self, line)` -- Executes an Arjun scan on the specified URL for parameter discovery.
- `ScanMigratedCommandSet.do_finger_user_enum` (method) `cli/commands/scan_migrated.py:1476` `def do_finger_user_enum(self, line)` -- Executes the `finger-user-enum` tool for enumerating users on the target host.
- `ScanMigratedCommandSet.do_wpscan` (method) `cli/commands/scan_migrated.py:1524` `def do_wpscan(self, line)` -- Command wpscan: Installs and runs WPScan to perform WordPress vulnerability scanning.
- `ScanMigratedCommandSet.do_loxs` (method) `cli/commands/scan_migrated.py:1580` `def do_loxs(self, line)` -- Command loxs: Installs and runs Loxs for multi-vulnerability web application scanning.
- `ScanMigratedCommandSet.do_blazy` (method) `cli/commands/scan_migrated.py:1624` `def do_blazy(self, line)` -- Command blazy: Installs and runs blazy for multi-vulnerability web application scanning.
- `ScanMigratedCommandSet.do_parth` (method) `cli/commands/scan_migrated.py:1674` `def do_parth(self, line)` -- Command parth: Installs and runs Parth for discovering vulnerable URLs and parameters.
- `ScanMigratedCommandSet.do_breacher` (method) `cli/commands/scan_migrated.py:1733` `def do_breacher(self, line)` -- Command breacher: Installs and runs Breacher for finding admin login pages and EAR vulnerabilities.
- `ScanMigratedCommandSet.do_openredirex` (method) `cli/commands/scan_migrated.py:1795` `def do_openredirex(self, line)` -- Command openredirex: Clones, installs, and runs OpenRedirex for testing open redirection vulnerabilities.
- `ScanMigratedCommandSet.do_odat` (method) `cli/commands/scan_migrated.py:1858` `def do_odat(self, line)` -- Command odat: Runs the ODAT sidguesser module to guess Oracle SIDs on a target Oracle database.
- `ScanMigratedCommandSet.do_rpcmap_py` (method) `cli/commands/scan_migrated.py:1971` `def do_rpcmap_py(self, line)` -- Command rpcmap_py: Executes rpcmap.py commands to enumerate MSRPC interfaces.
- `ScanMigratedCommandSet.do_pykerbrute` (method) `cli/commands/scan_migrated.py:2015` `def do_pykerbrute(self, line)` -- Command pykerbrute: Automates the installation and execution of PyKerbrute for bruteforcing Active Directory...
- `ScanMigratedCommandSet.do_netview` (method) `cli/commands/scan_migrated.py:2080` `def do_netview(self, line)` -- Executes the Impacket netview tool to list network shares on a specified target.
- `ScanMigratedCommandSet.do_rdp_check_py` (method) `cli/commands/scan_migrated.py:2144` `def do_rdp_check_py(self, line)` -- Executes the RDP check tool to verify credentials or hash-based authentication on a target system.
- `ScanMigratedCommandSet.do_mqtt_check_py` (method) `cli/commands/scan_migrated.py:2209` `def do_mqtt_check_py(self, line)` -- Executes the MQTT check tool to verify credentials on a target system with optional SSL.
- `ScanMigratedCommandSet.do_lookupsid_py` (method) `cli/commands/scan_migrated.py:2264` `def do_lookupsid_py(self, line)` -- Executes the LookupSID tool to perform SID enumeration on a target system.
- `ScanMigratedCommandSet.do_lookupsid` (method) `cli/commands/scan_migrated.py:2335` `def do_lookupsid(self, line)` -- Executes the Impacket lookupsid tool to enumerate SIDs on a target system.
- `ScanMigratedCommandSet.do_certipy_ad` (method) `cli/commands/scan_migrated.py:2397` `def do_certipy_ad(self, line)` -- Run certipy-ad against Active Directory Certificate Services.
- `ScanMigratedCommandSet.do_certipy` (method) `cli/commands/scan_migrated.py:2462` `def do_certipy(self, line)` -- Executes the Certipy tool to interact with Active Directory Certificate Services.
- `ScanMigratedCommandSet.do_sawks` (method) `cli/commands/scan_migrated.py:2545` `def do_sawks(self, line)` -- Executes the Swaks (Swiss Army Knife for SMTP) tool to send test emails for phishing simulations.
- `ScanMigratedCommandSet.do_ad_ldap_enum` (method) `cli/commands/scan_migrated.py:2582` `def do_ad_ldap_enum(self, line)` -- Executes ad-ldap-enum to enumerate Active Directory objects (users, groups, computers) through LDAP, collecting...
- `ScanMigratedCommandSet.do_net_rpc_addmem` (method) `cli/commands/scan_migrated.py:2636` `def do_net_rpc_addmem(self, line)` -- Executes the net rpc group addmem command to add a user to a specified group in Active Directory.
- `ScanMigratedCommandSet.do_pre2k` (method) `cli/commands/scan_migrated.py:2682` `def do_pre2k(self, line)` -- Executes the pre2k tool to query the self.params['domain'] for pre-Windows 2000 machine accounts or to pass a list...
- `ScanMigratedCommandSet.do_hound` (method) `cli/commands/scan_migrated.py:2778` `def do_hound(self, line)` -- Executes the hound tool for Hound is a simple and light tool for information gathering and capture exact GPS coordinates

## cli/commands/security.py
Depends on: `cli/commands/_base.py`, `core/config.py`, `core/console.py`, `core/credential_vault.py`, `modules/hash_cracker.py`, `modules/opsec_scorer.py`
- `SecurityCommandSet.do_opsec` (method) `cli/commands/security.py:26` `def do_opsec(self, line)` -- Score OPSEC risk for a LazyOwn command before execution.
- `SecurityCommandSet.do_seal_credentials` (method) `cli/commands/security.py:106` `def do_seal_credentials(self, _line)` -- Encrypt all sensitive values in payload.json using AES-256-GCM.
- `SecurityCommandSet.do_rotate_aes` (method) `cli/commands/security.py:127` `def do_rotate_aes(self, _line)` -- Generate a new AES key and re-encrypt all sealed credentials.
- `SecurityCommandSet.do_unseal_credentials` (method) `cli/commands/security.py:150` `def do_unseal_credentials(self, _line)` -- Decrypt sealed credential values in payload.json for inspection.
- `SecurityCommandSet.do_crack_hashes` (method) `cli/commands/security.py:170` `def do_crack_hashes(self, line)` -- Crack password hashes from a file using John the Ripper or Hashcat.
- `SecurityCommandSet.complete_opsec` (method) `cli/commands/security.py:267` `def complete_opsec(self, text, line, begidx, endidx)`
- `SecurityCommandSet.complete_crack_hashes` (method) `cli/commands/security.py:276` `def complete_crack_hashes(self, text, line, begidx, endidx)`

## cli/commands/session_ops.py
Depends on: `cli/aliases.py`, `cli/assign.py`, `cli/autosuggest.py`, `cli/chain_mode.py`, `cli/commands/_base.py`, `cli/config_history.py`, `cli/ops_commands.py`, `cli/session_resumer.py`, `cli/show.py`, `core/config.py`, `modules/autonomous_exploit_engine.py`, `modules/lazy_rbac.py`, `modules/module_registry.py`, `modules/payload_factory.py`, `modules/pipeline_engine.py`, `skills/autonomous_daemon.py`, `utils.py`
Imported by: `tests/test_session_ops_command_set.py`
- `SessionOpsCommandSet.do_note` (method) `cli/commands/session_ops.py:79` `def do_note(self, line)` -- Capture a quick operator note attached to the current target and phase.
- `SessionOpsCommandSet.do_l00t` (method) `cli/commands/session_ops.py:104` `def do_l00t(self, line)` -- Unified loot: show, search, reuse, graph, and mark credentials.
- `SessionOpsCommandSet.do_loot` (method) `cli/commands/session_ops.py:155` `def do_loot(self, line)` -- Alias for ``l00t`` — unified loot (show/search/reuse/graph/mark).
- `SessionOpsCommandSet.do_pivot` (method) `cli/commands/session_ops.py:163` `def do_pivot(self, line)` -- Record a newly discovered pivot target or show the pivot chain.
- `SessionOpsCommandSet.do_tasks` (method) `cli/commands/session_ops.py:188` `def do_tasks(self, line)` -- View and manage the task queue from sessions/tasks.json.
- `SessionOpsCommandSet.do_scans` (method) `cli/commands/session_ops.py:221` `def do_scans(self, line)` -- List nmap scan files in sessions/ with age, size, and open ports.
- `SessionOpsCommandSet.do_sitrep` (method) `cli/commands/session_ops.py:238` `def do_sitrep(self, line)` -- Print a unified operational situation report.
- `SessionOpsCommandSet.do_assign` (method) `cli/commands/session_ops.py:255` `def do_assign(self, line)` -- assign a parameter value, persist to payload.json and refresh aliases.
- `SessionOpsCommandSet.do_tenant` (method) `cli/commands/session_ops.py:307` `def do_tenant(self, line)` -- Manage multi-tenancy: list, switch, or create engagement tenants.
- `SessionOpsCommandSet.do_scope` (method) `cli/commands/session_ops.py:380` `def do_scope(self, line)` -- Manage the authorized engagement scope and the scope-guard posture.
- `SessionOpsCommandSet.do_show` (method) `cli/commands/session_ops.py:446` `def do_show(self, line)` -- Show params, modules, payloads, or active module options.
- `SessionOpsCommandSet.do_list` (method) `cli/commands/session_ops.py:520` `def do_list(self, line)` -- Lists all available scripts in the modules directory.
- `SessionOpsCommandSet.do_run` (method) `cli/commands/session_ops.py:555` `def do_run(self, line)` -- Runs a specific LazyOwn script or active module.
- `SessionOpsCommandSet.do_payload` (method) `cli/commands/session_ops.py:594` `def do_payload(self, line)` -- Load parameters from a specified payload JSON file.
- `SessionOpsCommandSet.do_next` (method) `cli/commands/session_ops.py:645` `def do_next(self, line)` -- Show next-step recommendations or execute the active autosuggest.
- `SessionOpsCommandSet.do_chainmode` (method) `cli/commands/session_ops.py:689` `def do_chainmode(self, line)` -- Toggle interactive kill-chain chaining after every command.
- `SessionOpsCommandSet.do_engage` (method) `cli/commands/session_ops.py:740` `def do_engage(self, line)` -- Drive a single target through the full kill-chain in one command.
- `SessionOpsCommandSet.do_pipeline` (method) `cli/commands/session_ops.py:868` `def do_pipeline(self, line)` -- Declarative composition layer: run a YAML pipeline of LazyOwn commands.
- `SessionOpsCommandSet.do_lazyscript` (method) `cli/commands/session_ops.py:961` `def do_lazyscript(self, line)` -- Executes commands defined in a lazyscript file.
- `SessionOpsCommandSet.do_hunt` (method) `cli/commands/session_ops.py:993` `def do_hunt(self, line)` -- Run an autonomous exploitation chain against a target.
- `SessionOpsCommandSet.do_resume` (method) `cli/commands/session_ops.py:1074` `def do_resume(self, line)` -- Browse previous sessions and load a target from a past engagement.
- `SessionOpsCommandSet.do_getseclist` (method) `cli/commands/session_ops.py:1094` `def do_getseclist(self, line)` -- Get the SecLists wordlist from GitHub.
- `SessionOpsCommandSet.do_download_resources` (method) `cli/commands/session_ops.py:1132` `def do_download_resources(self, line)` -- Downloads resources into the `sessions` directory.
- `SessionOpsCommandSet.do_collab_join` (method) `cli/commands/session_ops.py:1165` `def do_collab_join(self, line)` -- Print the multi-operator collaboration join URL and SSE endpoint.
- `SessionOpsCommandSet.do_kick` (method) `cli/commands/session_ops.py:1196` `def do_kick(self, line)` -- Handles the process of sending a spoofed ARP packet to a specified IP address with a given MAC address.
- `SessionOpsCommandSet.do_qa` (method) `cli/commands/session_ops.py:1243` `def do_qa(self, line)` -- Exits the application quickly without confirmation.
- `SessionOpsCommandSet.do_clock` (method) `cli/commands/session_ops.py:1284` `def do_clock(self, line)` -- Displays the current date and time, and runs a custom shell script.
- `SessionOpsCommandSet.do_gencert` (method) `cli/commands/session_ops.py:1332` `def do_gencert(self, line)` -- Generates a certificate authority (CA), client certificate, and client key.
- `SessionOpsCommandSet.do_load_session` (method) `cli/commands/session_ops.py:1344` `def do_load_session(self, line)` -- Load the session from the sessionLazyOwn.json file and display the status of various parameters.
- `SessionOpsCommandSet.do_clone_site` (method) `cli/commands/session_ops.py:1395` `def do_clone_site(self, line)` -- Clone a website and serve the files in sessions/{url_cloned}.
- `SessionOpsCommandSet.do_msfshellcoder` (method) `cli/commands/session_ops.py:1439` `def do_msfshellcoder(self, line)` -- Generate shellcode in C format using msfvenom for either a custom command or a reverse shell payload.

## cli/commands/shellsys.py
Depends on: `cli/commands/_base.py`, `core/safe_exec.py`, `utils.py`
Imported by: `tests/test_shellsys_command_set.py`
- `ShellSysCommandSet.do_sh` (method) `cli/commands/shellsys.py:30` `def do_sh(self, line)` -- Executes a shell command directly from the LazyOwn interface.
- `ShellSysCommandSet.do_sys` (method) `cli/commands/shellsys.py:62` `def do_sys(self, line)` -- Executes a shell command directly from the LazyOwn interface.
- `ShellSysCommandSet.do_pwd` (method) `cli/commands/shellsys.py:110` `def do_pwd(self, line)` -- Displays the current working directory and lists files, and copies the current directory path to the clipboard.
- `ShellSysCommandSet.do_nano` (method) `cli/commands/shellsys.py:148` `def do_nano(self, line)` -- Opens or creates the file using line in the sessions directory for editing using nano.
- `ShellSysCommandSet.do_cron` (method) `cli/commands/shellsys.py:172` `def do_cron(self, line)` -- Schedules a command to run at a specified time.
- `ShellSysCommandSet.lazyrun_command` (method) `cli/commands/shellsys.py:207` `def lazyrun_command()`
- `ShellSysCommandSet.do_clean` (method) `cli/commands/shellsys.py:218` `def do_clean(self, line)` -- Deletes files and directories in the `sessions` directory, excluding specified files and directories.
- `ShellSysCommandSet.do_fixperm` (method) `cli/commands/shellsys.py:305` `def do_fixperm(self, line)` -- Fix permissions for LazyOwn shell scripts.
- `ShellSysCommandSet.do_fixel` (method) `cli/commands/shellsys.py:338` `def do_fixel(self, line)` -- Fixes file permissions and line endings in the project directories.
- `ShellSysCommandSet.do_pop` (method) `cli/commands/shellsys.py:371` `def do_pop(self, line)` -- Open a centered popup in the current tmux session to execute a shell command.
- `ShellSysCommandSet.do_tab` (method) `cli/commands/shellsys.py:408` `def do_tab(self, line)` -- Executes the `lazypyautogui.py` script with optional arguments.

## cli/commands/sleep_obfuscation.py
Depends on: `cli/commands/_base.py`, `modules/sleep_obfuscation.py`, `utils.py`
- `SleepObfuscationCommandSet.do_sleep_list` (method) `cli/commands/sleep_obfuscation.py:23` `def do_sleep_list(self, line)` -- List available sleep obfuscation techniques.
- `SleepObfuscationCommandSet.do_sleep_info` (method) `cli/commands/sleep_obfuscation.py:50` `def do_sleep_info(self, line)` -- Show detailed information about a sleep obfuscation technique.
- `SleepObfuscationCommandSet.do_sleep_configure` (method) `cli/commands/sleep_obfuscation.py:82` `def do_sleep_configure(self, line)` -- Configure the active sleep obfuscation technique.

## cli/commands/socks_proxy.py
Depends on: `cli/commands/_base.py`, `modules/socks_proxy.py`, `utils.py`
- `SocksProxyCommandSet.do_socks_config` (method) `cli/commands/socks_proxy.py:25` `def do_socks_config(self, line)` -- Show or configure the SOCKS5 proxy.
- `SocksProxyCommandSet.do_socks_sessions` (method) `cli/commands/socks_proxy.py:75` `def do_socks_sessions(self, line)` -- List active SOCKS proxy sessions.
- `SocksProxyCommandSet.do_socks_export` (method) `cli/commands/socks_proxy.py:94` `def do_socks_export(self, line)` -- Export SOCKS5 proxy specification for beacon delivery.

## cli/commands/supply_chain.py
Depends on: `cli/commands/_base.py`, `utils.py`
- `SupplyChainCommandSet.do_depconfuse` (method) `cli/commands/supply_chain.py:95` `def do_depconfuse(self, line)` -- Scan a requirements.txt for dependency confusion candidates.
- `SupplyChainCommandSet.do_package_squat` (method) `cli/commands/supply_chain.py:140` `def do_package_squat(self, line)` -- Generate a malicious PyPI package for dependency confusion.
- `SupplyChainCommandSet.do_depscan` (method) `cli/commands/supply_chain.py:216` `def do_depscan(self, line)` -- Scan a directory tree for dependency files and flag risks.
- `SupplyChainCommandSet.is_internal_name` (method) `cli/commands/supply_chain.py:450` `def is_internal_name(name)` -- Check if a package name looks internal/private.

## cli/commands/ux.py
Depends on: `cli/commands/_base.py`, `cli/config_history.py`, `cli/fuzzy_match.py`, `cli/output_mode.py`, `cli/session_hud.py`, `cli/toast_bus.py`, `core/config.py`, `core/console.py`, `utils.py`
- `UxCommandSet.do_hud` (method) `cli/commands/ux.py:46` `def do_hud(self, line)` -- Session counters: elapsed time, commands run, material captured.
- `UxCommandSet.do_undo` (method) `cli/commands/ux.py:85` `def do_undo(self, line)` -- Revert the last assign/set configuration change.
- `UxCommandSet.do_config_diff` (method) `cli/commands/ux.py:115` `def do_config_diff(self, line)` -- Show what changed since the session started.
- `UxCommandSet.do_cheat` (method) `cli/commands/ux.py:140` `def do_cheat(self, line)` -- Render a cheatsheet section inside the shell.
- `UxCommandSet.do_toast` (method) `cli/commands/ux.py:167` `def do_toast(self, line)` -- Raise a toast notification inside the cmd2 shell.
- `UxCommandSet.do_suggest` (method) `cli/commands/ux.py:235` `def do_suggest(self, line)` -- Fuzzy command suggestion for typos and fragments.

## cli/config_history.py
Imported by: `cli/commands/session_ops.py`, `cli/commands/ux.py`
- `ConfigHistory.capture_baseline` (method) `cli/config_history.py:30` `def capture_baseline(self, state)` -- Store session-start snapshot used by diff.
- `ConfigHistory.push` (method) `cli/config_history.py:38` `def push(self, state)` -- Push a snapshot before mutation.
- `ConfigHistory.undo` (method) `cli/config_history.py:48` `def undo(self)` -- Pop the newest snapshot.
- `ConfigHistory.diff` (method) `cli/config_history.py:58` `def diff(self, current)` -- Compare current state against the baseline.
- `ConfigHistory.depth` (method) `cli/config_history.py:76` `def depth(self)` -- Return number of stored undo steps.
- `ConfigHistory.get_shell_history` (method) `cli/config_history.py:81` `def get_shell_history(shell)` -- Return the ConfigHistory bound to a shell, creating it on demand.
- `ConfigHistory.track_before` (method) `cli/config_history.py:104` `def track_before(history, state)` -- Capture baseline on first use then push a pre-mutation snapshot.

## cli/config_status.py
Depends on: `core/console.py`
Imported by: `cli/commands/help_ui.py`
- `ConfigStatus.__init__` (method) `cli/config_status.py:70` `def __init__(self, params, config)`
- `ConfigStatus.render_status` (method) `cli/config_status.py:89` `def render_status(self)` -- Render the grouped configuration status table.
- `ConfigStatus.render_quick_check` (method) `cli/config_status.py:129` `def render_quick_check(self)` -- Quick check: show only required fields that are not set.

## cli/confirm.py
Imported by: `cli/commands/ai.py`, `cli/commands/anti_forensics.py`, `cli/commands/cloud.py`, `cli/commands/infra.py`
- `confirm` (function) `cli/confirm.py:27` `def confirm(question, default, yes_values)` -- Ask a yes/no question, never raising on non-interactive stdin.

## cli/contextual_help.py
Depends on: `cli/palette.py`, `cli/phase_labels.py`, `core/console.py`
Imported by: `cli/commands/help_ui.py`, `tests/test_phase_labels.py`
- `ContextualHelp.__init__` (method) `cli/contextual_help.py:176` `def __init__(self, aliases, params, config)`
- `ContextualHelp.get_command_info` (method) `cli/contextual_help.py:188` `def get_command_info(self, name)` -- Return enriched info for a command, or None if not found.
- `ContextualHelp.render_command_help` (method) `cli/contextual_help.py:208` `def render_command_help(self, name)` -- Render contextual help for a single command.
- `ContextualHelp.render_phase_commands` (method) `cli/contextual_help.py:261` `def render_phase_commands(self, phase)` -- Render all commands for a given phase.
- `ContextualHelp.render_requirements_status` (method) `cli/contextual_help.py:281` `def render_requirements_status(self)` -- Show which requirements are met for the current session.

## cli/dashboard_layout.py
Imported by: `cli/dashboard_tui.py`
- `DashboardLayoutConfig.layout_mode` (method) `cli/dashboard_layout.py:28` `def layout_mode(width, config)` -- Return the layout bucket for a terminal width.
- `DashboardLayoutConfig.hidden_panels` (method) `cli/dashboard_layout.py:45` `def hidden_panels(mode)` -- Return panel ids hidden in the given layout mode.

## cli/dashboard_tui.py
Depends on: `cli/commands/containers.py`, `cli/dashboard_layout.py`, `cli/graph_advisor.py`, `cli/killchain.py`, `cli/ops_commands.py`, `cli/reactive_hints.py`, `cli/reasoning_stream.py`, `cli/recommendation_signals.py`, `cli/toast_bus.py`, `modules/killchain.py`
Imported by: `cli/commands/misc_migrated.py`, `tests/test_dashboard_tui.py`
- `CommandRequested.__init__` (method) `cli/dashboard_tui.py:100` `def __init__(self, command)`
- `PhaseSelected.__init__` (method) `cli/dashboard_tui.py:108` `def __init__(self, phase)`
- `PhaseSelected.dispatch_command` (method) `cli/dashboard_tui.py:113` `def dispatch_command(command, timeout)` -- Run one LazyOwn command headlessly and capture its output.
- `TargetPanel.get_selection` (method) `cli/dashboard_tui.py:335` `def get_selection(self, selection)` -- Override to prevent IndexError when selection offsets exceed text length.
- `TargetPanel.render_content` (method) `cli/dashboard_tui.py:348` `def render_content(self, payload, world)`
- `TargetPanel.update_data` (method) `cli/dashboard_tui.py:374` `def update_data(self, payload, world)`
- `KillChainPanel.__init__` (method) `cli/dashboard_tui.py:393` `def __init__(self)`
- `KillChainPanel.update_data` (method) `cli/dashboard_tui.py:397` `def update_data(self, progress)` -- Render kill-chain progress.
- `KillChainPanel.on_click` (method) `cli/dashboard_tui.py:418` `def on_click(self, event)` -- Select the phase whose row was clicked.
- `ConfigPanel.update_data` (method) `cli/dashboard_tui.py:443` `def update_data(self, payload)`
- `CommandsPanel.update_data` (method) `cli/dashboard_tui.py:473` `def update_data(self, commands)`
- `ReasoningPanel.update_data` (method) `cli/dashboard_tui.py:508` `def update_data(self, entries)` -- Render the most recent daemon decisions, newest first.
- `OpsPanel.update_data` (method) `cli/dashboard_tui.py:545` `def update_data(self, world, tasks, creds, hashes, beacons, cred_lines)`
- `HintBar.__init__` (method) `cli/dashboard_tui.py:611` `def __init__(self)`
- `HintBar.compose` (method) `cli/dashboard_tui.py:616` `def compose(self)`
- `HintBar.update_data` (method) `cli/dashboard_tui.py:620` `def update_data(self, hints)` -- Replace the hint buttons with one button per suggestion.
- `HintBar.on_button_pressed` (method) `cli/dashboard_tui.py:645` `def on_button_pressed(self, event)` -- Run the clicked suggestion as if it had been typed.
- `ToastPanel.update_data` (method) `cli/dashboard_tui.py:672` `def update_data(self, payload, sessions_dir, width)` -- Render the latest notifications for the active theme.
- `NextStepsPanel.update_data` (method) `cli/dashboard_tui.py:720` `def update_data(self, recommendations)`
- `LazyOwnDashboard.__init__` (method) `cli/dashboard_tui.py:809` `def __init__(self, payload_path, sessions_dir)`
- `LazyOwnDashboard.compose` (method) `cli/dashboard_tui.py:838` `def compose(self)`
- `LazyOwnDashboard.on_mount` (method) `cli/dashboard_tui.py:857` `def on_mount(self)`
- `LazyOwnDashboard.on_input_submitted` (method) `cli/dashboard_tui.py:862` `def on_input_submitted(self, event)` -- Run the typed command and clear the input.
- `LazyOwnDashboard.on_command_requested` (method) `cli/dashboard_tui.py:874` `def on_command_requested(self, event)` -- Dispatch a command in a worker so the UI never blocks.
- `LazyOwnDashboard.on_phase_selected` (method) `cli/dashboard_tui.py:914` `def on_phase_selected(self, event)` -- Filter the center panel to a phase chosen by clicking the kill chain.
- `LazyOwnDashboard.action_refresh_data` (method) `cli/dashboard_tui.py:925` `def action_refresh_data(self)`
- `LazyOwnDashboard.action_toggle_compact` (method) `cli/dashboard_tui.py:928` `def action_toggle_compact(self)` -- Toggle the compact single-column layout for narrow terminals.
- `LazyOwnDashboard.action_screenshot` (method) `cli/dashboard_tui.py:958` `def action_screenshot(self)` -- Save an SVG screenshot next to the sessions directory.
- `LazyOwnDashboard.action_export_snapshot` (method) `cli/dashboard_tui.py:969` `def action_export_snapshot(self)` -- Export the current dashboard data as JSON for automation.
- `LazyOwnDashboard.action_next_phase` (method) `cli/dashboard_tui.py:989` `def action_next_phase(self)` -- Advance to the next kill-chain phase and refresh the display.
- `LazyOwnDashboard.action_prev_phase` (method) `cli/dashboard_tui.py:993` `def action_prev_phase(self)` -- Step back to the previous kill-chain phase.
- `LazyOwnDashboard.launch` (method) `cli/dashboard_tui.py:1069` `def launch(payload_path, sessions_dir)` -- Launch the dashboard and block until the user quits.

## cli/doctor.py
Depends on: `cli/wizard.py`, `core/console.py`, `core/profiles.py`
Imported by: `cli/commands/help_ui.py`
- `DoctorReport.failures` (method) `cli/doctor.py:119` `def failures(self)` -- Return the checks whose status is :data:`STATUS_FAIL`.
- `DoctorReport.warnings` (method) `cli/doctor.py:124` `def warnings(self)` -- Return the checks whose status is :data:`STATUS_WARN`.
- `DoctorReport.healthy` (method) `cli/doctor.py:129` `def healthy(self)` -- Return ``True`` when no check failed (warnings are tolerated).
- `DoctorReport.overall_status` (method) `cli/doctor.py:134` `def overall_status(self)` -- Return the worst status across every check.
- `DoctorReport.check_python_version` (method) `cli/doctor.py:143` `def check_python_version(version_info)` -- Verify the interpreter satisfies :data:`MIN_PYTHON_VERSION`.
- `DoctorReport.check_virtualenv` (method) `cli/doctor.py:172` `def check_virtualenv()` -- Report whether the framework is running inside its virtual environment.
- `DoctorReport.check_packages` (method) `cli/doctor.py:209` `def check_packages(specs, finder)` -- Verify every dependency in ``specs`` is importable without importing it.
- `DoctorReport.check_certificates` (method) `cli/doctor.py:248` `def check_certificates(root)` -- Verify the self-signed C2 certificate pair exists.
- `DoctorReport.check_payload` (method) `cli/doctor.py:269` `def check_payload(root)` -- Verify ``payload.json`` exists in the repository root.
- `DoctorReport.check_seclists` (method) `cli/doctor.py:289` `def check_seclists(finder)` -- Verify a SecLists installation is discoverable on disk.
- `DoctorReport.check_command_index` (method) `cli/doctor.py:313` `def check_command_index(root)`
- `DoctorReport.check_external_tools` (method) `cli/doctor.py:343` `def check_external_tools(checker)` -- Adapt :func:`cli.wizard.check_binaries` into preflight check results.
- `DoctorReport.gather_report` (method) `cli/doctor.py:368` `def gather_report(root)` -- Run every preflight check and collect the results without printing.
- `DoctorReport.render_report` (method) `cli/doctor.py:406` `def render_report(report, console)` -- Render a :class:`DoctorReport` as a rich table with a summary banner.
- `DoctorReport.run` (method) `cli/doctor.py:451` `def run(root, console)` -- Gather and render the preflight report.
- `DoctorReport.fix_report` (method) `cli/doctor.py:468` `def fix_report(report)` -- Interactively offer to fix every failure and warning in the report.

## cli/engagement_hooks.py
Depends on: `cli/palette.py`, `core/config.py`, `modules/cli_auth.py`, `modules/lazy_rbac.py`
Imported by: `cli/banner_config.py`, `cli/commands/help_ui.py`, `cli/session_hud.py`, `cli/tips_engine.py`, `lazyown.py`, `modules/cli_auth.py`, `modules/redteam_gym.py`, `tests/test_engagement_and_ping.py`, `tests/test_engagement_command_gate.py`, `tests/test_engagement_elo_and_methodology.py`
- `EngagementState.heal_commands_seen` (method) `cli/engagement_hooks.py:365` `def heal_commands_seen(known)` -- Purge non-command entries from persisted ``commands_seen`` in place.
- `EngagementState.get_karma_name` (method) `cli/engagement_hooks.py:716` `def get_karma_name(elo)` -- Return karma rank for an ELO score.
- `EngagementState.render_engagement_hook` (method) `cli/engagement_hooks.py:898` `def render_engagement_hook(cmd, phase, enabled)` -- Post-command hook: curiosity reveal + ELO + VRI reward when due.
- `EngagementState.get_state_snapshot` (method) `cli/engagement_hooks.py:978` `def get_state_snapshot()` -- Return a read-only snapshot of current engagement state for CLI display.
- `EngagementState.reset_session` (method) `cli/engagement_hooks.py:1066` `def reset_session()` -- Reset session counters without clearing cross-session progress.

## cli/exploit_advisor.py
Depends on: `core/console.py`
Imported by: `cli/commands/recon.py`
- `ServiceInfo.search_query` (method) `cli/exploit_advisor.py:122` `def search_query(self)` -- Best query string for searchsploit / NVD.
- `ServiceInfo.display_name` (method) `cli/exploit_advisor.py:128` `def display_name(self)`
- `ServiceInfo.next_commands` (method) `cli/exploit_advisor.py:132` `def next_commands(self)` -- Return (command, reason) pairs recommended for this service.
- `ServiceResult.parse_nmap_xml` (method) `cli/exploit_advisor.py:164` `def parse_nmap_xml(path)` -- Extract open services from a nmap XML file.
- `ServiceResult.find_nmap_xml` (method) `cli/exploit_advisor.py:203` `def find_nmap_xml(rhost, sessions_dir)` -- Return all nmap XML files for a given rhost, newest first.
- `ServiceResult.print_exploit_summary` (method) `cli/exploit_advisor.py:222` `def print_exploit_summary(results, rhost)` -- Print a rich summary table of exploit search results with next-step commands.
- `ServiceResult.save_ss_results` (method) `cli/exploit_advisor.py:296` `def save_ss_results(results, rhost, sessions_dir)` -- Save exploit search results to sessions/ss_results_<rhost>.json.
- `ServiceResult.inject_exploit_tasks` (method) `cli/exploit_advisor.py:338` `def inject_exploit_tasks(results, rhost, tasks_path)` -- Append one task per service with significant exploit hits to tasks.json.

## cli/exploration.py
Imported by: `cli/command_chain.py`, `cli/commands/misc_migrated.py`, `cli/exploration_view.py`, `cli/lazynmap_post.py`, `cli/recommendation_signals.py`, `cli/recon_plan.py`, `lazyown.py`, `tests/test_command_chain.py`, `tests/test_exploration_and_addons.py`, `tests/test_lazynmap_post.py`, `tests/test_recon_plan.py`
- `DiscoveredService.label` (method) `cli/exploration.py:98` `def label(self)` -- Return a compact human-readable label such as ``smb:445/tcp``.
- `CoverageReport.service_coverage` (method) `cli/exploration.py:145` `def service_coverage(self)` -- Fraction of discovered services with at least one run command.
- `CoverageReport.addon_coverage` (method) `cli/exploration.py:153` `def addon_coverage(self)` -- Fraction of enabled addons that have been executed at least once.
- `CoverageReport.tool_coverage` (method) `cli/exploration.py:161` `def tool_coverage(self)` -- Fraction of active tools that have been executed at least once.
- `NmapXmlReader.__init__` (method) `cli/exploration.py:176` `def __init__(self, config)` -- Store the configuration used to locate the nmap XML directory.
- `NmapXmlReader.discover` (method) `cli/exploration.py:181` `def discover(self, target)` -- Return every open service across every nmap XML in sessions.
- `AddonCatalog.__init__` (method) `cli/exploration.py:264` `def __init__(self, config)` -- Store the configuration used to locate the addons directory.
- `AddonCatalog.load` (method) `cli/exploration.py:269` `def load(self)` -- Return every parseable addon as an :class:`AddonEntry`.
- `AddonCatalog.clear_cache` (method) `cli/exploration.py:299` `def clear_cache(cls)` -- Drop the per-process addon cache (mainly used by tests).
- `ToolCatalog.__init__` (method) `cli/exploration.py:344` `def __init__(self, config)` -- Store the configuration used to locate the tools directory.
- `ToolCatalog.load` (method) `cli/exploration.py:349` `def load(self)` -- Return every parseable ``.tool`` file as a :class:`ToolEntry`.
- `ToolCatalog.clear_cache` (method) `cli/exploration.py:379` `def clear_cache(cls)` -- Drop the per-process tool cache (mainly used by tests).
- `TriggerMatcher.__init__` (method) `cli/exploration.py:413` `def __init__(self, current_os)` -- Store the platform used to filter incompatible entries.
- `TriggerMatcher.addons_for_service` (method) `cli/exploration.py:418` `def addons_for_service(self, service, addons)` -- Return addons whose trigger and OS match the given service.
- `TriggerMatcher.tools_for_service` (method) `cli/exploration.py:435` `def tools_for_service(self, service, tools)` -- Return active tools whose trigger and OS match the service.
- `HistoryReader.__init__` (method) `cli/exploration.py:473` `def __init__(self, config)` -- Store the configuration used to locate the transcript file.
- `HistoryReader.executed_commands` (method) `cli/exploration.py:478` `def executed_commands(self)` -- Return the set of unique tool/command names already run.
- `ExplorationEngine.__init__` (method) `cli/exploration.py:510` `def __init__(self, config, current_os)` -- Wire collaborators together using the supplied configuration.
- `ExplorationEngine.services` (method) `cli/exploration.py:525` `def services(self, target)` -- Return the discovered services for the engagement.
- `ExplorationEngine.addons` (method) `cli/exploration.py:530` `def addons(self)` -- Return the parsed lazyaddon catalogue.
- `ExplorationEngine.tools` (method) `cli/exploration.py:535` `def tools(self)` -- Return the parsed ``.tool`` catalogue.
- `ExplorationEngine.history` (method) `cli/exploration.py:540` `def history(self)` -- Return the set of already-executed command names.
- `ExplorationEngine.suggestions_for_target` (method) `cli/exploration.py:545` `def suggestions_for_target(self, target)` -- Group matching addons and tools by service for a target.
- `ExplorationEngine.unexplored_addons` (method) `cli/exploration.py:568` `def unexplored_addons(self, target)` -- Return addons triggered by the scan that have never been run.
- `ExplorationEngine.unexplored_tools` (method) `cli/exploration.py:589` `def unexplored_tools(self, target)` -- Return tools triggered by the scan that have never been run.
- `ExplorationEngine.coverage` (method) `cli/exploration.py:610` `def coverage(self, target)` -- Return an aggregate :class:`CoverageReport` for the engagement.
- `ExplorationEngine.resolve_current_os` (method) `cli/exploration.py:656` `def resolve_current_os(payload)` -- Resolve the current victim platform from a payload-like mapping.
- `ExplorationEngine.normalise_os` (method) `cli/exploration.py:677` `def normalise_os(value, default)` -- Coerce arbitrary YAML/JSON values to a whitelisted OS string.
- `ExplorationEngine.normalise_trigger` (method) `cli/exploration.py:690` `def normalise_trigger(value)` -- Coerce arbitrary YAML/JSON values to a tuple of trigger strings.

## cli/exploration_view.py
Depends on: `cli/exploration.py`, `core/console.py`
Imported by: `cli/commands/misc_migrated.py`, `tests/test_exploration_and_addons.py`
- `render_exploration` (function) `cli/exploration_view.py:39` `def render_exploration(console, engine, target, history)` -- Render the full ``explore`` view to ``console``.

## cli/fuzzy_match.py
Depends on: `cli/fuzzy_picker.py`
Imported by: `cli/commands/ux.py`
- `FuzzyMatchConfig.suggest` (method) `cli/fuzzy_match.py:28` `def suggest(query, candidates, limit, config)` -- Return up to limit candidate names ranked by relevance to query.
- `FuzzyMatchConfig.did_you_mean` (method) `cli/fuzzy_match.py:56` `def did_you_mean(query, candidates)` -- Return the single best correction for query or None.

## cli/fuzzy_picker.py
Imported by: `cli/fuzzy_match.py`, `lazyown.py`, `tests/test_fuzzy_picker.py`
- `PickerConfig.from_payload` (method) `cli/fuzzy_picker.py:117` `def from_payload(cls, payload)` -- Build a config from a payload.json view, falling back to defaults.
- `MatchScorer.__init__` (method) `cli/fuzzy_picker.py:170` `def __init__(self, config)`
- `MatchScorer.rank` (method) `cli/fuzzy_picker.py:173` `def rank(self, items, query)` -- Return ``items`` ranked by descending relevance against ``query``.
- `PickerView.run` (method) `cli/fuzzy_picker.py:231` `def run(self, items, initial_query)`
- `CursesPickerView.__init__` (method) `cli/fuzzy_picker.py:243` `def __init__(self, config, scorer)`
- `CursesPickerView.run` (method) `cli/fuzzy_picker.py:247` `def run(self, items, initial_query)`
- `FuzzyPicker.__init__` (method) `cli/fuzzy_picker.py:551` `def __init__(self, config, view_factory)`
- `FuzzyPicker.config` (method) `cli/fuzzy_picker.py:562` `def config(self)`
- `FuzzyPicker.pick` (method) `cli/fuzzy_picker.py:565` `def pick(self, items, initial_query)` -- Return the selected item text or ``None`` on cancel / empty input.
- `ReadlineBridge.__init__` (method) `cli/fuzzy_picker.py:592` `def __init__(self, picker)`
- `ReadlineBridge.install` (method) `cli/fuzzy_picker.py:595` `def install(self)` -- Wire the picker into ``readline.set_completion_display_matches_hook``.
- `ReadlineBridge.uninstall` (method) `cli/fuzzy_picker.py:603` `def uninstall(self)` -- Remove the readline display hook installed by :py:meth:`install`.
- `ReadlineBridge.install_fuzzy_completion` (method) `cli/fuzzy_picker.py:645` `def install_fuzzy_completion(shell, payload, config)` -- Install the fuzzy picker into a cmd2 shell.

## cli/graph_advisor.py
Imported by: `cli/commands/misc_migrated.py`, `cli/dashboard_tui.py`, `cli/graph_overlay.py`, `cli/reactive_hints.py`, `cli/recommendation_signals.py`, `lazyown.py`, `modules/unified_dashboard.py`, `skills/lazyown_mcp.py`, `tests/test_graph_advisor.py`
- `GraphNode.to_summary` (method) `cli/graph_advisor.py:109` `def to_summary(self)` -- Return a small, JSON-safe summary suitable for MCP responses.
- `GraphEdge.to_summary` (method) `cli/graph_advisor.py:132` `def to_summary(self)`
- `GraphLoader.__init__` (method) `cli/graph_advisor.py:156` `def __init__(self, config)`
- `GraphLoader.resolve_path` (method) `cli/graph_advisor.py:160` `def resolve_path(self, override)` -- Resolve which graphify JSON file to load.
- `GraphLoader.load` (method) `cli/graph_advisor.py:184` `def load(self, override)`
- `GraphLoader.clear_cache` (method) `cli/graph_advisor.py:207` `def clear_cache(cls)`
- `GraphIndex.__init__` (method) `cli/graph_advisor.py:214` `def __init__(self, data)`
- `GraphIndex.nodes` (method) `cli/graph_advisor.py:277` `def nodes(self)`
- `GraphIndex.get` (method) `cli/graph_advisor.py:280` `def get(self, node_id)`
- `GraphIndex.neighbors` (method) `cli/graph_advisor.py:283` `def neighbors(self, node_id)`
- `GraphIndex.edges_between` (method) `cli/graph_advisor.py:286` `def edges_between(self, source, target)`
- `GraphIndex.community_members` (method) `cli/graph_advisor.py:289` `def community_members(self, community_id)`
- `GraphIndex.degree` (method) `cli/graph_advisor.py:292` `def degree(self, node_id)`
- `GraphIndex.degree_ranked` (method) `cli/graph_advisor.py:295` `def degree_ranked(self)`
- `GraphScorer.__init__` (method) `cli/graph_advisor.py:304` `def __init__(self, config)`
- `GraphScorer.rank` (method) `cli/graph_advisor.py:307` `def rank(self, nodes, query)`
- `GraphAdvisor.__init__` (method) `cli/graph_advisor.py:362` `def __init__(self, config, loader, index, scorer)`
- `GraphAdvisor.from_path` (method) `cli/graph_advisor.py:375` `def from_path(cls, path, config)`
- `GraphAdvisor.is_available` (method) `cli/graph_advisor.py:384` `def is_available(self)`
- `GraphAdvisor.reload` (method) `cli/graph_advisor.py:387` `def reload(self, path)`
- `GraphAdvisor.summary` (method) `cli/graph_advisor.py:396` `def summary(self)`
- `GraphAdvisor.search` (method) `cli/graph_advisor.py:445` `def search(self, query, limit)`
- `GraphAdvisor.neighbors` (method) `cli/graph_advisor.py:456` `def neighbors(self, node_query, depth, limit)`
- `GraphAdvisor.god_nodes` (method) `cli/graph_advisor.py:505` `def god_nodes(self, limit)`
- `GraphAdvisor.suggest_next` (method) `cli/graph_advisor.py:520` `def suggest_next(self, recent_commands, limit)` -- Suggest next commands by walking the graph outward from recent ones.
- `GraphAdvisor.read_recent_commands` (method) `cli/graph_advisor.py:566` `def read_recent_commands(self, window)` -- Read the last N executed commands from the session transcript.
- `GraphAdvisor.did_you_mean` (method) `cli/graph_advisor.py:591` `def did_you_mean(self, query, limit)`
- `GraphAdvisor.truncate_to_budget` (method) `cli/graph_advisor.py:605` `def truncate_to_budget(self, payload, budget_tokens)` -- Trim list fields in-place so the JSON dump fits a token budget.
- `GraphAdvisor.format_search_table` (method) `cli/graph_advisor.py:691` `def format_search_table(results)` -- Render search results as a fixed-width table for the cmd2 shell.
- `GraphAdvisor.format_neighbors` (method) `cli/graph_advisor.py:706` `def format_neighbors(result)` -- Render a :py:meth:`GraphAdvisor.neighbors` result as plain text.
- `GraphAdvisor.format_god_nodes` (method) `cli/graph_advisor.py:724` `def format_god_nodes(results)`
- `GraphAdvisor.format_suggestions` (method) `cli/graph_advisor.py:734` `def format_suggestions(results)`

## cli/graph_overlay.py
Depends on: `cli/commands/containers.py`, `cli/commands/enum.py`, `cli/graph_advisor.py`, `cli/themes.py`, `core/text_utils.py`
Imported by: `cli/commands/misc_migrated.py`, `tests/test_graph_overlay.py`
- `GraphOverlayState.is_available` (method) `cli/graph_overlay.py:77` `def is_available(self)` -- Return ``True`` when the underlying graph advisor has data.
- `GraphOverlayState.set_focus` (method) `cli/graph_overlay.py:87` `def set_focus(self, value)` -- Replace the focus query.
- `GraphOverlayState.toggle_view` (method) `cli/graph_overlay.py:95` `def toggle_view(self)` -- Switch between god-nodes and neighbors-of-focus.
- `GraphOverlayState.snapshot` (method) `cli/graph_overlay.py:102` `def snapshot(self)` -- Return ``(header, items)`` for the current view.
- `GraphOverlayState.build_state` (method) `cli/graph_overlay.py:192` `def build_state(config, advisor_factory)` -- Wire the canonical state used by :func:`launch_overlay`.
- `GraphOverlayState.launch_overlay` (method) `cli/graph_overlay.py:203` `def launch_overlay(payload, state, runner)` -- Open the overlay and return the last-focused node id on exit.
- `_GraphOverlayApp.__init__` (method) `cli/graph_overlay.py:260` `def __init__(self)`
- `_GraphOverlayApp.compose` (method) `cli/graph_overlay.py:265` `def compose(self)`
- `_GraphOverlayApp.on_mount` (method) `cli/graph_overlay.py:273` `def on_mount(self)`
- `_GraphOverlayApp.on_input_changed` (method) `cli/graph_overlay.py:276` `def on_input_changed(self, event)`
- `_GraphOverlayApp.action_toggle_view` (method) `cli/graph_overlay.py:280` `def action_toggle_view(self)`
- `_GraphOverlayApp.action_close` (method) `cli/graph_overlay.py:284` `def action_close(self)`

## cli/headless.py
Imported by: `lazyown.py`
- `load_profile` (function) `cli/headless.py:31` `def load_profile(path)` -- Load a YAML profile that overrides payload.json keys.
- `apply_profile` (function) `cli/headless.py:48` `def apply_profile(config, profile)` -- Merge profile values into config (shallow overlay).
- `HeadlessRunner.__init__` (method) `cli/headless.py:72` `def __init__(self, shell, json_output, profile_path)`
- `HeadlessRunner.run_command` (method) `cli/headless.py:87` `def run_command(self, cmd, timeout)` -- Execute a single command, capture output, return structured result.
- `HeadlessRunner.run_chain` (method) `cli/headless.py:132` `def run_chain(self, commands)` -- Execute multiple commands and emit final summary.

## cli/killchain.py
Depends on: `modules/killchain.py`
Imported by: `cli/dashboard_tui.py`, `tests/test_killchain.py`
- `PhaseProgress.compute_killchain` (method) `cli/killchain.py:83` `def compute_killchain(events, world, phases)` -- Compute kill-chain progress from daemon events and the world model.


Next: [API_p4.md](API_p4.md)
