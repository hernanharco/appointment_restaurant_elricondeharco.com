"""
API Router para la configuración del restaurante.
Este endpoint maneja el CRUD de la configuración principal del negocio.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.models.restaurant_config import RestaurantConfig
from app.schemas.restaurant_config import (
    RestaurantConfigCreate, 
    RestaurantConfigRead, 
    RestaurantConfigUpdate
)

router = APIRouter()


@router.get("/", response_model=List[RestaurantConfigRead])
def get_restaurant_configs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtiene todas las configuraciones del restaurante.
    """
    try:
        configs = db.query(RestaurantConfig).offset(skip).limit(limit).all()
        return configs
    except Exception as e:
        print(f"Error obteniendo configuraciones: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al obtener las configuraciones"
        )


@router.get("/active", response_model=Optional[RestaurantConfigRead])
def get_active_restaurant_config(db: Session = Depends(get_db)):
    """
    Obtiene la configuración activa del restaurante.
    """
    try:
        config = db.query(RestaurantConfig).filter(RestaurantConfig.is_active == True).first()
        return config
    except Exception as e:
        print(f"Error obteniendo configuración activa: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al obtener la configuración activa"
        )


@router.post("/", response_model=RestaurantConfigRead, status_code=status.HTTP_201_CREATED)
def create_restaurant_config(
    config_data: RestaurantConfigCreate, 
    db: Session = Depends(get_db)
):
    """
    Crea una nueva configuración del restaurante.
    """
    try:
        # Si se marca como activa, desactivar las demás
        if config_data.is_active:
            db.query(RestaurantConfig).filter(RestaurantConfig.is_active == True).update({
                RestaurantConfig.is_active: False
            })
        
        db_config = RestaurantConfig(**config_data.model_dump())
        db.add(db_config)
        db.commit()
        db.refresh(db_config)
        return db_config
        
    except Exception as e:
        print(f"Error creando configuración: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al crear la configuración"
        )


@router.put("/{config_id}", response_model=RestaurantConfigRead)
def update_restaurant_config(
    config_id: int,
    config_update: RestaurantConfigUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza una configuración existente del restaurante.
    """
    try:
        db_config = db.query(RestaurantConfig).filter(RestaurantConfig.id == config_id).first()
        
        if not db_config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Configuración no encontrada"
            )
        
        # Si se marca como activa, desactivar las demás
        if config_update.is_active:
            db.query(RestaurantConfig).filter(
                RestaurantConfig.id != config_id,
                RestaurantConfig.is_active == True
            ).update({RestaurantConfig.is_active: False})
        
        # Actualizar solo los campos proporcionados
        update_data = config_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_config, field, value)
        
        db.commit()
        db.refresh(db_config)
        return db_config
        
    except Exception as e:
        print(f"Error actualizando configuración: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al actualizar la configuración"
        )


@router.delete("/{config_id}")
def delete_restaurant_config(config_id: int, db: Session = Depends(get_db)):
    """
    Elimina una configuración del restaurante (soft delete).
    """
    try:
        db_config = db.query(RestaurantConfig).filter(RestaurantConfig.id == config_id).first()
        
        if not db_config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Configuración no encontrada"
            )
        
        db_config.is_active = False
        db.commit()
        return {"message": "Configuración desactivada correctamente"}
        
    except Exception as e:
        print(f"Error eliminando configuración: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al eliminar la configuración"
        )
