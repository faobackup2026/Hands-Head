#!/bin/bash
# HANDS & HEAD by Fao Labs
# Script de Instalação

set -e

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║     🤝 HANDS & HEAD by Fao Labs - INSTALLER              ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Python
echo -e "${YELLOW}Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 não encontrado. Instale Python 3.10 ou superior.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}Python $PYTHON_VERSION encontrado${NC}"

# Verificar pip
echo -e "${YELLOW}Verificando pip...${NC}"
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}pip3 não encontrado.${NC}"
    exit 1
fi
echo -e "${GREEN}pip encontrado${NC}"

# Criar ambiente virtual (opcional)
if [ ! -d "venv" ]; then
    echo ""
    echo -e "${YELLOW}Criar ambiente virtual? (recomendado)${NC}"
    read -p "Pressione ENTER para criar ou 'n' para pular: " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        python3 -m venv venv
        source venv/bin/activate
        echo -e "${GREEN}Ambiente virtual criado e ativado${NC}"
    fi
fi

# Instalar dependências
echo ""
echo -e "${YELLOW}Instalando dependências...${NC}"
pip install -r requirements.txt

# Verificar instalação
echo ""
echo -e "${YELLOW}Verificando instalação...${NC}"
python3 -c "import fastapi; import uvicorn; import litellm" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Todas as dependências instaladas com sucesso!${NC}"
else
    echo -e "${RED}Erro ao instalar dependências${NC}"
    exit 1
fi

# Criar diretórios necessários
echo ""
echo -e "${YELLOW}Criando diretórios...${NC}"
mkdir -p backend/tools backend/llm frontend static

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗"
echo -e "║                                                           ║"
echo -e "║     ✅ INSTALAÇÃO CONCLUÍDA!                             ║"
echo -e "║                                                           ║"
echo -e "║     Para iniciar o servidor, execute:                     ║"
echo -e "║     ${YELLOW}./run.sh${GREEN}                                              ║"
echo -e "║                                                           ║"
echo -e "╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""