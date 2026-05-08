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

## Restaurant Reservation API

### Reservation System
El backend incluye un sistema completo de reservas para restaurantes:

#### Key Endpoints
- **`/api/v1/reservations/`** - CRUD completo de reservas
- **`/api/v1/availability/`** - Consulta de disponibilidad por fecha y capacidad
- **`/api/v1/clients/`** - Gestión de clientes del restaurante
- **`/api/v1/business-hours/`** - Configuración de horarios de operación

#### Data Model
```python
# Reservation Model
class Reservation(Base):
    client_name: str          # Nombre del cliente
    party_size: int           # Número de personas (1-20)
    client_phone: str         # Teléfono opcional
    client_email: str         # Email opcional
    client_notes: str         # Notas especiales
    start_time: datetime      # Inicio de reserva
    end_time: datetime        # Fin de reserva
    status: ReservationStatus # scheduled, confirmed, in_progress, completed, cancelled, no_show
    source: str              # manual, ia, web
```

#### Status Types
- **scheduled**: Reserva programada (estado inicial)
- **confirmed**: Reserva confirmada
- **in_progress**: Cliente presente en restaurante
- **completed**: Reserva finalizada
- **cancelled**: Cancelada por cliente/restaurante
- **no_show**: Cliente no asistió

#### Availability System
- **Capacity checking**: Verificación de capacidad por horario
- **Time slots**: Generación de horarios disponibles (30 min intervals)
- **Party size validation**: Validación según capacidad del restaurante

#### Business Logic
- **ReservationService**: Lógica de negocio central
- **CapacityService**: Gestión de capacidad y disponibilidad
- **ClientService**: Gestión de clientes y búsqueda por teléfono

### Environment Configuration
```bash
# .env.development
ENVIRONMENT=development
DATABASE_URL=postgresql://user:pass@localhost/appointment_restaurant

# .env.production  
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@prod-db/appointment_restaurant
```

## Testing

```bash
# Correr tests
poetry run pytest

# Coverage
poetry run pytest --cov=app
```
