rule SapphireStealer {
    meta:
        author = "ditekSHen"
        description = "Detects SapphireStealer"
        cape_type = "SapphireStealer Payload"
    strings:
       $s1 = "Sapphire.Modules." ascii
       $s2 = "sapphire\\" wide
       $s3 = "by r3vengerx0" wide
       $s4 = "Sapphire\\obj\\" ascii
       $s5 = "[ERROR_GETSECRETKEY_METHOD]" fullword wide
       $s6 = "[ERROR_CANT_GET_PASSWORD]" fullword wide
       $s7 = "<h2>------NEW LOGS------</h2>" wide
       $s8 = "[ERROR] can't create grab directory" wide
       $s9 = "<UploadToTelegram>d__" ascii
       $s10 = "UploadToTelegram" ascii
       $s11 = ".SendLog+<UploadToTelegram>d__" ascii
    condition:
       uint16(0) == 0x5a4d and 5 of them
}
