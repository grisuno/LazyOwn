#!/bin/bash

# Actualiza la documentación
python3 readmeneitor.py lazyown
python3 readmeneitor.py utils.py

# Crea el readme en html
pandoc README.md -f markdown -t html -s -o README.html
# Este script actualiza el index.html de manera automatizada con los html generados por readmeneitor
# el html generado es horrible si... es horrible, pero es automatizado... TODO mejorar el html horrible 
./index.sh
# Nombre del archivo de changelog
CHANGELOG_FILE="CHANGELOG.md"

# Opciones de tipo de commit
echo "Selecciona el tipo de commit:"
echo "1) feat"
echo "2) feature"
echo "3) fix"
echo "4) hotfix"
echo "5) refactor"
echo "6) docs"
echo "7) test"
read -p "Introduce el número del tipo de commit: " TYPE_OPTION

# Mapeo de opciones a los tipos de commit
case $TYPE_OPTION in
  1) TYPE="feat" ;;
  2) TYPE="feature" ;;
  3) TYPE="fix" ;;
  4) TYPE="hotfix" ;;
  5) TYPE="refactor" ;;
  6) TYPE="docs" ;;
  7) TYPE="test" ;;
  *) echo "Opción no válida"; exit 1 ;;
esac

# Solicitar el tipo del commit al usuario
read -p "Introduce el tipo del commit (type): " TYPEDESC

# Solicitar el mensaje del commit al usuario
read -p "Introduce el mensaje del commit (subject): " SUBJECT

# Solicitar el cuerpo del commit
read -p "Introduce el cuerpo del commit (body): " BODY

# Definir el footer fijo
FOOTER="👽 LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429  👽  https://www.reddit.com/r/LazyOwn/   👽  https://grisuno.github.io/LazyOwn/"

# Formatear el mensaje del commit
COMMIT_MESSAGE="${TYPE}(${TYPEDESC}): ${SUBJECT}\n\n${BODY}\n\n${FOOTER}"

# Obtener el último tag y el commit actual
START_COMMIT=$(git describe --tags --abbrev=0)
END_COMMIT=$(git rev-parse HEAD)

# Crear o limpiar el archivo de changelog
echo "# Changelog" > $CHANGELOG_FILE
echo "" >> $CHANGELOG_FILE

# Agregar los cambios al changelog
git log --pretty=format:"* %s" $START_COMMIT..$END_COMMIT >> $CHANGELOG_FILE

# Mensaje indicando que el changelog se ha generado
echo "Changelog generado en $CHANGELOG_FILE"

# Añadir todos los cambios
git add .

# Realizar el commit con el mensaje proporcionado
git commit -m "$COMMIT_MESSAGE"

# Generar el changelog después del commit
# Actualizar el archivo CHANGELOG.md
echo "# Changelog" > $CHANGELOG_FILE
echo "" >> $CHANGELOG_FILE
git log --pretty=format:"* %s" $START_COMMIT..$END_COMMIT >> $CHANGELOG_FILE
echo "Changelog actualizado en $CHANGELOG_FILE"

# Añadir el archivo de changelog al commit
git add $CHANGELOG_FILE

# Convertir el changelog a HTML
pandoc $CHANGELOG_FILE -f markdown -t html -s -o CHANGELOG.html
mv CHANGELOG.html docs/CHANGELOG.html
git add docs/CHANGELOG.html

# Realizar el commit (modificar el commit actual para incluir el changelog)
git commit --amend --no-edit

# Hacer push al repositorio remoto
git push

echo "Cambios enviados al repositorio remoto."
