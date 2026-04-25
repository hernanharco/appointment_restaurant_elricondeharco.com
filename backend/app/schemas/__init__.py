# Importamos todos los esquemas para que estén disponibles cuando se importe este paquete
from .business_hours import (
    BusinessHoursCreate,
    BusinessHoursRead,
    BusinessHoursUpdate,
    TimeSlotCreate,
    TimeSlotRead,
    TimeSlotUpdate,
)

# --- SCHEMAS DE RESTAURANTE ---
from .reservations import (
    ReservationCreate,
    ReservationRead,
    ReservationUpdate,
    AvailableTimeSlot,
    RestaurantAvailabilityResponse,
    RestaurantConfigRead,
    RestaurantConfigUpdate,
)

__all__ = [
    "BusinessHoursCreate",
    "BusinessHoursRead",
    "BusinessHoursUpdate",
    "TimeSlotCreate",
    "TimeSlotRead",
    "TimeSlotUpdate",
    # --- RESTAURANTE ---
    "ReservationCreate",
    "ReservationRead",
    "ReservationUpdate",
    "AvailableTimeSlot",
    "RestaurantAvailabilityResponse",
    "RestaurantConfigRead",
    "RestaurantConfigUpdate",
]
