rule privilege_escalation_tools {
    meta:
        description = "Detects common privilege escalation tool indicators"
        author = "LazyOwn RedTeam"
        severity = "high"
        category = "privesc"
    strings:
        $linpeas = "linpeas" nocase wide ascii
        $winpeas = "winpeas" nocase wide ascii
        $mimikatz1 = "mimikatz" nocase wide ascii
        $mimikatz2 = "sekurlsa" nocase wide ascii
        $mimikatz3 = "kiwi" nocase wide ascii
        $lazagne = "lazagne" nocase wide ascii
        $procdump = "procdump" nocase wide ascii
        $pspy = "pspy" nocase wide ascii
        $find_suid = "find / -perm -4000" nocase ascii
        $find_cap = "getcap -r /" nocase ascii
        $suid = "-u=s -g=s" nocase ascii
        $docker_escape = "docker run -v /:/host" nocase ascii
        $nsenter = "nsenter --mount" nocase ascii
        $cgroup = "cgroup" nocase ascii
    condition:
        any of them
}

rule credential_dump_patterns {
    meta:
        description = "Detects credential dumping tool output and commands"
        author = "LazyOwn RedTeam"
        severity = "critical"
        category = "credential_access"
    strings:
        $sam = "SAM" wide ascii
        $system_hive = "SYSTEM" wide ascii
        $security_hive = "SECURITY" wide ascii
        $ntds = "ntds.dit" nocase wide ascii
        $lsass = "lsass.exe" nocase wide ascii
        $reg_save = "reg save" nocase ascii
        $shadow_copy = "vssadmin create shadow" nocase wide ascii
        $ntlm_hash = "$NT$" ascii
        $krb5 = "krb5tgs$" ascii
        $ticket = "kirbi" nocase ascii
        $cmdkey = "cmdkey /list" nocase wide ascii
        $dpapi = "dpapi::" nocase ascii
        $masterkey = "masterkey" nocase ascii
    condition:
        2 of them
}
