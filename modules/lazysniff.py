import os
import sys
import curses
from scapy.all import sniff, wrpcap, hexdump, Ether, IP, UDP, TCP
import argparse
import signal
import threading
import time

BANNER = """
██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝ ╚═╝ ╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
[*] Iniciando: LazyOwn Sniffer [;,;]
"""

# Verificar y relanzar con sudo si es necesario
def check_sudo():
    if os.geteuid() != 0:
        print("[S] Este script necesita permisos de superusuario. Relanzando con sudo...")
        args = ['sudo', sys.executable] + sys.argv
        os.execvpe('sudo', args, os.environ)

check_sudo()

# Manejar la interrupción de Ctrl+C
def signal_handler(sig, frame):
    print('\n [->] Captura interrumpida.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Configuración de la interfaz ncurses
def setup_curses():
    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr

# Restaurar la configuración de la terminal al salir
def restore_curses(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

# Función para mostrar el banner
def show_banner(stdscr, banner):
    stdscr.clear()
    stdscr.addstr(0, 0, banner)
    stdscr.refresh()
    time.sleep(3)  # Esperar 3 segundos antes de continuar

# Función para procesar y mostrar cada paquete capturado
def process_packet(packet, packets, stdscr):
    packets.append(packet)
    stdscr.clear()
    stdscr.addstr(0, 0, "[P] Paquetes capturados: {}".format(len(packets)))
    for i, pkt in enumerate(packets):
        stdscr.addstr(i + 1, 0, "{}".format(pkt.summary()[:curses.COLS - 1]))
    stdscr.refresh()

# Función para analizar un paquete y extraer información detallada
def analyze_packet(packet):
    details = []

    if Ether in packet:
        eth = packet[Ether]
        details.append(f"[E] Ethernet: {eth.src} -> {eth.dst} (Type: {eth.type})")

    if IP in packet:
        ip = packet[IP]
        details.append(f"[I] IP: {ip.src} -> {ip.dst} (Proto: {ip.proto}, TTL: {ip.ttl})")

    if UDP in packet:
        udp = packet[UDP]
        details.append(f"[U] UDP: {udp.sport} -> {udp.dport} (Len: {udp.len})")

    if TCP in packet:
        tcp = packet[TCP]
        details.append(f"[T] TCP: {tcp.sport} -> {tcp.dport} (Flags: {tcp.flags})")

    return details

# Función principal de captura de paquetes
def capture_packets(interface, count, filter, pcap_file, packets, stdscr):
    sniff(iface=interface, filter=filter, prn=lambda x: process_packet(x, packets, stdscr), count=count)
    if pcap_file:
        wrpcap(pcap_file, packets)

# Función principal de la interfaz ncurses con scrolling
def main_curses(stdscr, packets):
    idx = 0
    start_idx = 0
    h_offset = 0
    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        try:
            stdscr.addstr(0, 0, "[P] Paquetes capturados: {}".format(len(packets)))
            if packets:
                display_packets = packets[start_idx:start_idx + max_y - 4]
                for i, pkt in enumerate(display_packets):
                    if i == idx - start_idx:
                        stdscr.addstr(i + 1, 0, "{}".format(pkt.summary()[h_offset:h_offset + max_x - 1]), curses.A_REVERSE)
                    else:
                        stdscr.addstr(i + 1, 0, "{}".format(pkt.summary()[h_offset:h_offset + max_x - 1]))

                details = analyze_packet(packets[idx])
                for j, detail in enumerate(details):
                    if len(display_packets) + 2 + j >= max_y - 3:
                        break
                    stdscr.addstr(len(display_packets) + 2 + j, 0, detail[h_offset:h_offset + max_x - 1])

                stdscr.addstr(len(display_packets) + 2 + len(details), 0, "[C] Contenido del paquete:")
                hexdump_lines = hexdump(packets[idx], dump=True).split('\n')
                for k, line in enumerate(hexdump_lines):
                    if len(display_packets) + 3 + len(details) + k >= max_y - 1:
                        break
                    stdscr.addstr(len(display_packets) + 3 + len(details) + k, 0, line[h_offset:h_offset + max_x - 1])
            
            stdscr.addstr(max_y - 1, 0, "[?] Usa las flechas arriba/abajo para navegar, izquierda/derecha para desplazamiento horizontal, 'q' para salir.")
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord('q'):
                break
            elif key == curses.KEY_UP:
                if idx > 0:
                    idx -= 1
                if idx < start_idx:
                    start_idx -= 1
            elif key == curses.KEY_DOWN:
                if idx < len(packets) - 1:
                    idx += 1
                if idx >= start_idx + max_y - 4:
                    start_idx += 1
            elif key == curses.KEY_LEFT:
                if h_offset > 0:
                    h_offset -= 1
            elif key == curses.KEY_RIGHT:
                h_offset += 1
        except curses.error:
            pass

# Argumentos de la línea de comandos
def parse_arguments():
    parser = argparse.ArgumentParser(description="Captura de paquetes en la terminal con navegación.")
    parser.add_argument('-i', '--interface', type=str, required=True, help='Interfaz de red para la captura de paquetes')
    parser.add_argument('-c', '--count', type=int, default=0, help='Número de paquetes a capturar (0 para infinito)')
    parser.add_argument('-f', '--filter', type=str, default="", help='Filtro BPF (opcional)')
    parser.add_argument('-p', '--pcap', type=str, default="", help='Nombre del archivo pcap para guardar')
    return parser.parse_args()

# Función principal
def main():
    args = parse_arguments()
    packets = []

    stdscr = setup_curses()
    try:
        show_banner(stdscr, BANNER)  # Mostrar el banner antes de empezar la captura
        pcap_file = os.path.join("pcaps", args.pcap if args.pcap else "capture.pcap")
        os.makedirs("pcaps", exist_ok=True)
        capture_thread = threading.Thread(target=capture_packets, args=(args.interface, args.count, args.filter, pcap_file, packets, stdscr))
        capture_thread.daemon = True
        capture_thread.start()
        main_curses(stdscr, packets)
    finally:
        restore_curses(stdscr)

if __name__ == '__main__':
    main()
