{
	"toolname": "hydrardp",
	"command": "hydra -L sessions/users.txt -P /usr/share/wordlists/rockyou.txt rdp://{ip}:{port} > {outputdir}/{toolname}.txt",
	"trigger": ["rdp"],
	"active": true
}
