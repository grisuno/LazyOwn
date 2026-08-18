rule AgnianeStealer {
    meta:
        author = "ditekSHen"
        description = "Detects Agniane infostealer"
        cape_type = "AgnianeStealer Payload"
    strings:
        $x1 = "Agniane.pdb" ascii
        $x2 = "IEnumerable<Agniane.Classes.LogRecord>." ascii
        $x3 = "Agniane Stealer" wide
        $x4 = "cinoshibot" wide
        $x5 = "yqbiguuno2zp5jxsmqbev4rwckvy27bqws5cgm3hiid7xolt65j72kqd.onion" wide
        $s1 = "<Pass encoding=\"base64\">" wide
        $s2 = "Domain Detect: detected {0}" wide
        $s3 = "DOMAINDETECTCOOKIES" ascii
        $s4 = /(Opera|Edge|Chrome|Brave|Vivaldi|Blink|Universal|Gecko|OperaGx|Firefox)Grabber/ fullword ascii
        $u1 = "/antivm.php?id=" wide
        $u2 = "/ferr.php?id=" wide
        $u3 = ".php?ownerid=" wide
        $u4 = "&buildid=" wide
        $u5 = "&username=" wide
        $u6 = "&BSSID=" wide
        $u7 = "&rndtoken=" wide
        $u8 = "&domaindetects=" wide
    condition:
       uint16(0) == 0x5a4d and (2 of ($x*) or (1 of ($x*) and (2 of ($s*) or 3 of ($u*))) or (all of ($s*) and 3 of ($u*)) or (7 of ($u*)))
}
