# schemas/peticion_schema.py
from pydantic import BaseModel, EmailStr, validator

class PeticionIn(BaseModel):
    nombre: str
    correo_electronico: EmailStr
    asunto: str
    peticion: str

    @validator("nombre", "asunto")
    def min_length_2(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("mínimo 2 caracteres")
        return v

    @validator("peticion")
    def min_length_10(cls, v):
        if len(v.strip()) < 10:
            raise ValueError("mínimo 10 caracteres")
        return v

class PeticionOut(BaseModel):
    id: int
    ticket: int
    nombre: str
    correo_electronico: EmailStr
    asunto: str
    peticion: str

    class Config:
        from_attributes = True