"""
HANDS & HEAD by Fao Labs
Ferramenta de Terminal
"""
import subprocess
import os
from typing import Dict, Optional


class TerminalTool:
    """Executa comandos no terminal do sistema"""
    
    name = "terminal"
    description = "Executa comandos no terminal do sistema"
    
    def execute(self, command: str, working_dir: Optional[str] = None, timeout: int = 60) -> Dict:
        """
        Executa um comando no terminal
        
        Args:
            command: Comando a executar
            working_dir: Diretório de trabalho (opcional)
            timeout: Timeout em segundos
            
        Returns:
            Dict com stdout, stderr e exit_code
        """
        try:
            cwd = working_dir or os.getcwd()
            
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": True,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
                "command": command
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Comando expirou após {timeout} segundos",
                "stdout": "",
                "stderr": "",
                "exit_code": -1,
                "command": command
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "stdout": "",
                "stderr": "",
                "exit_code": -1,
                "command": command
            }
    
    def get_info(self) -> Dict:
        """Retorna informações sobre o sistema"""
        try:
            os_info = subprocess.run("uname -a", shell=True, capture_output=True, text=True)
            cpu_info = subprocess.run("nproc", shell=True, capture_output=True, text=True)
            
            return {
                "os": os_info.stdout.strip(),
                "cpu_cores": cpu_info.stdout.strip(),
                "cwd": os.getcwd(),
                "user": os.getenv("USER", "unknown"),
                "home": os.path.expanduser("~")
            }
        except Exception as e:
            return {"error": str(e)}