from pydantic import BaseModel, EmailStr, validator

class PeticionIn(BaseModel):
    ticket: int
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

    @validator("ticket")
    def positive_ticket(cls, v):
        if v <= 0:
            raise ValueError("El ticket debe ser un número positivo")
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
