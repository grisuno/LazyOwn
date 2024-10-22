#!/bin/bash

# Constantes
readonly CHANGELOG_FILE="CHANGELOG.md"
readonly README_FILE="README.md"
readonly UTILS_FILE="UTILS.md"
readonly COMMANDS_FILE="COMMANDS.md"
readonly INDEX_FILE="docs/index.html"
readonly README_FILE_HTML="docs/README.html"

# Función para incrementar la versión
increment_version() {
    local version=$1
    local increment_type=${2:-"patch"}  # default to patch
    local major minor patch

    IFS='.' read -r major minor patch <<< "$version"
    case $increment_type in
        major) ((major++)); minor=0; patch=0 ;;
        minor) ((minor++)); patch=0 ;;
        patch) ((patch++)) ;;
        *) echo "Invalid increment type: $increment_type" >&2; return 1 ;;
    esac
    echo "$major.$minor.$patch"
}

# Obtener la versión actual
CURRENT_VERSION=$(git -C . describe --tags --abbrev=0 2>/dev/null || echo "0.2.0")

# Ejecutar pruebas si no se pasa el parámetro --no-test
if [[ "$1" != "--no-test" ]]; then
    python3 testmeneitor.py lazyown
fi

# Eliminar archivos que comiencen con d2
rm d2*

# Actualizar la documentación
python3 readmeneitor.py lazyown
python3 readmeneitor.py utils.py

# Función para actualizar una sección específica en un archivo Markdown
update_section_md() {
    local start_comment="$1"
    local end_comment="$2"
    local content_file="$3"
    sed -i "/$start_comment/,/$end_comment/{
        /$start_comment/!{/$end_comment/!d}
        /$start_comment/r $content_file
    }" "$README_FILE"
}

# Actualizar las secciones del README.md
update_section_md "<!-- START UTILS -->" "<!-- END UTILS -->" "$UTILS_FILE"
update_section_md "<!-- START COMMANDS -->" "<!-- END COMMANDS -->" "$COMMANDS_FILE"
update_section_md "<!-- START CHANGELOG -->" "<!-- END CHANGELOG -->" "$CHANGELOG_FILE"

echo "[*] El archivo $README_FILE ha sido actualizado con el contenido de UTILS.md, COMMANDS.md, y CHANGELOG.md."

# Crear el README en HTML
pandoc "$README_FILE" -f markdown -t html -s -o README.html --metadata title="README LazyOwn Framework Pentesting t00lz"
mv README.html docs/README.html

# Crear una copia de seguridad del archivo index.html
cp "$INDEX_FILE" "$INDEX_FILE.bak"

# Función para actualizar una sección específica en un archivo HTML
update_section_html() {
    local start_comment="$1"
    local end_comment="$2"
    local content_file="$3"
    sed -i "/$start_comment/,/$end_comment/{
        /$start_comment/!{/$end_comment/!d}
        /$start_comment/r $content_file
    }" "$INDEX_FILE"
}

# Actualizar las secciones del index.html
update_section_html "<!-- START README -->" "<!-- END README -->" "$README_FILE_HTML"
echo "[*] El archivo $INDEX_FILE ha sido actualizado con el contenido de README.html"

# Opciones de tipo de commit
echo -e "[?] Selecciona el tipo de commit:\n1) feat\n2) feature\n3) fix\n4) hotfix\n5) refactor\n6) docs\n7) test\n8) release\n9) patch"
read -r -p "Introduce el número del tipo de commit: " TYPE_OPTION

# Mapeo de opciones a los tipos de commit
case $TYPE_OPTION in
    "1") TYPE="feat" ;;
    "2") TYPE="feature" ;;
    "3") TYPE="fix" ;;
    "4") TYPE="hotfix" ;;
    "5") TYPE="refactor" ;;
    "6") TYPE="docs" ;;
    "7") TYPE="test" ;;
    "8") TYPE="release" ;;
    "9") TYPE="patch" ;;
    *) echo "Opción no válida"; exit 1 ;;
esac

# Solicitar información del commit al usuario
read -r -p "Introduce el tipo del commit (type): " TYPEDESC
read -r -p "Introduce el mensaje del commit (subject): " SUBJECT
read -r -p "Introduce el cuerpo del commit (body): " BODY

# Definir el footer fijo
FOOTER=" LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n"

# Determinar el incremento de versión basado en el tipo de commit
case $TYPE in
    feat|feature|fix|hotfix) NEW_VERSION=$(increment_version "$CURRENT_VERSION" "patch") ;;
    refactor|docs|test) NEW_VERSION="$CURRENT_VERSION" ;;
    release) NEW_VERSION=$(increment_version "$CURRENT_VERSION" "major") ;;
    patch) NEW_VERSION=$(increment_version "$CURRENT_VERSION" "minor") ;;
    *) echo "Invalid commit type: $TYPE" >&2; exit 1 ;;
esac

# Guardar la nueva versión en un archivo JSON
echo "{\"version\": \"$NEW_VERSION\"}" > version.json
git -C . add version.json

