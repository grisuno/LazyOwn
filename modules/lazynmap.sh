#!/bin/bash
################################################################################
# Nombre del script: lazynmap.sh
# Autor: Gris Iscomeback
# Correo electrónico: grisiscomeback[at]gmail[dot]com
# Fecha de creación: 09/06/2024
# Descripción: Este script contiene la lógica principal de la aplicación. lazynmap
# Licencia: GPL v3
################################################################################

echo "    ██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗"
echo "    ██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║"
echo "    ██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║"
echo "    ██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║"
echo "    ███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║"
echo "    ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝"
echo "    LazyNmap...:::...::.::......::::....::..::::..:::..:::...:::..:"
trap ctrl_c INT

function ctrl_c() {
	echo "    [;,;] Trapped CTRL-C"
	exit 1
}

DIRECTORIO="./sessions"
ARCHIVO="$DIRECTORIO/nmap-bootstrap.xsl"

# Verificar si el archivo no existe
if [ ! -f "$ARCHIVO" ]; then
    echo "    [*] The file don't exist. Downloading..."
    wget https://raw.githubusercontent.com/honze-net/nmap-bootstrap-xsl/stable/nmap-bootstrap.xsl -O "$ARCHIVO"
else
    echo "    [+] The file exist. Don't download again."
fi

if [ $# -lt 1 ]; then
	echo "    [?] use: $0 -t <target>"
	exit 1
fi

TARGET=""
DISCOVER_NETWORK=false

while getopts "t:d" opt; do
	case ${opt} in
	t)
		TARGET=$OPTARG
		;;
	d)
		DISCOVER_NETWORK=true
		;;
	\?)
		echo "    [?] Use: $0 -t <target> [-d]"
		exit 1
		;;
	esac
done

if [ -z "$TARGET" ] && [ "$DISCOVER_NETWORK" = false ]; then
	echo "    [?] Use: $0 -t <target> [-d]"
	exit 1
fi

echo "    [+] Updating Nmap NSE Scripts DataBase..."
sudo nmap --script-updatedb

discover_network() {
	echo "    [+] Discovering local network..."
	local subnet=$(ip -o -f inet addr show | awk '/scope global/ {print $4}')
	for net in $subnet; do
		net_sanitized=$(echo "$net" | tr '/' '_')
		echo "    [-] Scannign subnet $net..."
		sudo nmap -sn $net -oG network_discovery -oN "sessions/scan_discovery_${net_sanitized}.nmap" --stylesheet "$ARCHIVO" -oX "sessions/scan_discovery_${net_sanitized}.nmap.xml"
		echo "    [+] Active Host in the network $net:"
		grep "Up" network_discovery | awk '{print $2}'
	done
}

for xmlfile in "$DIRECTORIO"/*.xml; do
	echo "$xmlfile"
    base_name=$(basename "$xmlfile" .xml)
    echo "$base_name"
    nmapfile="$DIRECTORIO/$base_name"
    if [[ -f "$nmapfile" ]]; then
        htmlfile="$DIRECTORIO/$base_name.html"
        xsltproc -o "$htmlfile" "$ARCHIVO" "$xmlfile"
        echo "    [+] Report generated HTML: $htmlfile"
    else
        echo "    [-] File .nmap Notfound to: $xmlfile"
    fi
done

OUTPUT_HTML="./sessions/index2.html"

cat <<EOL > $OUTPUT_HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚠ LazyOwn ⚠ Framwork 👽 WebServer ☠ [;,;] </title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
		body {
			display: flex;
			min-height: 100vh;
			background-color: #2b2b2b;
			color: #a9b7c6;
			font-family: Arial, sans-serif;
		}
		.sidebar {
			min-width: 350px;
			max-width: 350px;
			background-color: #3c3f41;
			padding: 15px;
		}
		.content {
			flex: 1;
			padding: 15px;
			background-color: #2b2b2b;
			color: #a9b7c6;
		}
		.sidebar a {
			display: block;
			padding: 10px;
			color: #a9b7c6;
			text-decoration: none;
		}
		.sidebar a:hover {
			background-color: #007bff;
			color: #ffffff;
		}
		img {
			border-radius: 15px; /* Bordes redondeados */
			box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Sombra */
			border: 2px dotted #4CAF50; /* Línea punteada de delimitador */
			padding: 5px; /* Espacio interno */
			transition: transform 0.3s; /* Efecto de transición */
			transform: scale(0.5); /* Reduce el tamaño a la mitad */
		}

		/* Efecto al pasar el ratón */
		img:hover {
			animation: bounce 0.5s; /* Animación de rebote */
			transform: scale(1); /* Aumenta al tamaño original */
		}

		/* Definición de la animación de rebote */
		@keyframes bounce {
			0%, 20%, 50%, 80%, 100% {
				transform: scale(1); /* Tamaño original */
			}
			40% {
				transform: scale(1.2); /* Aumenta el tamaño */
			}
			60% {
				transform: scale(1.1); /* Aumenta un poco menos */
			}
		}
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>Reportes Nmap 👽</h2>

