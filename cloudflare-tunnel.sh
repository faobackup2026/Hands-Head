#!/bin/bash

# HANDS & HEAD by Fao Labs
# Script para criar túnel Cloudflare e acessar remotamente

set -e

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║     🌐 HANDS & HEAD - Cloudflare Tunnel Setup                ║"
echo "║                                                               ║"
echo "║     Acesse seu HANDS & HEAD de qualquer lugar!               ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

PORT=${PORT:-12000}
TUNNEL_NAME=${TUNNEL_NAME:-"hands-head-$(date +%s)"}

# 1. Verificar cloudflared
echo "🔍 Verificando cloudflared..."
if ! command -v cloudflared &> /dev/null; then
    echo "📥 cloudflared não encontrado. Instalando..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "📦 Instalando para Linux..."
        curl -L --output /tmp/cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
        sudo dpkg -i /tmp/cloudflared.deb
        rm /tmp/cloudflared.deb
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "🍎 Instalando para macOS..."
        brew install cloudflare/cloudflare/cloudflared
    else
        echo "❌ SO não suportado!"
        echo "Instale manualmente: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"
        exit 1
    fi
    echo "✅ cloudflared instalado"
else
    echo "✅ cloudflared encontrado"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║     Escolha um tipo de túnel:                                 ║"
echo "║                                                               ║"
echo "║     1️⃣  RÁPIDO: Túnel temporário (sem configuração)           ║"
echo "║     2️⃣  PERMANENTE: Túnel com domínio customizado            ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

read -p "Escolha (1 ou 2): " choice

if [ "$choice" = "1" ]; then
    
    echo ""
    echo "🚀 Iniciando túnel RÁPIDO (temporário)..."
    echo ""
    echo "📝 Seu servidor será acessível via link Cloudflare"
    echo "⏱️  O link expira em 24 horas ou quando você encerrar"
    echo ""
    echo "🔴 IMPORTANTE: Mantenha este terminal aberto!"
    echo ""
    echo "Iniciando em 3 segundos..."
    sleep 3
    echo ""
    
    cloudflared tunnel --url http://localhost:${PORT}
    
elif [ "$choice" = "2" ]; then
    
    echo ""
    echo "🔐 Configurando túnel PERMANENTE..."
    echo ""
    
    # Verificar se já está logado
    if [ ! -f ~/.cloudflared/cert.pem ]; then
        echo "📝 Você será redirecionado para fazer login no Cloudflare."
        echo "Após o login, volte aqui para continuar."
        echo ""
        read -p "Pressione ENTER para continuar..."
        
        cloudflared tunnel login
        echo "✅ Login realizado!"
    else
        echo "✅ Você já está logado no Cloudflare"
    fi
    
    echo ""
    read -p "Digite um nome para o túnel (ex: hands-head-api): " tunnel_name
    tunnel_name=${tunnel_name:-$TUNNEL_NAME}
    
    echo ""
    echo "📝 Criando túnel: $tunnel_name"
    cloudflared tunnel create $tunnel_name
    
    echo ""
    echo "✅ Túnel criado com sucesso!"
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo "📚 PRÓXIMOS PASSOS:"
    echo "════════════════════════════════════════════════════════════"
    echo ""
    echo "1️⃣  Acesse: https://dash.cloudflare.com/"
    echo ""
    echo "2️⃣  Selecione seu domínio (você precisa de um domínio em"
    echo "    Cloudflare ou transferir um)"
    echo ""
    echo "3️⃣  Vá para DNS > Records"
    echo ""
    echo "4️⃣  Crie um CNAME record:"
    echo "    Nome: $tunnel_name (ou subdomain desejado)"
    echo "    Tipo: CNAME"
    echo "    Conteúdo: $tunnel_name.cfargotunnel.com"
    echo "    Proxied: SIM (ícone laranja)"
    echo ""
    echo "5️⃣  Para iniciar o túnel, execute:"
    echo ""
    echo "    cloudflared tunnel run $tunnel_name"
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo ""
    echo "💡 DICA: Você pode adicionar variáveis de ambiente no .env:"
    echo "   TUNNEL_NAME=$tunnel_name"
    echo ""
    
    read -p "Deseja iniciar o túnel agora? (s/n): " start_tunnel
    
    if [[ $start_tunnel == "s" || $start_tunnel == "S" ]]; then
        echo ""
        echo "🚀 Iniciando túnel permanente..."
        echo ""
        echo "🔴 IMPORTANTE: Mantenha este terminal aberto!"
        echo ""
        sleep 2
        cloudflared tunnel run $tunnel_name
    fi
    
else
    echo "❌ Opção inválida"
    exit 1
fi
