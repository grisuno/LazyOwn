rule RisePro {
    meta:
        author = "ditekShen"
        description = "Detects RisePro infostealer"
        cape_type = "RisePro Payload"
    strings:
        $x1 = "t.me/riseprosupport" ascii wide nocase
        $s1 = "failed readpacket" fullword wide
        $s2 = "faield sendpacket" fullword wide
        $s3 = "PersistWal" fullword wide
        $s4 = /CRED_ENUMERATE_(ALL|SESSION)_CREDENTIALS/ fullword ascii
        $s5 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36" fullword wide
        $s6 = { 4c 00 6f 00 67 00 69 00 6e 00 20 00 44 00 61 00 
                74 00 61 [10] 57 00 65 00 62 00 20 00 44 00 61 00
                74 00 61 [2] 48 00 69 00 73 00 74 00 6f 00 72 00
                79 [21] 43 00 6f 00 6f 00 6b 00 69 00 65 00 73 }
        $s7 = { 61 00 70 00 70 00 6c 00 69 00 63 00 61 00 74 00
                69 00 6f 00 6e 00 2f 00 78 00 2d 00 77 00 77 00
                77 00 2d 00 66 00 6f 00 72 00 6d 00 2d 00 75 00
                72 00 6c 00 65 00 6e 00 63 00 6f 00 64 00 65 00
                64 00 3b 00 20 00 63 00 68 00 61 00 72 00 73 00
                65 00 74 00 3d 00 75 00 74 00 66 00 2d 00 38 00
                42 61 00 70 00 70 00 6c 00 69 00 63 00 61 00 74
                00 69 00 6f 00 6e 00 2f 00 6a 00 73 00 6f 00 6e
                00 2c 00 20 00 74 00 65 00 78 00 74 00 2f 00 70
                00 6c 00 61 00 69 00 6e 00 2c 00 20 00 2a 00 2f
                00 2a }
        $s8 = /_(SET|GET)_(GRABBER|LOADER)/ wide
        $s9 = /catch (save )?(windows cred|screen|pluginscrypto|historyCC|autofill|cookies|passwords|passwords sql|autofills sql|dwnlhistory sql|discordToken|quantum|isDropped)/ fullword wide
    condition:
        uint16(0) == 0x5a4d and (1 of ($x*) or 6 of ($s*))
}
