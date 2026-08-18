rule CyberStealer {
    meta:
        author = "ditekSHen"
        description = "Detects CyberStealer infostealer"
        cape_type = "CyberStealer Payload"
    strings:
        $x1 = "\\Cyber Stealer\\" ascii
        $s1 = "[Virtualization]" fullword wide
        $s2 = "\"encryptedPassword\":\"([^\"]+)\"" fullword wide
        $s3 = "CreditCard" fullword ascii
        $s4 = "DecryptPassword" fullword ascii
        $s5 = "_modTime" fullword ascii
        $s6 = "_pathname" fullword ascii
        $s7 = "_pathnameInZip" fullword ascii
        $s8 = "GetBookmarksDBPath" fullword ascii
        $s9 = "GrabberImages" fullword ascii
        $r1 = "^1[a-km-zA-HJ-NP-Z1-9]{25,34}$" wide // Crypto Wallet Address
        $r2 = "^3[a-km-zA-HJ-NP-Z1-9]{25,34}$" wide // Crypto Wallet Address
        $r3 = "^([a-zA-Z0-9_\\-\\.]+)@([a-zA-Z0-9_\\-\\.]+)\\.([a-zA-Z]{2,5})$" wide
        $r4 = "^(?!:\\/\\/)([a-zA-Z0-9-_]+\\.)*[a-zA-Z0-9][a-zA-Z0-9-_]+\\.[a-zA-Z]{2,11}?$" wide
    condition:
        uint16(0) == 0x5a4d and ((1 of ($x*) and (2 of ($s*) or 2 of ($r*))) or 7 of ($s*) or (5 of ($s*) and 2 of ($r*)) or (all of ($r*) and 4 of ($s*)))
}
