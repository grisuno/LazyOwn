rule RageStealer {
    meta:
        author = "ditekShen"
        description = "Detect Rage / Priv8 infostealer"
        cape_type = "Rage Payload"
    strings:
        $x1 = "\\RageStealer\\obj\\" ascii
        $x2 = "Priv8 Stealer" wide
        $s1 = "\\Screen.png" wide
        $s2 = "Content-Disposition: form-data; name=\"document\"; filename=\"{1}\"" wide
        $s3 = "NEW LOG FROM" wide
        $s4 = "GRABBED SOFTWARE" wide
        $s5 = "DOMAINS DETECTED" wide
        $s6 = "snder" ascii
    condition:
        uint16(0) == 0x5a4d and (1 of ($x*) and 4 of ($s*))
}
