# HANDS & HEAD by Fao Labs
## Especificação Técnica Completa v1.0

---

## 1. Visão Geral do Projeto

### 1.1 Descrição
**HANDS & HEAD** é um sistema de agente de IA conversacional que pode interagir com computadores para executar tarefas. Inspirado no OpenHands, oferece uma interface web completa com terminal integrado, editor de arquivos, navegação browser, e muito mais.

### 1.2 Objetivos
- Criar um agente de IA autônomo capaz de executar comandos e interagir com o sistema
- Fornecer interface web moderna e intuitiva
- Permitir integração com múltiplos provedores de LLM
- Suportar ferramentas nativas como terminal, editor de arquivos, git, e browser

### 1.3 Tecnologias
| Componente | Tecnologia |
|------------|------------|
| Backend | Python 3.10+ / FastAPI / WebSocket |
| Frontend | HTML5 / CSS3 / JavaScript (Vanilla) |
| LLM Integration | LiteLLM Proxy |
| Tunnel | Cloudflare Tunnel |
| Runtime | Debian 13 (Trixie) |

---

## 2. Arquitetura do Sistema

### 2.1 Diagrama de Arquitetura
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

### 2.2 Fluxo de Execução do Agente
```
1. User Input → "Abra o arquivo config.py"
         ↓
2. THINK: Agente analisa a entrada usando LLM
         ↓
3. ACTION: Seleciona ferramenta apropriada (FileEditor)
         ↓
4. OBSERVE: Executa ação e observa resultado
         ↓
5. Se necessário, repete THINK→ACTION→OBSERVE
         ↓
6. Response: Retorna resultado ao usuário
```

---

## 3. Especificação do Backend

### 3.1 Stack Técnico
- **Framework**: FastAPI 0.104+
- **WebSocket**: Starlette WebSocket
- **LLM**: LiteLLM Proxy
- **Python**: 3.10+

### 3.2 Endpoints da API

#### POST /api/chat
Envia mensagem e recebe resposta do agente.

**Request:**
```json
{
  "message": "string",
  "stream": false
}
```

**Response:**
```json
{
  "response": "string",
  "actions": [
    {
      "tool": "terminal",
      "command": "ls -la",
      "output": "..."
    }
  ]
}
```

#### GET /api/config
Retorna configurações do sistema.

**Response:**
```json
{
  "model": "string",
  "available_tools": ["terminal", "file_editor", "git", "browser", "think"],
  "system_info": {...}
}
```

#### WebSocket /ws
Conexão bidirecional para comunicação em tempo real.

**Mensagens do Cliente:**
```json
{
  "type": "message",
  "content": "string"
}
```

**Mensagens do Servidor:**
```json
{
  "type": "stream|action|complete|error",
  "content": "string",
  "data": {}
}
```

### 3.3 Modelos de Dados

#### ConversationMessage
```python
{
  "role": "user|assistant|system",
  "content": str,
  "timestamp": datetime
}
```

#### ToolCall
```python
{
  "tool": str,
  "action": str,
  "params": dict,
  "result": Any,
  "error": str | None
}
```

---

## 4. Especificação do Frontend

### 4.1 Estrutura de Arquivos
```
frontend/
└── index.html          # Aplicação completa (SPA)
```

### 4.2 Componentes da Interface

#### Header
- Logo "HANDS & HEAD" (SVG)
- Branding "by Fao Labs"
- Indicador de status (connected/disconnected)

#### Chat Window
- Área de mensagens com scroll automático
- Suporte a markdown
- Animações de digitação
- Timestamps

#### Terminal Panel
- Terminal emulado com xterm.js ou similar
- Suporte a ANSI colors
- Scrollback ilimitado
- Input interativo

#### File Tree
- Navegação hierárquica de arquivos
- Ícones por tipo de arquivo
- Preview de conteúdo
- Ações de contexto (criar, editar, deletar)

#### Settings Panel
- Configuração de API key
- Seleção de modelo
- Preferências de interface

### 4.3 Design System

#### Cores
| Nome | Hex | Uso |
|------|-----|-----|
| Primary | #6366F1 | Botões, links, acentos |
| Secondary | #8B5CF6 | Gradientes, destaques |
| Background | #0F172A | Fundo principal |
| Surface | #1E293B | Cards, painéis |
| Text Primary | #F8FAFC | Texto principal |
| Text Secondary | #94A3B8 | Texto secundário |
| Success | #22C55E | Status OK |
| Error | #EF4444 | Erros |
| Warning | #F59E0B | Avisos |

