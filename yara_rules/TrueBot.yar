rule TrueBot {
    meta:
        author = "ditekSHen"
        description = "Detects TrueBot"
        cape_type = "TrueBot Payload"
    strings:
        $s1 = "%s\\rundll32.exe" fullword wide
        $s2 = "ChkdskExs" fullword wide
        $s3 = "n=%s&o=%s&a=%d&u=%s&p=%s&d=%s" ascii
        $s4 = "KLLS" fullword ascii
        $s5 = "%s\\%08x-%08x.ps1" fullword ascii
        $s6 = ".JSONIP" ascii
        $s7 = "CreateProcessAsUserW res %d err %d" fullword ascii
        $s8 = "ldr_sys64.dll" fullword ascii
        $s9 = "SVCHOST" fullword ascii
        $s10 = "WINLOGON" fullword ascii
        $s11 = { 67 6f 6f 67 6c 65 2e 63 6f 6d 00 00 00 00 00 00 
                2f 00 63 00 20 00 64 00 65 00 6c 00 20 00 00 00 
                20 00 3e 00 3e 00 20 00 4e 00 55 00 4c 00 }
    condition:
        uint16(0) == 0x5a4d and 6 of them
}
