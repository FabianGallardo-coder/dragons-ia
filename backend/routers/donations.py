"""
Router de donaciones — Retorna links de PayPal y MercadoPago.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.config import get_settings

router = APIRouter()
settings = get_settings()


class DonationInfo(BaseModel):
    """Schema de respuesta de donaciones."""
    paypal_url: str | None = None
    mercadopago_url: str | None = None
    message: str = ""


@router.get("/info", response_model=DonationInfo)
async def donations_info():
    """Retorna los links de donación configurados."""
    return DonationInfo(
        paypal_url=settings.paypal_donate_link or None,
        mercadopago_url=settings.mercadopago_donate_link or None,
        message="¡Gracias por apoyar Dragons & IA! Tu donación nos ayuda a seguir desarrollando.",
    )
