{
	"toolname": "dirb",
	"command": "dirb http{s}://{ip}:{port} -o {outputdir}/{toolname}.txt",
	"trigger": ["http", "https", "http-mgmt", "http-alt"],
	"active": true
}
