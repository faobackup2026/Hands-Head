# Contributing to HANDS & HEAD

## Setup para Desenvolvimento

### 1. Clone o repositório
```bash
git clone https://github.com/faobackup2026/Hands-Head.git
cd Hands-Head
```

### 2. Execute o setup
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Ative o ambiente virtual
```bash
source venv/bin/activate
```

### 4. Configure o .env
```bash
cp .env.example .env
# Edite .env com suas chaves de API
```

## Rodando Testes

```bash
pytest
pytest --cov=backend  # Com cobertura
pytest -v            # Modo verbose
```

## Formatação de Código

```bash
# Format com Black
black backend/

# Lint com Flake8
flake8 backend/

# Type checking com Mypy
mypy backend/
```

## Estrutura de Commits

Use o padrão:
```
<tipo>: <descrição curta>

<descrição detalhada (opcional)>

Tipos:
- feat: Nova funcionalidade
- fix: Correção de bug
- docs: Mudanças na documentação
- style: Formatação, sem mudança de código
- refactor: Refatoração de código
- test: Adição ou modificação de testes
- chore: Mudanças em dependencias ou ferramentas
```

## Adicionando Novas Ferramentas

Para criar uma nova ferramenta:

1. Crie um novo arquivo em `backend/tools/`
2. Implemente a classe da ferramenta com método `__call__`
3. Registre em `backend/tools/__init__.py`
4. Adicione testes
5. Documente em SPEC.md

Exemplo:
```python
class MyTool:
    name = "my_tool"
    description = "Descrição"
    
    def __call__(self, param: str) -> dict:
        return {
            "success": True,
            "result": "..."
        }
```

## Pull Requests

1. Crie uma branch: `git checkout -b feature/sua-feature`
2. Faça commit das mudanças
3. Push para a branch: `git push origin feature/sua-feature`
4. Abra um Pull Request
5. Descreva o que foi mudado

## Código de Conduta

- Seja respeitoso
- Não faça spam
- Teste suas mudanças
- Documente seu código

## Suporte

Para dúvidas:
- Abra uma issue
- Verifique issues existentes
- Consulte a documentação em SPEC.md
