rule GetCrypt {
    meta:
        author = "ditekshen"
        description = "GetCrypt ransomware payload"
        cape_type = "GetCrypt payload"
    strings:
        $x1 = "delete shadows /all /quiet" wide
        $x2 = "C:\\Windows\\System32\\svchost.exe" fullword wide
        $x3 = "desk.bmp" fullword wide
        $x4 = ":\\Boot" fullword wide
        $x5 = "\\encrypted_key.bin" fullword wide
        $x6 = "vssadmin.exe" fullword wide
        $x7 = ":\\Recovery" fullword wide
        $s1 = "CryptEncrypt" fullword ascii
        $s2 = "NtWow64ReadVirtualMemory64" fullword ascii
        $s3 = "MPR.dll" fullword ascii
        $s4 = "%key%" fullword ascii
        $s5 = "CryptDestroyKey" fullword ascii
        $s6 = "ntdll.dll" fullword ascii
        $s7 = "WNetCancelConnection2W" fullword ascii
        $s8 = ".%c%c%c%c" fullword wide
        $s9 = /([Gg]uest|[Aa]dmin(istrator)?|[Dd]eveloper)/ fullword ascii wide
        // /[Rr][0Oo]t/ is slowing down scanning
        $r0 = "R00t" fullword ascii wide
        $r1 = "R0Ot" fullword ascii wide
        $r2 = "R0ot" fullword ascii wide
        $r3 = "RO0t" fullword ascii wide
        $r4 = "ROOt" fullword ascii wide
        $r5 = "ROot" fullword ascii wide
        $r6 = "Ro0t" fullword ascii wide
        $r7 = "RoOt" fullword ascii wide
        $r8 = "Root" fullword ascii wide
        $r9 = "r00t" fullword ascii wide
        $r10 = "r0Ot" fullword ascii wide
        $r11 = "r0ot" fullword ascii wide
        $r12 = "rO0t" fullword ascii wide
        $r13 = "rOOt" fullword ascii wide
        $r14 = "rOot" fullword ascii wide
        $r15 = "ro0t" fullword ascii wide
        $r16 = "roOt" fullword ascii wide
        $r17 = "root" fullword ascii wide
        $s10 = { 43 72 79 70 74 49 6d 70 6f 72 74 4b 65 79 00 00
                 cb 00 43 72 79 70 74 45 6e 63 72 79 70 74 00 00
                 c1 00 43 72 79 70 74 41 63 71 75 69 72 65 43 6f
                 6e 74 65 78 74 41 00 00 c8 00 43 72 79 70 74 44
                 65 73 74 72 6f 79 4b 65 79 00 d2 00 43 72 79 70
                 74 47 65 6e 52 61 6e 64 6f 6d 00 00 c2 00 43 72
                 79 70 74 41 63 71 75 69 72 65 43 6f 6e 74 65 78
                 74 57 00 00 41 44 56 41 50 49 33 32 2e 64 6c 6c
                 00 00 b5 01 53 68 65 6c 6c 45 78 65 63 75 74 65
                 45 78 57 00 53 48 45 4c 4c 33 32 2e 64 6c 6c 00 }
    condition:
        uint16(0) == 0x5a4d and (3 of ($x*) or 8 of ($s*) or (7 of ($s*) and 1 of ($r*)))
}
