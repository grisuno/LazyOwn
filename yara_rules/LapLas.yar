rule LapLas {
    meta:
        author = "ditekSHen"
        description = "Detects LapLas Infostealer"
        cape_type = "LapLas Payload"
    strings:
        // Go variant
        $c1 = "/bot/" ascii
        $c2 = "key=" ascii
        $f1 = "main.isRunning" fullword ascii
        $f2 = "main.writePid" fullword ascii
        $f3 = "main.isStartupEnabled" fullword ascii
        $f4 = "main.enableStartup" fullword ascii
        $f5 = "main.waitOpenClipboard" fullword ascii
        $f6 = "main.clipboardWrite" fullword ascii
        $f7 = "main.setOnline" fullword ascii
        $f8 = "main.getRegex" fullword ascii
        // .NET variant
        $v2_1 = "{0}/bot/{1}?{2}" wide
        $v2_2 = /\{0\}\\\{1\}\.(exe|pid)/ wide
        $v2_3 = "schtasks /create /tn" wide
        $v2_4 = "SetOnline" fullword ascii
        $v2_5 = "IsAutoRunInstance" fullword ascii
        $v2_6 = "GetNewAddress" fullword ascii
        $v2_7 = "RefreshRegex" fullword ascii
    condition:
        uint16(0) == 0x5a4d and ((all of ($c*) and 5 of ($f*)) or (1 of ($c*) and 7 of ($f*)) or (6 of ($v2*)))
} 
