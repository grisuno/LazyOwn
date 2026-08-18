rule ARCrypt {
    meta:
        author = "ditekSHen"
        description = "Detects ARCrypt / ChileLocker ransomware"
        cape_type = "ARCrypt Payload"
    strings:
        $c1 = "readme_for_unlock.txt" wide
        $c2 = "vssadmin.exe delete shadows /all /quiet" wide
        $c3 = "START /b \"\" cmd /c wmic /node:" wide
        $c4 = "START /b \"\" cmd /c DEL \"" wide
        $c5 = "process call create cmd /c START" wide
        $c6 = "net config server /autodisconnect:" wide
        $c7 = "/NOBREAK>NUL) ELSE (START /b \"\" cmd /c DEL \"%~f" ascii
        $c8 = ":\\_ARC\\_WorkSolution\\cryptopp" ascii // or just \\cryptopp
        $e1 = /\.crYpt([A-F]{0,1}(\d+)?)?/ fullword wide
        $e2 = ".dnt___.crYpt" wide nocase
        $s1 = "create_directory" fullword ascii
        $s2 = "create_directories" fullword ascii
        $s3 = "NoClose" fullword ascii
        $s4 = "StartMenuLogOff" fullword ascii
        $s5 = "NoLogOff" fullword ascii
        $s6 = "DisableTaskMgr" fullword ascii
        $s7 = "DisableChangePassword" fullword ascii
        $s8 = "HideFastUserSwitching" fullword ascii
        $s9 = "RemotePath" fullword ascii
    condition:
        uint16(0) == 0x5a4d and (5 of ($c*) or 7 of ($s*) or (3 of ($c*) and 4 of ($s*)) or (1 of ($e*) and (1 of ($c*) and 1 of ($s*))) or (all of ($e*) and (1 of ($c*) or 1 of ($s*))))
}
