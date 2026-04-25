import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, text
from alembic import context

# Importar configuración y metadatos
from app.core.config import settings
from app.models.base import Base 

# Cargar configuración de logs de alembic.ini
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
SCHEMA_NAME = settings.pg_schema

def run_migrations_offline() -> None:
    """Migraciones en modo offline."""
    url = settings.database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=SCHEMA_NAME,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Migraciones en modo online."""
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = settings.database_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # 1. Asegurar existencia del Mundo (Schema)
        connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}"))
        
        # --- SOLUCIÓN DE RAÍZ: Activar pgvector ---
        # Esto permite que PostgreSQL reconozca el tipo 'vector' 
        # antes de intentar crear las tablas de los agentes.
        # En env.py dentro de run_migrations_online
        connection.execute(text(f"CREATE EXTENSION IF NOT EXISTS vector SCHEMA {SCHEMA_NAME} CASCADE"))
        
        connection.execute(text(f"SET search_path TO {SCHEMA_NAME}"))
        connection.commit()

        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            version_table_schema=SCHEMA_NAME,
            include_schemas=True,
            # Filtro: Solo migrar objetos del esquema actual
            include_name=lambda name, type_, parent_names: 
                not (type_ == "schema" and name != SCHEMA_NAME)
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()