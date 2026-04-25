# app/models/metrics.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.models.base import Base
from app.core.config import settings # Importamos settings

class ApiRouteMetric(Base):
    __tablename__ = "api_route_metrics"   
    
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer)
    process_time = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())