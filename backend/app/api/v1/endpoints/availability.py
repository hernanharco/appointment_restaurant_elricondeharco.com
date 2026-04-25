"""
API Router para la consulta de disponibilidad.
Este endpoint actúa como interfaz entre el Frontend (Astro) y nuestro motor de disponibilidad.
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.db.session import get_db
from app.services.capacity_service import CapacityService
from app.schemas.reservations import RestaurantAvailabilityResponse

router = APIRouter()


@router.get("/", response_model=RestaurantAvailabilityResponse)
def read_availability(
    *,
    db: Session = Depends(get_db),
    date: str = Query(
        ..., description="Fecha en formato YYYY-MM-DD", examples=["2026-02-25"]
    ),
    party_size: int = Query(..., description="Número de personas en la reserva"),
):
    """
    Endpoint para obtener los slots disponibles para reservas de restaurante.
    Calcula en tiempo real los huecos libres basado en la capacidad del restaurante.
    """
    # 1. Validación de entrada (Date Parsing)
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD"
        )

    # 2. Validación de party_size
    if party_size <= 0:
        raise HTTPException(
            status_code=400, detail="El tamaño del grupo debe ser mayor que 0"
        )

    # 3. Obtener disponibilidad usando CapacityService
    try:
        capacity_service = CapacityService(db)
        available_slots = capacity_service.get_available_slots(
            date=target_date, party_size=party_size
        )

        # 4. Construcción de respuesta
        return {
            "date": date,
            "party_size": party_size,
            "available_slots": available_slots,
            "total_slots": len(available_slots),
        }

    except Exception as e:
        # Aquí podrías usar un logger real como Loguru o Sentry en el futuro
        print(f"❌ Error en motor de disponibilidad: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error interno al calcular huecos disponibles"
        )
