#!/bin/bash

# HANDS & HEAD by Fao Labs
# Run Script

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║     🤝 HANDS & HEAD by Fao Labs - Starting Server          ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🚀 Ativando ambiente virtual..."
    source venv/bin/activate
else
    echo "⚠️  Ambiente virtual não encontrado. Execute setup.sh primeiro."
    exit 1
fi

# Load environment variables
if [ -f ".env" ]; then
    echo "📋 Carregando variáveis de ambiente..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  .env não encontrado. Usando valores padrão."
fi

# Check if dependencies are installed
echo ""
echo "🔍 Verificando dependências..."
if ! python3 -c "import fastapi, uvicorn" 2>/dev/null; then
    echo "❌ Dependências não estão instaladas"
    echo "Execute: pip install -r requirements.txt"
    exit 1
fi
echo "✅ Dependências OK"

# Start server
echo ""
echo "🚀 Iniciando servidor..."
echo ""
python3 -m backend.server
