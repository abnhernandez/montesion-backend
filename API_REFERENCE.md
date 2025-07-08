# API Reference - Monte Sion Backend

## Base URL
- **Desarrollo**: `http://localhost:8000`
- **Producción**: `https://montesion-backend.onrender.com`

## Autenticación

La API utiliza JWT (JSON Web Tokens) para autenticación. Los tokens deben incluirse en el header `Authorization` con el formato:

```
Authorization: Bearer {your_jwt_token}
```

**Duración del token**: 7 días  
**Algoritmo**: HS256

---

## Endpoints

### 🏠 General

#### GET `/`
Mensaje de bienvenida a la API.

**Respuesta:**
```json
{
  "mensaje": "Bienvenido a la API de Monte Sion"
}
```

#### GET `/health`
Verificación del estado de la API.

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "Monte Sion API"
}
```

---

### 🔐 Autenticación (`/auth`)

#### POST `/auth/register`
Registra un nuevo usuario en el sistema.

**Request Body:**
```json
{
  "nombre": "string",
  "apellido": "string", 
  "correo_electronico": "user@example.com",
  "password": "string"
}
```

**Respuesta 201:**
```json
{
  "id": 1,
  "nombre": "string",
  "apellido": "string",
  "correo_electronico": "user@example.com",
  "is_active": true
}
```

**Errores:**
- `400`: Email ya registrado
- `422`: Datos de validación incorrectos

---

#### POST `/auth/token`
Inicia sesión y obtiene un token JWT (OAuth2).

**Request Body (Form Data):**
```
username: user@example.com
password: your_password
```

**Headers:**
```
Content-Type: application/x-www-form-urlencoded
```

**Respuesta 200:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errores:**
- `401`: Credenciales inválidas

---

#### GET `/auth/auth`
Endpoint protegido que devuelve un mensaje bíblico.

**Respuesta 200:**
```json
{
  "mensaje": "JUAN 10:28 RVR1960\n\nY yo les doy vida eterna; y no perecerán jamás, ni nadie las arrebatará de mi mano."
}
```

---

#### POST `/auth/password-reset`
Solicita el restablecimiento de contraseña. Envía una nueva contraseña temporal por email.

**Request Body:**
```json
{
  "correo_electronico": "user@example.com"
}
```

**Respuesta 200:**
```json
{
  "mensaje": "Nueva contraseña enviada al correo electrónico registrado."
}
```

**Errores:**
- `404`: Usuario no encontrado
- `500`: Error enviando correo

---

#### PUT `/auth/update`
🔒 **Requiere autenticación**

Actualiza la información del perfil del usuario autenticado.

**Headers:**
```
Authorization: Bearer {token}
```

**Request Body (todos los campos son opcionales):**
```json
{
  "nombre": "string",
  "apellido": "string",
  "correo_electronico": "new@example.com",
  "telefono": "+52 951 123 4567",
  "descripcion": "string",
  "cumpleaños": "1990-12-25"
}
```

**Respuesta 200:**
```json
{
  "id": 1,
  "nombre": "string",
  "apellido": "string", 
  "correo_electronico": "new@example.com",
  "is_active": true
}
```

**Errores:**
- `401`: Token inválido
- `422`: Datos de validación incorrectos

---

#### DELETE `/auth/delete`
🔒 **Requiere autenticación**

Elimina permanentemente la cuenta del usuario autenticado.

**Headers:**
```
Authorization: Bearer {token}
```

**Respuesta 204:** No Content

**Errores:**
- `401`: Token inválido
- `500`: Error eliminando la cuenta

---

### 🙏 Peticiones de Oración (`/peticiones`)

#### POST `/peticiones/`
Crea una nueva petición de oración y envía confirmación por email.

**Request Body:**
```json
{
  "nombre": "string",
  "correo_electronico": "user@example.com",
  "asunto": "string",
  "peticion": "string"
}
```

**Validaciones:**
- `nombre`: Mínimo 2 caracteres
- `asunto`: Mínimo 2 caracteres  
- `peticion`: Mínimo 10 caracteres
- `correo_electronico`: Formato de email válido

**Respuesta 201:**
```json
{
  "id": 1,
  "ticket": 1001,
  "nombre": "string",
  "correo_electronico": "user@example.com",
  "asunto": "string",
  "peticion": "string"
}
```

**Errores:**
- `422`: Datos de validación incorrectos
- `500`: Error guardando la petición

**Nota:** Se enviará un email de confirmación automáticamente al correo proporcionado.

---

#### GET `/peticiones/`
Devuelve un mensaje bíblico relacionado con la oración.

**Respuesta 200:**
```json
{
  "mensaje": "Confesaos vuestras ofensas unos a otros, y orad unos por otros, para que seáis sanados. La oración eficaz del justo puede mucho. · Santiago 5:16 RVR1960"
}
```

---

## Códigos de Estado HTTP

| Código | Significado | Descripción |
|--------|-------------|-------------|
| 200 | OK | Petición exitosa |
| 201 | Created | Recurso creado exitosamente |
| 204 | No Content | Operación exitosa sin contenido |
| 400 | Bad Request | Error en la petición del cliente |
| 401 | Unauthorized | Autenticación requerida o fallida |
| 404 | Not Found | Recurso no encontrado |
| 422 | Unprocessable Entity | Error de validación de datos |
| 500 | Internal Server Error | Error interno del servidor |

## Ejemplos de Uso

### Registro y Login Completo

```bash
# 1. Registrar usuario
curl -X POST "https://api.montesion.com/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan",
    "apellido": "Pérez",
    "correo_electronico": "juan@example.com",
    "password": "micontraseña123"
  }'

