import os
from pwn import *
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad
import argparse
from rich.console import Console
from rich.prompt import Confirm
from rich.spinner import Spinner
import binascii

console = Console()

def generate_key_iv(sessions_path="./sessions"):
    os.makedirs(sessions_path, exist_ok=True)
    key_path = os.path.join(sessions_path, "key.aes")
    iv_path = os.path.join(sessions_path, "iv.aes")

    replace = False
    if os.path.exists(key_path):
        console.print("The AES key file already exists. If you replace the key, the old implants, they may not work properly", style="bold yellow")
        replace = Confirm.ask("Do you want to replace the existing key?", default=False)
    elif os.path.exists(iv_path):
        console.print("The AES IV file already exists.", style="yellow")
        if not replace:
            replace = Confirm.ask("Do you want to replace the existing IV?", default=replace)
    else:
        replace = True

    if replace or not os.path.exists(key_path) or not os.path.exists(iv_path):
        with console.status("Generating new AES key and IV...", spinner="dots") as status:
            try:
                aes_key = os.urandom(32)
                with open(key_path, 'wb') as f:
                    f.write(aes_key)
                aes_iv = os.urandom(16)
                with open(iv_path, 'wb') as f:
                    f.write(aes_iv)
                status.update("AES key and IV generated successfully!")
                console.print(f"AES Key (Hex): {binascii.hexlify(aes_key).decode()}", style="bold magenta")
                console.print(f"AES IV (Hex): {binascii.hexlify(aes_iv).decode()}", style="bold cyan")
                return key_path, iv_path
            except Exception as e:
                status.update(f"[bold red]Error generating keys: {e}[/bold red]")
                return key_path, iv_path # Return even on error to try other parts of the script
    else:
        console.print("Using existing AES key and IV.", style="bold cyan")
        with open(key_path, "rb") as f:
            key = f.read()
        with open(iv_path, "rb") as f:
            iv = f.read()
        console.print(f"AES Key (Hex): {binascii.hexlify(key).decode()}", style="bold magenta")
        console.print(f"AES IV (Hex): {binascii.hexlify(iv).decode()}", style="bold cyan")
        return key_path, iv_path

def main():
    parser = argparse.ArgumentParser(description="Extract and encrypt shellcode from an ELF file.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input ELF file.")
    parser.add_argument("-o", "--output", required=True, help="Path to save the encrypted shellcode.")
    args = parser.parse_args()

    sessions_path = "./sessions"
    key_file, iv_file = generate_key_iv(sessions_path)

    try:
    
        with open(key_file, "rb") as f:
            key = f.read()
        with open(iv_file, "rb") as f:
            iv = f.read()

    
        elf = ELF(args.input)
        text_section = elf.section(b'.text')

        if text_section:
            shellcode = text_section.data

        
            cipher = AES.new(key, AES.MODE_CFB, iv)
            encrypted_shellcode = iv + cipher.encrypt(shellcode)

        
            with open(args.output, "wb") as f:
                f.write(encrypted_shellcode)

            console.print(f"Shellcode extraído, cifrado con AES-CFB y guardado en '{args.output}'.", style="bold green")

        else:
            console.print(f"Error: Sección .text no encontrada en '{args.input}'.", style="bold red")

    except FileNotFoundError as e:
        console.print(f"Error: El archivo '{e.filename}' no fue encontrado.", style="bold red")
    except Exception as e:
        console.print(f"Ocurrió un error: {e}", style="bold red")

if __name__ == "__main__":
    main()