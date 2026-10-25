#!/bin/bash

# Verifica si se pasó una IP
if [ -z "$1" ]; then
  echo "Uso: $0 <ip>"
  exit 1
fi

IP=$1
DAYS=365

# Generate a random passphrase instead of a hardcoded one
PASSPHRASE=$(openssl rand -base64 24)

# Crear openssl.cnf dinámicamente
cat > openssl.cnf <<EOF
[ req ]
default_bits       = 2048
prompt             = no
default_md         = sha256
req_extensions     = req_ext
distinguished_name = dn

[ dn ]
CN = $IP

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
IP.1 = $IP
DNS.1 = localhost
EOF

echo "[+] Archivo openssl.cnf creado con IP: $IP"

# Generar clave privada con passphrase aleatoria
openssl genrsa -aes256 -passout "pass:$PASSPHRASE" -out key.pem 2048
echo "[+] Clave privada generada con passphrase aleatoria"

# Generar CSR usando el CN y SAN definidos
openssl req -new -key key.pem -out csr.pem -config openssl.cnf -passin "pass:$PASSPHRASE"
echo "[+] Solicitud de certificado generada (CSR)"

# Generar certificado auto-firmado con SANs
openssl x509 -req -in csr.pem -signkey key.pem -CAcreateserial -out cert.pem -days $DAYS -extensions req_ext -extfile openssl.cnf -passin "pass:$PASSPHRASE"
echo "[+] Certificado generado: cert.pem"

echo "[+] Passphrase de la clave privada (guárdala en un gestor seguro):"
echo "    $PASSPHRASE"

# Limpieza opcional (comentar si quieres conservar csr/serial)
rm -f csr.pem *.srl openssl.cnf
echo "[+] Archivos temporales eliminados"
