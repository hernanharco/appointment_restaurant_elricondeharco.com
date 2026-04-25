#!/bin/bash

# setup.sh - Core Business (Frontend)
# Uso: ./setup.sh development | ./setup.sh production

# 1. Validar que se pase un argumento
if [ -z "$1" ]; then
    echo "❌ Error: Debes especificar el entorno."
    echo "Uso: ./setup.sh [development|production]"
    exit 1
fi

if [ "$1" == "development" ]; then
    echo "🚀 MODO DESARROLLO: Iniciando Astro + Svelte con HMR..."
    # Usamos pnpm como definiste en tu stack
    pnpm dev

elif [ "$1" == "production" ]; then
    echo "🐳 MODO PRODUCCIÓN: Validando con Docker (Entorno de Staging)..."
    
    # Intentar construir la imagen y detenerse si hay error (|| exit 1)
    # Esto evita que intentes correr un contenedor que no se creó
    docker build -t core-frontend-prod . || { echo "❌ Error en el build de Docker"; exit 1; }
    
    echo "✅ Build exitoso. Limpiando contenedores previos..."
    # Detenemos cualquier versión anterior que esté usando el mismo puerto
    docker stop core-frontend-staging 2>/dev/null || true
    
    echo "🌐 Servidor listo en http://localhost:4321"
    # Ejecutamos el contenedor:
    # --rm: se borra al cerrar (mantiene tu PC limpia)
    # --name: para identificarlo fácilmente
    docker run -it --rm --name core-frontend-staging -p 4321:4321 core-frontend-prod
else
    echo "❌ Opción no válida: $1"
    echo "Usa './setup.sh development' o './setup.sh production'"
    exit 1
fi