EOL

for file in "$DIRECTORIO"/*.html; do
    if [[ -f "$file" ]]; then
        file_name=$(basename "$file")
        echo "        <a href=\"$file_name\">$file_name</a>" >> $OUTPUT_HTML
    fi
done

cat <<EOL >> $OUTPUT_HTML
		<img src="graph.png" alt="graph.png">
    </div>
    <div class="content">
        <h2>⚠ LazyOwn ⚠ Framwork 👽 WebServer ☠ [;,;] </h2>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>File name</th>
                </tr>
            </thead>
            <tbody>
EOL

for file in "$DIRECTORIO"/*; do
    if [[ -f "$file" ]]; then
        file_name=$(basename "$file")

        echo "                <tr>" >> $OUTPUT_HTML
        echo "                    <td><a href='$file_name'>$file_name</a></td>" >> $OUTPUT_HTML

        echo "                </tr>" >> $OUTPUT_HTML
    fi
done

# Finalizar el archivo HTML
cat <<EOL >> $OUTPUT_HTML
            </tbody>
        </table>
			
    </div>
</body>
</html>
EOL

echo "    [*] File generated: $OUTPUT_HTML"

chown 1000:1000 sessions -R
chmod 755 sessions -R

if [ "$DISCOVER_NETWORK" = true ]; then
	discover_network
	exit 0
fi

START_TIME=$(date +%s)

echo "    [-] Starting Recon LazyOwn RedTeam Framework Nmap Script..."
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn $TARGET -oG puertos -oN "sessions/scan_${TARGET}.nmap" --stylesheet "$ARCHIVO" -oX "sessions/scan_${TARGET}.nmap.xml"
echo "sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn $TARGET -oG puertos -oN "sessions/scan_${TARGET}.nmap" --stylesheet "$ARCHIVO" -oX "sessions/scan_${TARGET}.nmap.xml""
echo "sudo nmap -sTV -A --script=vulners.nse $TARGET -oN 'sessions/vulns_${TARGET}.nmap' --stylesheet '$ARCHIVO' -oX 'sessions/vulns_${TARGET}.nmap.xml'"
sudo nmap -sTV -A --script=vulners.nse $TARGET -oN "sessions/vulns_${TARGET}.nmap" --stylesheet "$ARCHIVO" -oX "sessions/vulns_${TARGET}.nmap.xml"

extract_ports_info() {
	local file=$1
	ports=$(grep -oP '\d{1,5}/open' $file | awk '{print $1}' FS='/' | xargs | tr ' ' ',')
	ip_address=$(grep -oP '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' $file | sort -u | head -n 1)
	echo -e "\n    [*] Extrcting info...\n"
	echo -e "\t    [*] IP Address: $ip_address"
	echo -e "\t    [*] Open Ports: $ports\n"
}

extract_ports_info "puertos"

PORTS=$(grep -oP '\d{1,5}/open/tcp' puertos | awk -F/ '{print $1}' | tr '\n' ',' | sed 's/,$//')

if [ -z "$PORTS" ]; then
	echo "    [!] Not open ports found in the target: $TARGET"
	exit 1
fi

echo "    [+] Open Ports found:: $PORTS"

run_nmap_script() {
	PORT=$1
	echo "    [;,;] Scanning port: $PORT at the target: $TARGET..."
	sudo nmap -p $PORT -sCV $TARGET -oN "sessions/scan_${TARGET}_${PORT}.nmap" --stylesheet "$ARCHIVO" -oX "sessions/scan_${TARGET}_${PORT}.nmap.xml"
}

export -f run_nmap_script
export TARGET

echo $PORTS | tr ',' '\n' | xargs -P 0 -I {} bash -c 'run_nmap_script "$@"' _ {}

SCANS=$(ls -1 sessions/scan_*.nmap 2>/dev/null)

if [ -z "$PORTS" ]; then
	echo "    [-] Not found open ports at file 'puertos'"
	exit 1
fi

if [ -z "$SCANS" ]; then
	echo "    [-] Not found open scan files (scan_*.nmap)"
	exit 1
fi

print_row() {
	printf "    | %-10s | %-60s |\n" "$1" "$2"
}

echo "    +------------+--------------------------------------------------------------+"
print_row "    Port:" "Information of Scann"
echo "    +------------+--------------------------------------------------------------+"

for PORT in $(echo $PORTS |     tr ',' ' '); do
	INFO=""

	for SCAN_FILE in $SCANS; do

		SCAN_INFO=$(grep -A 10 "$PORT/tcp" "$SCAN_FILE" | grep -v "$PORT/tcp")
		if [ -n "$SCAN_INFO" ]; then
			INFO="$SCAN_INFO"
			break
		fi
	done

	print_row "$PORT" "$INFO"
done

echo "    +------------+--------------------------------------------------------------+"

for xmlfile in "$DIRECTORIO"/*.xml; do

	echo "$xmlfile"
    base_name=$(basename "$xmlfile" .xml)
    echo "$base_name"

    nmapfile="$DIRECTORIO/$base_name"
    if [[ -f "$nmapfile" ]]; then

        htmlfile="$DIRECTORIO/$base_name.html"
        xsltproc -o "$htmlfile" "$ARCHIVO" "$xmlfile"
        echo "    [+] Rport generating HTML: $htmlfile"
    else
        echo "    [-] File .nmap not found to $xmlfile"
    fi
done

OUTPUT_HTML="./sessions/index2.html"

cat <<EOL > $OUTPUT_HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚠ LazyOwn ⚠ Framwork 👽 WebServer ☠ [;,;] </title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
		body {
			display: flex;
			min-height: 100vh;
			background-color: #2b2b2b;
			color: #a9b7c6;
			font-family: Arial, sans-serif;
		}
		.sidebar {
			min-width: 350px;
			max-width: 350px;
			background-color: #3c3f41;
			padding: 15px;
		}
		.content {
			flex: 1;
			padding: 15px;
			background-color: #2b2b2b;
			color: #a9b7c6;
		}
		.sidebar a {
			display: block;
			padding: 10px;
			color: #a9b7c6;
			text-decoration: none;
		}
		.sidebar a:hover {
			background-color: #007bff;
			color: #ffffff;
		}
		img {
			border-radius: 15px; /* Bordes redondeados */
			box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Sombra */
			border: 2px dotted #4CAF50; /* Línea punteada de delimitador */
			padding: 5px; /* Espacio interno */
			transition: transform 0.3s; /* Efecto de transición */
			transform: scale(0.5); /* Reduce el tamaño a la mitad */
		}

		/* Efecto al pasar el ratón */
		img:hover {
			animation: bounce 0.5s; /* Animación de rebote */
			transform: scale(1); /* Aumenta al tamaño original */
		}

		/* Definición de la animación de rebote */
		@keyframes bounce {
			0%, 20%, 50%, 80%, 100% {
				transform: scale(1); /* Tamaño original */
			}
			40% {
				transform: scale(1.2); /* Aumenta el tamaño */
			}
			60% {
				transform: scale(1.1); /* Aumenta un poco menos */
			}
		}
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>Nmap Reports 👽</h2>
EOL

