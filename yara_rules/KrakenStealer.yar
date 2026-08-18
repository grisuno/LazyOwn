rule KrakenStealer {
    meta:
        author = "ditekSHen"
        description = "Detect Kraken infostealer"
        cape_type = "KrakenStealer Payload"
    strings:
        $x1 = /Kraken(_)?(Stub|Keyboard|Clipboard|GeneratorMachine|PostLogs|Screenshot|Keylogs|Password)/ ascii wide
        $s1 = /(get|set)_(Clipboard|Keyboard|Screen)Recorder/ fullword ascii
        $s2 = /Dumping(FileZilla|360_China|Opera|Epic|CocCoc|Thunderbird|Brave)/ fullword ascii
        $s3 = "ScreenPostData" fullword ascii
        $s4 = "encrypt_data" fullword ascii
        $s5 = "KeyboardProc" fullword ascii
        $s6 = "UploadsKeyboard" fullword ascii
        $s7 = "ClpUploader" fullword ascii
        $s8 = "StartKeylogger" fullword ascii
        $s9 = "ClipoDetectedRemover" fullword ascii
        $s10 = "Disable_Regis" fullword ascii
        $s11 = "RecordedClips" fullword ascii
        $s12 = "HoneyPotStatus" fullword ascii
    condition:
        uint16(0) == 0x5a4d and ((1 of ($x*) and 2 of ($s*)) or 9 of ($s*))
}
