rule AxolotlLoader
{
    meta:
        author = "enzok"
        description = "AxolotlLoader Payload"
        cape_type = "AxolotlLoader Payload"

    strings:
        $s_api_init_guid = /\/api\/init\/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/ ascii nocase
        $s_inline_post = {E8 05 00 00 00 50 4F 53 54 00}
        $s_jfif_stub = {FF D8 FF E0 00 10 4A 46 49 46 00}

        $win1 = "InternetOpenA" ascii
        $win2 = "InternetConnectA" ascii
        $win3 = "HttpOpenRequestA" ascii
        $win4 = "HttpSendRequestA" ascii
        $win5 = "InternetReadFile" ascii
        $win6 = "InternetCloseHandle" ascii

        $http_hdr = "Content-Type: image/jpeg" ascii wide
        $http_ua  = /Mozilla\/5\.0 \(Windows NT [0-9\.]+; Win64; x64; rv:[0-9\.]+\) Gecko\/20100101 Firefox\/[0-9\.]+/ ascii wide

        $wh1 = "WinHttpOpen" ascii
        $wh2 = "WinHttpConnect" ascii
        $wh3 = "WinHttpOpenRequest" ascii
        $wh4 = "WinHttpAddRequestHeaders" ascii
        $wh5 = "WinHttpSendRequest" ascii
        $wh6 = "WinHttpReceiveResponse" ascii
        $wh7 = "WinHttpQueryDataAvailable" ascii

    condition:
        2 of ($s_*) and 1 of ($http*) and (4 of ($win*) or 4 of ($wh*))
}

rule AxolotlLoaderDll
{
    meta:
        author = "enzok"
        description = "AxolotlLoaderDll Payload"
        cape_type = "AxolotlLoader Payload"

strings:
        $resolver_loadlibrary = {E8 0D 00 00 00 4C 6F 61 64 4C 69 62 72 61 72 79 41 00 [1-10] 41 FF 97 ?? ?? ?? 00}
        $call_decoded_buffer = {49 8D 4D 10 49 8D 87 ?? ?? ?? 00 [0-30] FF (D0 | E0)}
        $alloc = {4? 83 EC ?? [2-12] 4? C7 ?? [4] 4? C7 C0 40 00 00 00 4? 8D ?? 24}

    condition:
        uint16(0) == 0x5A4D and all of them
}

rule AxolotlLoaderShellCode
{
    meta:
        author = "enzok"
        description = "AxolotlLoaderShellCode Payload"
        cape_type = "AxolotlLoader Payload"

    strings:
        $start = {C0 0F 84 [4] [0-6] FF D8 FF E0 00 10 4A 46 49 46}
        $xor_loop = {4? 83 E4 ?? 4? 83 EC ?? 4? 8D 05 [4] 4? 8D 0D [4] [7-13] 4? 83 C0 0? 4? 39 C8 72}
        $decoded1 = {48 39 F6 48 0F 44 31 48 39 FF 48 0F 44 79 08 E8}
        $decoded2 = {48 39 F6 75 ?? 48 39 F6 75 ?? 48 8B 31 48 39 FF 48 0F 44 79 08 E8}
    condition:
        $start and $xor_loop and 1 of ($decoded*)
}
