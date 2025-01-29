{
	"toolname": "bigbang",
	"command": "cd /home/grisun0/src/scripts ; python3 exploit_bigbang.py | tee {outputdir}/{toolname}.txt",
	"trigger": ["http", "https", "http-mgmt", "http-alt"],
	"active": true
}
