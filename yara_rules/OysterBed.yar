rule OysterBed
{
    meta:
        author = "enzok"
        description = "OysterBed Payload"
        cape_type = "OysterBed Payload"
        hash = "ecbe7875c593b2a78df82a16de05d59d06394c427b87bfb0d78a30035fad6409"
    strings:
        $endico = {80 [1-2] 65 75 ?? 80 [1-2] 01 6E 75 ?? 80 [1-2] 02 64 75 ?? 80 [1-2] 03 69 75 ?? 80 [1-2] 04 63 75 ?? 80 [1-2] 05 6F}
        $rc4decode_1 = {4? 8D 05 [4] 8B D? 4? 8B C? 4? 8B D8 E8 [4] 80 ?? 4D 74 ?? 80 ?? 01 5A}
        $rc4decode_2 = {4? 8D 05 [4] 4? 89 ?? E8 [4] 80 ?? 4D 74 ?? 80 ?? 01 5A 0F}
        $fail1 = "Fail Find End .ICO File\n"
        $fail2 = "Fail Find DLL File Round 2\n"
        $fail3 = "[CountStartupProcessSystem] EnumProcesses failed"
        $rc4key = "vpjNm4FDCr82AtUfhe39EG5JLwuZszKPyTcXWVMHYnRgBkSQqxzBfb6m75HZV3UyRY8vPxDna4WC2KMAgJjQqukrFdELXeGNSws9SBFXnYJ6ExMyu97KCebD5mTwaUj42NPAvHdkGhVtczWgfrZ3sLyRZg4HuX97AnQtK8xvpLU2CWDhVq5PEfjTNz36wdFasecBrkGSDApf83d6NMyaJCsvcRBq9ZYKthjuw5S27EVzWrPHgkmUxFL4bQSgMa4F"
    condition:
        4 of them
}
