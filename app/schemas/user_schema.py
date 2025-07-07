from pydantic import BaseModel, EmailStr
from typing import Optional

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

class Token(BaseModel):
    access_token: str
    token_type: str
