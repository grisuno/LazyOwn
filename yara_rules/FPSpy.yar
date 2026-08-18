import "pe"

rule FPSpy {
    meta:
        author = "ditekshen"
        description = "Detects FPSpy"
        cape_type = "FPSpy Payload"
    strings:
        $f1 = "[Analys_Spy]" wide
        $f2 = "[DeletePoorDll]" wide
        $f3 = "[DownloadProc]" wide
        $f4 = "[DragWarp]" wide
        $f5 = "[GetCoolDir]" wide
        $f6 = "[JackSleep]" wide
        $f7 = "[KillCmdExe]" wide
        $f8 = "[PsDownProc]" wide
        $f9 = "[PsUpProc]" wide
        $f10 = "[ReadFileFromPacket]" wide
        $f11 = "[RemoteDropExec]" wide
        $f12 = "[RemoteExec]" wide
        $f13 = "[RemoteInject]" wide
        $f14 = "[SendHttpForUpload]" wide
        $s1 = "MazeFunc" fullword ascii
        $s2 = /(Exit|Update|Drop)_EVT/ fullword ascii
        $s3 = "Key.dat" fullword ascii
        $s4 = "%sSysInfo_%02d_%02d_%02d.txt" fullword ascii
        $s5 = "cmd /c systeminfo >> %s" fullword ascii
        $s6 = "Content-Disposition: form-data; name=\"MAX_FILE_SIZE\"" fullword ascii
        $s7 = "FPSpy" fullword wide
    condition: 
        uint16(0) == 0x5a4d and ((pe.exports("MazeFunc") and 2 of ($f*) and 1 of ($s*)) or (6 of ($f*) and 1 of ($s*)) or (5 of ($s*) and 1 of ($f*)) or (8 of ($f*)))
}
