#!/bin/bash
# HANDS & HEAD by Fao Labs
# Script de Execução

set -e

# Carregar ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Configurações
PORT=${PORT:-12000}
HOST=${HOST:-0.0.0.0}

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║     🤝 HANDS & HEAD by Fao Labs                          ║"
echo "║                                                           ║"
echo "║     🌐 http://localhost:${PORT}                             ║"
echo "║     📡 WebSocket: ws://localhost:${PORT}/ws                 ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Verificar dependências
python3 -c "import fastapi" 2>/dev/null || {
    echo "Erro: Dependências não instaladas. Execute ./setup.sh primeiro."
    exit 1
}

# Exportar variáveis
export PORT
export HOST

# Executar servidor
python3 -m uvicorn backend.server:app --host ${HOST} --port ${PORT} --log-level info