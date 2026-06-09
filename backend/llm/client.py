"""
HANDS & HEAD by Fao Labs
Cliente LLM usando LiteLLM
"""
import os
import json
from typing import Dict, List, Optional, Iterator
from litellm import acompletion, completion


class LLMClient:
    """Cliente para integração com LLM via LiteLLM"""
    
    def __init__(self, model: str = None, api_key: str = None, base_url: str = None):
        self.model = model or os.getenv("LLM_MODEL", "litellm_proxy/minimax-m2.7")
        self.api_key = api_key or os.getenv("LLM_API_KEY", "")
        self.base_url = base_url or os.getenv("LLM_BASE_URL", "https://llm-proxy.app.all-hands.dev")
        self.timeout = 300
        
        # Configurar ambiente
        if self.api_key:
            os.environ["LLM_API_KEY"] = self.api_key
        os.environ["LLM_BASE_URL"] = self.base_url
    
    def get_system_prompt(self) -> str:
        """Retorna o system prompt do agente"""
        return """You are HANDS & HEAD, an AI agent by Fao Labs that can interact with a computer to solve tasks.

<ROLE>
* Your primary role is to assist users by executing commands, modifying code, and solving technical problems effectively.
* You should be thorough, methodical, and prioritize quality over speed.
* If the user asks a question, like "why is X happening", don't try to fix the problem. Just give an answer to the question.
</ROLE>

<CAPABILITIES>
You have access to the following tools:

1. **terminal** - Execute shell commands on the system
   - Use for: running programs, navigating filesystem, git operations
   
2. **file_editor** - Read, write, and edit files
   - Use for: creating files, modifying code, viewing content
   
3. **git** - Execute git commands
   - Use for: version control, commits, branches
   
4. **browser** - Navigate and interact with web pages
   - Use for: searching the web, filling forms, clicking elements
   
5. **think** - Think and reason about a problem
   - Use for: planning, analysis, internal reasoning

When using tools, always respond with the proper tool call format.
After each tool execution, observe the result and decide the next step.
"""
    
    async def chat(self, messages: List[Dict], stream: bool = False) -> Dict:
        """Envia mensagem para o LLM e retorna resposta"""
        try:
            # Preparar mensagens
            formatted_messages = []
            
            # Adicionar system prompt
            formatted_messages.append({
                "role": "system",
                "content": self.get_system_prompt()
            })
            
            # Adicionar histórico
            for msg in messages:
                formatted_messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
            
            response = await acompletion(
                model=self.model,
                messages=formatted_messages,
                stream=False,
                timeout=self.timeout,
            )
            
            return {
                "content": response["choices"][0]["message"]["content"],
                "model": self.model,
                "usage": response.get("usage", {}),
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "content": f"Erro ao comunicar com LLM: {str(e)}"
            }
    
    def chat_sync(self, messages: List[Dict], stream: bool = False) -> Dict:
        """Versão síncrona do chat"""
        try:
            formatted_messages = [
                {"role": "system", "content": self.get_system_prompt()}
            ]
            
            for msg in messages:
                formatted_messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
            
            response = completion(
                model=self.model,
                messages=formatted_messages,
                stream=False,
                timeout=self.timeout,
            )
            
            return {
                "content": response["choices"][0]["message"]["content"],
                "model": self.model,
                "usage": response.get("usage", {}),
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "content": f"Erro ao comunicar com LLM: {str(e)}"
            }


# Instância global
llm_client = LLMClient()