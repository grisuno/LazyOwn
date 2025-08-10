# ai_model.py
import os
import json
import requests
from abc import ABC, abstractmethod
from typing import Generator, Union
from groq import Groq
from flask import Response, stream_with_context

class AIModel(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> Union[str, Generator[str, None, None]]:
        pass

    @abstractmethod
    def stream_generate(self, prompt: str) -> Generator[str, None, None]:
        pass


class GroqModel(AIModel):
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.client = Groq(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Error con Groq: {str(e)}"

    def stream_generate(self, prompt: str) -> Generator[str, None, None]:
        try:
            stream = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                stream=True,
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            yield f"Error streaming Groq: {str(e)}"


class OllamaModel(AIModel):
    def __init__(self, model: str = "deepseek-r1:1.5b", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host

    def generate(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                return f"Error Ollama: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error conexión Ollama: {str(e)}"

    def stream_generate(self, prompt: str) -> Generator[str, None, None]:
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True
                },
                stream=True
            )
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line.decode('utf-8'))
                            if "response" in chunk:
                                yield chunk["response"]
                        except json.JSONDecodeError:
                            continue
            else:
                yield f"Error Ollama: {response.status_code}"
        except Exception as e:
            yield f"Error streaming Ollama: {str(e)}"