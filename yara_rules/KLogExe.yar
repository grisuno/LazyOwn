rule KLogExe {
    meta:
        author = "ditekshen"
        description = "Detects KLogExe"
        cape_type = "KLogExe Payload"
    strings:
        $s1 = "[clip_s]: %s" ascii
        $s2 = "------ %d/%d/%d : %d/%d ------" ascii
        $s3 = "[RWin+]" ascii
        $s4 = "[Too many clip_tail]" ascii
        $s5 = "name=\"userfile\"; filename=\"%s\"" ascii
        $s6 = "Origin: http://" wide
        $s7 = "%s_%d_%d_%d_%d" wide
        $s8 = "/wp-content/include.php?_sys_" wide
        $s9 = "\\desktops.ini" wide
        $s10 = "KLogExe" wide nocase
        $s11 = "dynamic_import.cpp [resolve_call] can`nt" wide
    condition: 
        uint16(0) == 0x5a4d and 6 of them
}
