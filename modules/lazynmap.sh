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
sudo chown 1000:1000 sessions -R
sudo chmod 777 sessions/temp_uploads -R
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
		python3 modules/nmap2csv.py -i "sessions/scan_discovery_${net_sanitized}.nmap" -o "sessions/scan_discovery_${net_sanitized}.csv"
		echo "    [+] Active Host in the network $net:" 
		grep "Up" network_discovery | awk '{print $2}' | tee "sessions/hosts_$(echo "$net" | tr '/' '_')_discovery.txt"
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
		/* Estilo general para el texto neón */
		.neon-text {
			color: #00ffff;
			text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 40px #00ffff;
			animation: flicker 1.5s infinite alternate;
			font-family: 'VT323', 'Courier New', Courier, monospace;
			white-space: pre !important;
			transition: all 0.3s ease;
		}

		/* Animación de parpadeo para el texto neón */
		@keyframes flicker {
			0%, 18%, 22%, 25%, 53%, 57%, 100% {
				opacity: 1;
			}
			24%, 54% {
				opacity: 0.8;
			}
		}

		/* Estilo para el contenedor de la red */
		#mynetwork {
			width: 100%;
			height: 768px;
			border: 1px solid #333;
			background: linear-gradient(135deg, #1e1e1e, #2e2e2e);
			border-radius: 10px;
			box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
			animation: fadeIn 1s ease-in-out;
			transition: all 0.3s ease;
		}

		/* Estilo para las secciones */
		.section {
			display: none;
		}

		.section.active {
			display: block;
			animation: fadeIn 0.5s ease-in-out;
			transition: all 0.3s ease;
		}

		@keyframes fadeIn {
			from {
				opacity: 0;
			}
			to {
				opacity: 1;
			}
		}

		/* Estilo para la ventana de terminal */
		.terminal-window {
			background-color: #1e1e1e;
			color: #c0c0c0;
			font-family: 'Fira Code', 'Courier New', Courier, monospace;
			padding: 20px;
			border: 2px solid #333;
			border-radius: 8px;
			position: relative;
			box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
			word-break: break-all;
			max-width: 800px;
			margin: auto;
			transition: transform 0.3s ease, box-shadow 0.3s ease;
		}

		.terminal-window:hover {
			transform: scale(1.02);
			box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
		}

		/* Estilo para el encabezado del terminal */
		.terminal-header {
			background-color: #2e2e2e;
			color: #c0c0c0;
			padding: 10px 20px;
			border-bottom: 2px solid #444;
			display: flex;
			justify-content: space-between;
			align-items: center;
			border-top-left-radius: 8px;
			border-top-right-radius: 8px;
		}

		/* Estilo para el título del terminal */
		.terminal-title {
			font-weight: bold;
			font-size: 1.2em;
		}

		/* Estilo para los controles del terminal */
		.terminal-controls {
			display: flex;
			gap: 10px;
		}

		.terminal-control-button {
			width: 14px;
			height: 14px;
			border-radius: 50%;
			cursor: pointer;
			transition: background-color 0.3s, transform 0.3s;
		}

		.close-button {
			background-color: #e81123;
		}

		.minimize-button {
			background-color: #f0ad4e;
		}

		.maximize-button {
			background-color: #00ffff;
		}

		.terminal-control-button:hover {
			opacity: 0.8;
			transform: scale(1.2);
		}

		/* Estilo para el cuerpo del terminal */
		.card-body {
			background-color: #1e1e1e;
			color: #c0c0c0;
			padding: 20px;
			border-radius: 0 0 8px 8px;
			font-family: 'Fira Code', 'Courier New', Courier, monospace;
			white-space: pre-wrap;
		}

		/* Estilo para el texto pequeño */
		.chico {
			font-size: 12px;
		}

		/* Estilo para las notificaciones */
		.toastr {
			position: fixed;
			top: 20px;
			right: 20px;
			z-index: 1050;
			width: 300px;
			opacity: 0;
			transition: opacity 0.5s, transform 0.5s;
			background-color: #333;
			color: #c0c0c0;
			border: 1px solid #444;
			border-radius: 8px;
			padding: 10px;
			box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
			transform: translateY(-20px);
		}

		.toastr.show {
			opacity: 1;
			transform: translateY(0);
		}

		/* Estilo para el dropdown personalizado */
		.custom-dropdown {
			background-color: #f8f9fa;
			border: 1px solid #ced4da;
			border-radius: 0.25rem;
			box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
		}

		/* Estilo para el contenedor principal */
		.container {
			max-width: 1200px;
			margin: 0 auto;
			padding: 20px;
			animation: fadeIn 1s ease-in-out;
			transition: all 0.3s ease;
		}

		/* Estilo para el encabezado principal */
		h1.neon-text {
			font-size: 2.5em;
			margin-bottom: 20px;
			animation: slideIn 1s ease-in-out;
			transition: all 0.3s ease;
		}

		@keyframes slideIn {
			from {
				opacity: 0;
				transform: translateX(-100%);
			}
			to {
				opacity: 1;
				transform: translateX(0);
			}
		}

		/* Estilo para el pie de página */
		.footer {
			background-color: #2e2e2e;
			color: #c0c0c0;
			padding: 20px;
			border-top: 2px solid #444;
			text-align: center;
			font-size: 1em;
			animation: fadeIn 1s ease-in-out;
			transition: all 0.3s ease;
		}

		/* Estilo para los botones */
		.btn {
			background-color: #00ffff;
			border: none;
			color: #fff;
			padding: 10px 20px;
			border-radius: 8px;
			transition: background-color 0.3s, transform 0.3s;
		}

		.btn:hover {
			background-color: #00e6e6;
			transform: scale(1.05);
		}

		/* Estilo para los enlaces de navegación */
		.nav-link {
			color: #c0c0c0;
			transition: color 0.3s, transform 0.3s;
		}

		.nav-link:hover {
			color: #fff;
			transform: scale(1.1);
		}

		/* Estilo para los formularios */
		.form-group {
			margin-bottom: 15px;
		}

		.form-control {
			background-color: #333;
			color: #00ffff;
			border: 1px solid #444;
			border-radius: 8px;
			padding: 10px;
			transition: background-color 0.3s, border-color 0.3s, transform 0.3s;
		}

		.form-control:focus {
			background-color: #444;
			border-color: #00ffff;
			transform: scale(1.02);
		}

		/* Estilo para el input de tipo file */
		.form-control-file {
			background-color: #333;
			color: #7a7a7a;
			border: 1px solid #444;
			border-radius: 8px;
			padding: 10px;
			transition: background-color 0.3s, border-color 0.3s, transform 0.3s;
		}

		.form-control-file:focus {
			background-color: #444;
			border-color: #00ffff;
			transform: scale(1.02);
		}

		/* Estilo para los acordeones */
		.accordion .card {
			background-color: #2e2e2e;
			border: 1px solid #444;
			border-radius: 8px;
			margin-bottom: 10px;
			transition: background-color 0.3s, transform 0.3s;
		}

		.accordion .card:hover {
			background-color: #3e3e3e;
			transform: scale(1.02);
		}

		.accordion .card-header {
			background-color: #3e3e3e;
			color: #535353;
			padding: 10px 20px;
			border-bottom: 1px solid #444;
			cursor: pointer;
			transition: background-color 0.3s;
		}

		.accordion .card-header:hover {
			background-color: #4e4e4e;
		}

		.accordion .card-body {
			background-color: #1e1e1e;
			color: #c0c0c0;
			padding: 20px;
			border-radius: 0 0 8px 8px;
		}

		/* Estilo para los elementos de la lista */
		.list-group-item {
			background-color: #2e2e2e;
			color: #c0c0c0;
			border: 1px solid #444;
			border-radius: 8px;
			margin-bottom: 10px;
			transition: background-color 0.3s, transform 0.3s;
		}

		.list-group-item:hover {
			background-color: #3e3e3e;
			transform: scale(1.02);
		}

		/* Estilo para los elementos de la lista de éxito */
		.list-group-item-success {
			background-color: #00ffff;
			color: #fff;
			transition: background-color 0.3s, transform 0.3s;
		}

		.list-group-item-success:hover {
			background-color: #00e6e6;
			transform: scale(1.02);
		}

		/* Estilo para los elementos de la lista de éxito al pasar el ratón */
		.list-group-item-success:active {
			background-color: #00b3b3;
			transform: scale(0.98);
		}

		/* Estilo para el preformateado */
		pre {
			background-color: #1e1e1e;
			color: #c0c0c0;
			padding: 10px;
			border-radius: 8px;
			font-family: 'Fira Code', 'Courier New', Courier, monospace;
			white-space: pre-wrap;
			transition: background-color 0.3s, transform 0.3s;
		}

		pre:hover {
			background-color: #2e2e2e;
			transform: scale(1.02);
		}

		/* Estilo para el cuerpo de la página */
		body.bg-dark {
			background: linear-gradient(135deg, #1e1e1e, #2e2e2e);
			color: #c0c0c0;
			font-family: 'Fira Code', 'Courier New', Courier, monospace;
			animation: fadeIn 1s ease-in-out;
			transition: all 0.3s ease;
		}

		/* Estilo para el input cuando tiene el foco */
		input[type="text"]:focus {
			background-color: #ffffff;
			color: #000000;
			border-color: #007bff;
			outline: none;
		}

		/* Estilo para los enlaces */
		a {
			color: #00ffff;
			transition: color 0.3s, transform 0.3s;
		}

		a:hover {
			color: #00e6e6;
			transform: scale(1.05);
		}

		/* Animación de carga */
		@keyframes loading {
			0% {
				transform: rotate(0deg);
			}
			100% {
				transform: rotate(360deg);
			}
		}

		/* Estilo para el spinner de carga */
		.loading-spinner {
			border: 4px solid rgba(0, 0, 0, 0.1);
			border-top: 4px solid #00ffff;
			border-radius: 50%;
			width: 40px;
			height: 40px;
			animation: loading 1s linear infinite;
			position: fixed;
			top: 50%;
			left: 50%;
			transform: translate(-50%, -50%);
			z-index: 10000;
		}

		/* Estilo para el contenedor de carga */
		.loading-container {
			position: fixed;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			background: rgba(0, 0, 0, 0.8);
			display: flex;
			justify-content: center;
			align-items: center;
			z-index: 9999;
		}

		/* Estilo para la barra de navegación */
		nav {
			background-color: #343a40;
			color: white;
			padding: 10px 0;
			text-align: center;
			transition: all 0.3s ease;
		}

		nav .nav-content {
			max-width: 1200px;
			margin: 0 auto;
			display: flex;
			justify-content: center;
		}

		nav ul {
			list-style: none;
			padding: 0;
			display: flex;
			gap: 20px;
		}

		nav ul li {
			margin: 0;
		}

		nav ul li a {
			color: white;
			text-decoration: none;
			padding: 10px 15px;
			transition: background-color 0.3s, color 0.3s, transform 0.3s;
		}

		nav ul li a:hover {
			background-color: #495057;
			color: #00ffff;
			transform: scale(1.1);
			box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
		}

		.sticky {
			position: fixed;
			top: 0;
			left: 0;
			width: 100%;
			z-index: 1000;
			box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
			animation: fadeIn 0.5s ease-in-out;
		}

		/* Animación de entrada para la barra de navegación */
		@keyframes fadeIn {
			from {
				opacity: 0;
			}
			to {
				opacity: 1;
			}
		}

    </style>
</head>
<body>
    <div class="sidebar">
        <h2>Reportes Nmap 👽</h2>
		<h3><a href="http://127.0.0.1:4444">C&C</h3>

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
        <h2>⚠ LazyOwn ⚠ RedTeam ☠ Framwork 👽 WebServer ☠ [;,;] </h2>
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
python3 modules/nmap2csv.py -i "sessions/scan_${TARGET}.nmap" -o "sessions/scan_${TARGET}.csv"
echo "sudo nmap -sTV -A --script=vulners.nse $TARGET -oN 'sessions/vulns_${TARGET}.nmap' --stylesheet '$ARCHIVO' -oX 'sessions/vulns_${TARGET}.nmap.xml'"
sudo nmap -sTV -A --script=vulners.nse $TARGET -oN "sessions/vulns_${TARGET}.nmap" --stylesheet "$ARCHIVO" -oX "sessions/vulns_${TARGET}.nmap.xml"
python3 modules/nmap2csv.py -i "sessions/vulns_${TARGET}.nmap" -o "sessions/vulns_${TARGET}.csv"

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
	python3 modules/nmap2csv.py -i "sessions/scan_${TARGET}_${PORT}.nmap" -o "sessions/scan_${TARGET}_${PORT}.csv" 
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
		/* Estilo general para el texto neón */
		.neon-text {
			color: #00ffff;
			text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 40px #00ffff;
			animation: flicker 1.5s infinite alternate;
			font-family: 'VT323', 'Courier New', Courier, monospace;
			white-space: pre !important;
			transition: all 0.3s ease;
		}

		/* Animación de parpadeo para el texto neón */
		@keyframes flicker {
			0%, 18%, 22%, 25%, 53%, 57%, 100% {
				opacity: 1;
			}
			24%, 54% {
				opacity: 0.8;
			}
		}

		/* Estilo para el contenedor de la red */
		#mynetwork {
			width: 100%;
			height: 768px;
			border: 1px solid #333;
			background: linear-gradient(135deg, #1e1e1e, #2e2e2e);
			border-radius: 10px;
			box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
			animation: fadeIn 1s ease-in-out;
			transition: all 0.3s ease;
		}

		/* Estilo para las secciones */
		.section {
			display: none;
		}

		.section.active {
			display: block;
			animation: fadeIn 0.5s ease-in-out;
			transition: all 0.3s ease;
		}

		@keyframes fadeIn {
			from {
				opacity: 0;
			}
			to {
				opacity: 1;
			}
		}

		/* Estilo para la ventana de terminal */
		.terminal-window {
			background-color: #1e1e1e;
			color: #c0c0c0;
			font-family: 'Fira Code', 'Courier New', Courier, monospace;
			padding: 20px;
			border: 2px solid #333;
			border-radius: 8px;
			position: relative;
			box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
			word-break: break-all;
			max-width: 800px;
			margin: auto;
			transition: transform 0.3s ease, box-shadow 0.3s ease;
		}

		.terminal-window:hover {
			transform: scale(1.02);
			box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
		}

		/* Estilo para el encabezado del terminal */
		.terminal-header {
			background-color: #2e2e2e;
			color: #c0c0c0;
			padding: 10px 20px;
			border-bottom: 2px solid #444;
			display: flex;
			justify-content: space-between;
			align-items: center;
			border-top-left-radius: 8px;
			border-top-right-radius: 8px;
		}

		/* Estilo para el título del terminal */
		.terminal-title {
			font-weight: bold;
			font-size: 1.2em;
		}

		/* Estilo para los controles del terminal */
		.terminal-controls {
			display: flex;
			gap: 10px;
		}

		.terminal-control-button {
			width: 14px;
			height: 14px;
			border-radius: 50%;
			cursor: pointer;
			transition: background-color 0.3s, transform 0.3s;
		}

		.close-button {
			background-color: #e81123;
		}

		.minimize-button {
			background-color: #f0ad4e;
		}

		.maximize-button {
			background-color: #00ffff;
		}

		.terminal-control-button:hover {
			opacity: 0.8;
			transform: scale(1.2);
		}

		/* Estilo para el cuerpo del terminal */
		.card-body {
			background-color: #1e1e1e;
			color: #c0c0c0;
			padding: 20px;
			border-radius: 0 0 8px 8px;
			font-family: 'Fira Code', 'Courier New', Courier, monospace;
			white-space: pre-wrap;
		}

		/* Estilo para el texto pequeño */
		.chico {
			font-size: 12px;
		}

		/* Estilo para las notificaciones */
		.toastr {
			position: fixed;
			top: 20px;
			right: 20px;
			z-index: 1050;
			width: 300px;
			opacity: 0;
			transition: opacity 0.5s, transform 0.5s;
			background-color: #333;
			color: #c0c0c0;
			border: 1px solid #444;
			border-radius: 8px;
			padding: 10px;
			box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
			transform: translateY(-20px);
		}

		.toastr.show {
			opacity: 1;
			transform: translateY(0);
		}

		/* Estilo para el dropdown personalizado */
		.custom-dropdown {
			background-color: #f8f9fa;
			border: 1px solid #ced4da;
			border-radius: 0.25rem;
			box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
		}

		/* Estilo para el contenedor principal */
		.container {
			max-width: 1200px;
			margin: 0 auto;
			padding: 20px;
			animation: fadeIn 1s ease-in-out;
			transition: all 0.3s ease;
		}

		/* Estilo para el encabezado principal */
		h1.neon-text {
			font-size: 2.5em;
			margin-bottom: 20px;
			animation: slideIn 1s ease-in-out;
			transition: all 0.3s ease;
		}

		@keyframes slideIn {
			from {
				opacity: 0;
				transform: translateX(-100%);
			}
			to {
				opacity: 1;
				transform: translateX(0);
			}
		}

		/* Estilo para el pie de página */
		.footer {
			background-color: #2e2e2e;
			color: #c0c0c0;
			padding: 20px;
			border-top: 2px solid #444;
			text-align: center;
			font-size: 1em;
			animation: fadeIn 1s ease-in-out;
			transition: all 0.3s ease;
		}

		/* Estilo para los botones */
		.btn {
			background-color: #00ffff;
			border: none;
			color: #fff;
			padding: 10px 20px;
			border-radius: 8px;
			transition: background-color 0.3s, transform 0.3s;
		}

		.btn:hover {
			background-color: #00e6e6;
			transform: scale(1.05);
		}

		/* Estilo para los enlaces de navegación */
		.nav-link {
			color: #c0c0c0;
			transition: color 0.3s, transform 0.3s;
		}

		.nav-link:hover {
			color: #fff;
			transform: scale(1.1);
		}

		/* Estilo para los formularios */
		.form-group {
			margin-bottom: 15px;
		}

		.form-control {
			background-color: #333;
			color: #00ffff;
			border: 1px solid #444;
			border-radius: 8px;
			padding: 10px;
			transition: background-color 0.3s, border-color 0.3s, transform 0.3s;
		}

		.form-control:focus {
			background-color: #444;
			border-color: #00ffff;
			transform: scale(1.02);
		}

		/* Estilo para el input de tipo file */
		.form-control-file {
			background-color: #333;
			color: #7a7a7a;
			border: 1px solid #444;
			border-radius: 8px;
			padding: 10px;
			transition: background-color 0.3s, border-color 0.3s, transform 0.3s;
		}

		.form-control-file:focus {
			background-color: #444;
			border-color: #00ffff;
			transform: scale(1.02);
		}

		/* Estilo para los acordeones */
		.accordion .card {
			background-color: #2e2e2e;
			border: 1px solid #444;
			border-radius: 8px;
			margin-bottom: 10px;
			transition: background-color 0.3s, transform 0.3s;
		}

		.accordion .card:hover {
			background-color: #3e3e3e;
			transform: scale(1.02);
		}

		.accordion .card-header {
			background-color: #3e3e3e;
			color: #535353;
			padding: 10px 20px;
			border-bottom: 1px solid #444;
			cursor: pointer;
			transition: background-color 0.3s;
		}

		.accordion .card-header:hover {
			background-color: #4e4e4e;
		}

		.accordion .card-body {
			background-color: #1e1e1e;
			color: #c0c0c0;
			padding: 20px;
			border-radius: 0 0 8px 8px;
		}

		/* Estilo para los elementos de la lista */
		.list-group-item {
			background-color: #2e2e2e;
			color: #c0c0c0;
			border: 1px solid #444;
			border-radius: 8px;
			margin-bottom: 10px;
			transition: background-color 0.3s, transform 0.3s;
		}

		.list-group-item:hover {
			background-color: #3e3e3e;
			transform: scale(1.02);
		}

		/* Estilo para los elementos de la lista de éxito */
		.list-group-item-success {
			background-color: #00ffff;
			color: #fff;
			transition: background-color 0.3s, transform 0.3s;
		}

		.list-group-item-success:hover {
			background-color: #00e6e6;
			transform: scale(1.02);
		}

		/* Estilo para los elementos de la lista de éxito al pasar el ratón */
		.list-group-item-success:active {
			background-color: #00b3b3;
			transform: scale(0.98);
		}

		/* Estilo para el preformateado */
		pre {
			background-color: #1e1e1e;
			color: #c0c0c0;
			padding: 10px;
			border-radius: 8px;
			font-family: 'Fira Code', 'Courier New', Courier, monospace;
			white-space: pre-wrap;
			transition: background-color 0.3s, transform 0.3s;
		}

		pre:hover {
			background-color: #2e2e2e;
			transform: scale(1.02);
		}

		/* Estilo para el cuerpo de la página */
		body.bg-dark {
			background: linear-gradient(135deg, #1e1e1e, #2e2e2e);
			color: #c0c0c0;
			font-family: 'Fira Code', 'Courier New', Courier, monospace;
			animation: fadeIn 1s ease-in-out;
			transition: all 0.3s ease;
		}

		/* Estilo para el input cuando tiene el foco */
		input[type="text"]:focus {
			background-color: #ffffff;
			color: #000000;
			border-color: #007bff;
			outline: none;
		}

		/* Estilo para los enlaces */
		a {
			color: #00ffff;
			transition: color 0.3s, transform 0.3s;
		}

		a:hover {
			color: #00e6e6;
			transform: scale(1.05);
		}

		/* Animación de carga */
		@keyframes loading {
			0% {
				transform: rotate(0deg);
			}
			100% {
				transform: rotate(360deg);
			}
		}

		/* Estilo para el spinner de carga */
		.loading-spinner {
			border: 4px solid rgba(0, 0, 0, 0.1);
			border-top: 4px solid #00ffff;
			border-radius: 50%;
			width: 40px;
			height: 40px;
			animation: loading 1s linear infinite;
			position: fixed;
			top: 50%;
			left: 50%;
			transform: translate(-50%, -50%);
			z-index: 10000;
		}

		/* Estilo para el contenedor de carga */
		.loading-container {
			position: fixed;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			background: rgba(0, 0, 0, 0.8);
			display: flex;
			justify-content: center;
			align-items: center;
			z-index: 9999;
		}

		/* Estilo para la barra de navegación */
		nav {
			background-color: #343a40;
			color: white;
			padding: 10px 0;
			text-align: center;
			transition: all 0.3s ease;
		}

		nav .nav-content {
			max-width: 1200px;
			margin: 0 auto;
			display: flex;
			justify-content: center;
		}

		nav ul {
			list-style: none;
			padding: 0;
			display: flex;
			gap: 20px;
		}

		nav ul li {
			margin: 0;
		}

		nav ul li a {
			color: white;
			text-decoration: none;
			padding: 10px 15px;
			transition: background-color 0.3s, color 0.3s, transform 0.3s;
		}

		nav ul li a:hover {
			background-color: #495057;
			color: #00ffff;
			transform: scale(1.1);
			box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
		}

		.sticky {
			position: fixed;
			top: 0;
			left: 0;
			width: 100%;
			z-index: 1000;
			box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
			animation: fadeIn 0.5s ease-in-out;
		}

		/* Animación de entrada para la barra de navegación */
		@keyframes fadeIn {
			from {
				opacity: 0;
			}
			to {
				opacity: 1;
			}
		}

    </style>
</head>
<body>
    <div class="sidebar">
        <h2>Nmap Reports 👽</h2>
		<h3><a href="http://127.0.0.1:4444">C&C</h3>
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
        <h2>⚠ LazyOwn ⚠ RedTeam ☠ Framwork 👽 WebServer ☠ [;,;] </h2>
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


END_TIME=$(date +%s)
EXECUTION_TIME=$(($END_TIME - $START_TIME))

echo "    [t] The Execution time was:: $EXECUTION_TIME seconds."
chown 1000:1000 sessions -R
chmod 755 sessions -R