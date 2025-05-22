{
	"toolname": "sslscan_tool",
	"command": "sslscan --xml=- {ip}:{port} > {outputdir}/{toolname}.xml",
	"trigger": ["https"],
	"active": false
}
