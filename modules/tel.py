import requests
import re
import uuid
import json
from Crypto.Cipher import AES
from datetime import datetime

def get_machine_id():
    try:
        with open('/etc/machine-id', 'r') as f:
            machine_id = f.read().strip()
            if machine_id:
                return machine_id
    except FileNotFoundError:
        machine_id = uuid.uuid4()
        return machine_id
    except Exception as e:
        print(f"Error leyendo /etc/machine-id: {e}")
    return None
def get_version():
    try:
        with open('version.json', 'r') as f:
            data = json.load(f)
            return data.get("version", "no version found")
    except FileNotFoundError:
        return "no version found"
    except Exception as e:
        print(f"Error leyendo version.json: {e}")
        return "no version found"
    
def to_numbers(hex_str):
    """Simula la función toNumbers de JavaScript"""
    return [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]

def to_hex(byte_list):
    """Simula la función toHex de JavaScript"""
    return ''.join(f'{b:02x}' for b in byte_list)

def decrypt_cookie(encrypted, key, iv):
    """Descifra usando AES en modo CBC (como slowAES.decrypt(c,2,a,b))"""
    cipher = AES.new(bytes(key), AES.MODE_CBC, bytes(iv))
    decrypted = cipher.decrypt(bytes(encrypted))
    return decrypted

def main():
    """Sistema de telemetría de uso por instalación no invasiva."""
    mi_uuid = get_machine_id()
    fecha_hora_actual = datetime.now()
    url = "https://lazyown.ct.ws/grisiscomebackeslacumbia.php"
    ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    version = get_version()
    params = {
        "id": mi_uuid,
        "version": version,
        "date": fecha_hora_actual
    }

    session = requests.Session()

    response = session.get(url, params=params, headers={
        "User-Agent": ua
    })

    html = response.text
    match_a = re.search(r'a=toNumbers\("([^"]+)"\)', html)
    match_b = re.search(r'b=toNumbers\("([^"]+)"\)', html)
    match_c = re.search(r'c=toNumbers\("([^"]+)"\)', html)

    if not (match_a and match_b and match_c):
        exit(1)

    a_hex = match_a.group(1)
    b_hex = match_b.group(1)
    c_hex = match_c.group(1)

    key = to_numbers(a_hex)
    iv = to_numbers(b_hex)
    enc = to_numbers(c_hex)

    decrypted = decrypt_cookie(enc, key, iv)
    cookie_value = to_hex(decrypted).lower()

    session.cookies.set("__test", cookie_value, path="/")

    final_url = f"{url}?id={params['id']}&version={params['version']}&date={params['date']}"
    session.get(final_url, headers={
        "User-Agent": ua
    })
if __name__ == "__main__":
    main()