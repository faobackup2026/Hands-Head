"""
HANDS & HEAD by Fao Labs
Configurações do sistema
"""
import os
import logging
from typing import Dict, List, Optional, Any
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class LLMConfig(BaseModel):
    """Configuração do LLM"""
    model: str = os.getenv("LLM_MODEL", "litellm_proxy/minimax-m2.7")
    api_key: str = os.getenv("LLM_API_KEY", "")
    base_url: str = os.getenv("LLM_BASE_URL", "https://llm-proxy.app.all-hands.dev")
    max_retries: int = 3
    timeout: int = 300


class ToolConfig(BaseModel):
    """Configuração de ferramenta"""
    name: str
    enabled: bool = True
    description: str


class SystemConfig(BaseModel):
    """Configuração do sistema"""
    name: str = "HANDS & HEAD"
    version: str = "1.0.0"
    brand: str = "by Fao Labs"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # LLM
    llm: LLMConfig = LLMConfig()
    
    # Ferramentas disponíveis
    tools: List[ToolConfig] = [
        ToolConfig(name="terminal", description="Executa comandos no terminal"),
        ToolConfig(name="file_editor", description="Lê e edita arquivos"),
        ToolConfig(name="git", description="Comandos Git"),
        ToolConfig(name="browser", description="Navegação web"),
        ToolConfig(name="think", description="Raciocínio interno"),
    ]
    
    # Sistema
    working_dir: str = os.getenv("WORKING_DIR", "/workspace")
    max_output_chars: int = 30000


class Config:
    """Classe de configuração global"""
    
    def __init__(self):
        self.system = SystemConfig()
        self.conversations: Dict[str, List[Dict]] = {}
        self.active_connections: Dict[str, Any] = {}
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Valida a configuração na inicialização"""
        # Validar LLM
        if not self.system.llm.api_key:
            logger.warning("⚠️ LLM_API_KEY não configurada. Configure no .env")
        
        # Validar diretório de trabalho
        if not os.path.exists(self.system.working_dir):
            logger.warning(f"⚠️ Diretório de trabalho não existe: {self.system.working_dir}")
            try:
                os.makedirs(self.system.working_dir, exist_ok=True)
                logger.info(f"✅ Diretório criado: {self.system.working_dir}")
            except Exception as e:
                logger.error(f"❌ Erro ao criar diretório: {e}")
        
        logger.info(f"✅ Configuração validada")
    
    def get_config(self) -> Dict:
        """Retorna configuração para o frontend"""
        return {
            "name": self.system.name,
            "version": self.system.version,
            "brand": self.system.brand,
            "model": self.system.llm.model,
            "available_tools": [t.name for t in self.system.tools if t.enabled],
            "debug": self.system.debug,
        }


# Instância global
config = Config()
