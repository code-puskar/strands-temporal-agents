import pytest
from unittest.mock import patch, MagicMock
from temporal_agent import (
    read_file_activity,
    list_files_activity,
    get_time_activity,
    strands_chat_activity
)


@pytest.mark.asyncio
async def test_read_file_not_found():
    """Test handling of missing files."""
    result = await read_file_activity("missing.txt")
    assert "File not found" in result


@pytest.mark.asyncio
async def test_list_files():
    """Test directory listing."""
    result = await list_files_activity(".")
    assert "config.py" in result


@pytest.mark.asyncio
async def test_get_time_format():
    """Test time format is correct."""
    result = await get_time_activity()
    assert len(result) == 19
    assert "-" in result and ":" in result


@pytest.mark.asyncio
@patch('strands.Agent')
async def test_strands_chat_mock(mock_agent_class):
    """Test Strands chat with mocked agent."""
    mock_agent = MagicMock()
    mock_agent.return_value = "test response"
    mock_agent_class.return_value = mock_agent
    
    result = await strands_chat_activity("test prompt")
    assert result == "test response"
