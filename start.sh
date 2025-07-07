#!/bin/bash

# Cargar variables de entorno si existe el archivo .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Validar que $PORT esté definido (obligatorio en Render)
if [ -z "$PORT" ]; then
    echo "ERROR: La variable de entorno \$PORT no está definida."
    exit 1
fi

# En producción, no usar --reload
if [ "$NODE_ENV" = "production" ] || [ "$RENDER" = "true" ]; then
    uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4
else
    uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
fi
