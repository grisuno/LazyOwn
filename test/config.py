# conftest.py o config.py
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# === CONFIGURACIÓN ===
C2_URL = "https://10.10.14.91:4444"
C2_USER = "LazyOwn"
C2_PASS = "LazyOwn"
MALEABLE = "/pleasesubscribe/v1/users/"
CLIENT_ID = "windows"
AES_KEY_HEX = "36870130f03bf0bba5c8ed1d3e27117891ab415c5ea6cdbcb8731ef8fc218124"
AES_KEY = bytes.fromhex(AES_KEY_HEX)
# En config.py
TEST_LATENCY_TIME = 5


backend = default_backend()

# === FUNCIONES DE CIFRADO/DESCIFRADO (iguales al C2) ===
def encrypt_data(data: bytes) -> str:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    combined = iv + encrypted_data
    return base64.b64encode(combined).decode('utf-8')

def decrypt_data(b64_data: str) -> str:
    encrypted_data = base64.b64decode(b64_data)
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted.decode('utf-8')
