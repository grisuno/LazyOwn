{
	"toolname": "ffuf",
	"command": "ffuf -u http{s}://{ip}:{port}/FUZZ -w /usr/share/wordlists/dirb/common.txt -mc 200,204,301,302,307,401 -o {outputdir}/{toolname}.txt",
	"trigger": ["http", "https", "http-mgmt", "http-alt"],
	"active": true
}
