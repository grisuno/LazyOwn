rule StrelaStealer {
    meta:
      author = "ditekSHen"
      description = "Detects StrelaStealer infostealer"
      cape_type = "StrelaStealer Payload"
    strings:
        $x1 = "strela" fullword ascii
        $s1 = "/server.php" fullword ascii
        $s2 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36" ascii
        $s3 = "SOFTWARE\\Microsoft\\Office\\16.0\\Outlook\\Profiles\\Outlook\\9375CFF0413111d3B88A00104B2A6676\\" ascii
        $s4 = "%s%s\\logins.json" fullword ascii
        $s5 = "%s%s\\key4.db" fullword ascii
        $s6 = /IMAP\s(Server|User|Password)/ fullword ascii
        $s7 = "\\Thunderbird\\Profiles\\" fullword ascii
        $s8 = "%s,%s,%s" fullword ascii
    condition:
        uint16(0) == 0x5a4d and ((1 of ($x*) and 1 of ($s*)) or (7 of ($s*)))
}
