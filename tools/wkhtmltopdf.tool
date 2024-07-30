{
	"toolname": "wkhtmltopdf",
	"command": "wkhtmltopdf {ip}:{port} {outputdir}/{toolname}.pdf",
	"trigger": ["http", "https", "http-mgmt", "http-alt"],
	"active": false
}
