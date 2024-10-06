#!/bin/bash

# Verificar si se proporcionó un argumento para el host remoto
if [ "$#" -ne 1 ]; then
    echo "Uso: $0 <host-remoto>"
    exit 1
fi

TARGET="$1"
LOCAL_DIR="./sessions/lynis"
REMOTE_DIR="~/tmp-lynis"
TAR_FILE="$LOCAL_DIR/lynis-remote.tar.gz"
REMOTE_TAR_FILE="~/tmp-lynis-remote.tgz"
REMOTE_LOG="/tmp/lynis.log"
REMOTE_REPORT="/tmp/lynis-report.dat"
LOCAL_LOG="$LOCAL_DIR/$TARGET-lynis.log"
LOCAL_REPORT="$LOCAL_DIR/$TARGET-lynis-report.dat"
CREDENTIALS_FILE="./sessions/credentials.txt"

# Verificar si el archivo de credenciales existe
if [ ! -f "$CREDENTIALS_FILE" ]; then
    echo "[Error] El archivo $CREDENTIALS_FILE debe existir. Ejemplo: createcredentials user:password"
    exit 1
fi

# Leer las credenciales
read -r CREDENTIALS < "$CREDENTIALS_FILE"
USER="${CREDENTIALS%%:*}"   # Obtener el usuario
PASSWORD="${CREDENTIALS##*:}" # Obtener la contraseña

# Función para verificar y relanzar con sudo si es necesario
check_sudo() {
    if [ "$EUID" -ne 0 ]; then
        echo "[S] Este script necesita permisos de superusuario. Relanzando con sudo..."
        exec sudo bash "$0" "$@"
        exit
    fi
}

check_sudo

# Paso 1: Crear tarball
mkdir -p $LOCAL_DIR && tar czf $TAR_FILE --exclude=$TAR_FILE /usr/sbin/lynis
echo "Tarball creado: $TAR_FILE"

# Paso 2: Copiar tarball al destino usando scp con autenticación
sshpass -p "$PASSWORD" scp -o StrictHostKeyChecking=no -q $TAR_FILE "$USER@$TARGET:$REMOTE_TAR_FILE"
echo "Tarball copiado a: $TARGET:$REMOTE_TAR_FILE"

# Paso 3: Ejecutar Lynis en el sistema remoto usando ssh con autenticación
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$USER@$TARGET" <<EOF
    mkdir -p $REMOTE_DIR
    cd $REMOTE_DIR
    tar -xzf ../$REMOTE_TAR_FILE
    rm ../$REMOTE_TAR_FILE
    cd lynis
    sudo ./lynis audit system
    echo 'Lynis audit completed'
EOF
echo "Lynis ejecutado en: $TARGET"

# Paso 4: Recuperar log y reporte
sshpass -p "$PASSWORD" scp -o StrictHostKeyChecking=no -q "$USER@$TARGET:$REMOTE_LOG" "$LOCAL_LOG"
sshpass -p "$PASSWORD" scp -o StrictHostKeyChecking=no -q "$USER@$TARGET:$REMOTE_REPORT" "$LOCAL_REPORT"
echo "Log y reporte recuperados a: $LOCAL_LOG y $LOCAL_REPORT"

# Paso 5: Limpiar archivos temporales
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$USER@$TARGET" "rm -f $REMOTE_LOG $REMOTE_REPORT"
echo "Archivos temporales limpiados en: $TARGET"

# Paso 6: Eliminar directorio temporal
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$USER@$TARGET" "rm -rf $REMOTE_DIR"
echo "Directorio temporal eliminado en: $TARGET"
