import os
import time
from rich.console import Console
from rich.prompt import Confirm


console = Console()

def main():
    path = os.getcwd()
    sessions_path = f"{path}/sessions"
    if not os.path.exists(sessions_path):
        os.makedirs(sessions_path)
        console.print(f"Created directory: [bold cyan]{sessions_path}[/bold cyan]")

    key_path = f"{sessions_path}/key.aes"

    if os.path.exists(key_path):
        console.print("The AES key file already exists. If you replace the key, the old implants, they may not work properly", style="bold yellow")
        should_replace = Confirm.ask("Do you want to replace the existing key?", default=False)
        if should_replace:
            with console.status("[bold green]Generating new AES key...[/bold green]", spinner="dots") as status:
                AES_KEY = os.urandom(32)
                with open(key_path, 'wb') as f:
                    f.write(AES_KEY)
                status.update("[bold green]AES key replaced successfully![/bold green]", spinner="dots")
                time.sleep(1)
        else:
            console.print("Exiting without replacing the key.", style="bold red")
    else:
        with console.status("[bold green]Generating new AES key...[/bold green]", spinner="dots") as status:
            AES_KEY = os.urandom(32)
            with open(key_path, 'wb') as f:
                f.write(AES_KEY)
            status.update("[bold green]AES key generated successfully![/bold green]", spinner="dots")
            time.sleep(1)

if __name__ == "__main__":
    main()
