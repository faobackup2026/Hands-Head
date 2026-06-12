"""
HANDS & HEAD by Fao Labs
Cliente LiteLLM para integração com múltiplos provedores de LLM
"""
import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

try:
    import litellm
except ImportError:
    raise ImportError("litellm não está instalado. Execute: pip install litellm")

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Cliente para integração com LiteLLM Proxy
    Suporta: OpenAI, Anthropic, MiniMax, e outros via LiteLLM
    """
    
    def __init__(self, 
                 model: Optional[str] = None,
                 api_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 max_retries: int = 3,
                 timeout: int = 300):
        """
        Inicializa o cliente LLM
        
        Args:
            model: Nome do modelo (ex: "litellm_proxy/minimax-m2.7")
            api_key: Chave da API (lê de LLM_API_KEY se não fornecida)
            base_url: URL base do proxy LLM
            max_retries: Número máximo de tentativas
            timeout: Timeout em segundos
        """
        self.model = model or os.getenv("LLM_MODEL", "litellm_proxy/minimax-m2.7")
        self.api_key = api_key or os.getenv("LLM_API_KEY", "")
        self.base_url = base_url or os.getenv("LLM_BASE_URL", "https://llm-proxy.app.all-hands.dev")
        self.max_retries = max_retries
        self.timeout = timeout
        
        # Configurar LiteLLM
        if self.base_url:
            litellm.api_base = self.base_url
        
        if self.api_key:
            litellm.api_key = self.api_key
        else:
            logger.warning("⚠️ LLM_API_KEY não configurada. O LLM pode não funcionar corretamente.")
        
        # Configurações adicionais
        litellm.request_timeout = self.timeout
        litellm.num_retries = self.max_retries
        
        logger.info(f"✅ LLMClient inicializado com modelo: {self.model}")
        logger.debug(f"   Base URL: {self.base_url}")
    
    def chat_sync(self, 
                  messages: List[Dict[str, str]],
                  temperature: float = 0.7,
                  max_tokens: Optional[int] = None,
                  system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Chat síncrono com o LLM
        
        Args:
            messages: Lista de mensagens no formato OpenAI
                     [{"role": "user", "content": "..."}, ...]
            temperature: Temperatura de criatividade (0.0-1.0)
            max_tokens: Número máximo de tokens na resposta
            system_prompt: Prompt de sistema personalizado
            
        Returns:
            Dicionário com resposta:
            {
                "content": "resposta do assistente",
                "usage": {...},
                "model": "...",
                "created": timestamp,
                "error": None
            }
        """
        try:
            # Adiciona system prompt se fornecido
            if system_prompt:
                system_msg = {"role": "system", "content": system_prompt}
                if messages and messages[0]["role"] != "system":
                    messages = [system_msg] + messages
            
            logger.debug(f"🤔 Chamando LLM com {len(messages)} mensagens")
            
            # Chamada ao LLM via LiteLLM
            response = litellm.completion(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=self.api_key,
                base_url=self.base_url
            )
            
            # Extrai conteúdo da resposta
            content = response.choices[0].message.content
            
            logger.debug(f"✅ Resposta recebida ({len(content)} caracteres)")
            
            return {
                "content": content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if hasattr(response.usage, 'prompt_tokens') else 0,
                    "completion_tokens": response.usage.completion_tokens if hasattr(response.usage, 'completion_tokens') else 0,
                    "total_tokens": response.usage.total_tokens if hasattr(response.usage, 'total_tokens') else 0,
                },
                "model": self.model,
                "created": datetime.now().isoformat(),
                "error": None
            }
        
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ Erro ao chamar LLM: {error_msg}")
            
            return {
                "content": "",
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                "model": self.model,
                "created": datetime.now().isoformat(),
                "error": error_msg
            }
    
    async def chat_async(self,
                        messages: List[Dict[str, str]],
                        temperature: float = 0.7,
                        max_tokens: Optional[int] = None,
                        system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Chat assíncrono com o LLM
        
        Args:
            messages: Lista de mensagens
            temperature: Temperatura
            max_tokens: Máximo de tokens
            system_prompt: Prompt de sistema
            
        Returns:
            Dicionário com resposta
        """
        # Por enquanto, usa implementação síncrona em thread
        # No futuro, pode ser otimizado com aiohttp
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.chat_sync,
            messages,
            temperature,
            max_tokens,
            system_prompt
        )
    
    def get_model_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o modelo configurado"""
        return {
            "model": self.model,
            "base_url": self.base_url,
            "has_api_key": bool(self.api_key),
            "max_retries": self.max_retries,
            "timeout": self.timeout
        }


# Instância global singleton
llm_client = LLMClient()

__all__ = ["LLMClient", "llm_client"]
