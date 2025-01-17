#!/bin/bash
KERNEL_VERSION=$(uname -r)
DEST_DIR="/lib/modules/$KERNEL_VERSION/build"
download_kernel_sources() {
    local version=$1
    local package="linux-source-$version"

    echo "Descargando las fuentes del kernel $version..."
    sudo apt-get update
    sudo apt-get install -y $package

    if [ $? -ne 0 ]; then
        echo "Error al descargar las fuentes del kernel."
        exit 1
    fi

    echo "Extrayendo las fuentes del kernel..."
    mkdir -p $DEST_DIR
    tar -xjf /usr/src/$package.tar.bz2 -C $DEST_DIR --strip-components=1

    if [ $? -ne 0 ]; then
        echo "Error al extraer las fuentes del kernel."
        exit 1
    fi

    echo "Fuentes del kernel $version instaladas en $DEST_DIR."
}
if [ $# -eq 1 ]; then
    KERNEL_VERSION=$1
fi


download_kernel_sources $KERNEL_VERSION
