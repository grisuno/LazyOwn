rule AgentRacoon {
    meta:
        author = "ditekShen"
        description = "Detects AgentRacoon"
        cape_type = "AgentRacoon Payload"
    strings:
        $s1 = "UdpClient" fullword ascii
        $s2 = "IPEndPoint" fullword ascii
        $s3 = "get_Client" fullword ascii
        $s4 = "set_ReceiveTimeout" fullword ascii
        $s5 = "Command failed:" wide
        $s6 = "uploaded" wide
        $s7 = "downloaded" wide
        $s8 = ".telemetry." wide
        $s9 = "xn--" wide
    condition:
      uint16(0) == 0x5a4d and 7 of them
}
