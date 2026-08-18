rule Akira {
    meta:
        author = "ditekSHen"
        description = "Detects Akira Ransomware"
        cape_type = "Akira Payload"
    strings:
        $x1 = "https://akira" ascii
        $x2 = ":\\akira\\" ascii
        $x3 = ".akira" ascii
        $x4= "akira_readme.txt" ascii
        $x5 = "\\akira\\asio\\include\\asio\\impl\\co_spawn.hpp" ascii
        $s1 = "Get-WmiObject Win32_Shadowcopy | Remove-WmiObject" ascii
        $s2 = "Win32_ProcessStartup" fullword wide
        $s3 = /Failed\sto\smake\s(part|full|spot)\sencrypt/ ascii wide
        $s4 = "--encryption_" ascii
        $s5 = "--share_file" ascii
        $s6 = { 24 00 52 00 45 00 43 00 59 00 43 00 4C 00 45 00 2E 00 42 00 49 00 4E 00 00 00 00 00 6? 6? 6? 00 (24|57) 00 (52|69) 00 }
        $s7 = " PUBLIC KEY-----" ascii
        $s8 = ".onion" ascii
        $s9 = "/Esxi_Build_Esxi6/./" ascii nocase
        $s10 = "No path to encrypt" ascii
        $s11 = "-fork" fullword ascii
    condition:
        uint16(0) == 0x5a4d and (3 of ($x*) or (1 of ($x*) and 4 of ($s*)) or 6 of ($s*))
}
