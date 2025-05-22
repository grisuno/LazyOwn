{
	"toolname": "nikto_tool",
	"command": "nikto -ask no -host {ip} -port {port} -output {outputdir}/{toolname}.html",
	"trigger": ["http", "https", "http-mgmt", "http-alt"],
	"active": false
}
