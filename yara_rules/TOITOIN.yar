rule TOITOINKritaLoader {
    meta:
        author = "ditekSHen"
        description = "Detects TOITOIN KritaLoader"
        cape_type = "TOITOIN Payload"
    strings:
       $p1 = ":\\Trabalho_2023\\OFF_2023\\" ascii
       $p2 = "DLL_Start_OK.pdb" ascii
       $s1 = "krita_main" fullword ascii
    condition:
       uint16(0) == 0x5a4d and (1 of ($p*) and 1 of ($s*))
}

rule TOITOINInjectorDLL {
    meta:
        author = "ditekSHen"
        description = "Detects TOITOIN InjectorDLL"
        cape_type = "TOITOIN Payload"
    strings:
       $p1 = ":\\Trabalho_2023\\OFF_2023\\" ascii
       $p2 = "DLL_START_IN.pdb" ascii
       $s1 = ".ini" fullword ascii
       $s2 = "\\users\\Public\\Documents\\" fullword ascii
    condition:
       uint16(0) == 0x5a4d and (1 of ($p*) and all of ($s*))
}

rule TOITOINDownloader {
    meta:
        author = "ditekSHen"
        description = "Detects TOITOIN Downloader"
        cape_type = "TOITOIN Payload"
    strings:
       $p1 = ":\\Trabalho_2023\\OFF_2023\\" ascii
       $s1 = { 20 2f 63 20 22 [6-15] 63 00 6d 00 64 00 00 00 6f 00 70 00 65 00 6e }
       $o1 = { 48 83 fa 10 72 34 48 8b 8d 10 ?? 00 00 48 ff c2 }
    condition:
       uint16(0) == 0x5a4d and all of them
}
