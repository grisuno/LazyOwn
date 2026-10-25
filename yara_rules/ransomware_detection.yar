rule ransomware_extensions {
    meta:
        description = "Detects common ransomware file extension patterns"
        author = "LazyOwn RedTeam"
        severity = "high"
        category = "ransomware"
    strings:
        $ext1 = ".encrypted" nocase wide ascii
        $ext2 = ".lock" nocase wide ascii
        $ext3 = ".crypt" nocase wide ascii
        $ext4 = ".pwned" nocase wide ascii
        $ext5 = ".enc" nocase wide ascii
    condition:
        2 of them
}

rule ransomware_notes {
    meta:
        description = "Detects ransomware ransom notes dropped on disk"
        author = "LazyOwn RedTeam"
        severity = "high"
        category = "ransomware"
    strings:
        $note1 = "YOUR FILES ARE ENCRYPTED" nocase wide ascii
        $note2 = "HOW TO RECOVER YOUR FILES" nocase wide ascii
        $note3 = "DECRYPTION INSTRUCTIONS" nocase wide ascii
        $note4 = "You have to pay" nocase wide ascii
        $note5 = "Bitcoin payment" nocase wide ascii
        $note6 = "Monero address" nocase wide ascii
    condition:
        any of them
}

rule ransomware_registry_keys {
    meta:
        description = "Detects ransomware-related Windows registry modifications"
        author = "LazyOwn RedTeam"
        severity = "high"
        category = "ransomware"
    strings:
        $key1 = "Software\\Microsoft\\Windows\\CurrentVersion\\Run" nocase wide
        $key2 = "EnableLinkedConnections" nocase wide
        $key3 = "DisableTaskMgr" nocase wide
        $key4 = "DisableCMD" nocase wide
        $shadow = "vssadmin delete shadows" nocase wide ascii
        $recovery = "bcdedit /set {default} recoveryenabled No" nocase wide ascii
    condition:
        ($shadow or $recovery) and any of ($key*)
}
