rule GraphicalProton_rsockstun {
    meta:
        author = "ditekShen"
        description = "Detects GraphicalProton custom rsockstun"
        cape_type = "GraphicalProton Payload"
    strings:
        $m1 = "main.connectviaproxy" ascii
        $m2 = "main.connectForSocks" ascii
        $m3 = "main.listenForClients" ascii
        $m4 = "main.listenForSocks" ascii
        $s1 = "Proxy-Authorization: NTLM TlRMTVNTUAABAAAABoIIAAAAAAAAAAAAAAAAAAAAAAA=" ascii
        $s2 = "Server: nginx/1.14.1" ascii
        $s3 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36" ascii
        $s4 = "wine_get" ascii
    condition:
        uint16(0) == 0x5a4d and ((all of ($m*) and 2 of ($s*)) or (all of ($s*) and 1 of ($m*)) or 7 of them)
}
