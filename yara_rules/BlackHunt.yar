rule BlackHunt {
    meta:
        author = "ditekSHen"
        description = "Detects BlackHunt ransomware"
        cape_type = "BlackHunt Payload"
    strings:
        $s1 = /#BlackHunt_(Logs|BG|Icon|Public|Private|ID|ReadMe|Update)\.(txt|jpg|ico|key|hta)/ ascii wide
        $s2 = /-(biggame|noencrypt|netinfo|nospread)/ fullword wide
        $s3 = "/v \"*BlackHunt\" /t REG_SZ /d" wide
        $s4 = "/sc onstart /TN \"Windows Critical Update\" /TR \"'%s' %s\" /F" wide
        $s5 = "/v \"DisableChangePassword\" /t REG_DWORD /d" wide
        $s6 = "<span> %s </span>this ID (<span> %s </span>)" wide
        $s7 = "}div.header h1 span#hunter" wide
        $s8 = "BLACK_HUNT_MUTEX" fullword ascii
    condition:
        uint16(0) == 0x5a4d and 4 of them
}
