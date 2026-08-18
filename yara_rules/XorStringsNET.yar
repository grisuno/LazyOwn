import "dotnet"

rule XorStringsNET {
    meta:
        description = "Detects XorStringsNET string encryption, and other obfuscators derived from it"
        author = "dr4k0nia"
        version = "1.0"
        date = "26/03/2023"
    strings:
        $pattern = { 06 1e 58 07 8e 69 fe 17 }
    condition:
        uint16be(0) == 0x4d5a
        and dotnet.is_dotnet
        and $pattern
}
