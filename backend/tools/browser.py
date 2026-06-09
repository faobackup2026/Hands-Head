"""
HANDS & HEAD by Fao Labs
Ferramenta de Navegação Browser
"""
import httpx
from typing import Dict, Optional
import asyncio


class BrowserTool:
    """Navega e interage com páginas web"""
    
    name = "browser"
    description = "Navega e interage com páginas web"
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)
        self.history = []
    
    async def execute(self, operation: str, url: str = None, **kwargs) -> Dict:
        """
        Executa operação de browser
        
        Args:
            operation: get | post | content | headers
            url: URL para acessar
            **kwargs: Parâmetros adicionais
        """
        if operation == "get":
            return await self._get(url)
        elif operation == "post":
            return await self._post(url, **kwargs)
        elif operation == "content":
            return await self._get_content(url)
        elif operation == "headers":
            return await self._get_headers(url)
        else:
            return {"error": f"Operação '{operation}' não suportada"}
    
    async def _get(self, url: str) -> Dict:
        """Faz GET request"""
        try:
            response = await self.client.get(url)
            self.history.append({"url": url, "status": response.status_code})
            
            return {
                "success": True,
                "url": str(response.url),
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.text[:10000],  # Limita tamanho
                "content_length": len(response.content)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _post(self, url: str, **kwargs) -> Dict:
        """Faz POST request"""
        try:
            data = kwargs.get("data", {})
            json_data = kwargs.get("json", {})
            
            response = await self.client.post(url, data=data, json=json_data)
            
            return {
                "success": True,
                "url": str(response.url),
                "status_code": response.status_code,
                "content": response.text[:10000],
                "content_length": len(response.content)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_content(self, url: str) -> Dict:
        """Retorna conteúdo da página"""
        try:
            response = await self.client.get(url)
            
            return {
                "success": True,
                "url": str(response.url),
                "content": response.text,
                "content_type": response.headers.get("content-type", ""),
                "encoding": response.encoding
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_headers(self, url: str) -> Dict:
        """Retorna headers da resposta"""
        try:
            response = await self.client.get(url)
            
            return {
                "success": True,
                "url": str(response.url),
                "headers": dict(response.headers),
                "status_code": response.status_code
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_history(self) -> list:
        """Retorna histórico de navegação"""
        return self.history
    
    async def close(self):
        """Fecha cliente HTTP"""
        await self.client.aclose()


# Para uso síncrono
def execute(operation: str, url: str = None, **kwargs) -> Dict:
    """Wrapper síncrono para operações de browser"""
    browser = BrowserTool()
    try:
        if asyncio.get_event_loop().is_running():
            # Se já há loop rodando, retorna erro amigável
            return {"error": "Operações de browser são assíncronas. Use await."}
        else:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(browser.execute(operation, url, **kwargs))
            loop.close()
            return result
    except Exception as e:
        return {"error": str(e)}