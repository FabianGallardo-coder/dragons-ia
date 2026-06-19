"""
Verificación de sistema — Detecta SO, estado de Ollama y RAM disponible.
Usado para dar diagnóstico claro al usuario cuando Ollama no está disponible
o no tiene el modelo configurado, y para recomendar modelos según hardware.
"""

import platform
import logging
import httpx
import psutil

logger = logging.getLogger(__name__)

OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"
OLLAMA_TIMEOUT_SECONDS = 3.0


def get_os_info() -> dict:
    """
    Detecta el sistema operativo actual y retorna información útil
    para dar instrucciones de instalación de Ollama específicas.

    Returns:
        dict con: os (raw de platform.system()), os_friendly (nombre legible),
        install_instructions (comando o link de instalación).
    """
    sistema = platform.system()  # 'Windows', 'Linux', 'Darwin'

    nombres_legibles = {
        "Windows": "Windows",
        "Linux": "Linux",
        "Darwin": "macOS",
    }

    instrucciones_instalacion = {
        "Windows": "Descargá el instalador desde https://ollama.ai/download/windows",
        "Linux": "Ejecutá: curl -fsSL https://ollama.ai/install.sh | sh",
        "Darwin": "Ejecutá: brew install ollama   (o descargá desde https://ollama.ai/download/mac)",
    }

    return {
        "os": sistema,
        "os_friendly": nombres_legibles.get(sistema, sistema),
        "install_instructions": instrucciones_instalacion.get(
            sistema, "Visitá https://ollama.ai para instrucciones de instalación"
        ),
    }


def get_available_ram_gb() -> float:
    """
    Retorna la memoria RAM disponible (no la total) en gigabytes,
    redondeada a 1 decimal. Se usa para recomendar qué modelo correr.
    """
    memoria = psutil.virtual_memory()
    return round(memoria.available / (1024 ** 3), 1)


def recommend_model_for_ram(ram_gb: float) -> str:
    """
    Recomienda un modelo de Ollama según la RAM disponible.
    Los umbrales son conservadores para dejar margen al sistema operativo
    y al resto de la aplicación corriendo en paralelo.

    Args:
        ram_gb: RAM disponible en GB (no total del sistema).

    Returns:
        Nombre del modelo recomendado, tal como se usa en `ollama pull <modelo>`.
    """
    if ram_gb >= 8.0:
        return "dolphin-mistral:7b-v2.6-dpo-laser-q4_K_M"
    elif ram_gb >= 4.0:
        return "dolphin-phi"
    else:
        return "llama3.2:1b"


async def check_ollama_status() -> dict:
    """
    Verifica si el servidor de Ollama está corriendo en localhost:11434
    y, si está activo, qué modelos tiene instalados.

    NUNCA lanza excepción: si Ollama no responde, retorna running=False
    junto con la información de SO e instrucciones de instalación/inicio.

    Returns:
        dict con: running (bool), models (list[str]), ram_available_gb (float),
        recommended_model (str), y si running=False también os_info completo.
    """
    ram_disponible = get_available_ram_gb()
    modelo_recomendado = recommend_model_for_ram(ram_disponible)

    try:
        async with httpx.AsyncClient(timeout=OLLAMA_TIMEOUT_SECONDS) as client:
            response = await client.get(OLLAMA_TAGS_URL)
            if response.status_code == 200:
                data = response.json()
                modelos_instalados = [m["name"] for m in data.get("models", [])]
                return {
                    "running": True,
                    "models": modelos_instalados,
                    "ram_available_gb": ram_disponible,
                    "recommended_model": modelo_recomendado,
                }
    except (httpx.ConnectError, httpx.TimeoutException) as e:
        logger.info(f"Ollama no disponible en {OLLAMA_TAGS_URL}: {e}")
    except Exception as e:
        logger.warning(f"Error inesperado verificando Ollama: {e}")

    return {
        "running": False,
        "models": [],
        "ram_available_gb": ram_disponible,
        "recommended_model": modelo_recomendado,
        **get_os_info(),
    }