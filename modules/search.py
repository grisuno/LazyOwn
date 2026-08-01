#!/usr/bin/env python3
"""
main.py

Autor: Gris Iscomeback
Correo electrónico: grisiscomeback[at]gmail[dot]com
Fecha de creación: 09/06/2024
Licencia: GPL v3

Descripción: webscrapper gtofbins

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

"""
import csv

import requests
from bs4 import BeautifulSoup

# URL del servidor que contiene el HTML
url = "https://gtfobins.github.io/index.html"

# Hacer una solicitud GET al servidor
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    html_content = response.text
else:
    print("Error getting HTML from server")
    exit()

# Parse HTML content with Beautiful Soup
soup = BeautifulSoup(html_content, 'html.parser')

# Encontrar el contenedor de la tabla
table_wrapper = soup.find('div', id='bin-table-wrapper')

# Initialize a list to store the information
data = []

# Iterate over all table rows
for row in table_wrapper.find_all('tr'):
    bin_name = row.find('a', class_='bin-name')
    if bin_name:
        bin_name_text = bin_name.text.strip()
        functions = []
        for func in row.find_all('li'):
            function_link = func.find('a')
            if function_link:
                function_href = function_link.get('href').strip()
                function_name = function_link.text.strip()
                functions.append({'name': function_name, 'href': function_href})

        # Add the information to the data list
        data.append({'binary': bin_name_text, 'functions': functions})

# Save the information to a CSV file
csv_file = "csv/bin_data.csv"
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Binary', 'Function Name', 'Function URL'])
    for entry in data:
        binary = entry['binary']
        for func in entry['functions']:
            writer.writerow([binary, func['name'], func['href']])

print(f"Data saved to {csv_file}")
