from fastapi import APIRouter
from sqlmodel import select

from app.models.registration import Registration
from app.data.db import SessionDep


router = APIRouter(prefix="/registrations", tags=["registrations"])
#Router.get/registration unica API obbligatoria
@router.get("/") #lista di {username, event_id}
def get_registrations(
        session: SessionDep
        )->list[Registration]:
    """Return all registrations"""

    registrations = session.exec(select(Registration)).all()
    return registrations

