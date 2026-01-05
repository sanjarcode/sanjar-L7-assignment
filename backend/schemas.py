from pydantic import BaseModel
from typing import List, Optional

# --- Base Schemas (Data only) ---

class GenreBase(BaseModel):
    name: str

class ActorBase(BaseModel):
    name: str

class DirectorBase(BaseModel):
    name: str

class MovieBase(BaseModel):
    title: str
    release_year: int

# --- Read Schemas (with IDs) ---

class Genre(GenreBase):
    id: int
    class Config:
        from_attributes = True

class ActorMinimal(ActorBase):
    id: int
    profile_url: Optional[str] = None
    class Config:
        from_attributes = True

class DirectorMinimal(DirectorBase):
    id: int
    profile_url: Optional[str] = None
    class Config:
        from_attributes = True

class MovieMinimal(MovieBase):
    id: int
    poster_url: Optional[str] = None
    class Config:
        from_attributes = True

# --- Detailed Schemas (with Relationships) ---

class Director(DirectorMinimal):
    movies: List[MovieMinimal] = []

class Actor(ActorMinimal):
    movies: List[MovieMinimal] = []

class Movie(MovieMinimal):
    director: Optional[DirectorMinimal] = None
    genres: List[Genre] = []
    actors: List[ActorMinimal] = []

# --- Action Schemas ---

class MovieCreate(MovieBase):
    director_name: str
    genre_names: List[str]
    actor_names: List[str]

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    release_year: Optional[int] = None
    director_id: Optional[int] = None
