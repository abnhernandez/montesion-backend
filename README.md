# Monte Sion Backend API

## Descripción

API backend de Python desarrollada con FastAPI, como proyecto para el Bootcamp de Backend con Python de Código Facilito. La aplicación está diseñada para proporcionar servicios de autenticación de usuarios y gestión de peticiones de oración, con la intención de ser utilizada en un futuro por la Iglesia Cristiana Monte Sion Oaxaca.

## Características Principales

- **Autenticación JWT**: Sistema completo de registro, login y gestión de usuarios
- **Gestión de Peticiones**: Sistema para crear y enviar peticiones de oración
- **Notificaciones por Email**: Confirmaciones automáticas y recuperación de contraseñas
- **Base de Datos PostgreSQL**: Persistencia de datos con SQLAlchemy
- **CORS Configurado**: Preparado para conexión con frontend
- **Zona Horaria**: Configurado para México (America/Mexico_City)

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para manejo de base de datos
- **PostgreSQL**: Base de datos relacional
- **JWT**: Autenticación con tokens
- **Passlib**: Hashing seguro de contraseñas
- **SMTP**: Envío de correos electrónicos
- **Uvicorn**: Servidor ASGI

## Estructura del Proyecto

```
montesion-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación principal y configuración
│   ├── db.py                # Configuración de base de datos
│   ├── models/              # Modelos de SQLAlchemy
│   │   ├── __init__.py
│   │   ├── user.py          # Modelo de usuario
│   │   └── peticion.py      # Modelo de petición
│   ├── schemas/             # Esquemas Pydantic
│   │   ├── __init__.py
│   │   ├── user_schema.py   # Esquemas de usuario
│   │   └── peticion_schema.py # Esquemas de petición
│   └── routers/             # Rutas de la API
│       ├── __init__.py
│       ├── auth_router.py   # Rutas de autenticación
│       └── peticion_router.py # Rutas de peticiones
├── requirements.txt         # Dependencias
├── start.sh                # Script de inicio
└── README.md               # Este archivo
```

## Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/abnhernandez/montesion-backend.git
cd montesion-backend
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
Crear un archivo `.env` con las siguientes variables:
```env
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_db
JWT_SECRET=tu_jwt_secret_key
EMAIL_REMITENTE=tu_email@gmail.com
EMAIL_PASSWORD=tu_app_password
PORT=8000
```

5. **Ejecutar la aplicación**
```bash
# Desarrollo
./start.sh

# O directamente con uvicorn
uvicorn app.main:app --reload
```

## Variables de Entorno Requeridas

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `DATABASE_URL` | URL de conexión a PostgreSQL | `postgresql://user:pass@host:5432/db` |
| `JWT_SECRET` | Clave secreta para JWT | `tu_clave_secreta_muy_segura` |
| `EMAIL_REMITENTE` | Email para envío de notificaciones | `iglesia@gmail.com` |
| `EMAIL_PASSWORD` | Contraseña de aplicación del email | `app_password_16_chars` |
| `PORT` | Puerto del servidor (requerido en Render) | `8000` |

## API Endpoints

### Autenticación (`/auth`)

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| `POST` | `/auth/register` | Registrar nuevo usuario | No |
| `POST` | `/auth/token` | Iniciar sesión (OAuth2) | No |
| `GET` | `/auth/auth` | Mensaje bíblico protegido | No |
| `POST` | `/auth/password-reset` | Recuperar contraseña | No |
| `PUT` | `/auth/update` | Actualizar perfil de usuario | Sí |
| `DELETE` | `/auth/delete` | Eliminar cuenta de usuario | Sí |

### Peticiones (`/peticiones`)

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| `POST` | `/peticiones/` | Crear nueva petición | No |
| `GET` | `/peticiones/` | Mensaje bíblico | No |

### Generales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Mensaje de bienvenida |
| `GET` | `/health` | Estado de salud de la API |

## Modelos de Datos

