from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.models.base import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)

    # 🎨 CAMBIO: Atributo para personalización visual
    # Usamos String(7) para guardar formatos '#RRGGBB'
    color = Column(String(7), nullable=False, server_default="#3B82F6")

    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # RELACIONES - Eliminadas relaciones con services y collaborators
    # En el sistema de restaurante, los departamentos pueden usarse para
    # categorizar áreas del restaurante (ej: terraza, interior, VIP)

    def __repr__(self):
        return f"<Department(id={self.id}, name='{self.name}', color='{self.color}')>"
