rule QwixxRAT {
    meta:
        author = "ditekSHen"
        description = "Detects QwixxRAT"
        cape_type = "QwixxRAT Payload"
    strings:
        $s1 = /Qwixx(\s)?Stealer/ ascii wide
        $s2 = "discord.gg/UXVFHzTjYe" wide
        $s3 = "t.me/QwixxTwixx" wide
        $s4 = "Secret Qwixx" wide
        $s5 = "\\Qwixx Rat\\" ascii
    condition:
        uint16(0) == 0x5a4d and 2 of them
}
