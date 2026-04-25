from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.models.base import Base

class RestaurantConfig(Base):
    __tablename__ = "restaurant_config"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # --- CONFIGURACIÓN PRINCIPAL ---
    max_capacity = Column(Integer, nullable=False, comment="Capacidad máxima del restaurante")
    name = Column(String(100), nullable=False, default="Mi Restaurante")
    
    # --- CONFIGURACIÓN DE HORARIOS ---
    time_slot_duration_minutes = Column(Integer, nullable=False, default=30, comment="Duración de cada slot en minutos")
    
    # --- CONFIGURACIÓN DE RESERVAS ---
    max_party_size = Column(Integer, nullable=False, default=10, comment="Tamaño máximo de grupo permitido")
    min_party_size = Column(Integer, nullable=False, default=1, comment="Tamaño mínimo de grupo permitido")
    
    # --- ESTADO ---
    is_active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<RestaurantConfig(id={self.id}, name='{self.name}', max_capacity={self.max_capacity})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "max_capacity": self.max_capacity,
            "time_slot_duration_minutes": self.time_slot_duration_minutes,
            "max_party_size": self.max_party_size,
            "min_party_size": self.min_party_size,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
