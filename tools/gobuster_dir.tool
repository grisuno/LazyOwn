{
  "toolname": "gobuster_http",
  "command": "gobuster dir -u https://{domain} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -o {outputdir}/gobuster_{port}.txt",
  "trigger": [
    "http",
    "http-proxy",
    "https-alt",
    "https"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: gobuster_http \u2014 triggers on ['http', 'http-proxy', 'https-alt', 'https']"
}