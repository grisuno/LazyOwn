rule GreetingGhoul {
    meta:
        author = "ditekSHen"
        description = "Detects GreetingGhoul Cryptocurrency Infostealer"
        cape_type = "GreetingGhoul Payload"
    strings:
        $s1 = "peer_list" fullword ascii
        $s2 = "seed_hash" fullword ascii
        $s3 = "pool_id" fullword ascii
        $s4 = "%smutex=%s:%lu" ascii
        $s5 = "miner.cfg" fullword ascii
        $s6 = "{\"method\": \"%s\"%s}" ascii
        $s7 = "/app/manager/%s" ascii
        $s8 = "X-VNC-STATUS" fullword ascii
        $s9 = "%s\\%lu.zip" fullword ascii
        $s10 = "\\??\\%programdata%\\" wide
    condition:
        uint16(0) == 0x5a4d and 6 of them
}
