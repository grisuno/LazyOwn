#!/bin/bash

# Definir los archivos Markdown
README_FILE="README.md"
UTILS_FILE="UTILS.md"
COMMANDS_FILE="COMMANDS.md"
CHANGELOG_FILE="CHANGELOG.md"

# Función para actualizar una sección específica
update_section() {
    local start_comment="$1"
    local end_comment="$2"
    local content_file="$3"
    
    sed -i "/$start_comment/,/$end_comment/{
        /$start_comment/!{/$end_comment/!d}
        /$start_comment/r $content_file
    }" "$README_FILE"
}

# Actualizar cada sección
update_section "<!-- START UTILS -->" "<!-- END UTILS -->" "$UTILS_FILE"
update_section "<!-- START COMMANDS -->" "<!-- END COMMANDS -->" "$COMMANDS_FILE"
update_section "<!-- START CHANGELOG -->" "<!-- END CHANGELOG -->" "$CHANGELOG_FILE"

echo "[*] El archivo $README_FILE ha sido actualizado con el contenido de UTILS.md, COMMANDS.md, y CHANGELOG.md."