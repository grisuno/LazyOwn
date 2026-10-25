rule RootTeamStealer {
    meta:
        author = "ditekSHen"
        description = "Detects RootTeam infostealer"
        cape_type = "RootTeamStealer Payload"
    strings:
        $x1 = "RootTeamStl" ascii
        $x2 = "Bot: https://t.me/rootteam_bot" ascii
        $x3 = "rootteam_bot" ascii
        $x4 = "Root Team" ascii
        $s1 = "-ldflags=\"-s -w -H windowsgui -X" ascii
        $s2 = "'RootTeamStl/vars." ascii
        $s3 = "{ Hostname string \"json:\\\"hostname\\\"\"; EncryptedUsername string \"json:\\\"encryptedUsername\\\"\"; EncryptedPassword string \"json:\\\"encryptedPassword\\\"\" }" ascii
        $s4 = "\\Program Files (x86)\\Steam\\config\\loginusers.vdf" ascii
        $s5 = /RootTeamStl\/managers\/(browser|coldwallets|discord|filegrabber|steam|userinformation)?/ ascii
    condition:
        uint16(0) == 0x5a4d and (3 of ($x*) or (1 of ($x*) and 3 of ($s*)) or 4 of ($s*) or 5 of them)
}
