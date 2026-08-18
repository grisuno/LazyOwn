rule Underground {
    meta:
        author = "ditekSHen"
        description = "Detects Underground ransomware"
        cape_type = "Underground Payload"
    strings:
        $x1 = "Underground team" ascii
        $ip1 = "172.16.10." ascii
        $ip2 = "10.10.10." ascii
        $s1 = "temp.cmd" ascii wide
        $s2 = "%s\\!!readme!!!.txt" wide
        $s3 = "VIPinfo.txt" wide
        $s4 = "File opening error is:%d" wide
        $s5 = "\\\\?\\%s" fullword wide
        $s6 = "http://undgr" ascii
        $s7 = "password:" ascii
        $s8 = "login:" ascii
        $s9 = ".onion" ascii
        $b1 = "\\microsoft\\" fullword wide
        $b2 = "\\google\\chrome" fullword wide
        $b3 = "\\mozilla\\firefox" fullword wide
        $b4 = "\\opera\\" fullword wide
    condition:
        uint16(0) == 0x5a4d and ((1 of ($x*) and ((all of ($ip*) and 2 of ($s*)) or 4 of ($s*) or (2 of ($b*) and 2 of ($s*)))) or 7 of ($s*) or (3 of ($b*) and 4 of ($s*)) or (1 of ($ip*) and 2 of ($b*) and 2 of ($s*)))
}
