{
	"toolname": "hydrasmb",
	"command": "hydra -L sessions/users.txt -P /usr/share/wordlists/rockyou.txt smb://{ip}:{port} > {outputdir}/{toolname}.txt",
	"trigger": ["smb"],
	"active": true
}
