{
	"toolname": "dig",
	"command": "dig any {domain} @{ip} | tee {outputdir}/{toolname}.txt",
	"trigger": ["domain"],
	"active": true
}
