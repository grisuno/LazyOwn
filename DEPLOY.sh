#!/bin/bash
set -euo pipefail

# Constantes
readonly CHANGELOG_FILE="CHANGELOG.md"
readonly README_FILE="README.md"
readonly UTILS_FILE="UTILS.md"
readonly COMMANDS_FILE="COMMANDS.md"

# Detectar si GPG signing esta disponible
GPG_SIGN=""
if git config --get user.signingkey >/dev/null 2>&1 && gpg --list-secret-keys "$(git config --get user.signingkey)" >/dev/null 2>&1; then
    GPG_SIGN="-S"
    echo "[*] GPG signing habilitado."
else
    echo "[!] GPG signing no disponible (sin user.signingkey o clave secreta). Commits/tags se crearan sin firma."
fi

increment_version() {
    local version=$1
    local major minor patch
    IFS='.' read -r major minor patch <<< "$version"

    local increment_type=${2:-"patch"}

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
CURRENT_VERSION=$(git -C . describe --tags --abbrev=0 2>/dev/null || echo "release/0.2.0")

# Obtener commits de referencia ANTES de usarlos
START_COMMIT=$(git -C . describe --tags --abbrev=0)
END_COMMIT=$(git -C . rev-parse HEAD)

#TEST ME NEITOR
if [[ "${1:-}" != "--no-test" ]]; then
    python3 testmeneitor.py lazyown.py
fi

# Ejecuta el comando para eliminar archivos que comiencen con d2 (ignora error si no hay coincidencias)
rm -f d2* || true

# Actualiza la documentación
python3 readmeneitor.py lazyown.py
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
pandoc "$README_FILE" -f markdown -t html -s -o README.html --metadata title="README LazyOwn Framework Pentesting t00lz"
mv README.html docs/README.html

# Este script actualiza el index.html de manera automatizada con los html generados por readmeneitor
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

# Solicitar datos del commit
read -r -p "Introduce el tipo del commit (type): " TYPEDESC
read -r -p "Introduce el mensaje del commit (subject): " SUBJECT
read -r -p "Introduce el cuerpo del commit (body): " BODY

# Definir el footer fijo
FOOTER=" LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n"

# Determinar el incremento de versión basado en el tipo de commit
case $TYPE in
    feat|feature|fix|hotfix)
        NEW_VERSION=$(increment_version "$CURRENT_VERSION" "patch")
        ;;
    refactor|docs|test|style|shore)
        NEW_VERSION=$CURRENT_VERSION
        ;;
    release)
        NEW_VERSION=$(increment_version "$CURRENT_VERSION" "major")
        ;;
    patch)
        NEW_VERSION=$(increment_version "$CURRENT_VERSION" "minor")
        ;;
    *)
        echo "Invalid commit type: $TYPE" >&2
        exit 1
        ;;
esac

echo "{\"version\": \"$NEW_VERSION\"}" > version.json
git -C . add version.json

# Capturar archivos modificados/eliminados/creados
MODIFIED_FILES=$(git diff --name-only "$START_COMMIT" "$END_COMMIT" | sed 's/^/- /' || true)
DELETED_FILES=$(git diff --name-only --diff-filter=D "$START_COMMIT" "$END_COMMIT" | sed 's/^/- /' || true)
CREATED_FILES=$(git diff --name-only --diff-filter=A "$START_COMMIT" "$END_COMMIT" | sed 's/^/- /' || true)

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

echo -e "$LISTFILES"

# Formatear el mensaje del commit
COMMIT_MESSAGE="${TYPE}(${TYPEDESC}): ${SUBJECT} \n\n Version: ${NEW_VERSION} \n\n ${BODY} \n\n ${LISTFILES} ${FOOTER} \n\n Fecha: $(date) \n\n Hora: $(date +%s)"

# Crear o limpiar el archivo de changelog
echo "# Changelog" > "$CHANGELOG_FILE"
echo "" >> "$CHANGELOG_FILE"

# Agregar los cambios al changelog
git -C . log --format="%s" "$START_COMMIT".."$END_COMMIT" >> "$CHANGELOG_FILE" || true

echo "[*] Changelog generado en $CHANGELOG_FILE"

# Añadir todos los cambios
git -C . add .

# Realizar el commit (con o sin firma GPG)
# shellcheck disable=SC2086
git -C . commit $GPG_SIGN -a -m "$COMMIT_MESSAGE"

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
echo "# Changelog" > "$CHANGELOG_FILE"
echo "" >> "$CHANGELOG_FILE"

# Obtener todos los commits desde el inicio en orden inverso
git log --pretty=format:"%s" | while read -r commit_message; do
  commit_type=$(get_commit_type "$commit_message")
  echo "$commit_type" >> "$CHANGELOG_FILE"
  echo "  * $commit_message" >> "$CHANGELOG_FILE"
  echo "" >> "$CHANGELOG_FILE"
done

