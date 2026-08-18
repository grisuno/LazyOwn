rule DarkEye {
    meta:
        author = "ditekSHen"
        description = "Detects DarkEye infostealer"
        cape_type = "DarkEye Payload"
    strings:
        $c1 = /Prynt(\s)?Stealer/ ascii wide
        $c2 = /WorldWind(\s)?Stealer/ ascii wide
        $c3 = "ToxicEye" ascii wide
        $x2 = "@FlatLineStealer" ascii wide
        $x3 = "@CashOutGangTalk" ascii wide
        $s1 = "--- Clipper" wide
        $s2 = "Downloading file: \"{file}\"" wide
        $s3 = "/bot{0}/getUpdates?offset={1}" wide
        $s4 = "send command to bot!" wide
        $s5 = " *Keylogger " fullword wide
        $s6 = "*Stealer" wide
        $s7 = "Bot connected" wide
    condition:
        uint16(0) == 0x5a4d and not any of ($c*) and ((1 of ($x*) and 2 of ($s*)) or (4 of ($s*)))
}
