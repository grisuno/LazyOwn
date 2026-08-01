rule c2_http_beacon {
    meta:
        description = "Detects HTTP-based C2 beacon communication patterns"
        author = "LazyOwn RedTeam"
        severity = "critical"
        category = "c2"
    strings:
        $beacon1 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        $beacon2 = "Mozilla/5.0 (X11; Linux x86_64)"
        $pattern1 = "/login/process.php"
        $pattern2 = "/submit.php?id="
        $pattern3 = "/news.php"
        $pattern4 = "/jquery-3.3.1.min.js"
        $sleep1 = "sleep" nocase ascii
        $jitter1 = "jitter" nocase ascii
        $cobalt1 = "/ca" ascii
        $cobalt2 = "/submit" ascii
        $cobalt3 = "/pixel" ascii
        $cb_conf = "sleeptime" nocase wide ascii
        $hb1 = "HTTP/1.1 200 OK" nocase ascii
        $hb2 = "Content-Type: text/plain" nocase ascii
        $hb3 = "Content-Length: 0" nocase ascii
    condition:
        ($cobalt1 and $cobalt2 and $cobalt3) or
        ($pattern2 and $sleep1 and $jitter1) or
        ($beacon1 and $pattern1 and $hb1) or
        ($cb_conf and $sleep1)
}

rule c2_dns_tunneling {
    meta:
        description = "Detects DNS tunneling used for C2 communication"
        author = "LazyOwn RedTeam"
        severity = "high"
        category = "c2"
    strings:
        $dns1 = "AAAA" ascii
        $dns2 = "TXT" ascii
        $tun1 = "900-byte" ascii
        $tun2 = "Base64" ascii
        $iodine = "iodine" nocase ascii
        $dnscat = "dnscat2" nocase ascii
        $dnsexx = "dnsexe" nocase ascii
    condition:
        2 of ($tun1, $tun2, $iodine, $dnscat, $dnsexx) and ($dns1 or $dns2)
}

rule c2_sliver_metasploit {
    meta:
        description = "Detects Sliver and Metasploit C2 framework indicators"
        author = "LazyOwn RedTeam"
        severity = "high"
        category = "c2"
    strings:
        $sliver1 = "sliver" nocase ascii
        $sliver2 = "BishopFox" nocase ascii
        $meterp = "meterpreter" nocase ascii
        $msf1 = "windows/meterpreter/reverse" nocase ascii
        $msf2 = "payload/windows" nocase ascii
        $msf3 = "metasploit" nocase ascii
        $mtls = "mtls://" nocase ascii
        $wg = "WireGuard" nocase ascii
    condition:
        any of ($sliver*) or (any of ($msf*) and ($meterp or $mtls)) or ($sliver2)
}
