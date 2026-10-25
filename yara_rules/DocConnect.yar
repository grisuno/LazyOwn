rule DocConnect
{
    meta:
        description = "DocConnect Loader"
        author = "enzok"
        cape_type = "TrustConnect Loader"
        hash = "a8fe355f21db53762e0e17e8fc8270ef39f9ff6582f3084ef6ddba28a81496ba"

    strings:
        $s1 = "DocConnect" ascii wide
        $s2 = "NATIVE_DLL_SEARCH_DIRECTORIES" ascii wide
        $s3 = "Ready to Run disabled - no loaded PE image"
        $s4 = "D3DCompiler_47_cor3" ascii wide
        $s5 = "runtimeconfig.json" ascii wide
        $s6 = "<application>.deps.json" ascii wide


        $dccfg = "DCCFG" ascii wide


    condition:
        uint16(0) == 0x5A4D and $dccfg and ($s1 or 3 of ($s*))
}
