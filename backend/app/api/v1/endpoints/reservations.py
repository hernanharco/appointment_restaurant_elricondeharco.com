"""
API Router para la gestión de reservas de restaurante.
Este endpoint maneja el CRUD completo de reservas.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, date as date_class, timedelta
from typing import List, Optional

from app.db.session import get_db
from app.services.reservation_service import ReservationService
from app.schemas.reservations import (
    ReservationCreate, 
    ReservationRead, 
    ReservationUpdate,
    RestaurantAvailabilityResponse
)

router = APIRouter()


@router.post("/", response_model=ReservationRead, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reservation_data: ReservationCreate, 
    db: Session = Depends(get_db)
):
    """
    Crea una nueva reserva de restaurante.
    """
    try:
        service = ReservationService(db)
        return service.create_reservation(reservation_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error creando reserva: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al crear la reserva"
        )


@router.get("/", response_model=List[ReservationRead])
def get_reservations(
    date: Optional[str] = Query(None, description="Fecha en formato YYYY-MM-DD"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Obtiene lista de reservas.
    Si se proporciona fecha, filtra por ese día.
    """
    try:
        service = ReservationService(db)
        
        if date:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
            return service.get_reservations_by_date(target_date)
        else:
            # Si no hay fecha, devolver reservas de hoy en adelante
            today = date_class.today()
            all_reservations = []

            # Obtener reservas de los próximos 30 días
            for i in range(30):
                current_date = today + timedelta(days=i)
                day_reservations = service.get_reservations_by_date(current_date)
                all_reservations.extend(day_reservations)
            
            return all_reservations[skip:skip + limit]
            
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de fecha inválido. Use YYYY-MM-DD"
        )
    except Exception as e:
        print(f"Error obteniendo reservas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al obtener las reservas"
        )


@router.get("/{reservation_id}", response_model=ReservationRead)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una reserva específica por su ID.
    """
    try:
        service = ReservationService(db)
        reservation = service.get_reservation_by_id(reservation_id)
        
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        
        return reservation
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error obteniendo reserva: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al obtener la reserva"
        )


@router.put("/{reservation_id}", response_model=ReservationRead)
def update_reservation(
    reservation_id: int,
    reservation_update: ReservationUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza una reserva existente.
    """
    try:
        service = ReservationService(db)
        updated_reservation = service.update_reservation(reservation_id, reservation_update)
        
        if not updated_reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        
        return updated_reservation
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error actualizando reserva: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al actualizar la reserva"
        )


@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """
    Cancela una reserva (soft delete).
    """
    try:
        service = ReservationService(db)
        success = service.cancel_reservation(reservation_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        
        return {"message": "Reserva cancelada correctamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error cancelando reserva: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al cancelar la reserva"
        )


@router.post("/{reservation_id}/confirm")
def confirm_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """
    Confirma una reserva.
    """
    try:
        service = ReservationService(db)
        success = service.confirm_reservation(reservation_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada o no está en estado programado"
            )
        
        return {"message": "Reserva confirmada correctamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error confirmando reserva: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al confirmar la reserva"
        )


@router.get("/client/phone/{phone}", response_model=List[ReservationRead])
def get_reservations_by_phone(phone: str, db: Session = Depends(get_db)):
    """
    Obtiene todas las reservas de un cliente por su teléfono.
    """
    try:
        service = ReservationService(db)
        return service.get_reservations_by_phone(phone)
        
    except Exception as e:
        print(f"Error obteniendo reservas por teléfono: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al obtener las reservas"
        )


@router.get("/daily-summary/{date}")
def get_daily_summary(date: str, db: Session = Depends(get_db)):
    """
    Obtiene un resumen de ocupación para un día específico.
    """
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
        service = ReservationService(db)
        return service.get_daily_capacity_summary(target_date)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de fecha inválido. Use YYYY-MM-DD"
        )
    except Exception as e:
        print(f"Error obteniendo resumen diario: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al obtener el resumen"
        )
