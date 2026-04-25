from sqlalchemy.ext.declarative import declarative_base, declared_attr
from app.core.config import settings

# La base de SQLAlchemy de siempre
Base = declarative_base()

class MultiTenantBase:
    """
    Clase Mixin para aplicar el esquema automáticamente a todos los modelos.
    """
    @declared_attr
    def __table_args__(cls):
        # Esto inyecta el esquema de forma dinámica a cada tabla hija
        return {"schema": settings.pg_schema}