rule Bagle {
    meta:
        author = "ditekSHen"
        description = "Detect Bagle / Beagle email worm"
        cape_type = "Bagle Payload"
    strings:
        $s1 = "SOFTWARE\\DateTime" fullword ascii
        $s2 = "%s?p=%lu" fullword ascii
        $s3 = "-upd" ascii
        $s4 = "[%RAND%]" fullword ascii
        $s5 = "MAIL FROM:<%s>" fullword ascii
        $s6 = "RCPT TO:<%s>" fullword ascii
        $s7 = "Message-ID: <%s%s>" fullword ascii
        $s8 = "Content-Disposition: attachment; filename=\"%s%s\"" fullword ascii
        $s9 = "http://www.%s" fullword ascii
    condition:
        uint16(0) == 0x5a4d and 8 of them
}