### Usuario (User)
```python
class User:
    id: int                    # ID único
    nombre: str               # Nombre del usuario
    apellido: str             # Apellido del usuario
    correo_electronico: str   # Email único
    hashed_password: str      # Contraseña hasheada
    telefono: str (opcional)  # Número de teléfono
    descripcion: str (opcional) # Descripción personal
    cumpleaños: date (opcional) # Fecha de nacimiento
    is_active: bool           # Estado activo (default: True)
```

### Petición (Peticion)
```python
class Peticion:
    id: int                   # ID único
    ticket: int               # Número de ticket único
    nombre: str               # Nombre del solicitante
    apellido: str (opcional)  # Apellido del solicitante
    correo_electronico: str   # Email del solicitante
    telefono: str (opcional)  # Teléfono del solicitante
    asunto: str               # Asunto de la petición
    peticion: str             # Contenido de la petición
    fecha: datetime           # Fecha y hora (zona México)
```

## Esquemas de Validación

### Usuarios
- **UserCreate**: Registro de usuario (nombre, apellido, email, password)
- **UserOut**: Respuesta pública del usuario (sin contraseña)
- **UserUpdate**: Actualización parcial de perfil
- **PasswordResetRequest**: Solicitud de recuperación de contraseña
- **UserDeleteRequest**: Confirmación para eliminar cuenta

### Peticiones
- **PeticionIn**: Datos de entrada (nombre, email, asunto, petición)
- **PeticionOut**: Respuesta completa con ticket e ID

## Funcionalidades Especiales

### Autenticación JWT
- Tokens con expiración de 7 días
- Middleware de CORS configurado para `https://montesion.me`, `http://127.0.0.1:8000` y `http://localhost:8000`
- Hashing seguro con bcrypt

### Sistema de Tickets
- Generación automática de números de ticket únicos
- Secuencia incremental basada en el último ticket

### Notificaciones por Email
- Confirmación automática de peticiones de oración
- Recuperación de contraseñas con contraseña temporal
- Plantillas HTML personalizadas para la iglesia

### Zona Horaria
- Todas las fechas se almacenan en zona horaria de México (CDMX)
- Configuración automática con `zoneinfo`

## Despliegue

### Render.com
El proyecto está configurado para desplegarse en Render:

```bash
# El script start.sh detecta automáticamente el entorno
# En producción (RENDER=true):
uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4

# En desarrollo:
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
```

### Docker (Opcional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["./start.sh"]
```

## Seguridad

- **Validación de entrada**: Todos los datos se validan con Pydantic
- **Hashing de contraseñas**: Bcrypt con salt automático
- **JWT seguro**: Tokens firmados con clave secreta
- **CORS restrictivo**: Solo permite origen específico
- **Validación de email**: Formato y existencia

## Logging y Monitoreo

- Logging configurado para errores de email
- Health check endpoint para monitoreo
- Manejo de excepciones en operaciones críticas

## Desarrollo

### Agregar nuevas rutas
1. Crear el router en `app/routers/`
2. Definir esquemas en `app/schemas/`
3. Crear modelos en `app/models/` si es necesario
4. Registrar el router en `app/main.py`

### Testing
```bash
# Instalar dependencias de desarrollo
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest
```

## Contribución

1. Fork del proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Soporte

Para reportar bugs o solicitar features, crear un issue en el repositorio.

## Licencia

Este proyecto fue desarrollado por **Abner** como parte del **Bootcamp de Backend con Python de Código Facilito**. Está destinado para uso futuro de la Iglesia Cristiana Monte Sion de Santa María Atzompa, Oaxaca.

**Autor**: Abner Daniel Hernández Ruiz
**Programa**: Bootcamp Backend con Python - Código Facilito  
**Propósito**: Proyecto educativo con aplicación real para Iglesia Cristiana Monte Sion

---

*Hagan lo que hagan, trabajen de buena gana, como para el Señor y no como para nadie en este mundo, conscientes de que el Señor los recompensará con la herencia. Ustedes sirven a Cristo el Señor.*  💖
**·**· Colosenses 3:23-24 NVI
