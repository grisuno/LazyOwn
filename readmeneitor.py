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
        file.write("# Documentation by readmeneitor.py\n\n")
        for func_name, docstring in functions:
            file.write(f"## {func_name}\n")
            file.write(
                f"{docstring}\n\n" if docstring else "No description available.\n\n"
            )


if __name__ == "__main__":
    script_path = "/home/gris/LazyOwn/lazyown"  # Cambia esto por la ruta de tu script
    output_path = "COMMANDS.md"
    functions = extract_functions_and_comments(script_path)
    generate_readme(functions, output_path)
