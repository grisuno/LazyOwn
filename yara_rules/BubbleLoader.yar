rule BubbleLoader
{
    meta:
        author = "enzok"
        description = "BubbleLoader Loader"
        cape_type = "BubbleLoader Loader"
        hash1 = "5397e96e590d5274bdbdb353c651d0c7087c848c640f5199c62a00720050b9a4"
        hash2 = "aa86a08cf0f2bcdc26a04c4fba92957e0ecbc5d2c9f1e2c7278b6498a6738a41"
        hash3 = "a7fc44c3665cb254f73fc16e4950eb111f910573e0f0cf63471cce69c04fc684"
    strings:
        $png_hdr = {49 45 4e 44 ae 42 60 82 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52}
        $stub = {55 48 [2] 48 83 [2] 49 55 41 56 53 [4] 51 52 [2] 08 15 09 d7 94 dc}
        $decrypt = {48 0f b6 01 48 85 c9 75 08 [4] 00 00 00 00 30 02 48 85 d2 75 08 [4] 00 00 00 00 48 83 c2 01 48 83 c1 01 4c 39 c2 72 bf}
    condition:
        uint16(0) == 0x5A4D and ($stub or $decrypt) and $png_hdr
}


