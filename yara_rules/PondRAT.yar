rule PondRAT {
    meta:
        author = "ditekshen"
        description = "Detects PondRAT"
        cape_type = "PondRAT Payload"
    strings:
        $s1 = "MsgDown" ascii
        $s2 = "MsgUp" ascii
        $s3 = "MsgRun" ascii
        $s4 = "MsgCmd" ascii
        $s5 = "CryptPayload" ascii
        $s6 = "RecvPayload" ascii
        $s7 = "csleepi" ascii
        $s8 = "FConnectProxy" ascii
    condition: 
        (uint16(0) == 0x457f or uint16(0) == 0xfacf or uint16(0) == 0xfeca) and 7 of them
}
