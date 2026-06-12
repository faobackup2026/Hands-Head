# 🌐 Como Acessar HANDS & HEAD via Cloudflare Tunnel

## 📋 Resumo

Você pode acessar seu HANDS & HEAD de qualquer lugar do mundo via Cloudflare Tunnel!

Existem 2 opções:
1. **RÁPIDO** - Túnel temporário (perfeito para testes)
2. **PERMANENTE** - Com domínio customizado (para produção)

---

## 🚀 Opção 1: Túnel RÁPIDO (Sem Configuração)

### Pré-requisitos
- ✅ Servidor rodando (`./run.sh`)
- ✅ Cloudflared instalado (script instala automaticamente)

### Passos

```bash
# 1. Faça seu servidor estar rodando em outro terminal
./run.sh

# 2. Em um novo terminal, execute:
chmod +x cloudflare-tunnel.sh
./cloudflare-tunnel.sh

# 3. Escolha opção 1 (RÁPIDO)

# 4. Você receberá um link como:
# https://xxxxx.trycloudflare.com
```

### Características
- ⚡ Instantâneo (nenhuma configuração)
- ⏱️ Válido por 24 horas
- 🔒 HTTPS automático
- 🌍 Acessível globalmente
- ❌ Sem domínio customizado

### Exemplo de Acesso
```
https://abc123def456.trycloudflare.com
wss://abc123def456.trycloudflare.com/ws
```

---

## 🔐 Opção 2: Túnel PERMANENTE (Com Domínio)

