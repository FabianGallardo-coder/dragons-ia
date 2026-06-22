import pytest
from unittest.mock import patch, AsyncMock
from backend.services.ai_service import get_ai_response


@pytest.mark.asyncio
async def test_ollama_model_installed():
    """
    Ollama corriendo, modelo configurado SÍ está instalado
    → debe usar ese modelo, sin fallback, sin warnings.
    """
    with patch('backend.services.ai_service.check_ollama_status') as mock_check, \
         patch('litellm.acompletion') as mock_acompletion:
        # Mock check_ollama_status to return a running Ollama with the model installed
        mock_check.return_value = {
            "running": True,
            "models": ["dolphin-mistral:7b-v2.6-dpo-laser-q4_K_M", "llama3:8b"],
            "ram_available_gb": 8.0,
            "recommended_model": "dolphin-mistral:7b-v2.6-dpo-laser-q4_K_M",
            "os": "Linux",
            "os_friendly": "Linux",
            "install_instructions": "test instructions"
        }
        # Mock litellm.acompletion to return a dummy response
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_acompletion.return_value = mock_response

        # Call the function
        result = await get_ai_response(
            messages=[{"role": "user", "content": "Hello"}],
            model="ollama/dolphin-mistral:7b-v2.6-dpo-laser-q4_K_M"
        )

        # Assertions
        assert result == "Test response"
        # Check that the model used in the call is the one we passed (no fallback)
        mock_acompletion.assert_awaited_once()
        args, kwargs = mock_acompletion.call_args
        assert kwargs["model"] == "ollama/dolphin-mistral:7b-v2.6-dpo-laser-q4_K_M"


@pytest.mark.asyncio
async def test_ollama_model_not_installed_but_other_available():
    """
    Ollama corriendo, modelo configurado NO está instalado, pero hay otros modelos
    → debe loguear un warning y usar el modelo recomendado por recommend_model_for_ram(),
    y ese modelo debe estar en la lista de modelos instalados que devolvió el mock.
    """
    with patch('backend.services.ai_service.check_ollama_status') as mock_check, \
         patch('litellm.acompletion') as mock_acompletion, \
         patch('backend.services.ai_service.logger') as mock_logger:
        # Mock check_ollama_status to return a running Ollama with some models installed,
        # but the model we are going to ask for is not installed.
        # We set the RAM to 6.0 so that the recommended model is dolphin-phi.
        # We make sure that dolphin-phi is in the installed models list.
        mock_check.return_value = {
            "running": True,
            "models": ["llama3:8b", "dolphin-phi"],  # installed models
            "ram_available_gb": 6.0,
            "recommended_model": "dolphin-phi",
            "best_model": "dolphin-phi",  # Because for 6GB RAM, dolphin-phi is the best match
            "os": "Linux",
            "os_friendly": "Linux",
            "install_instructions": "test instructions"
        }
        # Mock litellm.acompletion to return a dummy response
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_acompletion.return_value = mock_response

        # Call the function with a model that is NOT installed (e.g., we ask for a model that is not in the list)
        result = await get_ai_response(
            messages=[{"role": "user", "content": "Hello"}],
            model="ollama/mistral:7b"  # This model is not in the installed models list
        )

        # Assertions
        assert result == "Test response"
        # Check that the model used in the call is the recommended model (dolphin-phi)
        mock_acompletion.assert_awaited_once()
        args, kwargs = mock_acompletion.call_args
        assert kwargs["model"] == "ollama/dolphin-phi"
        # Check that a warning was logged
        mock_logger.warning.assert_called_once()
        warning_args, _ = mock_logger.warning.call_args
        warning_message = warning_args[0]
        assert "mistral:7b" in warning_message
        assert "dolphin-phi" in warning_message


@pytest.mark.asyncio
async def test_ollama_no_models_installed():
    """
    Ollama corriendo pero sin NINGÚN modelo instalado
    → debe lanzar una excepción específica y clara (no un error genérico de conexión
    ni un 500 sin contexto), con un mensaje que incluya el comando exacto a ejecutar,
    ej: "ollama pull llama3.2:1b"
    """
    with patch('backend.services.ai_service.check_ollama_status') as mock_check:
        # Mock check_ollama_status to return a running Ollama but no models installed
        mock_check.return_value = {
            "running": True,
            "models": [],  # No models installed
            "ram_available_gb": 2.0,
            "recommended_model": "llama3.2:1b",  # Based on low RAM
            "os": "Linux",
            "os_friendly": "Linux",
            "install_instructions": "test instructions"
        }

        # Call the function and expect a RuntimeError
        with pytest.raises(RuntimeError) as exc_info:
            await get_ai_response(
                messages=[{"role": "user", "content": "Hello"}],
                model="ollama/llama3:8b"
            )

        # Check the exception message
        assert "No se encontró ningún modelo de Ollama instalado" in str(exc_info.value)
        assert "ollama pull llama3.2:1b" in str(exc_info.value)