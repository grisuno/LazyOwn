rule Mystic {
    meta:
        author = "ditekSHen"
        description = "Hunts for Mystic Infostealer"
        cape_type = "Mystic Payload"
    strings:  
        $s1 = "LaStFiLe:)" ascii wide
        $s2 = "LaStPrOcEsS:)" ascii wide
        $s3 = "credit_cards" ascii wide
        $s4 = "number_of_processors" ascii wide
        $s5 = "computername" ascii wide
        $p1 = "G:\\Projects\\Python\\morpher\\" ascii wide
        $p2 = /G:\\Projects\\stealer\\.{15}\\Release\\.{5,25}\.pdb/ ascii wide
    condition:
        (uint16(0) == 0x5a4d and (4 of ($s*) or (1 of ($p*) and 3 of ($s*)))) or (all of ($s*))
}
