"""
Endpoint para horarios del restaurante (sin colaboradores).
Gestiona BusinessHours y TimeSlot a nivel global del restaurante.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import time
from pydantic import BaseModel, Field

from app.db.session import get_db
from app.models.business_hours import BusinessHours, TimeSlot

router = APIRouter()


# --- Schemas locales (simples, sin collaborator) ---
class TimeSlotSchema(BaseModel):
    start_time: str = Field(..., description="Formato HH:MM")
    end_time: str = Field(..., description="Formato HH:MM")
    slot_order: int = 1


class DayHoursSchema(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6)
    day_name: str
    is_enabled: bool = True
    is_split_shift: bool = False
    time_slots: List[TimeSlotSchema] = []


class BusinessHoursResponse(BaseModel):
    days: List[DayHoursSchema]


class BusinessHoursUpdate(BaseModel):
    days: List[DayHoursSchema]


# --- Endpoints ---

@router.get("/", response_model=BusinessHoursResponse)
def get_restaurant_hours(db: Session = Depends(get_db)):
    """Obtiene los horarios del restaurante (7 días)."""
    business_hours = (
        db.query(BusinessHours)
        .order_by(BusinessHours.day_of_week)
        .all()
    )

    days = []
    for bh in business_hours:
        bh.time_slots.sort(key=lambda x: x.start_time)
        days.append(
            DayHoursSchema(
                day_of_week=bh.day_of_week,
                day_name=bh.day_name,
                is_enabled=bh.is_enabled,
                is_split_shift=bh.is_split_shift,
                time_slots=[
                    TimeSlotSchema(
                        start_time=slot.start_time.strftime("%H:%M"),
                        end_time=slot.end_time.strftime("%H:%M"),
                        slot_order=slot.slot_order,
                    )
                    for slot in bh.time_slots
                ],
            )
        )

    return BusinessHoursResponse(days=days)


@router.put("/", status_code=status.HTTP_200_OK)
def update_restaurant_hours(
    payload: BusinessHoursUpdate, db: Session = Depends(get_db)
):
    """
    Actualiza los horarios del restaurante.
    Elimina todos los existentes y crea los nuevos (transacción atómica).
    """
    try:
        # Eliminar horarios existentes
        db.query(BusinessHours).delete(synchronize_session=False)

        # Insertar nuevos
        for day_data in payload.days:
            if not day_data.is_enabled:
                continue

            new_bh = BusinessHours(
                day_of_week=day_data.day_of_week,
                day_name=day_data.day_name,
                is_enabled=day_data.is_enabled,
                is_split_shift=day_data.is_split_shift,
            )
            db.add(new_bh)
            db.flush()

            for slot_data in day_data.time_slots:
                start_h, start_m = map(int, slot_data.start_time.split(":"))
                end_h, end_m = map(int, slot_data.end_time.split(":"))

                new_slot = TimeSlot(
                    start_time=time(start_h, start_m),
                    end_time=time(end_h, end_m),
                    slot_order=slot_data.slot_order,
                    business_hours_id=new_bh.id,
                )
                db.add(new_slot)

        db.commit()
        return {"status": "success", "message": "Horarios actualizados correctamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar horarios: {str(e)}",
        )
