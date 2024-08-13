#!/bin/bash

# Definir los archivos HTML
INDEX_FILE="docs/index.html"
README_FILE="README.html"
COMMANDS_FILE="docs/COMMANDS.html"
UTILS_FILE="docs/UTILS.html"

# Crear una copia de seguridad del archivo index.html
cp "$INDEX_FILE" "$INDEX_FILE.bak"

# Función para actualizar una sección específica
update_section() {
    local start_comment="$1"
    local end_comment="$2"
    local content_file="$3"
    
    sed -i "/$start_comment/,/$end_comment/{
        /$start_comment/!{/$end_comment/!d}
        /$start_comment/r $content_file
    }" "$INDEX_FILE"
}

# Actualizar cada sección
update_section "<!-- START README -->" "<!-- END README -->" "$README_FILE"
update_section "<!-- START COMMANDS -->" "<!-- END COMMANDS -->" "$COMMANDS_FILE"
update_section "<!-- START UTILS -->" "<!-- END UTILS -->" "$UTILS_FILE"

echo "El archivo $INDEX_FILE ha sido actualizado con el contenido de README.html, COMMANDS.html, y UTILS.html."