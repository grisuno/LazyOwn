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

from utils import *

ANSI_COLOR_TEMPLATE = "\033[48;2;{r};{g};{b}m  \033[0m"

def image_to_bash(image_path, image_res):
    
    img = Image.open(image_path)
    img = img.convert('RGB')  
    width, height = img.size
    aspect_ratio = height / width
    new_width = image_res
    new_height = int(aspect_ratio * new_width * 0.55)  
    img = img.resize((new_width, new_height))
    
    for y in range(img.height):
        line = ""
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            line += ANSI_COLOR_TEMPLATE.format(r=r, g=g, b=b)
        print(line)

def list_png_files():
    png_files = [f for f in os.listdir('banners') if f.endswith('.png')]
    if not png_files:
        print_error("No PNG files found in the 'banners' directory.")
        sys.exit(1)
    
    selected_image = random.choice(png_files)
    print_msg(f"Randomly selected image: {selected_image}")
    return os.path.join('banners', selected_image)

def main():

    rows, columns = get_terminal_size()
    if rows and columns:
        #Make responsive image ;) feel like frontend 
        image_res = int(columns/2)
       

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
