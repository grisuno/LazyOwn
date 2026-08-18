rule Stealerium {
    meta:
        author = "ditekSHen"
        description = "Detects Stealerium infostealer"
        cape_type = "Stealerium Payload"
    strings:
        $x1 = "Stealerium" ascii wide
        $x2 = /\.Target\.(Passwords|Messengers|Browsers|VPN|Gaming)\./ ascii
        $x3 = /\.Modules\.(Keylogger|Implant|Passwords|Messengers|Browsers|VPN|Gaming|Clipper)\./ ascii
        $s1 = "Timeout /T 2 /Nobreak" fullword wide
        $s2 = "Directory not exists" wide
        $s3 = "### {0} ### ({1})" wide
        $s4 = /---\s(AntiAnalysis|WebcamScreenshot|Keylogger|Clipper)/ wide
        $s5 = " *Keylogger " fullword wide
    condition:
        uint16(0) == 0x5a4d and (all of ($x*) or (2 of ($x*) and all of ($s*)))
}
