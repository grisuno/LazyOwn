"""
banner.py

Autor: Gris Iscomeback 
Correo electrónico: grisiscomeback[at]gmail[dot]com
Fecha de creación: 09/06/2024
Licencia: GPL v3

Descripción: Este archivo contiene la definición 
de la lógica banners de la aplicaciòn LazyOwn RedTeam Framework

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

"""

from utils import print_error, Image, os, sys, random, get_terminal_size

ANSI_COLOR_TEMPLATE = "\033[48;2;{r};{g};{b}m  \033[0m"

def image_to_bash(image_path, image_res):
    from PIL import Image
    img = Image.open(image_path)
    img = img.convert('RGB')
    width, height = img.size
    aspect_ratio = height / width
    new_width = image_res
    new_height = int(aspect_ratio * new_width * 0.5)  # ajustado a 0.5
    img = img.resize((new_width, new_height))

    # Hacer altura par
    if img.height % 2 == 1:
        img = img.crop((0, 0, img.width, img.height - 1))

    for y in range(0, img.height, 2):
        line = ""
        for x in range(img.width):
            r1, g1, b1 = img.getpixel((x, y))
            r2, g2, b2 = img.getpixel((x, y + 1))
            line += f"\033[38;2;{r1};{g1};{b1};48;2;{r2};{g2};{b2}m▀\033[0m"
        print(line)

def list_png_files():
    png_files = [f for f in os.listdir('banners') if f.endswith('.png')]
    if not png_files:
        print_error("No PNG files found in the 'banners' directory.")
        sys.exit(1)
    
    selected_image = random.choice(png_files)
    return os.path.join('banners', selected_image)

def main():

    rows, columns = get_terminal_size()
    if rows and columns:
        #Make responsive image ;) feel like frontend 
        
        image_res = int(columns)
    else:
        image_res = 50

    if '-i' in sys.argv or '--image' in sys.argv:
        try:
            if '-i' in sys.argv:
                image_path = sys.argv[sys.argv.index('-i') + 1]
            else:
                image_path = sys.argv[sys.argv.index('--image') + 1]
        except IndexError:
            print_error("Error: No image path provided after the flag.")
            sys.exit(1)
    elif '-h' in sys.argv or '--half' in sys.argv:
        image_res = 50
    else:
        
        image_path = list_png_files()

    if not os.path.isfile(image_path):
        print_error(f"Error: The file '{image_path}' does not exist.")
        sys.exit(1)

    image_to_bash(image_path, image_res)

if __name__ == "__main__":
    
    main()
