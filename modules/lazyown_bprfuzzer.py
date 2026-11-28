#!/usr/bin/env python3
"""
main.py

Autor: Gris Iscomeback
Correo electrónico: grisiscomeback[at]gmail[dot]com
Fecha de creación: 09/06/2024
Licencia: AGPL v3

Descripción: Lazy Burp-Like Fuzzer con Proxy y Repeater

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

"""

import argparse
import json
import os
import signal
import subprocess
import sys
import tempfile
import threading
from urllib.parse import urlsplit, urlunsplit

import requests

_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_MODULE_DIR)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from modules.browser_sync import apply_identity_to_url  # noqa: E402
from modules.security_sanitizers import (  # noqa: E402
    HeaderValueSanitizer,
    build_default_config,
)

_PAYLOAD_PATH = os.path.join(_PROJECT_ROOT, "payload.json")


def _load_security_config():
    """Return a :class:`SecurityConfig` from ``payload.json`` when present.

    A missing or unreadable payload file falls back to the
    conservative defaults so the fuzzer can be invoked even before
    the framework wizard has produced a configuration.
    """
    try:
        with open(_PAYLOAD_PATH, "r") as fh:
            return build_default_config(json.load(fh))
    except (OSError, ValueError):
        return build_default_config(None)


_SECURITY_CONFIG = _load_security_config()
_HEADER_SANITIZER = HeaderValueSanitizer(_SECURITY_CONFIG)

_METADATA_HOSTS = frozenset(
    {
        "169.254.169.254",
        "169.254.170.2",
        "100.100.100.200",
        "fd00:ec2::254",
        "metadata",
        "metadata.google.internal",
        "metadata.azure.com",
        "instance-data",
    }
)
_LOOPBACK_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})
_PROXY_ALLOWED_HOSTS: set[str] = set()
_PROXY_ALLOW_LOOPBACK = os.environ.get("LAZY_BPRFUZZER_ALLOW_LOOPBACK", "").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}

# Forzar UTF-8 encoding
os.environ["PYTHONIOENCODING"] = "utf-8"

from http.server import BaseHTTPRequestHandler, HTTPServer  # noqa: E402

# Global flag for graceful shutdown
should_exit = False
BANNER = """
 _                           _____
(_)            _____        (_____)             _
(_)      ____ (_____)_   _ (_)   (_) _   _   _ (_)__
(_)     (____)  _(_)(_) (_)(_)   (_)(_) ( ) (_)(____)
(_)____( )_( ) (_)__(_)_(_)(_)___(_)(_)_(_)_(_)(_) (_)
(______)(__)_)(_____)(____) (_____)  (__) (__) (_) (_)
                      __(_)
                     (___)

 _____                          ______
(_____)         _              (______)     _____  _____  ____  _
(_)__(_) _   _ (_)__  ____     (_)__  _   _(_____)(_____)(____)(_)__
(_____) (_) (_)(____)(____)    (____)(_) (_) _(_)   _(_)(_)_(_)(____)
(_)__(_)(_)_(_)(_)   (_)_(_)   (_)   (_)_(_)(_)__  (_)__(__)__ (_)
(_____)  (___) (_)   (____)    (_)    (___)(_____)(_____)(____)(_)
                     (_)
                     (_)

[*] Iniciando: LazyOwn Fuzzer and Repeater Cli Assistent [;,;]
"""
print(BANNER)


def load_headers_from_file(file_path):
    with open(file_path, "r") as file:
        headers = json.load(file)
    return headers


def load_data_from_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def _normalise_proxy_host(value):
    """Return a lowercase host without scheme, port or IPv6 brackets."""
    text = str(value or "").strip().lower()
    if not text:
        return ""
    if "://" in text:
        try:
            text = urlsplit(text).hostname or ""
        except ValueError:
            return ""
    return text.strip("[]")


