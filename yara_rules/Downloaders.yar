import "pe"

rule DLAgent01 {
    meta:
      author = "ditekshen"
      description = "Detects downloader agent"
      cape_type = "DLAgent01 Payload"
    strings:
        $s1 = "Mozilla/5.0 Gecko/41.0 Firefox/41.0" fullword wide
        $s2 = "/Node:localhost /Namespace:\\\\root\\SecurityCenter2 Path AntiVirusProduct Get displayName /Format:List" fullword wide
        $s3 = "GUID.log" fullword wide
        $s4 = "NO AV" fullword wide
        $s5 = "%d:%I64d:%I64d:%I64d" fullword wide
    condition:
        uint16(0) == 0x5a4d and 4 of them
}

rule DLAgent02 {
    meta:
      author = "ditekSHen"
      description = "Detects known downloader agent downloading encoded binaries in patches from paste-like websites, most notably hastebin"
      cape_type = "DLAgent02 Payload"
    strings:
        $x1 = "/c timeout {0}" fullword wide
        $x2 = "^(https?|ftp):\\/\\/" fullword wide
        $x3 = "{0}{1}{2}{3}" wide
        $x4 = "timeout {0}" fullword wide
        $s1 = "HttpWebRequest" fullword ascii
        $s2 = "GetResponseStream" fullword ascii
        $s3 = "set_FileName" fullword ascii
        $s4 = "set_UseShellExecute" fullword ascii
        $s5 = "WebClient" fullword ascii
        $s6 = "set_CreateNoWindow" fullword ascii
        $s7 = "DownloadString" fullword ascii
        $s8 = "WriteByte" fullword ascii
        $s9 = "CreateUrlCacheEntryW" fullword ascii
        $s10 = "HttpStatusCode" fullword ascii
        $s11 = "FILETIME" fullword ascii
    condition:
        uint16(0) == 0x5a4d and filesize < 5000KB and ((2 of ($x*) and 2 of ($s*)) or (#x3 > 2 and 4 of ($s*)))
}

rule DLAgent03 {
    meta:
      author = "ditekSHen"
      description = "Detects known Delphi downloader agent downloading second stage payload, notably from discord"
      cape_type = "DLAgent03 Payload"
    strings:
        $delph1 = "FastMM Borland Edition" fullword ascii
        $delph2 = "SOFTWARE\\Borland\\Delphi" ascii
        $v1_1 = "InternetOpenUrlA" fullword ascii
        $v1_2 = "CreateFileA" fullword ascii
        $v1_3 = "WriteFile" fullword ascii
        $v1_4 = "$(,048<@DHLLPPTTXX\\\\``ddhhllppttttxxxx||||" ascii
        $v2_1 = "WinHttp.WinHttpRequest.5.1" fullword ascii
        $v2_2 = { 6f 70 65 6e ?? ?? ?? ?? ?? 73 65 6e 64 ?? ?? ?? ?? 72 65 73 70 6f 6e 73 65 74 65 78 74 }
        // $pat is slowing down scanning
        //$pat = /[a-f0-9]{168}/ fullword ascii
        $url1 = "https://discord.com/" fullword ascii
        $url2 = "http://www.superutils.com" fullword ascii
    condition:
        //uint16(0) == 0x5a4d and 1 of ($delph*) and $discord and ((all of ($v1*) or all of ($v2*)) or $pat)
        uint16(0) == 0x5a4d and 1 of ($delph*) and 1 of ($url*) and (all of ($v1*) or 1 of ($v2*))
}

rule DLAgent04 {
    meta:
      author = "ditekSHen"
      description = "Detects known downloader agent downloading encoded binaries in patches from paste-like websites, most notably hastebin"
      cape_type = "DLAgent04 Payload"
    strings:
        $x1 = "@@@http" ascii wide
        $s1 = "HttpWebRequest" fullword ascii
        $s2 = "GetResponseStream" fullword ascii
        $s3 = "set_FileName" fullword ascii
        $s4 = "set_UseShellExecute" fullword ascii
        $s5 = "WebClient" fullword ascii
        $s6 = "set_CreateNoWindow" fullword ascii
        $s7 = "DownloadString" fullword ascii
    condition:
        uint16(0) == 0x5a4d and filesize < 300KB and #x1 > 1 and 4 of ($s*)
}

rule DLAgent05 {
    meta:
        author = "ditekSHen"
        description = "Detects an unknown dropper. Typically exisys as a DLL in base64-encoded gzip-compressed file embedded within another executable"
        cape_type = "DLAgent05 Payload"
    strings:
        $s1 = "MARCUS.dll" fullword ascii wide
        $s2 = "GZipStream" fullword ascii
        $s3 = "MemoryStream" fullword ascii
        $s4 = "proj_name" fullword ascii
        $s5 = "res_name" fullword ascii
    condition:
        uint16(0) == 0x5a4d and all of them
}

rule DLAgent06 {
    meta:
      author = "ditekSHen"
      description = "Detects known downloader agent downloading encoded binaries in patches"
      cape_type = "DLAgent06 Payload"
    strings:
        $s1 = "totallist" fullword ascii wide
        $s2 = "LINKS_HERE" fullword wide
        $s3 = "[SPLITTER]" fullword wide
        $var2_1 = "DownloadWeb" fullword ascii
        $var2_2 = "WriteByte" fullword ascii
        $var2_3 = "MemoryStream" fullword ascii
        $var2_4 = "DownloadString" fullword ascii
        $var2_5 = "WebClient" fullword ascii
    condition:
        uint16(0) == 0x5a4d and ((all of ($s*) and 2 of ($var2*)) or (4 of ($var2*) and 2 of ($s*)))
}

rule DLAgent07 {
    meta:
        author = "ditekSHen"
        description = "Detects delf downloader agent"
        cape_type = "DLAgent07 Payload"
    strings:
        $s1 = "C:\\Users\\Public\\Libraries\\temp" fullword ascii
        $s2 = "SOFTWARE\\Borland\\Delphi" ascii
        $s3 = "Mozilla/5.0(compatible; WinInet)" fullword ascii
        $o1 = { f3 a5 e9 6b ff ff ff 5a 5d 5f 5e 5b c3 a3 00 40 }
        $o2 = { e8 83 d5 ff ff 8b 15 34 40 41 00 89 10 89 58 04 }
        $o3 = { c3 8b c0 53 51 e8 f1 ff ff ff 8b d8 85 db 74 3e }
        $o4 = { e8 5c e2 ff ff 8b c3 e8 b9 ff ff ff 89 04 24 83 }
        $o5 = { 85 c0 74 1f e8 62 ff ff ff a3 98 40 41 00 e8 98 }
        $o6 = { 85 c0 74 19 e8 be ff ff ff 83 3d 98 40 41 00 ff }
        $x1 = "22:40:08        \"> <rdf:RDF xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"> <rdf:Description rdf:about=\"\"" ascii
        $x2 = "uuid:A9BD8E384B2FDE118D26E6EE744C235C\" stRef:documentID=\"uuid:A8BD8E384B2FDE118D26E6EE744C235C\"/>" ascii
    condition:
        uint16(0) == 0x5a4d and ((2 of ($s*) and 5 of ($o*)) or (all of ($s*) and 2 of ($o*)) or (all of ($x*) and 2 of them))
}

rule DLAgentGo {
    meta:
        author = "ditekSHen"
        description = "Detects Go-based downloader"
        cape_type = "DLAgentGo Payload"
    strings:
        $s1 = "main.downloadFile" fullword ascii
        $s2 = "main.fetchFiles" fullword ascii
        $s3 = "main.createDefenderAllowanceException" fullword ascii
        $s4 = "main.unzip" fullword ascii
        $s5 = "HideWindow" fullword ascii
        $s6 = "/go/src/installwrap/main.go" ascii
    condition:
        uint16(0) == 0x5a4d and 4 of them
}

rule DLAgent09 {
    meta:
        author = "ditekSHen"
        description = "Detects known downloader agent"
        cape_type = "DLAgent09 Payload"
    strings:
        $h1 = "//:ptth" ascii wide nocase
        $h2 = "//:sptth" ascii wide nocase
        $s1 = "DownloadString" fullword ascii wide
        $s2 = "StrReverse" fullword ascii wide
        $s3 = "FromBase64String" fullword ascii wide
        $s4 = "WebClient" fullword ascii wide
    condition:
        uint16(0) == 0x5a4d and (1 of ($h*) and all of ($s*))
}

rule DLAgent10 {
    meta:
        author = "ditekSHen"
        description = "Detects known downloader agent"
        cape_type = "DLAgent10 Payload"
    strings:
        $s1 = "powershell.exe" ascii wide nocase
        $s2 = ".DownloadFile(" ascii wide nocase
        $s3 = "_UseShellExecute" ascii wide nocase
        $s4 = "_CreateNoWindow" ascii wide nocase
    condition:
        uint16(0) == 0x5a4d and all of them
}

rule DLAgent11 {
    meta:
        author = "ditekSHen"
        description = "Detects downloader agent"
        cape_type = "DLAgent11 Payload"
    strings:
        $pdb = "\\loader2\\obj\\Debug\\loader2.pdb" ascii
        $s1 = "DownloadFile" fullword ascii
        $s2 = "ZipFile" fullword ascii
        $s3 = "WebClient" fullword ascii
        $s4 = "ExtractToDirectory" fullword ascii
        $s5 = "System Clear" fullword ascii
    condition:
        uint16(0) == 0x5a4d and (all of ($s*) or (($pdb) and 4 of ($s*)))
}

rule DLAgent12 {
    meta:
        author = "ditekSHen"
        description = "Detects downloader agent"
        cape_type = "DLAgent12 Payload"
    strings:
        $s1 = "WebClient" fullword ascii
        $s2 = "DownloadData" fullword ascii
        $s3 = "packet_server" fullword wide
    condition:
        uint16(0) == 0x5a4d and all of them and filesize < 50KB
}

rule DLInjector01 {
    meta:
        author = "ditekSHen"
        description = "Detects specific downloader injector shellcode"
    strings:
        $s1 = "process call create \"%s\"" ascii wide
        $s2 = "\\REGISTRY\\MACHINE\\System\\CurrentControlSet\\Enum\\" ascii wide
        $s3 = "%systemroot%\\system32\\ntdll.dll" ascii wide
        $s4 = "qemu-ga.exe" ascii wide
        $s5 = "prl_tools.exe" ascii wide
        $s6 = "vboxservice.exe" ascii wide
        $o1 = { 75 04 74 02 38 6e 8b 34 24 83 c4 04 eb 0a 08 81 }
        $o2 = { 16 f8 f7 ba f0 3d 87 c7 95 13 b7 64 22 be e1 59 }
        $o3 = { 8b 0c 24 83 c4 04 eb 05 ea f2 eb ef 05 e8 ad fe }
        $o4 = { eb 05 1d 51 eb f5 ce e8 80 fd ff ff 77 a1 f4 cd }
        $o5 = { eb 05 6e 33 eb f5 73 e8 64 f6 ff ff 77 a1 f4 77 }
        $o6 = { 59 eb 05 fd 98 eb f4 50 e8 d5 f5 ff ff 3b b9 00 }
        $o7 = "bYkoDA7G" fullword ascii
    condition:
        (uint16(0) == 0x5a4d and all of ($o*)) or (all of ($s*))
}

rule DLInjector02 {
    meta:
        author = "ditekSHen"
        description = "Detects downloader injector"
    strings:
        $x1 = "In$J$ct0r" fullword wide
        $x2 = "%InJ%ector%" fullword wide
        $a1 = "WriteProcessMemory" fullword wide
        $a2 = "URLDownloadToFileA" fullword ascii
        $a3 = "Wow64SetThreadContext" fullword wide
        $a4 = "VirtualAllocEx" fullword wide
        $s1 = "RunPE" fullword wide
        $s2 = "SETTINGS" fullword wide
        $s3 = "net.pipe" fullword wide
        $s4 = "vsmacros" fullword wide
    condition:
        uint16(0) == 0x5a4d and (1 of ($x*) or (all of ($a*) and 3 of ($s*)))
}

rule DLAgent14 {
    meta:
        author = "ditekSHen"
        description = "Detects downloader injector"
        cape_type = "DLAgent14 Payload"
    strings:
        $s1 = "%ProgramData%\\AVG" fullword wide
        $s2 = "%ProgramData%\\AVAST Software" fullword wide
        $s3 = "%wS\\%wS.vbs" fullword wide
        $s4 = "%wS\\%wS.exe" fullword wide
        $s5 = "CL,FR,US,CY,FI,HR,HU,RO,PL,IT,PT,ES,CA,DK,AT,NL,AU,AR,NP,SE,BE,NZ,SK,GR,BG,NO,GE" ascii
        $s6 = "= CreateObject(\"Microsoft.XMLHTTP\")" ascii
    condition:
        uint16(0) == 0x5a4d and 5 of them
}

rule DLInjector03 {
    meta:
        author = "ditekSHen"
        description = "Detects unknown loader / injector"
    strings:
        $x1 = "LOADER ERROR" fullword ascii
        $s1 = "_ZN6curlpp10OptionBaseC2E10CURLoption" fullword ascii
        $s2 = "The procedure entry point %s could not be located in the dynamic link library %s" fullword ascii
    condition:
        uint16(0) == 0x5a4d and all of them
}

rule Phonzy {
    meta:
        author = "ditekSHen"
        description = "Detects specific downloader agent"
        cape_type = "Phonzy Payload"
    strings:
        $ua1 = "User-Agent: Mozilla/5.0 (X11; Linux" wide
        $s1 = "<meta name=\"keywords\" content=\"([\\w\\d ]*)\">" fullword wide
        $s2 = "WebClient" fullword ascii
        $s3 = "WriteAllText" fullword ascii
        $s4 = "DownloadString" fullword ascii
        $s5 = "WriteByte" fullword ascii
    condition:
        uint16(0) == 0x5a4d and (all of ($s*) or (1 of ($ua*) and ($s1) and 2 of ($s*)))
}

rule ShellcodeDLEI {
    meta:
        author = "ditekSHen"
        description = "Detects shellcode downloader, executer, injector"
        cape_type = "ShellcodeInject Payload"
    strings:
        $s1 = "PPidSpoof" fullword ascii
        $s2 = "ProcHollowing" fullword ascii
        $s3 = "CreateProcess" fullword ascii
        $s4 = "DynamicCodeInject" fullword ascii
        $s5 = "PPIDDynCodeInject" fullword ascii
        $s6 = "MapAndStart" fullword ascii
        $s7 = "PPIDAPCInject" fullword ascii
        $s8 = "PPIDDLLInject" fullword ascii
        $s9 = "CopyShellcode" fullword ascii
        $s10 = "GetEntryFromBuffer" fullword ascii
    condition:
        uint16(0) == 0x5a4d and filesize < 100KB and 5 of ($s*)
}

rule EXEPWSHDL {
    meta:
        author = "ditekSHen"
        description = "Detects executable downloaders using PowerShell"
    strings:
        $x1 = "[Ref].Assembly.GetType(" ascii wide
        $x2 = ".SetValue($null,$true)" ascii wide
        $s1 = "replace" ascii wide
        $s2 = "=@(" ascii wide
        $s3 = "[System.Text.Encoding]::" ascii wide
        $s4 = ".substring" ascii wide
        $s5 = "FromBase64String" ascii wide
        $d1 = "New-Object" ascii wide
        $d2 = "Microsoft.XMLHTTP" ascii wide
        $d3 = ".open(" ascii wide
        $d4 = ".send(" ascii wide
    condition:
        uint16(0) == 0x5a4d and filesize < 100KB and all of ($x*) and (3 of ($s*) or all of ($d*))
}

rule DLInjector04 {
    meta:
        author = "ditekSHen"
        description = "Detects downloader / injector"
    strings:
        $s1 = "Runner" fullword ascii
        $s2 = "DownloadPayload" fullword ascii
        $s3 = "RunOnStartup" fullword ascii
        $a1 = "Antis" fullword ascii
        $a2 = "antiVM" fullword ascii
        $a3 = "antiSandbox" fullword ascii
        $a4 = "antiDebug" fullword ascii
        $a5 = "antiEmulator" fullword ascii
        $a6 = "enablePersistence" fullword ascii
        $a7 = "enableFakeError" fullword ascii
        $a8 = "DetectVirtualMachine" fullword ascii
        $a9 = "DetectSandboxie" fullword ascii
        $a10 = "DetectDebugger" fullword ascii
        $a11 = "CheckEmulator" fullword ascii
    condition:
        uint16(0) == 0x5a4d and ((all of ($s*) and 5 of ($a*)) or 10 of ($a*))
}

rule DLInjector05 {
    meta:
        author = "ditekSHen"
        description = "Detects downloader / injector (NiceProcess)"
    strings:
        $s1 = "pidhtmpfile.tmp" fullword ascii
        $s2 = "pidhtmpdata.tmp" fullword ascii
        $s3 = "pidHTSIG" fullword ascii
        $s4 = "Taskmgr.exe" fullword ascii
        $s5 = "[HP][" ascii
        $s6 = "[PP][" ascii
        $s7 = { 70 69 64 68 74 6d 70 66 69 6c 65 2e 74 6d 70 00
                2e 64 6c 6c 00 00 00 00 70 69 64 48 54 53 49 47
                00 00 00 00 ?? ?? 00 00 54 61 73 6b 6d 67 72 2e
                65 78 65 }
    condition:
        uint16(0) == 0x5a4d and 4 of them
}

rule DLInjector06 {
    meta:
        author = "ditekSHen"
        description = "Detects downloader / injector"
    strings:
        $s1 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ascii wide
        $s2 = "Content-Type: application/x-www-form-urlencoded" wide
        $s3 = "https://ipinfo.io/" wide
        $s4 = "https://db-ip.com/" wide
        $s5 = "https://www.maxmind.com/en/locate-my-ip-address" wide
        $s6 = "https://ipgeolocation.io/" wide
        $s7 = "POST" fullword wide
    condition:
        uint16(0) == 0x5a4d and all of them
}

rule dotRunpeX {
    meta:
        author = "ditekSHen"
        description = "Detects dotRunpeX injector"
    strings:
        $s1 = "\\Registry\\Machine\\System\\CurrentControlSet\\Services\\TaskKill" fullword wide
        $s2 = "KoiVM" ascii
        $s3 = "RunpeX.Stub.Framework" wide
        $s4 = "ExceptionServices.ExceptionDispatchInfo" wide
        $s5 = "Kernel32.Dll" wide
    condition:
        uint16(0) == 0x5a4d and all of them
}

rule DLInjector07 {
    meta:
        author = "ditekSHen"
        description = "Detects downloader injector"
    strings:
        $x1 = "23lenrek[||]lldtn[||]daerhTemuseR[||]txetnoCdaerhTteS46woW[||]txetnoCdaerhTteS[||]txetnoCdaerhTteG46woW[||]txetnoCdaerhTteG[||]xEcollAlautriV[||]yromeMssecorPetirW[||]yromeMssecorPdaeR[||]noitceSfOweiVpamnUwZ[||]AssecorPetaerC" wide
        $l1 = "[||]" wide
        $r1 = "yromeMssecorPetirW" wide
        $r2 = "xEcollAlautriV" wide
        $r3 = "daerhTemuseR" ascii wide
        $r4 = "noitceSfOweiVpamnUwZ" wide
        $s1 = "Debugger Detected" fullword wide
        $s2 = "payload" fullword ascii
        $s3 = "_ENABLE_PROFILING" fullword wide // Confuser Anti-Debug
    condition:
        uint16(0) == 0x5a4d and (1 of ($x*) or (1 of ($l*) and 2 of ($r*)) or 6 of them)
}

rule RookIEDownloader {
    meta:
        author = "ditekSHen"
        description = "Detect malware downlaoder, variant of ZombieBoy downloader"
    strings:
        $s1 = "shell:::{2559a1f3-21d7-11d4-bdaf-00c04f60b9f0}" fullword ascii
        $s2 = "taskkill /f /im hh.exe" fullword ascii
        $s3 = "RookIE/1.0" fullword ascii
        $s4 = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\Zones\\0" fullword ascii
        $s5 = "#32770" fullword ascii
    condition:
        uint16(0) == 0x5a4d and 4 of them
}

rule PackedLoader {
    meta:
        author = "ditekShen"
        description = "Detects unknown loader / packer"
    strings:
        $s1 = "Error at hooking API \"%S\"" wide
        $s2 = "Dumping first %d bytes:" wide
        $s3 = "Error at initialization of bundled DLL: %s" wide
        $s4 = "GetMemoryForDLL()" ascii
        $s5 = "type=activation&code=" ascii
        $s6 = "activation.php?code=" ascii
        $s7 = "&hwid=" ascii
        $s8 = "&hash=" ascii
        $s9 = "type=deactivation&hash=" ascii
        $s10 = "deactivation.php?hash=" ascii
        $s11 = "BANNED" fullword ascii
        $s12 = "GetAdaptersInfo" ascii
    condition:
        uint16(0) == 0x5a4d and 11 of them
}

rule PWSHDLLDL {
    meta:
        author = "ditekShen"
        description = "Detects downloader"
    strings:
        $s1 = "powershell.exe Set-ExecutionPolicy Bypass -Scope Process ; powershell -file " fullword wide nocase
        $s2 = "objShell.run \"powershell -WindowStyle hidden -command wscript.exe //b //nologo '" fullword wide nocase
        $s3 = "cmd.exe /c schtasks.exe /create /tn \"" fullword wide nocase
        $s4 = "-WindowStyle hidden -command wscript.exe //b //nologo '" fullword wide nocase
        $s6 = "\" /tr \"wscript.exe //b //nologo '" fullword wide nocase
        $s7 = "\" -Value \"Powershell.exe -WindowStyle hidden \"\"& '" fullword wide nocase
        $op0 = { 61 01 00 34 53 79 73 74 65 6d 2e 57 65 62 2e 53 }
        $op1 = { 4b 04 00 00 34 01 00 00 7f 05 00 00 1a }
    condition:
        uint16(0) == 0x5a4d and pe.is_dll() and 5 of them
}

rule VBSDownloader {
    meta:
        author = "ditekShen"
        description = "Detects second stage VBS downloader of third stage VBS"
    strings:
        $s1 = "CreateObject(\"MSXML2.ServerXMLHTTP\")" wide
        $s2 = ".Open \"GET\"," wide
        $s3 = ".Send" wide
        $s4 = ".responseText" wide
        $s5 = "ExecuteGlobal" wide
    condition:
       filesize < 50KB and all of them 
}
