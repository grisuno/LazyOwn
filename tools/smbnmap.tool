{
	"toolname": "smbnmap",
	"command": "nmap --script smb-enum-domains.nse,smb-enum-groups.nse,smb-enum-processes.nse,smb-enum-sessions.nse,smb-enum-shares.nse,smb-enum-users.nse,smb-ls.nse,smb-mbenum.nse,smb-os-discovery.nse,smb-print-text.nse,smb-psexec.nse,smb-security-mode.nse,smb-server-stats.nse,smb-system-info.nse,smb-vuln-conficker.nse,smb-vuln-cve2009-3103.nse,smb-vuln-ms06-025.nse,smb-vuln-ms07-029.nse,smb-vuln-ms08-067.nse,smb-vuln-ms10-054.nse,smb-vuln-ms10-061.nse,smb-vuln-regsvc-dos.nse -p {port} {ip} -oN sessions/autoscan_{ip}_{port}.nmap --stylesheet sessions/nmap-bootstrap.xsl -oX sessions/autoscan_{ip}_{port}.nmap.xml  | tee {outputdir}/{toolname}.txt ; xsltproc -o  sessions/autoscan_{ip}_{port}.nmap.html sessions/nmap-bootstrap.xsl sessions/autoscan_{ip}_{port}.nmap.xml",
	"trigger": ["microsoft-ds"],
	"active": false
}
