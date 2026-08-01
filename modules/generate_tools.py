# generate_tools.py
import ast
import json


def extract_cmd2_tools(script_path="lazyown.py"):
    with open(script_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read())

    tools = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name.startswith("do_") and node.name != "do_exit":
                name = node.name[3:]
                desc = ast.get_docstring(node) or "No description"
                tools.append({
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": desc.strip(),
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "line": {"type": "string", "description": "Command arguments"}
                            },
                            "required": ["line"]
                        }
                    }
                })
    return tools

# Guardar para Ollama
if __name__ == "__main__":
    tools = extract_cmd2_tools()
    with open("tools.json", "w") as f:
        json.dump(tools, f, indent=2)
    print("[+] tools.json generated successfully")
