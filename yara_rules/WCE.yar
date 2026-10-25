rule WindowsCredentialsEditor
{
meta:
	description = "Identifies Windows Credentials Editor (WCE), post-exploitation tool."
	author = "@bartblaze"
	date = "2020-01"
	reference = "https://www.ampliasecurity.com/research/windows-credentials-editor/"
	tlp = "White"
	cape_type = "WCE Payload"

strings:
	$ = "Windows Credentials Editor" ascii wide
	$ = "Can't enumerate logon sessions!" ascii wide
	$ = "Cannot get PID of LSASS.EXE!" ascii wide
	$ = "Error: cannot dump TGT" ascii wide
	$ = "Error: Cannot extract auxiliary DLL!" ascii wide
	$ = "Error: cannot generate LM Hash." ascii wide
	$ = "Error: cannot generate NT Hash." ascii wide
	$ = "Error: Cannot open LSASS.EXE!." ascii wide
	$ = "Error in cmdline!." ascii wide
	$ = "Forced Safe Mode Error: cannot read credentials using 'safe mode'." ascii wide
	$ = "Reading by injecting code! (less-safe mode)" ascii wide
	$ = "username is too long!." ascii wide
	$ = "Using WCE Windows Service.." ascii wide
	$ = "Using WCE Windows Service..." ascii wide
	$ = "Warning: I will not be able to extract the TGT session key" ascii wide
	$ = "WCEAddNTLMCredentials" ascii wide
	$ = "wceaux.dll" ascii wide fullword
	$ = "WCEGetNTLMCredentials" ascii wide
	$ = "wce_ccache" ascii wide fullword
	$ = "wce_krbtkts" ascii wide fullword

condition:
	3 of them
}

rule WCE
{
	meta:
		description		= "Windows Credentials Editor"
		author			= "Benjamin DELPY (gentilkiwi)"
		tool_author		= "Hernan Ochoa (hernano)"
		cape_type		= "WCE Payload"

	strings:
		$hex_legacy		= { 8b ff 55 8b ec 6a 00 ff 75 0c ff 75 08 e8 [0-3] 5d c2 08 00 }
		$hex_x86		= { 8d 45 f0 50 8d 45 f8 50 8d 45 e8 50 6a 00 8d 45 fc 50 [0-8] 50 72 69 6d 61 72 79 00 }
		$hex_x64		= { ff f3 48 83 ec 30 48 8b d9 48 8d 15 [0-16] 50 72 69 6d 61 72 79 00 }

	condition:
		any of them
}
