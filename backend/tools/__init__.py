"""
HANDS & HEAD by Fao Labs
Ferramentas do sistema
"""
from .terminal import TerminalTool
from .file_editor import FileEditorTool
from .git_tool import GitTool
from .browser import BrowserTool
from .think import ThinkTool

__all__ = [
    "TerminalTool",
    "FileEditorTool",
    "GitTool",
    "BrowserTool",
    "ThinkTool",
]


class ToolsRegistry:
    """Registro de ferramentas disponíveis"""
    
    def __init__(self):
        self._tools = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Registra ferramentas padrão"""
        self.register("terminal", TerminalTool())
        self.register("file_editor", FileEditorTool())
        self.register("git", GitTool())
        self.register("browser", BrowserTool())
        self.register("think", ThinkTool())
    
    def register(self, name: str, tool):
        """Registra uma nova ferramenta"""
        self._tools[name] = tool
    
    def get(self, name: str):
        """Retorna ferramenta pelo nome"""
        return self._tools.get(name)
    
    def list_tools(self):
        """Lista todas as ferramentas"""
        return list(self._tools.keys())
    
    def execute(self, name: str, **kwargs):
        """Executa uma ferramenta"""
        tool = self.get(name)
        if not tool:
            return {"error": f"Ferramenta '{name}' não encontrada"}
        
        try:
            return tool.execute(**kwargs)
        except Exception as e:
            return {"error": str(e)}


# Instância global
tools_registry = ToolsRegistry()