rule UmbralStealer {
    meta:
        author = "ditekShen"
        description = "Detects Umbral infostealer"
        cape_type = "UmbralStealer Payload"
    strings:
        $x1 = "Umbral Stealer" wide
        $x2 = "Umbral.payload." ascii
        $s1 = "U2V0LU1wUHJlZmVyZW5jZ" wide
        $s2 = "{{ Key = {0}, Value = {1} }}" wide
        $s3 = "csproduct get uuid" wide
        $s4 = "0.0.0.0 www." 
        $s5 = /(set|get)_Take(Screen|WebcamSnap)shot/ fullword ascii
        $s6 = "still_pin" fullword ascii
        $c1 = "kaspersky.com" wide
        $c2 = "bitdefender.com" wide
        $c3 = "virustotal.com" wide
        $c4 = "malwarebytes.com" wide
        $c5 = "clamav.net" wide
        $c6 = "trendmicro.com" wide
    condition:
       uint16(0) == 0x5a4d and (1 of ($x*) or 5 of ($s*) or (3 of ($s*) and 4 of ($c*))) 
}
