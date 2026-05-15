from datetime import datetime, date
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_

from app.models.reservations import Reservation, ReservationStatus
from app.models.clients import Client
from app.models.restaurant_config import RestaurantConfig
from app.schemas.reservations import ReservationCreate, ReservationRead, ReservationUpdate
from app.services.capacity_service import CapacityService


class ReservationService:
    """
    Servicio para gestionar reservas de restaurante.
    Reemplaza la lógica de AppointmentService para el sistema de restaurante.
    """

    def __init__(self, db: Session):
        self.db = db
        self.capacity_service = CapacityService(db)

    def create_reservation(self, reservation_data: ReservationCreate) -> ReservationRead:
        """
        Crea una nueva reserva validando capacidad y restricciones.
        """
        # Validar restricciones de capacidad
        is_valid, error_message = self.capacity_service.validate_reservation_constraints(
            reservation_data.party_size,
            reservation_data.start_time,
            reservation_data.end_time
        )
        
        if not is_valid:
            raise ValueError(error_message)

        # Verificar disponibilidad específica
        if not self.capacity_service.is_time_slot_available(
            reservation_data.start_time,
            reservation_data.end_time,
            reservation_data.party_size
        ):
            raise ValueError("No hay capacidad disponible para ese horario")

        # Buscar o crear cliente si viene con phone/email
        client = None
        if reservation_data.client_phone:
            client = self.db.query(Client).filter(
                Client.phone == reservation_data.client_phone
            ).first()

        # Crear la reserva
        reservation = Reservation(
            client_id=client.id if client else None,
            client_name=reservation_data.client_name,
            client_phone=reservation_data.client_phone,
            client_email=reservation_data.client_email,
            client_notes=reservation_data.client_notes,
            party_size=reservation_data.party_size,
            start_time=reservation_data.start_time,
            end_time=reservation_data.end_time,
            source=reservation_data.source or "manual",
            status=ReservationStatus.SCHEDULED
        )

        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)

        return self._to_read_model(reservation)

    def get_reservation_by_id(self, reservation_id: int) -> Optional[ReservationRead]:
        """Obtiene una reserva por su ID."""
        reservation = self.db.query(Reservation).options(
            joinedload(Reservation.client)
        ).filter(Reservation.id == reservation_id).first()
        
        if reservation:
            return self._to_read_model(reservation)
        return None

    def get_reservations_by_date(self, selected_date: date) -> List[ReservationRead]:
        """
        Obtiene todas las reservas para un día específico.
        """
        reservations = self.db.query(Reservation).options(
            joinedload(Reservation.client)
        ).filter(
            func.date(Reservation.start_time) == selected_date
        ).order_by(Reservation.start_time).all()

        return [self._to_read_model(reservation) for reservation in reservations]

    def update_reservation(
        self, 
        reservation_id: int, 
        update_data: ReservationUpdate
    ) -> Optional[ReservationRead]:
        """
        Actualiza una reserva existente.
        """
        reservation = self.db.query(Reservation).filter(
            Reservation.id == reservation_id
        ).first()

        if not reservation:
            return None

        # Si se está actualizando el horario o tamaño, validar capacidad
        update_dict = update_data.model_dump(exclude_unset=True)
        
        if any(key in update_dict for key in ['start_time', 'end_time', 'party_size']):
            new_start_time = update_dict.get('start_time', reservation.start_time)
            new_end_time = update_dict.get('end_time', reservation.end_time)
            new_party_size = update_dict.get('party_size', reservation.party_size)

            # Validar restricciones
            is_valid, error_message = self.capacity_service.validate_reservation_constraints(
                new_party_size, new_start_time, new_end_time
            )
            
            if not is_valid:
                raise ValueError(error_message)

            # Verificar disponibilidad (excluyendo esta reserva)
            if not self.capacity_service.is_time_slot_available(
                new_start_time, new_end_time, new_party_size, reservation_id
            ):
                raise ValueError("No hay capacidad disponible para ese horario")

        # Aplicar actualizaciones
        for field, value in update_dict.items():
            setattr(reservation, field, value)

        self.db.commit()
        self.db.refresh(reservation)

        return self._to_read_model(reservation)

    def cancel_reservation(self, reservation_id: int) -> bool:
        """
        Cancela una reserva.
        """
        reservation = self.db.query(Reservation).filter(
            Reservation.id == reservation_id
        ).first()

        if not reservation:
            return False

        reservation.status = ReservationStatus.CANCELLED
        self.db.commit()

        return True

    def confirm_reservation(self, reservation_id: int) -> bool:
        """
        Confirma una reserva.
        """
        reservation = self.db.query(Reservation).filter(
            Reservation.id == reservation_id,
            Reservation.status == ReservationStatus.SCHEDULED
        ).first()

        if not reservation:
            return False

        reservation.status = ReservationStatus.CONFIRMED
        self.db.commit()

        return True

    def get_client_reservations(self, client_id: int) -> List[ReservationRead]:
        """
        Obtiene todas las reservas de un cliente específico.
        """
        reservations = self.db.query(Reservation).options(
            joinedload(Reservation.client)
        ).filter(
            Reservation.client_id == client_id
        ).order_by(Reservation.start_time.desc()).all()

        return [self._to_read_model(reservation) for reservation in reservations]

    def get_reservations_by_phone(self, phone: str) -> List[ReservationRead]:
        """
        Busca reservas por número de teléfono del cliente.
        """
        reservations = self.db.query(Reservation).options(
            joinedload(Reservation.client)
        ).filter(
            Reservation.client_phone == phone
        ).order_by(Reservation.start_time.desc()).all()

        return [self._to_read_model(reservation) for reservation in reservations]

    def get_daily_capacity_summary(self, selected_date: date) -> dict:
        """
        Obtiene un resumen de capacidad para un día específico.
        """
        config = self.capacity_service.get_restaurant_config()
        if not config:
            return {}

        # Obtener reservas del día
        reservations = self.db.query(Reservation).filter(
            func.date(Reservation.start_time) == selected_date,
            Reservation.status.in_(['scheduled', 'confirmed', 'in_progress'])
        ).all()

        # Calcular ocupación por horas
        hourly_occupancy = {}
        for reservation in reservations:
            hour = reservation.start_time.hour
            if hour not in hourly_occupancy:
                hourly_occupancy[hour] = 0
            hourly_occupancy[hour] += reservation.party_size

        return {
            "date": selected_date.isoformat(),
            "max_capacity": config.max_capacity,
            "total_reservations": len(reservations),
            "total_people": sum(r.party_size for r in reservations),
            "hourly_occupancy": hourly_occupancy,
            "peak_hour": max(hourly_occupancy.items(), key=lambda x: x[1])[0] if hourly_occupancy else None
        }

    def get_history(
        self,
        page: int = 1,
        per_page: int = 50,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        status_filter: Optional[str] = None,
        search: Optional[str] = None,
    ) -> dict:
        """
        Obtiene historial paginado de reservas con filtros.
        """
        query = self.db.query(Reservation).options(joinedload(Reservation.client))

        # Filtro por rango de fechas
        if start_date:
            query = query.filter(func.date(Reservation.start_time) >= start_date)
        if end_date:
            query = query.filter(func.date(Reservation.start_time) <= end_date)

        # Filtro por estado (separado por comas: "scheduled,completed")
        if status_filter:
            statuses = [s.strip() for s in status_filter.split(",")]
            query = query.filter(Reservation.status.in_(statuses))

        # Filtro por búsqueda (nombre o teléfono)
        if search:
            pattern = f"%{search}%"
            query = query.filter(
                (Reservation.client_name.ilike(pattern)) |
                (Reservation.client_phone.ilike(pattern))
            )

        # Ordenar por fecha descendente
        query = query.order_by(Reservation.start_time.desc())

        # Paginación
        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()

        return {
            "items": [self._to_read_model(r) for r in items],
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": max(1, (total + per_page - 1) // per_page),
        }

    def get_stats(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> dict:
        """
        Obtiene estadísticas agregadas del historial de reservas.
        """
        query = self.db.query(Reservation)

        if start_date:
            query = query.filter(func.date(Reservation.start_time) >= start_date)
        if end_date:
            query = query.filter(func.date(Reservation.start_time) <= end_date)

        all_reservations = query.all()
        total = len(all_reservations)

        # Reservas activas vs canceladas
        completed = sum(1 for r in all_reservations if r.status == 'completed')
        cancelled = sum(1 for r in all_reservations if r.status == 'cancelled')
        scheduled = sum(1 for r in all_reservations if r.status == 'scheduled')
        confirmed = sum(1 for r in all_reservations if r.status == 'confirmed')
        no_show = sum(1 for r in all_reservations if r.status == 'no_show')

        # Personas totales
        total_people = sum(r.party_size for r in all_reservations) if all_reservations else 0
        avg_party = round(total_people / total, 1) if total > 0 else 0

        # Origen de reservas
        sources = {}
        for r in all_reservations:
            src = r.source or 'manual'
            sources[src] = sources.get(src, 0) + 1

        return {
            "total_reservations": total,
            "total_people": total_people,
            "avg_party_size": avg_party,
            "by_status": {
                "completed": completed,
                "cancelled": cancelled,
                "scheduled": scheduled,
                "confirmed": confirmed,
                "no_show": no_show,
            },
            "by_source": sources,
        }

    def _to_read_model(self, reservation: Reservation) -> ReservationRead:
        """
        Convierte un modelo Reservation a ReservationRead.
        """
        return ReservationRead(
            id=reservation.id,
            client_id=reservation.client_id,
            client_name=reservation.client_name,
            client_phone=reservation.client_phone,
            client_email=reservation.client_email,
            client_notes=reservation.client_notes,
            party_size=reservation.party_size,
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            status=reservation.status,
            created_at=reservation.created_at,
            updated_at=reservation.updated_at,
            source=reservation.source
        )
