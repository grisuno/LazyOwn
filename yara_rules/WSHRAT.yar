rule WSHRATPlugin {
    meta:
        author = "ditekshen"
        description = "WSHRAT keylogger plugin payload"
        cape_type = "WSHRAT Payload"
    strings:
        $s1 = "GET /open-keylogger HTTP/1.1" fullword wide
        $s2 = "KeyboardChange: nCode={0}, wParam={1}, vkCode={2}, scanCode={3}, flags={4}, dwExtraInfo={6}" wide
        $s3 = "MouseChange: nCode={0}, wParam={1}, x={2}, y={3}, mouseData={4}, flags={5}, dwExtraInfo={7}" wide
        $s4 = "sendKeyLog" fullword ascii
        $s5 = "saveKeyLog" fullword ascii
        $s6 = "get_TotalKeyboardClick" fullword ascii
        $s7 = "get_SessionMouseClick" fullword ascii
        $pdb = "\\Android\\documents\\visual studio 2010\\Projects\\Keylogger\\Keylogger\\obj\\x86\\Debug\\Keylogger.pdb" ascii
    condition:
        uint16(0) == 0x5a4d and filesize < 100KB and 4 of them
}

rule WSHRAT {
    meta:
        author = "ditekSHen"
        description = "Detects WASHRAT"
        cape_type = "WSHRAT Payload"
    strings:
        $x1 = "WSH Rat v" wide
        $x2 = "SOFTWARE\\WSHRat" wide
        $x3 = "WSH Remote" wide nocase
        $x4 = "WSHRAT" wide nocase
        $s1 = "shellobj.regwrite \"HKEY_" ascii nocase
        $s2 = "shellobj.run(\"%comspec% /c" ascii nocase
        $s3 = "objhttpdownload.setrequestheader \"user-agent:\"," ascii nocase
        $s4 = "WScript.CreateObject(\"Shell.Application\").ShellExecute" ascii nocase
        $s5 = "objwmiservice.ExecQuery(\"select" ascii nocase
        $s6 = "httpobj.open(\"post\",\"http" ascii nocase
        $s7 = /(rdp|keylogger|get-pass|uvnc)\|http/ wide
    condition:
        uint16(0) == 0x5a4d and (2 of ($x*) or (1 of ($x*) and 1 of ($s*)) or (6 of ($s*)))
}
