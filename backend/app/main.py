import os
import sys
import time
from datetime import datetime
from contextlib import asynccontextmanager
from zoneinfo import ZoneInfo

import uvicorn
from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.db.session import SessionLocal, engine
from app.models import Base 
import app.models.metrics
import app.agents.memory.memory_models 
from app.api.v1.api_route import api_router
from app.models.metrics import ApiRouteMetric

# --- Lógica de Métricas (SRP) ---
def save_metric_task(path: str, method: str, status_code: int, process_time: float):
    db = SessionLocal()
    try:
        new_metric = ApiRouteMetric(
            path=path, method=method,
            status_code=status_code, process_time=process_time
        )
        db.add(new_metric)
        db.commit()
    except Exception as e:
        print(f"⚠️ Error guardando métricas: {e}")
    finally:
        db.close()

# --- Ciclo de Vida de la Aplicación ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 Starting FastAPI app: {settings.TITLE_BACKEND}")
    print(f"🛠️ Environment: {settings.ENVIRONMENT}")
    
    try:
        local_tz = ZoneInfo(settings.APP_TIMEZONE)
        print(f"🌍 Timezone: {local_tz} | 🕒 Local Time: {datetime.now(local_tz)}")
    except Exception as e:
        print(f"❌ Error de Timezone: {e}")

    # 1. Sincronización de Base de Datos (BLOQUEANTE)
    print(f"--- Verificando conexión a {settings.NAME_DATABASE} ---")
    try:
        with engine.begin() as conn:
            # A. Crear esquema
            if settings.pg_schema and settings.pg_schema != "public":
                print(f"🛠️ Asegurando esquema: {settings.pg_schema}")
                conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {settings.pg_schema}"))

            # B. PARCHE: pgvector + Search Path
            print(f"🧬 Configurando pgvector en: {settings.pg_schema}")
            conn.execute(text(f"CREATE EXTENSION IF NOT EXISTS vector SCHEMA {settings.pg_schema} CASCADE"))
            conn.execute(text(f"SET search_path TO {settings.pg_schema}, public"))

            # C. Crear tablas
            print("📑 Sincronizando tablas...")
            Base.metadata.create_all(bind=conn)
            print("✅ DB Sincronizada correctamente.")

    except Exception as e:
        print(f"❌ ERROR CRÍTICO EN DB: {str(e)}", file=sys.stderr)
        if settings.is_production:
            raise e 

    # 2. LangGraph Checkpointer
    from app.agents.routing.graph import graph
    if settings.USE_PERSISTENT_CHECKPOINTS and settings.LANGGRAPH_DATABASE_URL:
        from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
        async with AsyncPostgresSaver.from_conn_string(settings.LANGGRAPH_DATABASE_URL) as checkpointer:
            await checkpointer.setup()
            graph.checkpointer = checkpointer
            print("✅ LangGraph: PostgreSQL activo")
            yield
    else:
        from langgraph.checkpoint.memory import MemorySaver
        graph.checkpointer = MemorySaver()
        print("✅ LangGraph: MemorySaver activo")
        yield

    print("👋 Cerrando aplicación...")
    engine.dispose()

# --- Inicialización de FastAPI ---
app = FastAPI(
    title=settings.TITLE_BACKEND,
    lifespan=lifespan,
    debug=settings.DEBUG
)

# --- Middlewares ---

@app.middleware("http")
async def log_route_metrics(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    background_tasks = BackgroundTasks()
    background_tasks.add_task(
        save_metric_task,
        request.url.path, request.method,
        response.status_code, process_time
    )
    response.background = background_tasks
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Rutas de Utilidad (Fuera del prefijo v1) ---

@app.get("/")
async def root():
    return {"status": "online", "timestamp": datetime.now().isoformat()}

# PARCHE 1: Endpoint de Salud para el HealthStore del Frontend
@app.get("/health")
async def health_check():
    """
    Endpoint para que el frontend valide la conexión. 
    Se coloca fuera de v1 por compatibilidad con sistemas de monitoreo.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": settings.ENVIRONMENT
    }

# --- Inclusión de Rutas Principales ---
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    # PARCHE 2: Soporte para Proxies (Fundamental para Dokploy/HTTPS)
    # proxy_headers=True y forwarded_allow_ips='*' resuelven el error de "Unsafe attempt"
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        proxy_headers=True, 
        forwarded_allow_ips="*"
    )