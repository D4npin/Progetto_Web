#ROUTER DEDICATO AGLI UTENTI
from fastapi import APIRouter, HTTPException
from sqlmodel import select, delete           #delete: per cancellare più righe in un colpo

from app.models.user import UserDB, UserPublic, CreateUser
from app.data.db import SessionDep
from app.models.registration import Registration


#prefix: collocato a tutti i path del file
#tags: raggruppa queste API sotto un'unica sezione "users"
router = APIRouter(prefix = "/users", tags = ["users"])
#PARTE OBBLIGATORIA (2 get e 1 post)
@router.get("")
def get_all_users(session: SessionDep) -> list[UserPublic]:
    """Returns a list of all users"""
    users = session.exec(select(UserDB)).all() #.all() prende tutti i risultati trovati
    return list(users)#restituisce gli utenti sotto forma di lista


@router.post("", status_code = 201)
def create_user(user: CreateUser, session: SessionDep) -> UserPublic:
    """Creates a new user"""
    # Controllo prima se esiste già qualcuno con stesso username, se lo username esiste già rispondo 409
    existing_user = session.exec(
        select(UserDB).where(UserDB.username == user.username)
    ).first()#cerca un eventuale utente già presente .first() restituisce il primo utente trovato (se esiste)
    if existing_user is not None: #se lo username è già presente non possiamo creare un secondo utente con lo stesso username
        raise HTTPException(status_code = 409, detail = "Nome utente già in uso")
    user_db = UserDB.model_validate(user)
    session.add(user_db)     #salva user nel database trasformandolo in un oggetto
    session.commit()         #commit() rende effettive le modifiche nel database
    session.refresh(user_db)  #rilegge la riga appena salvata
    return user_db #restituisce l'utente appena creato


@router.get("/{username}")
def get_user(username: str, session: SessionDep) -> UserPublic:
    """Returns a user"""
    user = session.exec(
        select(UserDB).where(UserDB.username == username)
    ).first() #cerchiamo l'utente il cui username corrisponde a quello ricevuto
    if user is None: #se non si trova nessun utente viene restituito None
        raise HTTPException(status_code = 404, detail = "Utente non trovato")
    return user #se viene trovato l'utente lo restituiamo

#PARTE FACOLTATIVA (2 delete)
@router.delete("")
def delete_all_users(session: SessionDep) -> dict:
    """Deletes all users"""
    session.exec(delete(Registration)) #elimino prima le registrazioni
    session.exec(delete(UserDB)) #poi tutti gli utenti
    session.commit() #vengono confermate le cancellazioni
    return {"message": "Utenti cancellati con successo"} #messaggio di conferma


@router.delete("/{username}")
def delete_user(username: str, session: SessionDep) -> dict:
    """Deletes a user"""
    user = session.exec(
        select(UserDB).where(UserDB.username == username)
    ).first() #cerchiamo l'utente da cancellare
    if user is None:
        raise HTTPException(status_code = 404, detail = "Utente non trovato") #se non esiste non si può cancellare
    registrations = session.exec(
        select(Registration).where(Registration.username == username)
    ).all() #controlliamo a quali eventi è registrato l'utente prima di cancellarlo
    for registration in registrations:
        session.delete(registration) #quando non ci sono più registrazioni si elimina l'utente
    session.delete(user)
    session.commit() #tutte le cancellazioni sono definitive
    return {"message": "Utente cancellato con successo"} #messaggio di conferma