for file in "$DIRECTORIO"/*.html; do
    if [[ -f "$file" ]]; then
        file_name=$(basename "$file")
        echo "        <a href=\"$file_name\">$file_name</a>" >> $OUTPUT_HTML
    fi
done

cat <<EOL >> $OUTPUT_HTML
	<img src="graph.png" alt="graph.png">
    </div>
    <div class="content">
        <h2>⚠ LazyOwn ⚠ Framwork 👽 WebServer ☠ [;,;] </h2>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Nombre del Archivo</th>
                </tr>
            </thead>
            <tbody>
EOL

for file in "$DIRECTORIO"/*; do
    if [[ -f "$file" ]]; then
        file_name=$(basename "$file")

        echo "                <tr>" >> $OUTPUT_HTML
        echo "                    <td><a href='$file_name'>$file_name</a></td>" >> $OUTPUT_HTML

        echo "                </tr>" >> $OUTPUT_HTML
    fi
done

cat <<EOL >> $OUTPUT_HTML
            </tbody>
        </table>
    </div>
</body>
</html>
EOL

echo "    [*] File HTML Generated: $OUTPUT_HTML"
chown 1000:1000 sessions -R
chmod 755 sessions -R

END_TIME=$(date +%s)
EXECUTION_TIME=$(($END_TIME - $START_TIME))

echo "    [t] The Execution time was:: $EXECUTION_TIME seconds."
