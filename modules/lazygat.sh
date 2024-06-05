#!/bin/bash

# Verifica si se está ejecutando como root
if [ "$EUID" -ne 0 ]; then
  echo "Por favor, ejecute este script como root."
  exit 1
fi

# Directorio de salida
output_dir="system_info"
mkdir -p $output_dir

echo "Gathering system information..."

# Información del sistema operativo
echo "Recolectando información del sistema operativo..."
uname -a > $output_dir/os_info.txt
cat /etc/os-release >> $output_dir/os_info.txt

# Información del hardware
echo "Recolectando información del hardware..."
lscpu > $output_dir/cpu_info.txt
lsblk > $output_dir/block_devices.txt
lspci > $output_dir/pci_devices.txt
lsusb > $output_dir/usb_devices.txt
dmidecode > $output_dir/dmi_info.txt

# Información de la memoria
echo "Recolectando información de la memoria..."
free -h > $output_dir/memory_info.txt
vmstat -s > $output_dir/vmstat_info.txt

# Información de la red
echo "Recolectando información de la red..."
ip a > $output_dir/ip_info.txt
ip route > $output_dir/route_info.txt
ss -tuln > $output_dir/listening_ports.txt
iptables -L > $output_dir/iptables_info.txt

# Información del almacenamiento
echo "Recolectando información del almacenamiento..."
df -h > $output_dir/disk_usage.txt
mount > $output_dir/mount_info.txt

# Información de los procesos y servicios
echo "Recolectando información de los procesos y servicios..."
ps aux > $output_dir/processes.txt
systemctl list-units --type=service > $output_dir/services.txt

# Información de los usuarios
echo "Recolectando información de los usuarios..."
cut -d: -f1 /etc/passwd > $output_dir/users.txt
cut -d: -f1 /etc/group > $output_dir/groups.txt
last > $output_dir/last_logins.txt
who > $output_dir/current_logins.txt

# Información de los paquetes instalados
echo "Recolectando información de los paquetes instalados..."
if [ -x "$(command -v dpkg)" ]; then
  dpkg -l > $output_dir/installed_packages.txt
elif [ -x "$(command -v rpm)" ]; then
  rpm -qa > $output_dir/installed_packages.txt
fi

# Información del kernel
echo "Recolectando información del kernel..."
uname -r > $output_dir/kernel_version.txt
lsmod > $output_dir/kernel_modules.txt

# Información del entorno
echo "Recolectando información del entorno..."
env > $output_dir/environment_variables.txt

# Recolección de información de /proc
proc_dir="$output_dir/proc"
mkdir -p $proc_dir

echo "Recolectando información de /proc..."

# Información de la CPU
echo "Recolectando información de la CPU..."
cp /proc/cpuinfo $proc_dir/cpuinfo.txt

# Información de la memoria
echo "Recolectando información de la memoria..."
cp /proc/meminfo $proc_dir/meminfo.txt

# Información del sistema
echo "Recolectando información del sistema..."
cp /proc/version $proc_dir/version.txt
cp /proc/uptime $proc_dir/uptime.txt
cp /proc/loadavg $proc_dir/loadavg.txt

# Información de la red
echo "Recolectando información de la red..."
cp /proc/net/dev $proc_dir/net_dev.txt
cp /proc/net/tcp $proc_dir/net_tcp.txt
cp /proc/net/udp $proc_dir/net_udp.txt
cp /proc/net/raw $proc_dir/net_raw.txt
cp /proc/net/arp $proc_dir/net_arp.txt
cp /proc/net/route $proc_dir/net_route.txt

# Información de los procesos
echo "Recolectando información de los procesos..."
ps aux > $proc_dir/processes.txt

# Información del sistema de archivos montados
echo "Recolectando información del sistema de archivos montados..."
cp /proc/mounts $proc_dir/mounts.txt

# Información de los módulos del kernel
echo "Recolectando información"