#### Tipografia
| Elemento | Font | Size | Weight |
|----------|------|------|--------|
| Logo | Inter | 24px | 700 |
| Heading | Inter | 18px | 600 |
| Body | Inter | 14px | 400 |
| Code | JetBrains Mono | 13px | 400 |

#### Espaçamento
- Base unit: 4px
- Padding padrão: 16px
- Gap entre elementos: 12px
- Border radius: 8px

---

## 5. Ferramentas (Tools)

### 5.1 TerminalTool
**Descrição**: Executa comandos no terminal do sistema

**Parâmetros:**
- `command` (str): Comando a executar
- `working_dir` (str, opcional): Diretório de trabalho

**Retorno:**
```json
{
  "stdout": "string",
  "stderr": "string",
  "exit_code": int
}
```

### 5.2 FileEditorTool
**Descrição**: Ler, criar e editar arquivos

**Operações:**
- `read`: Lê conteúdo de arquivo
- `write`: Criasobrescreve arquivo
- `edit`: Edita linhas específicas
- `create_dir`: Cria diretório
- `list_dir`: Lista conteúdo de diretório

**Parâmetros:**
- `path` (str): Caminho do arquivo
- `operation` (str): read|write|edit|create_dir|list_dir
- `content` (str, opcional): Conteúdo para escrever

### 5.3 GitTool
**Descrição**: Executa comandos git

**Operações:**
- `status`: Status do repositório
- `log`: Histórico de commits
- `diff`: Diferenças
- `commit`: Criar commit
- `push`: Enviar para remote
- `pull`: Baixar do remote

### 5.4 BrowserTool
**Descrição**: Navega e interage com páginas web

**Operações:**
- `navigate`: Abre URL
- `click`: Clica em elemento
- `type`: Digita em campo
- `scroll`: Rola a página
- `get_content`: Extrai conteúdo

### 5.5 ThinkTool
**Descrição**: Permite ao agente pensar reasoning internal

**Parâmetros:**
- `thought` (str): Pensamento a ser registrado

---

## 6. Integração LLM

### 6.1 LiteLLM Proxy Configuration
```yaml
model_list:
  - model_name: minimax-m2.7
    litellm_params:
      model: minimax/m2.7
      api_key: os.environ/MINIMAX_API_KEY

  - model_name: gpt-4o
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  - model_name: claude-3.5-sonnet
    litellm_params:
      model: anthropic/claude-3.5-sonnet
      api_key: os.environ/ANTHROPIC_API_KEY
```

### 6.2 System Prompt
```
You are HANDS & HEAD, an AI agent by Fao Labs that can interact with a computer to solve tasks.

Your capabilities:
- Execute terminal commands
- Read, write, and edit files
- Use git version control
- Browse the web
- Think and reason about problems

Always be thorough, methodical, and prioritize quality over speed.
```

---

## 7. Scripts de Deploy

### 7.1 setup.sh
Script de instalação e configuração inicial.

### 7.2 run.sh
Script para iniciar o servidor.

### 7.3 cloudflare-tunnel.sh
Script para criar túnel Cloudflare.

---

## 8. Estrutura de Diretórios
```
hands-head-fao-labs/
├── SPEC.md                 # Esta especificação
├── README.md               # Documentação do usuário
├── LICENSE                 # Licença MIT
├── requirements.txt        # Dependências Python
├── setup.sh               # Script de instalação
├── run.sh                 # Script de execução
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
    └── logo.svg           # Logo do projeto
```

---

## 9. Critérios de Aceitação

### 9.1 Funcionalidade
- [ ] Interface web carrega corretamente
- [ ] Chat aceita mensagens e retorna respostas
- [ ] Terminal executa comandos
- [ ] Editor de arquivos funciona (ler/escrever)
- [ ] WebSocket mantém conexão estável
- [ ] Logo e branding visíveis

### 9.2 Performance
- [ ] Tempo de resposta < 5s para mensagens simples
- [ ] Interface responsiva (60fps)
- [ ] Memória < 500MB em uso idle

### 9.3 Segurança
- [ ] API key não exposta no frontend
- [ ] Comandos restritos a operações seguras
- [ ] Rate limiting implementado

---

## 10. Roadmap

### v1.0 (Atual)
- Interface web básica
- Terminal integrado
- File editor básico
- Chat funcional

### v1.1
- Multi-provider LLM support
- Histórico de conversas
- Temas (dark/light)

### v1.2
- Compartilhamento de sessão
- Plugin system
- API REST completa

---

**Documento criado por:** OpenHands Agent
**Data:** 2026-06-09
**Versão:** 1.0