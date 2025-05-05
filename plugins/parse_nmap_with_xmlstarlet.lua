function parse_nmap_with_xmlstarlet()
    local session_dir = "sessions"
    local output_dir = "sessions/output/nmap_parsed"

    -- Limpiar y crear directorio de salida
    os.execute("rm -rf " .. output_dir)
    os.execute("mkdir -p " .. output_dir)

    -- Listar archivos XML en sessions
    local find_cmd = "find " .. session_dir .. " -type f -name \"*.xml\" > /tmp/xml_files.txt"
    os.execute(find_cmd)

    local file = io.open("/tmp/xml_files.txt", "r")
    if not file then
        return "Error: No se pudieron listar los archivos XML."
    end

    local xml_files = {}
    for line in file:lines() do
        table.insert(xml_files, line)
    end
    file:close()

    if #xml_files == 0 then
        return "No se encontraron archivos .xml en la carpeta 'sessions'."
    end

    -- Procesar cada archivo XML con xmlstarlet
    for _, xml_file in ipairs(xml_files) do
        local base_name = string.match(xml_file, "([^/]+)%.xml$") or "scan"
        local out_path = output_dir .. "/" .. base_name

        -- Crear carpeta por archivo si no existe
        os.execute("mkdir -p " .. out_path)

        -- Extraer IPs activas
        os.execute(string.format([[xmlstarlet sel -t -v "//address/@addr" -n %s | sort -u > %s/ips.txt]], xml_file, out_path))

        -- Extraer puertos abiertos
        os.execute(string.format([[
            xmlstarlet sel -t -m "//port[state/@state='open']" \
                -v "concat(../../address/@addr, ',', @portid, ',', @protocol)" -n %s \
                | sort -u > %s/open_ports.csv
        ]], xml_file, out_path))

        -- Extraer servidores HTTP/HTTPS (puertos 80, 443, 8080, etc.)
        os.execute(string.format([[
            xmlstarlet sel -t -m "//port[state/@state='open'][@portid=80 or @portid=443 or @portid=8080 or @portid=8443]" \
                -v "concat('http://', ../../address/@addr, ':', @portid)" -n %s \
                > %s/http_servers.txt
        ]], xml_file, out_path))
    end

    os.execute("rm -f /tmp/xml_files.txt")

    return string.format(
        "Procesados %d archivos NMAP con xmlstarlet.\nResultados guardados en: %s",
        #xml_files,
        output_dir
    )
end

register_command("parse_nmap_with_xmlstarlet", parse_nmap_with_xmlstarlet)