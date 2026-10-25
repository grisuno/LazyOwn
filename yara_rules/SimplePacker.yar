rule SimplePacker {
    meta:
        author = "ditekSHen"
        description = "Detects Hydrochasma packer / dropper"
        cape_type = "SimplePacker Payload"
    strings:
        $p1 = "\\cloud-compiler-" ascii
        $p2 = "\\deps\\simplepacker.pdb" ascii
        $s1 = "uespemosarenegylmodnarodsetybdetqueue" ascii
        $s2 = "None{\"" ascii
    condition:
        uint16(0) == 0x5a4d and (all of ($p*) and 1 of ($s*))
}
