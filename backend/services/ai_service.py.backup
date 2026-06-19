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

    # Validar que el modelo tenga un formato reconocido (previene basura de frontend)
    valid_prefixes = ("ollama/", "claude", "anthropic/", "openai/", "gpt-")
    if not any(target_model.startswith(p) for p in valid_prefixes):
        logger.warning("Modelo inválido recibido: %r, usando default", target_model)
        target_model = settings.default_ai_model

    # Construir kwargs
    kwargs: dict = {"model": target_model, "messages": messages, "max_tokens": 2048}

    if api_key:
        kwargs["api_key"] = api_key

    # Detectar proveedor y configurar api_base / auth
    if target_model.startswith("ollama/"):
        raw_model = target_model.removeprefix("ollama/")
        if api_key:
            # Ollama Cloud: usar endpoint OpenAI-compatible de ollama.com
            # LiteLLM's native Ollama handler no envía Authorization headers,
            # así que usamos el prefijo openai/ para que LiteLLM use el handler
            # de OpenAI que sí envía Bearer tokens.
            kwargs["model"] = f"openai/{raw_model}"
            kwargs["api_base"] = "https://ollama.com/v1"
        else:
            # Ollama Local: usar endpoint local nativo
            kwargs["api_base"] = settings.ollama_api_base
    elif target_model.startswith("claude"):
        # Asegurar que Anthropic reciba la API key
        if not api_key and settings.anthropic_api_key:
            kwargs["api_key"] = settings.anthropic_api_key

    logger.info("Llamando a modelo: %s (kwargs.model=%s)", target_model, kwargs["model"])

    try:
        response = await litellm.acompletion(**kwargs)
        msg = response.choices[0].message

        # Extraer contenido — algunos modelos "thinking" ponen el texto final
        # en content y el razonamiento en otro campo. Si content está vacío,
        # intentar extraer de campos alternativos.
        content = msg.content or ""

        # Fallback: buscar en campos de modelos thinking
        if not content.strip():
            # Algunos modelos devuelven reasoning_content o thinking
            for attr in ("reasoning_content", "thinking"):
                alt = getattr(msg, attr, None)
                if alt and alt.strip():
                    content = alt
                    break

        if not content.strip():
            logger.warning(
                "Respuesta vacía del modelo %s. Response: %s",
                target_model,
                response.model_dump_json()[:500] if hasattr(response, "model_dump_json") else str(response)[:500],
            )
            raise RuntimeError("El modelo retornó una respuesta vacía. Probá con otro modelo.")
        return content.strip()

    except RuntimeError:
        # Re-lanzar RuntimeErrors propios sin envolverlos
        raise

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
