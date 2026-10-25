rule PWSHCUMII {
    meta:
        author = "ditekSHen"
        description = "Detects multi-dropper PowerShell"
        cape_type = "CUMII Payload"
    strings:
        $s1 = ".('{1}{$}'.replace('$','0')" ascii nocase
        $s2 = ",'I').replace('!','ex')" ascii nocase
        $s3 = "'.replace('*','0001')" ascii nocase
        $s4 = "Remove-Item $" ascii nocase
        $s5 = "the File will start cumiing" ascii nocase
        $b1 = "011001100111010101101110011*" ascii
        $b2 = "0101001000*1110110*010011111" ascii
        $b3 = "01001101010110101001*11*0000" ascii
    condition:
       (3 of ($s*) and 1 of ($b*))
}
