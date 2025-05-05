package main

import (
	"bytes"
	"compress/zlib"
	"encoding/binary"
	"hash/crc32"
	"image"
	"log"
	"os"
	"syscall"
	"unsafe"
)

// ======================
// 1. Definiciones de Windows API
// ======================
var (
	user32                  = syscall.NewLazyDLL("user32.dll")
	gdi32                   = syscall.NewLazyDLL("gdi32.dll")
	procGetDC               = user32.NewProc("GetDC")
	procReleaseDC           = user32.NewProc("ReleaseDC")
	procGetSystemMetrics    = user32.NewProc("GetSystemMetrics")
	procGetWindowDC         = user32.NewProc("GetWindowDC")
	procCreateCompatibleDC  = gdi32.NewProc("CreateCompatibleDC")
	procCreateCompatibleBitmap = gdi32.NewProc("CreateCompatibleBitmap")
	procSelectObject        = gdi32.NewProc("SelectObject")
	procBitBlt             = gdi32.NewProc("BitBlt")
	procGetDIBits          = gdi32.NewProc("GetDIBits")
	procDeleteObject       = gdi32.NewProc("DeleteObject")
)

type BITMAPINFOHEADER struct {
	BiSize          uint32
	BiWidth         int32
	BiHeight        int32
	BiPlanes        uint16
	BiBitCount      uint16
	BiCompression   uint32
	BiSizeImage     uint32
	BiXPelsPerMeter int32
	BiYPelsPerMeter int32
	BiClrUsed       uint32
	BiClrImportant  uint32
}

type BITMAPINFO struct {
	BmiHeader BITMAPINFOHEADER
	BmiColors [3]uint32
}

// ======================
// 2. Captura de pantalla
// ======================
func captureScreen() (*image.RGBA, error) {
	// Obtener dimensiones de la pantalla
	smXVirtualScreen, _, _ := procGetSystemMetrics.Call(76)
	smYVirtualScreen, _, _ := procGetSystemMetrics.Call(77)
	smCxVirtualScreen, _, _ := procGetSystemMetrics.Call(78)
	smCyVirtualScreen, _, _ := procGetSystemMetrics.Call(79)

	width := int(smCxVirtualScreen)
	height := int(smCyVirtualScreen)

	// Crear DC y bitmap
	hdc, _, _ := procGetWindowDC.Call(0)
	defer procReleaseDC.Call(0, hdc)

	memdc, _, _ := procCreateCompatibleDC.Call(hdc)
	defer procDeleteObject.Call(memdc)

	bitmap, _, _ := procCreateCompatibleBitmap.Call(hdc, uintptr(width), uintptr(height))
	defer procDeleteObject.Call(bitmap)

	procSelectObject.Call(memdc, bitmap)
	procBitBlt.Call(memdc, 0, 0, uintptr(width), uintptr(height), hdc, uintptr(smXVirtualScreen), uintptr(smYVirtualScreen), 0x00CC0020) // SRCCOPY

	// Obtener bits de la imagen
	bmi := BITMAPINFO{
		BmiHeader: BITMAPINFOHEADER{
			BiSize:        uint32(unsafe.Sizeof(BITMAPINFOHEADER{})),
			BiWidth:       int32(width),
			BiHeight:      -int32(height), // Negativo para top-down
			BiPlanes:      1,
			BiBitCount:    24,
			BiCompression: 0, // BI_RGB
		},
	}

	buffer := make([]byte, width*height*3)
	procGetDIBits.Call(
		memdc,
		bitmap,
		0,
		uintptr(height),
		uintptr(unsafe.Pointer(&buffer[0])),
		uintptr(unsafe.Pointer(&bmi)),
		0,
	)

	// Convertir BGR a RGB
	for i := 0; i < len(buffer); i += 3 {
		buffer[i], buffer[i+2] = buffer[i+2], buffer[i]
	}

	// Crear imagen RGBA
	img := image.NewRGBA(image.Rect(0, 0, width, height))
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			pos := (y*width + x) * 3
			img.SetRGBA(x, y, image.RGBA{
				R: buffer[pos],
				G: buffer[pos+1],
				B: buffer[pos+2],
				A: 255,
			})
		}
	}

	return img, nil
}

// ======================
// 3. Guardar como PNG (igual que antes)
// ======================
func savePNG(img *image.RGBA, filename string) error {
	// ... (usa la misma implementación PNG que compartí anteriormente) ...
}

func main() {
	img, err := captureScreen()
	if err != nil {
		log.Fatal("Error capturando pantalla:", err)
	}

	if err := savePNG(img, "screenshot.png"); err != nil {
		log.Fatal("Error guardando PNG:", err)
	}
	log.Println("Captura guardada como screenshot.png")
}