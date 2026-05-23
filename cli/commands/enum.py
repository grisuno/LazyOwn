"""Enumeration command set.

Service enumeration commands: SMB, RPC, LDAP quick checks, and related
impacket tools.
"""

from __future__ import annotations

import os

import cmd2

from cli.commands._base import LazyOwnCommandSet
from core.validators import check_lhost
from utils import (
    GREEN,
    RESET,
    check_rhost,
    copy2clip,
    exploitation_category,
    get_credentials,
    get_domain,
    get_hash,
    get_users_dic,
    print_error,
    print_msg,
    scanning_category,
)


class EnumCommandSet(LazyOwnCommandSet):
    """Enumeration phase commands."""

    phase = "enum"
    category = "02. Scanning & Enumeration"

    @cmd2.with_category(scanning_category)
    def do_smbclient(self, line):
        """
        Interacts with SMB shares using the `smbclient` command to perform the following operations:

        1. Checks if `rhost` (remote host) and `lhost` (local host) are assign; if not, an error message is displayed.
        2. If `line` (share name) is provided:
        - Attempts to access the specified SMB share on the remote host using the command: `smbclient -N \\\\{rhost}\\{line}`
        3. If `line` is not provided:
        - Lists available SMB shares on the remote host with the command: `smbclient -N -L \\\\{rhost}`
        4. Suggests a potential SMB exploit if possible by mounting the share from the local host using: `mount -t cifs "//{lhost}/share" /mnt/smb`

        :param line: The name of the SMB share to access on the remote host. If not provided, the function will list all available shares.
        :returns: None
        """

        rhost = self.params["rhost"]
        lhost = self.params["lhost"]
        path_cred = "sessions/credentials.txt"
        url = self.params["url"]
        domain = get_domain(url)
        if not check_rhost(rhost):
            return

        if not check_lhost(lhost):
            return

        if not os.path.exists(path_cred):
            if line:
                nargs = len(line.split(" "))
                if nargs == 1:
                    print_msg(f"Try .. smbclient -N \\\\{rhost}\\\\{line} {RESET}")
                    self.cmd(f"smbclient -N \\\\\\\\{rhost}\\\\{line}")
                    return
                if nargs == 2:
                    args = line.split(" ")
                    directorio = args[0]
                    user = args[1]
                    print_msg(f"Try .. smbclient \\\\{rhost}\\\\{directorio} -U {user} {RESET}")
                    self.cmd(f"smbclient \\\\\\\\{rhost}\\\\{directorio} -U {user} ")
                    return

            print_msg(f"Perform this command: smbclient -N -L \\\\{rhost}\\ {RESET}")
            self.cmd(f"smbclient -N -L \\\\{rhost}\\")
            print_msg(
                f'Exploit smb if is posible mount -t cifs -o rw,username=guest,password= "//{rhost}/share" /mnt/smb '
            )
            print_msg(
                'find /mnt/smb -type d -exec sh -c \'touch "$0/x" 2>/dev/null && echo "$0 is writable" && rm "$0/x"\' {} \\;'
            )

            return
        else:
            with open(path_cred, "r") as file:
                for file_line in file:
                    params = file_line.split(":")
                    user = params[0]
                    passwd = params[1].replace("\n", "")
                    command = f"smbclient -L //{domain}/{line} -U '{domain}\\\\{user}'"
                    copy2clip(passwd)
                    print_msg(command)
                    self.cmd(command)
                    print_msg(
                        f'Exploit smb if is posible mount -t cifs -o rw,username=guest,password= "//{rhost}/share" /mnt/smb '
                    )
                    print_msg(
                        'find /mnt/smb -type d -exec sh -c \'touch "$0/x" 2>/dev/null && echo "$0 is writable" && rm "$0/x"\' {} \\;'
                    )
                    return

    @cmd2.with_category(scanning_category)
    def do_smbclient_impacket(self, line):
        """
        Interacts with SMB shares using the `smbclient` command to perform the following operations:

        1. Checks if `rhost` (remote host) and `lhost` (local host) are assign; if not, an error message is displayed.
        2. If `line` (share name) is provided:
        - Attempts to access the specified SMB share on the remote host using the command: `smbclient -N \\\\{rhost}\\{line}`
        3. If `line` is not provided:
        - Lists available SMB shares on the remote host with the command: `smbclient -N -L \\\\{rhost}`
        4. Suggests a potential SMB exploit if possible by mounting the share from the local host using: `mount -t cifs "//{lhost}/share" /mnt/smb`

        :param line: The name of the SMB share to access on the remote host. If not provided, the function will list all available shares.
        :returns: None
        """

        rhost = self.params["rhost"]
        lhost = self.params["lhost"]
        path_cred = "sessions/credentials.txt"
        url = self.params["url"]
        get_domain(url)
        if not check_rhost(rhost):
            return

        if not check_lhost(lhost):
            return

        if not os.path.exists(path_cred):
            if line:
                nargs = len(line.split(" "))
                if nargs == 1:
                    print_msg(f"Try .. impacket-smbclient -N \\\\{rhost}\\\\{line} {RESET}")
                    self.cmd(f"impacket-smbclient -N \\\\\\\\{rhost}\\\\{line}")
                    return
                if nargs == 2:
                    args = line.split(" ")
                    directorio = args[0]
                    user = args[1]
                    print_msg(f"Try .. impacket-smbclient \\\\{rhost}\\\\{directorio} -U {user} {RESET}")
                    self.cmd(f"impacket-smbclient \\\\\\\\{rhost}\\\\{directorio} -U {user} ")
                    return

            print_msg(f"Perform this command: impacket-smbclient -N -L \\\\{rhost}\\ {RESET}")
            self.cmd(f"impacket-smbclient -N -L \\\\{rhost}\\")
            print_msg(
                f'Exploit smb if is posible mount -t cifs -o rw,username=guest,password= "//{rhost}/share" /mnt/smb '
            )
            print_msg(
                'find /mnt/smb -type d -exec sh -c \'touch "$0/x" 2>/dev/null && echo "$0 is writable" && rm "$0/x"\' {} \\;'
            )

            return
        else:
            with open(path_cred, "r") as file:
                for file_line in file:
                    params = file_line.split(":")
                    user = params[0]
                    passwd = params[1].replace("\n", "")
                    command = f"impacket-smbclient {user}@{rhost}"
                    copy2clip(passwd)
                    print_msg(command)
                    self.cmd(command)
                    print_msg(
                        f'Exploit smb if is posible mount -t cifs -o rw,username=guest,password= "//{rhost}/share" /mnt/smb '
                    )
                    print_msg(
                        'find /mnt/smb -type d -exec sh -c \'touch "$0/x" 2>/dev/null && echo "$0 is writable" && rm "$0/x"\' {} \\;'
                    )
                    return

    @cmd2.with_category(scanning_category)
    def do_smbclient_py(self, line):
        """
        Interacts with SMB shares using the `smbclient.py` command to perform the following operations:

        1. Checks if `rhost` (remote host) and `lhost` (local host) are assign; if not, an error message is displayed.
        2. If `line` (share name) is provided:
        - Attempts to access the specified SMB share on the remote host using the command: `smbclient.py -N \\\\{rhost}\\{line}`
        3. If `line` is not provided:
        - Lists available SMB shares on the remote host with the command: `smbclient.py -N -L \\\\{rhost}`
        4. Suggests a potential SMB exploit if possible by mounting the share from the local host using: `mount -t cifs "//{lhost}/share" /mnt/smb`

        :param line: The name of the SMB share to access on the remote host. If not provided, the function will list all available shares.
        :returns: None
        """

        rhost = self.params["rhost"]
        lhost = self.params["lhost"]
        path_cred = "sessions/credentials.txt"
        url = self.params["url"]
        get_domain(url)
        if not check_rhost(rhost):
            return

        if not check_lhost(lhost):
            return

        if not os.path.exists(path_cred):
            print_error(f"You need credentialts use:{GREEN} createcredentials admin:admin")
            return
        else:
            with open(path_cred, "r") as file:
                for file_line in file:
                    params = file_line.split(":")
                    user = params[0]
                    passwd = params[1].replace("\n", "")
                    command = f"smbclient.py {user}:'{passwd}'@{rhost}"
                    print_msg(command)
                    self.cmd(command)
                    print_msg(
                        f'Exploit smb if is posible mount -t cifs -o rw,username=guest,password= "//{rhost}/share" /mnt/smb '
                    )
                    print_msg(
                        'find /mnt/smb -type d -exec sh -c \'touch "$0/x" 2>/dev/null && echo "$0 is writable" && rm "$0/x"\' {} \\;'
                    )
                    return

    @cmd2.with_category(scanning_category)
    def do_smbmap(self, line):
        """smbmap -H 10.10.10.3 [OPTIONS]
        Uses the `smbmap` tool to interact with SMB shares on a remote host:

        1. Checks if `rhost` (remote host) and `lhost` (local host) are assign; if not, an error message is displayed.
        2. If no `line` (share name or options) is provided:
        - Attempts to access SMB shares on the remote host with a default user `deefbeef` using the command: `smbmap -H {rhost} -u 'deefbeef'`
        3. If `line` is provided:
        - Executes `smbmap` with the specified options or share name using the command: `smbmap -H {rhost} -R {line}`
        4. Suggests a potential SMB exploit if possible by mounting the share from the local host using: `mount -t cifs "//{lhost}/documents" /mnt/smb`

        :param line: Options or share name to use with `smbmap`. If not provided, uses a default user to list shares.
        :returns: None"""
        rhost = self.params["rhost"]
        lhost = self.params["lhost"]
        domain = self.params["domain"]
        path = os.getcwd()
        path_cred = f"{path}/sessions/credentials.txt"
        if not check_rhost(rhost):
            return

        if not check_lhost(lhost):
            return

        if not os.path.exists(path_cred):
            if not line:
                print_msg(f"Try... smbmap -H {rhost} -u 'deefbeef'")
                self.cmd(f"smbmap -H {rhost} -u 'deefbeef'")
                return
            else:
                if line.startswith("hash"):
                    username = input("    [!] Enter a valid username (default: henry.vinson): ") or "henry.vinson"
                    domain = input(f"    [!] Enter a valid domain (default: {domain}): ") or domain
                    rhost = input(f"    [!] Enter a valid host (default: {rhost}): ") or rhost
                    hashis = get_hash()

                    command = f"smbmap -u {username} -d {domain} -p '{hashis}' -H {rhost}"
                    print_msg(command)
                    self.cmd(command)
                    return
                else:
                    print_msg(f"Try... smbmap -H {rhost} -R {line}")
                    self.cmd(f"smbmap -H {rhost} -R {line}")
                    print_msg(
                        f'exploit smb if is posible mount -t cifs -o rw,username=guest,password= "//{rhost}/documents" /mnt/smb '
                    )
                    print_msg(
                        'find /mnt/smb -type d -exec sh -c \'touch "$0/x" 2>/dev/null && echo "$0 is writable" && rm "$0/x"\' {} \\;'
                    )
                    return
        else:
            path_cred = get_credentials(True)
            try:
                if_execute = input(f"    {GREEN}[?] Do you wanna try exec commands (y/n)") or "n"
            except EOFError:
                if_execute = "n"
            if if_execute == "y":
                execute = " -x "
                command_try = input(f"    {GREEN}[!] Enter the command to try (default: whoami): ") or "whoami"
                execute += command_try
            else:
                if_search = input(f"    {GREEN}[?] Do you wanna try search files (y/n)") or "n"
                if if_search == "y":
                    execute = " -A "

                    command_try = (
                        input(
                            f"    {GREEN}[!] Enter the share for potentially interesting files [default: (xlsx|docx|txt|xml)]: "
                        )
                        or "(xlsx|docx|txt|xml)"
                    )
                    execute += f"'{command_try}' -R"
                else:
                    execute = ""

            with open(path_cred, "r") as file:
                for file_line in file:
                    params = file_line.split(":")
                    user = params[0]
                    passwd = params[1].replace("\n", "")

            if len(execute) == 0:
                if line:
                    command = f"smbmap -u {user} -p {passwd} -H {rhost} -R {line}"
                    copy2clip(passwd)
                    print_msg(command)
                    self.cmd(command)
                    print_msg(
                        f'Exploit smb if is posible mount -t cifs -o rw,username=guest,password= "//{rhost}/share" /mnt/smb '
                    )
                    print_msg(
                        'find /mnt/smb -type d -exec sh -c \'touch "$0/x" 2>/dev/null && echo "$0 is writable" && rm "$0/x"\' {} \\;'
                    )
                    return
                else:
                    command = f"smbmap -u {user} -p {passwd} -H {rhost}"
                    copy2clip(passwd)
                    print_msg(command)
                    self.cmd(command)
                    print_msg(
                        f'Exploit smb if is posible mount -t cifs -o rw,username=guest,password= "//{rhost}/share" /mnt/smb '
                    )
                    print_msg(
                        'find /mnt/smb -type d -exec sh -c \'touch "$0/x" 2>/dev/null && echo "$0 is writable" && rm "$0/x"\' {} \\;'
                    )
                    return
            else:
                command = f"cd sessions && smbmap -u {user} -p {passwd} -d {domain} -H {rhost} {execute}"
                print_msg(command)
                self.cmd(command)
                print_msg(
                    f'Exploit smb if is posible mount -t cifs -o rw,username=guest,password= "//{rhost}/share" /mnt/smb '
                )
                print_msg(
                    'find /mnt/smb -type d -exec sh -c \'touch "$0/x" 2>/dev/null && echo "$0 is writable" && rm "$0/x"\' {} \\;'
                )
                return
        return

    @cmd2.with_category(scanning_category)
    def do_getnpusers(self, line):
        """sudo impacket-GetNPUsers mist.htb/ -no-pass -usersfile sessions/users.txt
        Executes the `impacket-GetNPUsers` command to enumerate users with Kerberos pre-authentication disabled.

        1. Checks if the `line` (domain) argument is provided; if not, an error message is displayed, instructing the user to provide a domain.
        2. Executes `impacket-GetNPUsers` with the following options:
        - `-no-pass`: Skips password prompt.
        - `-usersfile sessions/users.txt`: Specifies the file containing the list of users to check.

        :param line: The domain to query. Must be provided in the format `domain.com`. Example usage: `getnpusers domain.com`
        :returns: None

        Manual execution:
        To manually run this command, use the following syntax:
            sudo impacket-GetNPUsers <domain> -no-pass -usersfile sessions/users.txt
        Replace `<domain>` with the actual domain name you want to query."""

        rhost = self.params["rhost"]
        domain = self.params["domain"]
        if not line:
            users = get_users_dic()
            command = f"GetNPUsers.py {domain}/ -no-pass -usersfile {users} -dc-ip {rhost}"
            print_msg(command)
            self.cmd(command)
            command = f"sudo impacket-GetNPUsers {domain}/ -no-pass -usersfile {users} -dc-ip {rhost}"
            print_msg(command)
            self.cmd(command)
        else:
            if line.startswith("hashs"):
                hashes = get_users_dic()
                username = input("   [!] Enter username to sprayhashes (default: admin) ") or "admin"
                with open(hashes, "r") as file:
                    hashes = file.readlines()
                    for hash_line in hashes:
                        hash_line = hash_line.strip()
                        if hash_line:
                            command = f"GetNPUsers.py -hashes {hash_line} {domain}/{username} -dc-ip {rhost}"
                            print_msg(command)
                            self.cmd(command)
                            # choice = input("    [!] Continue ? (y/n)") or "n"
                            # if choice == "n":
                            #    return
        return

    @cmd2.with_category(exploitation_category)
    def do_psexec(self, line):
        """
        Executes the Impacket PSExec tool to attempt remote execution on the specified target.

        This function performs the following actions:
        1. Checks if the provided target host (`rhost`) is valid.
        2. If the `line` argument is "pass", it searches for credential files with the pattern `credentials*.txt`
        and allows the user to select which file to use for executing the command.
        3. If the `line` argument is not "pass", it assumes execution without a password (using the current credentials).
        4. Copies the `rhost` IP address to the clipboard for ease of use.

        Parameters:
        line (str): A command argument to determine the action.
                    If "pass", the function searches for credential files and authenticates using the selected file.
                    Otherwise, it executes PSExec without a password using the `rhost` IP.

        Returns:
        None
        """
        rhost = self.params["rhost"]

        if not check_rhost(rhost):
            return

        if line == "pass":
            credentials = get_credentials()
            if not credentials:
                return

            for user, passwd in credentials:
                command = f"impacket-psexec {user}:'{passwd}'@{rhost}"
                print_msg(command)
                self.cmd(command)
            return

        elif line == "hash":
            hash_value = get_hash()
            if not hash_value:
                return
            if ":" in hash_value:
                hashis = f"-hashes {hash_value}"
            else:
                hashis = f"-hashes :{hash_value}"

            user = input("    [!] Enter Username (default: Administrator): ") or "Administrator"
            command = f"impacket-psexec {user}@{rhost} {hashis}"
            print_msg(command)
            self.cmd(command)
            return
        else:
            command = f"impacket-psexec administrator@{rhost}"
            print_msg(command)
            self.cmd(command)
        return

    @cmd2.with_category(exploitation_category)
    def do_psexec_py(self, line):
        """
        Executes the Impacket PSExec tool to attempt remote execution on the specified target.

        This function performs the following actions:
        1. Checks if the provided target host (`rhost`) is valid.
        2. If the `line` argument is "pass", it searches for credential files with the pattern `credentials*.txt`
        and allows the user to select which file to use for executing the command.
        3. If the `line` argument is not "pass", it assumes execution without a password (using the current credentials).
        4. Copies the `rhost` IP address to the clipboard for ease of use.

        Parameters:
        line (str): A command argument to determine the action.
                    If "pass", the function searches for credential files and authenticates using the selected file.
                    Otherwise, it executes PSExec without a password using the `rhost` IP.

        Returns:
        None
        """
        rhost = self.params["rhost"]

        if not check_rhost(rhost):
            return

        if line == "pass":
            credentials = get_credentials()
            if not credentials:
                return

            for user, passwd in credentials:
                command = f"psexec.py {user}:'{passwd}'@{rhost}"
                print_msg(command)
                self.cmd(command)
            return

        elif line == "hash":
            hash_value = get_hash()
            if not hash_value:
                return
            if ":" in hash_value:
                hashis = f"-hashes {hash_value}"
            else:
                hashis = f"-hashes :{hash_value}"

            user = input("    [!] Enter Username (default: Administrator): ") or "Administrator"
            command = f"psexec.py {user}@{rhost} {hashis}"
            print_msg(command)
            self.cmd(command)
            return
        else:
            command = f"psexec.py administrator@{rhost}"
            print_msg(command)
            self.cmd(command)
        return

    @cmd2.with_category(scanning_category)
    def do_rpcdump(self, line):
        """
        Executes the `rpcdump.py` script to dump RPC services from a target host.

        1. Retrieves the target host IP from the `rhost` parameter.
        2. Checks if the `rhost` parameter is valid using `check_rhost()`. If invalid, the function returns early.
        3. Executes the `rpcdump.py` script on port 135 and 593 to gather RPC service information from the target host.

        :param line: This parameter is not used in this command but is included for consistency with other methods.
        :returns: None

        Manual execution:
        To manually run this command, use the following syntax:
            rpcdump.py -p 135 <target_host>
            rpcdump.py -p 593 <target_host>
        Replace `<target_host>` with the IP address or hostname of the target machine.
        """
        rhost = self.params["rhost"]
        if check_rhost(rhost):
            print_msg(f"Try... rpcdump.py -p 135 {rhost}{RESET}")
            self.cmd(f"rpcdump.py -p 135 {rhost}")
            print_msg(f"Try... rpcdump.py -p 593 {rhost}{RESET}")
            self.cmd(f"rpcdump.py -p 593 {rhost}")
        return

    @cmd2.with_category(scanning_category)
    def do_enum4linux(self, line):
        """
        Performs enumeration of information from a target Linux/Unix system using `enum4linux`.

        1. Executes the `enum4linux` command with the `-a` option to gather extensive information from the specified target.

        :param line: This parameter is not used in the current implementation but could be used to pass additional options or arguments if needed.
        :param rhost: The target host for enumeration, specified in the `params` dictionary.

        :returns: None

        Manual execution:
        To manually enumerate information from a Linux/Unix system, use the following command:
            enum4linux -a <target_host>

        Replace `<target_host>` with the IP address or hostname of the target system.

        For example:
            enum4linux -a 192.168.1.10
        """

        if not self.params["rhost"]:
            print_msg("rhost must be assign")
            return
        rhost = self.params["rhost"]
        print_msg(f"Try... enum4linux -a {rhost} {RESET}")
        self.cmd(f"enum4linux -a {rhost}")
        return

    @cmd2.with_category(scanning_category)
    def do_rpcclient(self, line):
        """
        Executes the `rpcclient` command to interact with a remote Windows system over RPC (Remote Procedure Call) using anonymous credentials.

        1. Runs `rpcclient` with the `-U ''` (empty username) and `-N` (no password) options to connect to the target host specified by `rhost`.

        :param line: This parameter is not used in the current implementation but could be used to specify additional options or arguments if needed.
        :param rhost: The IP address of the remote host to connect to, specified in the `params` dictionary.

        :returns: None

        Manual execution:
        To manually interact with a remote Windows system using RPC, use the following command:
            rpcclient -U '' -N <target_ip>

        Replace `<target_ip>` with the IP address of the target system. For example:
            rpcclient -U '' -N 10.10.10.10
        """

        if not self.params["rhost"]:
            print_error(f"rhost must be assign{RESET}")
            return
        rhost = self.params["rhost"]
        domain = self.params["domain"]
        adomain = domain.split(".")
        machine = adomain[0]
        if not line:
            path_cred = "sessions/credentials.txt"

            if not os.path.exists(path_cred):
                command = f"rpcclient -U '' -N {rhost}"
                print_msg(f"Try... {GREEN} {command} {RESET}")
                self.cmd(command)

            else:
                with open(path_cred, "r") as file:
                    for file_line in file:
                        params = file_line.split(":")
                        username = params[0]
                        password = params[1].replace("\n", "")
                        command = f"rpcclient -U {machine}/{username}%{password}  {rhost}"
                        print_msg(f"Try... {GREEN} {command} {RESET}")
                        self.cmd(command)

        else:
            command = f"rpcclient -U {machine}/{line} {rhost}"
            print_msg(f"Try... {GREEN} {command} {RESET}")
            self.cmd(command)
        return


__all__ = ["EnumCommandSet"]
