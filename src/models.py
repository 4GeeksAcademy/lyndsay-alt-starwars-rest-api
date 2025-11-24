from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), default=True, nullable=False)

    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
        }


class People(db.Model):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    height: Mapped[str] = mapped_column(String(20), nullable=True)
    mass: Mapped[str] = mapped_column(String(20), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)

    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="people", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
        }


class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=True)
    population: Mapped[str] = mapped_column(String(120), nullable=True)
    terrain: Mapped[str] = mapped_column(String(120), nullable=True)
    diameter: Mapped[str] = mapped_column(String(50), nullable=True)
    rotation_period: Mapped[str] = mapped_column(String(50), nullable=True)
    orbital_period: Mapped[str] = mapped_column(String(50), nullable=True)

    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="planet", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "terrain": self.terrain,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
        }


class Favorite(db.Model):
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int | None] = mapped_column(
        ForeignKey("planet.id"), nullable=True)
    people_id: Mapped[int | None] = mapped_column(
        ForeignKey("people.id"), nullable=True)

    user: Mapped["User"] = relationship(back_populates="favorites")
    planet: Mapped["Planet"] = relationship(back_populates="favorites")
    people: Mapped["People"] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id,
            "planet": self.planet.serialize() if self.planet else None,
            "people": self.people.serialize() if self.people else None,
        }
