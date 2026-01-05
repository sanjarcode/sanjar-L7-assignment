from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Association Tables
movie_genres = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)

movie_actors = Table(
    "movie_actors",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("actor_id", Integer, ForeignKey("actors.id"), primary_key=True),
)

class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    profile_url = Column(String, nullable=True)

    movies = relationship("Movie", back_populates="director", lazy="selectin")

class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    profile_url = Column(String, nullable=True)

    movies = relationship("Movie", secondary=movie_actors, back_populates="actors", lazy="selectin")

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)

    movies = relationship("Movie", secondary=movie_genres, back_populates="genres", lazy="selectin")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    release_year = Column(Integer)
    poster_url = Column(String, nullable=True)
    director_id = Column(Integer, ForeignKey("directors.id"))

    director = relationship("Director", back_populates="movies", lazy="selectin")
    genres = relationship("Genre", secondary=movie_genres, back_populates="movies", lazy="selectin")
    actors = relationship("Actor", secondary=movie_actors, back_populates="movies", lazy="selectin")
