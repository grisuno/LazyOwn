{
  "toolname": "swaks_smtp_test",
  "command": "swaks --to info@{domain} --from attacker@test.com --server {ip} > {outputdir}/swaks_smtp_test.txt",
  "trigger": [
    "smtp"
  ],
  "active": true,
  "category": "01. Reconnaissance",
  "description": "Pwntomate tool: swaks_smtp_test \u2014 triggers on ['smtp']"
}