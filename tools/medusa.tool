{
	"toolname": "medusa",
	"command": "medusa -h {ip} -U sessions/users.txt -P /usr/share/wordlists/rockyou.txt -e ns -M ssh -n {port} > {outputdir}/{toolname}.txt",
	"trigger": ["ssh"],
	"active": true
}
