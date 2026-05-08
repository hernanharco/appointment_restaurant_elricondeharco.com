"""
Schemas para la configuración del restaurante.
Define la estructura de datos para la API de configuración.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RestaurantConfigBase(BaseModel):
    """Base schema para RestaurantConfig."""
    name: str = Field(..., description="Nombre del restaurante")
    max_capacity: int = Field(..., gt=0, description="Capacidad máxima del restaurante")
    time_slot_duration_minutes: int = Field(30, gt=0, description="Duración de cada slot en minutos")
    max_party_size: int = Field(10, gt=0, description="Tamaño máximo de grupo permitido")
    min_party_size: int = Field(1, gt=0, description="Tamaño mínimo de grupo permitido")
    is_active: bool = Field(True, description="Si la configuración está activa")


class RestaurantConfigCreate(RestaurantConfigBase):
    """Schema para crear una nueva configuración."""
    pass


class RestaurantConfigRead(RestaurantConfigBase):
    """Schema para leer configuración del restaurante."""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RestaurantConfigUpdate(BaseModel):
    """Schema para actualizar una configuración existente."""
    name: Optional[str] = None
    max_capacity: Optional[int] = Field(None, gt=0, description="Capacidad máxima del restaurante")
    time_slot_duration_minutes: Optional[int] = Field(None, gt=0, description="Duración de cada slot en minutos")
    max_party_size: Optional[int] = Field(None, gt=0, description="Tamaño máximo de grupo permitido")
    min_party_size: Optional[int] = Field(None, gt=0, description="Tamaño mínimo de grupo permitido")
    is_active: Optional[bool] = None