echo "[+] Changelog generado y formateado en $CHANGELOG_FILE"

# Formatear el CHANGELOG usando sponge
echo "[+] Formateando el CHANGELOG"
awk -F: '{
  if ($1 ~ /^#/) {
    print "\n" $0 "\n"
  } else {
    split($0, a, "\n\n")
    for (i in a) {
      if (a[i] ~ /^feat\(/) {
        print "### Nuevo grupo de características\n"
        print "  * " a[i] "\n"
      } else if (a[i] ~ /^feature\(/) {
        print "### Nuevas características\n"
        print "  * " a[i] "\n"
      } else if (a[i] ~ /^release\(/) {
        print "### Nuevo Release\n"
        print "  * " a[i] "\n"
      } else if (a[i] ~ /^patch\(/) {
        print "### Nuevo parche\n"
        print "  * " a[i] "\n"
      } else if (a[i] ~ /^fix\(/) {
        print "### Correcciones\n"
        print "  * " a[i] "\n"
      } else if (a[i] ~ /^hotfix\(/) {
        print "### Correcciones urgentes\n"
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
}' "$CHANGELOG_FILE" | sponge "$CHANGELOG_FILE"

# Añadir el archivo de changelog al commit
git -C . add "$CHANGELOG_FILE"

# Convertir el changelog a HTML
pandoc "$CHANGELOG_FILE" -f markdown -t html -s -o CHANGELOG.html --metadata title="CHANGELOG LazyOwn Framework RedTeaming t00lz"
mv CHANGELOG.html docs/CHANGELOG.html
git -C . add docs/CHANGELOG.html

# Modificar el commit actual para incluir el changelog
# shellcheck disable=SC2086
git -C . commit $GPG_SIGN --amend --no-edit

# Crear un nuevo tag con la nueva versión
# Si el tag ya existe localmente, eliminarlo primero para evitar conflictos
FINAL_VERSION="$NEW_VERSION"
while git -C . rev-parse "$FINAL_VERSION" >/dev/null 2>&1; do
    echo "[!] Tag '$FINAL_VERSION' ya existe localmente — eliminando tag local huérfano..."
    git -C . tag -d "$FINAL_VERSION" || true
    echo "[*] Reintentando con parche incrementado..."
    FINAL_VERSION=$(increment_version "$FINAL_VERSION" "patch")
done

if [ "$FINAL_VERSION" != "$NEW_VERSION" ]; then
    echo "[*] Versión final ajustada: $FINAL_VERSION"
    NEW_VERSION="$FINAL_VERSION"
    echo "{\"version\": \"$NEW_VERSION\"}" > version.json
    git -C . add version.json
    # shellcheck disable=SC2086
    git -C . commit $GPG_SIGN --amend --no-edit
fi

# Crear el tag (con o sin firma GPG)
# shellcheck disable=SC2086
git -C . tag $GPG_SIGN "$NEW_VERSION" -m "Version $NEW_VERSION"

# Push al remoto (con tags)
git -C . push origin main --follow-tags

# Crear release en GitHub usando gh CLI
if command -v gh >/dev/null 2>&1; then
    echo "[*] Creando release en GitHub con gh..."

    # GitHub API limita el body de release a 125000 caracteres
    # Si el changelog es muy largo, truncarlo para la release
    MAX_RELEASE_CHARS=120000
    RELEASE_NOTES_FILE="$CHANGELOG_FILE"
    if [ "$(wc -c < "$CHANGELOG_FILE")" -gt "$MAX_RELEASE_CHARS" ]; then
        RELEASE_NOTES_FILE="/tmp/lazyown_release_notes_$$.md"
        head -c "$MAX_RELEASE_CHARS" "$CHANGELOG_FILE" > "$RELEASE_NOTES_FILE"
        echo -e "\n\n... *(Notas truncadas por limite de GitHub. Ver CHANGELOG.md completo en el repo)*" >> "$RELEASE_NOTES_FILE"
        echo "[!] CHANGELOG.md excede limite de GitHub (${MAX_RELEASE_CHARS} chars) — se trunco para la release."
    fi

    gh release create "$NEW_VERSION" \
        --title "LazyOwn $NEW_VERSION" \
        --notes-file "$RELEASE_NOTES_FILE" \
        --target main || echo "[!] No se pudo crear la release con gh. ¿Estas autenticado? (gh auth status)"

    # Limpiar temp si se creo
    if [ "${RELEASE_NOTES_FILE:-}" != "$CHANGELOG_FILE" ] && [ -f "${RELEASE_NOTES_FILE:-}" ]; then
        rm -f "$RELEASE_NOTES_FILE"
    fi
else
    echo "[!] gh CLI no encontrado. Sube la release manualmente o instala gh."
fi

echo "[*] Cambios enviados al repositorio remoto con la nueva versión $NEW_VERSION."
# TODO: DELETE ALL SPAGETTI CODE
