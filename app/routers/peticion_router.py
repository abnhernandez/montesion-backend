from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import logging
import os
import smtplib
from email.message import EmailMessage

from app.schemas.peticion_schema import PeticionIn, PeticionOut
from app.models.peticion import Peticion
from app.db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def enviar_correo_confirmacion(destinatario: str, nombre: str, mensaje_peticion: str, ticket: int) -> bool:
    remitente = os.getenv("EMAIL_REMITENTE")
    password = os.getenv("EMAIL_PASSWORD")

    mensaje = EmailMessage()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = f"Confirmación de petición de oración, {ticket}"
    mensaje["Reply-To"] = remitente
    mensaje.set_content(f"""
Hola, {nombre} 👋.

Gracias por enviar tu petición de oración. Estaremos orando por ti.

Tu petición:
{mensaje_peticion}

---

Dios te bendiga ✨.
El equipo de soporte y oración Monte Sion 💖
Declaración de privacidad: montesion/privacy
Iglesia Cristiana Monte Sion - Santa María Atzompa, Oaxaca, CP 71222

---

Nunca enviamos SPAM y nos ponemos en contacto contigo únicamente con información de confirmación o avisos que pensamos pueden interesarte.
Por favor no respondas a este correo.
Si tienes dudas, escríbenos a {remitente}
""")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(remitente, password)
            smtp.send_message(mensaje)
        logging.info("Correo enviado exitosamente a %s", destinatario)
        return True
    except smtplib.SMTPException as e:
        logging.error("Error enviando correo: %s", e, exc_info=True)
        return False

@router.post("/", response_model=PeticionOut)
def crear_peticion(peticion: PeticionIn, db: Session = Depends(get_db)):
    # Generar ticket único: máximo ticket actual + 1, o 1 si no hay ninguno
    ultimo_ticket = db.query(Peticion).order_by(Peticion.ticket.desc()).first()
    nuevo_ticket = 1 if not ultimo_ticket else ultimo_ticket.ticket + 1

    nueva_peticion = Peticion(
        ticket=nuevo_ticket,
        nombre=peticion.nombre.strip(),
        correo_electronico=peticion.correo_electronico.strip(),
        asunto=peticion.asunto.strip(),
        peticion=peticion.peticion.strip()
    )

    try:
        db.add(nueva_peticion)
        db.commit()
        db.refresh(nueva_peticion)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error guardando la petición")

    enviado = enviar_correo_confirmacion(
        destinatario=nueva_peticion.correo_electronico,
        nombre=nueva_peticion.nombre,
        mensaje_peticion=nueva_peticion.peticion,
        ticket=nueva_peticion.ticket
    )
    if not enviado:
        logging.warning("No se pudo enviar correo a %s", nueva_peticion.correo_electronico)

    return nueva_peticion

@router.get("/")
def mensaje_biblico():
    return {
        "mensaje": "Confesaos vuestras ofensas unos a otros, y orad unos por otros, para que seáis sanados. La oración eficaz del justo puede mucho. · Santiago 5:16 RVR1960"
    }