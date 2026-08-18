rule ValidAlpha {
    meta:
        author = "ditekshen"
        description = "Detects ValidApha / BlackRAT"
        cape_type = "ValidAlpha Payload"
    strings:
        $x1 = "RAT/Black/" ascii
        $x2 = "RAT/Black/Client_Go/" ascii
        $s1 = "main.RunTask" fullword ascii
        $s2 = "main.CmdShell" fullword ascii
        $s3 = "main.SelfDelete" fullword ascii
        $s4 = "main.RecvPacket" fullword ascii
        $s5 = "main.FileDownload" fullword ascii
        $s6 = "main.CaptureScreen" fullword ascii
        $s7 = "main.PeekNamedPipe" fullword ascii
    condition:
        uint16(0) == 0x5a4d and ((1 of ($x*) and 2 of ($s*)) or (6 of ($s*)))
}
