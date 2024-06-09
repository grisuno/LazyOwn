#!/bin/bash

################################################################################
# Nombre del script: py2elf.sh
# Autor: Gris Iscomeback
# Correo electrónico: grisiscomeback[at]gmail[dot]com
# Fecha de creación: 09/06/2024
# Descripción: Este script contiene la lógica principal de la aplicación. py2elf 
# para ofuscar y paquetizar el Framework mediante pyinstaller
# Licencia: GPL v3
################################################################################
pip install pyinstaller
pyinstaller --onefile app.py
mv app.spec.dist app.spec
pyinstaller app.spec
