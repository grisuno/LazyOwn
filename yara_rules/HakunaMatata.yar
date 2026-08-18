rule HakunaMatata {
    meta:
        author = "ditekSHen"
        description = "Detects HakunaMatata ransomware"
        cape_type = "HakunaMatata Payload"
    strings:
        $s1 = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" wide
        $s2 = "(?:[13]{1}[a-km-zA-HJ-NP-Z1-9]{26,33}|bc1[a-z0-9]{39,59})" wide
        $s3 = "<RSAKeyValue><Modulus>" wide
        $s4 = "HAKUNA MATATA" ascii wide nocase
        $s5 = "EXCEPTIONAL_FILE" ascii
        $s6 = "TRIPLE_ENCRYPT" ascii
        $s7 = "FULL_ENCRYPT" ascii
        $s8 = "TARGETED_EXTENSIONS" ascii
        $s9 = "CHANGE_PROCESS_NAME" ascii
        $s10 = "KILL_APPS_ENCRYPT_AGAIN" ascii
        $s11 = "<ALL_DRIVES>b__" ascii
        $s12 = "dataToEncrypt" ascii
        $s13 = "<RECURSIVE_DIRECTORY_LOOK>" ascii
        $b1 = "ENCRYPT FILES IN PROCESS" wide
        $b2 = "#TARGET_FILES" ascii wide
        $b3 = "#PRIVATE_KEY" ascii wide
        $b4 = "/target:winexe /platform:anycpu /optimize+" wide
        $b5 = "/win32icon:" fullword wide
        $b6 = "SkippedFolders" ascii
        $b7 = "RECURSIVE_DIRECTORY_LOOK(" ascii
        $b8 = "DRAW_WALLPAPER(" ascii
        $b9 = "startupKey.SetValue(MESSAGE_FILE.Split('.')[0], executablePath);" ascii
        $b10 = /\\obj\\(Debug|Release)\\Hakuna\sMatata\.pdb/ ascii
    condition:
        uint16(0) == 0x5a4d and 6 of them
}
