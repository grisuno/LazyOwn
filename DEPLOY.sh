#!/bin/bash

# Constantes
readonly CHANGELOG_FILE="CHANGELOG.md"
readonly README_FILE="README.md"
UTILS_FILE="UTILS.md"
COMMANDS_FILE="COMMANDS.md"

increment_version() {
    local version=$1
    local major minor patch
    IFS='.' read -r major minor patch <<< "$version"

    local increment_type=${2:-"patch"}  # default to patch

    case $increment_type in
        major)
            ((major++))
            minor=0
            patch=0
            ;;
        minor)
            ((minor++))
            patch=0
            ;;
        patch)
            ((patch++))
            ;;
        *)
            echo "Invalid increment type: $increment_type" >&2
            return 1
            ;;
    esac

    echo "$major.$minor.$patch"
}

# Obtener la versión actual
CURRENT_VERSION=$(git -C . describe --tags --abbrev=0 2>/dev/null || echo "0.2.0")

# Verifica si el parámetro --no-test está presente
if [[ "$1" != "--no-test" ]]; then
    python3 testmeneitor.py lazyown
fi

# Actualiza la documentación
python3 readmeneitor.py lazyown
python3 readmeneitor.py utils.py

# Actualizar README.md
update_section_md() {
    local start_comment="$1"
    local end_comment="$2"
    local content_file="$3"
    
    sed -i "/$start_comment/,/$end_comment/{
        /$start_comment/!{/$end_comment/!d}
        /$start_comment/r $content_file
    }" "$README_FILE"
}

update_section_md "<!-- START UTILS -->" "<!-- END UTILS -->" "$UTILS_FILE"
update_section_md "<!-- START COMMANDS -->" "<!-- END COMMANDS -->" "$COMMANDS_FILE"
update_section_md "<!-- START CHANGELOG -->" "<!-- END CHANGELOG -->" "$CHANGELOG_FILE"

echo "[*] El archivo $README_FILE ha sido actualizado."

# Crea el README en HTML
pandoc $README_FILE -f markdown -t html -s -o README.html --metadata title="README LazyOwn Framework Pentesting t00lz"
mv README.html docs/README.html

# Actualiza el index.html
INDEX_FILE="docs/index.html"
README_FILE_HTML="docs/README.html"
cp "$INDEX_FILE" "$INDEX_FILE.bak"

update_section_html() {
    local start_comment="$1"
    local end_comment="$2"
    local content_file="$3"
    
    sed -i "/$start_comment/,/$end_comment/{
        /$start_comment/!{/$end_comment/!d}
        /$start_comment/r $content_file
    }" "$INDEX_FILE"
}

update_section_html "<!-- START README -->" "<!-- END README -->" "$README_FILE_HTML"
echo "[*] El archivo $INDEX_FILE ha sido actualizado."

# Opciones de tipo de commit
echo -e "[?] Selecciona el tipo de commit:\n1) feat\n2) fix\n3) docs\n4) refactor\n5) test\n6) release\n7) patch"
read -r -p "Introduce el número del tipo de commit: " TYPE_OPTION

# Mapeo de opciones a los tipos de commit
case $TYPE_OPTION in
  "1") TYPE="feat" ;;
  "2") TYPE="fix" ;;
  "3") TYPE="docs" ;;
  "4") TYPE="refactor" ;;
  "5") TYPE="test" ;;
  "6") TYPE="release" ;;
  "7") TYPE="patch" ;;
  *) echo "Opción no válida"; exit 1 ;;
esac

# Solicitar detalles del commit
read -r -p "Introduce el mensaje del commit (subject): " SUBJECT
read -r -p "Introduce el cuerpo del commit (body): " BODY

# Definir el footer fijo
FOOTER="LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429\nLazyOwn: https://grisuno.github.io/LazyOwn/\n"

# Determinar el incremento de versión basado en el tipo de commit
case $TYPE in
    feat|fix)
        NEW_VERSION=$(increment_version "$CURRENT_VERSION" "patch")
        ;;
    release)
        NEW_VERSION=$(increment_version "$CURRENT_VERSION" "major")
        ;;
    patch)
        NEW_VERSION=$(increment_version "$CURRENT_VERSION" "minor")
        ;;
    refactor|docs|test)
        NEW_VERSION=$CURRENT_VERSION
        ;;
    *)
        echo "Invalid commit type: $TYPE" >&2
        exit 1
        ;;
esac

echo "{\"version\": \"$NEW_VERSION\"}" > version.json
git add version.json

# Capturar archivos modificados
MODIFIED_FILES=$(git diff --name-only HEAD~1 | sed 's/^/- /')
LISTFILES=""
if [ -n "$MODIFIED_FILES" ]; then
    LISTFILES+="Modified file(s):\n$MODIFIED_FILES\n"
fi

# Formatear el mensaje del commit
COMMIT_MESSAGE="${TYPE}: ${SUBJECT}\n\nVersion: ${NEW_VERSION}\n\n${BODY}\n\n${LISTFILES}${FOOTER}\n\nFecha: $(date)\n"

# Realizar el commit con el mensaje proporcionado
git add .
git commit -m "$COMMIT_MESSAGE"

# Generar changelog
git log --pretty=format:"* %s" > "$CHANGELOG_FILE"
echo "[*] Changelog generado en $CHANGELOG_FILE"

# Crear un nuevo tag con la nueva versión
git tag -a "v$NEW_VERSION" -m "Version $NEW_VERSION"

# Hacer push al repositorio remoto, incluyendo los tags
git push origin main --follow-tags

echo "[*] Cambios enviados al repositorio remoto con la nueva versión $NEW_VERSION."
