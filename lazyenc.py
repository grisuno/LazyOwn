import argparse
import base64
import getpass
import os
import secrets

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT_FILE = ".lazyown_salt"


def _generate_salt() -> bytes:
    """Generate a cryptographically random 16-byte salt."""
    return secrets.token_bytes(16)


def _load_or_create_salt(directory: str) -> bytes:
    """
    Load the salt file from the target directory or create one.

    Stores the salt in a hidden file inside the directory so decryption
    can recover the same salt. If the directory is encrypted, the salt
    file is encrypted along with everything else; during decryption the
    file must be excluded from processing.

    Args:
        directory: Path to the target directory.

    Returns:
        bytes: 16-byte cryptographic salt.
    """
    salt_path = os.path.join(directory, SALT_FILE)
    if os.path.isfile(salt_path):
        with open(salt_path, "rb") as f:
            raw = f.read()
            if len(raw) >= 16:
                return raw[:16]
    return _generate_salt()


def derive_key(password: str, salt: bytes | None = None) -> bytes:
    """
    Derive an AES key from the password using PBKDF2HMAC.

    Args:
        password: The user-provided password.
        salt: 16-byte salt for key derivation. When None, a random salt
              is generated per call (not recommended for encryption that
              needs to be reversed — use _load_or_create_salt instead).

    Returns:
        bytes: Base64-encoded key suitable for Fernet.
    """
    if salt is None:
        salt = _generate_salt()
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

    On encrypt, a per-directory salt is generated and persisted as
    ``.lazyown_salt`` inside the directory so decryption can recover the
    same salt.
    """
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a LazyOwn directory")
    parser.add_argument('action', choices=['encrypt', 'decrypt'], help="Action to perform")
    parser.add_argument('--directory', required=True, help="Path to the LazyOwn directory")
    parser.add_argument('--key-file', help="Path to the AES key file (optional)")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory")
        exit(1)

    exclude_files = [os.path.abspath(__file__)]
    if args.key_file:
        exclude_files.append(os.path.abspath(args.key_file))

    salt_path = os.path.join(args.directory, SALT_FILE)
    salt = _load_or_create_salt(args.directory)

    if args.action == 'encrypt':
        salt = _generate_salt()
        with open(salt_path, "wb") as f:
            f.write(salt)

    exclude_files.append(os.path.abspath(salt_path))

    password = getpass.getpass("Enter the password: ")
    key = derive_key(password, salt=salt)
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
