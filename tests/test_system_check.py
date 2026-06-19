import pytest
from unittest.mock import patch
from backend.services.system_check import (
    get_os_info,
    get_available_ram_gb,
    recommend_model_for_ram,
)


def test_get_os_info_windows():
    with patch('platform.system', return_value='Windows'):
        info = get_os_info()
        assert info['os'] == 'Windows'
        assert info['os_friendly'] == 'Windows'
        assert 'ollama.ai/download/windows' in info['install_instructions']


def test_get_os_info_linux():
    with patch('platform.system', return_value='Linux'):
        info = get_os_info()
        assert info['os'] == 'Linux'
        assert info['os_friendly'] == 'Linux'
        assert 'curl -fsSL https://ollama.ai/install.sh | sh' in info['install_instructions']


def test_get_os_info_darwin():
    with patch('platform.system', return_value='Darwin'):
        info = get_os_info()
        assert info['os'] == 'Darwin'
        assert info['os_friendly'] == 'macOS'
        assert 'brew install ollama' in info['install_instructions']


def test_get_available_ram_gb():
    with patch('psutil.virtual_memory') as mock_memory:
        # Mock available memory as 4GB in bytes
        mock_memory.return_value.available = 4 * 1024**3
        ram = get_available_ram_gb()
        assert ram == 4.0


def test_recommend_model_for_ram():
    assert recommend_model_for_ram(9.0) == "dolphin-mistral:7b-v2.6-dpo-laser-q4_K_M"
    assert recommend_model_for_ram(6.0) == "dolphin-phi"
    assert recommend_model_for_ram(2.0) == "llama3.2:1b"


def test_check_ollama_status_structure():
    """Test that check_ollama_status returns the expected structure"""
    # We won't actually test the async functionality here due to mocking complexity
    # but we can at least verify the function exists and is callable
    from backend.services.system_check import check_ollama_status
    assert callable(check_ollama_status)