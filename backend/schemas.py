from pydantic import BaseModel
from typing import List, Optional

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int
    class Config:
        from_attributes = True

class ActorBase(BaseModel):
    name: str

class ActorCreate(ActorBase):
    pass

class Actor(ActorBase):
    id: int
    class Config:
        from_attributes = True

class DirectorBase(BaseModel):
    name: str

class DirectorCreate(DirectorBase):
    pass

class Director(DirectorBase):
    id: int
    class Config:
        from_attributes = True

class MovieBase(BaseModel):
    title: str
    release_year: int

class MovieCreate(MovieBase):
    director_name: str
    genre_names: List[str]
    actor_names: List[str]

class Movie(MovieBase):
    id: int
    director: Optional[Director] = None
    genres: List[Genre] = []
    actors: List[Actor] = []

    class Config:
        from_attributes = True

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    release_year: Optional[int] = None
    director_id: Optional[int] = None
