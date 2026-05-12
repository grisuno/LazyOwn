{
  "toolname": "bigbang",
  "command": "cd /home/grisun0/src/scripts ; python3 exploit_bigbang.py | tee {outputdir}/{toolname}.txt",
  "trigger": [
    "http",
    "https",
    "http-mgmt",
    "http-alt"
  ],
  "active": false,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: bigbang \u2014 triggers on ['http', 'https', 'http-mgmt', 'http-alt']"
}