{
	"toolname": "dirb_domain_tool",
	"command": "dirb http{s}://{domain} -o {outputdir}/{toolname}.txt -f",
	"trigger": ["http", "https", "http-mgmt", "http-alt"],
	"active": false
}
