"""
Tests para as ferramentas
"""
import pytest
from backend.tools import tools_registry


def test_tools_registry_initialization():
    """Testa inicialização do registry"""
    assert tools_registry is not None
    tools = tools_registry.list_tools()
    assert len(tools) > 0


def test_list_tools():
    """Testa listagem de ferramentas"""
    tools = tools_registry.list_tools()
    assert isinstance(tools, list)
    tool_names = [t["name"] for t in tools]
    expected = ["terminal", "file_editor", "git", "browser", "think"]
    for expected_tool in expected:
        assert expected_tool in tool_names


def test_get_tool():
    """Testa obtenção de ferramenta"""
    tool = tools_registry.get("terminal")
    assert tool is not None
    tool_not_found = tools_registry.get("inexistente")
    assert tool_not_found is None


def test_execute_nonexistent_tool():
    """Testa execução de ferramenta inexistente"""
    result = tools_registry.execute("inexistente", param="valor")
    assert result["success"] == False
    assert "error" in result
