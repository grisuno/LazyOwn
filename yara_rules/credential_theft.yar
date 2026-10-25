
rule CredentialTheft_Tools {
    meta:
        description = "Detects credential theft tools and dumpers"
        author = "LazyOwn"
        severity = "critical"
        category = "credential_access"
    strings:
        $mimikatz = "mimikatz" ascii wide nocase
        $mimidrv = "mimidrv" ascii wide nocase
        $sekurlsa = "sekurlsa" ascii wide nocase
        $lsadump = "lsadump" ascii wide nocase
        $laZagne = "laZagne" ascii wide nocase
        $pypykatz = "pypykatz" ascii wide nocase
        $mimipenguin = "mimiPenguin" ascii wide nocase
        $procdump_cmd = "procdump" ascii wide nocase
        $sam_dump = "samdump" ascii wide nocase
    condition:
        any of them
}
