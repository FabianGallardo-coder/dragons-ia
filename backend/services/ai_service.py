"""
Servicio de IA — Abstracción sobre LiteLLM.

Maneja llamadas a cualquier modelo de IA (Anthropic, Ollama Cloud, Ollama Local)
a través de LiteLLM con manejo de errores y fallbacks.
"""

import logging
import os

import litellm

from backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Desactivar logs excesivos de LiteLLM
litellm.set_verbose = False


async def get_ai_response(
    messages: list[dict],
    model: str | None = None,
    api_key: str | None = None,
) -> str:
    """
    Envía mensajes al modelo de IA y retorna la respuesta narrativa.

    Args:
        messages: Lista de mensajes [{role, content}].
        model: Modelo a usar (override del default).
        api_key: API key específica (override de las de entorno).

    Returns:
        Texto de respuesta del modelo.

    Raises:
        RuntimeError: Si el modelo no responde o hay un error irrecuperable.
    """
    target_model = model or settings.default_ai_model

    # Construir kwargs
    kwargs: dict = {"model": target_model, "messages": messages, "max_tokens": 600}

    if api_key:
        kwargs["api_key"] = api_key

    # Detectar si es Ollama y configurar api_base
    if target_model.startswith("ollama/"):
        if api_key:
            # Ollama Cloud: usar endpoint remoto
            kwargs["api_base"] = "https://api.ollama.com"
        else:
            # Ollama Local: usar endpoint local
            kwargs["api_base"] = settings.ollama_api_base
    elif target_model.startswith("claude"):
        # Asegurar que Anthropic reciba la API key
        if not api_key and settings.anthropic_api_key:
            kwargs["api_key"] = settings.anthropic_api_key

    logger.info("Llamando a modelo: %s", target_model)

    try:
        response = await litellm.acompletion(**kwargs)
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("El modelo retornó una respuesta vacía.")
        return content.strip()

    except litellm.exceptions.AuthenticationError:
        logger.error("Error de autenticación con el modelo %s", target_model)
        raise RuntimeError(
            "Error de autenticación. Verificá tu API Key en Configuración."
        )

    except litellm.exceptions.RateLimitError:
        logger.warning("Rate limit alcanzado en el modelo %s", target_model)
        raise RuntimeError(
            "Se alcanzó el límite de solicitudes. Intenta de nuevo en unos segundos."
        )

    except litellm.exceptions.APIConnectionError as exc:
        logger.error("Error de conexión con el modelo %s: %s", target_model, exc)
        if target_model.startswith("ollama/"):
            raise RuntimeError(
                "No se pudo conectar con Ollama. "
                "Si usás Ollama Local, verificá que esté corriendo. "
                "Si usás Ollama Cloud, verificá tu API Key."
            )
        raise RuntimeError(
            f"No se pudo conectar con el proveedor de IA ({target_model}). "
            "Verificá tu API Key y conexión a internet."
        )

    except Exception as exc:
        logger.exception("Error inesperado al llamar al modelo %s", target_model)
        raise RuntimeError(f"Error al comunicarse con la IA: {exc}") from exc
