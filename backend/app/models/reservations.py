from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.models.base import Base

class ReservationStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

class ReservationSource(str, enum.Enum):
    IA = "ia"
    MANUAL = "manual"
    WEB = "web"

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="SET NULL"), nullable=True)
    
    # --- CAMBIO CLAVE: Eliminamos service_id y collaborator_id ---
    # Ya no necesitamos servicios ni colaboradores para reservas de restaurante
    
    client_name = Column(String(100), nullable=False)
    client_phone = Column(String(20), nullable=True)
    client_email = Column(String(255), nullable=True)
    client_notes = Column(Text, nullable=True)
    
    # --- NUEVO CAMPO: party_size ---
    party_size = Column(Integer, nullable=False, comment="Número de personas en la reserva")
    
    source = Column(
        String(50), 
        default="manual", 
        nullable=False, 
        comment="Origen: ia, manual o web"
    )
    
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.SCHEDULED, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # --- RELACIONES EXISTENTES ---    
    client = relationship("Client", back_populates="reservations")

    # --- RELACIÓN CON RECORDATORIOS ---
    reminders = relationship(
        "ScheduledReminder", 
        back_populates="reservation", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Reservation(id={self.id}, party_size={self.party_size}, source='{self.source}', status={self.status})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "client_name": self.client_name,
            "party_size": self.party_size,
            "source": self.source,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "status": self.status.value if self.status else None
        }
