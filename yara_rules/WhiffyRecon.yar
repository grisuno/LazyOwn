rule WhiffyRecon {
    meta:
        author = "ditekSHen"
        description = "Detects Whiffy Recon"
        cape_type = "WhiffyRecon Payload"
    strings:
        $s1 = "WLANSVC" fullword wide
        $s2 = "f02fe1c0-137a-4802-8881-55dd300c5022" fullword wide
        $s3 = "\\wlan.lnk" fullword wide
        $s4 = "str-12.bin" wide
        $s5 = "/geolocation/v1/geolocate?key=" wide
        $s6 = "/wlan" fullword wide
        $s7 = "/scanned" fullword wide
        $s8 = "/bots/" fullword wide
        $s9 = "wlan.pdb" fullword ascii
        $s10 = "botId" fullword ascii
        $s11 = "wifiAccessPoints" fullword ascii
        $s12 = "considerIp" fullword ascii
        $s13 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36" fullword wide
    condition:
        uint16(0) == 0x5a4d and 5 of them
}
