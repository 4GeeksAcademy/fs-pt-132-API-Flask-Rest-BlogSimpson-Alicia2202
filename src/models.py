from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    __tablename__="user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

# Favoritos (arriba porque es de asociación m-m),Episodios, Personajes y Localización

class Character(db.Model):
    __tablename__="character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    age: Mapped[int] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(String(10), nullable = False)
    occupation: Mapped[str] = mapped_column(String(50), nullable = False)
    portrait_path: Mapped[str] = mapped_column(Text, nullable = False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "occupation": self.occupation,
            "portrait_path": self.portrait_path
            
        }