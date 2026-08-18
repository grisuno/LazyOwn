import "pe"

rule R77 {
    meta:
        author = "ditekSHen"
        description = "Detects r77 rootkit"
        cape_type = "R77 Payload"
    strings:
        $s1 = "startup" fullword wide
        $s2 = "process_names" fullword wide
        $s3 = "paths" fullword wide
        $s4 = "service_names" fullword wide
        $s5 = "tcp_local" fullword wide
        $s6 = "tcp_remote" fullword wide
        $s7 = "\\\\.\\pipe\\" wide
        $s8 = "SOFTWARE\\" wide
    condition:
        uint16(0) == 0x5a4d and (
            all of ($s*) or 
            (5 of them and pe.exports("ReflectiveDllMain")) or
            (5 of them and 
                for any i in (0 .. pe.number_of_sections) : (
                    (
                        pe.sections[i].name == ".detourd"
                    )
                )
            )
        )
}
