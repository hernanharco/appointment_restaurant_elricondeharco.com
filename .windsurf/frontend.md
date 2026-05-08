# Frontend Documentation

## Overview
Frontend built with Astro 6.x + Svelte 5 (Runes) following atomic design patterns. Optimized for Vercel deployment with pnpm package management.

## Stack Tecnológico
- **Framework**: Astro 6.x
- **UI Framework**: Svelte 5 (Runes: $state, $derived, onclick)
- **Package Manager**: pnpm
- **Styling**: TailwindCSS
- **Deployment**: Vercel
- **TypeScript**: Full TypeScript support

## Estructura de Directorios

```
frontend/
├── .astro/              # Astro build cache
├── .vercel/             # Vercel deployment cache
├── dist/                # Build output
├── node_modules/        # Dependencies
├── public/              # Static assets
├── src/
│   ├── components/      # Componentes UI
│   ├── config/          # Configuración
│   ├── layouts/         # Layout components
│   ├── lib/             # Utilidades y helpers
│   ├── pages/           # Páginas Astro
│   ├── styles/          # Estilos globales
│   ├── types/           # Type definitions
│   ├── env.d.ts         # Environment types
│   └── middleware.ts    # Astro middleware
├── .dockerignore
├── .env
├── .gitignore
├── astro.config.mjs     # Astro configuration
├── package.json
├── pnpm-lock.yaml
├── setup.sh             # Setup script
└── tsconfig.json        # TypeScript configuration
```

## Componentes Principales

### src/components/
Componentes UI organizados siguiendo atomic design:
- **atoms/**: Elementos UI básicos (buttons, inputs)
- **molecules/**: Combinaciones de atoms (form fields, cards)
- **organisms/**: Estructuras complejas (headers, sections)
- **templates/**: Layout templates
- **pages/**: Páginas completas

### src/layouts/
Layout components de Astro:
- Base layout con estructura común
- Page-specific layouts

### src/lib/
Utilidades y helpers:
- API clients
- Formateadores
- Validadores
- Constants

### src/pages/
Páginas Astro con routing file-based.

### src/types/
TypeScript type definitions para:
- API responses
- Component props
- Domain models

### src/middleware.ts
Middleware de Astro para:
- Authentication
- Route protection
- Request handling

## Configuración

### Astro Configuration
`astro.config.mjs` incluye:
- Svelte integration
- TailwindCSS
- Vercel adapter
- TypeScript settings

### Environment Variables
`.env` para configuración de:
- API endpoints
- Feature flags
- Third-party services

### TypeScript
Configuración estricta en `tsconfig.json` con:
- Strict mode
- Path aliases
- Modern ES features

## Development Setup

```bash
# Instalar dependencias
pnpm install

# Setup script (auto-detecta entorno)
./setup.sh

# Desarrollo local
pnpm dev
```

## Build & Deploy

```bash
# Build para producción
pnpm build

# Preview local
pnpm preview

# Deploy a Vercel (automático con git push)
```

## Svelte 5 Runes

Uso de modern Svelte 5 features:
- `$state` para estado reactivo
- `$derived` para valores computados
- `onclick` y otros event handlers modernos
- Component-based architecture

## Styling

- **TailwindCSS**: Utility-first CSS
- **Component-scoped**: Estilos por componente
- **Responsive**: Mobile-first design
- **Theme system**: Variables CSS personalizadas

## Performance Optimizations

- Astro islands architecture
- Lazy loading de componentes
- Optimización de imágenes
- Bundle optimization

## Testing Setup

Configuración para testing con:
- Vitest para unit tests
- Playwright para E2E
- Component testing

## Security

- CSP headers configurados
- Input sanitization
- Authentication middleware
- Environment variable protection

## Authentication System

### Environment-Based Authentication
El sistema de autenticación es condicional según el entorno:

#### Development Mode (`ENVIRONMENT=development`)
- **Authentication disabled**: Acceso directo sin login
- **Mock user**: Usuario simulado con rol SUPERADMIN
- **Purpose**: Desarrollo rápido sin necesidad de servicio de auth

#### Production Mode (`ENVIRONMENT=production`)
- **OAuth with Google**: Flujo completo de autenticación
- **Role-based access**: Control por roles (SUPERADMIN, ADMIN, MANAGER)
- **JWT tokens**: Almacenamiento seguro en cookies HTTP-only
- **Route protection**: Middleware de protección de rutas

### Authentication Components

#### Files
- `src/middleware.ts` - Middleware de Astro para protección de rutas
- `src/pages/login.astro` - Página de login con OAuth Google
- `src/lib/api/auths.ts` - API client para autenticación
- `src/lib/stores/auth.ts` - Svelte store para estado de auth
- `src/pages/api/auth/` - API routes proxy para auth

#### Flow
1. **Development**: `pnpm dev` → Acceso directo → Mock user
2. **Production**: Visita → `/login` → OAuth Google → Token → Dashboard

#### Environment Variables
```bash
# Development
ENVIRONMENT=development

# Production  
ENVIRONMENT=production
PUBLIC_AUTH_API_URL=https://your-auth-api.com
```

## Restaurant Reservation System

### Adapted Components
El frontend fue adaptado de sistema de citas de barbería a reservas de restaurante:

#### Key Changes
- **AppointmentHeader.astro**: Estadísticas de restaurante (reservas, cubiertos, ocupación)
- **DaySchedule.svelte**: Muestra party_size en lugar de servicios
- **ReservationModal.svelte**: Formulario para reservas con capacidad y disponibilidad
- **API Service**: `src/services/api.js` para comunicación con backend

#### Data Model
- **Party size**: Número de personas en lugar de duración de servicio
- **Availability**: Verificación de capacidad del restaurante
- **Status types**: scheduled, confirmed, in_progress, completed, cancelled, no_show
- **Time slots**: Horarios de restaurante (8:00-20:00)

#### Backend Integration
- **Endpoint**: `/api/v1/reservations/` con CRUD completo
- **Availability**: `/api/v1/availability/` para consultar horarios disponibles
- **Clients**: `/api/v1/clients/` para gestión de clientes

### Component Architecture
```
src/components/appointment/
├── AppointmentHeader.astro    # Header con estadísticas
├── Appviewsday.svelte         # Selector de fechas
├── DaySchedule.svelte         # Horario diario con reservas
└── ReservationModal.svelte    # Modal para crear/editar reservas
```

### API Integration
- **Service**: `src/services/api.js` - Cliente HTTP para backend
- **Methods**: CRUD operations, availability checking, client management
- **Error handling**: Manejo de errores y loading states
