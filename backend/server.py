"""
HANDS & HEAD by Fao Labs
Servidor FastAPI com WebSocket
"""
import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, Set
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Adiciona path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import config
from backend.agent import Agent
from backend.llm.client import llm_client


# Modelo de request
class ChatRequest(BaseModel):
    message: str
    stream: bool = False


# Modelo de response
class ChatResponse(BaseModel):
    response: str
    actions: list = []
    iterations: int = 0


# Gerenciamento de conexões WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.agents: Dict[WebSocket, Agent] = {}
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        self.agents[websocket] = Agent(llm_client)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        if websocket in self.agents:
            del self.agents[websocket]
    
    async def send_message(self, websocket: WebSocket, message: dict):
        await websocket.send_json(message)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager"""
    print("🚀 HANDS & HEAD by Fao Labs - Servidor iniciando...")
    print(f"📁 Diretório de trabalho: {config.system.working_dir}")
    print(f"🔧 Ferramentas: {', '.join([t.name for t in config.system.tools])}")
    yield
    print("👋 HANDS & HEAD - Servidor encerrando...")


# Criar app FastAPI
app = FastAPI(
    title="HANDS & HEAD",
    description="Agente de IA por Fao Labs",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== ROTAS HTTP ==============

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve interface web"""
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return """
    <html>
        <head><title>HANDS & HEAD</title></head>
        <body>
            <h1>HANDS & HEAD by Fao Labs</h1>
            <p>Interface não encontrada. Verifique se frontend/index.html existe.</p>
        </body>
    </html>
    """


@app.get("/api/config")
async def get_config():
    """Retorna configuração do sistema"""
    return config.get_config()


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Endpoint HTTP para chat"""
    try:
        agent = Agent(llm_client)
        result = await agent.process_message(request.message)
        
        return ChatResponse(
            response=result["response"],
            actions=result["actions"],
            iterations=result["iterations"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "service": "HANDS & HEAD",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/tools")
async def list_tools():
    """Lista ferramentas disponíveis"""
    from backend.tools import tools_registry
    return {
        "tools": tools_registry.list_tools()
    }


# ============== WEBSOCKET ==============

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint WebSocket para comunicação em tempo real"""
    await manager.connect(websocket)
    agent = manager.agents[websocket]
    
    try:
        # Envia confirmação de conexão
        await manager.send_message(websocket, {
            "type": "connected",
            "content": "Conexão estabelecida com HANDS & HEAD",
            "config": config.get_config()
        })
        
        while True:
            # Recebe mensagem do cliente
            data = await websocket.receive_json()
            msg_type = data.get("type", "message")
            content = data.get("content", "")
            
            if msg_type == "ping":
                await manager.send_message(websocket, {"type": "pong", "content": "pong"})
                continue
            
            if msg_type == "reset":
                agent.reset()
                await manager.send_message(websocket, {
                    "type": "reset",
                    "content": "Conversa resetada"
                })
                continue
            
            if msg_type == "message":
                # Processa mensagem
                await manager.send_message(websocket, {
                    "type": "thinking",
                    "content": "Processando..."
                })
                
                try:
                    result = await agent.process_message(content)
                    
                    # Envia resposta
                    await manager.send_message(websocket, {
                        "type": "response",
                        "content": result["response"],
                        "iterations": result["iterations"]
                    })
                    
                    # Envia ações executadas
                    if result["actions"]:
                        await manager.send_message(websocket, {
                            "type": "actions",
                            "actions": [
                                {
                                    "tool": a["tool"],
                                    "params": a["params"],
                                    "observation": a["observation"]
                                }
                                for a in result["actions"]
                            ]
                        })
                    
                    # Envia sinal de completo
                    await manager.send_message(websocket, {
                        "type": "complete",
                        "content": "Tarefa concluída"
                    })
                    
                except Exception as e:
                    await manager.send_message(websocket, {
                        "type": "error",
                        "content": f"Erro ao processar: {str(e)}"
                    })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Cliente desconectado")
    except Exception as e:
        print(f"Erro WebSocket: {e}")
        manager.disconnect(websocket)


# ============== ARQUIVOS ESTÁTICOS ==============

# Monta arquivos estáticos
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


# ============== MAIN ==============

def main():
    """Inicia o servidor"""
    import uvicorn
    
    port = int(os.getenv("PORT", "12000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     🤝 HANDS & HEAD by Fao Labs                          ║
║                                                           ║
║     Agente de IA para automação e execução de tarefas    ║
║                                                           ║
║     🌐 http://localhost:{port}                             ║
║     📡 WebSocket: ws://localhost:{port}/ws                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "backend.server:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()