rule POOLRAT {
    meta:
        author = "ditekshen"
        description = "Detects POOLRAT"
        cape_type = "POOLRAT Payload"
    strings:
        $s1 = "MSG_CmdP" ascii
        $s2 = "MSG_WriteConfigP" ascii
        $s3 = "MSG_SecureDelP" ascii
        $s4 = "ConnectToProxyP" ascii
        $s5 = "MSG_KeepConP" ascii
        $s6 = "MSG_SleepP" ascii
        $s7 = "MSG_TestP" ascii
        $s8 = "MSG_SetPathP" ascii
    condition: 
        (uint16(0) == 0x457f or uint16(0) == 0xfacf or uint16(0) == 0xfeca) and 7 of them
}
