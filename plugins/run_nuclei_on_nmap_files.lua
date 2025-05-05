function run_nuclei_on_nmap_files()
    local session_dir = "sessions"
    local template_dir = "../nuclei-templates"
    local tmp_file = "/tmp/nuclei_targets.txt"
    local out_file = "/tmp/nuclei_output.txt"

    -- Limpiar archivos temporales si existen
    os.execute("rm -f " .. tmp_file)
    os.execute("rm -f " .. out_file)

    -- 1. Listar archivos XML en la carpeta sessions
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

    -- 2. Extraer direcciones IP de cada archivo XML
    for _, xml_file in ipairs(xml_files) do
        local cmd_extract = string.format("xq '.nmaprun.host[].address.\"@addr\"' %s >> %s", xml_file, tmp_file)
        os.execute(cmd_extract)
    end

    -- 3. Eliminar duplicados
    os.execute(string.format("sort -u %s -o %s", tmp_file, tmp_file))

    -- 4. Ejecutar nuclei con las IPs obtenidas
    local nuclei_cmd = string.format("xargs -I {} nuclei -u {} -t %s > %s < %s",
                                     template_dir, out_file, tmp_file)
    os.execute(nuclei_cmd)

    -- 5. Leer salida del archivo temporal
    local out_handle = io.open(out_file, "r")
    if not out_handle then
        return "Núcleo ejecutado, pero no se generó salida o hubo un error."
    end

    local output = out_handle:read("*a")
    out_handle:close()

    -- 6. Limpiar archivos temporales
    os.execute("rm -f /tmp/xml_files.txt")
    os.execute("rm -f " .. tmp_file)
    os.execute("rm -f " .. out_file)

    if not output or #output == 0 then
        return "Ningún resultado encontrado o no hay direcciones válidas."
    end

    return "Resultados de escaneo con nuclei:\n\n" .. output
end

register_command("run_nuclei_on_nmap_files", run_nuclei_on_nmap_files)