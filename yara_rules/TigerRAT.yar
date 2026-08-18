rule TigerRAT {
    meta:
        author = "ditekshen"
        description = "Detects TigerRAT"
        cape_type = "TigerRAT Payload"
    strings:
        $m0 = ".?AVCryptorRC4@@" fullword ascii
        $m1 = ".?AVModuleShell@@" fullword ascii
        $m2 = ".?AVModuleKeyLogger@@" fullword ascii
        $m3 = ".?AVModuleSocksTunnel@@" fullword ascii
        $m4 = ".?AVModuleScreenCapture@@" fullword ascii
        $m5 = ".?AVModulePortForwarder@@" fullword ascii
        $s1 = "\\x9891-009942-xnopcopie.dat" fullword wide
        $s2 = "(%02d : %02d-%02d %02d:%02d:%02d)--- %s[Clipboard]" fullword ascii
        $s3 = "[%02d : %02d-%02d %02d:%02d:%02d]--- %s[Title]" fullword ascii
        $s4 = "~KPTEMP" fullword wide
        $s5 = "del \"%s\"%s \"%s\" goto " ascii
    condition:
        uint16(0) == 0x5a4d and ((all of ($s*)) or (5 of ($m*)) or (3 of ($m*) and 2 of ($s*)) or (5 of them))
}
