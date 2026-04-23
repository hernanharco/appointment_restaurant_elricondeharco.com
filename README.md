# CoreAppointment - SaaS Modular de Agendamiento

Sistema completo de gestión de citas y agendamiento construido con arquitectura moderna full-stack. Diseñado para ser escalable, multi-tenant y optimizado para costos cloud.

## 🏗️ Arquitectura del Proyecto

```
CoreAppointment/
├── Backend-CoreAppointment/     # API FastAPI + PostgreSQL
└── frontend-SvelteAppointment/   # Frontend Astro + Svelte 5
```

## 🚀 Stack Tecnológico

### Frontend (SvelteAppointment)
- **Framework**: Astro 5.17.1 con Svelte 5.50.0 (Runes)
- **Estilos**: TailwindCSS 4.1.18 con Vite integration
- **UI Components**: Sistema de 74+ componentes reutilizables
- **Icons**: Lucide Svelte 0.563.0
- **Estado**: Svelte 5 Runes + Stores especializados
- **Deployment**: Vercel con analytics integrados
- **Package Manager**: pnpm con optimizaciones

### Backend (CoreAppointment)
- **Framework**: FastAPI 0.129.0 con Python 3.12+
- **Base de Datos**: Neon PostgreSQL serverless
- **ORM**: SQLAlchemy 2.0.46 con Alembic
- **Async**: Uvicorn 0.41.0
- **AI/Agentes**: LangGraph 1.0.9 + LangChain OpenAI
- **Dependency Management**: Poetry

## ⚡ Características Principales

- **🎯 Gestión Completa de Citas**: Creación, edición, eliminación con validación
- **👥 Gestión de Clientes**: Búsqueda por teléfono, historial, notas
- **📅 Calendario Inteligente**: Disponibilidad en tiempo real
- **🤖 IA Integrada**: Agentes de LangGraph para automatización
- **📱 Responsive Design**: Mobile-first con hooks personalizados
- **🔐 Seguridad**: CORS dinámico, validación, manejo seguro de secrets
- **📊 Optimización de Costos**: Reducción de consumo en Neon DB
- **♿ Accesibilidad**: A11y completo con ARIA y keyboard navigation

## 🛠️ Instalación y Desarrollo

### Prerrequisitos
- Node.js 18+
- Python 3.12+
- pnpm
- Poetry
- Cuenta Neon (PostgreSQL)

### Backend Setup
```bash
cd Backend-CoreAppointment
poetry install
cp .env.example .env  # Configurar variables
poetry run uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend-SvelteAppointment
pnpm install
pnpm dev
```

### Variables de Entorno Clave
```env
# Backend
DATABASE_URL=postgresql://...
ENVIRONMENT=development
SECRET_KEY=tu-secret-key

# Frontend
PUBLIC_API_URL=http://localhost:8000
```

## 📁 Estructura del Código

### Frontend Architecture
```
src/
├── components/
│   ├── ui/              # 74+ componentes reutilizables
│   └── appointment/     # Componentes de dominio
├── lib/
│   ├── state/           # Stores con Svelte 5 Runes
│   ├── api/             # Cliente API
│   └── utils.ts         # Utilidades (cn, createVariants)
└── types/               # Definiciones TypeScript
```

### Backend Architecture
```
app/
├── api/                 # Endpoints FastAPI
├── models/              # Modelos SQLAlchemy
├── services/            # Lógica de negocio
├── schemas/             # Pydantic schemas
├── agents/              # Agentes LangGraph
└── core/                # Configuración
```

## 🎨 Patrones de Diseño Implementados

### Componentes Reutilizables
- **Variant System**: `createVariants()` para componentes configurables
- **Tailwind Merge**: `cn()` utility para combinar clases
- **Type Safety**: TypeScript estricto en todo el frontend

### Estado Reactivo (Svelte 5)
- **$state**: Para datos locales reactivos
- **$derived**: Para valores computados
- **$effect**: Para side effects y cleanup
- **Stores**: Clases especializadas por dominio

### Backend Patterns
- **Repository Pattern**: Abstracción de datos
- **Service Layer**: Lógica de negocio separada
- **Dependency Injection**: Configuración modular
- **Background Tasks**: Procesamiento asíncrono

## 📊 Optimización y Performance

### Neon Database Optimization
- **Reducción de Costos**: 28.2 → ~5-10 CU-hrs
- **Connection Management**: Desactivación de SSE para idle state
- **Manual Refresh**: Sincronización explícita cuando se necesita

### Frontend Performance
- **SSR**: Server-side rendering con Astro
- **Code Splitting**: Vite optimization
- **Lazy Loading**: Componentes bajo demanda
- **Bundle Analysis**: Optimización de dependencias

## 🔧 Desarrollo Local

### Endpoints Disponibles
- **Frontend**: http://localhost:4321
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Scripts Útiles
```bash
# Backend
poetry run pytest          # Tests
poetry run alembic upgrade # Migraciones

# Frontend
pnpm build                 # Build producción
pnpm preview              # Preview build
```

## 🚀 Deployment

### Frontend (Vercel)
```bash
vercel --prod
```

### Backend (Hetzner + Dokploy)
- Docker containerizado
- Variables de entorno de producción
- SSL con Cloudflare
- Monitoreo con métricas integradas

## 📈 Métricas y Monitoreo

- **API Metrics**: Tiempo de respuesta, status codes
- **Database Performance**: Connection pooling, query optimization
- **Frontend Analytics**: Vercel web analytics
- **Error Tracking**: Logs estructurados y manejo de errores

## 🤝 Contribuir

1. Fork del proyecto
2. Feature branch (`git checkout -b feature/amazing-feature`)
3. Commit con mensajes convencionales
4. Push al branch
5. Pull Request con descripción técnica

## 📄 Licencia

Este proyecto es software propietario desarrollado para uso comercial.

---

**Desarrollado con ❤️ usando FastAPI, Astro, Svelte 5 y Neon PostgreSQL**
# appointment_restaurant_elricondeharco.com
# appointment_restaurant_elricondeharco.com
# appointment_restaurant_elricondeharco.com
