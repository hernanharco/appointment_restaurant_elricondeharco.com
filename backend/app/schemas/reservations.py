import re
from typing import Optional, List
from datetime import datetime, date
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    ValidationInfo,
    ConfigDict,
    computed_field,
)
from app.models.reservations import ReservationStatus


# Esta clase es la base para crear y actualizar reservas
class ReservationBase(BaseModel):
    # --- CAMBIO CLAVE: Eliminamos service_id y collaborator_id ---
    # --- NUEVO CAMPO: party_size ---
    party_size: int = Field(..., ge=1, le=20, description="Número de personas en la reserva")
    
    client_name: str = Field(..., min_length=1, max_length=100)
    client_phone: Optional[str] = Field(None, max_length=20)
    client_email: Optional[str] = Field(None, max_length=255)
    client_notes: Optional[str] = Field(None, max_length=1000)
    start_time: datetime
    end_time: datetime
    source: Optional[str] = Field(
        "manual", max_length=50
    )  # Por defecto "manual", pero se puede sobreescribir

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def clean_tz_info(cls, v):
        if isinstance(v, str):
            # Si viene como string, lo convertimos a datetime primero
            v = datetime.fromisoformat(v.replace("Z", "+00:00"))
        if isinstance(v, datetime):
            return v.replace(tzinfo=None)
        return v


# Esta clase es la que se usa para crear una reserva
class ReservationCreate(ReservationBase):
    pass  # No necesita validaciones adicionales


# Esta clase es la que se devuelve cuando se lee una reserva
class ReservationRead(BaseModel):
    # Campos que existen en la base de datos
    id: int
    client_id: Optional[int] = None
    client_name: str
    client_phone: Optional[str] = None
    client_email: Optional[str] = None
    client_notes: Optional[str] = None
    party_size: int
    start_time: datetime
    end_time: datetime
    status: ReservationStatus
    created_at: datetime
    updated_at: datetime
    source: str

    # --- PROPIEDAD CALCULADA ---
    @computed_field
    @property
    def is_active(self) -> bool:
        # Esta lógica debe coincidir con la de tu modelo
        return self.status in [ReservationStatus.SCHEDULED, ReservationStatus.CONFIRMED]

    # Configuración para Pydantic v2
    model_config = ConfigDict(from_attributes=True)


# Esta clase es la que se usa para actualizar una reserva
class ReservationUpdate(BaseModel):
    party_size: Optional[int] = None
    client_name: Optional[str] = None
    client_phone: Optional[str] = None
    client_email: Optional[str] = None
    client_notes: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[ReservationStatus] = None

    @field_validator("start_time", "end_time")
    @classmethod
    def clean_update_times(cls, v: Optional[datetime]):
        if v is None:
            return v
        return v.replace(tzinfo=None) if v.tzinfo else v


# --- Esquemas para disponibilidad de restaurante ---
class AvailableTimeSlot(BaseModel):
    start_time: datetime
    end_time: datetime
    available_capacity: int
    total_capacity: int


class RestaurantAvailabilityResponse(BaseModel):
    date: str
    party_size: int
    available_slots: List[AvailableTimeSlot]
    total_slots: int
    restaurant_config: dict


class RestaurantConfigRead(BaseModel):
    id: int
    name: str
    max_capacity: int
    time_slot_duration_minutes: int
    max_party_size: int
    min_party_size: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class RestaurantConfigUpdate(BaseModel):
    name: Optional[str] = None
    max_capacity: Optional[int] = None
    time_slot_duration_minutes: Optional[int] = None
    max_party_size: Optional[int] = None
    min_party_size: Optional[int] = None
    is_active: Optional[bool] = None
