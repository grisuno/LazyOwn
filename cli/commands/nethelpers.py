"""Network helpers extracted from the miscellaneous cluster.

Pending status: originals deleted from ``cli/commands/misc_migrated.py``;
this set is registered by ``cli.registry``.
"""

from __future__ import annotations

import base64

import cmd2

from cli.commands._base import LazyOwnCommandSet

__all__ = ["NetworkHelpersCommandSet"]


class NetworkHelpersCommandSet(LazyOwnCommandSet):
    """Network helpers."""

    phase = "misc"
    category = "12. Miscellaneous"

    @cmd2.with_category("12. Miscellaneous")
    def do_ip(self, line):
        """
        Displays IP addresses of network interfaces and copies the IP address from the `tun0` interface to the clipboard.

        This function performs the following tasks:
        1. Displays IP addresses for all network interfaces using `ip a show scope global` and `awk`.
        2. Copies the IP address from the `tun0` interface to the clipboard using `xclip`.

        Usage:
            ip

        :param line: This parameter is not used in the function but is included for consistency with other command methods.
        :type line: str
        :returns: None

        Manual execution:
        1. The command `ip a show scope global | awk '/^[0-9]+:/ { sub(/:/,"",$2); iface=$2 } /^[[:space:]]*inet / { split($2, a, "/"); print "    [\033[96m" iface"\033[0m] "a[1] }'` is executed to display the IP addresses of all network interfaces.
        2. The IP address of the `tun0` interface is copied to the clipboard using the command `ip a show tun0 | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1 | xclip -sel clip`.

        Dependencies:
        - The function relies on `awk`, `grep`, `cut`, and `xclip` to process and copy the IP address.

        Example:
            ip
            # This will display IP addresses for all network interfaces and copy the IP address from `tun0` to the clipboard.

        Note:
            Ensure that the `tun0` interface exists and has an IP address assigned. If `tun0` is not present or has no IP address, the clipboard will not be updated.
        """

        try:
            result = subprocess.run(
                ["ip", "a", "show", "scope", "global"],
                capture_output=True, text=True, timeout=5, check=False,
            )
            current_iface = ""
            for line in result.stdout.splitlines():
                stripped = line.strip()
                if stripped and stripped[0].isdigit() and ":" in stripped:
                    parts = stripped.split(":", 2)
                    if len(parts) >= 2:
                        current_iface = parts[1].strip().rstrip("@")
                elif stripped.startswith("inet ") and current_iface:
                    addr = stripped.split()[1].split("/")[0]
                    print(f"    [\033[96m{current_iface}\033[0m] {addr}")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        try:
            result = subprocess.run(
                ["ip", "a", "show", "tun0"],
                capture_output=True, text=True, timeout=5, check=False,
            )
            for line in result.stdout.splitlines():
                stripped = line.strip()
                if stripped.startswith("inet "):
                    clipboard_ip = stripped.split()[1].split("/")[0]
                    break
            else:
                clipboard_ip = ""
        except (FileNotFoundError, subprocess.TimeoutExpired):
            clipboard_ip = ""

        print_msg(f"IP from tun0 copied to clipboard :) {RESET}")
        lhost = self.params['lhost']
        if not check_lhost(self.params['lhost']):
            return
        if clipboard_ip and clipboard_ip != self.params['lhost']:
            lhost = clipboard_ip
            self.onecmd(f"assign self.params['lhost'] {clipboard_ip}")
            self.custom_prompt = getprompt()

            print_msg(f"Updated self.params['lhost'] to {clipboard_ip}")
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_ipp(self, line):
        """
        Displays IP addresses of network interfaces and prints the IP address from the `tun0` interface.

        This function performs the following tasks:
        1. Displays IP addresses for all network interfaces using `ip a show scope global` and `awk`.
        2. Prints the IP address from the `tun0` interface.

        Usage:
            ip

        :param line: This parameter is not used in the function but is included for consistency with other command methods.
        :type line: str
        :returns: None

        Manual execution:
        1. The command `ip a show scope global | awk '/^[0-9]+:/ { sub(/:/,"",$2); iface=$2 } /^[[:space:]]*inet / { split($2, a, "/"); print "    [\033[96m" iface"\033[0m] "a[1] }'` is executed to display the IP addresses of all network interfaces.
        2. The IP address of the `tun0` interface is printed to the console using the command `ip a show tun0 | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1`.

        Dependencies:
        - The function relies on `awk`, `grep`, `cut`, and `xclip` to process and display the IP address.

        Example:
            ip
            # This will display IP addresses for all network interfaces and print the IP address from `tun0`.

        Note:
            Ensure that the `tun0` interface exists and has an IP address assigned. If `tun0` is not present or has no IP address, the address will not be displayed.
        """

        try:
            result = subprocess.run(
                ["ip", "a", "show", "scope", "global"],
                capture_output=True, text=True, timeout=5, check=False,
            )
            current_iface = ""
            for line in result.stdout.splitlines():
                stripped = line.strip()
                if stripped and stripped[0].isdigit() and ":" in stripped:
                    parts = stripped.split(":", 2)
                    if len(parts) >= 2:
                        current_iface = parts[1].strip().rstrip("@")
                elif stripped.startswith("inet ") and current_iface:
                    addr = stripped.split()[1].split("/")[0]
                    print(f"    [\033[96m{current_iface}\033[0m] {addr}")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        try:
            result = subprocess.run(
                ["ip", "a", "show", "tun0"],
                capture_output=True, text=True, timeout=5, check=False,
            )
            ip_address = ""
            for line in result.stdout.splitlines():
                stripped = line.strip()
                if stripped.startswith("inet "):
                    ip_address = stripped.split()[1].split("/")[0]
                    break


        except subprocess.CalledProcessError:
            print_error("Error retrieving IP address from tun0.")

        # Optionally update self.params['lhost']
        lhost = self.params['lhost']
        if ip_address and ip_address != self.params['lhost']:
            lhost = ip_address
            # Example of how you might set the new self.params['lhost']
            self.params['lhost'] = self.params['lhost']

            print_msg(f"Updated self.params['lhost'] to {self.params['lhost']}")

        return

    @cmd2.with_category("12. Miscellaneous")
    def do_rhost(self, line):
        """
        Copies the remote host (self.params['rhost']) to the clipboard and updates the command prompt.

        This function performs two tasks:
        1. It copies the `self.params['rhost']` parameter to the clipboard if it is valid.
        2. It updates the command prompt to include the `self.params['rhost']` and the current working directory.

        Usage:
            self.params['rhost'] [clean]

        :param line: An optional argument that determines the behavior of the function:
            - If 'clean', it resets the command prompt to its default format.
            - If any other value, it updates the command prompt to include the `self.params['rhost']` and current working directory.
        :type line: str
        :returns: None

        Manual execution:
        1. If `line` is 'clean':
        - The command prompt is reset to its default format.
        2. If `line` is any other value:
        - The command prompt is updated to show the `self.params['rhost']` and the current working directory.
        - The `self.params['rhost']` is copied to the clipboard using `xclip`.

        Dependencies:
        - The script uses `xclip` to copy the `self.params['rhost']` to the clipboard.

        Example:
            self.params['rhost']
            # This will copy the current `self.params['rhost']` to the clipboard and update the prompt.

            self.params['rhost'] clean
            # This will reset the command prompt to its default format.

        Note:
            Ensure that the `self.params['rhost']` is valid by checking it with the `check_rhost` function before copying it to the clipboard.
        """
        url   = self.params['url']
        rhost = self.params['rhost']
        if not check_rhost(self.params['rhost']):
            return
        if not url:
            print_error("url must be assign, use: assign url http://host.ext")
            return
        self.refresh_prompt()
        if line != 'clean':
            from core.hardening import safe_clipboard_copy
            safe_clipboard_copy(self.params.get('rhost', ''))
            print_msg(f"ip from payload: {rhost=}, copied to clipboard :) {RESET}")
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_rrhost(self, line):
        """
        Updates the command prompt to include the remote host (self.params['rhost']) and current working directory.

        This function performs two tasks:
        1. It updates the command prompt to include the `self.params['rhost']` and the current working directory if `line` is not 'clean'.
        2. It resets the command prompt to its default format if `line` is 'clean'.

        Usage:
            self.params['rhost'] [clean]

        :param line: An optional argument that determines the behavior of the function:
            - If 'clean', it resets the command prompt to its default format.
            - If any other value, it updates the command prompt to include the `self.params['rhost']` and current working directory.
        :type line: str
        :returns: None

        Manual execution:
        1. If `line` is 'clean':
        - The command prompt is reset to its default format.
        2. If `line` is any other value:
        - The command prompt is updated to show the `self.params['rhost']` and the current working directory.

        Example:
            self.params['rhost']
            # This will update the command prompt to include the `self.params['rhost']` and current working directory.

            self.params['rhost'] clean
            # This will reset the command prompt to its default format.

        Note:
            Ensure that the `self.params['rhost']` is valid by checking it with the `check_rhost` function before updating the prompt.
        """
        if not check_rhost(self.params['rhost']):
            return

        self.refresh_prompt()

        return

    @cmd2.with_category("12. Miscellaneous")
    def do_addhosts(self, line):
        """
        Adds an entry to the `/etc/hosts` file, mapping an IP address to a domain name.

        :param line: The domain name to be added to the `/etc/hosts` file.
            - Example: `permx.htb`

        :returns: None

        Manual execution:
        To manually add a domain to the `/etc/hosts` file, use the following command:

            sudo sh -c -e "echo '<rhost> <domain>' >> /etc/hosts"

        Example:
            sudo sh -c -e "echo '10.10.11.23 permx.htb' >> /etc/hosts"

        This command appends the IP address and domain name to the `/etc/hosts` file, enabling local resolution of the domain.
        """
        self.onecmd("PTMultiTools")

        return

    @cmd2.with_category("12. Miscellaneous")
    def do_ip2asn(self, line):
        """Command to get ASN for a given IP address."""
        path = os.getcwd()
        file = f"{path}/sessions/ip2asn-v4.tsv.gz"

        url = "https://github.com/pl-strflt/iptoasn/raw/main/data/ip2asn-v4.tsv.gz"
        if not os.path.exists(file):
            command = f"curl -o {file} {url}"
            self.cmd(command)
        self.ip2asn.open_file(file)
        rhost = self.params['rhost']

        if line:
            target = line.strip()
        else:
            print_warn("Usage: ip2asn <IP>")
            target = self.params['rhost']

        ip = target
        asn = self.ip2asn.as_of_ip(ip)
        if asn == 0:
            print_warn(f"IP {ip} not found in any ASN records.")
        else:

            as_name = self.ip2asn.as_name.get(asn, "Unknown")
            as_country = self.ip2asn.as_country.get(asn, "Unknown")
            print_msg(f"IP {ip} is part of ASN {asn} ({as_name}, {as_country})")
        self.logcsv(f"ip2asn {line}")

    @cmd2.with_category("12. Miscellaneous")
    def do_ignorearp(self, line):
        """
        Configures the system to ignore ARP requests by setting a kernel parameter.

        This function performs the following tasks:
        1. Prints a message indicating the command that will be executed.
        2. Executes the command `echo 1 > /proc/sys/net/ipv4/conf/all/arp_ignore` with elevated privileges using `sudo` to configure the system to ignore ARP requests.
        3. Prints a confirmation message indicating that the operation is complete.

        Usage:
            ignorearp

        :param line: This parameter is not used in the function but is included for consistency with other command methods.
        :type line: str
        :returns: None

        Manual execution:
            1. The command `sudo bash -c 'echo 1 > /proc/sys/net/ipv4/conf/all/arp_ignore'` is executed to assign the `arp_ignore` parameter to `1`, which configures the system to ignore ARP requests.

        Dependencies:
            - The function requires `sudo` to run the command with elevated privileges.

        Example:
            ignorearp
            # This will assign the `arp_ignore` parameter to `1` to ignore ARP requests.

        Note:
            Ensure that you have the necessary permissions to use `sudo` and that the `arp_ignore` parameter can be modified on your system.
        """
        print_msg(
            f"Try... sudo bash -c 'echo {CYAN}1 {RED}> {GREEN}/proc/sys/net/ipv4/conf/all/arp_ignore'{RESET}"
        )
        self.cmd("sudo bash -c 'echo 1 > /proc/sys/net/ipv4/conf/all/arp_ignore'")
        print_msg(f"    {GREEN}[+] Done.{RESET}")
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_ignoreicmp(self, line):
        """
        Configures the system to ignore ICMP echo requests by setting a kernel parameter.

        This function performs the following tasks:
        1. Prints a message indicating the command that will be executed.
        2. Executes the command `echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all` with elevated privileges using `sudo` to configure the system to ignore ICMP echo requests (ping).
        3. Prints a confirmation message indicating that the operation is complete.

        Usage:
            ignoreicmp

        :param line: This parameter is not used in the function but is included for consistency with other command methods.
        :type line: str
        :returns: None

        Manual execution:
            1. The command `sudo bash -c 'echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all'` is executed to assign the `icmp_echo_ignore_all` parameter to `1`, which configures the system to ignore ICMP echo requests (ping).

        Dependencies:
            - The function requires `sudo` to run the command with elevated privileges.

        Example:
            ignoreicmp
            # This will assign the `icmp_echo_ignore_all` parameter to `1` to ignore ICMP echo requests.

        Note:
            Ensure that you have the necessary permissions to use `sudo` and that the `icmp_echo_ignore_all` parameter can be modified on your system.
        """
        print_msg(
            f"Try... sudo bash -c 'echo {CYAN}1 {RED}> {GREEN}/proc/sys/net/ipv4/icmp_echo_ignore_all'{RESET}"
        )
        self.cmd("sudo bash -c 'echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all'")
        print_msg(f"Done.{RESET}")
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_acknowledgearp(self, line):
        """
        Configures the system to acknowledge ARP requests by setting a kernel parameter.

        This function performs the following tasks:
        1. Prints a message indicating the command that will be executed.
        2. Executes the command `echo 0 > /proc/sys/net/ipv4/conf/all/arp_ignore` with elevated privileges using `sudo` to configure the system to acknowledge ARP requests.
        3. Prints a confirmation message indicating that the operation is complete.

        Usage:
            acknowledgearp

        :param line: This parameter is not used in the function but is included for consistency with other command methods.
        :type line: str
        :returns: None

        Manual execution:
            1. The command `sudo bash -c 'echo 0 > /proc/sys/net/ipv4/conf/all/arp_ignore'` is executed to assign the `arp_ignore` parameter to `0`, which configures the system to acknowledge ARP requests.

        Dependencies:
            - The function requires `sudo` to run the command with elevated privileges.

        Example:
            acknowledgearp
            # This will assign the `arp_ignore` parameter to `0` to acknowledge ARP requests.

        Note:
            Ensure that you have the necessary permissions to use `sudo` and that the `arp_ignore` parameter can be modified on your system.
        """
        print_msg(
            f"Try... sudo bash -c 'echo {CYAN}0 {RED}> {GREEN}/proc/sys/net/ipv4/conf/all/arp_ignore'{RESET}"
        )
        self.cmd("sudo bash -c 'echo 0 > /proc/sys/net/ipv4/conf/all/arp_ignore'")
        print_msg(f"Done.{RESET}")
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_acknowledgeicmp(self, line):
        """
        Configures the system to respond to ICMP echo requests by setting a kernel parameter.

        This function performs the following tasks:
        1. Prints a message indicating the command that will be executed.
        2. Executes the command `echo 0 > /proc/sys/net/ipv4/icmp_echo_ignore_all` with elevated privileges using `sudo` to configure the system to respond to ICMP echo requests.
        3. Prints a confirmation message indicating that the operation is complete.

        Usage:
            acknowledgeicmp

        :param line: This parameter is not used in the function but is included for consistency with other command methods.
        :type line: str
        :returns: None

        Manual execution:
            1. The command `sudo bash -c 'echo 0 > /proc/sys/net/ipv4/icmp_echo_ignore_all'` is executed to assign the `icmp_echo_ignore_all` parameter to `0`, which configures the system to respond to ICMP echo requests.

        Dependencies:
            - The function requires `sudo` to run the command with elevated privileges.

        Example:
            acknowledgeicmp
            # This will assign the `icmp_echo_ignore_all` parameter to `0` to allow responses to ICMP echo requests.

        Note:
            Ensure that you have the necessary permissions to use `sudo` and that the `icmp_echo_ignore_all` parameter can be modified on your system.
        """
        print_msg(
            f"Try... sudo bash -c 'echo {CYAN}0 {RED}> {GREEN}/proc/sys/net/ipv4/icmp_echo_ignore_all'{RESET}"
        )
        self.cmd("sudo bash -c 'echo 0 > /proc/sys/net/ipv4/icmp_echo_ignore_all'")
        print_msg(f"Done.{RESET}")
        return


import utils as _lazy_utils

for _lazy_name in dir(_lazy_utils):
    if not _lazy_name.startswith('_'):
        globals().setdefault(_lazy_name, getattr(_lazy_utils, _lazy_name))
del _lazy_utils, _lazy_name


def __getattr__(name: str):
    """Fall back to ``utils`` for bare-name references used by migrated commands."""
    import utils as _utils
    try:
        return getattr(_utils, name)
    except AttributeError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None
