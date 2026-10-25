rule ToxicEye {
    meta:
        author = "ditekSHen"
        description = "Detects ToxicEye / TelegramRAT"
        cape_type = "ToxicEye Payload"
    strings:
        $s1 = "[~] Handling command" wide 
        $s2 = "[?] Sleeping {0}" wide 
        $s3 = "GETPASSWORDS" wide 
        $s4 = "FORKBOMB" wide 
        $s5 = "SENDKEYPRESS" wide 
        $s6 = "KEYLOGGER" wide 
        $s7 = "/ToxicEye/master/TelegramRAT/" wide 
        $s8 = "desktopScreenshot" ascii 
        $s9 = "MeltFile" ascii 
        $s10 = "AutoStealer" ascii 
        $s11 = /\/LimerBoy\/(ToxicEye|Adamantium-Thief|hackpy)/ wide
    condition:
        uint16(0) == 0x5a4d and 7 of them
}
