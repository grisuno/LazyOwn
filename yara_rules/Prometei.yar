rule Prometei
{
    meta:
        id = "1tLZbijQrm8kKt1oDLFgVx"
        fingerprint = "59c25b325938e0ade0f4437005d25e48444f5a79a91f7836490e826e588c2e66"
        version = "1.0"
        first_imported = "2023-03-24"
        last_modified = "2023-03-24"
        status = "RELEASED"
        sharing = "TLP:WHITE"
        source = "BARTBLAZE"
        author = "@bartblaze"
        description = "Identifies Prometei botnet main modules."
        category = "MALWARE"
        malware = "PROMETEI"
        malware_type = "BOT"
        reference = "https://malpedia.caad.fkie.fraunhofer.de/details/win.prometei"
        cape_type = "Prometei payload"

  strings:
    $ = "prometeicmd" ascii wide fullword
    $ = "/cgi-bin/prometei.cgi" ascii wide
    
condition:
    any of them
}
