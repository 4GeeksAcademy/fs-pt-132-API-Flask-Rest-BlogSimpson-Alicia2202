from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()
class Favorites(db.Model):
    __tablename__= "favorites"
    id: Mapped[int] = mapped_column(primary_key=True)
    # clavesforaneas
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable = False)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable = True)
    episode_id: Mapped[int] = mapped_column(ForeignKey("episode.id"), nullable = True)
    #relacion
    user: Mapped["User"] = relationship(back_populates = "favorites")
    character: Mapped["Character"] = relationship(back_populates = "favorites")
    episode: Mapped["Episode"] = relationship(back_populates = "favorites")

    def serialize(self):
        return{
            "id": self.id,
            "user": {
                "id": self.user.id
            },
            "character":{
                "id": self.character.id if self.character else None,
                "name": self.character.name if self.character else None,
                "age": self.character.age if self.character else None,
                "gender": self.character.gender if self.character else None,
                "occupation": self.character.occupation if self.character else None,
            },

            "episode": {
                "id": self.episode.id if self.episode else None,
                "name": self.episode.name if self.episode else None,
                "synopsis": self.episode.synopsis if self.episode else None
            }
        }



class User(db.Model):
    __tablename__="user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    #relacion
    favorites: Mapped[List["Favorites"]] = relationship(back_populates = "user", cascade="all, delete-orphan")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": [fav.serialize() for fav in self.favorites] if self.favorites else None
        
            # do not serialize the password, its a security breach
        }

# Favoritos (arriba porque es de asociación m-m),Episodios, Personajes

class Character(db.Model):
    __tablename__="character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    age: Mapped[int] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(String(10), nullable = False)
    occupation: Mapped[str] = mapped_column(String(50), nullable = False)
    #relacion
    favorites: Mapped[List["Favorites"]] = relationship(back_populates = "character", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "occupation": self.occupation,
            "favorites": [fav.serialize()for fav in self.favorites] if self.favorites else None
                     
        }
    
class Episode(db.Model):
    __tablename__="episode"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable = False, unique=True)
    synopsis: Mapped[str] = mapped_column(Text, nullable = False)
    #relacion
    favorites: Mapped[List["Favorites"]] = relationship(back_populates = "episode", cascade="all, delete-orphan")

    def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "sypnosis": self.synopsis,
                "favorites": [fav.serialize()for fav in self.favorites] if self.favorites else None                    
            }