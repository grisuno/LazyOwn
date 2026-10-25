rule AbubasbanditBot {
    meta:
        author = "ditekSHen"
        description = "Detects Abubasbandit Bot"
        cape_type = "AbubasbanditBot Payload"
    strings:
        $x1 = "magickeycmd" ascii
        $x2 = "chat_id" ascii
        $x3 = "GetTempPathW" ascii
        $x4 = "Add-MpPreference" ascii
        $x5 = "-Command" ascii
        $s1 = "application/x-www-form-urlencoded" ascii
        $s2 = "gzip, deflate/index.html" ascii
        $s3 = "powershellAdd-MpPreference -ExclusionPath" ascii
        $s4 = "tar-xf-C" ascii
        $s5 = "temp_file.bin" ascii
    condition:
        uint16(0) == 0x5a4d and (all of ($x*) or (4 of ($x*) and 2 of ($s*)) or ((all of ($s*) and 3 of ($x*))) or (8 of them))
}
