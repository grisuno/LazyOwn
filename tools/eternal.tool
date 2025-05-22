{
	"toolname": "etarnalblue",
	"command": "nmap -p {port} --script smb-vuln-ms17-010 {ip} -oN {outputdir}/{toolname}.txt",
	"trigger": ["microsoft-ds"],
	"active": false
}
