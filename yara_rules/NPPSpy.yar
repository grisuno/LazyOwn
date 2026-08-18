import "pe"

rule NPPSpy {
    meta:
        author = "ditekShen"
        description = "Detects NPPSpy / Ntospy"
        cape_type = "NPPSpy Payload"
    strings:
        $s1 = "ntskrnl.dll" fullword ascii
        $s2 = "PasswordStealing.dll" fullword ascii
        $s3 = "ntoskrnl.dll" fullword ascii
        $s4 = "\\programdata\\packag~" ascii
        $s5 = "NPPSPY.dll" fullword ascii
        $s6 = "MSControll.dll" fullword ascii
        $s7 = "\\Windows\\Temp\\" ascii
        $s8 = "\\NPPSpy\\" ascii
        // hunt
        $s9 = "NPGetCaps" fullword ascii
        $s10 = "NPLogonNotify" fullword ascii
        // C:\Users\GrzegorzTworek\source\repos\NPPSpy\x64\Release\NPPSPY.pdb
        $path = "\\GrzegorzTworek\\" ascii
    condition:
      uint16(0) == 0x5a4d and ((pe.is_dll() and filesize < 110KB and pe.number_of_exports == 2 and ((pe.exports("NPGetCaps") and pe.exports("NPLogonNotify")) or (1 of ($s*) and (pe.exports("NPGetCaps") or pe.exports("NPLogonNotify"))))) or (($path) and any of ($s*)))
}
