# Orquestador - Guía de Referencia

## Propósito
Este archivo sirve como guía central para saber qué documentación consultar según tus necesidades de desarrollo y mantenimiento del proyecto Appointment.

## Mapa de Documentación

### 🏗️ **backend.md** - Backend Core
**Cuándo consultar:**
- Desarrollo de APIs REST
- Configuración de base de datos
- Lógica de negocio (services)
- Models y schemas
- Setup de desarrollo backend
- Testing del backend

**Contenido principal:**
- Estructura FastAPI + Poetry
- Configuración PostgreSQL + Alembic
- Endpoints y servicios
- **NO incluye** agentes (ver agent.md)

---

### 🎨 **frontend.md** - Frontend Astro + Svelte
**Cuándo consultar:**
- Desarrollo de componentes UI
- Configuración Astro/Svelte
- Estilos con TailwindCSS
- Setup de desarrollo frontend
- Deploy en Vercel
- TypeScript configuration

**Contenido principal:**
- Astro 6.x + Svelte 5 (Runes)
- Atomic design patterns
- Componentes y layouts
- Build y deployment

---

### 🤖 **agent.md** - Sistema de Agentes
**Cuándo consultar:**
- Desarrollo de agentes LangGraph
- Configuración de LangSmith
- Sistema de memoria
- Tools y routing
- Niveles de agentes
- Debugging de agentes

**Contenido principal:**
- LangGraph + LangSmith
- Memory system persistente
- Nodos y routing
- Claude v1 + ChatGPT configs
- Tools integration

---

## Flujo de Trabajo por Tipo de Tarea

### 🚀 **Nuevo Desarrollo**
1. **Feature Backend** → `backend.md`
2. **Feature Frontend** → `frontend.md`
3. **Feature Agentes** → `agent.md`
4. **Full Stack** → Todos los anteriores según necesidad

### 🔧 **Mantenimiento**
1. **Bug Backend** → `backend.md`
2. **Bug Frontend** → `frontend.md`
3. **Bug Agentes** → `agent.md`
4. **Configuración** → Archivo específico del área

### 📚 **Onboarding**
1. **Stack completo** → Leer todos en orden: backend → frontend → agent
2. **Rol específico** → Enfocarse en el área correspondiente

### 🔄 **Actualización de Documentación**
- **backend.md** → Actualizar solo estructura backend (excluyendo agents)
- **frontend.md** → Actualizar solo estructura frontend
- **agent.md** → Actualizar solo sistema de agentes
- **orquestador.md** → Actualizar este mapa cuando cambie estructura

## Decisiones de Arquitectura

### Separación de Responsabilidades
- **Backend**: API REST, base de datos, lógica de negocio tradicional
- **Frontend**: UI/UX, routing cliente, estado del cliente
- **Agents**: Inteligencia artificial, automatización, procesos complejos

### Comunicación Entre Sistemas
- **Frontend ↔ Backend**: HTTP APIs (REST)
- **Backend ↔ Agents**: Llamadas internas al sistema de agentes
- **Agents ↔ External**: APIs externas via tools

## Regla de Oro

> **Un archivo, una responsabilidad** - Cada archivo de documentación maneja un dominio específico sin overlap. Si estás trabajando en algo que podría ir en múltiples archivos, pregúntate: ¿cuál es el dominio principal?

## Quick Reference

| Necesitas... | Archivo a consultar |
|-------------|-------------------|
| Crear API endpoint | `backend.md` |
| Crear componente UI | `frontend.md` |
| Crear nuevo agente | `agent.md` |
| Configurar database | `backend.md` |
| Deploy en Vercel | `frontend.md` |
| Debug de agentes | `agent.md` |
| Setup desarrollo | Archivo específico del área |
| Actualizar documentación | `orquestador.md` |

## Contacto y Soporte

Si tienes dudas sobre qué archivo consultar:
1. Revisa esta tabla primero
2. Si aún no estás seguro, tu caso de uso probablemente necesite múltiples archivos
3. Para cambios estructurales, actualiza `orquestador.md`

---

**Última actualización**: Creación inicial del sistema de documentación modular.
