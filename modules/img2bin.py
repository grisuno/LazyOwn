from PIL import Image
import numpy as np
import sys

def imagen_a_binario(imagen_input, binario_output, block_size=4):
    # Carga la imagen
    img = Image.open(imagen_input)
    img = img.convert('RGB')
    imagen = np.array(img)

    # Separa la capa de redundancia de la imagen original
    alto, ancho, _ = imagen.shape
    redundancia_alto = (len(imagen) // ancho) // 3
    redundancia = imagen[-redundancia_alto:, :, 0]

    # Extrae los datos de la imagen usando los bits menos significativos
    datos_binarios = ''
    for y in range(alto - redundancia_alto):
        for x in range(ancho):
            for c in range(3):  # RGB
                bit = imagen[y, x, c] & 1
                datos_binarios += str(bit)

    # Verifica la redundancia
    for y in range(0, redundancia_alto, block_size):
        for x in range(0, ancho, block_size):
            bit_redundancia = np.mean(redundancia[y:y+block_size, x:x+block_size]) > 127
            if bit_redundancia != int(datos_binarios[y//block_size * (ancho//block_size) + x//block_size]):
                print(f"Error de redundancia en el bloque ({y},{x})")

    # Convierte los bits a bytes
    byte_data = bytearray()
    for i in range(0, len(datos_binarios), 8):
        byte_data.append(int(datos_binarios[i:i+8], 2))

    # Guarda los datos en un archivo binario
    with open(binario_output, 'wb') as f:
        f.write(byte_data)

def main():
    if len(sys.argv) < 3:
        print("Uso: python script.py <imagen_input> <binario_output>")
        sys.exit(1)

    imagen_input = sys.argv[1]
    binario_output = sys.argv[2]

    imagen_a_binario(imagen_input, binario_output)
    print(f"Binario extraído de la imagen y guardado como {binario_output}")

if __name__ == "__main__":
    main()
