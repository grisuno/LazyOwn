rule RustyLoader {
    meta:
        author = "enzok"
        description = "RustyLoader Loader"
        cape_type = "RustyLoader Loader"
        hash = "93389f4234f81358fa29c65473b5bfc3c60ab7b3c2189185988f03a66aeda66f"
    strings:
        $seed = {0F 11 ?? ?? ?? 00 00 48 B8 [8] 48 89 85 [4] C7 85 [8] 66 C7 85}
        $decrypt1_1 = {FF C? 0F B6 D? 4? 8? ?? 15 [4] 4? 00 C1 4? 0F B6 C9}
        $decrypt1_2 = {4? 0F B6 C0 4? 8A 84 05 [4] 4? 30 04 07 4? FF C0 4? 39 C6 75 ?? 4? 63 77}
        $decrypt2_1 = {FF C? 0F B6 D? 4? 8? 95 [4] 02 8C 15 [4] 4? 0F B6 C1}
        $decrypt2_2 = {0F B6 D2 8A 94 15 [4] 30 14 1E 4? FF C3 EB ?? 4? 8B}
        $mz_check = {4? 63 ?? 3C 31 C0 4? 85 ?? 0F 95 C0 66 81 3? 4D 5A}
    condition:
        uint16(0) == 0x5A4D and
        $seed and
        (all of ($decrypt1_*) or all of ($decrypt2_*)) and
        $mz_check
}