{
	"toolname": "sslyze_tool",
	"command": "sslyze --regular --xml_out=- {ip}:{port} > {outputdir}/{toolname}.xml",
	"trigger": ["https"],
	"active": false
}
