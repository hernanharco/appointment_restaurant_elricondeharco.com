# app/models/__init__.py
from .base import Base

# --- MODELOS DE RESTAURANTE ---
from .reservations import Reservation
from .restaurant_config import RestaurantConfig
from .business_hours import BusinessHours, TimeSlot
from .clients import Client
from .departments import Department
from .reminder import ScheduledReminder
from .metrics import ApiRouteMetric

# IMPORTANTE: Importamos el modelo de chat que está en la carpeta de agentes
from app.agents.memory.memory_models import ChatMessage

__all__ = [
    "Base",
    "BusinessHours",
    "TimeSlot",
    "Client",
    "Department",
    "Reservation",
    "RestaurantConfig",
    "ScheduledReminder",
    "ApiRouteMetric",
    "ChatMessage",
]
