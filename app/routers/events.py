from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select, delete
from app.data.db import SessionDep

from app.models.event import EventCreate, EventPublic, EventDB
from app.models.user import CreateUser, UserDB
from app.models.registration import Registration


router = APIRouter(prefix="/events", tags=["events"])

@router.get("/") #Get -> lista di tutti gli elementi
def get_all_events(session: SessionDep) -> list[EventPublic] :
    #con session: SessionDep stiamo creando una instanza di accesso al database
    """Return the list of all events."""
    events = session.exec(select(EventDB)).all()

    return events

@router.get("/{id}")
def get_event_by_id(session: SessionDep, id: int) -> EventPublic:
    """Return the event with the given id."""
    event=session.get(EventDB, id)
    # con events sto creando un oggetto che ha come caratteristiche la sessione dell'
    # evento e il suo iD

    if event is None: #utilizzare is none al posto di not event è più preciso in quanto
                      # questo oggetto è proprio l'assenza di risultato
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/")
def create_event(session: SessionDep, event: EventCreate):
    """Create a new event."""
    #In questo caso non ci serve -> EventPublic in quanto non ci serve restituire nulla
    event_entry = EventDB.model_validate(event)
    session.add(event_entry)
    session.commit()
    return event_entry

@router.put("/{id}")
def replace_event(session: SessionDep, id: int, new_event: EventCreate):
    """Replace the event with the given id."""

    event=session.get(EventDB, id)

    if event is None: raise HTTPException(status_code=404, detail="Event not found")

    event.title = new_event.title
    event.description = new_event.description
    event.location = new_event.location
    event.date = new_event.date

    session.add(event)
    session.commit()
    return event


@router.post ("/{id}/register") #Iscrive un utente (lo crea se non esiste)
                                #Evento inesistente ->404
                                #Evento duplicato-> mai 5XX
def register_to_event(id:int, session: SessionDep, user: CreateUser) ->Registration:
    """Register user to a new event, creating one if needed."""
    #Per prima cosa controlliamo se l'evento esiste, altrimenti 404 per evento non trovato
    event = session.get(EventDB, id)
    if event is None: raise HTTPException(status_code=404, detail="EVENTO NON TROVATO")

    #Primo caso: l'utente non c'è ancora, quindi lo creiamo
    existing_user = session.get(UserDB, user.username)

    if existing_user is None:
        user_entry = UserDB.model_validate(user)
        session.add(user_entry)
        session.commit()


    #Secondo caso: Utente già presente e registrato a questo evento, restituisco quindi
    #la registrazione esistente invece di crearne una nuova
    existing_registration = session.exec(
        select(Registration).where(
            Registration.username == user.username,
                        Registration.event_id == id
        )
    ).first()

    if existing_registration:
        return existing_registration

    #Creo e restituisco la nuova registrazione
    registration = Registration(
        username = user.username,
        event_id = id,
    )
    session.add(registration)
    session.commit()
    return registration




