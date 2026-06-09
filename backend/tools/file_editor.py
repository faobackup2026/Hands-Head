"""
HANDS & HEAD by Fao Labs
Ferramenta de Edição de Arquivos
"""
import os
from typing import Dict, List, Optional


class FileEditorTool:
    """Lê, escreve e edita arquivos no sistema"""
    
    name = "file_editor"
    description = "Lê, escreve e edita arquivos no sistema de arquivos"
    
    def execute(self, operation: str, path: str = None, content: str = None, 
                old_str: str = None, new_str: str = None) -> Dict:
        """
        Executa operação de arquivo
        
        Args:
            operation: read | write | edit | create_dir | list_dir | delete | exists
            path: Caminho do arquivo/diretório
            content: Conteúdo para escrever
            old_str: String antiga (para edição)
            new_str: Nova string (para edição)
            
        Returns:
            Dict com resultado da operação
        """
        if operation == "read":
            return self._read(path)
        elif operation == "write":
            return self._write(path, content)
        elif operation == "edit":
            return self._edit(path, old_str, new_str)
        elif operation == "create_dir":
            return self._create_dir(path)
        elif operation == "list_dir":
            return self._list_dir(path)
        elif operation == "delete":
            return self._delete(path)
        elif operation == "exists":
            return self._exists(path)
        else:
            return {"error": f"Operação '{operation}' não suportada"}
    
    def _read(self, path: str) -> Dict:
        """Lê conteúdo de arquivo"""
        try:
            if not os.path.exists(path):
                return {"success": False, "error": f"Arquivo não encontrado: {path}"}
            
            if os.path.isdir(path):
                return {"success": False, "error": f"Caminho é um diretório: {path}"}
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "success": True,
                "path": path,
                "content": content,
                "size": len(content),
                "lines": len(content.split('\n'))
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _write(self, path: str, content: str) -> Dict:
        """Escreve conteúdo em arquivo"""
        try:
            # Criar diretórios pais se necessário
            os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "success": True,
                "path": path,
                "bytes_written": len(content.encode('utf-8'))
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _edit(self, path: str, old_str: str, new_str: str) -> Dict:
        """Edita arquivo substituindo string"""
        try:
            if not os.path.exists(path):
                return {"success": False, "error": f"Arquivo não encontrado: {path}"}
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_str not in content:
                return {"success": False, "error": "String não encontrada no arquivo"}
            
            new_content = content.replace(old_str, new_str)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return {
                "success": True,
                "path": path,
                "replacements": content.count(old_str)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _create_dir(self, path: str) -> Dict:
        """Cria diretório"""
        try:
            os.makedirs(path, exist_ok=True)
            return {
                "success": True,
                "path": path,
                "created": True
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _list_dir(self, path: str = ".") -> Dict:
        """Lista conteúdo de diretório"""
        try:
            if not os.path.exists(path):
                return {"success": False, "error": f"Diretório não encontrado: {path}"}
            
            if not os.path.isdir(path):
                return {"success": False, "error": f"Caminho não é diretório: {path}"}
            
            items = []
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                stat = os.stat(item_path)
                items.append({
                    "name": item,
                    "type": "dir" if os.path.isdir(item_path) else "file",
                    "size": stat.st_size,
                    "modified": stat.st_mtime
                })
            
            return {
                "success": True,
                "path": path,
                "items": items
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _delete(self, path: str) -> Dict:
        """Deleta arquivo ou diretório"""
        try:
            if not os.path.exists(path):
                return {"success": False, "error": f"Caminho não encontrado: {path}"}
            
            if os.path.isdir(path):
                import shutil
                shutil.rmtree(path)
            else:
                os.remove(path)
            
            return {
                "success": True,
                "path": path,
                "deleted": True
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _exists(self, path: str) -> Dict:
        """Verifica se caminho existe"""
        return {
            "success": True,
            "path": path,
            "exists": os.path.exists(path),
            "is_dir": os.path.isdir(path) if os.path.exists(path) else None,
            "is_file": os.path.isfile(path) if os.path.exists(path) else None
        }