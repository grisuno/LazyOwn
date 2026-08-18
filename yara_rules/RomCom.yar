import "pe"

rule MALWARE_Win_RomCom_Loader {
    meta:
        author = "ditekShen"
        description = "Hunt for RomCom loader"
    //strings:
        //$s1 = "\\REGISTRY\\MACHINE\\SOFTWARE\\Classes" wide nocase
        //$s2 = "\\REGISTRY\\USER" wide nocase
        //$s3 = "CreateToolhelp32Snapshot" fullword ascii
    condition:
        uint16(0) == 0x5a4d and pe.is_dll() and (
            pe.exports("DllCanUnloadNow") and pe.exports("DllGetClassObject")
            and pe.exports("DllRegisterServer") and pe.exports("DllUnregisterServer")
            and pe.exports("GetProxyDllInfo")
        ) and for any fn in pe.export_details: (
            fn.forward_name contains "Dll"
        )
}

rule RomCom_Worker {
    meta:
        author = "ditekShen"
        description = "Hunt for RomCom worker"
        cape_type = "RomCom Payload"
    strings:
        $s1 = "UpdateProcThreadAttribute" fullword ascii
        $s2 = "WriteFile" fullword ascii
        $s3 = "GetAdaptersAddresses" fullword ascii nocase
        $s4 = /inflate\s\d+\.\d+\.\d+\sCopyright/ ascii
        $s5 = "SetHandleInformation" fullword ascii
        $s6 = "PeekNamedPipe" fullword ascii
    condition:
        uint16(0) == 0x5a4d and pe.is_dll() and pe.number_of_exports == 1 and pe.exports("Main") and all of them
}

rule RomCom_Dropper {
    meta:
        author = "ditekShen"
        description = "Hunt for RomCom worker"
        cape_type = "RomCom Payload"
    strings:
        $s1 = "\\REGISTRY\\MACHINE\\SOFTWARE\\Classes" wide nocase
        $s2 = "\\REGISTRY\\USER" wide nocase
        $s3 = "BINARY" fullword wide
        $s4 = "POST" fullword wide
    condition:
        uint16(0) == 0x5a4d and pe.is_dll() and pe.number_of_exports == 1 and pe.exports("Main") and 3 of them
}
