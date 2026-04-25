from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field

class Settings(BaseSettings):
    """
    Configuración centralizada del SaaS.
    Mapea las variables del archivo .env a atributos de Python.
    """

    # --- Base de Datos (PostgreSQL Nativo en VPS) ---
    pg_host: str = Field(..., alias="PGHOST")
    pg_port: int = Field(5432, alias="PGPORT")
    pg_database: str = Field(..., alias="PGDATABASE")
    pg_user: str = Field(..., alias="PGUSER")
    pg_password: str = Field(..., alias="PGPASSWORD")
    pg_schema: str = Field("public", alias="PGSCHEMA")
    pg_sslmode: str = Field("disable", alias="PGSSLMODE")
    pg_channel_binding: str = Field("disable", alias="PGCHANNELBINDING")

    @computed_field
    @property
    def database_url(self) -> str:
        """
        URL de conexión para SQLAlchemy + Psycopg3.
        Inyecta automáticamente el search_path con soporte para extensiones.
        """
        return (
            f"postgresql+psycopg://{self.pg_user}:{self.pg_password}@"
            f"{self.pg_host}:{self.pg_port}/{self.pg_database}?"
            f"options=-csearch_path%3D{self.pg_schema},public&"
            f"sslmode={self.pg_sslmode}"
        )

    # --- OpenAI & Agentes ---
    OPENAI_API_KEY: str = ""
    NAME_IA: str = "Maria"
    USE_PERSISTENT_CHECKPOINTS: bool = False
    LANGGRAPH_DATABASE_URL: Optional[str] = None

    # --- Configuración del Negocio ---
    BUSINESS_NAME: str = "Default Business Name"
    TITLE_BACKEND: str = "authAppointment-Backend"
    NAME_DATABASE: str = "Default Database Name"

    # --- Entorno y Debug ---
    ENVIRONMENT: str = "development" 
    DEBUG: bool = True
    APP_TIMEZONE: str = "Europe/Madrid"

    # --- Seguridad & JWT ---
    SECRET_KEY: Optional[str] = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # --- API Prefix ---
    API_V1_STR: str = "/api/v1"

    # --- CORS Settings ---
    CORS_ORIGINS: str = "http://localhost:3000"

    # --- Integraciones Externas ---
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    WHATSAPP_TOKEN: str = ""
    PHONE_NUMBER_ID: str = ""
    TELEGRAM_BOT_NAME: str = ""
    TELEGRAM_TOKEN: str = ""

    # --- LangSmith (Tracing) ---
    LANGSMITH_TRACING: bool = False
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_PROJECT: str = ""

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

    @property
    def allow_origins(self) -> List[str]:
        if not self.CORS_ORIGINS:
            return []
        origins = [origin.strip().rstrip('/') for origin in self.CORS_ORIGINS.split(",")]
        return origins

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore",
        populate_by_name=True
    )

settings = Settings()