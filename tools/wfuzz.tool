{
	"toolname": "wfuzz_tool",
	"command": "wfuzz -c --hc 404  -t 200 -w /usr/share/wordlists/SecLists-master/Discovery/Web-Content/directory-list-2.3-medium.txt -f {outputdir}/{toolname}.txt http{s}://{domain}/FUZZ",
	"trigger": ["http", "https", "http-mgmt", "http-alt"],
	"active": false
}