def _payload_proxy_hosts():
    """Return proxy allowlist candidates from payload.json."""
    try:
        with open(_PAYLOAD_PATH, "r") as fh:
            payload = json.load(fh)
    except (OSError, ValueError):
        return []
    values = [payload.get("rhost"), payload.get("domain"), payload.get("url")]
    extra = payload.get("bprfuzzer_allowed_hosts") or []
    if isinstance(extra, str):
        extra = [part.strip() for part in extra.split(",")]
    values.extend(extra if isinstance(extra, (list, tuple, set)) else [])
    return [str(value) for value in values if value]


def configure_proxy_allowlist(hosts, *, reset=False):
    """Seed the proxy host allowlist from trusted operator configuration.

    Args:
        hosts: Hostnames or URLs explicitly authorised for proxying.
        reset: When True, replace the current allowlist instead of extending it.
    """
    if reset:
        _PROXY_ALLOWED_HOSTS.clear()
    for host in hosts or ():
        normalized = _normalise_proxy_host(host)
        if normalized:
            _PROXY_ALLOWED_HOSTS.add(normalized)


def _is_loopback_host(host):
    return host in _LOOPBACK_HOSTS or host.startswith("127.")


def _allowed_proxy_host(host):
    """Return the canonical allowlist entry for *host*, or an empty string."""
    normalized = _normalise_proxy_host(host)
    if not normalized or normalized in _METADATA_HOSTS:
        return ""
    if _is_loopback_host(normalized):
        if _PROXY_ALLOW_LOOPBACK or normalized in _PROXY_ALLOWED_HOSTS:
            return normalized
        return ""
    return normalized if normalized in _PROXY_ALLOWED_HOSTS else ""


def _validated_proxy_target(url):
    """Return a reconstructed URL for an authorised proxy target.

    The host is replaced by the exact allowlist entry so the outbound
    request never carries an unvalidated hostname.

    Args:
        url: Absolute URL received from the proxy client.

    Returns:
        Safe absolute URL, or an empty string when the target is not allowed.
    """
    try:
        parts = urlsplit(url)
    except ValueError:
        return ""
    if parts.scheme not in {"http", "https"}:
        return ""
    host = _allowed_proxy_host(parts.hostname or "")
    if not host:
        return ""
    try:
        port = parts.port
    except ValueError:
        return ""
    if port is not None and not 1 <= port <= 65535:
        return ""
    netloc = f"[{host}]" if ":" in host else host
    if port is not None:
        netloc = f"{netloc}:{port}"
    return urlunsplit((parts.scheme, netloc, parts.path or "/", parts.query, ""))


def signal_handler(sig, frame):
    global should_exit
    print("\n [<-] Saliendo...")
    should_exit = True


signal.signal(signal.SIGINT, signal_handler)


class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._handle_request("GET")

    def do_POST(self):
        self._handle_request("POST")

    def _request_url(self):
        if "://" in self.path:
            return self.path
        host = self.headers.get("Host", "")
        return f"http://{host}{self.path}" if host else ""

    def _handle_request(self, method):
        url = _validated_proxy_target(self._request_url())
        if not url:
            self.send_error(403, "Proxy target not allowed")
            return
        headers = dict(self.headers)
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length else None

        _HOP_BY_HOP = frozenset(
            {
                "connection",
                "keep-alive",
                "proxy-authenticate",
                "proxy-authorization",
                "te",
                "trailer",
                "transfer-encoding",
                "upgrade",
            }
        )

        try:
            headers, body = apply_identity_to_url(url, headers, body if body else b"")
        except Exception:
            pass
        try:
            response = requests.request(method, url, headers=headers, data=body, timeout=10)
            self.send_response(response.status_code)
            for key, value in response.headers.items():
                if key.lower() in _HOP_BY_HOP:
                    continue
                if not _HEADER_SANITIZER.is_valid_name(key):
                    continue
                safe_value = _HEADER_SANITIZER.sanitize_value(value)
                if not safe_value:
                    continue
                safe_key = key.replace("\r", "").replace("\n", "").replace("\x00", "")
                safe_value = safe_value.replace("\r", "").replace("\n", "").replace("\x00", "")
                if not safe_key or not safe_value:
                    continue
                self.send_header(safe_key, safe_value)
            self.end_headers()
            self.wfile.write(response.content)
        except requests.RequestException:
            self.send_error(500, "Proxy Error")


