#!/usr/bin/env python3
"""
main.py

Autor: Gris Iscomeback
Email: grisiscomeback[at]gmail[dot]com
Creation date: 09/06/2024
Licencia: GPL v3

Description: This file contains route definitions and application logic for the readmeneitor automated documentation generator.

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

"""
import ast
import os
import sys


def extract_functions_and_comments(script_path):
    with open(script_path, "r") as file:
        tree = ast.parse(file.read(), filename=script_path)

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
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
            print(f"[*] Documented function: {func_name}")
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
    if sys.argv[1] != 'lazyown.py':
        output_path = sys.argv[1].upper().replace('.PY','') + ".md"
    else:
        output_path = "COMMANDS.md"


    print(f"[+] Script path provided: {script_path}")


    if os.path.exists(script_path):
        print(f"[+] Executing script at {script_path}")
        functions = extract_functions_and_comments(script_path)
        generate_readme(functions, output_path)
        os.system(f"pandoc {output_path} -f markdown -t html -s -o {output_path.replace('.md','')}.html --metadata title='LazyOwn Framework Doc: {output_path}' && mv {output_path.replace('.md','')}.html docs/")
    else:
        print(f"[-] Script path {script_path} does not exist.")


