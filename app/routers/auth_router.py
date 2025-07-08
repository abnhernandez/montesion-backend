from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt
import os
import secrets
import smtplib
from email.message import EmailMessage
import logging

from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserOut, Token, PasswordResetRequest, UserUpdate

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 días

# ----------- DB Dependency -----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------- Utilidades -----------
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_email(db: Session, correo_electronico: str):
    return db.query(User).filter(User.correo_electronico == correo_electronico).first()

def authenticate_user(db: Session, correo_electronico: str, password: str):
    user = get_user_by_email(db, correo_electronico)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# ----------- Registro -----------
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.correo_electronico)
    if existing_user:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    hashed_password = get_password_hash(user.password)
    db_user = User(
        nombre=user.nombre,
        apellido=user.apellido,
        correo_electronico=user.correo_electronico,
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ----------- Login -----------
@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    access_token = create_access_token(
        data={"sub": user.correo_electronico},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# ----------- Obtener Usuario Actual -----------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        correo_electronico = payload.get("sub")
        if correo_electronico is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = get_user_by_email(db, correo_electronico)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# ----------- Versículo Seguro (GET) -----------
@router.get("/auth")
def mensaje_biblico():
    return {
        "mensaje": "JUAN 10:28 RVR1960\n\nY yo les doy vida eterna; y no perecerán jamás, ni nadie las arrebatará de mi mano."
    }

# ----------- Recuperación de Contraseña -----------
@router.post("/password-reset")
def reset_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.correo_electronico)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    nueva_contraseña = secrets.token_urlsafe(10)
    hashed_password = get_password_hash(nueva_contraseña)
    user.hashed_password = hashed_password
    db.commit()

    remitente = os.getenv("EMAIL_REMITENTE")
    password = os.getenv("EMAIL_PASSWORD")

    mensaje = EmailMessage()
    mensaje["From"] = remitente
    mensaje["To"] = user.correo_electronico
    mensaje["Subject"] = "Recuperación de contraseña - Monte Sion"
    mensaje.set_content(f"""
Hola, {user.nombre} 👋

Has solicitado restablecer tu contraseña. Aquí tienes una nueva contraseña temporal:

Nueva contraseña: {nueva_contraseña}

Inicia sesión y cámbiala lo antes posible por seguridad.

---

Monte Sion – Santa María Atzompa
""")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(remitente, password)
            smtp.send_message(mensaje)
    except smtplib.SMTPException as e:
        logging.error("Error al enviar correo de recuperación: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error enviando correo")

    return {"mensaje": "Nueva contraseña enviada al correo electrónico registrado."}
# ----------- Actualizar Usuario -----------
@router.put("/update", response_model=UserOut)
def update_user(data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if data.nombre is not None:
        current_user.nombre = data.nombre
    if data.apellido is not None:
        current_user.apellido = data.apellido
    if data.correo_electronico is not None:
        current_user.correo_electronico = data.correo_electronico
    if data.telefono is not None:
        current_user.telefono = data.telefono
    if data.descripcion is not None:
        current_user.descripcion = data.descripcion
    if data.cumpleaños is not None:
        current_user.cumpleaños = data.cumpleaños

    db.commit()
    db.refresh(current_user)
    return current_user

    @router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        db.delete(current_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error eliminando la cuenta")
    return