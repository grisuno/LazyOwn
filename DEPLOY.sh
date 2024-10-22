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

determine_increment_type() {
    if git log -1 --pretty=%B | grep -q '^feat'; then
        echo "minor"
    elif git log -1 --pretty=%B | grep -q '^fix'; then
        echo "patch"
    else
        echo "none"
    fi
}

# Obtener la versión actual
CURRENT_VERSION=$(git -C . describe --tags --abbrev=0 2>/dev/null || echo "0.2.0")

# Revisa si el parámetro --no-test está presente
if [[ "$1" != "--no-test" ]]; then
    python3 testmeneitor.py lazyown
fi

# Ejecuta el comando para eliminar archivos que comiencen con d2
rm d2*

# Actualiza la documentación
python3 readmeneitor.py lazyown
python3 readmeneitor.py utils.py

# Función para actualizar una sección específica
update_section_md() {
    local start_comment="$1"
    local end_comment="$2"
    local content_file="$3"
    
    sed -i "/$start_comment/,/$end_comment/{
        /$start_comment/!{/$end_comment/!d}
        /$start_comment/r $content_file
    }" "$README_FILE"
}

# Actualizar cada sección
update_section_md "<!-- START UTILS -->" "<!-- END UTILS -->" "$UTILS_FILE"
update_section_md "<!-- START COMMANDS -->" "<!-- END COMMANDS -->" "$COMMANDS_FILE"
update_section_md "<!-- START CHANGELOG -->" "<!-- END CHANGELOG -->" "$CHANGELOG_FILE"

echo "[*] El archivo $README_FILE ha sido actualizado con el contenido de UTILS.md, COMMANDS.md, y CHANGELOG.md."

# Crea el readme en html
pandoc $README_FILE -f markdown -t html -s -o README.html --metadata title="README LazyOwn Framework Pentesting t00lz"
mv README.html docs/README.html

# Crear una copia de seguridad del archivo index.html
INDEX_FILE="docs/index.html"
README_FILE_HTML="docs/README.html"
cp "$INDEX_FILE" "$INDEX_FILE.bak"

# Función para actualizar una sección específica
update_section_html() {
    local start_comment="$1"
    local end_comment="$2"
    local content_file="$3"
    
    sed -i "/$start_comment/,/$end_comment/{
        /$start_comment/!{/$end_comment/!d}
        /$start_comment/r $content_file
    }" "$INDEX_FILE"
}

# Actualizar cada sección
update_section_html "<!-- START README -->" "<!-- END README -->" "$README_FILE_HTML"
echo "[*] El archivo $INDEX_FILE ha sido actualizado con el contenido de README.html"

# Opciones de tipo de commit
echo -e "[?] Selecciona el tipo de commit:\n1) feat\n2) feature\n3) fix\n4) hotfix\n5) refactor\n6) docs\n7) test\n8) release \n9) patch"
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

# Solicitar el tipo del commit al usuario
read -r -p "Introduce el tipo del commit (type): " TYPEDESC

# Solicitar el mensaje del commit al usuario
read -r -p "Introduce el mensaje del commit (subject): " SUBJECT

# Solicitar el cuerpo del commit
read -r -p "Introduce el cuerpo del commit (body): " BODY

# Definir el footer fijo
FOOTER=" LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n"

# Determinar el incremento de versión basado en el tipo de commit
case $TYPE in
    feat|feature)
        # Incrementar el número menor
        NEW_VERSION=$(increment_version $CURRENT_VERSION "minor")
        ;;
    fix|hotfix)
        # Incrementar el número de parche
        NEW_VERSION=$(increment_version $CURRENT_VERSION "patch")
        ;;
    refactor|docs|test)
        # No cambiar la versión
        NEW_VERSION=$CURRENT_VERSION
        ;;
    release)
        # Incrementar el número mayor y reiniciar los números menor y parche a 0
        NEW_VERSION=$(increment_version $CURRENT_VERSION "major")
        ;;
    patch)
        # Incrementar el número menor
        NEW_VERSION=$(increment_version $CURRENT_VERSION "minor")
        ;;
    *)
        echo "Invalid commit type: $TYPE" >&2
        exit 1
        ;;
