from typing import Callable, Dict, Any, List
import inspect
import json
import logging

class AgentTool:
    """Representa una herramienta ejecutable por el agente"""
    
    def __init__(self, name: str, description: str, func: Callable, 
                 parameters: Dict[str, Any], required: List[str] = None):
        self.name = name
        self.description = description
        self.func = func
        self.parameters = {
            "type": "object",
            "properties": parameters,
            "required": required or list(parameters.keys())
        }
    
    def to_api_format(self) -> Dict[str, Any]:
        """Convierte al formato API de LLM (Groq/Ollama)"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }
    
    def execute(self, **kwargs) -> str:
        """Ejecuta la herramienta con manejo de errores robusto"""
        try:
            result = self.func(**kwargs)
            return json.dumps({"success": True, "result": result})
        except Exception as e:
            error_msg = f"Error ejecutando {self.name}: {str(e)}"
            logging.error(error_msg)
            return json.dumps({"success": False, "error": error_msg})