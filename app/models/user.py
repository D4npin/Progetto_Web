#CLASSE PER "USER"
from sqlmodel import SQLModel, Field

class User(SQLModel): #la classe base che contiene i dati comuni a tutti i tipi di utente
    username: str
    name: str
    email: str

class CreateUser(User): #dati richiesti per creare un nuovo utente
    pass #serve per dire che non devo aggiungere altro alla classe, prende da "User"

class UserDB(User, table = True): #la classe che rappresenta la tabella del database
    __tablename__ = "user" #nome della tabella nel database SQL
    username: str = Field(default = None, primary_key = True)
#primary_key serve per identificare univocamente ogni utente e per non far esistere due righe con lo stesso username
class UserPublic(User): #dati restituiti dalle api al client
    pass