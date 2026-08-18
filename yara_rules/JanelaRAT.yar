rule JanelaRAT {
    meta:
        author = "ditekSHen"
        description = "Detects JanelaRAT"
        cape_type = "JanelaRAT Payload"
    strings:
        $x1 = "<Janela>k__" ascii
        $x2 = "janela" fullword ascii
        $x3 = "\\CSHARP\\RAT\\" ascii
        $s1 = "<SystemInfos>k__" ascii
        $s2 = "<SendKeepAlives>b__" ascii
        $s3 = "hookStruct" fullword ascii
        $s4 = "[^a-zA-Z]" fullword wide
        $s5 = "GetRecycled" fullword ascii
        $s6 = "import \"bcl.proto\";" wide
        $s7 = "\\KL_FINAL\\" ascii
        $s8 = "\\KL_FASEAVAST" ascii
        $s9 = "\\kl c++" ascii
        $s10 = "VisaoAPP" ascii wide
    condition:
        uint16(0) == 0x5a4d and (all of ($x*) or (2 of ($x*) and 3 of ($s*)) or (1 of ($x*) and 5 of ($s*)) or (6 of ($s*)))
}
