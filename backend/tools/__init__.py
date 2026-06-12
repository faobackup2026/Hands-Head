"""
HANDS & HEAD by Fao Labs
Registry de Ferramentas
"""
import logging
from typing import Dict, List, Any, Callable
from .terminal import TerminalTool
from .file_editor import FileEditorTool
from .git_tool import GitTool
from .browser import BrowserTool
from .think import ThinkTool

logger = logging.getLogger(__name__)


class ToolsRegistry:
    """
    Registro central de ferramentas disponíveis
    Gerencia instâncias e execução de ferramentas
    """
    
    def __init__(self):
        """Inicializa o registry com todas as ferramentas"""
        self._tools: Dict[str, Any] = {}
        self._register_builtin_tools()
    
    def _register_builtin_tools(self):
        """Registra as ferramentas built-in"""
        tools = [
            TerminalTool(),
            FileEditorTool(),
            GitTool(),
            BrowserTool(),
            ThinkTool(),
        ]
        
        for tool in tools:
            self.register(tool.name, tool)
            logger.info(f"✅ Ferramenta registrada: {tool.name}")
    
    def register(self, name: str, tool: Any) -> None:
        """
        Registra uma nova ferramenta
        
        Args:
            name: Nome da ferramenta
            tool: Instância da ferramenta (deve ter __call__)
        """
        if not hasattr(tool, '__call__'):
            raise ValueError(f"Ferramenta {name} deve ser callable")
        
        self._tools[name] = tool
        logger.debug(f"Ferramenta registrada: {name}")
    
    def get(self, name: str) -> Any:
        """
        Obtém uma ferramenta pelo nome
        
        Args:
            name: Nome da ferramenta
            
        Returns:
            Instância da ferramenta ou None
        """
        return self._tools.get(name)
    
    def execute(self, name: str, **params) -> Dict[str, Any]:
        """
        Executa uma ferramenta
        
        Args:
            name: Nome da ferramenta
            **params: Parâmetros para a ferramenta
            
        Returns:
            Resultado da execução
        """
        tool = self.get(name)
        
        if not tool:
            return {
                "success": False,
                "error": f"Ferramenta '{name}' não encontrada",
                "available_tools": self.list_tools()
            }
        
        try:
            logger.debug(f"Executando ferramenta: {name} com params: {params}")
            result = tool(**params)
            logger.debug(f"Ferramenta {name} executada com sucesso")
            return result
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Erro ao executar {name}: {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
    
    def list_tools(self) -> List[Dict[str, str]]:
        """
        Lista todas as ferramentas disponíveis
        
        Returns:
            Lista de ferramentas com nome e descrição
        """
        tools = []
        for name, tool in self._tools.items():
            tools.append({
                "name": name,
                "description": getattr(tool, 'description', 'Sem descrição')
            })
        return tools
    
    def get_tool_info(self, name: str) -> Dict[str, Any]:
        """
        Obtém informações detalhadas sobre uma ferramenta
        
        Args:
            name: Nome da ferramenta
            
        Returns:
            Dicionário com informações da ferramenta
        """
        tool = self.get(name)
        
        if not tool:
            return {"error": f"Ferramenta '{name}' não encontrada"}
        
        return {
            "name": name,
            "description": getattr(tool, 'description', 'Sem descrição'),
            "parameters": getattr(tool, 'parameters', {}),
            "example": getattr(tool, 'example', None)
        }


# Instância global
tools_registry = ToolsRegistry()

__all__ = ["tools_registry", "ToolsRegistry"]
