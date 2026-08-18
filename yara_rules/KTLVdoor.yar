rule KTLVdoor {
    meta:
        author = "ditekshen"
        description = "Detects KTLVdoor"
        cape_type = "KTLVdoor Payload"
    strings:
        $s1 = "/cmd/acc/agent_acc" ascii
        $s2 = "main.DLLWMain" ascii
        $s3 = "main.checkSilent" ascii
        $h1 = ".handleInteractiveShell" ascii
        $h2 = ".handleNetstat" ascii
        $h3 = ".handleProcess" ascii
        $h4 = ".handleRefreshHostInfo" ascii
        $h5 = ".handleTimestomp" ascii
        $h6 = ".handleSoInject" ascii
        $h7 = ".HandleRegInfo" ascii
        $h8 = ".handlePortscan" ascii
        $h9 = ".handleReflectDllInject" ascii
        $h10 = ".handleFileDownload" ascii
        $f1 = ".RdpWithNTLM." ascii
        $f2 = ".FingerPrintOs." ascii
        $f3 = ".ScanWMI." ascii
        $f4 = ".ScanWinRM." ascii
        $f5 = ".ScanWeb." ascii
        $f6 = ".ScanSmb2." ascii
        $f7 = ".ScanRDP." ascii
        $f8 = ".ScanPing." ascii
        $f9 = ".ScanOxid." ascii
        $f10 = ".ScanMssql." ascii
        $f11 = ".ScanBanner." ascii
        $fr1 = /\.proxy[CS]2[CS](TC|UD)P/ ascii
        $fr2 = /\.Scan(WMI|WinRM|Web|Smb2|RDP|Ping|Oxid|Mssql|Banner)\./ ascii
    condition:
        (uint16(0) == 0x5a4d or uint16(0) == 0x457f) and ((6 of ($h*)) or (12 of ($f*)) or (2 of ($h*) and 4 of ($f*)) or (1 of ($s*) and (4 of ($h*) or 4 of ($f*))) or (13 of them))
}
