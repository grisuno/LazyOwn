#!/usr/bin/env python3
# _*_ coding: utf8 _*_
"""
main.py

Autor: Gris Iscomeback
Correo electrónico: grisiscomeback[at]gmail[dot]com
Fecha de creación: 09/06/2024
Licencia: GPL v3

Descripción: Este archivo contiene la definición de las rutas y la lógica de la aplicación de readmineitor creador de documentaciòn automatizada

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

"""
import sys
import os
import ast


def extract_functions_and_comments(script_path):
    with open(script_path, "r") as file:
        tree = ast.parse(file.read(), filename=script_path)

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            # Eliminar prefijos 'do_' o 'run_' si están presentes
            if func_name.startswith("do_"):
                func_name = func_name[3:]
            elif func_name.startswith("run_"):
                func_name = func_name[4:]
            docstring = ast.get_docstring(node)
            functions.append((func_name, docstring))

    return functions


def generate_readme(functions, output_path):
    with open(output_path, "w") as file:
        file.write(f"# {output_path} Documentation  by readmeneitor.py\n\n")
        for func_name, docstring in functions:
            print(f"[*] {func_name} : {docstring}")
            file.write(f"## {func_name}\n")
            file.write(
                f"{docstring}\n\n" if docstring else "No description available.\n\n"
            )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./readmeneitor.py /path/to/script.py")
        sys.exit(1)

    path = os.getcwd()
    script_path = path + "/" + sys.argv[1]
    if sys.argv[1] != 'lazyown':
        output_path = sys.argv[1].upper().replace('.PY','') + ".md"
    else:
        output_path = "COMMANDS.md"

    
    print(f"[+] Script path provided: {script_path}")
    
    
    if os.path.exists(script_path):
        print(f"[+] Executing script at {script_path}")
        functions = extract_functions_and_comments(script_path)
        generate_readme(functions, output_path)
    else:
        print(f"[-] Script path {script_path} does not exist.")


