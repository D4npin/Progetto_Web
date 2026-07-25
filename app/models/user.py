#CLASSE PER "USER"
from sqlmodel import SQLModel, Field

class User(SQLModel): #la classe base dei modelli del database
    username: str
    name: str
    email: str

class CreateUser(User): #dati richiesti per creare un nuovo utente
    pass

class UserDB(User, table = True): #la classe che rappresenta la tabella del database
    __tablename__ = "user" #nome della classe nel database SQL
    username: str = Field(default=None, primary_key=True)

class UserPublic(User): #dati restituiti al client
    pass