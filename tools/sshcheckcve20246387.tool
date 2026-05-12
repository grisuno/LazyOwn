{
  "toolname": "sshcheckcve20246387",
  "command": "python3 /home/grisun0/LazyOwn/external/.exploit/CVE-2024-6387/CVE-2024-6387.py scan -T {ip} -p {port} -n tun0 | tee {outputdir}/{toolname}.txt",
  "trigger": [
    "ssh"
  ],
  "active": false,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: sshcheckcve20246387 \u2014 triggers on ['ssh']"
}