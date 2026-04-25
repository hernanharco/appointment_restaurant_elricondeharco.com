# Backend Documentation

## Overview
Backend built with Python + FastAPI using Poetry for dependency management. Follows clean architecture patterns with clear separation of concerns.

## Stack Tecnológico
- **Framework**: FastAPI
- **Dependency Management**: Poetry
- **Database**: PostgreSQL with Alembic migrations
- **Testing**: pytest
- **Containerization**: Docker
- **Language Graph**: LangGraph para agentes

## Estructura de Directorios

```
backend/
├── app/
│   ├── api/           # Endpoints y rutas HTTP
│   ├── core/          # Configuración central
│   ├── db/            # Configuración de base de datos
│   ├── main.py        # Entry point de la aplicación
│   ├── models/        # Modelos de base de datos
│   ├── schemas/       # Pydantic schemas para API
│   ├── services/      # Lógica de negocio
│   ├── utils/         # Utilidades compartidas
│   └── agents/        # (EXCLUIDO - ver agent.md)
├── migrations/        # Alembic migration files
├── scripts/           # Scripts de utilidad
├── tests/             # Test suite
├── .dockerignore
├── .env
├── .env.development
├── .gitignore
├── Dockerfile
├── alembic.ini
├── docker-compose.yml
├── langgraph.json
├── package.json
├── poetry.lock
├── pyproject.toml
└── test_flow.py
```

## Componentes Principales

### app/api/
Endpoints REST de la API. Organizados por dominio de negocio.

### app/core/
Configuración central incluyendo:
- Settings de aplicación
- Configuración de seguridad
- Variables de entorno

### app/db/
Configuración y conexión a PostgreSQL:
- Database session management
- Connection pooling

### app/models/
Modelos SQLAlchemy que representan tablas en la base de datos.

### app/schemas/
Modelos Pydantic para:
- Request/response validation
- Serialización de datos

### app/services/
Lógica de negocio pura, separada de la API:
- Domain services
- Business rules
- External integrations

### app/utils/
Funciones utilitarias reutilizables across modules.

## Configuración

### Environment Variables
- `.env` - Producción
- `.env.development` - Desarrollo

### Database
- PostgreSQL con soporte JSONB
- Alembic para migrations
- Multi-tenant architecture

### Testing
- pytest configuration
- Test coverage en `tests/`

## Deployment

### Docker
- `Dockerfile` optimizado para producción
- `docker-compose.yml` para desarrollo local

### Scripts
- Scripts automatizados en `scripts/`

## Regla de Actualización

**IMPORTANTE**: Al actualizar este archivo, incluir solo la información de la carpeta `backend` EXCLUYENDO el contenido de `app/agents`. La documentación de agentes se maneja en `agent.md`.

## Development Setup

```bash
# Instalar dependencias
poetry install

# Setup base de datos
alembic upgrade head

# Correr desarrollo
poetry run uvicorn app.main:app --reload
```

## Testing

```bash
# Correr tests
poetry run pytest

# Coverage
poetry run pytest --cov=app
```
