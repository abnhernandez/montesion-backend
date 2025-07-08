# schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    nombre: str
    apellido: str
    correo_electronico: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    nombre: str
    apellido: str
    correo_electronico: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

class PasswordResetRequest(BaseModel):
    correo_electronico: EmailStr

class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    correo_electronico: Optional[EmailStr] = None
    telefono: Optional[str] = None
    descripcion: Optional[str] = None
    cumpleaños: Optional[date] = None

class UserDeleteRequest(BaseModel):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
