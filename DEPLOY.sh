#!/bin/bash

# Constantes
readonly CHANGELOG_FILE="CHANGELOG.md"
readonly README_FILE="README.md"

# Función para incrementar la versión
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
CURRENT_VERSION=$(git -C . describe --tags --abbrev=0 2>/dev/null || echo "0.0.0")

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

#Actualiza el README.md con los ultimos cambios
./dump_readme.sh

# Crea el readme en html
pandoc $README_FILE -s -o README.html
# Este script actualiza el index.html de manera automatizada con los html generados por readmeneitor

# el html generado es horrible si... es horrible, pero es automatizado... TODO mejorar el html horrible 
./index.sh

# Opciones de tipo de commit
echo -e "[?] Selecciona el tipo de commit:\n1) feat\n2) feature\n3) fix\n4) hotfix\n5) refactor\n6) docs\n7) test"
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
if [[ "$TYPE" == "feat" || "$TYPE" == "feature" ]]; then
    NEW_VERSION=$(increment_version $CURRENT_VERSION "minor")
elif [[ "$TYPE" == "fix" || "$TYPE" == "hotfix" ]]; then
    NEW_VERSION=$(increment_version $CURRENT_VERSION "patch")
else
    NEW_VERSION=$CURRENT_VERSION
fi

# Formatear el mensaje del commit
COMMIT_MESSAGE="${TYPE}(${TYPEDESC}): ${SUBJECT} \n\n Version: ${NEW_VERSION} \n\n ${BODY} \n\n ${FOOTER} \n\n Fecha: $(git log -1 --format=%ad) \n\n Hora: $(git log -1 --format=%at)"

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
git -C . commit -a -m "$COMMIT_MESSAGE"

# Generar el changelog después del commit
# Actualizar el archivo CHANGELOG.md
echo "# Changelog" > $CHANGELOG_FILE
echo "" >> $CHANGELOG_FILE
git -C . log --format="%s" $START_COMMIT..$END_COMMIT >> $CHANGELOG_FILE
echo "[+] Changelog actualizado en $CHANGELOG_FILE"

# formatear el change log
echo "[+] Formateando el change log"
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
}' $CHANGELOG_FILE | sponge $CHANGELOG_FILE

# Añadir el archivo de changelog al commit
git -C . add $CHANGELOG_FILE

# Convertir el changelog a HTML
pandoc $CHANGELOG_FILE -s -c docs/style.css -t docs/template.html -T "Changelog de LazyOwn" -A "Resumen del changelog" -o CHANGELOG.html
mv CHANGELOG.html docs/CHANGELOG.html
git -C . add docs/CHANGELOG.html

# Realizar el commit (modificar el commit actual para incluir el changelog)
git -C . commit --amend --no-edit

# Crear un nuevo tag con la nueva versión
git -C . tag -s $NEW_VERSION -m "Version $NEW_VERSION"

# Hacer push al repositorio remoto, incluyendo los tags
git -C . push --follow-tags

echo "[*] Cambios enviados al repositorio remoto con la nueva versión $NEW_VERSION."