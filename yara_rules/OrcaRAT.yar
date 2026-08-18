rule OracRAT {
    meta:
        author = "ditekSHen"
        description = "Detects OracRAT / Comfoo / Babar"
        cape_type = "OrcaRAT Payload"
    strings:
        $s1 = "\\\\.\\DevCtrlKrnl" fullword ascii
        $s2 = "SOFTWARE\\Microsoft\\IE4\\Setup" fullword ascii
        $s3 = "\\PLUGINS" fullword ascii
        $s4 = "\\config\\sam" fullword ascii
        $s5 = "\\iexplore.exe\" about:blank" fullword ascii
        $s6 = "usbak.sys" fullword ascii
        $s7 = "userctfm" fullword ascii
    condition:
        uint16(0) == 0x5a4d and 5 of them
}
