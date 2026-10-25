rule Prynt {
    meta:
        author = "ditekSHen"
        description = "Detects Prynt infostealer"
        cape_type = "Prynt Payload"
    strings:
        $c1 = /Prynt(\s)?Stealer/ ascii wide
        $x2 = "@FlatLineStealer" ascii wide
        $x3 = "@CashOutGangTalk" ascii wide
        $m1 = ".Passwords.Targets." ascii
        $m2 = ".Modules.Keylogger" ascii
        $m3 = ".Modules.Clipper" ascii
        $m4 = ".Modules.Implant" ascii
        $s1 = "--- Clipper" wide
        $s2 = "Downloading file: \"{file}\"" wide
        $s3 = "/bot{0}/getUpdates?offset={1}" wide
        $s4 = "send command to bot!" wide
        $s5 = " *Keylogger " fullword wide
        $s6 = "*Stealer" wide
        $s7 = "Bot connected" wide
    condition:
        uint16(0) == 0x5a4d and 1 of ($c*) and (1 of ($x*) or 2 of ($m*) or 3 of ($s*))
}
