import os
from typing import Optional
from abc import ABC, abstractmethod
from pathlib import Path

class PromptSource(ABC):
    @abstractmethod
    def get_prompt(self) -> str:
        pass

class StaticPromptSource(PromptSource):
    def __init__(self, prompt: Optional[str] = None):
        self.prompt = prompt or os.getenv('STATIC_PROMPT', 'Default prompt')
    
    def get_prompt(self) -> str:
        return self.prompt

class FilePromptSource(PromptSource):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path or os.getenv('PROMPT_FILE_PATH', 'prompts/default.txt')
    
    def get_prompt(self) -> str:
        try:
            with open(self.file_path, 'r') as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading prompt file: {e}")
            return ""

class APIPromptSource(PromptSource):
    def __init__(self, api_url: Optional[str] = None):
        self.api_url = api_url or os.getenv('PROMPT_API_URL', 'http://localhost:8000/prompt')
    
    def get_prompt(self) -> str:
        # TODO: Implement API call
        return "API prompt not implemented yet"

class PromptSourceFactory:
    @staticmethod
    def create_source(source_type: str) -> PromptSource:
        if source_type == 'static':
            return StaticPromptSource()
        elif source_type == 'file':
            return FilePromptSource()
        elif source_type == 'api':
            return APIPromptSource()
        else:
            raise ValueError(f"Unknown prompt source type: {source_type}") 