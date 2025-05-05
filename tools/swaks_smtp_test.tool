{
    "toolname": "swaks_smtp_test",
    "command": "swaks --to info@{domain} --from attacker@test.com --server {ip} > {outputdir}/swaks_smtp_test.txt",
    "trigger": ["smtp"],
    "active": true
}