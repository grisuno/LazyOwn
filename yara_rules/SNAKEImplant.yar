rule SNAKE {
    meta:
        author = "ditekSHen"
        description = "Detects SNAKE implant"
        cape_type = "SNAKE Payload"
    strings:
        $c1 = { 25 73 23 31 }
        $c2 = { 25 73 23 32 }
        $c3 = { 25 73 23 33 }
        $c4 = { 25 73 23 34 }
        $c5 = { 2e 74 6d 70 }
        $c6 = { 2e 73 61 76 }
        $c7 = { 2e 75 70 64 }
        $s1 = "tapisetschema.dll" fullword wide
        $s2 = "\\\\.\\%s\\\\" fullword ascii wide
        $s3 = "\\BaseNamedObjects\\%S" fullword wide
        $s4 = "{CACE3174-CF88-4906-921A-A16A7DC8CF4B}.{B6066E99-37D7-4668-9B06-301CE2C1D367}.crmlog" ascii
        $s5 = "-crash-" fullword ascii
        $s6 = "rcv_buf=%d%c" fullword ascii
        $s7 = "write_peer_nfo=%s:%d%cfrag_no_scrambling=Y%c" fullword ascii
    condition:
        (uint16(0) == 0x5a4d and (all of ($s*) or (all of ($c*) and 1 of ($s*)))) or (all of ($c*) and 1 of ($s*))
}
