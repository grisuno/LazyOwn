rule G0Crypt {
    meta:
        author = "ditekSHen"
        description = "Detects G0Crypt / BRG0SNet / NovaGP ransomware"
        cape_type = "G0Crypt Payload"
    strings:
        $x1 = "G0Crypt/go/" ascii
        $x2 = "BRG0SNet" ascii
        $x3 = "/NovaGroup" ascii
        $x4 = "novagroup@onionmail.org" ascii nocase
        $x5 = "# Nova Group" ascii
        $f1 = "main.HaveRun" ascii
        $f2 = "main.FindFile" ascii
        $f3 = "main.deriveKey" ascii
        $f4 = "main.Pwd" fullword ascii
        $f5 = "/ClearBashFile" ascii
        $f6 = "/ClearUserTempFiles" ascii
        $f7 = "/KillProccess" ascii
        $f8 = "/Encryptor" ascii
        $f9 = "/NoDirEncrypt" ascii
        $f10 = "/RunCmdEexecutable" ascii
        $f11 = "/StopImportantServices" ascii
        $f12 = "/GetPwd" ascii
        $s1 = "\\$Recycle.Bin"
        $s2 = ".README.txt"
        $s3 = "\\BRSPATH.exe"
        $s4 = "taskkill /F /IM sql*"
        $s5 = "C:\\inetpub\\logs\\"
        $s6 = "shutdown /r"
        $s7 = ":\\Program Files\\VMware\\"
        $s8 = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Message /t REG_SZ /d"
        $s9 = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v DelLogSoft /t REG_SZ /d"
    condition:
        uint16(0) == 0x5a4d and (2 of ($x*) or 7 of ($f*) or (1 of ($x*) and (5 of ($f*) or 5 of ($s*))) or (6 of ($f*) and 4 of ($s*)) or 12 of them)
}