def run_proxy(port, allowed_hosts=None):
    """Serve the intercepting proxy on loopback.

    Args:
        port: TCP port to bind.
        allowed_hosts: Hosts to authorise before serving. When omitted the
            allowlist configured by :func:`configure_proxy_allowlist` is used.
    """
    if allowed_hosts:
        configure_proxy_allowlist(allowed_hosts)
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, ProxyHandler)
    print(f"[P] Proxy ejecutándose en 127.0.0.1:{port}")
    httpd.serve_forever()


def edit_file_with_nano(content):
    with tempfile.NamedTemporaryFile(delete=False, mode="w+") as temp_file:
        temp_file.write(content)
        temp_file.flush()
        subprocess.run(["nano", temp_file.name])
        temp_file.seek(0)
        edited_content = temp_file.read()
    return edited_content


def send_request(url, method="GET", headers=None, params=None, data=None, json_data=None, proxies=None, hide_code=None):
    """
    Envía una solicitud HTTP y devuelve la respuesta.
    """
    headers = dict(headers or {})
    body_bytes = None
    if isinstance(data, (bytes, bytearray)):
        body_bytes = bytes(data)
    elif isinstance(data, str):
        body_bytes = data.encode()
    try:
        headers, body_bytes = apply_identity_to_url(url, headers, body_bytes)
    except Exception:
        pass
    if body_bytes is not None:
        data = body_bytes
    try:
        response = requests.request(
            method, url, headers=headers, params=params, data=data, json=json_data, proxies=proxies, timeout=30
        )

        if hide_code and response.status_code == hide_code:
            return None

        print(f"[S] Solicitud {method} a {url} enviada.")
        print(f"[C] Código de estado: {response.status_code}")
        print("[H] Encabezados de la respuesta:")
        print(response.headers)
        print("[R] Contenido de la respuesta:")
        print(response.text)
        return response
    except requests.RequestException as e:
        print(f"[E] Error en la solicitud: {e}")
        return None


def repeater(url, method, headers, params, data, json_data, proxies, hide_code):
    """
    Funcionalidad de Repeater que permite enviar solicitudes múltiples veces con posibilidad de modificación.
    """
    while not should_exit:
        print("[*] \n--- Nueva iteración del Repeater ---")

        headers_json = json.dumps(headers, indent=4)
        edited_headers = edit_file_with_nano(headers_json)
        headers = json.loads(edited_headers)

        data_json = json.dumps(data, indent=4)
        edited_data = edit_file_with_nano(data_json)
        data = json.loads(edited_data)

        response = send_request(url, method, headers, params, data, json_data, proxies, hide_code)
        if response is not None and response.headers.get("Content-Type") == "application/json":
            try:
                response_json = response.json()
                print("[J] Contenido de la respuesta en JSON:")
                print(json.dumps(response_json, indent=4))
            except ValueError:
                print("[e] La respuesta no es un JSON válido")

        repeat = input("[?] ¿Quieres repetir la solicitud? (s/n): ").strip().lower()
        if repeat != "s":
            print("[R] Finalizando el Repeater.")
            break


