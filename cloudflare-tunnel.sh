#!/bin/bash
# HANDS & HEAD by Fao Labs
# Script para criar túnel Cloudflare

set -e

TUNNEL_NAME=${TUNNEL_NAME:-"hands-head-tunnel"}
PORT=${PORT:-12000}

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║     🌐 HANDS & HEAD - Cloudflare Tunnel                   ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Verificar cloudflared
if ! command -v cloudflared &> /dev/null; then
    echo "Instalando cloudflared..."
    
    if command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        curl -L --output /tmp/cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
        sudo dpkg -i /tmp/cloudflared.deb
    elif command -v brew &> /dev/null; then
        # macOS
        brew install cloudflare/cloudflare/cloudflared
    else:
        echo "Instale cloudflared manualmente: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"
        exit 1
    fi
fi

echo "Criando túnel Cloudflare..."

# Criar túnel
cloudflared tunnel create ${TUNNEL_NAME} 2>/dev/null || true

# Obter túnel ID
TUNNEL_ID=$(cloudflared tunnel list --output json 2>/dev/null | grep -o "\"ID\":\"[^\"]*\"" | head -1 | cut -d'"' -f4)

if [ -z "$TUNNEL_ID" ]; then
    echo "Erro ao criar túnel. Verifique suas credenciais Cloudflare."
    exit 1
fi

echo ""
echo -e "${GREEN}Túnel criado com sucesso!${NC}"
echo "Tunnel ID: $TUNNEL_ID"
echo ""
echo "Agora configure seu túnel no dashboard Cloudflare Zero Trust"
echo "e execute: cloudflared tunnel run --url http://localhost:${PORT} ${TUNNEL_NAME}"
echo ""
echo "Ou use o comando quick: cloudflared tunnel --url http://localhost:${PORT}"