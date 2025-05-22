{
	"toolname": "subwfuzz_tool",
	"command": "wfuzz -c --hc 404,301 -t 200 -w /usr/share/wordlists/SecLists-master/Discovery/DNS/subdomains-top1million-110000.txt -H 'Host: FUZZ.{domain}' -f {outputdir}/{toolname}.txt {domain}",
	"trigger": ["http", "https", "http-mgmt", "http-alt"],
	"active": true
}
