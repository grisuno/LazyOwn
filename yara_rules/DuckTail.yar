rule DuckTail {
    meta:
        author = "ditekSHen"
        description = "Detects DuckTail"
        cape_type = "DuckTail Payload"
    strings:
        $s1 = "&global_scope_id=" wide
        $s2 = "#ResolveMyIpAll" wide
        $s3 = "#ApproveInvitesHandler" wide
        $s4 = "#ProcessShareCok" wide
        $s5 = "#InviteEmpHandler" wide
        $s6 = "__activeScenarioIDs=%" wide
        $s7 = "&__a=1&fb_dtsg=" wide
        $s8 = "adAccountLimit\":(.*?)}" wide
        $s9 = "|PUSH|" fullword wide
        $s10 = "|SCREEN|" fullword wide
        $s11 = "|SCREEC|" fullword wide
        $s12 = "_ad_accounts>k__" ascii
        $s13 = "get_Pwds" fullword ascii
        $s14 = "Telegram.Bot" ascii
        $s15 = { 2f 00 7b 00 43 00 59 00 52 00 7d 00 2e 00 74 00
               78 00 74 00 00 15 2f 00 7b 00 4c 00 4f 00 47 00
               7d 00 2e 00 74 00 78 00 74 00 00 15 2f 00 7b 00
               43 00 46 00 47 00 7d 00 2e 00 74 00 78 00 74 00
               00 15 2f 00 7b 00 50 00 52 00 53 00 7d 00 2e 00
               74 00 78 00 74 00 00 15 2f 00 7b 00 53 00 43 00
               52 00 7d 00 2e 00 6a 00 70 00 67 }
    condition:
        uint16(0) == 0x5a4d and 13 of them
}
