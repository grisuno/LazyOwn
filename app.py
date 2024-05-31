import os
import subprocess
import shlex
from cmd import Cmd

BANNER = """
██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
[*] Iniciando: Framework [;,;]
"""
print(BANNER)

class LazyOwnShell(Cmd):
    prompt = "LazyOwn> "
    intro = "Welcome to the LazyOwn interactive shell! Type ? to list commands"

    def __init__(self):
        super().__init__()
        self.params = {
            "binary_name": None,
            "target_ip": "127.0.0.1",
            "api_key": None,
            "prompt": None,
            "url": None,
            "method": "GET",
            "headers": "{}",
            "params": "{}",
            "data": "{}",
            "json_data": "{}",
            "proxy_port": 8080,
            "wordlist": None,
            "hide_code": None,
            "mode": None,
            "attacker_ip": None,
            "reverse_shell_ip": None,
            "reverse_shell_port": None
        }

    def do_set(self, line):
        """ Set a parameter value. Usage: set <parameter> <value> """
        args = shlex.split(line)
        if len(args) != 2:
            print("[?] Usage: set <parameter> <value>")
            return

        param, value = args
        if param in self.params:
            self.params[param] = value
            print(f"[SET] {param} set to {value}")
        else:
            print(f"[?] Unknown parameter: {param}")

    def do_show(self, line):
        """ Show the current parameter values """
        for param, value in self.params.items():
            print(f"{param}: {value}")

    def do_run(self, line):
        """ Run a specific LazyOwn script """
        args = shlex.split(line)
        if not args:
            print("[?] Usage: run <script_name>")
            return

        script_name = args[0]
        if script_name == "lazysearch":
            self.run_lazysearch()
        elif script_name == "lazysearch_gui":
            self.run_lazysearch_gui()
        elif script_name == "lazyown":
            self.run_lazyown()
        elif script_name == "update_db":
            self.run_update_db()
        elif script_name == "lazynmap":
            self.run_lazynmap()
        elif script_name == "lazygptcli":
            self.run_lazygptcli()
        elif script_name == "lazyburpfuzzer":
            self.run_lazyburpfuzzer()
        elif script_name == "lazyreverse_shell":
            self.run_lazyreverse_shell()
        elif script_name == "lazyattack":
            self.run_lazyattack()
        else:
            print(f"Unknown script: {script_name}")

    def run_lazysearch(self):
        binary_name = self.params["binary_name"]
        if not binary_name:
            print("[?] binary_name not set")
            return
        self.run_script("lazysearch.py", binary_name)

    def run_lazysearch_gui(self):
        self.run_script("LazyOwnExplorer.py")

    def run_lazyown(self):
        self.run_script("lazyown.py")

    def run_update_db(self):
        os.chdir("LazyOwn")
        os.system("rm *.csv")
        os.system("rm *.parquet")
        os.system("./update_db.sh")
        os.chdir("..")

    def run_lazynmap(self):
        target_ip = self.params["target_ip"]
        os.system(f"./lazynmap.sh -t {target_ip}")

    def run_lazygptcli(self):
        prompt = self.params["prompt"]
        api_key = self.params["api_key"]
        if not prompt or not api_key:
            print("[?] prompt and api_key must be set")
            return
        os.environ["GROQ_API_KEY"] = api_key
        self.run_script("lazygptcli.py", "--prompt", prompt)

    def run_lazyburpfuzzer(self):
        url = self.params["url"]
        method = self.params["method"]
        headers = self.params["headers"]
        params = self.params["params"]
        data = self.params["data"]
        json_data = self.params["json_data"]
        proxy_port = self.params["proxy_port"]
        wordlist = self.params["wordlist"]
        hide_code = self.params["hide_code"]

        command = [
            "python3", "lazyown_bprfuzzer.py",
            "--url", url,
            "--method", method,
            "--headers", headers,
            "--params", params,
            "--data", data,
            "--json_data", json_data,
            "--proxy_port", str(proxy_port)
        ]
        if wordlist:
            command.extend(["-w", wordlist])
        if hide_code:
            command.extend(["-hc", str(hide_code)])

        self.run_command(command)

    def run_lazyreverse_shell(self):
        ip = self.params["reverse_shell_ip"]
        port = self.params["reverse_shell_port"]
        if not ip or not port:
            print("[?] reverse_shell_ip and reverse_shell_port must be set")
            return
        os.system(f"./lazyreverse_shell.sh --ip {ip} --puerto {port}")

    def run_lazyattack(self):
        mode = self.params["mode"]
        target_ip = self.params["target_ip"]
        attacker_ip = self.params["attacker_ip"]
        if not mode or not target_ip or not attacker_ip:
            print("[?] mode, target_ip, and attacker_ip must be set")
            return
        os.system(f"./lazyatack.sh --modo {mode} --ip {target_ip} --atacante {attacker_ip}")

    def run_script(self, script_name, *args):
        """ Run a script with the given arguments """
        command = ["python3", script_name] + list(args)
        self.run_command(command)

    def run_command(self, command):
        """ Run a command and print output in real-time """
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            for line in iter(process.stdout.readline, ''):
                print(line, end='')
            for line in iter(process.stderr.readline, ''):
                print(line, end='')
            process.stdout.close()
            process.stderr.close()
            process.wait()
        except KeyboardInterrupt:
            process.terminate()
            process.wait()
            print("\n[Interrupted] Process terminated")

    def do_exit(self, line):
        """ Exit the LazyOwn shell """
        return True

if __name__ == "__main__":
    LazyOwnShell().cmdloop()
