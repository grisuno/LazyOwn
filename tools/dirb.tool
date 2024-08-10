{
	"toolname": "dirb",
	"command": "dirb http{s}://{ip}:{port} -o {outputdir}/{toolname}.txt -f",
	"trigger": ["http", "https", "http-mgmt", "http-alt"],
	"active": true
}
