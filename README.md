# HANDS & HEAD by Fao Labs 🤝

![Version](https://img.shields.io/badge/version-1.0.0--blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

> **HANDS & HEAD** é um agente de IA conversacional que pode interagir com seu computador para resolver tarefas. Inspirado no OpenHands, oferece interface web completa com terminal integrado, editor de arquivos, navegação browser, e muito mais.

---

## ✨ Funcionalidades

- 💬 **Chat com IA** - Conversação natural em português
- 🖥️ **Terminal Integrado** - Execute comandos shell diretamente
- 📁 **Editor de Arquivos** - Leia, escreva e edite arquivos
- 📚 **Git Integration** - Comandos git para versionamento
- 🌐 **Navegador Web** - Acesse e interaja com páginas
- 🔄 **Loop THINK→ACTION→OBSERVE** - Execução autônoma de tarefas
- 🎨 **Interface Moderna** - Design responsivo e intuitivo
- 🔌 **WebSocket** - Comunicação em tempo real

---

## 🚀 Quick Start

### 1. Clone ou baixe o projeto

```bash
cd hands-head-fao-labs
```

### 2. Execute o instalador

```bash
chmod +x setup.sh run.sh
./setup.sh
```

### 3. Inicie o servidor

```bash
./run.sh
```

### 4. Acesse no navegador

```
http://localhost:12000
```

---

## 📋 Requisitos

- **Python** 3.10 ou superior
- **pip** (gerenciador de pacotes Python)
- **Sistema operacional**: Linux, macOS, Windows (com WSL)

---

## 🔧 Configuração

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `PORT` | Porta do servidor | `12000` |
| `HOST` | Host do servidor | `0.0.0.0` |
| `LLM_MODEL` | Modelo LLM a usar | `litellm_proxy/minimax-m2.7` |
| `LLM_API_KEY` | Chave API do LLM | (vazio) |
| `LLM_BASE_URL` | URL base do proxy LLM | `https://llm-proxy.app.all-hands.dev` |

### Modelos Suportados

- MiniMax M2.7
- OpenAI GPT-4o
- Anthropic Claude 3.5 Sonnet
- Qualquer modelo via LiteLLM

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser)                         │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  Web Interface (index.html)                              │   │
│   │  ├── Chat Window                                         │   │
│   │  ├── Terminal Output                                     │   │
│   │  ├── File Tree                                           │   │
│   │  └── Settings Panel                                     │   │
│   └─────────────────────────────────────────────────────────┘   │
│                              │ WebSocket                        │
└──────────────────────────────┼──────────────────────────────────┘
                               │
┌──────────────────────────────┼──────────────────────────────────┐
│                         SERVER (Backend)                        │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  FastAPI + WebSocket Server (server.py)                  │   │
│   │  ├── /api/chat - HTTP endpoint                          │   │
│   │  ├── /ws - WebSocket endpoint                           │   │
│   │  └── /api/config - Configurações                        │   │
│   └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  Agent Engine (agent.py)                                │   │
│   │  ├── THINK → ACTION → OBSERVE Loop                      │   │
│   │  ├── LLM Integration (LiteLLM)                          │   │
│   │  └── Conversation Manager                                │   │
│   └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  Tools (tools/)                                         │   │
│   │  ├── TerminalTool       - Executa comandos shell         │   │
│   │  ├── FileEditorTool     - Ler/editar arquivos           │   │
│   │  ├── GitTool           - Comandos git                    │   │
│   │  ├── BrowserTool       - Navegação web                  │   │
│   │  └── ThinkTool         - Raciocínio interno             │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura do Projeto

```
hands-head-fao-labs/
├── SPEC.md                 # Especificação técnica
├── README.md               # Este arquivo
├── LICENSE                 # Licença MIT
├── requirements.txt        # Dependências Python
├── setup.sh               # Script de instalação
├── run.sh                 # Script de execução
├── cloudflare-tunnel.sh   # Script para túnel Cloudflare
├── frontend/
│   └── index.html         # Interface web completa
├── backend/
│   ├── __init__.py
│   ├── server.py          # FastAPI server + WebSocket
│   ├── agent.py           # Motor do agente
│   ├── config.py          # Configurações
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── terminal.py    # TerminalTool
│   │   ├── file_editor.py # FileEditorTool
│   │   ├── git_tool.py    # GitTool
│   │   ├── browser.py     # BrowserTool
│   │   └── think.py       # ThinkTool
│   └── llm/
│       ├── __init__.py
│       └── client.py      # Cliente LiteLLM
└── static/
    └── (arquivos estáticos)
```

---

## 🌐 Deploy na Nuvem

### Usando Cloudflare Tunnel

1. Execute o servidor localmente:
```bash
./run.sh
```

2. Em outro terminal, crie o túnel:
```bash
cloudflared tunnel --url http://localhost:12000
```

3. Use o link gerado para acessar seu HANDS & HEAD de qualquer lugar!

### Usando ngrok

```bash
ngrok http 12000
```

---

## 🛠️ API Reference

### Endpoints HTTP

#### `GET /api/config`
Retorna configuração do sistema.

#### `POST /api/chat`
Envia mensagem ao agente.

**Request:**
```json
{
  "message": "Olá, como você está?",
  "stream": false
}
```

**Response:**
```json
{
  "response": "Olá! Estou bem, obrigado por perguntar!",
  "actions": [],
  "iterations": 1
}
```

#### `GET /api/health`
Health check do servidor.

#### `GET /api/tools`
Lista ferramentas disponíveis.

### WebSocket `/ws`

Conecte-se ao WebSocket para comunicação em tempo real.

**Mensagens do Cliente:**
```json
{"type": "message", "content": "Olá!"}
{"type": "ping"}
{"type": "reset"}
```

**Mensagens do Servidor:**
```json
{"type": "connected", "content": "...", "config": {...}}
{"type": "thinking", "content": "Processando..."}
{"type": "response", "content": "...", "iterations": 1}
{"type": "actions", "actions": [...]}
{"type": "complete", "content": "Tarefa concluída"}
{"type": "error", "content": "..."}
```

---

## 🔒 Segurança

- API keys são armazenadas apenas localmente
- Conexões WebSocket são limitadas ao servidor
- Comandos shell são executados no contexto do servidor
- Recomendado: use em ambiente controlado

---

## 📝 Licença

Este projeto está sob licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🤝 Contribuir

Contribuições são bem-vindas! Feel free para abrir issues e pull requests.

---

## 📧 Contato

**Fao Labs**
- Website: https://faolabs.com
- Email: contato@faolabs.com

---

<p align="center">
  <strong>HANDS & HEAD by Fao Labs</strong> - Powered by AI 🤝
</p>