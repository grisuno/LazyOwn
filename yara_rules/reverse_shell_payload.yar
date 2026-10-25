
rule ReverseShell_Payload {
    meta:
        description = "Detects common reverse shell payloads"
        author = "LazyOwn"
        severity = "high"
        category = "payload"
    strings:
        $bash_tcp = "/dev/tcp/" ascii
        $nc_e = "nc -e" ascii wide
        $nc_nodns = "nc -n" ascii wide
        $python_socket = "socket.socket" ascii
        $powershell_rc = "Net.Sockets.TCPClient" ascii wide
        $powershell_stream = "GetStream()" ascii wide
        $sh_i = "sh -i" ascii
        $bash_i = "bash -i" ascii
    condition:
        (filesize < 100KB) and (2 of them)
}
