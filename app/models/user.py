from sqlalchemy import Column, Integer, String, Boolean, Date
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    correo_electronico = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    telefono = Column(String, nullable=True)
    descripcion = Column(String, nullable=True)
    cumpleaños = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)