rule ArrowRAT {
    meta:
        author = "ditekSHen"
        description = "Detects ArrowRAT"
        cape_type = "ArrowRAT Payload"
    strings:
        $s1 = "29mdHdhcmVcTWljcm9zb2Z0XFdpbmRvd3MgTlRcQ3VycmVudFZlcnNpb25cV2lubG9nb" wide
        $s2 = "Software\\Classes\\ms-settings\\shell\\open\\command" wide
        $s3 = "DelegateExecute" fullword wide
        $s4 = "powershell" wide
        $s5 = "DESKTOP_HOOKCONTROL" fullword ascii
        $s6 = "PROCESS_INFORMATION" fullword ascii
        $s7 = "STARTUP_INFORMATION" fullword ascii
        $s8 = /(Venom|Pandora)\shVNC/ fullword wide
        $s9 = "cmd.exe /k START" fullword wide
        $s10 = "ExclusionWD" fullword ascii
        $s11 = "WinExec" fullword ascii
    condition:
        uint16(0) == 0x5a4d and 5 of them
}
