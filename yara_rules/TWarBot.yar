rule TWarBot {
    meta:
        author = "ditekSHen"
        description = "Detect TWarBot IRC Bot"
        cape_type = "TWarBot Payload"
    strings:
        $x1 = "TWarBot" fullword ascii
        $s1 = "PRIVMSG #" ascii
        $s2 = "C:\\marijuana.txt" fullword ascii
        $s3 = "C:\\rar.bat" fullword ascii
        $s4 = "C:\\zip.bat" fullword ascii
        $s5 = "software\\microsoft\\windows\\currentversion\\app paths\\winzip32.exe" ascii
        $s6 = "software\\microsoft\\windows\\currentversion\\app paths\\WinRAR.exe" ascii
        $s7 = "a -idp -inul -c- -m5" ascii
    condition:
        uint16(0) == 0x5a4d and ((1 of ($x*) and 3 of ($s*)) or 5 of ($s*))
}
