import ast
import inspect
from typing import List, Dict, Any, Optional

def extract_tools_from_source(file_path: str, class_name: str = None, 
                               prefix: str = "do_") -> List[AgentTool]:
    """Extrae AgentTool desde archivos Python (ideal para cmd2)"""
    
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    
    tools = []
    target_class = None
    
    # Encontrar clase si se especificó
    if class_name:
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                target_class = node
                break
    
    # Extraer métodos
    container = target_class.body if target_class else tree.body
    
    for node in container:
        if isinstance(node, ast.FunctionDef) and node.name.startswith(prefix):
            tool_name = node.name[len(prefix):]
            docstring = ast.get_docstring(node) or f"Comando {tool_name}"
            
            # Detectar parámetros (cmd2 usa 'line' o 'args')
            params = {}
            for arg in node.args.args:
                if arg.arg == 'self':
                    continue
                params[arg.arg] = {
                    "type": "string",
                    "description": f"Parámetro {arg.arg}"
                }
            
            # Cmd2 usa 'line' por defecto
            if not params:
                params = {"line": {
                    "type": "string", 
                    "description": "Argumentos del comando"
                }}
            
            # Crear tool stub (la función real se vinculará después)
            tools.append(AgentTool(
                name=f"cmd_{tool_name}",
                description=docstring.strip(),
                func=None,  # Se asignará en runtime
                parameters=params
            ))
    
    return tools