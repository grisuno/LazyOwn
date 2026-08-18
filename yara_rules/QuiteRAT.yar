rule QuiteRAT {
    meta:
        author = "ditekSHen"
        description = "Detects QuiteRAT"
        cape_type = "QuiteRAT Payload"
    strings:
        $x1 = "< No Pineapple! >" ascii // error message
        $x2 = ".?AVPineapple" ascii
        $x3 = ".?AVApple@@" ascii
        $s1 = "XgsdCwsRFxZF" ascii // http
        $s2 = "XggZChkVRQ==" ascii // http
        $s3 = "RxUZERQRHEU=" ascii // http
        $s4 = "XhkbDBEXFkU" ascii  // http
    condition:
        uint16(0) == 0x5a4d and ((all of ($x*) and 1 of ($s*)) or (1 of ($x*) and 3 of ($s*)))
}
