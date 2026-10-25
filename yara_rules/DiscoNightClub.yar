rule DiscoNightClub {
    meta:
        author = "ditekSHen"
        description = "Hunts for Disco NightClub"
        cape_type = "DiscoNightClub Payload"
    strings:
        $s1 = "\\OfficeBroker\\OfficeBroker.exe" ascii wide nocase
        $s2 = "\\EDGEUPDATE\\EDGEAOUT" ascii wide nocase
        $s3 = "\\EDGEUPDATE\\update" ascii wide nocase
        $s4 = "windows.system.update.com" ascii wide nocase
        $s5 = "edgeupdate-security-windows.com" ascii wide nocase
        $s6 = "nightclub::" ascii wide nocase
        $s7 = "EncryptedPasswordFlt" ascii wide nocase
        $s8 = "Microsoft\\def\\Gfr45.cfg" ascii wide nocase
        $s9 = "::keylog::" ascii wide nocase
        $pdb1 = "\\AbcdMainProject\\Rootsrc\\Projects\\MainS\\Ink\\" ascii wide nocase
        $pdb2 = "\\Autogen\\Kh\\AutogenAlg\\" ascii wide nocase
    condition: 
        uint16(0) == 0x5a4d and ((1 of ($pdb*) and 2 of ($s*)) or (4 of ($s*)))
}
