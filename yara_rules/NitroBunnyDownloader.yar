rule NitroBunnyDownloader
{
    meta:
        author = "enzok"
        description = "NitroBunnyDownloader"
        cape_type = "NitroBunnyDownloader Payload"
        hash = "960e59200ec0a4b5fb3b44e6da763f5fec4092997975140797d4eec491de411b"
        hash2 = "a9be0114857faacd4d5781459b5f8305d07e48c2541f74885a9f194cfcb20456"
    strings:
        $config1 = {E8 [3] 00 41 B8 ?? ?? 00 00 48 8D 15 [3] 00 48 (89 C1 | 8B C8) 4? 89 ?? E8 [3] 00}
        $config2 = {E8 [3] 00 48 8D 15 [3] 00 41 B8 ?? ?? 00 00 48 (89 C1 | 8B C8) 4? 89 ?? E8 [3] 00}
        $config3 = {E8 [3] 00 48 (8B C8 | 89 C1) 48 8D 15 [3] 00 41 B8 ?? ?? 00 00 4? 8B ?? E8 [3] 00}
    condition:
        uint16(0) == 0x5A4D and any of ($config*)
}
