#!/bin/bash


readonly CHANGELOG_FILE="CHANGELOG.md"
readonly README_FILE="README.md"

UTILS_FILE="UTILS.md"
COMMANDS_FILE="COMMANDS.md"

FORCE_VERSION=""

# Función para procesar argumentos
process_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --force-version)
                FORCE_VERSION="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done
}

process_args "$@"

if [[ "$1" != "--no-test" ]]; then
    
    python3 testmeneitor.py lazyown
fi
increment_version() {
  if [[ -n "$FORCE_VERSION" ]]; then
      NEW_VERSION="${FORCE_VERSION#release/}"  # Extrae la versión después de 'release/'
  else
      CURRENT_VERSION=$(git -C . describe --tags --abbrev=0 2>/dev/null || echo "0.2.0")
      
      case $TYPE in
          feat|feature|fix|hotfix)
              NEW_VERSION=$(increment_version $CURRENT_VERSION "patch")
              ;;
          refactor|docs|test)
              NEW_VERSION=$CURRENT_VERSION
              ;;
          release)
              NEW_VERSION=$(increment_version $CURRENT_VERSION "major")
              ;;
          patch)
              NEW_VERSION=$(increment_version $CURRENT_VERSION "minor")
              ;;
          *)
              echo "Invalid commit type: $TYPE" >&2
              exit 1
              ;;
      esac
  fi

}


rm d2*


python3 readmeneitor.py lazyown
python3 readmeneitor.py utils.py

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
echo "[*] El archivo $README_FILE ha sido actualizado con el contenido de UTILS.md, COMMANDS.md, y CHANGELOG.md."
pandoc $README_FILE -f markdown -t html -s -o  README.html --metadata title="README LazyOwn Framework Pentesting t00lz"
mv README.html docs/README.html
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
echo "[*] El archivo $INDEX_FILE ha sido actualizado con el contenido de README.html"
echo -e "[?] Selecciona el tipo de commit:\n1) feat\n2) feature\n3) fix\n4) hotfix\n5) refactor\n6) docs\n7) test\n8) release \n9) patch\n10) style\n11) chore "
read -r -p "Introduce el número del tipo de commit: " TYPE_OPTION

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

read -r -p "Introduce el tipo del commit (type): " TYPEDESC
read -r -p "Introduce el mensaje del commit (subject): " SUBJECT
read -r -p "Introduce el cuerpo del commit (body): " BODY
FOOTER=" LazyOwn on HackTheBox: https://app.hackthebox.com/teams/overview/6429 \n\n  LazyOwn/   https://grisuno.github.io/LazyOwn/ \n\n"
case $TYPE in
    feat|feature|fix|hotfix)
        
        NEW_VERSION=$(increment_version $CURRENT_VERSION "patch")
        ;;
    refactor|docs|test|style|chore)
        
        NEW_VERSION=$CURRENT_VERSION
        ;;
    release)
        
        NEW_VERSION=$(increment_version $CURRENT_VERSION "major")
        ;;
    patch)
        
        NEW_VERSION=$(increment_version $CURRENT_VERSION "minor")
        ;;
    *)
        echo "Invalid commit type: $TYPE" >&2
        exit 1
        ;;
esac
echo "{\"version\": \"$NEW_VERSION\"}" > version.json
git -C . add version.json
#LISTFILES=" Modified file(s): $(git diff --name-only $START_COMMIT $END_COMMIT | sed 's/^/- /')"
MODIFIED_FILES=$(git diff --name-only $START_COMMIT $END_COMMIT | sed 's/^/- /')
DELETED_FILES=$(git diff --name-only --diff-filter=D $START_COMMIT $END_COMMIT | sed 's/^/- /')
CREATED_FILES=$(git diff --name-only --diff-filter=A $START_COMMIT $END_COMMIT | sed 's/^/- /')

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
COMMIT_MESSAGE="${TYPE}(${TYPEDESC}): ${SUBJECT} \n\n Version: ${NEW_VERSION} \n\n ${BODY} \n\n ${LISTFILES} ${FOOTER} \n\n Fecha: $(git log -1 --format=%ad) \n\n Hora: $(git log -1 --format=%at)"
START_COMMIT=$(git -C . describe --tags --abbrev=0)
END_COMMIT=$(git -C . rev-parse HEAD)


echo "# Changelog" > $CHANGELOG_FILE
echo "" >> $CHANGELOG_FILE
git -C . log --format="%s" $START_COMMIT..$END_COMMIT >> $CHANGELOG_FILE
echo "[*] Changelog generado en $CHANGELOG_FILE"
git -C . add .
git -C . commit -S -a -m "$COMMIT_MESSAGE"

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

echo "# Changelog" > $CHANGELOG_FILE
echo "" >> $CHANGELOG_FILE

git log --pretty=format:"%s" | while read -r commit_message; do
  commit_type=$(get_commit_type "$commit_message")
  echo "$commit_type" >> $CHANGELOG_FILE
  echo "  * $commit_message" >> $CHANGELOG_FILE
  echo "" >> $CHANGELOG_FILE
done

echo "[+] Changelog generado y formateado en $CHANGELOG_FILE"

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
      } else if (a[i] ~ /^style\(/) {
        print "### Estilo\n"
        print "  * " a[i] "\n"
      } else if (a[i] ~ /^chore\(/) {
        print "### Tarea\n"
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

git -C . add $CHANGELOG_FILE

pandoc $CHANGELOG_FILE -f markdown -t html -s -o CHANGELOG.html --metadata title="CHANGELOG LazyOwn Framework Pentesting t00lz"
mv CHANGELOG.html docs/CHANGELOG.html
git -C . add docs/CHANGELOG.html
git -C . commit  -S --amend --no-edit
git -C . tag -s $NEW_VERSION -m "Version $NEW_VERSION"
git -C . push --follow-tags
echo "[*] Cambios enviados al repositorio remoto con la nueva versión $NEW_VERSION."
