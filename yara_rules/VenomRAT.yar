rule VenomRAT {
    meta:
        author = "ditekSHen"
        description = "Detects VenomRAT"
        cape_type = "VenomRAT Payload"
    strings:
        $x1 = "Venom RAT + HVNC" fullword ascii
        $x2 = "Venom" fullword ascii
        $x3 = "VenomByVenom" fullword wide
        $s1 = "/c schtasks /create /f /sc onlogon /rl highest /tn \"" fullword wide
        $s2 = "UmVjZWl2ZWQ" wide
        $s3 = "Pac_ket" fullword wide
        $s4 = "Po_ng" fullword wide
    condition:
        uint16(0) == 0x5a4d and (1 of ($x*) and 2 of ($s*))
}

rule venomrat_kingrat {
    meta:
        author = "jeFF0Falltrades"
        cape_type = "VenomRAT Payload"
    strings:
        $str_id_venomrat = "venomrat" wide ascii nocase
        $str_hvnc = "HVNC_REPLY_MESSAGE" wide ascii
        $str_offline_keylogger = "OfflineKeylog sending...." wide ascii
        $str_videocontroller = "select * from Win32_VideoController" wide ascii
        $byte_aes_key_base = { 7E [3] 04 73 [3] 06 80 }
        $patt_config = { 72 [3] 70 80 [3] 04 }
        $patt_keylog = {73 [3] 06 80 [3] 04}
        $patt_verify_hash = { 7e [3] 04 6f [3] 0a 6f [3] 0a 74 [3] 01 }

    condition:
        5 of them and #patt_config >= 10
}