esac

echo "{\"version\": \"$NEW_VERSION\"}" > version.json
git -C . add version.json

# Capturar archivos modificados
MODIFIED_FILES=$(git diff --name-only HEAD^ HEAD | sed 's/^/- /')
# Capturar archivos eliminados
DELETED_FILES=$(git diff --name-only --diff-filter=D HEAD^ HEAD | sed 's/^/- /')
# Capturar archivos creados
CREATED_FILES=$(git diff --name-only --diff-filter=A HEAD^ HEAD | sed 's/^/- /')

# Crear LISTFILES incluyendo solo las secciones no vacías
LISTFILES=""
if [ -n "$MODIFIED_FILES" ]; then
    LISTFILES+="Modified file(s):\n$MODIFIED_FILES\n"
fi
if [ -n "$DELETED_FILES" ]; then
    LISTFILES+="Deleted file(s):\n$DELETED_FILES\n"
fi
if [ -n "$CREATED_FILES" ]; then
    LISTFILES+="Created file(s):\n$CREATED_FILES\n"
fi

# Usar LISTFILES en tu mensaje de commit
echo -e "$LISTFILES"

# Formatear el mensaje del commit
COMMIT_MESSAGE="${TYPE}(${TYPEDESC}): ${SUBJECT} \n\n Version: ${NEW_VERSION} \n\n ${BODY} \n\n ${LISTFILES} ${FOOTER} \n\n Fecha: $(git log -1 --format=%ad) \n\n Hora: $(git log -1 --format=%at)"

# Crear o limpiar el archivo de changelog
echo "# Changelog" > $CHANGELOG_FILE
echo "" >> $CHANGELOG_FILE

# Agregar los cambios al changelog
git -C . log --pretty=format:"%s" HEAD^..HEAD >> $CHANGELOG_FILE

# Mensaje indicando que el changelog se ha generado
echo "[*] Changelog generado en $CHANGELOG_FILE"

# Añadir todos los cambios
git -C . add .

# Realizar el commit con el mensaje proporcionado
git -C . commit -S -a -m "$COMMIT_MESSAGE"

# Función para obtener el tipo de cambio basado en el mensaje del commit
get_commit_type() {
    local message=$1
    if [[ $message =~ ^feat\(.*\) ]]; then
        echo "### Nuevas características"
    elif [[ $message =~ ^fix\(.*\) ]]; then
        echo "### Correcciones"
    elif [[ $message =~ ^hotfix\(.*\) ]]; then
        echo "### Correcciones urgentes"
    elif [[ $message =~ ^refactor\(.*\) ]]; then
        echo "### Refactorización"
    elif [[ $message =~ ^docs\(.*\) ]]; then
        echo "### Documentación"
    elif [[ $message =~ ^test\(.*\) ]]; then
        echo "### Pruebas"
    elif [[ $message =~ ^release\(.*\) ]]; then
        echo "### Nuevo Release"
    elif [[ $message =~ ^patch\(.*\) ]]; then
        echo "### Nuevo parche"
    else
        echo "### Otros"
    fi
}

# Crear o limpiar el archivo de changelog
echo "# Changelog" > $CHANGELOG_FILE
echo "" >> $CHANGELOG_FILE

# Obtener todos los commits desde el inicio en orden inverso
git log --pretty=format:"* %s" > "$CHANGELOG_FILE"

# Mensaje indicando que el changelog se ha generado
echo "[*] Changelog generado en $CHANGELOG_FILE"

# Etiquetar el nuevo commit
git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"

# Publicar cambios en el repositorio remoto
git push origin master
git push origin "v$NEW_VERSION"

echo "[*] Se ha realizado un nuevo commit y se ha etiquetado la versión $NEW_VERSION."
