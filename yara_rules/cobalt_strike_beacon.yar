
rule CobaltStrike_Beacon_Config {
    meta:
        description = "Detects Cobalt Strike beacon configuration patterns"
        author = "LazyOwn"
        severity = "critical"
        category = "c2"
    strings:
        $profile_cfg = "%c%" ascii
        $uri_1 = "/submit.php" ascii wide
        $uri_2 = "/jquery" ascii wide
        $sleep_mask = { 69 ?? 69 ?? 69 ?? 69 }
        $malleable = "Mozilla/5.0" ascii wide
    condition:
        uint16(0) == 0x5A4D and any of them
}
