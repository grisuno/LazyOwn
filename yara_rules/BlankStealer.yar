rule BlankStealer {
    meta:
        author = "ditekSHen"
        description = "Detects BlankStealer / BlankGrabber / Blank-c Stealer"
        cape_type = "BlankStealer Payload"
    strings:
        $s1 = "Blank-c" ascii
        $s2 = "Stealer License" ascii
        $s3 = "UID=" ascii
        $h1 = { 42 6c 61 6e 6b 2d 63 0a 53 74 65 61 6c 65 72 20 4c 69 63 65 6e 73 65 0a 55 49 44 3d }
    condition:
        (uint16(0) == 0x4152 and 2 of them) or (all of ($s*) or 1 of ($h*))
}