def lazyfuzz(url, method, headers, params, data, json_data, proxies, wordlist_path, hide_code):
    """
    Funcionalidad de fuzzing que reemplaza LAZYFUZZ con palabras de una wordlist.
    """
    with open(wordlist_path, "r") as f:
        words = f.read().splitlines()

    for word in words:
        if should_exit:
            break

        # Convertir los encabezados, datos y parámetros a cadenas JSON
        headers_json = json.dumps(headers)
        data_json = json.dumps(data)
        params_json = json.dumps(params)
        json_data_json = json.dumps(json_data)

        # Reemplazar LAZYFUZZ en las cadenas JSON
        headers_json = headers_json.replace("LAZYFUZZ", word)
        data_json = data_json.replace("LAZYFUZZ", word)
        params_json = params_json.replace("LAZYFUZZ", word)
        json_data_json = json_data_json.replace("LAZYFUZZ", word)

        # Convertir las cadenas JSON de nuevo a diccionarios
        headers = json.loads(headers_json)
        data = json.loads(data_json)
        params = json.loads(params_json)
        json_data = json.loads(json_data_json)

        # Reemplazar LAZYFUZZ en la URL
        fuzzed_url = url.replace("LAZYFUZZ", word)

        response = send_request(fuzzed_url, method, headers, params, data, json_data, proxies, hide_code)
        if response is not None:
            print(f"\n--- [*] Nueva iteración del Fuzzing con {word} ---")

            if response.headers.get("Content-Type") == "application/json":
                try:
                    response_json = response.json()
                    print("[J] Contenido de la respuesta en JSON:")
                    print(json.dumps(response_json, indent=4))
                except ValueError:
                    print("[e] La respuesta no es un JSON válido")


def parse_arguments():
    """
    Parsear los argumentos de la línea de comandos.
    """
    parser = argparse.ArgumentParser(description="Script HTTP Repeater y Fuzzer")
    parser.add_argument("--url", required=True, help="URL a la que se enviará la solicitud")
    parser.add_argument("--method", default="GET", help="Método HTTP (GET, POST, PUT, DELETE, etc.)")
    parser.add_argument("--headers", type=json.loads, default="{}", help="Encabezados de la solicitud en formato JSON")
    parser.add_argument("--params", type=json.loads, default="{}", help="Parámetros de la URL en formato JSON")
    parser.add_argument("--data", type=json.loads, default="{}", help="Datos del formulario en formato JSON")
    parser.add_argument(
        "--json_data", type=json.loads, default="{}", help="Datos JSON para la solicitud en formato JSON"
    )
    parser.add_argument("--proxy_port", type=int, default=8080, help="Puerto del proxy interno")
    parser.add_argument("--headers_file", help="Archivo JSON que contiene los encabezados")
    parser.add_argument("--data_file", help="Archivo JSON que contiene los datos")
    parser.add_argument("--params_file", help="Archivo JSON que contiene los parámetros de la URL")
    parser.add_argument("--json_data_file", help="Archivo JSON que contiene los datos en formato JSON")
    parser.add_argument("-w", "--wordlist", help="Ruta del diccionario para el modo fuzzing")
    parser.add_argument("-hc", "--hide_code", type=int, help="Código de estado HTTP para ocultar en la salida")

    return parser.parse_args()


def main():
    args = parse_arguments()
    configure_proxy_allowlist([args.url, *_payload_proxy_hosts()], reset=True)

    # Cargar headers y datos desde archivos JSON si se proporcionan
    headers = load_headers_from_file(args.headers_file) if args.headers_file else json.loads(args.headers)
    data = load_data_from_file(args.data_file) if args.data_file else json.loads(args.data)
    params = load_data_from_file(args.params_file) if args.params_file else json.loads(args.params)
    json_data = load_data_from_file(args.json_data_file) if args.json_data_file else json.loads(args.json_data)

    # Iniciar el proxy en segundo plano
    proxy_thread = threading.Thread(target=run_proxy, args=(args.proxy_port,), daemon=True)
    proxy_thread.start()

    proxies = {"http": f"http://localhost:{args.proxy_port}", "https": f"http://localhost:{args.proxy_port}"}

    print(f"[P] Configuración del proxy: {proxies}")

    if args.wordlist:
        lazyfuzz(args.url, args.method, headers, params, data, json_data, proxies, args.wordlist, args.hide_code)
    else:
        repeater(args.url, args.method, headers, params, data, json_data, proxies, args.hide_code)


if __name__ == "__main__":
    main()
