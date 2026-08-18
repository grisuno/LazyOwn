rule Sliver {
     meta:
        author = "ditekSHen"
        description = "Detects Sliver implant cross-platform adversary emulation/red team"
        cape_type = "Sliver Payload"
    strings:
        $x1 = "github.com/bishopfox/sliver/protobuf/sliverpbb." ascii
        $s1 = ".commonpb.ResponseR" ascii
        $s2 = ".PortfwdProtocol" ascii
        $s3 = ".WGTCPForwarder" ascii
        $s4 = ".WGSocksServerR" ascii
        $s5 = ".PivotEntryR" ascii
        $s6 = ".BackdoorReq" ascii
        $s7 = ".ProcessDumpReq" ascii
        $s8 = ".InvokeSpawnDllReq" ascii
        $s9 = ".SpawnDll" ascii
        $s10 = ".TCPPivotReq" ascii
    condition:
        (uint16(0) == 0x5a4d or uint16(0) == 0x457f or uint16(0) == 0xfacf) and (1 of ($x*) or 5 of ($s*))
}
