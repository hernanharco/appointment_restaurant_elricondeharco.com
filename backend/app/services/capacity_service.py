from datetime import datetime, timedelta, time
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from app.models.reservations import Reservation
from app.models.restaurant_config import RestaurantConfig
from app.models.business_hours import BusinessHours
from app.schemas.reservations import AvailableTimeSlot, RestaurantAvailabilityResponse


class CapacityService:
    """
    Servicio para gestionar la capacidad y disponibilidad del restaurante.
    Reemplaza la lógica de disponibilidad basada en servicios/collaboradores
    por una lógica basada en aforo total del restaurante.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_restaurant_config(self) -> Optional[RestaurantConfig]:
        """Obtiene la configuración activa del restaurante"""
        return self.db.query(RestaurantConfig).filter(
            RestaurantConfig.is_active == True
        ).first()

    def calculate_current_capacity(
        self, 
        start_time: datetime, 
        end_time: datetime,
        exclude_reservation_id: Optional[int] = None
    ) -> int:
        """
        Calcula el total de personas reservadas en un bloque horario específico.
        
        Args:
            start_time: Inicio del bloque a verificar
            end_time: Fin del bloque a verificar
            exclude_reservation_id: ID de reserva a excluir (para updates)
            
        Returns:
            Total de personas ya reservadas en ese bloque
        """
        query = self.db.query(
            func.sum(Reservation.party_size).label('total_people')
        ).filter(
            # Reservas que se solapan con el bloque horario
            and_(
                Reservation.start_time < end_time,
                Reservation.end_time > start_time,
                # Solo reservas activas
                Reservation.status.in_(['scheduled', 'confirmed', 'in_progress'])
            )
        )

        # Excluir reserva específica (para cuando estamos actualizando)
        if exclude_reservation_id:
            query = query.filter(Reservation.id != exclude_reservation_id)

        result = query.first()
        return result.total_people or 0

    def is_time_slot_available(
        self, 
        start_time: datetime, 
        end_time: datetime, 
        party_size: int,
        exclude_reservation_id: Optional[int] = None
    ) -> bool:
        """
        Verifica si hay capacidad disponible para una reserva específica.
        
        Args:
            start_time: Inicio de la reserva
            end_time: Fin de la reserva  
            party_size: Número de personas
            exclude_reservation_id: ID de reserva a excluir
            
        Returns:
            True si hay capacidad, False si no
        """
        config = self.get_restaurant_config()
        if not config:
            return False

        current_capacity = self.calculate_current_capacity(
            start_time, end_time, exclude_reservation_id
        )
        
        return (current_capacity + party_size) <= config.max_capacity

    def get_available_time_slots(
        self, 
        date: datetime.date, 
        party_size: int
    ) -> List[AvailableTimeSlot]:
        """
        Genera los slots disponibles para una fecha y tamaño de grupo específicos.
        
        Args:
            date: Fecha para consultar disponibilidad
            party_size: Número de personas en la reserva
            
        Returns:
            Lista de slots disponibles
        """
        config = self.get_restaurant_config()
        if not config:
            return []

        # Obtener horarios de negocio para ese día
        weekday = date.weekday()
        opening_time, closing_time = self._get_day_hours(weekday)

        # Si no hay horarios configurados, usar defaults
        if opening_time is None or closing_time is None:
            opening_time, closing_time = self._default_business_hours(weekday)

        # Generar slots basados en la configuración
        slots = []
        slot_duration = timedelta(minutes=config.time_slot_duration_minutes)
        
        current_time = datetime.combine(date, opening_time)

        # Manejar cierre después de medianoche
        if closing_time <= opening_time:
            # Cierre al día siguiente — combinamos con día+1
            closing_dt = datetime.combine(date + timedelta(days=1), closing_time)
        else:
            closing_dt = datetime.combine(date, closing_time)

        while current_time + slot_duration <= closing_dt:
            slot_end = current_time + slot_duration
            
            # Verificar disponibilidad para este slot
            current_capacity = self.calculate_current_capacity(
                current_time, slot_end
            )
            available_capacity = config.max_capacity - current_capacity
            
            if available_capacity >= party_size:
                slots.append(AvailableTimeSlot(
                    start_time=current_time,
                    end_time=slot_end,
                    available_capacity=available_capacity,
                    total_capacity=config.max_capacity
                ))
            
            current_time += slot_duration

        return slots

    def get_restaurant_availability(
        self, 
        date: datetime.date, 
        party_size: int
    ) -> RestaurantAvailabilityResponse:
        """
        Obtiene la disponibilidad completa del restaurante para una fecha.
        
        Args:
            date: Fecha a consultar
            party_size: Tamaño del grupo
            
        Returns:
            Respuesta completa con disponibilidad
        """
        config = self.get_restaurant_config()
        if not config:
            raise ValueError("No hay configuración activa del restaurante")

        available_slots = self.get_available_time_slots(date, party_size)

        return RestaurantAvailabilityResponse(
            date=date.isoformat(),
            party_size=party_size,
            available_slots=available_slots,
            total_slots=len(available_slots),
            restaurant_config=config.to_dict()
        )

    def _get_day_hours(self, weekday: int) -> tuple[Optional[time], Optional[time]]:
        """
        Obtiene la hora de apertura y cierre para un día.
        Busca en time_slots asociados al BusinessHours del día.
        """
        business_hours = self.db.query(BusinessHours).filter(
            BusinessHours.day_of_week == weekday,
            BusinessHours.is_enabled == True
        ).first()

        if not business_hours:
            return None, None

        # Obtener el primer y último slot del día
        slots = business_hours.time_slots
        if not slots:
            return None, None

        opening = min(s.start_time for s in slots)
        closing = max(s.end_time for s in slots)
        return opening, closing

    def _default_business_hours(self, weekday: int) -> tuple[time, time]:
        """
        Devuelve horarios por defecto si no hay configuración en DB.
        Lunes a Viernes: 09:00-23:00, Sábado: 10:00-01:00, Domingo: 10:00-00:00
        """
        defaults = {
            0: (time(9, 0), time(23, 0)),   # Lunes
            1: (time(9, 0), time(23, 0)),   # Martes
            2: (time(9, 0), time(23, 0)),   # Miércoles
            3: (time(9, 0), time(23, 0)),   # Jueves
            4: (time(9, 0), time(23, 0)),   # Viernes
            5: (time(10, 0), time(1, 0)),   # Sábado (cierra a la 1 AM → día siguiente)
            6: (time(10, 0), time(0, 0)),   # Domingo
        }
        return defaults.get(weekday, (time(9, 0), time(23, 0)))

    def validate_reservation_constraints(
        self, 
        party_size: int, 
        start_time: datetime, 
        end_time: datetime
    ) -> tuple[bool, Optional[str]]:
        """
        Valida las restricciones de una reserva.
        
        Args:
            party_size: Número de personas
            start_time: Inicio de la reserva
            end_time: Fin de la reserva
            
        Returns:
            Tuple (is_valid, error_message)
        """
        config = self.get_restaurant_config()
        if not config:
            return False, "No hay configuración activa del restaurante"

        # Validar tamaño de grupo
        if party_size < config.min_party_size:
            return False, f"El tamaño mínimo de grupo es {config.min_party_size} personas"
        
        if party_size > config.max_party_size:
            return False, f"El tamaño máximo de grupo es {config.max_party_size} personas"

        # Validar que esté dentro de horarios de negocio
        weekday = start_time.weekday()
        opening_time, closing_time = self._get_day_hours(weekday)

        # Si no hay horarios configurados, usar defaults
        if opening_time is None or closing_time is None:
            opening_time, closing_time = self._default_business_hours(weekday)

        # Convertir a time objects para comparación
        reservation_start = start_time.time()
        reservation_end = end_time.time()

        # Manejar cierre después de medianoche (ej. Sábado cierra 01:00)
        if closing_time < opening_time:
            # El cierre es al día siguiente
            # Si la reserva empieza después de la medianoche y antes del cierre
            if reservation_start >= time(0, 0) and reservation_start < closing_time:
                pass  # Horario válido (post-medianoche)
            elif reservation_start < opening_time:
                return False, f"El restaurante abre a las {opening_time.strftime('%H:%M')}"
            elif reservation_start >= closing_time and reservation_start < opening_time:
                return False, f"El restaurante abre a las {opening_time.strftime('%H:%M')}"
        else:
            if reservation_start < opening_time:
                return False, f"El restaurante abre a las {opening_time.strftime('%H:%M')}"
            if reservation_end > closing_time:
                return False, f"El restaurante cierra a las {closing_time.strftime('%H:%M')}"

        # Validar duración mínima/máxima si es necesario
        reservation_duration = end_time - start_time
        min_duration = timedelta(minutes=30)  # Mínimo 30 minutos
        max_duration = timedelta(hours=4)    # Máximo 4 horas
        
        if reservation_duration < min_duration:
            return False, "La reserva debe ser de al menos 30 minutos"
        
        if reservation_duration > max_duration:
            return False, "La reserva no puede exceder las 4 horas"

        return True, None
