{
	"toolname": "finalrecon",
	"command": "finalrecon --url=http{s}://{ip}:{port} --full -o txt -cd {outputdir}/{toolname}/ ",
	"trigger": ["http", "https", "http-mgmt", "http-alt"],
	"active": true
}