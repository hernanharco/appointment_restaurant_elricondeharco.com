#!/usr/bin/env python3
"""
Script para crear la configuración por defecto del restaurante.
Este script inserta un registro inicial en la tabla restaurant_config.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import sessionmaker
from app.db.session import engine
from app.models.restaurant_config import RestaurantConfig

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def create_default_config():
    """Crea la configuración por defecto del restaurante."""
    try:
        # Verificar si ya existe una configuración
        existing_config = db.query(RestaurantConfig).first()
        
        if existing_config:
            print("✅ Ya existe una configuración del restaurante:")
            print(f"   - ID: {existing_config.id}")
            print(f"   - Nombre: {existing_config.name}")
            print(f"   - Capacidad: {existing_config.max_capacity}")
            return
        
        # Crear configuración por defecto
        default_config = RestaurantConfig(
            name="Mi Restaurante",
            max_capacity=50,
            time_slot_duration_minutes=30,
            max_party_size=20,
            min_party_size=1,
            is_active=True
        )
        
        db.add(default_config)
        db.commit()
        db.refresh(default_config)
        
        print("✅ Configuración por defecto creada exitosamente:")
        print(f"   - ID: {default_config.id}")
        print(f"   - Nombre: {default_config.name}")
        print(f"   - Capacidad máxima: {default_config.max_capacity} personas")
        print(f"   - Duración de slot: {default_config.time_slot_duration_minutes} minutos")
        print(f"   - Tamaño de grupo: {default_config.min_party_size}-{default_config.max_party_size}")
        
    except Exception as e:
        print(f"❌ Error creando configuración por defecto: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_default_config()
