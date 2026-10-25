rule CommonMagic {
    meta:
        author = "ditekSHen"
        description = "Detects CommonMagic and Modules"
        cape_type = "CommonMagic Payload"
    strings:
        $p1 = "\\\\.\\pipe\\PipeMd" wide
        $p2 = "\\\\.\\pipe\\PipeCrDtMd" wide
        $p3 = "\\\\.\\pipe\\PipeDtMd" wide
        $s1 = "graph.microsoft.com" fullword wide
        $s2 = "CreateNamedPipe" ascii
        $s3 = "\\CommonCommand\\" wide
        $ua1 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36" wide
        $ua2 = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136" wide
    condition:
        uint16(0) == 0x5a4d and (2 of ($p*) and 1 of ($s*)) or (1 of ($ua*) and 1 of ($s*) and 1 of ($p*))
}
