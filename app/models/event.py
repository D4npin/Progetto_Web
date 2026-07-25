from sqlmodel import SQLModel, Field
from datetime import datetime


class Event(SQLModel):  #Attributi comuni per tutte le classi

    title: str
    description: str
    date: datetime
    location: str


class EventCreate(Event): #Classe da utilizzare nelle POST

    pass


class EventPublic(Event): #Classe da utilizzare nelle GET

    id: int  #ID dell'evento


class EventDB(Event, table=True): #Collegamento tra codice e DB
    __tablename__ = "event" #Senza questo il DB assegnerebbe un nome automatico

    id: int = Field(default=None, primary_key=True)