"""Reconnaissance command set.

Network reconnaissance commands: nmap variants, DNS tools, web fingerprinting,
and quick recon scripts.
"""

from __future__ import annotations

import json
import os

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    BLUE,
    GREEN,
    RESET,
    UNDERLINE,
    print_error,
    print_msg,
    print_warn,
    recon_category,
    scanning_category,
    exploitation_category,
    check_rhost,
    is_binary_present,
    is_package_installed,
    run_command,
)


class ReconCommandSet(LazyOwnCommandSet):
    """Reconnaissance phase commands."""

    phase = "recon"
    category = "01. Reconnaissance"

    @cmd2.with_category(scanning_category)
    def do_batchnmap(self, line):
        """
        Runs the internal module `modules/lazynmap.sh` for multiple Nmap scans.

        This method executes the `lazynmap` script, using the current working directory
        and the `rhost` parameter from the `self.params` dictionary as the target IP.
        If `rhost` is not set, it prints an error message.

        :return: None
        """

        file_path = get_users_dic('txt')
        path = os.getcwd()
        try:
            with open(file_path, 'r') as file:
                for target in file:
                    target = target.strip()
                    if target:
                        self.cmd(f"{path}/modules/lazynmap.sh -t {target}")
        except FileNotFoundError:
            self.perror(f"File not found: {file_path}")
        except Exception as e:
            self.perror(f"An error occurred: {e}")


        return


    @cmd2.with_category(scanning_category)
    def do_lazynmap(self, line):
        """
        Runs the internal module `modules/lazynmap.sh` with target mode.

        OS detection (via ping TTL) is performed automatically before scanning
        when the target OS is not yet known, so that tool selectors downstream
        have a valid platform context.

        :param line: The network IP to scan. Defaults to rhost from params.
        :type line: str

        :return: None
        """
        if not line:
            line = self.params["rhost"]
        path = os.getcwd()

        # Gate: run ping first if OS has not been identified yet.
        os_json_path = "sessions/os.json"
        os_known = False
        try:
            if os.path.isfile(os_json_path):
                with open(os_json_path) as _f:
                    _data = json.load(_f)
                    if _data and _data[0].get("state") == "active":
                        os_known = True
        except Exception:
            pass

        if not os_known:
            print_msg(
                "OS not yet identified — running ping before nmap "
                "to select the correct tool chain."
            )
            # Temporarily override rhost to the explicit target if different
            _prev_rhost = self.params.get("rhost")
            if line and line != _prev_rhost:
                self.params["rhost"] = line
            self.onecmd("ping")
            if line and line != _prev_rhost:
                self.params["rhost"] = _prev_rhost

        self.cmd(f"{path}/modules/lazynmap.sh -t {line}")

        try:
            from rich.console import Console as _PostScanConsole

            from cli.lazynmap_post import run_post_scan as _run_post_scan

            _run_post_scan(
                target=line,
                payload=self.params,
                console=_PostScanConsole(highlight=False, soft_wrap=True),
            )
        except Exception as _post_exc:
            print_warn(f"recon plan post-processing failed: {_post_exc}")

        if (self.params.get("api_key") or "").strip():
            self.onecmd("vulnbot_groq")
        else:
            print_warn(
                "Skipping vulnbot_groq: 'api_key' not set in payload.json "
                "(use 'assign api_key <token>' to enable Groq-backed analysis)."
            )
        self.onecmd("report")
        return


    @cmd2.with_category(recon_category)
    def do_dig(self, line):
        """
        Executes the `dig` command to query DNS information.

        1. Retrieves the DNS server IP from the `line` parameter and the target host from the `rhost` parameter.
        2. If either the DNS server or `rhost` is not provided, an error message is printed.
        3. Executes the `dig` command to query the version of the DNS server and additional records.

        :param line: DNS server IP or hostname. Must be provided for the `dig` command.
        :param rhost: Target host for additional `dig` queries.

        :returns: None

        Manual execution:
        To manually run these commands, use the following syntax:
            dig version.bind CHAOS TXT @<dns_server>
            dig any <domain> @<rhost>

        Replace `<dns_server>` with the IP address or hostname of the DNS server, `<domain>` with the target domain, and `<rhost>` with the IP address or hostname of the target machine.
        """

        rhost = self.params["rhost"]
        if not line or not rhost:
            print_error(
                "[-] rhost must be assign or you must pass the dns argument like dig box.htb"
            )
            return
        print_msg(f"Try dig version.bind CHAOS TXT @{line} {RESET}")
        self.cmd(f"dig version.bind CHAOS TXT @{line}")
        print_msg(f"dig any {line} @{rhost}")
        self.cmd(f"dig any {line} @{rhost}")
        return


    @cmd2.with_category(recon_category)
    def do_dnsenum(self, line):
        """
        Performs DNS enumeration using `dnsenum` to identify subdomains for a given domain.

        1. Executes the `dnsenum` command with parameters to specify the DNS server, output file, and wordlist for enumeration.

        :param line: The target domain to perform DNS enumeration on, e.g., `ghost.htb`.
        :param rhost: The DNS server to use for enumeration, e.g., `10.10.11.24`.
        :param dnswordlist: The path to the DNS wordlist file used for subdomain discovery.

        :returns: None

        Manual execution:
        To manually perform DNS enumeration, use the following command:
            dnsenum --dnsserver <dns_server> --enum -p 0 -s 0 -o <output_file> -f <dns_wordlist> <target_domain>

        Replace `<dns_server>` with the DNS server IP, `<output_file>` with the file path to save the results, `<dns_wordlist>` with the path to your DNS wordlist file, and `<target_domain>` with the domain to be enumerated.

        For example:
            dnsenum --dnsserver 10.10.11.24 --enum -p 0 -s 0 -o sessions/subdomains.txt -f /path/to/dnswordlist.txt ghost.htb
        """

        rhost = self.params["rhost"]
        dnswordlist = self.params["dnswordlist"]
        if not line or not rhost or not dnswordlist:
            print_error(
                "rhost and dnswordlist must be assign example: assign rhost 10.10.10.10 or you need pass the domain "
            )
            return
        print_msg(
            f"Try ... dnsenum --dnsserver {rhost} --enum -p 0 -s 0 -o sessions/subdomains.txt -f {dnswordlist} {line} {RESET}"
        )
        self.cmd(
            f"dnsenum --dnsserver {rhost} --enum -p 0 -s 0 -o sessions/subdomains.txt -f {dnswordlist} {line}"
        )
        return

    @cmd2.with_category(recon_category)
    def do_dnsmap(self, line):
        """
        Performs DNS enumeration using `dnsmap` to discover subdomains for a specified domain.

        1. Executes the `dnsmap` command to scan the given domain with a specified wordlist.

        :param line: The target domain to perform DNS enumeration on, e.g., `ghost.htb`.
        :param dnswordlist: The path to the wordlist file used for DNS enumeration.

        :returns: None

        Manual execution:
        To manually perform DNS enumeration, use the following command:
            dnsmap <target_domain> -w <dns_wordlist>

        Replace `<target_domain>` with the domain you want to scan and `<dns_wordlist>` with the path to your DNS wordlist file.

        For example:
            dnsmap ghost.htb -w /path/to/dnswordlist.txt
        """

        rhost = self.params["rhost"]
        dnswordlist = self.params["dnswordlist"]
        if not line or not dnswordlist:
            print_error(
                f"dnswordlist must be assign example: assign dnswordlist path/to/wordlist or you need pass the domain {RESET}"
            )
            return
        print_msg(f"    {GREEN}[+] Try ... dnsmap {line} -w {dnswordlist} {RESET}")
        self.cmd(f"dnsmap {line} -w {dnswordlist}")
        return


    @cmd2.with_category(recon_category)
    def do_whatweb(self, line):
        """
        Performs a web technology fingerprinting scan using `whatweb`.

        1. Executes the `whatweb` command to identify technologies used by the target web application.

        :param line: This parameter is not used in the current implementation but could be used to pass additional options or arguments if needed.
        :param rhost: The target web host to be scanned, specified in the `params` dictionary.

        :returns: None

        Manual execution:
        To manually perform web technology fingerprinting, use the following command:
            whatweb <target_host>

        Replace `<target_host>` with the URL or IP address of the web application you want to scan.

        For example:
            whatweb example.com
        """
        rhost = self.params["rhost"]
        url = self.params["url"]
        if not check_rhost(rhost):
            return


        if not line:
            print_msg(f"Try... whatweb {rhost}{RESET}")
            self.cmd(f"whatweb {rhost}")
        else:
            if line.startswith("ssl"):
                print_msg(f"Try... whatweb {rhost}{RESET}")
                self.cmd(f"whatweb https://{rhost}")
            elif line.startswith("url"):
                print_msg(f"Try... whatweb {url}{RESET}")
                self.cmd(f"whatweb {url}")


    @cmd2.with_category(scanning_category)
    def do_nbtscan(self, line):
        """
        Performs network scanning using `nbtscan` to discover NetBIOS names and addresses in a specified range.

        1. Executes the `nbtscan` command with the `-r` option to scan the specified range of IP addresses for NetBIOS information.

        :param line: This parameter is not used in the current implementation but could be used to specify additional options or arguments if needed.
        :param rhost: The target network range for scanning, specified in the `params` dictionary.

        :returns: None

        Manual execution:
        To manually perform a NetBIOS scan across a network range, use the following command:
            sudo nbtscan -r <network_range>

        Replace `<network_range>` with the IP address range you want to scan. For example:
            sudo nbtscan -r 192.168.1.0/24
        """

        if not self.params["rhost"]:
            print_error(f"rhost must be assign{RESET}")
            return
        rhost = self.params["rhost"]
        print_msg(f"Try... sudo nbtscan -r {rhost}/24 {RESET}")
        self.cmd(f"sudo nbtscan -r {rhost}/24")
        return


    @cmd2.with_category(scanning_category)
    def do_nikto(self, line):
        """
        Runs the `nikto` tool to perform a web server vulnerability scan against the specified target host.

        1. Executes `nikto` with the `-h` option to specify the target host IP address.
        2. Installs `nikto` if it is not already installed.

        :param line: This parameter is not used in the current implementation but could be used to specify additional options or arguments if needed.
        :param rhost: The IP address of the target web server, specified in the `params` dictionary.

        :returns: None

        Manual execution:
        To manually perform a web server vulnerability scan using `nikto`, use the following command:
            nikto -h <target_ip>

        Replace `<target_ip>` with the IP address of the target web server. For example:
            nikto -h 10.10.10.10
        """

        rhost = self.params["rhost"]
        if not check_rhost(rhost):
            return

        if not is_binary_present("nikto"):
            print_warn("Installing nikto...")
            self.cmd("sudo apt install nikto -y")

        options = {
            "ask": input("    [?] Enter whether to ask about submitting updates (yes, no, auto): "),
            "check6": input("    [?] Check if IPv6 is working (yes/no): "),
            "cgidirs": input("    [?] Enter CGI dirs to scan (none, all, or values like '/cgi/ /cgi-a/'): "),
            "config": input("    [?] Enter the config file to use: "),
            "display": input("    [?] Enter display options (1, 2, 3, 4, D, E, P, S, V): "),
            "dbcheck": input("    [?] Check database and key files for syntax errors (yes/no): "),
            "evasion": input("    [?] Enter encoding technique (1-8, A, B): "),
            "followredirects": input("    [?] Follow 3xx redirects (yes/no): "),
            "format": input("    [?] Enter output format (csv, json, htm, nbe, sql, txt, xml): "),
            "host": rhost,
            "id": input("    [?] Enter host authentication (id:pass or id:pass:realm): "),
            "ipv4": input("    [?] Use IPv4 only (yes/no): "),
            "ipv6": input("    [?] Use IPv6 only (yes/no): "),
            "key": input("    [?] Enter client certificate key file: "),
            "list_plugins": input("    [?] List all available plugins (yes/no): "),
            "maxtime": input("    [?] Enter maximum testing time per host (e.g., 1h, 60m, 3600s): "),
            "mutate": input("    [?] Enter mutation options (1-6): "),
            "nointeractive": input("    [?] Disable interactive features (yes/no): "),
            "nolookup": input("    [?] Disable DNS lookups (yes/no): "),
            "nossl": input("    [?] Disable the use of SSL (yes/no): "),
            "noslash": input("    [?] Strip trailing slash from URL (yes/no): "),
            "no404": input("    [?] Disable nikto attempting to guess a 404 page (yes/no): "),
            "option": input("    [?] Override an option in nikto.conf: "),
            "output": input("    [?] Write output to this file ('.' for auto-name): "),
            "pause": input("    [?] Pause between tests (seconds): "),
            "plugins": input("    [?] Enter list of plugins to run (default: ALL): "),
            "port": input("    [?] Enter port to use (default 80): "),
            "rsacert": input("    [?] Enter client certificate file: "),
            "root": input("    [?] Prepend root value to all requests (format: /directory): "),
            "save": input("    [?] Save positive responses to this directory ('.' for auto-name): "),
            "ssl": input("    [?] Force ssl mode on port (yes/no): "),
            "tuning": input("    [?] Enter scan tuning (1-9, a-e, x): "),
            "timeout": input("    [?] Enter timeout for requests (default 10 seconds): "),
            "userdbs": input("    [?] Load only user databases, not the standard databases (all, tests): "),
            "useragent": input("    [?] Override the default useragent: "),
            "until": input("    [?] Run until the specified time or duration: "),
            "url": self.params["url"],
            "usecookies": input("    [?] Use cookies from responses in future requests (yes/no): "),
            "useproxy": input("    [?] Use the proxy defined in nikto.conf, or argument http://server:port: "),
            "version": input("    [?] Print plugin and database versions (yes/no): "),
            "vhost": input("    [?] Enter virtual host (for Host header): "),
            "404code": input("    [?] Ignore these HTTP codes as negative responses (always). Format: '302,301': "),
            "404string": input("    [?] Ignore this string in response body content as negative response (always). Can be a regular expression: ")
        }

        nikto_command = f"nikto -h {options['host']}"

        for key, value in options.items():
            if value:
                if key == "host":
                    continue
                elif key in ["ask", "check6", "dbcheck", "followredirects", "ipv4", "ipv6", "list_plugins", "nointeractive", "nolookup", "nossl", "noslash", "no404", "ssl", "usecookies", "useproxy", "version"]:
                    nikto_command += f" --{key} {value}"
                else:
                    nikto_command += f" --{key} {value}"

        print_msg(f"Running nikto with the following command: {nikto_command}")
        self.cmd(nikto_command)
        return


    @cmd2.with_category(recon_category)
    def do_finalrecon(self, line):
        """
        Runs the `finalrecon` tool to perform a web server vulnerability scan against the specified target host.

        1. Executes `finalrecon` with the `-h` option to specify the target host IP address.

        :param line: This parameter is not used in the current implementation but could be used to specify additional options or arguments if needed.
        :param rhost: The IP address of the target web server, specified in the `params` dictionary.

        :returns: None

        Manual execution:
        To manually perform a web server vulnerability scan using `finalrecon`, use the following command:
            finalrecon --url=http://<target_ip> --full -o txt -cd <directory_reports>

        Replace `<target_ip>` with the IP address of the target web server. For example:
            finalrecon --url=http://192.168.1.92 --full -o txt -cd /home/gris/finalrecon
        """

        if not is_binary_present("finalrecon"):
            print_error(f"You need install finalrecon first:{GREEN} apt install finalrecon")
            return

        if not line:
            print_error(f"You must pass the url to perfom the scann ex: {GREEN}finalrecon http://10.10.10.10/")
            return
        command = f"finalrecon --url={line} --full -o txt -cd sessions/finalrecon_manual "
        copy2clip(command)
        self.cmd(command)
        return


    @cmd2.with_category(recon_category)
    def do_openssl_sclient(self, line):
        """
        Uses `openssl s_client` to connect to a specified host and port, allowing for testing and debugging of SSL/TLS connections.

        :param line: The port number to connect to on the target host. This must be provided as an argument.
        :param rhost: The IP address or hostname of the target server, specified in the `params` dictionary.

        :returns: None

        Manual execution:
        To manually connect to a server using `openssl s_client` and test SSL/TLS, use the following command:
            openssl s_client -connect <target_ip>:<port>

        Replace `<target_ip>` with the IP address or hostname of the target server and `<port>` with the port number. For example:
            openssl s_client -connect 10.10.10.10:443
        """

        if not self.params["rhost"] or not line:
            print_error(
                "rhost must be assign and you need pass the port by argument ex: openssl_sckient 443"
            )
            return
        rhost = self.params["rhost"]
        domain = self.params["domain"]
        print_msg(f"Try... openssl s_client -connect  {rhost}:{line} {RESET}")
        self.cmd(f"openssl s_client -connect  {rhost}:{line}")
        command = f"true | openssl s_client -connect {domain}:443 2>/dev/null | openssl x509 -noout -text  | perl -l -0777 -ne '@names=/\\bDNS:([^\\s,]+)/g; print join(\"\n\", sort @names);' | tee sessions/domains_{domain}.txt"
        print_msg(command)
        self.cmd(command)
        return


    @cmd2.with_category(exploitation_category)
    def do_ss(self, line):
        """Search all exploit sources and map findings to the next LazyOwn command.

        Without arguments: reads the nmap XML for the current rhost, extracts
        every open service+version, searches all sources for each one, saves
        structured results to sessions/ss_results_<rhost>.json, creates tasks
        for services with hits, and prints a 'what to try next' table.

        With a manual query: runs the full multi-source search (searchsploit,
        NVD, ExploitAlert, PacketStorm, MSF, Sploitus) for that term and shows
        recommended commands for the matching service.

        Usage:
            ``ss``                  — auto-scan from nmap XML for current rhost
            ``ss apache 2.4.49``    — manual query
            ``ss OpenSSH 8.4``      — manual query
        """
        from cli.exploit_advisor import (
            ExploitHit, ServiceInfo, ServiceResult,
            find_nmap_xml, inject_exploit_tasks,
            parse_nmap_xml, print_exploit_summary, save_ss_results,
        )

        rhost = self.params.get("rhost") or ""

        def _run_single_search(query: str) -> list[ExploitHit]:
            hits: list[ExploitHit] = []
            import subprocess as _sp
            try:
                out = _sp.run(
                    ["searchsploit", "--disable-colour", query],
                    capture_output=True, text=True, timeout=15,
                )
                for ln in (out.stdout or "").splitlines():
                    ln = ln.strip()
                    if ln and not ln.startswith("-") and "|" in ln:
                        parts = ln.split("|")
                        title = parts[0].strip()
                        ref   = parts[1].strip() if len(parts) > 1 else ""
                        if title and title.lower() not in ("exploits", "shellcodes", "papers", "title"):
                            hits.append(ExploitHit(source="searchsploit", title=title, ref=ref))
            except Exception:
                pass
            return hits

        # ── Auto mode: read nmap XML ──────────────────────────────────────
        if not line.strip():
            if not check_rhost(rhost):
                return
            xml_files = find_nmap_xml(rhost)
            if not xml_files:
                print_warn(f"No nmap XML found for {rhost}. Run lazynmap first.")
                print_msg(f"Or use: ss <service> <version>")
                return
            xml_path = xml_files[0]
            services = parse_nmap_xml(xml_path)
            if not services:
                print_warn(f"No open services found in {xml_path}")
                return
            print_msg(f"Found {len(services)} open service(s) in {os.path.basename(xml_path)}")
            results: list[ServiceResult] = []
            for svc in services:
                query = svc.search_query
                if not query:
                    results.append(ServiceResult(service=svc))
                    continue
                print_msg(f"  [{svc.port}/{svc.name}] searching: {query}")
                hits = _run_single_search(query)
                result = ServiceResult(service=svc, hits=hits)
                results.append(result)
            saved = save_ss_results(results, rhost)
            n_tasks = inject_exploit_tasks(results, rhost)
            print_exploit_summary(results, rhost)
            print_msg(f"Results saved to {saved}")
            if n_tasks:
                print_msg(f"{n_tasks} task(s) added — run 'tasks' to view")
            return

        # ── Manual mode: existing multi-source search + next-step table ───
        query = line.strip()
        print_msg(f"Searching in searchsploit")
        self.cmd(f"searchsploit {query}")
        getnvd = find_ss(query)
        nvddb(getnvd)
        getnvd = find_ea(query)
        exploitalert(getnvd)
        getnvd = find_ps(query)
        packetstormsecurity(getnvd)
        self.cmd(f"msfconsole -q -x \"search {query}; exit\"")
        q_url = query.replace(" ", "+")
        if not is_binary_present("pompem"):
            self.display_toastr("Not Found pompem, installing", type="warning")
            self.cmd("sudo apt install pompem -y")
        self.cmd(f"cd sessions && pompem -s {q_url} --txt")
        self.onecmd(f"creds_py '{query}'")
        print_msg(f"To open use Ctrl + Click: {BLUE}{UNDERLINE}https://sploitus.com/?query={q_url}#exploits")
        print_msg(f"To open use Ctrl + Click: {BLUE}{UNDERLINE}https://exploits.shodan.io/?q={q_url}")
        # infer service from query first token and show next-step table
        svc_name = query.split()[0].lower()
        dummy_svc = ServiceInfo(port=0, protocol="tcp", name=svc_name, product=query, version="")
        dummy_hits = _run_single_search(query)
        dummy_result = ServiceResult(service=dummy_svc, hits=dummy_hits)
        print_exploit_summary([dummy_result], rhost)
        if rhost and dummy_hits:
            inject_exploit_tasks([dummy_result], rhost)
            print_msg("Task created in tasks.json — run 'tasks' to view")


    @cmd2.with_category(scanning_category)
    def do_wfuzz(self, line):
        """
        Uses `wfuzz` to perform fuzzing based on provided parameters. This function supports various options for directory and file fuzzing.

        :param line: The options and arguments for `wfuzz`. The `line` parameter can include the following:
            - `sub <domain>`: Fuzz DNS subdomains. Requires `dnswordlist` to be assign.
            - `iis`: Fuzz IIS directories. Uses a default wordlist if `iiswordlist` is not assign.
            - Any other argument: General directory and file fuzzing.

        :returns: None

        Manual execution:
        To manually use `wfuzz` for directory and file fuzzing, use the following commands:

        1. For fuzzing DNS subdomains:
            wfuzz -c <extra_options> -t <threads> -w <wordlist> -H 'Host: FUZZ.<domain>' <domain>

        Example:
            wfuzz -c --hl=7 -t 200 -w /path/to/dnswordlist -H 'Host: FUZZ.example.com' example.com

        2. For fuzzing IIS directories:
            wfuzz -c <extra_options> -t <threads> -w /path/to/iiswordlist http://<rhost>/FUZZ

        Example:
            wfuzz -c --hl=7 -t 200 -w /usr/share/wordlists/SecLists-master/Discovery/Web-Content/IIS.fuzz.txt http://10.10.10.10/FUZZ

        3. For general directory and file fuzzing:
            wfuzz -c <extra_options> -t <threads> -w <wordlist> http://<rhost>/FUZZ

        Example:
            wfuzz -c --hl=7 -t 200 -w /path/to/dirwordlist http://10.10.10.10/FUZZ
        """

        dirwordlist = self.params["dirwordlist"]
        choice = input("    [!] Enter the numer 1 to directory-list-2.3-medium.txt 2 to raft-large-words.txt [1/2] (Default 2): ") or '2'
        if choice == '2':
            dirwordlist = dirwordlist.replace("directory-list-2.3-medium.txt", "raft-large-words.txt")
        rhost = self.params["rhost"]
        url = self.params["url"]
        url = get_domain(url)
        choice = input(f"    [?] Use 1 to url or 2 to rhost (default {url})") or '1'
        if choice == '1':
            rhost = url
        if not rhost or not dirwordlist:
            print_error(f"dirwordlist and rhost must be assign{RESET}")
            return

        if line:
            if line.startswith("sub"):
                params = line.split(" ")
                count = len(params)
                dnswordlist = self.params["dnswordlist"]
                if not dnswordlist:
                    print_error(
                        "use payload or p to load the parameter from payload.json, or just assign dnswordlist path/to/dnswordlist"
                    )
                    return

                if count == 1:
                    print_error(
                        f"you must pass the dommain like argument ex:{GREEN} wfuzz sub box.htb"
                    )
                    return

                arg1 = params[0]
                domain = params[1]
                if count > 2:
                    arg3 = params[2]
                else:
                    arg3 = ""
                print_msg(
                    f"Try ...  wfuzz -c {arg3} -t 200 -w {dnswordlist} -H 'Host: FUZZ.{domain}' {domain} {RESET}"
                )
                self.cmd(
                    f"wfuzz -c {arg3} -t 200 -w {dnswordlist} -H 'Host: FUZZ.{domain}' {domain}"
                )
                return

            if line.startswith("iis"):
                params = line.split(" ")
                print_msg(params)
                count = len(params)
                arg1 = params[0]
                iiswordlist = "/usr/share/wordlists/SecLists-master/Discovery/Web-Content/IIS.fuzz.txt"  # dont know why this line dont work ... self.params['iiswordlist']

                if not os.path.exists(iiswordlist):
                    print_error(
                        f"you must have file iiswordlist use the command: getseclist, use p or payload to load parameters from payload.json, or just assign iiswordlist /pat/to/iiswordlist"
                    )
                    return
                # Abre el archivo en modo de lectura
                if count > 1:
                    arg3 = params[1]
                else:
                    arg3 = ""
                print_msg(
                    f"Try ...  wfuzz -c {arg3} -t 200 -w {iiswordlist} http://{rhost}/FUZZ {RESET}"
                )
                self.cmd(
                    f"wfuzz -c {arg3} -t 200 -w {iiswordlist} http://{rhost}/FUZZ"
                )
                return

        print_msg(
            f"Try ... wfuzz -c {line} -t 200 -w {dirwordlist} http://{rhost}/FUZZ {RESET}"
        )
        self.cmd(f"wfuzz -c {line} -t 200 -w {dirwordlist} http://{rhost}/FUZZ")
        return




__all__ = ["ReconCommandSet"]
