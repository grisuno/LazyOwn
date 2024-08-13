#!/bin/bash

# Crea el readme en html
pandoc README.md -f markdown -t html -s -o README.html

# Nombre del archivo de changelog
CHANGELOG_FILE="CHANGELOG.md"

# Solicitar el mensaje del commit al usuario
read -p "Introduce el mensaje del commit: " COMMIT_MESSAGE

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

pandoc $CHANGELOG_FILE -f markdown -t html -s -o CHANGELOG.html
mv CHANGELOG.html docs/CHANGELOG.html
git add docs/CHANGELOG.html

# Realizar el commit (modificar el commit actual para incluir el changelog)
git commit --amend --no-edit

# Hacer push al repositorio remoto
git push

echo "Cambios enviados al repositorio remoto."
