rule Rhysida {
    meta:
        author = "ditekSHen"
        description = "Detects Rhysida ransomware"
        cape_type = "Rhysida Payload" 
    strings:
        $s1 = "cmd.exe /c reg add \"HK" ascii
        $s2 = "rundll32.exe user32.dll,UpdatePerUserSystemParameters" fullword ascii
        $s3 = "C:/Users/Public/bg.jpg" fullword ascii
        $s4 = "CriticalBreachDetected.pdf" fullword ascii
        $s5 = "rhysida" ascii
        $s6 = "cmd.exe /c reg delete \"HKCU\\Cont" ascii
        $s7 = "Rhysida-" ascii
    condition:
        uint16(0) == 0x5a4d and 5 of ($s*) or (3 of ($s*) and #s1 > 5)
}
