rule LightHand {
    meta:
        author = "ditekshen"
        description = "Detects LightHand"
        cape_type = "LightHand Payload"
    strings:
        $x1 = "27.102." ascii
        $x2 = "109.248.150.179" fullword ascii
        $s1 = /Hello (Client|Server)/ fullword ascii
        $s2 = "%s|%s|%s|%s|%s|%s|" fullword wide
        $s3 = "%s\\cmd.exe" fullword wide
        $s4 = "Remote PC" fullword wide
        $s5 = { 2e 62 61 74 [3-4] 3a 4c 31 0d 0a 64 65 6c
                20 2f 46 20 22 25 73 22 0d 0a 69 66 20 65 78 69
                73 74 20 22 25 73 22 20 67 6f 74 6f 20 4c 31 0d
                0a 64 65 6c 20 2f 46 20 22 25 73 22 0d 0a 00 00
                6f 70 65 6e }
        $s6 = { 25 00 2e 00 32 00 66 00 47 00 42 00 00 00 00 00
                25 00 73 00 7c 00 25 00 73 00 7c 00 25 00 73 00
                0a 00 00 00 00 00 00 00 5c 00 2a 00 2e 00 2a 00
                00 00 00 00 0a 00 00 00 2e 00 00 00 2e 00 2e 00
                00 00 00 00 00 00 00 00 46 00 6f 00 6c 00 64 00
                65 00 72 00 00 00 00 00 25 00 73 00 5c 00 25 00
                73 00 00 00 00 00 00 00 25 00 64 00 42 00 00 00
                25 00 2e 00 31 00 66 00 4b 00 42 00 00 00 00 00
                25 00 2e 00 31 00 66 00 4d 00 42 }
    condition:
        uint16(0) == 0x5a4d and ((5 of ($s*)) or (1 of ($x*) and 3 of ($s*)))
}
