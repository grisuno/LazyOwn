from PIL import Image
import numpy as np
import sys

def binario_a_imagen(binario, imagen_input, imagen_output, block_size=4):
    # Lee los datos del archivo binario
    with open(binario, 'rb') as f:
        datos = f.read()

    # Convierte los datos en una cadena de bits
    datos_binarios = ''.join(format(byte, '08b') for byte in datos)
    datos_binarios += '0' * ((8 - len(datos_binarios) % 8) % 8)  # Asegura que la longitud sea múltiplo de 8

    # Carga la imagen
    img = Image.open(imagen_input)
    img = img.convert('RGB')
    imagen = np.array(img)

    # Incrusta los datos en la imagen usando los bits menos significativos
    alto, ancho, _ = imagen.shape
    datos_idx = 0

    for y in range(alto):
        for x in range(ancho):
            for c in range(3):  # RGB
                if datos_idx < len(datos_binarios):
                    bit = int(datos_binarios[datos_idx])
                    imagen[y, x, c] = (imagen[y, x, c] & ~1) | bit
                    datos_idx += 1

    # Calcula el tamaño necesario para la capa de redundancia
    redundancia_alto = (len(datos_binarios) // ancho) + block_size
    redundancia = np.zeros((redundancia_alto, ancho), dtype=np.uint8)

    # Añade la capa de redundancia usando cuadrados blancos y negros al final de la imagen
    datos_idx = 0
    for y in range(0, redundancia_alto, block_size):
        for x in range(0, ancho, block_size):
            if datos_idx < len(datos_binarios):
                bit = int(datos_binarios[datos_idx])
                redundancia[y:y+block_size, x:x+block_size] = bit * 255
                datos_idx += 1

    # Combina la imagen original con la capa de redundancia
    imagen_completa = np.vstack((imagen, np.dstack((redundancia, redundancia, redundancia))))

    # Guarda la imagen con el binario incrustado y la capa de redundancia
    img_incrusted = Image.fromarray(imagen_completa)
    img_incrusted.save(imagen_output)

def main():
    if len(sys.argv) < 3:
        print("Uso: python script.py <binario> <imagen_input> [imagen_output]")
        sys.exit(1)

    binario = sys.argv[1]
    imagen_input = sys.argv[2]

    if len(sys.argv) == 4:
        imagen_output = sys.argv[3]
    else:
        imagen_output = imagen_input.rsplit('.', 1)[0] + '_incrusted.' + imagen_input.rsplit('.', 1)[1]

    binario_a_imagen(binario, imagen_input, imagen_output)
    print(f"Binario incrustado en la imagen y guardado como {imagen_output}")

if __name__ == "__main__":
    main()
