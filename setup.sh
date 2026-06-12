#!/bin/bash

# HANDS & HEAD by Fao Labs
# Setup Script

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║     🤝 HANDS & HEAD by Fao Labs - Setup Script             ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale Python 3.10 ou superior."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✅ Python $PYTHON_VERSION encontrado"

# Check if version is >= 3.10
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)'; then
    echo "❌ Python 3.10+ é requerido. Você tem $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
else
    echo "⏭️  Ambiente virtual já existe"
fi

# Activate virtual environment
echo ""
echo "🚀 Ativando ambiente virtual..."
source venv/bin/activate
echo "✅ Ambiente virtual ativado"

# Upgrade pip
echo ""
echo "📥 Atualizando pip..."
pip install --upgrade pip setuptools wheel
echo "✅ Pip atualizado"

# Install requirements
echo ""
echo "📚 Instalando dependências..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt não encontrado"
    exit 1
fi
pip install -r requirements.txt
echo "✅ Dependências instaladas"

# Create .env if not exists
echo ""
echo "⚙️  Configurando variáveis de ambiente..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ .env criado a partir de .env.example"
    echo "⚠️  Configure suas variáveis de ambiente em .env"
else
    echo "⏭️  .env já existe"
fi

# Create workspace directory
echo ""
echo "📁 Criando diretório de trabalho..."
mkdir -p workspace
echo "✅ Diretório de trabalho criado"

# Make scripts executable
echo ""
echo "🔐 Tornando scripts executáveis..."
chmod +x run.sh cloudflare-tunnel.sh setup.sh
echo "✅ Scripts tornados executáveis"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║     ✅ Setup concluído com sucesso!                        ║"
echo "║                                                            ║"
echo "║     Próximos passos:                                       ║"
echo "║     1. Configure seu .env com as chaves de API             ║"
echo "║     2. Execute: source venv/bin/activate                  ║"
echo "║     3. Execute: ./run.sh                                   ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
