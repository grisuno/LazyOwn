import argparse
import binascii
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def pad(s):
    return s + b'\0' * (AES.block_size - len(s) % AES.block_size)

def encrypt(plaintext, key):
    plaintext = pad(plaintext)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(plaintext)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b'\0')

def generate_key(length=16):
    return get_random_bytes(length)

def main():
    parser = argparse.ArgumentParser(description="AES Encryption/Decryption")
    parser.add_argument("message", help="The message to encrypt")
    args = parser.parse_args()

    key = generate_key()
    print(f"Clave AES generada (hex): {binascii.hexlify(key).decode()}")

    plaintext = args.message.encode()
    ciphertext = encrypt(plaintext, key)
    print(f"Texto cifrado (hex): {binascii.hexlify(ciphertext).decode()}")

    decrypted_text = decrypt(ciphertext, key)
    print(f"Texto descifrado: {decrypted_text.decode()}")

if __name__ == "__main__":
    main()