# 2. Iniciar sesión
curl -X POST "https://api.montesion.com/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=juan@example.com&password=micontraseña123'

# Respuesta:
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer"
# }

# 3. Usar el token en requests posteriores
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X PUT "https://api.montesion.com/auth/update" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "telefono": "+52 951 123 4567",
    "descripcion": "Miembro activo de la iglesia"
  }'
```

### Crear Petición de Oración

```bash
curl -X POST "https://api.montesion.com/peticiones/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "María González",
    "correo_electronico": "maria@example.com",
    "asunto": "Oración por sanidad",
    "peticion": "Por favor oren por la recuperación de mi madre que está en el hospital. Necesitamos de sus oraciones en este momento difícil."
  }'

# Respuesta:
# {
#   "id": 15,
#   "ticket": 1015,
#   "nombre": "María González", 
#   "correo_electronico": "maria@example.com",
#   "asunto": "Oración por sanidad",
#   "peticion": "Por favor oren por la recuperación..."
# }
```

### JavaScript/Fetch Example

```javascript
// Registro de usuario
const registerUser = async () => {
  const response = await fetch('https://api.montesion.com/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      nombre: 'Ana',
      apellido: 'López',
      correo_electronico: 'ana@example.com',
      password: 'contraseña123'
    })
  });
  
  const user = await response.json();
  console.log('Usuario registrado:', user);
};

// Login y obtener token
const login = async () => {
  const formData = new FormData();
  formData.append('username', 'ana@example.com');
  formData.append('password', 'contraseña123');
  
  const response = await fetch('https://api.montesion.com/auth/token', {
    method: 'POST',
    body: formData
  });
  
  const tokenData = await response.json();
  localStorage.setItem('token', tokenData.access_token);
  return tokenData.access_token;
};

// Crear petición
const createPetition = async () => {
  const token = localStorage.getItem('token');
  
  const response = await fetch('https://api.montesion.com/peticiones/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // Nota: Las peticiones no requieren autenticación
    },
    body: JSON.stringify({
      nombre: 'Carlos Hernández',
      correo_electronico: 'carlos@example.com',
      asunto: 'Petición de trabajo',
      peticion: 'Oren por mí para encontrar un nuevo empleo que me permita proveer para mi familia.'
    })
  });
  
  const petition = await response.json();
  console.log('Petición creada:', petition);
};
```

## Rate Limiting y Límites

Actualmente no hay límites de rate implementados, pero se recomienda:

- **Registro**: Máximo 5 registros por IP por hora
- **Login**: Máximo 10 intentos por IP por hora  
- **Peticiones**: Máximo 3 peticiones por IP por hora
- **Recuperación de contraseña**: Máximo 1 por email por hora

## Soporte y Errores

Para reportar errores o solicitar soporte:

1. **Email**: soporte@montesion.me
2. **Issues**: GitHub repository
3. **Documentación**: Esta guía API

### Formato de Reporte de Error

```json
{
  "timestamp": "2025-07-07T12:00:00Z",
  "endpoint": "/auth/register",
  "method": "POST", 
  "status_code": 500,
  "error_message": "Error interno del servidor",
  "request_body": "{ datos enviados }",
  "user_agent": "Mozilla/5.0...",
  "ip_address": "192.168.1.1"
}
```

---

*Documentación actualizada: Julio 7, 2025*  
*Versión API: 1.0.0*
