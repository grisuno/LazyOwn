-- init_plugins.lua

local plugin_dir = "plugins/"  -- Directorio donde están los plugins

-- Función para cargar un plugin individual
local function load_plugin(filename)
    local filepath = plugin_dir .. filename
    local f, err = loadfile(filepath)
    if not f then
        print("Error al cargar el plugin '" .. filename .. "': " .. tostring(err))
        return
    end

    -- Ejecuta el plugin
    local success, result = pcall(f)
    if not success then
        print("Error al ejecutar el plugin '" .. filename .. "': " .. tostring(result))
    else
        print("Plugin '" .. filename .. "' cargado correctamente.")
    end
end

-- Obtener la lista de archivos usando la función de Python
local files = list_files_in_directory(plugin_dir)

-- Verificar si la lista de archivos está vacía
if type(files) ~= "table" or #files == 0 then
    print("    [!] No new pluggins found '" .. plugin_dir .. "'.")
    return
end

-- Iterar sobre los archivos y cargar los plugins
for _, filename in ipairs(files) do
    if filename:match("%.lua$") and filename ~= "init_plugins.lua" then
        load_plugin(filename)
    end
end