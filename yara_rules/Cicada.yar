rule Cicada3301 {
    meta:
        author = "ditekshen"
        description = "Detects Cicada3301"
        cape_type = "Cicada Payload"
    strings:
        $s1 = "cmd/Cchcp 65001 >nulnet view \\\\"
        $s2 = "create_file_recovery"
        $s3 = "ecnrypted_files_full"
        $s4 = "get_excluded_directories"
        $s5 = "collect_files_except"
        $s6 = ".exe4d5a" ascii
        $s7 = "-accepteula -s -d \"\" --" ascii
        $s8 = "[*.exe*.EXE*.DLL*.ini*.inf*.pol*.cmd*.ps1*.vbs*.bat*.pagefile.sys*.hiberfil.sys*.drv" ascii
        $s9 = "memtasveeamsvc$backupsqlvssmsexchangesql$mysqlmysql$sophosMSExchange" ascii
        $s10 = "-DATA.txt" ascii
        $s11 = /--no_(local|net|impl)/ fullword ascii
        $c1 = "fsutil" ascii
        $c2 = "iisreset" ascii
        $c3 = "vssadmin" ascii
        $c4 = "wmic" ascii
        $c5 = "bcdedit" ascii
        $c6 = "wevtutil" ascii
    condition: 
        uint16(0) == 0x5a4d and (6 of ($s*) or (4 of ($c*) and 4 of ($s*)) or (all of ($c*) and 2 of ($s*)) or 9 of them)
}
