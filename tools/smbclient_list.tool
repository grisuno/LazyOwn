{
    "toolname": "smbclient_list",
    "command": "smbclient -L \\\\\\\\{ip}\\\\ -N > {outputdir}/smb_shares.txt",
    "trigger": ["microsoft-ds"],
    "active": true
}