rule SolarMarker {
    meta:
        author = "ditekSHen"
        description = "Detects SolarMarker"
        cape_type = "SolarMarker Payload"
    strings:
        $x1 = "token_type" fullword ascii
        $x2 = "request_data" fullword ascii
        $x3 = "request_timeout" fullword ascii
        $x4 = { 74 6f 6b 65 6e 73 00 66 72 6f 6d 00 74 6f 00 73 5f (66|72) }
        $s1 = "set_UseShellExecute" fullword ascii
        $s2 = "<Select>b__0" fullword ascii
        $s3 = "<get>b__e" fullword ascii
        $s4 = "<get>b__10" fullword ascii
        $s5 = "<get>b__f" fullword ascii
        $s6 = "<set>b__0" fullword ascii
        $s7 = "<set>b__1" fullword ascii
    condition:
        uint16(0) == 0x5a4d and (all of ($x*) and 4 of ($s*))
}
