{
	"toolname": "smbmap",
	"command": "smbmap -H {ip} -u '{username}' {password} -A '(xlsx|docx|txt|xml)' -r --no-banner | tee {outputdir}/{toolname}.txt",
	"trigger": ["microsoft-ds"],
	"active": true
}
