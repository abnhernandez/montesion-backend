from sqlalchemy import Column, Integer, String, DateTime
from app.db import Base
from datetime import datetime
from zoneinfo import ZoneInfo

cdmx_tz = ZoneInfo("America/Mexico_City")

class Peticion(Base):
    __tablename__ = "peticiones"

    id = Column(Integer, primary_key=True, index=True)
    ticket = Column(Integer, unique=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    apellido = Column(String, index=True, nullable=True)
    correo_electronico = Column(String, index=True, nullable=False)
    telefono = Column(String, nullable=True)
    asunto = Column(String, nullable=False)
    peticion = Column(String, nullable=False)
    fecha = Column(DateTime, default=lambda: datetime.now(cdmx_tz))