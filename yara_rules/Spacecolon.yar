rule Spacecolon {
    meta:
        author = "ditekSHen"
        description = "Detects Spacecolon ransomware"
        cape_type = "Spacecolon Payload"
    strings:
        $s1 = "eraseext" fullword ascii
        $s2 = "*.encrypted" fullword ascii
        $s3 = "TIMATOMA#" fullword wide
        $s4 = ".Encrypted" fullword wide
        $s5 = "Already Encrypted" wide
        $s6 = "note.txt" fullword wide
        $s7 = "HOW TO RECOVERY FILES.TXT" fullword wide
        $s8 = "taskkill /f /im \"" wide nocase
        $s9 = "\\kill.bat" wide
        $s10 = "Search cancelled -" fullword wide
        $s11 = "%d folder(s) searched and %d file(s) found - %.3f second(s)" fullword wide
        $s12 = "Our TOX ID :" ascii
        $s13 = "tufhackteam@gmail.com" ascii
    condition:
        uint16(0) == 0x5a4d and 8 of them
}
