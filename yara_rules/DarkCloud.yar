rule DarkCloud {
    meta:
        author = "ditekSHen"
        description = "Detects DarkCloud infostealer"
        cape_type = "DarkCloud Payload"
    strings:
        $x1 = "=DARKCLOUD=" wide
        $x2 = "#DARKCLOUD#" wide
        $x3 = "DARKCLOUD" wide
        $s1 = "DC-Creds" fullword wide
        $s2 = "shell.application" fullword wide
        $s3 = "VBSQLite3.dll" ascii wide nocase
        $s4 = "getbinaryvalue" fullword wide
        $s5 = "sqlite_exec" fullword ascii
        $i1 = "RegWrite" fullword wide
        $i2 = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" wide
        $i3 = "\\Templates\\Stub\\Project" wide
        $i4 = "\\Credentials" wide
        $i5 = "SELECT " wide
        $i6 = "\\163MailContacts.txt" fullword wide
    condition:
        uint16(0) == 0x5a4d and ((1 of ($x*) and (3 of ($s*) or 3 of ($i*))) or (all of ($s*) and 1 of ($i*)) or (4 of ($s*) and 4 of ($i*)))
}
