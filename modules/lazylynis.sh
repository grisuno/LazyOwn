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

# Paso 2: Copiar tarball al destino
scp -q $TAR_FILE $TARGET:$REMOTE_TAR_FILE
echo "Tarball copiado a: $TARGET:$REMOTE_TAR_FILE"

# Paso 3: Ejecutar Lynis en el sistema remoto
ssh $TARGET <<EOF
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
scp -q $TARGET:$REMOTE_LOG $LOCAL_LOG
scp -q $TARGET:$REMOTE_REPORT $LOCAL_REPORT
echo "Log y reporte recuperados a: $LOCAL_LOG y $LOCAL_REPORT"

# Paso 5: Limpiar archivos temporales
ssh $TARGET "rm -f $REMOTE_LOG $REMOTE_REPORT"
echo "Archivos temporales limpiados en: $TARGET"

# Paso 6: Eliminar directorio temporal
ssh $TARGET "rm -rf $REMOTE_DIR"
echo "Directorio temporal eliminado en: $TARGET"
