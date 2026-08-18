import "pe"

rule STEALDEAL {
    meta:
        author = "ditekShen"
        description = "Hunt for STEALDEAL stealer"
        cape_type = "STEALDEAL Payload"
    strings:
        $x1 = "stealDll.dll" fullword ascii
        $s1 = "SqlExec" fullword ascii
        $s2 = "etilqs_" fullword ascii
        $s3 = "SUBQUERY %u" fullword ascii
    condition:
        uint16(0) == 0x5a4d and pe.is_dll() and pe.exports("stub") and (1 of ($x*) or all of ($s*))
}
