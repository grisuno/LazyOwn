rule KoadicBAT {
    meta:
        author = "ditekshen"
        description = "Koadic post-exploitation framework BAT payload"
        cape_type = "KoadicBAT payload"
    strings:
        $v1_1 = "&@cls&@set" ascii
        $v2_1 = { 26 63 6c 73 0d 0a 40 25 }
        $m1 = /:~\d+,1%+/ ascii
    condition:
        uint16(0) == 0xfeff and ((1 of ($v1*) or 1 of ($v2*)) and #m1 > 100)
}
