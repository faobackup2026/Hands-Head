"""
Tests para o Agent
"""
import pytest
from backend.agent import Agent


@pytest.fixture
def agent():
    """Cria uma instância do agent para testes"""
    return Agent()


def test_agent_initialization(agent):
    """Testa inicialização do agent"""
    assert agent is not None
    assert agent.conversation_history == []
    assert agent.max_iterations == 20
    assert agent.current_iteration == 0


def test_parse_tool_calls(agent):
    """Testa parsing de chamadas de ferramentas"""
    text = "<think>Vou pensar sobre isso</think>"
    calls = agent.parse_tool_calls(text)
    assert isinstance(calls, list)


def test_parse_params(agent):
    """Testa parsing de parâmetros"""
    params_str = "command=ls -la|path=/home"
    params = agent._parse_params(params_str)
    assert params["command"] == "ls -la"
    assert params["path"] == "/home"


def test_agent_reset(agent):
    """Testa reset do agent"""
    agent.conversation_history = [{"role": "user", "content": "test"}]
    agent.current_iteration = 5
    agent.reset()
    assert agent.conversation_history == []
    assert agent.current_iteration == 0
