rule Bandit {
    meta:
        author = "ditekSHen"
        description = "Detects Bandit Infostealer"
        cape_type = "Bandit Payload"
    strings:
       $x1 = "@Banditshopbot" ascii
       $x2 = "BANDIT STEALER" ascii
       $x3 = "Banditstealer" ascii
       $n1 = "bandit/browsers." ascii
       $n2 = "bandit/crypto." ascii
       $n3 = "bandit/decrypt." ascii
       $n4 = "bandit/messenger." ascii
       $n5 = "bandit/userdata." ascii
       $n6 = "bandit/utils." ascii
       $f1 = "main.sendZipToTelegram" fullword ascii
       $f2 = "main.killProcessHoldingFileHandle" fullword ascii
       $f3 = "main.killProcessByName" fullword ascii
       $f4 = "main.killProcessesHoldingFile" fullword ascii
       $f5 = "main.deleteDir" fullword ascii
       $f6 = "main.deleteUserDataDirs" fullword ascii
       $path = /bandit\/(browsers|common|crypto|messenger|userdata|utils)\/(browsers|common|crypto|messenger|userdata|utils)\.go/ ascii
       $m1 = "banditbot" ascii wide nocase
       $m2 = "blackListedIPS = [" ascii wide nocase
       $m3 = "blackListedPCNames = [" ascii wide nocase
       $m4 = "blackListedMacs = [" ascii wide nocase
       $m5 = "blacklisted_hwids = [" ascii wide nocase
       $m6 = "blacklisted_users = [" ascii wide nocase
       $m7 = "blacklisted_processes = [" ascii wide nocase
       $s1 = "User-AgentVirtualBox" ascii
       $s2 = "%s%sBinanceChainWallet" ascii
       $s3 = "coinbaseWalletcontent-lengthdata" ascii
       $s4 = "coinbaseWalletExtensioncommand" ascii
       $s5 = "\\s+pid:\\s+(\\d+)\\s+" ascii
       $s6 = "/user:Administrator" ascii
    condition:
      uint16(0) == 0x5a4d and (2 of ($x*) or 4 of ($n*) or 5 of ($f*) or ($path and (1 of ($n*) or 1 of ($f*))) or (1 of ($x*) and (1 of ($n*) or 1 of ($f2*))) or 6 of ($m*) or (all of ($s*)))
}
