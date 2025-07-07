#!/bin/bash

# Cargar variables de entorno si existe el archivo .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Usar el puerto proporcionado por Render o 8000 por defecto
PORT=${PORT:-10000}

# En producción, no usar --reload
if [ "$NODE_ENV" = "production" ] || [ "$RENDER" = "true" ]; then
    uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4
else
    uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
fi
