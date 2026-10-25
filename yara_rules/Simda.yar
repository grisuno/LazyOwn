rule Simda {
    meta:
        author = "ditekShen"
        description = "Detects Simda / Shifu infostealer"
        cape_type = "Simda Payload"
    strings:
        $s1 = "command=auth_loginByPassword&back_command=&back_custom1=&" fullword ascii
        $s2 = "iexplore.exe|opera.exe|java.exe|javaw.exe|explorer.exe|isclient.exe|intpro.exe|ipc_full.exe|mnp.exe|cbsmain.dll|firefox.exe|clma" ascii
        $s3 = "debug_%s_%s.log" fullword ascii
        $s4 = "Content-Disposition: form-data; name=\"file\"; filename=\"report\"" ascii
        $s5 = "name=%s&port=%u" ascii
        $s6 = "id=%s&ver=4.0.1&up=%u&os=%03u&rights=%s&ltime=%s%d&token=%d" ascii
        $s7 = "{BotVer:" fullword ascii
        $s8 = "software\\microsoft\\windows nt\\currentversion\\winlogon" ascii
        $s9 = /(!|&|data_)inject(=ok)?/ fullword ascii
    condition:
      uint16(0) == 0x5a4d and 6 of them
}
