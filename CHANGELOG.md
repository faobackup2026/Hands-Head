# Changelog

## [1.0.0] - 2026-06-12

### Added
- ✅ Backend FastAPI com WebSocket implementado
- ✅ LLM Client com integração LiteLLM
- ✅ Tools Registry com 5 ferramentas principais
- ✅ Agent com loop THINK → ACTION → OBSERVE
- ✅ Server com endpoints HTTP e WebSocket
- ✅ Rate limiting por IP
- ✅ Rate limiting middleware
- ✅ Logging estruturado
- ✅ Suite de testes com pytest
- ✅ CORS configurável por ambiente
- ✅ .env.example com variáveis de configuração
- ✅ setup.sh e run.sh para facilitar inicio

### Fixed
- ✅ Correção de tipo `any` para `Any` em config.py
- ✅ Remoção de flag `re.JSON` inválida em agent.py
- ✅ Implementação de tools_registry em __init__.py
- ✅ Criação de backend/llm/ module com client.py

### Security
- ✅ CORS restrito a hosts configuráveis
- ✅ Rate limiting implementado
- ✅ Validação de input em endpoints
- ✅ API keys em variáveis de ambiente
- ✅ Logging de erros estruturado

### Documentation
- ✅ CONTRIBUTING.md com guia para devs
- ✅ pytest.ini com configuração de testes
- ✅ .env.example com todas as variáveis
- ✅ Comments detalhados no código

## [0.1.0] - 2026-06-09

### Initial Release
- Frontend index.html básico
- README.md e SPEC.md
- Estrutura de projeto
- requirements.txt
