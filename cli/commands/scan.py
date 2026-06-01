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

import os
import subprocess

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    GREEN,
    RESET,
    check_rhost,
    copy2clip,
    get_domain,
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
            input(
                "    [!] Enter the numer 1 to directory-list-2.3-medium.txt 2 to raft-large-words.txt [1/2] (Default 2): "
            )
            or "2"
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
    def do_arpscan(self, line):
        """
        Executes an ARP scan using `arp-scan`.

        This function performs an ARP scan on the local network using the `arp-scan` tool. The network device to be used for scanning must be specified.

        Usage:
            arpscan

        :param line: Command parameters (not used in this function).
        :type line: str

        - Executes the `arp-scan` command with the specified network device.

        :returns: None

        Manual execution:
        1. Ensure that the network device is assign using the appropriate parameter.
        2. Run the method to perform an ARP scan.

        Dependencies:
        - `arp-scan` must be installed on the system.
        - The `sudo` command must be available for executing `arp-scan`.

        Examples:
            1. assign the device parameter using `assign device <network_device>`.
            2. Run `arpscan` to perform the ARP scan.

        Note:
            - The network device must be configured and available on the system for the scan to work.
            - Ensure that `arp-scan` is installed and accessible from the command line.
        """

        if not self.params["device"]:
            print_error("device must be assign")
            return
        device = self.params["device"]
        print_msg("try to arp-scan sudo arp-scan -I DEVICE --localnet")
        self.cmd(f"sudo arp-scan -I {device} --localnet")

    @cmd2.with_category(scanning_category)
    def do_dirsearch(self, line):
        """
        Runs the `dirsearch` tool to perform directory and file enumeration on a specified URL.

        This function executes `dirsearch` to scan a given URL for directories and files, while excluding specific HTTP status codes from the results. If `dirsearch` is not installed, the function will attempt to install it before running the scan.

        Usage:
            dirsearch <url>

        :param line: Not used in this function. The URL is provided via the `url` parameter.
        :type line: str
        :returns: None

        Manual execution:
        1. If `dirsearch` is present, the command `dirsearch -u <url> -x 403,404,400` is executed.
        2. If `dirsearch` is not present, the function installs `dirsearch` using `sudo apt install dirsearch -y` and then runs the command.

        Dependencies:
        - `dirsearch` must be installed. If not present, it will be installed using `sudo apt`.
        - Ensure the URL is assign via the `url` parameter before calling this function.

        Example:
            dirsearch http://example.com/

        Note:
            - Ensure that the `url` parameter is assign before calling this function.
            - The `-x` option specifies HTTP status codes to exclude from the results (e.g., 403, 404, 400).
            - The function will attempt to install `dirsearch` if it is not already installed.
        """

        url = self.params["url"]
        if not url:
            print_error("Url must be assign: use assign url http://url.ext/ more info in help assign")
            return
        if is_binary_present("dirsearch"):
            print_msg("[*] Try... dirsearch -u http://url.ext/ -x 403,404,400")
            self.cmd(f"dirsearch -u {url} -x 403,404,400")
        else:
            print_error("dirsearch is not installed, installing... (control + c to cancel)")
            self.cmd(f"sudo apt install dirsearch -y && dirsearch -u {url} -x 403,404,400")
        return

    @cmd2.with_category(scanning_category)
    def do_dmitry(self, line):
        """
        This function constructs and executes a command for the 'dmitry' tool.
        It first checks if the 'url' parameter is set. If not, it prints an error message.
        If the 'url' is set, it extracts the domain from the URL using the get_domain function.
        Then, it constructs a 'dmitry' command with the specified parameters and prepares it for execution.

        Run a domain whois lookup (w), an IP whois lookup (i), retrieve Netcraft info (n), search for subdomains (s), search for email addresses (e), do a TCP port scan (p), and save the output to example.txt (o) for the domain example.com:

        Parameters:
        line (str): The command line input for this function.

        Expected self.params keys:
        - url (str): The URL to be used for the 'dmitry' command.

        Example usage:
        - assign url http://example.com
        - do_dmitry
        """
        if not is_binary_present("dmitry"):
            print_warn("Installing dmitry...")
            self.cmd("sudo apt install dmitry -y")

        url = self.params["url"]
        if not url:
            print_error(f"Url must be assign use{GREEN} assign url http://example.com")
            return
        domain = get_domain(url)

        command = f"dmitry -winseo sessions/dmitry_{domain}.txt {domain}"
        print_msg(command)
        self.cmd(command)
        return

    @cmd2.with_category(scanning_category)
    def do_feroxbuster(self, line):
        """
        Command feroxbuster: Installs and runs Feroxbuster for performing forced browsing and directory brute-forcing.

        This function performs the following tasks:
        1. Installs Feroxbuster using a `curl` command if it's not already installed.
        2. Prompts the user for required inputs like the target URL, wordlist, file extensions, and additional options.
        3. Executes Feroxbuster for directory enumeration and brute-force attacks.

        Args:
            line (str): Optional argument for specifying the target URL, wordlist, and other Feroxbuster options.

        Returns:
            None

        Example:
            feroxbuster -u http://example.com -w wordlist.txt -x php,html
        """
        url = self.params["url"]
        wordlist = self.params["wordlist"]
        path = os.getcwd()

        exploit_dir = os.path.join(path, "external/.exploit")
        feroxbuster_url = "https://raw.githubusercontent.com/epi052/feroxbuster/main/install-nix.sh"
        feroxbuster_bin = os.path.join(os.getenv("HOME"), ".local/bin/feroxbuster")

        os.makedirs(exploit_dir, exist_ok=True)

        if not os.path.exists(feroxbuster_bin):
            print_msg("Installing Feroxbuster...")
            self.cmd(f"curl -sL {feroxbuster_url} | bash -s $HOME/.local/bin")
        else:
            print_msg("Feroxbuster already installed, skipping installation.")

        if not line:
            url = input(f"    {GREEN}[!] Enter the target URL (default: {url}): ").strip() or url
            wordlist = input(f"    [?] Enter the wordlist file (default: {wordlist}): ").strip() or wordlist
            extensions = input("    [?] Enter file extensions (comma-separated, optional): ").strip()
            headers = input("    [?] Enter additional headers (optional): ").strip()
            recursion = input("    [?] Enable recursion? (y/n, default 'y'): ").strip().lower() or "y"
            verbosity = input("    [?] Verbosity level (1-3, default '1'): ").strip() or "1"

        else:
            args = line.split()
            url = args[0] if len(args) > 0 else ""
            wordlist = args[1] if len(args) > 1 else ""
            extensions = args[2] if len(args) > 2 else ""
            headers = args[3] if len(args) > 3 else ""
            recursion = args[4] if len(args) > 4 else "y"
            verbosity = args[5] if len(args) > 5 else "1"

        if not url:
            print_warn("No URL provided, aborting scan.")
            return

        wordlist_option = f"-w {wordlist}" if wordlist else ""
        extensions_option = f"-x {extensions.replace(',', ' -x ')}" if extensions else ""
        headers_option = f"-H {headers}" if headers else ""
        recursion_option = "--no-recursion" if recursion == "n" else ""
        verbosity_option = f"-{'v' * int(verbosity)}"

        command = f"{feroxbuster_bin} -u {url} {wordlist_option} {extensions_option} {headers_option} {recursion_option} {verbosity_option}"

        print_msg(f"Running Feroxbuster scan: {command}")
        self.cmd(command)
        return

    @cmd2.with_category(scanning_category)
    def do_nmapscript(self, line):
        """Perform an Nmap scan using a specified script and port.

        :param line: A string containing the Nmap script and port, separated by a space. Example: "http-enum 80".

        :returns: None

        Manual execution:
        To manually run an Nmap scan with a script and port, use the following command format:

            nmap --script <script> -p <port> <target> -oN <output-file>

        Example:
        If you want to use the script `http-enum` on port `80` for the target `10.10.10.10`, you would run:

            nmap --script http-enum -p 80 10.10.10.10 -oN sessions/webScan_10.10.10.10

        Ensure you have the target host (`rhost`) assign in the parameters and provide the script and port as arguments. The results will be saved in the file `sessions/webScan_<rhost>`.
        """

        rhost = self.params["rhost"]
        if not check_rhost(rhost):
            return
        parts = line.split(" ", 2)
        if len(parts) != 2:
            print_error("Usage: nmapscript <script> <port>")
            return
        script = parts[0]
        port = parts[1]
        print_msg(f"Try... nmap -sCV --script {script} -p{port} {rhost} -oN sessions/{script}_{rhost}")
        self.cmd(f"nmap -sCV --script {script} -p{port} {rhost} -oN sessions/{script}_{rhost}")
        return

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
        choice = input("    [?] do you want use extra templates path: (y/n) ") or "y"
        if choice == "y":
            install = input("    [?] do you want clone extra templates repo: (y/n) ") or "y"
            if install == "y":
                self.cmd("cd .. && git clone https://github.com/projectdiscovery/nuclei-templates.git 2>/dev/null")
            path = input("    [!] Enter the path to templates (default ../nuclei-templates): ") or "../nuclei-templates"
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
    def do_amass(self, line):
        """
        Executes Amass to perform a passive enumeration on a given domain.

        This function performs the following steps:
        1. Executes the Amass tool with the provided domain for passive enumeration.
        2. Saves the results to a file named 'results.txt' in the current directory.

        Parameters:
        line (str): The domain to be enumerated, e.g., 'example.com'.

        Returns:
        None
        """
        if line:
            domain = line.strip()
        else:
            domain = self.params["domain"]
        if not domain:
            print_error("No domain provided. Please provide a valid domain to enumerate.")
            return

        command = f"amass enum -passive -d {domain} -o sessions/amass_{domain}_results.txt"
        print_msg(f"Running Amass for domain {domain}...")

        self.cmd(command)
        self.logcsv(f"amass {command}")
        print_msg(f"Amass enumeration completed. Results saved in sessions/amass_{domain}_results.txt.")

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
                input("    [!] Enter the mode (1 Subdomain, 2 Spider, 3 Email, 4 Web, 5 Web thorough, 6 All): ") or "6"
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

        if not os.path.exists(osmedeus_path):
            print_warn("Osmedeus is not installed. Cloning the repository and installing dependencies.")
            self.cmd(f"git clone {osmedeus_repo} {osmedeus_path}")
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

        scan_choice = input("    [!] Enter the number corresponding to your choice (default: 1): ").strip() or "1"
        flow = scan_types.get(scan_choice, "general").split()[0]
        domain = self.params["domain"]
        url = self.params["url"]
        target = input(f"    [!] Enter the target (e.g., {domain}, list_of_targets.txt): ").strip() or domain
        if not target:
            print_warn("A target is required to execute the scan.")
            return

        additional_params = ""
        if flow in ["cidr", "repo-scan"]:
            if flow == "cidr":
                additional_params = input(
                    "    [!] Enter CIDR format (e.g., 1.2.3.4/24) or leave empty for file input: "
                ).strip()
            elif flow == "repo-scan":
                additional_params = input(f"    [!] Enter the repository URL {url} or folder path: ").strip() or url

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
            target = input(f"Enter target domain default {url}: ").strip() or url
            mode = input("Enter mode option (-a, -p, -x, -r, -v, -m): ").strip() or "-a"
            notification = (
                input("Enable notifications via Discord, Telegram, or Slack? (yes/no): ").strip().lower() or "no"
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
        execute = input("Do you want to execute? (yes/no): ").strip().lower()
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
        execute = input("Do you want to execute? (yes/no): ").strip().lower()
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
        execute = input("Do you want to execute? (yes/no): ").strip().lower()
        if execute == "yes":
            self.cmd(command)
        else:
            copy2clip(command)
        return

    @cmd2.with_category(scanning_category)
    def do_skipfish(self, line):
        """
        This function executes the web security scanning tool Skipfish
        using the provided configuration and parameters. It allows
        scanning a specified target (rhost) and saves the results
        in a designated output directory.

        Parameters:
        - self: Refers to the instance of the class in which this function is defined.
        - line: A string that may contain additional options to modify the scanning behavior.

        Function Flow:
        1. Default values are set for the target IP (rhost), port (port), and output directory (outputdir).
        2. The validity of the target (rhost) is checked using the `check_rhost` function.
        3. If no argument is provided in `line`, a `skipfish` command is constructed using the default values.
        4. If `line` starts with 'url', the URL configured in `self.params['url']` is retrieved and used to construct the `skipfish` command.
        5. If the URL is not configured and an attempt is made to use the 'url' option, an error message is printed, and the function exits.
        6. The constructed `skipfish` command is displayed on the console and executed using `os.system`.

        Note:
        - The function assumes that the `skipfish` tool is installed on the system.
        - The output of the scan is saved in the directory `sessions/{rhost}/skipfish/`.
        - The wordlist used by Skipfish is specified in `wordlist`.
        """

        port = 80
        s = ""

        wordlist = "/usr/share/skipfish/dictionaries/complete.wl"
        rhost = self.params["rhost"]

        if not check_rhost(rhost):
            return
        outputdir = f"sessions/{rhost}/skipfish/"
        if not line:
            command = f"skipfish -o {outputdir} -S {wordlist} http{s}://{rhost}:{port}"
        else:
            if line.startswith("url"):
                url = self.params["url"]
                if not url:
                    print_error(
                        f"You need assign the url if use the parametter url ex: {GREEN}assign url http://url.ext/"
                    )
                    return
                command = f"skipfish -o {outputdir} -S {wordlist} {url}"
        print_msg(command)
        self.cmd(command)
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
        hosts = input("    [!] Enter the hosts to scan (comma-separated): ").strip() or rhost
        if not hosts:
            print_error("    [!] Hosts cannot be empty!")
            return

        ports = (
            input("    [!] Enter the ports to scan (comma-separated or range): ").strip()
            or "80,443,22,21,23,25,110,143,53,3306,8080,3389,135,139,445,993,995,1723,111,5900,1025,465,587,49152,49153,49154,49155,49156,49157,548,631,993,2049,444,5000,5060,5800,53,111,179,123,137,138,69,514,2049,520,162,4500"
        )

        output_file = input("    [!] Enter the output file : ").strip() or hosts.replace(",", "_")

        command = f"cd sessions && vscan -host {hosts} -p {ports} -v"

        if output_file:
            command += f" -json -o {output_file}.json"

        print_msg(f"Executing command: {command}")
        self.cmd(command)

        return


__all__ = ["ScanCommandSet"]
