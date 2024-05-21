import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import time
import os

# URL base del servidor
base_url = "https://gtfobins.github.io/"

# Nombre del archivo CSV de entrada
input_csv = "bin_data.csv"

# Nombre del archivo de salida CSV
output_csv = "bin_data_relevant.csv"

# Función para obtener la información relevante de una URL
def obtener_informacion(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error al obtener la URL: {url}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []

    for section in soup.find_all('h2', class_='function-name'):
        function_name = section.text.strip()
        function_id = section.get('id')
        function_url = f"{url}#{function_id}"
        description = section.find_next('p').text.strip() if section.find_next('p') else ""
        example = section.find_next('code').text.strip() if section.find_next('code') else ""

        data.append({
            "function_name": function_name,
            "function_url": function_url,
            "description": description,
            "example": example
        })

    return data

# Leer el archivo CSV de entrada
binarios_funciones = {}
with open(input_csv, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        binary = row['Binary']
        if binary not in binarios_funciones:
            binarios_funciones[binary] = row['Function URL'].split('#')[0]

# Verificar si ya existe un archivo de salida y hasta dónde se ha procesado
resume = False
if os.path.exists(output_csv):
    with open(output_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
        if len(rows) > 1:
            last_processed = rows[-1][2]
            resume = True

# Inicializar una lista para almacenar toda la información
informacion_binarios = []

# Abrir el archivo CSV para escritura
csv_file = open(output_csv, mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Binary', 'Function Name', 'Function URL', 'Description', 'Example'])

# Recorrer la lista de binarios y sus funciones
for binary, url in binarios_funciones.items():
    # Si estamos retomando desde un punto anterior, saltamos hasta el último URL procesado
    if resume:
        if url != last_processed:
            continue
        else:
            resume = False
    full_url = urljoin(base_url, url)
    
    informacion = obtener_informacion(full_url)
    for item in informacion:
        informacion_binarios.append({
            "binary": binary,
            "function_name": item["function_name"],
            "function_url": item["function_url"],
            "description": item["description"],
            "example": item["example"]
        })
        # Guardar la información en el archivo CSV
        csv_writer.writerow([binary, item['function_name'], item['function_url'], item['description'], item['example']])
        print(f"[+] Binary: {binary} {item['function_name']}")
    # Hacemos una pausa de 5 segundos entre cada solicitud de URL
    time.sleep(5)

# Cerrar el archivo CSV
csv_file.close()

print(f"Datos guardados en {output_csv}")
