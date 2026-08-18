rule Fiber {
    meta:
        author = "ditekSHen"
        description = "Detects Fiber .NET injector"
        cape_type = "Fiber Payload"
    strings:
        $x1 = "Fiber.dll" fullword ascii
        $s1 = "-WindowStyle Hidden Copy-Item -Path *.vbs -Destination" wide
        $s2 = "-WindowStyle Hidden {0} -WindowStyle Hidden Start-Sleep 5; Start-Process {1}" wide
        $s3 = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" wide
        $s4 = "WScript.Shell" fullword wide
        $s5 = "{0}_{1:N}.lnk" fullword wide
        $s6 = "notepad.exe,0" fullword wide
        $i1 = "AppLaunch.exe" fullword wide
        $i2 = "aspnet_regbrowsers.exe" fullword wide
        $i3 = "cvtres.exe" fullword wide
        $i4 = "ilasm.exe" fullword wide
        $i5 = "jsc.exe" fullword wide
        $i6 = "MSBuild.exe" fullword wide
        $i7 = "RegAsm.exe" fullword wide
        $i8 = "RegSvcs.exe" fullword wide
        $v1_1 = "is tampered" wide
        $v1_2 = "Debugger Detected" wide
        $v1_3 = "RepositoryUrl" ascii
        $v1_4 = { 72 00 63 00 65 00 41 00 00 11 56 00 69 00 72 00
                74 00 75 00 61 00 6c 00 20 00 00 0b 41 00 6c 00
                6c 00 6f 00 63 00 00 0d 57 00 72 00 69 00 74 00
                65 00 20 00 00 11 50 00 72 00 6f 00 63 00 65 00
                73 00 73 00 20 00 00 0d 4d 00 65 00 6d 00 6f 00
                72 00 79 00 00 0f 50 00 72 00 6f 00 74 00 65 00
                63 00 74 00 00 0b 4f 00 70 00 65 00 6e 00 20 00
                00 0f 50 00 72 00 6f 00 63 00 65 00 73 00 73 00
                00 0d 43 00 6c 00 6f 00 73 00 65 00 20 00 00 0d
                48 00 61 00 6e 00 64 00 6c 00 65 00 00 0f 6b 00
                65 00 72 00 6e 00 65 00 6c }
    condition:
        uint16(0) == 0x5a4d and ((1 of ($x*) and 3 of ($s*) and 2 of ($i*)) or (4 of ($s*) and 4 of ($i*)) or (2 of ($s*) and 6 of ($i*)) or (1 of ($x*) and 3 of ($v1*)) or (all of ($v1*)))
}
