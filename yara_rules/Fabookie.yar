rule Fabookie {
     meta:
        author = "ditekSHen"
        description = "Detects Fabookie / ElysiumStealer"
        cape_type = "Fabookie Payload"
    strings:
        $s1 = "rwinssyslog" fullword wide
        $s2 = "_kasssperskdy" fullword wide
        $s3 = "[Title:%s]" fullword wide
        $s4 = "[Execute]" fullword wide
        $s5 = "[Snapshot]" fullword wide
        $s6 = "Mozilla/4.0 (compatible)" fullword wide
        $s7 = "d-k netsvcs" fullword wide
        $s8 = "facebook.websmails.com" fullword wide
        $s9 = "CUdpClient::Start" fullword ascii
    condition:
        (uint16(0) == 0x5a4d or uint16(0) == 0x0805) and 6 of them
}

rule Fabookie_01 {
    meta:
        author = "ditekSHen"
        description = "Detects Fabookie"
        cape_type = "Fabookie Payload"
    strings:
        $s1 = "\"%1\\control.exe\" ncpa.cpl%2" wide
        $s2 = "Elevation:Administrator!new:%s" wide
        $s3 = "quar_qclintfy_mtx" wide
        $s4 = "Software\\Microsoft\\NetworkAccessProtection\\UI\\Branding\\%" wide
        $s5 = "napagent" fullword wide
        $s6 = "napstat.pdb" fullword ascii
        /*
        $fk1 = "GetKeyState" fullword ascii // keystrokes capture
        $fs1 = "CreateCompatibleDC" // screen capture
        $fs2 = "CreateCompatibleBitmap"  // screen capture
        $fs3 = "GetSystemMetrics" // screen capture
        */
    condition:
        uint16(0) == 0x5a4d and 4 of ($s*)
        //uint16(0) == 0x5a4d and 4 of ($s*) or (2 of ($s*) and 1 of ($fk1) and 2 of ($fs2))
}