# Obtener el último tag y el commit actual
START_COMMIT=$(git -C . describe --tags --abbrev=0)
END_COMMIT=$(git -C . rev-parse HEAD)

# Capturar archivos modificados, eliminados y creados
MODIFIED_FILES=$(git diff --name-only "$START_COMMIT" "$END_COMMIT" | sed 's/^/- /')
DELETED_FILES=$(git diff --name-only --diff-filter=D "$START_COMMIT" "$END_COMMIT" | sed 's/^/- /')
CREATED_FILES=$(git diff --name-only --diff-filter=A "$START_COMMIT" "$END_COMMIT" | sed 's/^/- /')

# Crear LISTFILES incluyendo solo las secciones no vacías
LISTFILES=""
[ -n "$MODIFIED_FILES" ] && LISTFILES+="Modified file(s):\n$MODIFIED_FILES\n"
[ -n "$DELETED_FILES" ] && LISTFILES+="Deleted file(s):\n$DELETED_FILES\n"
[ -n "$CREATED_FILES" ] && LISTFILES+="Created file(s):\n$CREATED_FILES\n"

# Formatear el mensaje del commit
COMMIT_MESSAGE="${TYPE}(${TYPEDESC}): ${SUBJECT} \n\n Version: ${NEW_VERSION} \n\n ${BODY} \n\n ${LISTFILES} ${FOOTER} \n\n Fecha: $(git log -1 --format=%ad) \n\n Hora: $(git log -1 --format=%at)"

# Crear o limpiar el archivo de changelog
echo "# Changelog" > $CHANGELOG_FILE
echo "" >> $CHANGELOG_FILE
git -C . log --format="%s" "$START_COMMIT..$END_COMMIT" >> $CHANGELOG_FILE
echo "[*] Changelog generado en $CHANGELOG_FILE"

# Añadir todos los cambios y realizar el commit
git -C . add .
git -C . commit -S -a -m "$COMMIT_MESSAGE"

# Función para obtener el tipo de cambio basado en el mensaje del commit
get_commit_type() {
    local message=$1
    case $message in
        feat\(*) echo "### Nuevas características" ;;
        fix\(*) echo "### Correcciones" ;;
        hotfix\(*) echo "### Correcciones urgentes" ;;
        refactor\(*) echo "### Refactorización" ;;
        docs\(*) echo "### Documentación" ;;
        test\(*) echo "### Pruebas" ;;
        release\(*) echo "### Nuevo Release" ;;
        patch\(*) echo "### Nuevo parche" ;;
        *) echo "### Otros" ;;
    esac
}

# Crear o limpiar el archivo de changelog
echo "# Changelog" > $CHANGELOG_FILE
echo "" >> $CHANGELOG_FILE

# Obtener todos los commits desde el inicio en orden inverso
git log --pretty=format:"%s" | while read -r commit_message; do
    commit_type=$(get_commit_type "$commit_message")
    echo "$commit_type" >> $CHANGELOG_FILE
    echo "  * $commit_message" >> $CHANGELOG_FILE
    echo "" >> $CHANGELOG_FILE
done

echo "[+] Changelog generado y formateado en $CHANGELOG_FILE"

# Formatear el changelog
awk -F: '{
    if ($1 ~ /^#/) {
        print "\n" $0 "\n"
    } else {
        split($0, a, "\n\n")
        for (i in a) {
            if (a[i] ~ /^feat\(/) {
                print "### Nuevas características\n"
                print "  * " a[i] "\n"
            } else if (a[i] ~ /^feature\(/) {
                print "### Nuevas características\n"
                print "  * " a[i] "\n"
            } else if (a[i] ~ /^release\(/) {
                print "### Nuevo Release\n"
                print "  * " a[i] "\n"
            } else if (a[i] ~ /^fix\(/) {
                print "### Correcciones\n"
                print "  * " a[i] "\n"
            } else if (a[i] ~ /^hotfix\(/) {
                print "### Correcciones urgentes\n"
                print "  * " a[i] "\n"
            } else if (a[i] ~ /^patch\(/) {
                print "### Nuevo parche\n"
                print "  * " a[i] "\n"
            } else if (a[i] ~ /^refactor\(/) {
                print "### Refactorización\n"
                print "  * " a[i] "\n"
            } else if (a[i] ~ /^docs\(/) {
                print "### Documentación\n"
                print "  * " a[i] "\n"
            } else if (a[i] ~ /^test\(/) {
                print "### Pruebas\n"
                print "  * " a[i] "\n"
            } else {
                print "### Otros\n"
                print "  * " a[i] "\n"
            }
        }
    }
}' "$CHANGELOG_FILE" > changelog_temp.txt
mv changelog_temp.txt "$CHANGELOG_FILE"

echo "[+] Changelog generado y formateado en $CHANGELOG_FILE"

echo "[@] Committing new release"
# Crear un nuevo tag con la nueva versión
git -C . tag -a "v${NEW_VERSION}" -m "Release version ${NEW_VERSION}"
echo "[+] Nueva versión: v${NEW_VERSION}"
git -C . push --follow-tags
