#!/bin/bash

infile="$1"
uri="$2"
username="$3"
password="$4"
if [[ ! -f "$infile" ]]; then
    echo "    [!] Error: File '$infile' not found."
    exit 1
fi
content_type=$(file --mime-type -b "$infile")
response=$(curl -s -o /dev/null -w "%{http_code}" -u "$username:$password" \
    -F "file=@$infile;type=$content_type" \
    "$uri")

if [[ "$response" -eq 200 || "$response" -eq 201 ]]; then
    echo "    [!] File Uploaded!"
else
    echo "    [!] Error Uploading... HTTP: $response"
fi
# invoke_multipart_form_data_upload.sh "/ruta/al/archivo.txt" "https://example.com/upload" "usuario" "contraseña"