from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.models.event import EventDB
from app.models.registration import Registration
from app.data.db import SessionDep
from app.models.user import UserDB
from app.test import EVENT

router = APIRouter(prefix="/registrations", tags=["registrations"])
#Router.get/registration unica API obbligatoria
@router.get("/") #lista di {username, event_id}
def get_registrations(
        session: SessionDep
        )->list[Registration]:
    """Return all registrations"""

    registrations = session.exec(select(Registration)).all()
    return registrations

#API opzionale

@router.delete("/")
def delete_registrations(username: str, event_id: int, session: SessionDep) ->dict:
    """"Delete registration"""

    event = session.get(EventDB, event_id)
    if event is None: raise HTTPException(status_code = 404, detail = "EVENTO NON TROVATO")

    user = session.get(UserDB, username)
    if user is None: raise HTTPException(status_code = 404, detail = "UTENTE NON TROVATO")

    registration = session.exec(
        select(Registration).where(
            Registration.username == username,
            Registration.event_id == event_id
            )
    ).first()

    if registration is None: raise HTTPException(status_code = 404, detail = "REGISTRAZIONE NON TROVATA")

    session.delete(registration)
    session.commit()

    return {"message" : "Registrazione eliminata con successo"}
