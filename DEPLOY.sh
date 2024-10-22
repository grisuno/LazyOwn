#!/bin/bash

# Constantes
readonly CHANGELOG_FILE="CHANGELOG.md"
readonly README_FILE="README.md"
# Definir los archivos Markdown

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

#TEST ME NEITOR
# Revisa si el parámetro --no-test está presente
if [[ "$1" != "--no-test" ]]; then
    # Ejecuta el comando si --no-test no está presente
    python3 testmeneitor.py lazyown
fi

# Ejecuta el comando para eliminar archivos que comiencen con d2
rm d2*

# Actualiza la documentación
python3 readmeneitor.py lazyown
python3 readmeneitor.py utils.py

# Actualiza el README.md con los últimos cambios

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
# Este script actualiza el index.html de manera automatizada con los html generados por readmeneitor

# el html generado es horrible si... es horrible, pero es automatizado... TODO mejorar el html horrible 
# Definir los archivos HTML
INDEX_FILE="docs/index.html"
README_FILE_HTML="docs/README.html"

# Crear una copia de seguridad del archivo index.html
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
echo -e "[?] Selecciona el tipo de commit:\n1) feat\n2) feature\n3) fix\n4) hotfix\n5) refactor\n6) docs\n7) test\n8) release\n9) patch\n10) style\n11) chore"
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
  "10") TYPE="style" ;;
  "11") TYPE="chore" ;;
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
    feat|feature|fix|hotfix|style|chore)
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
MODIFIED_FILES=$(git diff --name-only $START_COMMIT $END_COMMIT | sed 's/^/- /')
# Capturar archivos eliminados
DELETED_FILES=$(git diff --name-only --diff-filter=D $START_COMMIT $END_COMMIT | sed 's/^/- /')
# Capturar archivos creados
CREATED_FILES=$(git diff --name-only --diff-filter=A $START_COMMIT $END_COMMIT | sed 's/^/- /')

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

# Obtener el último tag y el commit actual
START_COMMIT=$(git -C . describe --tags --abbrev=0)
END_COMMIT=$(git -C . rev-parse HEAD)

# Crear o limpiar el archivo de changelog
echo "# Changelog" > $CHANGELOG_FILE
echo "" >> $CHANGELOG_FILE

# Agregar los cambios al changelog
git -C . log --format="%s" $START_COMMIT..$END_COMMIT >> $CHANGELOG_FILE

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
  elif [[ $message =~ ^style\(.*\) ]]; then
    echo "### Estilo"
  elif [[ $message =~ ^chore\(.*\) ]]; then
    echo "### Tareas"
  else
    echo "### Otros"
  fi
}

# Obtener los mensajes de commit desde el último tag
commits=$(git log $(git describe --tags --abbrev=0 @^)..@ --format="%s")

# Crear un nuevo changelog vacío
new_changelog=""

# Iterar sobre los commits y agregar al changelog
while IFS= read -r commit; do
  type=$(get_commit_type "$commit")
  new_changelog+="$type\n- $commit\n"
done <<< "$commits"

# Actualizar el archivo CHANGELOG.md
echo -e "$new_changelog" >> CHANGELOG.md

# Mostrar un mensaje indicando que el changelog se ha actualizado
echo "[*] El changelog se ha actualizado en $CHANGELOG_FILE"

# Realiza el tag y el push con la nueva versión
git tag "$NEW_VERSION"
git push origin --tags
git push

# Haz el build del paquete y publícalo en PyPI
python3 -m build
twine upload dist/*

# Mostrar un mensaje indicando que el proceso ha finalizado
echo "[*] Proceso completado con éxito. Versión $NEW_VERSION publicada en PyPI."

# Salida exitosa
exit 0
