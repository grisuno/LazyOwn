rule PovertyStealer {
    meta:
        author = "ditekSHen"
        description = "Detects PovertyStealer"
        cape_type = "PovertyStealer Payload"
    strings:
        $x1 = "Poverty is the parent of crime." ascii
        $s2 = "OperationSystem: %d:%d:%d" ascii
        $s3 = "ScreenSize: {lWidth=%d, lHeight=%d}" ascii
        $s4 = "VideoAdapter #%d: %s" ascii
        $s5 = "$d.log" fullword wide
    condition:
        ((uint16(0) == 0x5a4d and (1 of ($x*) or all of ($s*))) or all of them)
}
