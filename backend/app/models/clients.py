# app/models/client.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, default=1)

    full_name = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # 🧠 ESTADO DE LA SESIÓN ACTUAL (Para la reserva que se está haciendo ahora)
    # Estos campos son volátiles: se usan mientras el cliente habla con la IA
    current_party_size = Column(
        Integer, nullable=True, comment="Tamaño de grupo actual en sesión"
    )

    source = Column(String, default="ia", nullable=False)

    # 📂 ALMACENAMIENTO FLEXIBLE (Aquí guardamos preferencias del cliente)
    # Guardaremos: {"preferred_party_sizes": [2, 4, 6], "favorite_times": ["19:00", "20:30"]}
    # Al usar JSONB en Neon, podemos hacer consultas rápidas sobre estas preferencias
    metadata_json = Column(JSONB, server_default="{}", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )

    # --- RELACIONES ---
    # Reservas históricas del cliente
    reservations = relationship("Reservation", back_populates="client")

    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.full_name}', phone='{self.phone}')>"
