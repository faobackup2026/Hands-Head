"""
HANDS & HEAD by Fao Labs
Motor do Agente - Loop THINK → ACTION → OBSERVE
"""
import json
import re
from typing import Dict, List, Optional
from .llm.client import LLMClient
from .tools import tools_registry


class Agent:
    """
    Agente de IA com loop THINK → ACTION → OBSERVE
    
    Fluxo:
    1. THINK: Analisa input e decide próxima ação
    2. ACTION: Executa ação usando ferramenta
    3. OBSERVE: Observa resultado e decide próximo passo
    4. Repete até completar a tarefa
    """
    
    def __init__(self, llm_client: LLMClient = None):
        self.llm = llm_client or LLMClient()
        self.tools = tools_registry
        self.conversation_history: List[Dict] = []
        self.max_iterations = 20
        self.current_iteration = 0
    
    def think(self, user_input: str) -> str:
        """
        THINK: Usa LLM para analisar input e decidir ações
        
        Args:
            user_input: Mensagem do usuário
            
        Returns:
            Resposta planejada do LLM
        """
        messages = self.conversation_history.copy()
        messages.append({"role": "user", "content": user_input})
        
        response = self.llm.chat_sync(messages)
        return response.get("content", "")
    
    def parse_tool_calls(self, text: str) -> List[Dict]:
        """
        Extrai chamadas de ferramentas do texto
        
        Suporta formatos:
        - <tool_name>param1=value1|param2=value2</tool_name>
        - JSON com tool_calls
        """
        tool_calls = []
        
        # Padrão XML-like: <tool>params</tool>
        xml_pattern = r'<(\w+)>(.*?)</\1>'
        matches = re.findall(xml_pattern, text, re.DOTALL)
        
        for tool_name, params_str in matches:
            if self.tools.get(tool_name):
                params = self._parse_params(params_str)
                tool_calls.append({
                    "tool": tool_name,
                    "params": params
                })
        
        # Padrão JSON: {"tool": "name", "params": {...}}
        json_pattern = r'\{[^{}]*"tool"[^{}]*\}'
        json_matches = re.findall(json_pattern, text, re.JSON)
        for match in json_matches:
            try:
                data = json.loads(match)
                if "tool" in data:
                    tool_calls.append({
                        "tool": data["tool"],
                        "params": data.get("params", {})
                    })
            except:
                pass
        
        return tool_calls
    
    def _parse_params(self, params_str: str) -> Dict:
        """Parseia string de parâmetros"""
        params = {}
        for pair in params_str.split('|'):
            if '=' in pair:
                key, value = pair.split('=', 1)
                params[key.strip()] = value.strip()
        return params
    
    def execute_action(self, tool_name: str, params: Dict) -> Dict:
        """
        ACTION: Executa uma ferramenta
        
        Args:
            tool_name: Nome da ferramenta
            params: Parâmetros para execução
            
        Returns:
            Resultado da execução
        """
        return self.tools.execute(tool_name, **params)
    
    def observe(self, action_result: Dict) -> str:
        """
        OBSERVE: Formata resultado para o LLM
        
        Args:
            action_result: Resultado da execução
            
        Returns:
            Descrição observada do resultado
        """
        if action_result.get("error"):
            return f"Erro: {action_result['error']}"
        
        if action_result.get("success") is False:
            return f"Falha: {action_result.get('stderr', 'Erro desconhecido')}"
        
        # Formata resultado baseado no tipo
        if "stdout" in action_result:
            return action_result["stdout"][:5000] if action_result["stdout"] else "(sem saída)"
        
        if "content" in action_result:
            content = action_result["content"]
            if isinstance(content, str):
                return content[:5000]
            return str(content)
        
        return str(action_result)[:2000]
    
    async def process_message(self, user_input: str) -> Dict:
        """
        Processa mensagem do usuário com loop THINK → ACTION → OBSERVE
        
        Args:
            user_input: Mensagem do usuário
            
        Returns:
            Dicionário com resposta e ações executadas
        """
        self.current_iteration = 0
        self.conversation_history.append({"role": "user", "content": user_input})
        
        actions = []
        final_response = ""
        thoughts = []
        
        while self.current_iteration < self.max_iterations:
            self.current_iteration += 1
            
            # THINK: Analisa e decide
            think_result = self.think(user_input if self.current_iteration == 1 else 
                                      f"Continue a tarefa. Último resultado: {actions[-1] if actions else 'N/A'}")
            
            thoughts.append(think_result)
            
            # Extrai chamadas de ferramentas
            tool_calls = self.parse_tool_calls(think_result)
            
            if not tool_calls:
                # Não há mais ações, retorna resposta final
                final_response = think_result
                break
            
            # ACTION + OBSERVE: Executa cada ferramenta
            for call in tool_calls:
                tool_name = call["tool"]
                params = call["params"]
                
                result = self.execute_action(tool_name, params)
                observation = self.observe(result)
                
                actions.append({
                    "tool": tool_name,
                    "params": params,
                    "result": result,
                    "observation": observation
                })
                
                # Adiciona observação ao histórico
                self.conversation_history.append({
                    "role": "system",
                    "content": f"[{tool_name}] Resultado: {observation}"
                })
        
        # Adiciona resposta final ao histórico
        self.conversation_history.append({"role": "assistant", "content": final_response})
        
        return {
            "response": final_response,
            "thoughts": thoughts,
            "actions": actions,
            "iterations": self.current_iteration
        }
    
    def reset(self):
        """Reseta histórico da conversa"""
        self.conversation_history = []
        self.current_iteration = 0
    
    def get_history(self) -> List[Dict]:
        """Retorna histórico da conversa"""
        return self.conversation_history.copy()