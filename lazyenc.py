import os
import argparse
import getpass
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64

def derive_key(password: str, salt: bytes = b'lazyown_salt') -> bytes:
    """
    Derive an AES key from the password using PBKDF2.

    Args:
        password (str): The user-provided password.
        salt (bytes): Salt for key derivation. Defaults to b'lazyown_salt'.

    Returns:
        bytes: Base64-encoded key suitable for Fernet.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_directory(directory: str, cipher: Fernet, exclude_files: list) -> None:
    """
    Encrypt all files in the specified directory.

    Args:
        directory (str): Path to the directory to encrypt.
        cipher (Fernet): Fernet cipher instance for encryption.
        exclude_files (list): List of file paths to exclude from encryption.

    Raises:
        Exception: If encryption fails for any file.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path in exclude_files:
                continue
            try:
                with open(file_path, 'rb') as f:
                    data = f.read()
                encrypted_data = cipher.encrypt(data)
                with open(file_path, 'wb') as f:
                    f.write(encrypted_data)
                print(f"Encrypted: {file_path}")
            except Exception as e:
                print(f"Error encrypting {file_path}: {e}")

def decrypt_directory(directory: str, cipher: Fernet, exclude_files: list) -> None:
    """
    Decrypt all files in the specified directory.

    Args:
        directory (str): Path to the directory to decrypt.
        cipher (Fernet): Fernet cipher instance for decryption.
        exclude_files (list): List of file paths to exclude from decryption.

    Raises:
        InvalidToken: If the decryption key is incorrect.
        Exception: If decryption fails for any file.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path in exclude_files:
                continue
            try:
                with open(file_path, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = cipher.decrypt(encrypted_data)
                with open(file_path, 'wb') as f:
                    f.write(decrypted_data)
                print(f"Decrypted: {file_path}")
            except InvalidToken:
                print(f"Invalid key for {file_path}")
                raise
            except Exception as e:
                print(f"Error decrypting {file_path}: {e}")

def main():
    """
    Main function to encrypt or decrypt a directory using a password-derived key.

    Parses command-line arguments for action, directory, and optional key file.
    Prompts for a password and performs the requested operation.
    """
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a LazyOwn directory")
    parser.add_argument('action', choices=['encrypt', 'decrypt'], help="Action to perform")
    parser.add_argument('--directory', required=True, help="Path to the LazyOwn directory")
    parser.add_argument('--key-file', help="Path to the AES key file (optional)")
    args = parser.parse_args()

    # Validate directory
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory")
        exit(1)

    exclude_files = [os.path.abspath(__file__)] 
    if args.key_file:
        exclude_files.append(os.path.abspath(args.key_file))

    password = getpass.getpass("Enter the password: ")
    key = derive_key(password)
    cipher = Fernet(key)

    try:
        if args.action == 'decrypt':
            decrypt_directory(args.directory, cipher, exclude_files)
            print("Directory decrypted successfully. You can now work with LazyOwn.")
            print("Remember to encrypt the directory after your session.")
        elif args.action == 'encrypt':
            encrypt_directory(args.directory, cipher, exclude_files)
            print("Directory encrypted successfully.")
    except InvalidToken:
        print("Incorrect password. Decryption failed.")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()