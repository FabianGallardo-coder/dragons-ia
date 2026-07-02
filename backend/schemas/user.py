"""Schemas Pydantic para usuarios."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """Schema para registro de usuario."""
    email: EmailStr
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    """Schema para login de usuario."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema de respuesta de usuario (sin password)."""
    id: str
    email: str
    username: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """Schema de respuesta con JWT."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ForgotPasswordRequest(BaseModel):
    """Schema para solicitar reset de contraseña."""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Schema para resetear contraseña."""
    token: str = Field(min_length=1)
    password: str = Field(min_length=6, max_length=128)
