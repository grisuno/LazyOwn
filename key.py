import os
from rich.console import Console
from rich.prompt import Confirm
from rich.spinner import Spinner

console = Console()

def main():
    path = os.getcwd()
    path = f"{path}/sessions"
    key_path = f"{path}/key.aes"

    if os.path.exists(key_path):
        console.print("The AES key file already exists. If you replace the key, the old implants, they may not work properly", style="bold yellow")
        should_replace = Confirm.ask("Do you want to replace the existing key?", default=False)

        if should_replace:
            with Spinner("Generating new AES key...", style="bold green") as spinner:
                AES_KEY = os.urandom(32)
                with open(key_path, 'wb') as f:
                    f.write(AES_KEY)
                spinner.update("AES key replaced successfully!")
  
        else:
            console.print("Exiting without replacing the key.", style="bold red")
    else:
        with Spinner("Generating new AES key...", style="bold green") as spinner:
            AES_KEY = os.urandom(32)
            with open(key_path, 'wb') as f:
                f.write(AES_KEY)
            spinner.update("AES key generated successfully!")
       

if __name__ == "__main__":
    main()
