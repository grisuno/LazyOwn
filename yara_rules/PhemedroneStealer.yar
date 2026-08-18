rule PhemedroneStealer {
    meta:
        author = "ditekSHen"
        description = "Detects Phemedrone Stealer infostealer"
        cape_type = "PhemedroneStealer Payload"
    strings:
        $p1 = /\{ file = \{(0|file)\}, data = \{(1|data)\} \}/ ascii wide
        $p2 = "{ <>h__TransparentIdentifier0 = {0}, match = {1} }" wide
        $p3 = "{ <>h__TransparentIdentifier1 = {0}, encrypted = {1} }" wide
        $p4 = "{<>h__TransparentIdentifier0}, match = {match} }" ascii
        $p5 = "{<>h__TransparentIdentifier1}, encrypted = {encrypted} }" ascii
        $s1 = "<KillDebuggers>b__" ascii
        $s2 = "<ParseExtensions>b__" ascii
        $s3 = "<ParseDiscordTokens>b__" ascii
        $s4 = "<IsVM>b__" ascii
        $s5 = "<Key3Database>b__" ascii
        $s6 = "masterPass" ascii
        $s7 = "rootLocation" ascii
        $s8 = "rgsServiceNames" ascii
        $s9 = "rgsFilenames" ascii
    condition:
        uint16(0) == 0x5a4d and ((all of ($p*) and 3 of ($s*)) or (3 of ($p*) and 4 of ($s*)) or (7 of ($s*)))
}
