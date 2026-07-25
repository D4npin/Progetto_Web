from fastapi import APIRouter, HTTPException
from sqlmodel import select, delete           # delete: per cancellare più righe in un colpo

from app.models.user import UserDB, UserPublic, CreateUser
from app.data.db import SessionDep
from app.models.registration import Registration


# prefix: collocato a tutti i path del file
# tags: raggruppa queste API sotto un'unica sezione
router = APIRouter(prefix = "/users", tags = ["users"])


@router.get("")
def get_all_users(session: SessionDep) -> list[UserPublic]:
    """Returns a list of all users"""
    users = session.exec(select(UserDB)).all() #.all() prende tutte le righe
    return list(users)


@router.post("", status_code = 201)
def create_user(user: CreateUser, session: SessionDep) -> UserPublic:
    """Creates a new user"""
    # Controllo a monte: se lo username esiste già rispondo 409
    existing_user = session.exec(
        select(UserDB).where(UserDB.username == user.username)
    ).first()#cerca un eventuale utente già presente
    if existing_user is not None:
        raise HTTPException(status_code = 409, detail = "Username already taken")
    user_db = UserDB.model_validate(user)
    session.add(user_db)     # accoda l'oggetto alla sessione
    session.commit()         # scrive su database.db
    session.refresh(user_db)  # rilegge la riga salvata
    return user_db


@router.get("/{username}")
def get_user(username: str, session: SessionDep) -> UserPublic:
    """Returns a user"""
    user = session.exec(
        select(UserDB).where(UserDB.username == username)
    ).first()
    if user is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    return user


@router.delete("")
def delete_all_users(session: SessionDep) -> dict:
    """Deletes all users"""
    session.exec(delete(Registration))#elimino prima le registrazioni e poi gli utenti
    session.exec(delete(UserDB))
    session.commit()
    return {"message": "Utenti cancellati con successo"}


@router.delete("/{username}")
def delete_user(username: str, session: SessionDep) -> dict:
    """Deletes a user"""
    user = session.exec(
        select(UserDB).where(UserDB.username == username)
    ).first()
    if user is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    registrations = session.exec(
        select(Registration).where(Registration.username == username)
    ).all()
    for registration in registrations:
        session.delete(registration)
    session.delete(user)
    session.commit()
    return {"message": "Utente cancellato con successo"}