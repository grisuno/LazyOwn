{
	"toolname": "kerbrute",
	"command": "kerbrute userenum --dc {ip} -d {domain} -t 20  /usr/share/wordlists/SecLists-master/Usernames/xato-net-10-million-usernames.txt | tee {outputdir}/{toolname}.txt",
	"trigger": ["kerberos-sec"],
	"active": true
}