### Pré-requisitos
- ✅ Conta Cloudflare (gratuita em https://www.cloudflare.com)
- ✅ Um domínio registrado (pode usar em Cloudflare ou transferir)
- ✅ Servidor rodando (`./run.sh`)

### Passos

#### 1️⃣ Setup Inicial
```bash
chmod +x cloudflare-tunnel.sh
./cloudflare-tunnel.sh

# Escolha opção 2 (PERMANENTE)
# Você será redirecionado para fazer login no Cloudflare
```

#### 2️⃣ Fazer Login
```bash
# O script abrirá seu navegador
# Faça login na sua conta Cloudflare
# Autorize o cloudflared
# Você receberá um código de confirmação
```

#### 3️⃣ Criar o Túnel
```bash
# Digite um nome para o túnel (ex: hands-head-api)
# O script criará automaticamente
```

#### 4️⃣ Configurar DNS
```
1. Acesse https://dash.cloudflare.com/
2. Selecione seu domínio
3. Vá para DNS > Records
4. Crie um CNAME record:
   
   Nome: api (ou seu_subdomain)
   Tipo: CNAME
   Conteúdo: [tunnel_name].cfargotunnel.com
   Proxied: SIM (ícone laranja)
```

#### 5️⃣ Iniciar Túnel
```bash
cloudflared tunnel run hands-head-api
```

### Características
- ✅ Domínio customizado (api.seu-dominio.com)
- ✅ HTTPS com SSL automático
- ✅ Permanente (enquanto rodando)
- 🔒 Protegido por Cloudflare
- 🌍 Acessível globalmente

### Exemplo de Acesso
```
https://api.seu-dominio.com
wss://api.seu-dominio.com/ws
https://api.seu-dominio.com/api/docs
```

---

## 📊 Comparação

| Recurso | Rápido | Permanente |
|---------|--------|-----------|
| Setup | < 1 minuto | 5-10 minutos |
| URL permanente | ❌ | ✅ |
| Domínio customizado | ❌ | ✅ |
| Válido por | 24 horas | Indefinido |
| HTTPS | ✅ | ✅ |
| Perfeito para | Testes | Produção |
| Requer conta CF | ❌ | ✅ |

---

## 🧪 Testando via Cloudflare

### 1. Via Web
```
Acesse seu link no navegador
https://seu-link.trycloudflare.com
```

### 2. Via API
```bash
# Health check
curl https://seu-link.trycloudflare.com/api/health

# Config
curl https://seu-link.trycloudflare.com/api/config

# Listar ferramentas
curl https://seu-link.trycloudflare.com/api/tools
```

### 3. Via WebSocket (JavaScript)
```javascript
const ws = new WebSocket('wss://seu-link.trycloudflare.com/ws');

ws.onopen = () => {
    console.log('Conectado!');
    ws.send(JSON.stringify({
        type: 'message',
        content: 'Olá HANDS & HEAD!'
    }));
};

ws.onmessage = (event) => {
    console.log('Resposta:', event.data);
};
```

### 4. Via Python
```python
import requests
import asyncio
import websockets
import json

# HTTP Request
response = requests.get('https://seu-link.trycloudflare.com/api/health')
print(response.json())

# WebSocket
async def test_ws():
    async with websockets.connect('wss://seu-link.trycloudflare.com/ws') as ws:
        await ws.send(json.dumps({
            'type': 'message',
            'content': 'Olá!'
        }))
        response = await ws.recv()
        print(response)

asyncio.run(test_ws())
```

---

## 🔧 Troubleshooting

### Erro: "cloudflared not found"
```bash
# Instale manualmente:
# Linux: https://github.com/cloudflare/cloudflared/releases/download/2024.1.0/cloudflared-linux-amd64.deb
# macOS: brew install cloudflare/cloudflare/cloudflared
# Windows: https://github.com/cloudflare/cloudflared/releases
```

### Erro: "Connection refused"
```bash
# Certifique-se de que o servidor está rodando:
./run.sh

# Em outro terminal, rode o tunnel:
./cloudflare-tunnel.sh
```

### Erro: "Auth required"
```bash
# Fazer login novamente:
cloudflared tunnel login

# Depois criar/rodar o túnel
```

### Túnel desconectou
```bash
# Cloudflare reconecta automaticamente
# Se não reconectar, reinicie:
cloudflared tunnel run seu-tunnel-name
```

---

## 📱 Acessar de Mobile

```
1. Copie o URL do seu túnel
2. Acesse no navegador do seu telefone
3. Tudo funciona normalmente!
```

---

## 🔒 Segurança

### Boas Práticas
- ✅ Cloudflare protege com DDoS
- ✅ HTTPS automático
- ✅ Rate limiting habilitado
- ✅ Validação de input
- ✅ Logging de todas requisições

### Adicional (Opcional)
```bash
# Adicionar autenticação HTTP básica
# Editar arquivo de configuração do tunnel
# https://developers.cloudflare.com/cloudflare-one/connections/connect-applications/configuration/
```

---

## 📚 Recursos Úteis

- 📖 Docs Cloudflare: https://developers.cloudflare.com/cloudflare-one/
- 🔑 Dashboard: https://dash.cloudflare.com/
- 💬 Comunidade: https://community.cloudflare.com/
- 📞 Support: https://support.cloudflare.com/

---

## 💡 Exemplos Práticos

### Exemplo 1: Compartilhar com Equipe
```bash
# 1. Setup rápido
./cloudflare-tunnel.sh
# Escolha 1

# 2. Compartilhe o link
# https://xxx.trycloudflare.com

# 3. Todos podem acessar por 24 horas
```

### Exemplo 2: API em Produção
```bash
# 1. Setup permanente com domínio
./cloudflare-tunnel.sh
# Escolha 2

# 2. Configure DNS como indicado

# 3. Sua API está em:
# https://api.seu-dominio.com
# Acessível 24/7
```

### Exemplo 3: Deploy com GitHub Actions (Futuro)
```yaml
- name: Start Cloudflare Tunnel
  run: |
    cloudflared tunnel create hands-head-prod
    cloudflared tunnel route dns hands-head-prod api.seu-dominio.com
    cloudflared tunnel run hands-head-prod
```

---

**Seu HANDS & HEAD agora está acessível de qualquer lugar! 🚀**
