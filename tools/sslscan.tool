{
	"toolname": "sslscan",
	"command": "sslscan --xml=- {ip}:{port} > {outputdir}/{toolname}.xml",
	"trigger": ["https"],
	"active": true
}
