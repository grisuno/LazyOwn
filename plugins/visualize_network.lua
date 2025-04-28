function visualize_network()
    local input_file = "network_discovery" -- Hardcodeado para esta prueba
    local output_file = "sessions/network_visualization.html"

    if not input_file then
        return "Error: Debe especificar el archivo de entrada con la lista de IPs (ej: file=ips.txt)."
    end

    local nodos_array_lua = {}
    local error_message = nil
    local line_number = 0

    local file = io.open(input_file, "r")
    if not file then
        error_message = "Error: No se pudo abrir el archivo: " .. input_file
    else
        while true do
            local line = file:read("*l") -- Leer una línea completa
            line_number = line_number + 1
            print("[DEBUG] Línea:", line_number, "| Valor de 'line':", line) -- DEBUG
            if not line then
                print("[DEBUG] Fin del archivo o error de lectura.") -- DEBUG
                break -- Salir del bucle si no se puede leer más
            end
            print("[DEBUG] Línea:", line_number, "| Tipo de 'line':", type(line)) -- DEBUG
            if type(line) == 'string' then
                print("[DEBUG] Línea:", line_number, "| Longitud de 'line':", #line) -- DEBUG
                print("[DEBUG] Línea:", line_number, "| Contenido 'raw':", string.byte(line, 1, #line)) -- DEBUG
                local trimmed_line = line:gsub("^%s*(.-)%s*$", "%1") -- Usando la solución de Lua para trim
                print("[DEBUG] Línea:", line_number, "| IP después de trim:", trimmed_line) -- DEBUG

                if trimmed_line:match("%S") then
                    print("[DEBUG] Línea:", line_number, "| Contiene no-espacio (después de trim).") -- DEBUG
                    -- Usar la línea recortada
                    -- Construir el objeto Lua para la visualización
                    table.insert(nodos_array_lua, {id = trimmed_line, label = trimmed_line, title = 'Host: ' .. trimmed_line})
                else
                    print("[DEBUG] Línea:", line_number, "| Solo espacios o vacía (después de trim).") -- DEBUG
                end
            else
                print("[DEBUG] Línea:", line_number, "| NO es string:", line) -- DEBUG
            end
        end
        file:close()
    end

    if error_message then
        return error_message
    end

    -- --- PARTE DONDE SE GENERA EL JSON MANUALMENTE ---
    local nodos_json_parts = {}
    for i, nodo in ipairs(nodos_array_lua) do

        local nodo_json = '{ "id": "' .. nodo.id .. '", "label": "' .. nodo.label .. '", "title": "' .. nodo.title .. '" }'
        table.insert(nodos_json_parts, nodo_json)
    end

    -- Unimos todas las strings de nodos con una coma y las envolvemos en corchetes para hacer el array JSON
    local nodos_json = "[ " .. table.concat(nodos_json_parts, ", ") .. " ]"
    -- --- FIN DE LA GENERACIÓN MANUAL ---


    local html_content = [[
    <!DOCTYPE html>
    <html>
    <head>
        <title>Network Hosts</title>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style type="text/css">
            #mynetwork {
                width: 100%;
                height: 600px;
                border: 1px solid lightgray;
            }
        </style>
    </head>
    <body>
        <div id="mynetwork"></div>
        <script type="text/javascript">
            // Datos de nodos
            // vis.DataSet puede parsear la cadena JSON directamente
            var nodes = new vis.DataSet(]] .. nodos_json .. [[);

            // No hay aristas en este caso
            var edges = new vis.DataSet([]);

            // Opciones de layout para evitar superposición
            var options = {
                layout: {
                    improvedLayout: true
                },
                physics: {
                    stabilization: {
                        iterations: 1000
                    }
                }
            };

            // Contenedor
            var container = document.getElementById('mynetwork');

            // Datos para el grafo
            var data = {
                nodes: nodes,
                edges: edges
            };

            // Crear el grafo
            var network = new vis.Network(container, data, options);
        </script>
    </body>
    </html>
    ]]

    local output_path = output_file
    local outfile = io.open(output_path, "w")
    if not outfile then
        return "Error: No se pudo crear el archivo de salida: " .. output_path
    end

    outfile:write(html_content)
    outfile:close()

    return "Visualización de hosts guardada en: " .. output_path
end

register_command("visualize_network", visualize_network)