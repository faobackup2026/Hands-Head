"""
HANDS & HEAD by Fao Labs
Ferramenta de Pensamento (Think)
"""
from typing import Dict


class ThinkTool:
    """Permite ao agente pensar e raciocinar internamente"""
    
    name = "think"
    description = "Permite ao agente pensar e raciocinar sobre um problema"
    
    def execute(self, thought: str, context: str = None) -> Dict:
        """
        Registra pensamento do agente
        
        Args:
            thought: O pensamento/pensamento a ser registrado
            context: Contexto adicional (opcional)
            
        Returns:
            Confirmação do pensamento registrado
        """
        return {
            "success": True,
            "thought": thought,
            "context": context,
            "registered": True,
            "message": "Pensamento registrado com sucesso"
        }
    
    def analyze(self, problem: str, options: list = None) -> Dict:
        """
        Analisa um problema de forma estruturada
        
        Args:
            problem: Descrição do problema
            options: Lista de opções/alternativas (opcional)
            
        Returns:
            Análise estruturada do problema
        """
        analysis = {
            "problem": problem,
            "options": options or [],
            "analysis": {
                "complexity": self._estimate_complexity(problem),
                "category": self._categorize(problem),
            },
            "suggestions": self._generate_suggestions(problem)
        }
        
        return {
            "success": True,
            "analysis": analysis
        }
    
    def _estimate_complexity(self, problem: str) -> str:
        """Estima complexidade do problema"""
        problem_lower = problem.lower()
        
        complex_keywords = ["múltiplos", "vários", "complexo", "difícil", "avançado", "multiple", "complex"]
        simple_keywords = ["simples", "básico", "fácil", "rápido", "simple", "basic", "easy"]
        
        if any(kw in problem_lower for kw in complex_keywords):
            return "high"
        elif any(kw in problem_lower for kw in simple_keywords):
            return "low"
        else:
            return "medium"
    
    def _categorize(self, problem: str) -> str:
        """Categoriza o problema"""
        problem_lower = problem.lower()
        
        categories = {
            "code": ["código", "programa", "função", "bug", "code", "program", "function"],
            "config": ["config", "configuração", "setting", "setup"],
            "data": ["dados", "banco", "data", "database", "sql"],
            "network": ["rede", "url", "http", "network", "connection"],
            "file": ["arquivo", "file", "pasta", "directory", "folder"],
        }
        
        for category, keywords in categories.items():
            if any(kw in problem_lower for kw in keywords):
                return category
        
        return "general"
    
    def _generate_suggestions(self, problem: str) -> list:
        """Gera sugestões para abordar o problema"""
        suggestions = [
            "Analise o problema passo a passo",
            "Identifique os componentes principais",
            "Verifique dependências e configurações",
            "Teste cada parte individualmente",
            "Considere edge cases"
        ]
        return suggestions