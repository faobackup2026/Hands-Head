"""
HANDS & HEAD by Fao Labs
Ferramenta Git
"""
import subprocess
import os
from typing import Dict, Optional


class GitTool:
    """Executa comandos git"""
    
    name = "git"
    description = "Executa comandos Git para controle de versão"
    
    def execute(self, operation: str, path: str = ".", **kwargs) -> Dict:
        """
        Executa operação git
        
        Args:
            operation: status | log | diff | commit | push | pull | branch | checkout | add
            path: Caminho do repositório
            **kwargs: Parâmetros adicionais (message, branch, etc.)
        """
        operations = {
            "status": self._status,
            "log": self._log,
            "diff": self._diff,
            "commit": self._commit,
            "push": self._push,
            "pull": self._pull,
            "branch": self._branch,
            "checkout": self._checkout,
            "add": self._add,
            "clone": self._clone,
            "init": self._init,
        }
        
        if operation not in operations:
            return {"error": f"Operação '{operation}' não suportada"}
        
        return operations[operation](path, **kwargs)
    
    def _run_git(self, args: list, path: str = ".") -> Dict:
        """Executa comando git"""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _status(self, path: str = ".", **kwargs) -> Dict:
        """Retorna status do repositório"""
        return self._run_git(["status", "--porcelain"], path)
    
    def _log(self, path: str = ".", **kwargs) -> Dict:
        """Retorna histórico de commits"""
        n = kwargs.get("n", 10)
        result = self._run_git(["log", f"-{n}", "--pretty=format:%H|%an|%ae|%at|%s"], path)
        
        if result.get("success") and result.get("stdout"):
            commits = []
            for line in result["stdout"].strip().split('\n'):
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) == 5:
                        commits.append({
                            "hash": parts[0],
                            "author": parts[1],
                            "email": parts[2],
                            "timestamp": parts[3],
                            "message": parts[4]
                        })
            result["commits"] = commits
        
        return result
    
    def _diff(self, path: str = ".", **kwargs) -> Dict:
        """Retorna diferenças"""
        target = kwargs.get("target", "HEAD")
        result = self._run_git(["diff", target], path)
        return result
    
    def _commit(self, path: str = ".", **kwargs) -> Dict:
        """Cria commit"""
        message = kwargs.get("message", "")
        if not message:
            return {"success": False, "error": "Mensagem de commit é obrigatória"}
        
        return self._run_git(["commit", "-m", message], path)
    
    def _push(self, path: str = ".", **kwargs) -> Dict:
        """Envia para remote"""
        return self._run_git(["push"], path)
    
    def _pull(self, path: str = ".", **kwargs) -> Dict:
        """Baixa do remote"""
        return self._run_git(["pull"], path)
    
    def _branch(self, path: str = ".", **kwargs) -> Dict:
        """Lista/cria branches"""
        operation = kwargs.get("operation", "list")
        
        if operation == "list":
            return self._run_git(["branch", "-a"], path)
        elif operation == "create":
            name = kwargs.get("name", "")
            if not name:
                return {"success": False, "error": "Nome do branch é obrigatório"}
            return self._run_git(["checkout", "-b", name], path)
        else:
            return {"success": False, "error": f"Operação '{operation}' não suportada"}
    
    def _checkout(self, path: str = ".", **kwargs) -> Dict:
        """Muda de branch"""
        branch = kwargs.get("branch", "")
        if not branch:
            return {"success": False, "error": "Nome do branch é obrigatório"}
        
        return self._run_git(["checkout", branch], path)
    
    def _add(self, path: str = ".", **kwargs) -> Dict:
        """Adiciona arquivos"""
        files = kwargs.get("files", ["."])
        return self._run_git(["add"] + files, path)
    
    def _clone(self, path: str = ".", **kwargs) -> Dict:
        """Clona repositório"""
        url = kwargs.get("url", "")
        dest = kwargs.get("dest", "")
        
        if not url:
            return {"success": False, "error": "URL do repositório é obrigatória"}
        
        args = ["clone", url]
        if dest:
            args.append(dest)
        
        return self._run_git(args, path if not dest else ".")
    
    def _init(self, path: str = ".", **kwargs) -> Dict:
        """Inicializa repositório"""
        return self._run_git(["init"], path)